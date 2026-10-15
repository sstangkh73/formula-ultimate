"""Rotating ground contacts with brake rotors and stators (goal v2, pure Python).

Four corners are hung on the Work 160 deck, one at each end of both deck
sides. Each corner is a root-level assembly tagged
``[ground_propulsion, braking]`` with four ``func-leaf-mechanism-v2`` prisms
extruded outward along y (world frame, metres):

- axle: regular ``N_a``-gon with a flat face on top, its inner cap seated on
  the deck side face at mid thickness (``bonded`` to the deck);
- stator: a pentagon pad resting on the axle's flat top face (``bonded``),
  in the slab next to the deck, ``brake_gap_m`` from the rotor face;
- rotor: ``N_r``-gon disc with an axle bore, ``bonded`` to the wheel;
- wheel: even ``N_w``-gon disc with one vertex straight down and the same
  bore, joined to the axle by a ``bearing`` interface.

The bore is an ``N_a``-gon of apothem ``r_a + c`` whose face normals point at
the axle vertices: the static gap is ``c`` and, since the bore's inscribed
circle is larger than the axle's circumscribed circle, no rotation of the
wheel and rotor about the axle axis can reach the axle. The wheel and rotor
form one full-turn revolute motion per corner.

All wheels share one radius, drawn per vehicle with the wheel bottom vertices
below the deck bottom, so only the wheels lie in the ground band. Nothing here
models tyres, traction or braking torque; it is a representation gate only.
"""

from __future__ import annotations

import math
import random
from dataclasses import asdict, dataclass, replace
from typing import Any, Mapping, Sequence

import numpy as np

from .composition import LeafMaterial
from .leaf_geometry import placement_transforms
from .mechanisms import (
    DECK_ID,
    MECHANISM_LAYER_VERSION,
    MechanismAssembly,
    MechanismLayer,
    MechanismPart,
    _derived_seed,
    _loop_points,
    prism_program,
    prism_vertices,
    signed_area,
)


GROUND_CONTACT_VERSION = "func-ground-contacts-v1"
CORNER_FUNCTIONS = ("ground_propulsion", "braking")
CORNER_SUFFIX = "ground_propulsion_braking"
#: stator foot half-width as a fraction of the axle top face half-width
STATOR_FOOT_FRACTION = 0.8


@dataclass(frozen=True)
class GroundContactConfig:
    #: corner lines lie this far outside the deck core on both x ends
    line_offset_m: float = 0.06
    wheel_radius_m: tuple[float, float] = (0.22, 0.34)
    wheel_width_m: tuple[float, float] = (0.05, 0.09)
    wheel_sides: tuple[int, ...] = (16, 20, 24)
    axle_sides: tuple[int, ...] = (6, 8)
    axle_radius_m: tuple[float, float] = (0.010, 0.016)
    #: the axle stays this far inside the deck's top and bottom faces
    axle_seat_margin_m: float = 0.002
    bearing_clearance_m: float = 2.5e-5
    #: bore polygon sides; a multiple of every axle side count
    bore_sides: int = 48
    #: largest allowed gap between a bore vertex and the axle edge it faces
    max_bearing_vertex_gap_m: float = 7.5e-5
    stator_width_m: tuple[float, float] = (0.03, 0.05)
    stator_height_m: tuple[float, float] = (0.02, 0.035)
    stator_thickness_m: tuple[float, float] = (0.015, 0.03)
    #: gap between the deck side face and the stator
    stator_offset_m: float = 1e-3
    brake_gap_m: float = 5e-4
    rotor_thickness_m: tuple[float, float] = (0.006, 0.012)
    rotor_sides: tuple[int, ...] = (24, 32)
    rotor_radius_fraction: tuple[float, float] = (0.6, 0.8)
    axle_overhang_m: tuple[float, float] = (0.01, 0.03)
    #: minimum x gap between the front and rear wheels on one side
    wheel_spacing_gap_m: float = 0.05
    #: rotor and stator edges stay this far inside their partner outlines
    edge_margin_m: float = 5e-3
    ground_band_m: float = 1e-3


DEFAULT_GROUND_CONTACT_CONFIG = GroundContactConfig()


def ground_contact_config_record(config: GroundContactConfig = DEFAULT_GROUND_CONTACT_CONFIG) -> dict[str, Any]:
    return {"version": GROUND_CONTACT_VERSION,
            **{k: list(v) if isinstance(v, tuple) else v for k, v in asdict(config).items()}}


@dataclass(frozen=True)
class CornerGeometry:
    """Per-vehicle corner dimensions (metres); shared by all four corners."""

    wheel_radius: float
    wheel_width: float
    wheel_sides: int
    axle_sides: int
    axle_radius: float
    stator_width: float
    stator_height: float
    stator_thickness: float
    rotor_thickness: float
    rotor_sides: int
    rotor_radius: float
    axle_overhang: float


def regular_polygon(sides: int, radius: float, phase: float) -> list[list[float]]:
    """Counter-clockwise regular polygon (dx, dz) with a vertex at ``phase``."""

    return [[radius * math.cos(phase + 2 * math.pi * k / sides), radius * math.sin(phase + 2 * math.pi * k / sides)]
            for k in range(sides)]


def axle_profile(g: CornerGeometry) -> list[list[float]]:
    # Vertices at pi/2 +- pi/N: the top face is flat with normal +z.
    return regular_polygon(g.axle_sides, g.axle_radius, math.pi / 2 + math.pi / g.axle_sides)


def bore_profile(g: CornerGeometry, clearance: float, sides: int) -> list[list[float]]:
    # Apothem r_a + c (free rotation with gap >= c); ``sides`` is a multiple
    # of N_a and a bore vertex points at every axle vertex, so the vertex
    # samples of both meshes see the bearing contact.
    if sides % g.axle_sides:
        raise ValueError("bore sides must be a multiple of the axle sides")
    return regular_polygon(sides, (g.axle_radius + clearance) / math.cos(math.pi / sides),
                           math.pi / 2 + math.pi / g.axle_sides)


def wheel_profile(g: CornerGeometry) -> list[list[float]]:
    return regular_polygon(g.wheel_sides, g.wheel_radius, -math.pi / 2)


def rotor_profile(g: CornerGeometry) -> list[list[float]]:
    return regular_polygon(g.rotor_sides, g.rotor_radius, -math.pi / 2 + math.pi / g.rotor_sides)


def stator_profile(g: CornerGeometry) -> list[list[float]]:
    # The foot lies inside the axle's flat top face (so its vertices sample the
    # contact), then the pad widens above that face's plane.
    top = g.axle_radius * math.cos(math.pi / g.axle_sides)
    foot = STATOR_FOOT_FRACTION * g.axle_radius * math.sin(math.pi / g.axle_sides)
    w, h = g.stator_width / 2, g.stator_height
    return [[-foot, top], [foot, top], [w, top + 0.4 * h], [w, top + h], [-w, top + h], [-w, top + 0.4 * h]]


def _local(points: Sequence[Sequence[float]], side: int) -> list[list[float]]:
    """World (dx, dz) to local profile coordinates for an extrusion along side * y.

    Without a flip, ``placement_transforms("y")`` maps local (u, v, w) to world
    (u, w, -v); with a flip it maps to (u, -w, v). The result is made
    counter-clockwise.
    """

    local = [[float(dx), float(-dz if side > 0 else dz)] for dx, dz in points]
    return local if signed_area(local) > 0 else list(reversed(local))


def y_prism(part_id: str, role: str, outer: Sequence[Sequence[float]], length: float, x_c: float, z_c: float,
            y_start: float, side: int, holes: Sequence[Sequence[Sequence[float]]] = ()) -> dict[str, Any]:
    """A prism of world (dx, dz) profile about (x_c, z_c), from ``y_start`` outward along side * y."""

    placement = placement_transforms("y", side < 0, 0.0, [x_c, y_start, z_c])
    return prism_program(part_id, role, _local(outer, side), length, placement,
                         holes=[_local(h, side) for h in holes])


def draw_corner_geometry(seed: int, layer: MechanismLayer,
                         config: GroundContactConfig = DEFAULT_GROUND_CONTACT_CONFIG) -> CornerGeometry:
    rng = random.Random(_derived_seed(GROUND_CONTACT_VERSION, "corner", seed))
    b = layer.backbone
    span = (b.core_x1 - b.core_x0) + 2 * config.line_offset_m
    radius = min(rng.uniform(*config.wheel_radius_m), (span - config.wheel_spacing_gap_m) / 2)
    axle_max = min(config.axle_radius_m[1], b.thickness / 2 - config.axle_seat_margin_m)
    return CornerGeometry(
        wheel_radius=radius,
        wheel_width=rng.uniform(*config.wheel_width_m),
        wheel_sides=rng.choice(config.wheel_sides),
        axle_sides=rng.choice(config.axle_sides),
        axle_radius=rng.uniform(config.axle_radius_m[0], axle_max),
        stator_width=rng.uniform(*config.stator_width_m),
        stator_height=rng.uniform(*config.stator_height_m),
        stator_thickness=rng.uniform(*config.stator_thickness_m),
        rotor_thickness=rng.uniform(*config.rotor_thickness_m),
        rotor_sides=rng.choice(config.rotor_sides),
        rotor_radius=radius * rng.uniform(*config.rotor_radius_fraction),
        axle_overhang=rng.uniform(*config.axle_overhang_m),
    )


def _material(seed: int, part_id: str, catalogue: Sequence[LeafMaterial]) -> LeafMaterial:
    rng = random.Random(_derived_seed(MECHANISM_LAYER_VERSION, "material", seed, part_id))
    return rng.choice(list(catalogue))


def _assembly_index(assembly_id: str) -> int:
    return int(assembly_id[1:].split("-", 1)[0])


def corner_ids(index: int) -> dict[str, str]:
    assembly = f"m{index}-{CORNER_SUFFIX}"
    return {"assembly": assembly, "axle": assembly + ".axle", "stator": assembly + ".stator",
            "rotor": assembly + ".rotor", "wheel": assembly + ".wheel", "motion": assembly + ".spin"}


def add_ground_contacts(layer: MechanismLayer, seed: int, catalogue: Sequence[LeafMaterial],
                        config: GroundContactConfig = DEFAULT_GROUND_CONTACT_CONFIG) -> MechanismLayer:
    """The layer with four wheel-and-brake corners on the deck; deterministic per seed."""

    b = layer.backbone
    g = draw_corner_geometry(seed, layer, config)
    c = config.bearing_clearance_m
    z_c = b.z_top - b.thickness / 2
    stator_start = config.stator_offset_m
    rotor_start = stator_start + g.stator_thickness + config.brake_gap_m
    wheel_start = rotor_start + g.rotor_thickness
    axle_length = wheel_start + g.wheel_width + g.axle_overhang
    bore = bore_profile(g, c, config.bore_sides)
    first = 1 + max((_assembly_index(a.id) for a in layer.assemblies), default=-1)
    parts, assemblies, interfaces, motions = [], [], [], []
    corners = [(x, side) for x in (b.core_x0 - config.line_offset_m, b.core_x1 + config.line_offset_m)
               for side in (-1, 1)]
    for offset, (x_c, side) in enumerate(corners):
        ids = corner_ids(first + offset)
        face_y = b.y1 if side > 0 else b.y0

        def y_at(distance: float) -> float:
            return face_y + side * distance

        programs = {
            "axle": y_prism(ids["axle"], "axle", axle_profile(g), axle_length, x_c, z_c, face_y, side),
            "stator": y_prism(ids["stator"], "stator", stator_profile(g), g.stator_thickness, x_c, z_c,
                              y_at(stator_start), side),
            "rotor": y_prism(ids["rotor"], "rotor", rotor_profile(g), g.rotor_thickness, x_c, z_c,
                             y_at(rotor_start), side, holes=[bore]),
            "wheel": y_prism(ids["wheel"], "wheel", wheel_profile(g), g.wheel_width, x_c, z_c,
                             y_at(wheel_start), side, holes=[bore]),
        }
        for role in ("axle", "stator", "rotor", "wheel"):
            parts.append(MechanismPart(id=ids[role], parent=ids["assembly"], program=programs[role],
                                       material=_material(seed, ids[role], catalogue)))
        assemblies.append(MechanismAssembly(id=ids["assembly"],
                                            children=tuple(ids[r] for r in ("axle", "stator", "rotor", "wheel")),
                                            functions=CORNER_FUNCTIONS))
        interfaces.extend([
            {"id": ids["axle"] + ".seat", "a": ids["axle"], "b": DECK_ID, "kind": "bonded"},
            {"id": ids["stator"] + ".seat", "a": ids["stator"], "b": ids["axle"], "kind": "bonded"},
            {"id": ids["wheel"] + ".bearing", "a": ids["wheel"], "b": ids["axle"], "kind": "bearing"},
            {"id": ids["rotor"] + ".hub", "a": ids["rotor"], "b": ids["wheel"], "kind": "bonded"},
        ])
        motions.append({"id": ids["motion"], "parts": [ids["wheel"], ids["rotor"]], "type": "revolute",
                        "axis_point_m": [float(x_c), float(face_y), float(z_c)],
                        "axis_dir": [0.0, float(side), 0.0], "range_rad": 2 * math.pi})
    lead = corner_ids(first)
    evidence = dict(layer.evidence)
    evidence["ground_propulsion"] = {"motions": [m["id"] for m in motions]}
    evidence["braking"] = {"rotor_motion": lead["motion"], "stator": lead["stator"]}
    return replace(layer, parts=layer.parts + tuple(parts), assemblies=layer.assemblies + tuple(assemblies),
                   root_children=layer.root_children + tuple(a.id for a in assemblies),
                   interfaces=layer.interfaces + tuple(interfaces), motions=layer.motions + tuple(motions),
                   evidence=evidence)


# --------------------------------------------------------------------------
# Re-check from the programs
# --------------------------------------------------------------------------

def _polygon_radii(points: Sequence[Sequence[float]]) -> tuple[float, float]:
    """(apothem, circumradius) of a centred convex polygon."""

    pts = np.asarray(points, dtype=float)
    circum = float(np.linalg.norm(pts, axis=1).max())
    apothem = math.inf
    for a, b in zip(pts, np.roll(pts, -1, axis=0)):
        edge = b - a
        apothem = min(apothem, abs(float(a[0] * edge[1] - a[1] * edge[0])) / float(np.linalg.norm(edge)))
    return apothem, circum


def ground_contact_problems(layer: MechanismLayer,
                            config: GroundContactConfig = DEFAULT_GROUND_CONTACT_CONFIG) -> list[str]:
    """Every violated ground-contact rule, recomputed from the program vertices."""

    problems: list[str] = []
    programs = {p.id: p.program for p in layer.parts}
    verts = {pid: prism_vertices(program) for pid, program in programs.items()}
    corners = [a for a in layer.assemblies if a.id.endswith("-" + CORNER_SUFFIX)]
    if len(corners) != 4:
        return [f"expected 4 ground-contact corners, found {len(corners)}"]
    b = layer.backbone
    wheels = [a.id + ".wheel" for a in corners]
    lowest = min(float(v[:, 2].min()) for v in verts.values())
    band_top = lowest + config.ground_band_m
    for pid, v in verts.items():
        low = v[v[:, 2] <= band_top]
        if pid not in wheels and len(low):
            problems.append(f"{pid} reaches the ground band")
    for wheel in wheels:
        if float(verts[wheel][:, 2].min()) > lowest + 1e-9:
            problems.append(f"{wheel} does not reach the lowest height")
    motions = {m["id"]: m for m in layer.motions}
    kinds = {(i["a"], i["b"]): i["kind"] for i in layer.interfaces}
    for corner in corners:
        ids = corner_ids(_assembly_index(corner.id))
        motion = motions.get(ids["motion"])
        if motion is None or set(motion["parts"]) != {ids["wheel"], ids["rotor"]} or motion["type"] != "revolute":
            problems.append(f"{corner.id}: missing wheel-and-rotor revolute motion")
            continue
        if kinds.get((ids["wheel"], ids["axle"])) != "bearing":
            problems.append(f"{corner.id}: no wheel-axle bearing")
        axle_loops = programs[ids["axle"]]["profile"]["loops"]
        _, axle_circum = _polygon_radii(_loop_points(axle_loops[0]))
        for role in ("wheel", "rotor"):
            loops = programs[ids[role]]["profile"]["loops"]
            if len(loops) != 2:
                problems.append(f"{ids[role]}: needs exactly one bore")
                continue
            bore = _loop_points(loops[1])
            bore_apothem, _ = _polygon_radii(bore)
            if not bore_apothem > axle_circum:
                problems.append(f"{ids[role]}: bore does not clear the rotating axle")
            pairs = np.linalg.norm(np.asarray(_loop_points(axle_loops[0]))[:, None, :]
                                   - np.asarray(bore)[None, :, :], axis=2)
            if float(pairs.min(axis=1).max()) > config.max_bearing_vertex_gap_m:
                problems.append(f"{ids[role]}: no bore vertex faces each axle edge closely")
        stator, rotor = verts[ids["stator"]], verts[ids["rotor"]]
        side = 1.0 if motion["axis_dir"][1] > 0 else -1.0
        gap = float((rotor[:, 1] * side).min() - (stator[:, 1] * side).max())
        if not 0 < gap <= 2e-3:
            problems.append(f"{corner.id}: stator-rotor gap {gap:.3e} m outside (0, 2e-3]")
        axis = np.array([motion["axis_point_m"][0], motion["axis_point_m"][2]])
        rotor_apothem, _ = _polygon_radii(_loop_points(programs[ids["rotor"]]["profile"]["loops"][0]))
        reach = float(np.linalg.norm(stator[:, [0, 2]] - axis, axis=1).max())
        if reach > rotor_apothem - config.edge_margin_m:
            problems.append(f"{corner.id}: stator is not inside the rotor face")
        axle = verts[ids["axle"]]
        foot = stator[np.abs(stator[:, 2] - float(axle[:, 2].max())) <= 1e-9]
        top = axle[np.abs(axle[:, 2] - float(axle[:, 2].max())) <= 1e-9]
        if (len(foot) == 0 or float(stator[:, 2].min()) < float(axle[:, 2].max()) - 1e-9
                or foot[:, 0].min() < top[:, 0].min() or foot[:, 0].max() > top[:, 0].max()):
            problems.append(f"{corner.id}: stator foot does not rest inside the axle's top face")
        seat = axle[np.abs(axle[:, 1] - (b.y1 if side > 0 else b.y0)) <= 1e-9]
        if (len(seat) == 0 or seat[:, 0].min() < b.x0 + b.chamfer or seat[:, 0].max() > b.x1 - b.chamfer
                or seat[:, 2].min() < b.z_top - b.thickness or seat[:, 2].max() > b.z_top):
            problems.append(f"{corner.id}: axle cap is not seated on the deck side face")
    ground = layer.evidence.get("ground_propulsion", {}).get("motions", [])
    if sorted(ground) != sorted(corner_ids(_assembly_index(a.id))["motion"] for a in corners):
        problems.append("ground_propulsion evidence does not list the corner motions")
    return problems
