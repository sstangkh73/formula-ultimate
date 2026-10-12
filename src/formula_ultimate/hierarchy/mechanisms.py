"""Mechanism layer of the functional (goal v2) vehicle (pure Python).

The v1 cluster (decomposition, layout, bores, fasteners) is realized first.
Its re-read meshes give the measured cluster box and its lowest leaf; the
mechanism layer is then planned around that measured box and hung on a
structural deck:

- Deck (``load_structure``): a flat chamfered-octagon plate whose top face is
  the cluster's lowest mesh height ``Z0``. Its footprint is the cluster
  footprint plus a seed-drawn margin, plus a bay in +x reserved for later
  modules, plus a lip on both x ends reserved for the ground-contact lines.
  The cluster's lowest leaf has a vertex on the deck top, so the two are
  joined by a ``bonded`` interface without interpenetration.

Mechanism leaves live in root-level assemblies ``m<k>-<capability>`` tagged
with their capabilities, and use the grammar ``func-leaf-mechanism-v2``:
polygon ``section`` (outer loop plus optional hole loops) -> straight
``extrude`` along local +z -> rigid ``transform`` steps. Only flat faces are
produced, so contacts and clearances survive tessellation exactly.

Evidence is emitted only for capabilities whose mechanism exists. Nothing here
is physical validation: the deck is not shown to carry load.
"""

from __future__ import annotations

import hashlib
import math
import random
from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

import numpy as np

from .composition import LeafMaterial
from .leaf_geometry import (
    ANGULAR_TOLERANCE_RAD,
    LINEAR_TOLERANCE_FRACTION,
    SOLID_GRAMMAR_VERSION,
    WIRE_GRAMMAR_VERSION,
    LeafProgramError,
    placement_transforms,
    transform_points,
)
from .part_tree import canonical_sha256


MECHANISM_GRAMMAR_VERSION = "func-leaf-mechanism-v2"
MECHANISM_LAYER_VERSION = "func-mechanism-layer-v1"
DECK_ASSEMBLY = "m0-load_structure"
DECK_ID = DECK_ASSEMBLY + ".deck"
DECK_SEAT_ID = DECK_ID + ".seat"


@dataclass(frozen=True)
class MechanismConfig:
    deck_thickness_m: tuple[float, float] = (0.04, 0.06)
    deck_margin_m: tuple[float, float] = (0.08, 0.2)
    deck_chamfer_m: tuple[float, float] = (0.01, 0.03)
    bay_length_m: tuple[float, float] = (0.8, 1.2)
    #: x extension of the deck beyond the core region on both ends, reserved
    #: for the ground-contact lines (wheel centre line plus an axle seat).
    wheel_lip_m: float = 0.14


DEFAULT_MECHANISM_CONFIG = MechanismConfig()


@dataclass(frozen=True)
class ClusterBounds:
    lo: tuple[float, float, float]
    hi: tuple[float, float, float]
    lowest_leaf: str
    lowest_point: tuple[float, float, float]


@dataclass(frozen=True)
class Backbone:
    """Deck frame shared by later mechanism modules (metres)."""

    x0: float
    x1: float
    y0: float
    y1: float
    z_top: float
    thickness: float
    chamfer: float
    #: core region (cluster plus margin plus bay) along x
    core_x0: float
    core_x1: float
    #: start of the reserved bay along x (cluster end plus margin)
    bay_x0: float


@dataclass(frozen=True)
class MechanismPart:
    id: str
    parent: str
    program: dict
    material: LeafMaterial


@dataclass(frozen=True)
class MechanismAssembly:
    id: str
    children: tuple[str, ...]
    functions: tuple[str, ...]


@dataclass(frozen=True)
class MechanismLayer:
    seed: int
    backbone: Backbone
    parts: tuple[MechanismPart, ...]
    assemblies: tuple[MechanismAssembly, ...]
    root_children: tuple[str, ...]
    interfaces: tuple[dict, ...]
    motions: tuple[dict, ...]
    evidence: dict


def mechanism_config_record(config: MechanismConfig = DEFAULT_MECHANISM_CONFIG) -> dict[str, Any]:
    return {"version": MECHANISM_LAYER_VERSION, "grammar_version": MECHANISM_GRAMMAR_VERSION,
            **{k: list(v) if isinstance(v, tuple) else v for k, v in asdict(config).items()}}


def _derived_seed(*parts: object) -> int:
    text = "|".join(str(p) for p in parts)
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)


# --------------------------------------------------------------------------
# Measured cluster
# --------------------------------------------------------------------------

def measure_cluster(meshes: Mapping[str, np.ndarray]) -> ClusterBounds:
    """Box and lowest leaf of the realized cluster (ties broken by leaf id)."""

    if not meshes:
        raise ValueError("no cluster meshes")
    lo, hi = np.full(3, np.inf), np.full(3, -np.inf)
    lowest: tuple[float, str, tuple[float, float, float]] | None = None
    for leaf_id in sorted(meshes):
        pts = np.asarray(meshes[leaf_id], dtype=float).reshape(-1, 3)
        lo, hi = np.minimum(lo, pts.min(axis=0)), np.maximum(hi, pts.max(axis=0))
        index = int(np.argmin(pts[:, 2]))
        if lowest is None or pts[index, 2] < lowest[0]:
            lowest = (float(pts[index, 2]), leaf_id, tuple(float(v) for v in pts[index]))
    assert lowest is not None
    return ClusterBounds(lo=tuple(float(v) for v in lo), hi=tuple(float(v) for v in hi),
                         lowest_leaf=lowest[1], lowest_point=lowest[2])


# --------------------------------------------------------------------------
# Mechanism leaf programs
# --------------------------------------------------------------------------

def signed_area(points: Sequence[Sequence[float]]) -> float:
    total = 0.0
    for (ax, ay), (bx, by) in zip(points, list(points[1:]) + [points[0]]):
        total += ax * by - ay * bx
    return 0.5 * total


def point_in_polygon(point: Sequence[float], polygon: Sequence[Sequence[float]]) -> bool:
    """Strict interior test (even-odd); points on an edge count as outside."""

    x, y = float(point[0]), float(point[1])
    inside = False
    for (ax, ay), (bx, by) in zip(polygon, list(polygon[1:]) + [polygon[0]]):
        cross = (bx - ax) * (y - ay) - (by - ay) * (x - ax)
        if abs(cross) <= 1e-15 and min(ax, bx) <= x <= max(ax, bx) and min(ay, by) <= y <= max(ay, by):
            return False
        if (ay > y) != (by > y) and x < ax + (y - ay) * (bx - ax) / (by - ay):
            inside = not inside
    return inside


def _loop(loop_id: str, role: str, points: Sequence[Sequence[float]]) -> dict[str, Any]:
    pts = [[float(x), float(y)] for x, y in points]
    return {"loop_id": loop_id, "role": role, "segments": [{
        "segment_id": "s0", "operator": "polyline", "parameters": {"points_m": pts + [list(pts[0])]},
        "trim_fraction": [0.0, 1.0]}]}


def prism_program(leaf_id: str, role: str, outer: Sequence[Sequence[float]], height_m: float,
                  placement: Sequence[Mapping[str, Any]],
                  holes: Sequence[Sequence[Sequence[float]]] = ()) -> dict[str, Any]:
    """A straight polygon prism (optional hole loops) placed by rigid transforms."""

    loops = [_loop("outer", "outer", outer)] + [_loop(f"hole{i}", "hole", h) for i, h in enumerate(holes)]
    profile = {
        "profile_id": f"{leaf_id}-profile".lower(),
        "family": f"mechanism_{role}",
        "loops": loops,
        "transforms": [],
        "offset": {"distance_m": 0.0, "kind": "arc"},
        "constraints": [{"kind": "hole_count", "value": len(holes)}],
    }
    xy = np.asarray(outer, dtype=float)
    length = float(math.hypot(*(xy.max(axis=0) - xy.min(axis=0)), height_m))
    features: list[dict[str, Any]] = [
        {"feature_id": "sec", "operator": "section", "inputs": [], "parameters": {
            "profile_id": profile["profile_id"], "scale": 1.0,
            "translation_m": [0.0, 0.0, 0.0], "rotation_rad": 0.0}},
        {"feature_id": "body", "operator": "extrude", "inputs": ["sec"], "parameters": {
            "vector_m": [0.0, 0.0, float(height_m)], "taper_rad": 0.0}},
    ]
    previous = "body"
    for index, step in enumerate(placement):
        feature_id = f"place{index}"
        features.append({"feature_id": feature_id, "operator": "transform", "inputs": [previous],
                         "parameters": {key: step[key] for key in
                                        ("translation_m", "axis_start_m", "axis_end_m", "angle_rad")}})
        previous = feature_id
    program = {
        "leaf_grammar_version": MECHANISM_GRAMMAR_VERSION,
        "wire_grammar_version": WIRE_GRAMMAR_VERSION,
        "solid_grammar_version": SOLID_GRAMMAR_VERSION,
        "units": "SI_m_rad",
        "role": role,
        "characteristic_length_m": length,
        "height_m": float(height_m),
        "profile": profile,
        "candidate": {
            "candidate_id": f"{leaf_id}-solid".lower(), "family": f"mechanism_{role}",
            "expected_body_count": 1, "features": features, "final_feature_id": previous,
            "datums": [
                {"datum_id": "center", "kind": "bbox_center", "parameters": {}},
                {"datum_id": "long", "kind": "longest_bbox_axis", "parameters": {}},
                {"datum_id": "base", "kind": "extreme_plane", "parameters": {"axis": "z", "side": "min"}},
            ],
        },
        "tessellation": {"linear_tolerance_m": LINEAR_TOLERANCE_FRACTION * length,
                         "angular_tolerance_rad": ANGULAR_TOLERANCE_RAD},
    }
    validate_mechanism_program(program)
    return program


def _loop_points(loop: Mapping[str, Any]) -> list[list[float]]:
    segments = loop["segments"]
    if len(segments) != 1 or segments[0]["operator"] != "polyline" or segments[0]["trim_fraction"] != [0.0, 1.0]:
        raise LeafProgramError("mechanism loops must be one untrimmed polyline")
    points = segments[0]["parameters"]["points_m"]
    if len(points) < 4 or points[0] != points[-1]:
        raise LeafProgramError("mechanism loop must be closed with at least three vertices")
    for p in points:
        if len(p) != 2 or not all(isinstance(v, (int, float)) and math.isfinite(v) for v in p):
            raise LeafProgramError("mechanism loop vertices must be finite 2D points")
    return [list(map(float, p)) for p in points[:-1]]


def validate_mechanism_program(program: Mapping[str, Any]) -> None:
    """Check the exact mechanism prism structure emitted by ``prism_program``."""

    expected = {"leaf_grammar_version", "wire_grammar_version", "solid_grammar_version", "units", "role",
                "characteristic_length_m", "height_m", "profile", "candidate", "tessellation"}
    if set(program) != expected:
        raise LeafProgramError("mechanism program fields mismatch")
    if (program["leaf_grammar_version"], program["wire_grammar_version"], program["solid_grammar_version"],
            program["units"]) != (MECHANISM_GRAMMAR_VERSION, WIRE_GRAMMAR_VERSION, SOLID_GRAMMAR_VERSION,
                                  "SI_m_rad"):
        raise LeafProgramError("mechanism grammar identity or units mismatch")
    height = program["height_m"]
    if not (isinstance(height, float) and math.isfinite(height) and height > 0):
        raise LeafProgramError("mechanism height must be a positive float")
    loops = program["profile"]["loops"]
    if not loops or loops[0]["role"] != "outer" or any(loop["role"] != "hole" for loop in loops[1:]):
        raise LeafProgramError("mechanism profile needs one outer loop then hole loops")
    if program["profile"]["constraints"] != [{"kind": "hole_count", "value": len(loops) - 1}]:
        raise LeafProgramError("hole count constraint mismatch")
    outer = _loop_points(loops[0])
    if signed_area(outer) <= 0:
        raise LeafProgramError("outer loop must be counter-clockwise with positive area")
    for loop in loops[1:]:
        hole = _loop_points(loop)
        if abs(signed_area(hole)) <= 0 or not all(point_in_polygon(p, outer) for p in hole):
            raise LeafProgramError("hole loop must lie strictly inside the outer loop")
    features = program["candidate"]["features"]
    operators = [f["operator"] for f in features]
    if operators[:2] != ["section", "extrude"] or any(op != "transform" for op in operators[2:]):
        raise LeafProgramError("mechanism candidate must be section, extrude, then transforms")
    if features[1]["parameters"] != {"vector_m": [0.0, 0.0, height], "taper_rad": 0.0}:
        raise LeafProgramError("mechanism extrusion must be straight along +z by height_m")
    if program["candidate"]["final_feature_id"] != features[-1]["feature_id"]:
        raise LeafProgramError("final feature must be the last feature")
    for feature in features[2:]:
        p = feature["parameters"]
        for key in ("translation_m", "axis_start_m", "axis_end_m"):
            if len(p[key]) != 3 or not all(math.isfinite(float(v)) for v in p[key]):
                raise LeafProgramError(f"{key} must have three finite coordinates")
        if not math.isfinite(float(p["angle_rad"])) or math.dist(p["axis_start_m"], p["axis_end_m"]) <= 0:
            raise LeafProgramError("transform angle or axis is invalid")
    length = program["characteristic_length_m"]
    if not 0 < program["tessellation"]["linear_tolerance_m"] < length:
        raise LeafProgramError("tessellation tolerance is outside bounds")
    canonical_sha256(program)


def prism_vertices(program: Mapping[str, Any]) -> np.ndarray:
    """World coordinates of every polygon vertex of both prism caps."""

    validate_mechanism_program(program)
    height = program["height_m"]
    local = []
    for loop in program["profile"]["loops"]:
        for x, y in _loop_points(loop):
            local.extend([[x, y, 0.0], [x, y, height]])
    return transform_points(program, np.asarray(local, dtype=float))


# --------------------------------------------------------------------------
# Planning
# --------------------------------------------------------------------------

def chamfered_rectangle(x0: float, x1: float, y0: float, y1: float, c: float) -> list[list[float]]:
    """Counter-clockwise octagon: the rectangle with each corner cut by c."""

    return [[x0 + c, y0], [x1 - c, y0], [x1, y0 + c], [x1, y1 - c],
            [x1 - c, y1], [x0 + c, y1], [x0, y1 - c], [x0, y0 + c]]


def plan_backbone(seed: int, bounds: ClusterBounds,
                  config: MechanismConfig = DEFAULT_MECHANISM_CONFIG) -> Backbone:
    rng = random.Random(_derived_seed(MECHANISM_LAYER_VERSION, "deck", seed))
    thickness = rng.uniform(*config.deck_thickness_m)
    margin = rng.uniform(*config.deck_margin_m)
    chamfer = rng.uniform(*config.deck_chamfer_m)
    bay = rng.uniform(*config.bay_length_m)
    (cx0, cy0, cz0), (cx1, cy1, _cz1) = bounds.lo, bounds.hi
    core_x0, core_x1 = cx0 - margin, cx1 + margin + bay
    return Backbone(x0=core_x0 - config.wheel_lip_m, x1=core_x1 + config.wheel_lip_m,
                    y0=cy0 - margin, y1=cy1 + margin, z_top=cz0, thickness=thickness, chamfer=chamfer,
                    core_x0=core_x0, core_x1=core_x1, bay_x0=cx1 + margin)


def deck_program(backbone: Backbone) -> dict[str, Any]:
    b = backbone
    outer = chamfered_rectangle(b.x0, b.x1, b.y0, b.y1, b.chamfer)
    placement = placement_transforms("z", False, 0.0, [0.0, 0.0, b.z_top - b.thickness])
    return prism_program(DECK_ID, "deck", outer, b.thickness, placement)


def _material(seed: int, part_id: str, catalogue: Sequence[LeafMaterial]) -> LeafMaterial:
    rng = random.Random(_derived_seed(MECHANISM_LAYER_VERSION, "material", seed, part_id))
    return rng.choice(list(catalogue))


def plan_mechanisms(seed: int, bounds: ClusterBounds, catalogue: Sequence[LeafMaterial],
                    config: MechanismConfig = DEFAULT_MECHANISM_CONFIG) -> MechanismLayer:
    """The mechanism layer for a measured cluster; deterministic per seed."""

    backbone = plan_backbone(seed, bounds, config)
    deck = MechanismPart(id=DECK_ID, parent=DECK_ASSEMBLY, program=deck_program(backbone),
                         material=_material(seed, DECK_ID, catalogue))
    assemblies = (MechanismAssembly(id=DECK_ASSEMBLY, children=(DECK_ID,), functions=("load_structure",)),)
    interfaces = ({"id": DECK_SEAT_ID, "a": DECK_ID, "b": bounds.lowest_leaf, "kind": "bonded"},)
    evidence = {"load_structure": {"members": [DECK_ID]}}
    return MechanismLayer(seed=seed, backbone=backbone, parts=(deck,), assemblies=assemblies,
                          root_children=(DECK_ASSEMBLY,), interfaces=interfaces, motions=(), evidence=evidence)


def mechanism_problems(layer: MechanismLayer, bounds: ClusterBounds,
                       cluster_ids: Sequence[str]) -> list[str]:
    """Every violated mechanism-layer rule, recomputed from the programs."""

    problems: list[str] = []
    cluster = set(cluster_ids)
    part_ids = [p.id for p in layer.parts]
    assembly_ids = [a.id for a in layer.assemblies]
    new_ids = part_ids + assembly_ids
    if len(set(new_ids)) != len(new_ids) or set(new_ids) & cluster:
        problems.append("mechanism ids are not unique")
    for part in layer.parts:
        try:
            validate_mechanism_program(part.program)
        except (LeafProgramError, KeyError, TypeError, ValueError) as exc:
            problems.append(f"{part.id}: {exc}")
    children = [c for a in layer.assemblies for c in a.children]
    if sorted(children + list(layer.root_children)) != sorted(new_ids):
        problems.append("mechanism assemblies do not cover every mechanism node exactly once")
    known = cluster | set(part_ids)
    for item in layer.interfaces:
        if item["a"] not in known or item["b"] not in known or item["a"] == item["b"]:
            problems.append(f"{item['id']}: interface endpoints are not distinct leaves")
    deck = {p.id: p for p in layer.parts}.get(DECK_ID)
    if deck is None:
        return problems + ["no deck"]
    verts = prism_vertices(deck.program)
    if abs(float(verts[:, 2].max()) - bounds.lo[2]) > 1e-9:
        problems.append("deck top is not at the cluster's lowest height")
    outer = _loop_points(deck.program["profile"]["loops"][0])
    (x0, y0, _), (x1, y1, _) = bounds.lo, bounds.hi
    for corner in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
        if not point_in_polygon(corner, outer):
            problems.append("deck does not cover the cluster footprint")
            break
    if not point_in_polygon(bounds.lowest_point[:2], outer):
        problems.append("cluster's lowest point is not above the deck")
    return problems


# --------------------------------------------------------------------------
# Manifest merge
# --------------------------------------------------------------------------

def roll_up_manifest_nodes(nodes: Sequence[Mapping[str, Any]], root: str) -> list[dict]:
    """Copies of manifest nodes whose assembly masses and centres roll up exactly.

    Part values are kept; assembly values use the arithmetic of
    ``part_tree.roll_up`` (children in order, mass sum, then moment / mass).
    """

    by_id = {n["id"]: dict(n) for n in nodes}
    done: set[str] = set()
    stack: list[tuple[str, bool]] = [(root, False)]
    while stack:
        node_id, expanded = stack.pop()
        node = by_id[node_id]
        if node["kind"] == "part" or node_id in done:
            continue
        if not expanded:
            stack.append((node_id, True))
            stack.extend((child, False) for child in reversed(node["children"]))
            continue
        mass, moment = 0.0, [0.0, 0.0, 0.0]
        for child in node["children"]:
            child_mass = float(by_id[child]["mass_kg"])
            child_com = by_id[child]["center_of_mass_m"]
            mass += child_mass
            for axis in range(3):
                moment[axis] += float(child_com[axis]) * child_mass
        node["mass_kg"] = mass
        node["center_of_mass_m"] = [moment[0] / mass, moment[1] / mass, moment[2] / mass]
        done.add(node_id)
    return [by_id[n["id"]] for n in nodes]


def merge_mechanism_layer(manifest: Mapping[str, Any], layer: MechanismLayer,
                          measurements: Mapping[str, Mapping[str, Any]],
                          mesh_path: Any) -> dict:
    """The manifest with the mechanism nodes under the root and their interfaces."""

    result = dict(manifest)
    root = manifest["root"]
    nodes = []
    for node in manifest["nodes"]:
        if node["id"] == root:
            node = dict(node, children=list(node["children"]) + list(layer.root_children))
        nodes.append(node)
    for assembly in layer.assemblies:
        nodes.append({"id": assembly.id, "kind": "assembly", "children": list(assembly.children),
                      "functions": list(assembly.functions), "mass_kg": 0.0, "center_of_mass_m": [0.0, 0.0, 0.0]})
    for part in layer.parts:
        measured = measurements[part.id]
        nodes.append({
            "id": part.id, "kind": "part", "mesh": mesh_path(part.id),
            "material_id": part.material.material_id, "density_kg_m3": float(part.material.density_kg_m3),
            "mass_kg": float(measured["mass_kg"]),
            "center_of_mass_m": [float(v) for v in measured["center_of_mass_m"]],
            "generator": {"grammar_version": MECHANISM_GRAMMAR_VERSION, "program": part.program,
                          "program_sha256": canonical_sha256(part.program)},
        })
    result["nodes"] = roll_up_manifest_nodes(nodes, root)
    result["interfaces"] = list(manifest["interfaces"]) + [dict(item) for item in layer.interfaces]
    return result
