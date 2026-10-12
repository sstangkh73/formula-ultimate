"""Post-layout leaf refinement for the functional (goal v2) vehicle (pure Python).

The v1 layout places straight extruded leaves. This step adds one cylindrical
through-bore to a seed-chosen subset of placed leaves. The bore is cut from the
local extruded solid before the placement transforms, so the refined program is
``section -> extrude -> bore -> transforms``.

Local frame (metres, radians): the leaf extrudes along local +z from ``z = 0``
to ``z = h``; ``rho`` is the declared inscribed radius minus the tessellation
tolerance. The bore axis passes through the drawn axis point ``(ox, oy, h/2)``
with direction ``(sin b cos p, sin b sin p, cos b)``. The lateral clearance
rule ``|(ox, oy)| + (h/2) tan b + r / cos b <= (1 - wall) rho`` keeps the bore inside the
inscribed cylinder for ``0 <= z <= h``, so it enters through one end cap,
leaves through the other and never reaches a side wall.

A bore only removes material inside the leaf, so it cannot create new
interpenetration and never grows the leaf box. Contact is kept by rule: each
bore exit on a cap stays clear of every contact patch that the cap receives
from a neighbour (``contact_patches``). Leaves where no draw satisfies the
rules stay unrefined; nothing is clipped silently. An oblique bore makes the
mesh non-prismatic by the acceptance proxy; that is a representation measure,
not a claim about structural purpose.
"""

from __future__ import annotations

import copy
import hashlib
import math
import random
from dataclasses import asdict, dataclass, replace
from typing import Any, Mapping

import numpy as np

from .layout import LayoutResult, leaf_faces
from .leaf_geometry import LEAF_GRAMMAR_VERSION, LeafProgramError, transform_points, validate_leaf_program


REFINED_LEAF_GRAMMAR_VERSION = "func-leaf-bored-v2"
REFINEMENT_VERSION = "func-leaf-refinement-v1"
BORE_FEATURE_ID = "bore"


@dataclass(frozen=True)
class RefinementConfig:
    bore_probability: float = 0.8
    tilt_range_rad: tuple[float, float] = (math.radians(5.0), math.radians(40.0))
    radius_fraction: tuple[float, float] = (0.12, 0.3)
    wall_fraction: float = 0.12
    draws: int = 12


DEFAULT_REFINEMENT_CONFIG = RefinementConfig()


def refinement_config_record(config: RefinementConfig = DEFAULT_REFINEMENT_CONFIG) -> dict[str, Any]:
    return {"version": REFINEMENT_VERSION, "grammar_version": REFINED_LEAF_GRAMMAR_VERSION,
            **{k: list(v) if isinstance(v, tuple) else v for k, v in asdict(config).items()}}


def _derived_seed(*parts: object) -> int:
    text = "|".join(str(p) for p in parts)
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)


# --------------------------------------------------------------------------
# Contact patches
# --------------------------------------------------------------------------

def _face_radius(face: Mapping[str, Any]) -> float:
    if face["kind"] == "disk":
        return float(face["outer"])
    k = face["axis"]
    center = np.asarray(face["center"], dtype=float)
    return float(max(np.linalg.norm(np.delete(c - center, k)) for c in face["corners"]))


def contact_patches(result: LayoutResult) -> dict[str, dict[str, list[tuple[np.ndarray, float]]]]:
    """Per leaf and cap, the (world centre, radius) disks that the cap receives.

    A target cap under a smaller source cap (mode ``inside``) receives the
    source disk. A source cap that holds the target region (mode ``around``)
    receives that region. In the two other cases the leaf's whole face outline
    stays in contact, so no clearance is needed there.
    """

    faces = {leaf.id: leaf_faces(leaf.program)["faces"] for leaf in result.leaves}
    patches: dict[str, dict[str, list[tuple[np.ndarray, float]]]] = {leaf.id: {} for leaf in result.leaves}
    for item in result.interfaces:
        source, target = faces[item.a][item.a_face], faces[item.b][item.b_face]
        if item.mode == "inside" and target["kind"] == "disk":
            patches[item.b].setdefault(item.b_face, []).append(
                (np.asarray(source["center"], dtype=float), _face_radius(source)))
        elif item.mode == "around":
            patches[item.a].setdefault(item.a_face, []).append(
                (np.asarray(target["center"], dtype=float), _face_radius(target)))
    return patches


# --------------------------------------------------------------------------
# Refined programs
# --------------------------------------------------------------------------

def bore_parameters(program: Mapping[str, Any], radius_m: float, tilt_rad: float,
                    azimuth_rad: float, offset_m: tuple[float, float] = (0.0, 0.0)) -> dict[str, Any]:
    """Grammar ``bore`` parameters through the local axis point (ox, oy, h/2)."""

    height = program["contact"]["height_m"]
    direction = [math.sin(tilt_rad) * math.cos(azimuth_rad), math.sin(tilt_rad) * math.sin(azimuth_rad),
                 math.cos(tilt_rad)]
    # Long enough to pass through both caps with room to spare.
    length = 3.0 * height / math.cos(tilt_rad) + 4.0 * radius_m
    origin = [-0.5 * length * d for d in direction]
    origin[0] += float(offset_m[0])
    origin[1] += float(offset_m[1])
    origin[2] += 0.5 * height
    return {"radius_m": float(radius_m), "length_m": float(length), "origin_m": origin,
            "direction": direction}


def bore_program(program: Mapping[str, Any], radius_m: float, tilt_rad: float,
                 azimuth_rad: float, offset_m: tuple[float, float] = (0.0, 0.0)) -> dict[str, Any]:
    """A copy of a placed v1 program with one bore cut before the transforms."""

    validate_leaf_program(program)
    result = copy.deepcopy(dict(program))
    features = result["candidate"]["features"]
    bore = {"feature_id": BORE_FEATURE_ID, "operator": "bore", "inputs": [features[1]["feature_id"]],
            "parameters": bore_parameters(program, radius_m, tilt_rad, azimuth_rad, offset_m)}
    if len(features) > 2:
        features[2]["inputs"] = [BORE_FEATURE_ID]
    else:
        result["candidate"]["final_feature_id"] = BORE_FEATURE_ID
    features.insert(2, bore)
    result["leaf_grammar_version"] = REFINED_LEAF_GRAMMAR_VERSION
    validate_refined_program(result)
    return result


def base_program(program: Mapping[str, Any]) -> dict[str, Any]:
    """The v1 program a refined program was derived from (identity for v1)."""

    if program["leaf_grammar_version"] == LEAF_GRAMMAR_VERSION:
        return copy.deepcopy(dict(program))
    if program["leaf_grammar_version"] != REFINED_LEAF_GRAMMAR_VERSION:
        raise LeafProgramError("unknown leaf grammar version")
    result = copy.deepcopy(dict(program))
    features = result["candidate"]["features"]
    if len(features) < 3 or features[2]["feature_id"] != BORE_FEATURE_ID or features[2]["operator"] != "bore":
        raise LeafProgramError("refined program must have the bore as its third feature")
    features.pop(2)
    if len(features) > 2:
        features[2]["inputs"] = [features[1]["feature_id"]]
    else:
        result["candidate"]["final_feature_id"] = features[1]["feature_id"]
    result["leaf_grammar_version"] = LEAF_GRAMMAR_VERSION
    return result


def bore_exits(program: Mapping[str, Any]) -> dict[str, tuple[np.ndarray, float]]:
    """World exit centre and exit radius bound per cap for a refined program."""

    p = program["candidate"]["features"][2]["parameters"]
    height = program["contact"]["height_m"]
    d = np.asarray(p["direction"], dtype=float)
    shift = 0.5 * height / d[2]
    local = _axis_point(program)[None, :] + np.array([[-shift], [shift]]) * d
    world = transform_points(program, local)
    bound = p["radius_m"] / d[2]
    return {"cap0": (world[0], bound), "cap1": (world[1], bound)}


def _axis_point(program: Mapping[str, Any]) -> np.ndarray:
    """Point of the bore axis on the local mid plane z = h/2."""

    p = program["candidate"]["features"][2]["parameters"]
    d = np.asarray(p["direction"], dtype=float)
    origin = np.asarray(p["origin_m"], dtype=float)
    return origin + (0.5 * program["contact"]["height_m"] - origin[2]) / d[2] * d


def validate_refined_program(program: Mapping[str, Any]) -> None:
    """Check a v1 or refined leaf program, including the bore clearance rule."""

    validate_leaf_program(base_program(program))
    if program["leaf_grammar_version"] == LEAF_GRAMMAR_VERSION:
        return
    feature = program["candidate"]["features"][2]
    if feature["inputs"] != [program["candidate"]["features"][1]["feature_id"]]:
        raise LeafProgramError("bore must cut the extruded body")
    p = feature["parameters"]
    if set(p) != {"radius_m", "length_m", "origin_m", "direction"}:
        raise LeafProgramError("bore fields mismatch")
    d = np.asarray(p["direction"], dtype=float)
    if d.shape != (3,) or not np.all(np.isfinite(d)) or abs(float(np.linalg.norm(d)) - 1.0) > 1e-9 or d[2] <= 0:
        raise LeafProgramError("bore direction must be a unit vector with positive local z")
    height = program["contact"]["height_m"]
    rho = program["contact"]["inscribed_radius_m"] - program["tessellation"]["linear_tolerance_m"]
    radius, length = float(p["radius_m"]), float(p["length_m"])
    tilt = math.acos(min(1.0, float(d[2])))
    point = _axis_point(program)
    lateral = float(math.hypot(point[0], point[1]))
    if not (0 < radius and lateral + 0.5 * height * math.tan(tilt) + radius / math.cos(tilt) < rho):
        raise LeafProgramError("bore does not stay inside the inscribed cylinder")
    # The cylinder must span both caps around the mid-plane axis point.
    t = float((point - np.asarray(p["origin_m"], dtype=float)) @ d)
    reach = 0.5 * height / d[2] + radius * math.tan(tilt)
    if t < reach or length - t < reach:
        raise LeafProgramError("bore does not pass through both caps")


def _try_bore(program: Mapping[str, Any], patches: Mapping[str, list[tuple[np.ndarray, float]]],
              rng: random.Random, config: RefinementConfig) -> dict[str, Any] | None:
    height = program["contact"]["height_m"]
    tol = program["tessellation"]["linear_tolerance_m"]
    rho = program["contact"]["inscribed_radius_m"] - tol
    if rho <= 0:
        return None
    limit = (1.0 - config.wall_fraction) * rho
    for _ in range(config.draws):
        radius = rng.uniform(*config.radius_fraction) * rho
        tilt = rng.uniform(*config.tilt_range_rad)
        azimuth = rng.uniform(0.0, 2 * math.pi)
        room = limit - 0.5 * height * math.tan(tilt) - radius / math.cos(tilt)
        if room < 0:
            continue
        spread, angle = room * math.sqrt(rng.random()), rng.uniform(0.0, 2 * math.pi)
        candidate = bore_program(program, radius, tilt, azimuth,
                                 (spread * math.cos(angle), spread * math.sin(angle)))
        exits = bore_exits(candidate)
        if all(float(np.linalg.norm(exits[cap][0] - center)) >= r + exits[cap][1] + tol
               for cap, items in patches.items() if cap in exits for center, r in items):
            return candidate
    return None


def refine_layout(result: LayoutResult, config: RefinementConfig = DEFAULT_REFINEMENT_CONFIG) -> LayoutResult:
    """The layout with a seed-chosen subset of leaves bored; deterministic per leaf."""

    patches = contact_patches(result)
    leaves = []
    for leaf in result.leaves:
        rng = random.Random(_derived_seed(REFINEMENT_VERSION, result.seed, result.attempt, leaf.id))
        program = None
        if rng.random() < config.bore_probability:
            program = _try_bore(leaf.program, patches[leaf.id], rng, config)
        leaves.append(leaf if program is None else replace(leaf, program=program))
    return replace(result, leaves=tuple(leaves))


def refinement_problems(original: LayoutResult, refined: LayoutResult) -> list[str]:
    """Every violated refinement rule, recomputed from the programs."""

    problems: list[str] = []
    before = original.leaf_map()
    patches = contact_patches(original)
    if [leaf.id for leaf in refined.leaves] != [leaf.id for leaf in original.leaves]:
        return ["refined leaves do not match the layout leaves"]
    if refined.interfaces != original.interfaces:
        problems.append("refinement changed the interfaces")
    for leaf in refined.leaves:
        program = leaf.program
        try:
            validate_refined_program(program)
        except LeafProgramError as exc:
            problems.append(f"{leaf.id}: {exc}")
            continue
        if base_program(program) != before[leaf.id].program:
            problems.append(f"{leaf.id}: refined program is not derived from the placed program")
            continue
        if program["leaf_grammar_version"] == LEAF_GRAMMAR_VERSION:
            continue
        tol = program["tessellation"]["linear_tolerance_m"]
        exits = bore_exits(program)
        for cap, items in patches[leaf.id].items():
            for center, radius in items:
                if float(np.linalg.norm(exits[cap][0] - center)) < radius + exits[cap][1] + tol:
                    problems.append(f"{leaf.id}: bore exit on {cap} overlaps a contact patch")
    return problems
