"""Part-resolution and joint-system gates for Work 140.

The detailed vehicle declares three features per part and joins parts with a
parent-child label. This module turns "detailed enough" and "a real joint"
into measured gates. It never requires a particular joining technology: it
requires that whichever technology is declared is backed by geometry that can
be measured on the built solids.
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping, Sequence

PROTOCOL_VERSION = "part_resolution_gate_v1"
FINAL_STATUS = "passed_part_resolution_gate"

PART_STATUSES = (
    "passed_resolution",
    "insufficient_resolution",
    "unmanufacturable_feature",
    "unresolved_measurement",
)
JOINT_STATUSES = (
    "passed_joint_evidence",
    "unsupported_joint_evidence",
    "out_of_range_fit",
    "unresolved_joint_measurement",
)

#: Technology-neutral: the design may join parts however it likes, but the
#: declared technology must be backed by measurable geometry.
JOINT_EVIDENCE = {
    "threaded": ("engagement_faces", "bearing_face", "clearance_in_range"),
    "welded": ("added_fillet_material", "continuous_interface"),
    "bonded": ("bond_line_in_range", "overlap_area"),
    "interference": ("interference_in_range",),
    "integral": ("single_continuous_solid",),
}


class PartResolutionError(ValueError):
    """Raised when a declaration or its measured evidence is invalid."""


def canonical_sha256(value: Any) -> str:
    try:
        payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    except (TypeError, ValueError) as exc:
        raise PartResolutionError("evidence must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()


def _positive(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0.0:
        raise PartResolutionError(f"{label} must be a finite positive number")
    return float(value)


def _count(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise PartResolutionError(f"{label} must be a non-negative integer")
    return value


def validate_protocol(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Fail closed on the declaration before any kernel runs."""

    required = {
        "protocol_version", "units", "runtimes", "resolution", "part_classes",
        "parts", "joints", "controls", "experiment",
    }
    if set(raw) != required or raw.get("protocol_version") != PROTOCOL_VERSION:
        raise PartResolutionError("protocol schema or identity mismatch")
    if raw.get("units") != "SI_m":
        raise PartResolutionError("protocol units mismatch")
    for runtime in raw["runtimes"]:
        if set(runtime) != {"runtime_id", "path", "version"}:
            raise PartResolutionError("runtime identity is invalid")

    resolution = raw["resolution"]
    if set(resolution) != {"minimum_feature_m", "minimum_elements_across_feature", "mesh_size_factor"}:
        raise PartResolutionError("resolution schema is invalid")
    _positive(resolution["minimum_feature_m"], "minimum_feature_m")
    _positive(resolution["mesh_size_factor"], "mesh_size_factor")
    if _count(resolution["minimum_elements_across_feature"], "minimum_elements_across_feature") < 1:
        raise PartResolutionError("at least one element across the smallest feature is required")

    if not raw["part_classes"]:
        raise PartResolutionError("at least one part class is required")
    for class_id, requirement in raw["part_classes"].items():
        if set(requirement) != {"minimum_faces", "minimum_curved_faces", "minimum_distinct_feature_scales", "minimum_edges"}:
            raise PartResolutionError(f"part class {class_id} schema is invalid")
        for key, value in requirement.items():
            _count(value, f"{class_id}.{key}")

    if not raw["parts"]:
        raise PartResolutionError("at least one subject part is required")
    identities: set[str] = set()
    for part in raw["parts"]:
        if set(part) != {"part_id", "part_class", "source", "geometry"}:
            raise PartResolutionError("part schema is invalid")
        if part["part_id"] in identities:
            raise PartResolutionError("part identities are duplicated")
        identities.add(part["part_id"])
        if part["part_class"] not in raw["part_classes"]:
            raise PartResolutionError("part class is not declared")
        geometry = part["geometry"]
        if geometry["kind"] == "step_file":
            if set(geometry) != {"kind", "path"}:
                raise PartResolutionError("step_file geometry schema is invalid")
        elif geometry["kind"] == "reference_build":
            if set(geometry) != {"kind", "builder", "parameters"}:
                raise PartResolutionError("reference_build geometry schema is invalid")
        else:
            raise PartResolutionError("part geometry kind is not declared")

    joint_ids: set[str] = set()
    for joint in raw["joints"]:
        if set(joint) != {"joint_id", "technology", "parts", "placement", "fit_range_m", "minimum_overlap_area_m2"}:
            raise PartResolutionError("joint schema is invalid")
        if joint["joint_id"] in joint_ids:
            raise PartResolutionError("joint identities are duplicated")
        joint_ids.add(joint["joint_id"])
        if joint["technology"] not in JOINT_EVIDENCE:
            raise PartResolutionError(f"joint technology is not in the registry: {joint['technology']}")
        if len(joint["parts"]) != 2 or len(set(joint["parts"])) != 2:
            raise PartResolutionError("a joint connects exactly two distinct parts")
        if any(part_id not in identities for part_id in joint["parts"]):
            raise PartResolutionError("joint references an undeclared part")
        low, high = joint["fit_range_m"]
        if not isinstance(low, (int, float)) or not isinstance(high, (int, float)) or low > high:
            raise PartResolutionError("fit range is invalid")
        if joint["minimum_overlap_area_m2"] < 0.0:
            raise PartResolutionError("minimum overlap area must not be negative")

    controls = raw["controls"]
    if len(controls) != 8 or len(set(controls)) != 8:
        raise PartResolutionError("exactly eight registered controls are required")
    if any(not values for values in raw["experiment"].values()):
        raise PartResolutionError("experiment registration is incomplete")
    return {
        "status": "passed",
        "protocol_sha256": canonical_sha256(raw),
        "part_count": len(raw["parts"]),
        "joint_count": len(raw["joints"]),
        "technologies": sorted({joint["technology"] for joint in raw["joints"]}),
    }


def distinct_feature_scales(measurement: Mapping[str, Any]) -> int:
    """How many decade-separated length scales the part actually exhibits."""

    lengths = [value for value in measurement.get("edge_lengths_m", []) if value > 0.0]
    if not lengths:
        return 0
    decades = {int(math.floor(math.log10(value))) for value in lengths}
    return len(decades)


def evaluate_part(
    part: Mapping[str, Any], requirement: Mapping[str, Any], resolution: Mapping[str, Any],
    measurement: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Return exactly one registered status for one part."""

    if measurement is None or measurement.get("status") != "measured":
        return {
            "part_id": part["part_id"], "status": "unresolved_measurement",
            "cause": (measurement or {}).get("cause", "no measurement evidence"),
        }
    smallest = float(measurement["smallest_feature_m"])
    feature_scale = float(measurement.get("feature_scale_m", smallest))
    scales = distinct_feature_scales(measurement)
    record = {
        "part_id": part["part_id"],
        "part_class": part["part_class"],
        "source": part["source"],
        "face_count": measurement["face_count"],
        "curved_face_count": measurement["curved_face_count"],
        "edge_count": measurement["edge_count"],
        "smallest_feature_m": smallest,
        "feature_scale_m": feature_scale,
        "distinct_feature_scales": scales,
        "surface_types": measurement["surface_types"],
        "volume_m3": measurement["volume_m3"],
    }
    mesh = measurement.get("mesh")
    mesh_failure = None
    if mesh is not None and mesh.get("status") == "meshed":
        record["mesh_node_count"] = mesh["node_count"]
        record["mesh_characteristic_length_m"] = mesh["characteristic_length_m"]
        record["elements_across_feature_scale"] = (
            feature_scale / mesh["characteristic_length_m"] if mesh["characteristic_length_m"] > 0 else 0.0
        )
    elif mesh is not None:
        mesh_failure = mesh.get("cause", "mesh did not complete")
        record["mesh_failure"] = mesh_failure

    # Geometry facts first: whether a part is a sliver or under-modelled does
    # not depend on whether a mesher happened to succeed.
    if smallest < float(resolution["minimum_feature_m"]):
        return {**record, "status": "unmanufacturable_feature",
                "cause": f"smallest feature {smallest} m is below the registered floor"}
    shortfalls = []
    if measurement["face_count"] < requirement["minimum_faces"]:
        shortfalls.append(f"faces {measurement['face_count']} < {requirement['minimum_faces']}")
    if measurement["curved_face_count"] < requirement["minimum_curved_faces"]:
        shortfalls.append(f"curved faces {measurement['curved_face_count']} < {requirement['minimum_curved_faces']}")
    if measurement["edge_count"] < requirement["minimum_edges"]:
        shortfalls.append(f"edges {measurement['edge_count']} < {requirement['minimum_edges']}")
    if scales < requirement["minimum_distinct_feature_scales"]:
        shortfalls.append(f"feature scales {scales} < {requirement['minimum_distinct_feature_scales']}")
    if shortfalls:
        return {**record, "status": "insufficient_resolution", "cause": "; ".join(shortfalls)}
    if mesh_failure is not None:
        return {**record, "status": "unresolved_measurement", "cause": mesh_failure}
    across = record.get("elements_across_feature_scale")
    if across is not None and across < float(resolution["minimum_elements_across_feature"]):
        return {**record, "status": "unresolved_measurement",
                "cause": f"mesh places {across:.2f} elements across the modelled feature scale"}
    return {**record, "status": "passed_resolution", "cause": None}


def evaluate_joint(joint: Mapping[str, Any], measurement: Mapping[str, Any] | None) -> dict[str, Any]:
    """Check the declared technology against what the geometry actually shows."""

    required = JOINT_EVIDENCE[joint["technology"]]
    if measurement is None or measurement.get("status") != "measured":
        return {
            "joint_id": joint["joint_id"], "technology": joint["technology"],
            "status": "unresolved_joint_measurement",
            "cause": (measurement or {}).get("cause", "no measurement evidence"),
            "required_evidence": list(required),
        }
    low, high = (float(value) for value in joint["fit_range_m"])
    clearance = float(measurement["clearance_m"])
    overlap = float(measurement["overlap_area_m2"])
    record = {
        "joint_id": joint["joint_id"],
        "technology": joint["technology"],
        "parts": list(joint["parts"]),
        "clearance_m": clearance,
        "interference_volume_m3": measurement["interference_volume_m3"],
        "overlap_area_m2": overlap,
        "mating_face_pairs": measurement["mating_face_pairs"],
        "engagement_face_count": measurement["engagement_face_count"],
        "engagement_face_counts": measurement.get("engagement_face_counts"),
        "required_evidence": list(required),
    }
    found: list[str] = []
    missing: list[str] = []
    for item in required:
        if item == "engagement_faces":
            # A thread bears on a thread. Where the measurement reports each
            # side, both sides must carry engagement geometry; the pair total
            # is only a fallback for older evidence.
            per_side = measurement.get("engagement_face_counts")
            engaged = min(per_side) >= 1 if per_side else measurement["engagement_face_count"] >= 2
            (found if engaged else missing).append(item)
        elif item == "bearing_face":
            (found if measurement["mating_face_pairs"] >= 1 else missing).append(item)
        elif item in {"clearance_in_range", "bond_line_in_range", "interference_in_range"}:
            (found if low <= clearance <= high else missing).append(item)
        elif item == "overlap_area":
            (found if overlap >= float(joint["minimum_overlap_area_m2"]) else missing).append(item)
        elif item == "added_fillet_material":
            (found if measurement["interference_volume_m3"] > 0.0 else missing).append(item)
        elif item == "continuous_interface":
            (found if measurement["mating_face_pairs"] >= 1 and clearance <= 0.0 else missing).append(item)
        elif item == "single_continuous_solid":
            (found if measurement.get("single_solid") else missing).append(item)
        else:  # pragma: no cover - the registry and this branch are kept in step
            raise PartResolutionError(f"unhandled evidence requirement: {item}")
    record["evidence_found"] = found
    record["evidence_missing"] = missing
    if not missing:
        return {**record, "status": "passed_joint_evidence", "cause": None}
    fit_items = {"clearance_in_range", "bond_line_in_range", "interference_in_range"}
    if set(missing) <= fit_items:
        return {**record, "status": "out_of_range_fit",
                "cause": f"measured fit {clearance} m is outside [{low}, {high}]"}
    return {**record, "status": "unsupported_joint_evidence",
            "cause": f"missing measured evidence: {sorted(missing)}"}


def summarize(parts: Sequence[Mapping[str, Any]], joints: Sequence[Mapping[str, Any]],
              controls: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Aggregate; a failing subject is a finding, a failing control is a defect."""

    part_counts = {status: 0 for status in PART_STATUSES}
    for part in parts:
        if part["status"] not in part_counts:
            raise PartResolutionError(f"part carries an unregistered status: {part['status']}")
        part_counts[part["status"]] += 1
    joint_counts = {status: 0 for status in JOINT_STATUSES}
    for joint in joints:
        if joint["status"] not in joint_counts:
            raise PartResolutionError(f"joint carries an unregistered status: {joint['status']}")
        joint_counts[joint["status"]] += 1
    if sum(part_counts.values()) != len(parts) or sum(joint_counts.values()) != len(joints):
        raise PartResolutionError("status accounting does not close")
    rejected = [control for control in controls if control["rejected"]]
    return {
        "status": FINAL_STATUS if len(rejected) == len(controls) else "failed_controls",
        "part_status_counts": part_counts,
        "joint_status_counts": joint_counts,
        "parts_below_bar": sorted(part["part_id"] for part in parts if part["status"] != "passed_resolution"),
        "joints_without_evidence": sorted(joint["joint_id"] for joint in joints if joint["status"] != "passed_joint_evidence"),
        "controls_rejected": len(rejected),
        "control_count": len(controls),
        "discovery_claim": False,
        "promotion_allowed": False,
        "race_time_claim": False,
        "physical_validation": False,
    }
