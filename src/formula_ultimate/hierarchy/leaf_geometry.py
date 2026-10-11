"""Free-form leaf programs and mesh measurement for the part hierarchy.

A leaf program is a Work 091-style profile (one closed outer loop that is
star-shaped around the local origin) and a Work 092-style candidate that
extrudes it along local +z and then places it with rigid transforms. The flat
end faces at local ``z = 0`` and ``z = height_m`` are the planar contact faces
that later placement uses. All lengths are metres and angles radians.

Mass and centre of mass are measured from the exported float32 STL triangles,
never taken from the CAD kernel. Nothing here is physical validation.
"""

from __future__ import annotations

import math
import random
import struct
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

from formula_ultimate.components.freeform_solid_grammar import GRAMMAR_VERSION as SOLID_GRAMMAR_VERSION
from formula_ultimate.components.freeform_wire_grammar import GRAMMAR_VERSION as WIRE_GRAMMAR_VERSION

from .part_tree import canonical_sha256


LEAF_GRAMMAR_VERSION = "hier-leaf-extrusion-v1"
PROFILE_KINDS = ("polyline", "bspline")
AXES = ("x", "y", "z")
STL_HEADER = b"formula_ultimate hierarchy leaf binary STL, metres".ljust(80, b" ")

POLYLINE_VERTICES = (5, 11)
BSPLINE_POINTS = (6, 12)
RADIUS_FRACTION = (0.22, 0.5)
RADIUS_VARIATION = (0.62, 1.0)
HEIGHT_FRACTION = (0.12, 0.9)
LINEAR_TOLERANCE_FRACTION = 2e-3
ANGULAR_TOLERANCE_RAD = 0.3
# A periodic interpolating spline can bow inward between its points, so its
# declared inscribed radius keeps a margin below the smallest point radius.
BSPLINE_INSCRIBED_MARGIN = 0.8


class LeafProgramError(ValueError):
    """Raised when a leaf program is outside the declared bounds."""


class MeshError(ValueError):
    """Raised when a mesh is not a closed, consistently oriented solid."""


def program_sha256(program: Mapping[str, Any]) -> str:
    return canonical_sha256(program)


# --------------------------------------------------------------------------
# Rigid placement
# --------------------------------------------------------------------------

def placement_transforms(axis: str, flip: bool, spin_rad: float,
                         translation_m: Sequence[float]) -> list[dict[str, Any]]:
    """Transform parameters that map local +z to +axis (or -axis when flipped).

    Order: spin about local z, optional half turn about local x (flip), the
    axis remap, then the translation. Each item is a Work 092 ``transform``
    parameter set (rotation about the axis start->end, then translation).
    """

    if axis not in AXES:
        raise LeafProgramError("placement axis must be x, y or z")
    zero = [0.0, 0.0, 0.0]
    steps: list[dict[str, Any]] = []
    if spin_rad:
        steps.append({"translation_m": zero, "axis_start_m": zero, "axis_end_m": [0.0, 0.0, 1.0],
                      "angle_rad": float(spin_rad)})
    if flip:
        steps.append({"translation_m": zero, "axis_start_m": zero, "axis_end_m": [1.0, 0.0, 0.0],
                      "angle_rad": math.pi})
    if axis == "x":
        steps.append({"translation_m": zero, "axis_start_m": zero, "axis_end_m": [0.0, 1.0, 0.0],
                      "angle_rad": math.pi / 2})
    elif axis == "y":
        steps.append({"translation_m": zero, "axis_start_m": zero, "axis_end_m": [1.0, 0.0, 0.0],
                      "angle_rad": -math.pi / 2})
    translation = [float(v) for v in translation_m]
    if len(translation) != 3 or not all(math.isfinite(v) for v in translation):
        raise LeafProgramError("translation must be three finite coordinates")
    steps.append({"translation_m": translation, "axis_start_m": zero, "axis_end_m": [0.0, 0.0, 1.0],
                  "angle_rad": 0.0})
    return steps


def _rotation_matrix(axis_start: Sequence[float], axis_end: Sequence[float], angle: float) -> np.ndarray:
    k = np.asarray(axis_end, dtype=float) - np.asarray(axis_start, dtype=float)
    k = k / np.linalg.norm(k)
    kx = np.array([[0.0, -k[2], k[1]], [k[2], 0.0, -k[0]], [-k[1], k[0], 0.0]])
    return np.eye(3) + math.sin(angle) * kx + (1.0 - math.cos(angle)) * (kx @ kx)


def transform_points(program: Mapping[str, Any], points_local: np.ndarray) -> np.ndarray:
    """Apply the program's transform features to local points (right-hand rule)."""

    points = np.asarray(points_local, dtype=float).reshape(-1, 3).copy()
    for feature in program["candidate"]["features"]:
        if feature["operator"] != "transform":
            continue
        p = feature["parameters"]
        start = np.asarray(p["axis_start_m"], dtype=float)
        if p["angle_rad"]:
            rot = _rotation_matrix(p["axis_start_m"], p["axis_end_m"], p["angle_rad"])
            points = (points - start) @ rot.T + start
        points = points + np.asarray(p["translation_m"], dtype=float)
    return points


# --------------------------------------------------------------------------
# Program generation and validation
# --------------------------------------------------------------------------

def _polygon_inscribed_radius(points: Sequence[Sequence[float]]) -> float:
    best = math.inf
    for (ax, ay), (bx, by) in zip(points, list(points[1:]) + [points[0]]):
        length = math.hypot(bx - ax, by - ay)
        best = min(best, abs(ax * by - ay * bx) / length)
    return best


def leaf_program(rng: random.Random, characteristic_length_m: float,
                 placement: Sequence[Mapping[str, Any]] | None = None,
                 leaf_id: str = "leaf") -> dict[str, Any]:
    """Draw a free-form extruded leaf program sized by characteristic_length_m."""

    length = float(characteristic_length_m)
    if not math.isfinite(length) or length <= 0:
        raise LeafProgramError("characteristic length must be finite and positive")
    kind = rng.choice(PROFILE_KINDS)
    lo, hi = POLYLINE_VERTICES if kind == "polyline" else BSPLINE_POINTS
    count = rng.randint(lo, hi)
    radius = length * rng.uniform(*RADIUS_FRACTION)
    height = length * rng.uniform(*HEIGHT_FRACTION)
    phase = rng.uniform(0.0, 2 * math.pi)
    # Jittered angles keep the order strictly increasing (star-shaped loop).
    angles = [phase + 2 * math.pi * (i + rng.uniform(-0.3, 0.3)) / count for i in range(count)]
    radii = [radius * rng.uniform(*RADIUS_VARIATION) for _ in range(count)]
    points = [[r * math.cos(a), r * math.sin(a)] for r, a in zip(radii, angles)]
    if kind == "polyline":
        segment_params = {"points_m": points + [list(points[0])]}
        inscribed = _polygon_inscribed_radius(points)
    else:
        segment_params = {"control_points_m": points, "degree": 3, "periodic": True}
        inscribed = BSPLINE_INSCRIBED_MARGIN * min(radii) * math.cos(math.pi / count)
    profile = {
        "profile_id": f"{leaf_id}-profile".lower(),
        "family": f"star_{kind}",
        "loops": [{"loop_id": "outer", "role": "outer", "segments": [{
            "segment_id": "s0", "operator": kind, "parameters": segment_params,
            "trim_fraction": [0.0, 1.0],
        }]}],
        "transforms": [],
        "offset": {"distance_m": 0.0, "kind": "arc"},
        "constraints": [{"kind": "hole_count", "value": 0}],
    }
    features: list[dict[str, Any]] = [
        {"feature_id": "sec", "operator": "section", "inputs": [], "parameters": {
            "profile_id": profile["profile_id"], "scale": 1.0,
            "translation_m": [0.0, 0.0, 0.0], "rotation_rad": 0.0}},
        {"feature_id": "body", "operator": "extrude", "inputs": ["sec"], "parameters": {
            "vector_m": [0.0, 0.0, height], "taper_rad": 0.0}},
    ]
    previous = "body"
    for index, step in enumerate(placement or placement_transforms("z", False, 0.0, [0.0, 0.0, 0.0])):
        feature_id = f"place{index}"
        features.append({"feature_id": feature_id, "operator": "transform", "inputs": [previous],
                         "parameters": {key: step[key] for key in
                                        ("translation_m", "axis_start_m", "axis_end_m", "angle_rad")}})
        previous = feature_id
    program = {
        "leaf_grammar_version": LEAF_GRAMMAR_VERSION,
        "wire_grammar_version": WIRE_GRAMMAR_VERSION,
        "solid_grammar_version": SOLID_GRAMMAR_VERSION,
        "units": "SI_m_rad",
        "characteristic_length_m": length,
        "contact": {"height_m": height, "inscribed_radius_m": inscribed,
                    "outer_radius_m": max(radii) * (1.0 if kind == "polyline" else 1.0 / BSPLINE_INSCRIBED_MARGIN)},
        "profile": profile,
        "candidate": {
            "candidate_id": f"{leaf_id}-solid".lower(), "family": "extruded_star",
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
    validate_leaf_program(program)
    return program


def with_placement(program: Mapping[str, Any], placement: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Return a copy of program whose transform features are replaced by placement."""

    import copy

    result = copy.deepcopy(dict(program))
    features = [f for f in result["candidate"]["features"] if f["operator"] != "transform"]
    previous = features[-1]["feature_id"]
    for index, step in enumerate(placement):
        feature_id = f"place{index}"
        features.append({"feature_id": feature_id, "operator": "transform", "inputs": [previous],
                         "parameters": {key: step[key] for key in
                                        ("translation_m", "axis_start_m", "axis_end_m", "angle_rad")}})
        previous = feature_id
    result["candidate"]["features"] = features
    result["candidate"]["final_feature_id"] = previous
    validate_leaf_program(result)
    return result


def _finite(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise LeafProgramError(f"{label} must be a finite number")
    return float(value)


def validate_leaf_program(program: Mapping[str, Any]) -> None:
    """Check the exact program structure this module emits and executes."""

    expected = {"leaf_grammar_version", "wire_grammar_version", "solid_grammar_version", "units",
                "characteristic_length_m", "contact", "profile", "candidate", "tessellation"}
    if set(program) != expected:
        raise LeafProgramError("program fields mismatch")
    if (program["leaf_grammar_version"], program["wire_grammar_version"], program["solid_grammar_version"],
            program["units"]) != (LEAF_GRAMMAR_VERSION, WIRE_GRAMMAR_VERSION, SOLID_GRAMMAR_VERSION, "SI_m_rad"):
        raise LeafProgramError("grammar identity or units mismatch")
    length = _finite(program["characteristic_length_m"], "characteristic length")
    contact = program["contact"]
    if set(contact) != {"height_m", "inscribed_radius_m", "outer_radius_m"}:
        raise LeafProgramError("contact fields mismatch")
    height = _finite(contact["height_m"], "height")
    inscribed = _finite(contact["inscribed_radius_m"], "inscribed radius")
    outer = _finite(contact["outer_radius_m"], "outer radius")
    if not (length > 0 and height > 0 and 0 < inscribed < outer):
        raise LeafProgramError("contact dimensions must be positive with inscribed < outer")
    profile = program["profile"]
    loops = profile["loops"]
    if len(loops) != 1 or loops[0]["role"] != "outer" or len(loops[0]["segments"]) != 1:
        raise LeafProgramError("profile must have exactly one single-segment outer loop")
    segment = loops[0]["segments"][0]
    if segment["operator"] not in PROFILE_KINDS or segment["trim_fraction"] != [0.0, 1.0]:
        raise LeafProgramError("profile segment must be an untrimmed polyline or B-spline")
    if profile["offset"]["distance_m"] != 0.0 or profile["transforms"]:
        raise LeafProgramError("profile offset and transforms are not used by leaf programs")
    candidate = program["candidate"]
    operators = [f["operator"] for f in candidate["features"]]
    if operators[:2] != ["section", "extrude"] or any(op != "transform" for op in operators[2:]):
        raise LeafProgramError("candidate must be section, extrude, then transforms")
    extrude = candidate["features"][1]["parameters"]
    if extrude["vector_m"] != [0.0, 0.0, height] or extrude["taper_rad"] != 0.0:
        raise LeafProgramError("extrusion must be straight along +z by height_m")
    if candidate["final_feature_id"] != candidate["features"][-1]["feature_id"]:
        raise LeafProgramError("final feature must be the last feature")
    for feature in candidate["features"][2:]:
        p = feature["parameters"]
        for key in ("translation_m", "axis_start_m", "axis_end_m"):
            if len(p[key]) != 3:
                raise LeafProgramError(f"{key} must have three coordinates")
            for v in p[key]:
                _finite(v, key)
        _finite(p["angle_rad"], "angle")
        if math.dist(p["axis_start_m"], p["axis_end_m"]) <= 0:
            raise LeafProgramError("transform axis must have non-zero length")
    tess = program["tessellation"]
    if set(tess) != {"linear_tolerance_m", "angular_tolerance_rad"}:
        raise LeafProgramError("tessellation fields mismatch")
    if not (0 < _finite(tess["linear_tolerance_m"], "linear tolerance") < length
            and 0 < _finite(tess["angular_tolerance_rad"], "angular tolerance") < 1.0):
        raise LeafProgramError("tessellation tolerances are outside bounds")
    try:
        canonical_sha256(program)
    except (TypeError, ValueError) as exc:
        raise LeafProgramError(f"program is not canonical JSON: {exc}") from exc


# --------------------------------------------------------------------------
# STL and mesh measurement
# --------------------------------------------------------------------------

def stl_bytes(triangles: np.ndarray) -> bytes:
    """Deterministic binary STL with float32 vertices and computed normals."""

    tris = np.asarray(triangles, dtype=np.float64).reshape(-1, 3, 3)
    tris32 = tris.astype("<f4")
    normals = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    norms = np.linalg.norm(normals, axis=1, keepdims=True)
    normals = np.divide(normals, norms, out=np.zeros_like(normals), where=norms > 0)
    record = np.dtype([("normal", "<f4", 3), ("v", "<f4", (3, 3)), ("attr", "<u2")])
    data = np.zeros(len(tris), dtype=record)
    data["normal"] = normals.astype("<f4")
    data["v"] = tris32
    return STL_HEADER + struct.pack("<I", len(tris)) + data.tobytes()


def read_binary_stl(path: Path) -> np.ndarray:
    data = Path(path).read_bytes()
    count = struct.unpack_from("<I", data, 80)[0]
    if len(data) != 84 + 50 * count:
        raise MeshError(f"{path}: not a binary STL")
    record = np.dtype([("normal", "<f4", 3), ("v", "<f4", (3, 3)), ("attr", "<u2")])
    return np.frombuffer(data, dtype=record, count=count, offset=84)["v"].astype(np.float64)


def closure_problems(tris: np.ndarray) -> list[str]:
    """Closed, consistently oriented 2-manifold check on exact shared vertices."""

    if len(tris) < 4:
        return ["fewer than 4 triangles"]
    if not np.all(np.isfinite(tris)):
        return ["non-finite coordinate"]
    _, index = np.unique(tris.reshape(-1, 3), axis=0, return_inverse=True)
    faces = index.reshape(-1, 3)
    if np.any((faces[:, 0] == faces[:, 1]) | (faces[:, 1] == faces[:, 2]) | (faces[:, 0] == faces[:, 2])):
        return ["degenerate triangle with a repeated vertex"]
    directed = np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
    pairs, counts = np.unique(directed, axis=0, return_counts=True)
    problems = []
    if np.any(counts != 1):
        problems.append("a directed edge is used more than once")
    forward = {tuple(p) for p in pairs.tolist()}
    if any((b, a) not in forward for a, b in forward):
        problems.append("an edge has no opposite half-edge (open mesh)")
    return problems


def volume_and_centroid(tris: np.ndarray) -> tuple[float, np.ndarray]:
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    signed = np.einsum("ij,ij->i", a, np.cross(b, c)) / 6.0
    volume = float(signed.sum())
    if volume == 0.0:
        return 0.0, np.zeros(3)
    centroid = (signed[:, None] * (a + b + c) / 4.0).sum(axis=0) / volume
    return volume, centroid


def box_fill_fraction(tris: np.ndarray) -> float:
    pts = tris.reshape(-1, 3)
    box = float(np.prod(pts.max(axis=0) - pts.min(axis=0)))
    volume, _ = volume_and_centroid(tris)
    return volume / box if box > 0 else 0.0


def measure_mesh(tris: np.ndarray, density_kg_m3: float) -> dict[str, Any]:
    """Mass properties of a closed mesh; raises MeshError for invalid meshes."""

    problems = closure_problems(tris)
    if problems:
        raise MeshError("; ".join(problems))
    volume, centroid = volume_and_centroid(tris)
    if volume <= 0:
        raise MeshError(f"non-positive volume {volume!r} (inverted mesh?)")
    density = _finite(density_kg_m3, "density")
    if density <= 0:
        raise MeshError("density must be positive")
    pts = tris.reshape(-1, 3)
    lo, hi = pts.min(axis=0), pts.max(axis=0)
    return {
        "volume_m3": volume,
        "mass_kg": volume * density,
        "center_of_mass_m": [float(v) for v in centroid],
        "bbox_min_m": [float(v) for v in lo],
        "bbox_max_m": [float(v) for v in hi],
        "bbox_diagonal_m": float(np.linalg.norm(hi - lo)),
        "box_fill_fraction": box_fill_fraction(tris),
        "triangle_count": int(len(tris)),
    }
