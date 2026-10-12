"""Direction control: a steering post and a swinging arm on the deck (goal v2, pure Python).

One root-level assembly ``m<k>-direction_control`` tagged
``[direction_control]`` sits on the Work 160 deck top at the +x end of the
reserved bay. It has three ``func-leaf-mechanism-v2`` prisms extruded along
+z (world frame, metres):

- boss: regular ``N_b``-gon plate on the deck top (``bonded`` to the deck);
- post: regular ``N_p``-gon prism standing on the boss top (``bonded``);
- arm: a convex lever plate (convex hull of a hub polygon and a tip polygon)
  with a bore around the post, floating ``c`` above the boss top and joined
  to the post by a ``bearing`` interface.

The bore is a ``bore_sides``-gon of apothem ``r_p + c`` with a vertex in the
direction of every post vertex: the static gap is ``c``, the vertex samples of
both meshes see the bearing contact, and since the bore's inscribed circle is
larger than the post's circumscribed circle no rotation about the post axis
reaches the post. The arm forms one revolute motion about +z with a drawn
range; its full sweep circle stays inside the bay and the deck footprint, so
it clears the cluster and the wheels.

The steering axis is vertical while every ground-contact axis lies along y.
Nothing here links the arm to the wheels or models steering geometry; it is a
representation gate only.
"""

from __future__ import annotations

import math
import random
from dataclasses import asdict, dataclass, replace
from typing import Any, Sequence

import numpy as np

from .composition import LeafMaterial
from .ground_contacts import _assembly_index, _polygon_radii, regular_polygon
from .leaf_geometry import placement_transforms
from .mechanisms import (
    DECK_ID,
    MechanismAssembly,
    MechanismLayer,
    MechanismPart,
    _derived_seed,
    _loop_points,
    _material,
    prism_program,
    prism_vertices,
)


DIRECTION_CONTROL_VERSION = "func-direction-control-v1"
STEER_FUNCTIONS = ("direction_control",)
STEER_SUFFIX = "direction_control"


@dataclass(frozen=True)
class DirectionControlConfig:
    boss_sides: tuple[int, ...] = (6, 8, 10)
    boss_radius_m: tuple[float, float] = (0.05, 0.08)
    boss_height_m: tuple[float, float] = (0.01, 0.02)
    post_sides: tuple[int, ...] = (6, 8)
    post_radius_m: tuple[float, float] = (0.012, 0.025)
    #: post length above the arm top
    post_overhang_m: tuple[float, float] = (0.01, 0.03)
    arm_thickness_m: tuple[float, float] = (0.008, 0.015)
    hub_sides: int = 24
    #: hub circumradius as a multiple of the post circumradius
    hub_radius_factor: tuple[float, float] = (2.0, 3.0)
    #: smallest material ring between the bore and the hub outline
    min_hub_ring_m: float = 0.008
    arm_length_m: tuple[float, float] = (0.12, 0.28)
    tip_sides: int = 12
    tip_radius_m: tuple[float, float] = (0.015, 0.03)
    range_rad: tuple[float, float] = (0.3, 0.8)
    bearing_clearance_m: float = 2.5e-5
    #: bore polygon sides; a multiple of every post side count
    bore_sides: int = 96
    max_bearing_vertex_gap_m: float = 7.5e-5
    #: the arm's sweep circle stays this far inside the bay and the deck
    sweep_margin_m: float = 0.02
    min_range_rad: float = 0.2
    min_axis_angle_deg: float = 30.0


DEFAULT_DIRECTION_CONTROL_CONFIG = DirectionControlConfig()


def direction_control_config_record(
        config: DirectionControlConfig = DEFAULT_DIRECTION_CONTROL_CONFIG) -> dict[str, Any]:
    return {"version": DIRECTION_CONTROL_VERSION,
            **{k: list(v) if isinstance(v, tuple) else v for k, v in asdict(config).items()}}


def steer_ids(index: int) -> dict[str, str]:
    assembly = f"m{index}-{STEER_SUFFIX}"
    return {"assembly": assembly, "boss": assembly + ".boss", "post": assembly + ".post",
            "arm": assembly + ".arm", "motion": assembly + ".steer"}


def convex_hull(points: Sequence[Sequence[float]]) -> list[list[float]]:
    """Counter-clockwise convex hull (monotone chain), collinear points dropped."""

    pts = sorted({(float(x), float(y)) for x, y in points})

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: list[tuple[float, float]] = []
    upper: list[tuple[float, float]] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return [list(p) for p in lower[:-1] + upper[:-1]]


def steering_bore(post_sides: int, post_radius: float, clearance: float, sides: int) -> list[list[float]]:
    """Bore of apothem ``post_radius + clearance`` with a vertex at every post vertex direction."""

    if sides % post_sides:
        raise ValueError("bore sides must be a multiple of the post sides")
    return regular_polygon(sides, (post_radius + clearance) / math.cos(math.pi / sides), 0.0)


def _z_prism(part_id: str, role: str, outer, height: float, x_c: float, y_c: float, z0: float,
             holes=()) -> dict[str, Any]:
    placement = placement_transforms("z", False, 0.0, [x_c, y_c, z0])
    return prism_program(part_id, role, outer, height, placement, holes=holes)


def add_direction_control(layer: MechanismLayer, seed: int, catalogue: Sequence[LeafMaterial],
                          config: DirectionControlConfig = DEFAULT_DIRECTION_CONTROL_CONFIG) -> MechanismLayer:
    """The layer with a steering post and arm in the deck bay; deterministic per seed."""

    rng = random.Random(_derived_seed(DIRECTION_CONTROL_VERSION, "steer", seed))
    b = layer.backbone
    c = config.bearing_clearance_m
    boss_sides = rng.choice(config.boss_sides)
    boss_radius = rng.uniform(*config.boss_radius_m)
    boss_height = rng.uniform(*config.boss_height_m)
    post_sides = rng.choice(config.post_sides)
    post_radius = rng.uniform(*config.post_radius_m)
    overhang = rng.uniform(*config.post_overhang_m)
    thickness = rng.uniform(*config.arm_thickness_m)
    hub_radius = max(post_radius * rng.uniform(*config.hub_radius_factor),
                     (post_radius + c) / math.cos(math.pi / config.bore_sides) + config.min_hub_ring_m)
    arm_length = rng.uniform(*config.arm_length_m)
    tip_radius = rng.uniform(*config.tip_radius_m)
    heading = rng.uniform(0.0, 2 * math.pi)
    steer_range = rng.uniform(*config.range_rad)
    # The full sweep circle must fit in the bay along x and in the deck along y.
    room = min((b.core_x1 - b.bay_x0) / 2, (b.y1 - b.y0) / 2) - config.sweep_margin_m
    arm_length = min(arm_length, room - tip_radius)
    if arm_length <= hub_radius:
        raise ValueError("deck bay is too small for the steering arm")
    x_c = b.core_x1 - config.sweep_margin_m - (arm_length + tip_radius)
    y_c = (b.y0 + b.y1) / 2

    tip = [[arm_length * math.cos(heading) + x, arm_length * math.sin(heading) + y]
           for x, y in regular_polygon(config.tip_sides, tip_radius, heading)]
    arm_outer = convex_hull(regular_polygon(config.hub_sides, hub_radius, 0.0) + tip)
    bore = steering_bore(post_sides, post_radius, c, config.bore_sides)
    boss_top = b.z_top + boss_height
    first = 1 + max((_assembly_index(a.id) for a in layer.assemblies), default=-1)
    ids = steer_ids(first)
    programs = {
        "boss": _z_prism(ids["boss"], "steer_boss", regular_polygon(boss_sides, boss_radius, 0.0),
                         boss_height, x_c, y_c, b.z_top),
        "post": _z_prism(ids["post"], "steer_post", regular_polygon(post_sides, post_radius, 0.0),
                         c + thickness + overhang, x_c, y_c, boss_top),
        "arm": _z_prism(ids["arm"], "steer_arm", arm_outer, thickness, x_c, y_c, boss_top + c, holes=[bore]),
    }
    parts = tuple(MechanismPart(id=ids[role], parent=ids["assembly"], program=programs[role],
                                material=_material(seed, ids[role], catalogue)) for role in ("boss", "post", "arm"))
    assembly = MechanismAssembly(id=ids["assembly"], children=tuple(p.id for p in parts), functions=STEER_FUNCTIONS)
    interfaces = (
        {"id": ids["boss"] + ".seat", "a": ids["boss"], "b": DECK_ID, "kind": "bonded"},
        {"id": ids["post"] + ".seat", "a": ids["post"], "b": ids["boss"], "kind": "bonded"},
        {"id": ids["arm"] + ".bearing", "a": ids["arm"], "b": ids["post"], "kind": "bearing"},
    )
    motion = {"id": ids["motion"], "parts": [ids["arm"]], "type": "revolute",
              "axis_point_m": [float(x_c), float(y_c), float(boss_top)], "axis_dir": [0.0, 0.0, 1.0],
              "range_rad": float(steer_range)}
    evidence = dict(layer.evidence)
    evidence["direction_control"] = {"motion": ids["motion"]}
    return replace(layer, parts=layer.parts + parts, assemblies=layer.assemblies + (assembly,),
                   root_children=layer.root_children + (assembly.id,),
                   interfaces=layer.interfaces + interfaces, motions=layer.motions + (motion,),
                   evidence=evidence)


# --------------------------------------------------------------------------
# Re-check from the programs
# --------------------------------------------------------------------------

def direction_control_problems(layer: MechanismLayer,
                               config: DirectionControlConfig = DEFAULT_DIRECTION_CONTROL_CONFIG) -> list[str]:
    """Every violated direction-control rule, recomputed from the program vertices."""

    steering = [a for a in layer.assemblies if a.id.endswith("-" + STEER_SUFFIX)]
    if len(steering) != 1:
        return [f"expected 1 direction-control assembly, found {len(steering)}"]
    ids = steer_ids(_assembly_index(steering[0].id))
    programs = {p.id: p.program for p in layer.parts}
    if steering[0].functions != STEER_FUNCTIONS or set(steering[0].children) != {ids[r] for r in ("boss", "post", "arm")}:
        return [f"{steering[0].id}: unexpected children or functions"]
    problems: list[str] = []
    b = layer.backbone
    boss, post, arm = (prism_vertices(programs[ids[r]]) for r in ("boss", "post", "arm"))
    motion = {m["id"]: m for m in layer.motions}.get(ids["motion"])
    if motion is None or motion["parts"] != [ids["arm"]] or motion["type"] != "revolute":
        return problems + [f"{steering[0].id}: missing arm revolute motion"]
    if not config.min_range_rad <= motion["range_rad"] <= 2 * math.pi:
        problems.append(f"{ids['motion']}: range outside [{config.min_range_rad}, 2 pi]")
    axis = np.asarray(motion["axis_dir"], dtype=float)
    limit = math.cos(math.radians(config.min_axis_angle_deg))
    for other in layer.evidence.get("ground_propulsion", {}).get("motions", []):
        drive = np.asarray({m["id"]: m for m in layer.motions}[other]["axis_dir"], dtype=float)
        if abs(float(axis @ drive)) > limit:
            problems.append(f"{ids['motion']}: axis within {config.min_axis_angle_deg} deg of {other}")
    kinds = {(i["a"], i["b"]): i["kind"] for i in layer.interfaces}
    for pair, kind in (((ids["boss"], DECK_ID), "bonded"), ((ids["post"], ids["boss"]), "bonded"),
                       ((ids["arm"], ids["post"]), "bearing")):
        if kinds.get(pair) != kind:
            problems.append(f"{pair[0]}: missing {kind} interface to {pair[1]}")
    centre = np.asarray(motion["axis_point_m"][:2], dtype=float)
    boss_top = float(boss[:, 2].max())
    if abs(float(boss[:, 2].min()) - b.z_top) > 1e-9:
        problems.append(f"{ids['boss']}: not on the deck top")
    if abs(float(post[:, 2].min()) - boss_top) > 1e-9:
        problems.append(f"{ids['post']}: not on the boss top")
    if abs(float(motion["axis_point_m"][2]) - boss_top) > 1e-9:
        problems.append(f"{ids['motion']}: axis point is not on the boss top")
    boss_apothem, _ = _polygon_radii(_loop_points(programs[ids["boss"]]["profile"]["loops"][0]))
    post_outline = np.asarray(_loop_points(programs[ids["post"]]["profile"]["loops"][0]))
    _, post_circum = _polygon_radii(post_outline)
    if not post_circum < boss_apothem:
        problems.append(f"{ids['post']}: footprint is not inside the boss top")
    if not float(arm[:, 2].min()) > boss_top or not float(arm[:, 2].max()) < float(post[:, 2].max()):
        problems.append(f"{ids['arm']}: not between the boss top and the post top")
    loops = programs[ids["arm"]]["profile"]["loops"]
    if len(loops) != 2:
        problems.append(f"{ids['arm']}: needs exactly one bore")
    else:
        bore = np.asarray(_loop_points(loops[1]))
        bore_apothem, _ = _polygon_radii(bore)
        if not bore_apothem > post_circum:
            problems.append(f"{ids['arm']}: bore does not clear the rotating post")
        gaps = np.linalg.norm(post_outline[:, None, :] - bore[None, :, :], axis=2).min(axis=1)
        if float(gaps.max()) > config.max_bearing_vertex_gap_m:
            problems.append(f"{ids['arm']}: no bore vertex faces each post vertex closely")
    reach = float(np.linalg.norm(arm[:, :2] - centre, axis=1).max())
    m = config.sweep_margin_m
    if (centre[0] - reach < b.bay_x0 + m - 1e-9 or centre[0] + reach > b.core_x1 - m + 1e-9
            or centre[1] - reach < b.y0 + m - 1e-9 or centre[1] + reach > b.y1 - m + 1e-9):
        problems.append(f"{ids['arm']}: sweep circle leaves the deck bay")
    for verts, role in ((boss, "boss"), (post, "post")):
        if float(np.linalg.norm(verts[:, :2] - centre, axis=1).max()) > reach:
            problems.append(f"{ids[role]}: reaches beyond the arm sweep circle")
    if layer.evidence.get("direction_control") != {"motion": ids["motion"]}:
        problems.append("direction_control evidence does not name the steering motion")
    return problems
