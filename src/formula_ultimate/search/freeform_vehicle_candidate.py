"""Free-form vehicle candidate composition for Work 139.

A vehicle component may be a box, a cylinder, or an admitted Work 092 free-form
solid. Packaging is gated on the solids that were actually built, and every
component is scored by the Work 138 geometry-general evaluator. A curved shape
earns nothing by being curved.
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping, Sequence

PROTOCOL_VERSION = "freeform_vehicle_candidate_v1"
FINAL_STATUS = "passed_freeform_vehicle_composition"
INCOMPLETE_STATUS = "incomplete_composition"
COMPONENT_KINDS = ("primitive", "freeform_reference")
PRIMITIVE_TYPES = ("box", "cylinder_z")


class FreeformVehicleError(ValueError):
    """Raised when a composition declaration or its built evidence is invalid."""


def canonical_sha256(value: Any) -> str:
    try:
        payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    except (TypeError, ValueError) as exc:
        raise FreeformVehicleError("evidence must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()


def _positive(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0.0:
        raise FreeformVehicleError(f"{label} must be a finite positive number")
    return float(value)


def _point(value: Any, label: str) -> list[float]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) != 3:
        raise FreeformVehicleError(f"{label} must be a 3-vector")
    if any(isinstance(item, bool) or not isinstance(item, (int, float)) or not math.isfinite(item) for item in value):
        raise FreeformVehicleError(f"{label} must be finite")
    return [float(item) for item in value]


def validate_protocol(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Fail closed on the declaration before any CAD kernel runs."""

    required = {
        "protocol_version", "units", "runtimes", "corpus", "envelope", "keep_outs",
        "required_function_tags", "materials", "packaging", "evaluation", "candidates",
        "controls", "experiment",
    }
    if set(raw) != required or raw.get("protocol_version") != PROTOCOL_VERSION:
        raise FreeformVehicleError("protocol schema or identity mismatch")
    if raw.get("units") != "SI_m_kg_s_N_Pa":
        raise FreeformVehicleError("protocol units mismatch")

    corpus = raw["corpus"]
    if set(corpus) != {"solid_config", "wire_config", "declaration_sha256", "admitted_candidate_ids"}:
        raise FreeformVehicleError("corpus reference schema is invalid")
    if not isinstance(corpus["declaration_sha256"], str) or len(corpus["declaration_sha256"]) != 64:
        raise FreeformVehicleError("corpus declaration identity must be SHA-256")
    admitted = corpus["admitted_candidate_ids"]
    if not admitted or len(set(admitted)) != len(admitted):
        raise FreeformVehicleError("admitted corpus identities are missing or duplicated")

    envelope = raw["envelope"]
    if set(envelope) != {"minimum_m", "maximum_m"}:
        raise FreeformVehicleError("envelope schema is invalid")
    low, high = _point(envelope["minimum_m"], "envelope minimum"), _point(envelope["maximum_m"], "envelope maximum")
    if any(first >= second for first, second in zip(low, high)):
        raise FreeformVehicleError("envelope is degenerate")
    for keep_out in raw["keep_outs"]:
        if set(keep_out) != {"keep_out_id", "minimum_m", "maximum_m"}:
            raise FreeformVehicleError("keep-out schema is invalid")
        _point(keep_out["minimum_m"], "keep-out minimum")
        _point(keep_out["maximum_m"], "keep-out maximum")
    if not raw["required_function_tags"]:
        raise FreeformVehicleError("at least one required function tag must be declared")

    for material_id, material in raw["materials"].items():
        if set(material) != {"density_kg_m3", "evidence_class"}:
            raise FreeformVehicleError(f"material {material_id} schema is invalid")
        _positive(material["density_kg_m3"], "density_kg_m3")
        if material["evidence_class"] not in {"synthetic_geometry_only", "measured"}:
            raise FreeformVehicleError(f"material {material_id} evidence class is invalid")

    packaging = raw["packaging"]
    if set(packaging) != {"maximum_pairwise_intersection_m3", "minimum_keep_out_clearance_m", "declared_mass_relative"}:
        raise FreeformVehicleError("packaging schema is invalid")
    for key, value in packaging.items():
        _positive(value, key)

    evaluation = raw["evaluation"]
    if set(evaluation) != {"protocol_version", "units", "runtimes", "materials", "mesh_levels", "convergence", "budget", "residuals", "controls", "experiment"}:
        raise FreeformVehicleError("embedded evaluation template schema is invalid")

    candidates = raw["candidates"]
    if len(candidates) < 2:
        raise FreeformVehicleError("a matched comparison needs at least two candidates")
    seen: set[str] = set()
    for candidate in candidates:
        if set(candidate) != {"candidate_id", "role", "components"}:
            raise FreeformVehicleError("candidate schema is invalid")
        if candidate["candidate_id"] in seen:
            raise FreeformVehicleError("candidate identities are duplicated")
        seen.add(candidate["candidate_id"])
        if candidate["role"] not in {"primitive_baseline", "freeform_variant"}:
            raise FreeformVehicleError("candidate role is not declared")
        validate_components(raw, candidate)
    if {candidate["role"] for candidate in candidates} != {"primitive_baseline", "freeform_variant"}:
        raise FreeformVehicleError("both a primitive baseline and a free-form variant are required")

    controls = raw["controls"]
    if len(controls) != 8 or len(set(controls)) != 8:
        raise FreeformVehicleError("exactly eight registered controls are required")
    if any(not values for values in raw["experiment"].values()):
        raise FreeformVehicleError("experiment registration is incomplete")
    return {
        "status": "passed",
        "protocol_sha256": canonical_sha256(raw),
        "candidate_count": len(candidates),
        "freeform_component_count": sum(
            1 for candidate in candidates for component in candidate["components"]
            if component["geometry"]["kind"] == "freeform_reference"
        ),
    }


def validate_components(raw: Mapping[str, Any], candidate: Mapping[str, Any]) -> None:
    components = candidate["components"]
    if not components:
        raise FreeformVehicleError("a candidate needs at least one component")
    identities: set[str] = set()
    tags: set[str] = set()
    for component in components:
        if set(component) != {"component_id", "function_tags", "material_id", "geometry", "placement", "load_case"}:
            raise FreeformVehicleError("component schema is invalid")
        if component["component_id"] in identities:
            raise FreeformVehicleError("component identities are duplicated")
        identities.add(component["component_id"])
        if not component["function_tags"]:
            raise FreeformVehicleError("every component must declare a function tag")
        tags.update(component["function_tags"])
        if component["material_id"] not in raw["materials"]:
            raise FreeformVehicleError("component material is not declared")
        geometry = component["geometry"]
        if geometry["kind"] not in COMPONENT_KINDS:
            raise FreeformVehicleError("component geometry kind is not declared")
        if geometry["kind"] == "primitive":
            if set(geometry) != {"kind", "primitive_type", "dimensions_m"}:
                raise FreeformVehicleError("primitive geometry schema is invalid")
            if geometry["primitive_type"] not in PRIMITIVE_TYPES:
                raise FreeformVehicleError("primitive type is not declared")
            expected = 3 if geometry["primitive_type"] == "box" else 2
            dimensions = geometry["dimensions_m"]
            if len(dimensions) != expected or any(not isinstance(value, (int, float)) or value <= 0 for value in dimensions):
                raise FreeformVehicleError("primitive dimensions are invalid")
        else:
            if set(geometry) != {"kind", "corpus_candidate_id"}:
                raise FreeformVehicleError("free-form geometry schema is invalid")
            if geometry["corpus_candidate_id"] not in raw["corpus"]["admitted_candidate_ids"]:
                raise FreeformVehicleError("free-form component is not an admitted corpus member")
        placement = component["placement"]
        if set(placement) != {"translation_m", "rotation_deg_xyz"}:
            raise FreeformVehicleError("placement schema is invalid")
        _point(placement["translation_m"], "placement translation")
        _point(placement["rotation_deg_xyz"], "placement rotation")
        load_case = component["load_case"]
        if set(load_case) != {"case_id", "boundary", "selection", "force_n"}:
            raise FreeformVehicleError("component load case schema is invalid")
        _point(load_case["force_n"], "component force")
        if math.fsum(abs(value) for value in load_case["force_n"]) <= 0.0:
            raise FreeformVehicleError("component force must not be zero")
    missing = sorted(set(raw["required_function_tags"]) - tags)
    if missing:
        raise FreeformVehicleError(f"required function tags are unsupported: {missing}")


def matched_difference(raw: Mapping[str, Any]) -> dict[str, Any]:
    """The baseline and the variant must differ in exactly one component."""

    by_role = {candidate["role"]: candidate for candidate in raw["candidates"]}
    baseline = {item["component_id"]: item for item in by_role["primitive_baseline"]["components"]}
    variant = {item["component_id"]: item for item in by_role["freeform_variant"]["components"]}
    if set(baseline) != set(variant):
        raise FreeformVehicleError("matched candidates must declare the same component identities")
    changed = sorted(
        component_id for component_id in baseline
        if canonical_sha256(baseline[component_id]) != canonical_sha256(variant[component_id])
    )
    if len(changed) != 1:
        raise FreeformVehicleError("matched candidates must differ in exactly one component")
    substituted = variant[changed[0]]
    if substituted["geometry"]["kind"] != "freeform_reference":
        raise FreeformVehicleError("the substituted component must be the free-form one")
    return {
        "changed_component_id": changed[0],
        "corpus_candidate_id": substituted["geometry"]["corpus_candidate_id"],
        "baseline_geometry": baseline[changed[0]]["geometry"],
    }


def check_packaging(raw: Mapping[str, Any], manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Gate packaging on measurements taken from the built solids."""

    packaging = raw["packaging"]
    envelope = raw["envelope"]
    findings: list[str] = []
    for component in manifest["components"]:
        if not component["valid"] or component["solid_count"] != 1:
            findings.append(f"{component['component_id']} is not one valid solid")
        box = component["bounding_box_m"]
        for index in range(3):
            if box["minimum"][index] < envelope["minimum_m"][index] or box["maximum"][index] > envelope["maximum_m"][index]:
                findings.append(f"{component['component_id']} leaves the declared envelope")
                break
    worst_intersection = max((item["intersection_m3"] for item in manifest["pairwise_intersections"]), default=0.0)
    if worst_intersection > float(packaging["maximum_pairwise_intersection_m3"]):
        findings.append("components intersect above the declared tolerance")
    worst_keep_out = min((item["intersection_m3"] for item in manifest["keep_out_intersections"]), default=0.0)
    invaded = [item for item in manifest["keep_out_intersections"] if item["intersection_m3"] > 0.0]
    if invaded:
        findings.append(f"keep-out invaded by {sorted(item['component_id'] for item in invaded)}")
    declared = manifest.get("declared_mass_kg")
    if declared is not None:
        measured = float(manifest["mass_kg"])
        residual = abs(measured - float(declared)) / max(abs(measured), abs(float(declared)), 1e-30)
        if residual > float(packaging["declared_mass_relative"]):
            findings.append("declared mass contradicts the built geometry")
    return {
        "status": "passed" if not findings else "failed",
        "findings": findings,
        "maximum_pairwise_intersection_m3": worst_intersection,
        "minimum_keep_out_intersection_m3": worst_keep_out,
        "component_count": len(manifest["components"]),
        "mass_kg": manifest["mass_kg"],
    }


def evaluation_protocol(raw: Mapping[str, Any], candidate: Mapping[str, Any], manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Build the Work 138 protocol that scores each component of this candidate."""

    by_id = {item["component_id"]: item for item in manifest["components"]}
    template = json.loads(json.dumps(raw["evaluation"]))
    candidates = []
    for component in candidate["components"]:
        built = by_id.get(component["component_id"])
        if built is None:
            raise FreeformVehicleError(f"component {component['component_id']} was not built")
        load_case = component["load_case"]
        candidates.append({
            "candidate_id": f"{candidate['candidate_id']}__{component['component_id']}",
            "source": f"{PROTOCOL_VERSION}:{candidate['candidate_id']}:{component['geometry']['kind']}",
            "geometry": {"kind": "step_file", "path": built["step_path"]},
            "material_id": component["material_id"],
            "length_unit_m": 0.001,
            "boundary": load_case["boundary"],
            "load_cases": [{
                "case_id": load_case["case_id"],
                "selection": load_case["selection"],
                "force_n": load_case["force_n"],
            }],
            "declared_mass_kg": built["mass_kg"],
        })
    template["candidates"] = candidates
    return template


def summarize(candidates: Sequence[Mapping[str, Any]], controls: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Aggregate; nothing may vanish, and no result here is a discovery."""

    rejected = [control for control in controls if control["rejected"]]
    packaging_failed = [item["candidate_id"] for item in candidates if item["packaging"]["status"] != "passed"]
    unsupported = [
        item["candidate_id"] for item in candidates
        if any(component["status"] == "unsupported_representation" for component in item["components"])
    ]
    unresolved = sorted(
        (item["candidate_id"], component["candidate_id"], component["status"], component.get("cause"))
        for item in candidates for component in item["components"]
        if component["status"].startswith("unresolved_")
    )
    status = FINAL_STATUS
    if packaging_failed or unsupported:
        status = INCOMPLETE_STATUS
    elif len(rejected) != len(controls):
        status = "failed_controls"
    return {
        "status": status,
        "packaging_failed": packaging_failed,
        "unsupported_components": unsupported,
        "unresolved_components": unresolved,
        "controls_rejected": len(rejected),
        "control_count": len(controls),
        "discovery_claim": False,
        "promotion_allowed": False,
        "race_time_claim": False,
        "physical_validation": False,
    }


def matched_report(candidates: Sequence[Mapping[str, Any]], difference: Mapping[str, Any]) -> dict[str, Any]:
    """State the pair side by side, and state what it cannot establish."""

    by_role = {item["role"]: item for item in candidates}
    baseline, variant = by_role["primitive_baseline"], by_role["freeform_variant"]

    def component_of(candidate: Mapping[str, Any]) -> Mapping[str, Any] | None:
        target = f"{candidate['candidate_id']}__{difference['changed_component_id']}"
        return next((item for item in candidate["components"] if item["candidate_id"] == target), None)

    baseline_component, variant_component = component_of(baseline), component_of(variant)
    return {
        "changed_component_id": difference["changed_component_id"],
        "corpus_candidate_id": difference["corpus_candidate_id"],
        "baseline_mass_kg": baseline["packaging"]["mass_kg"],
        "variant_mass_kg": variant["packaging"]["mass_kg"],
        "mass_difference_kg": variant["packaging"]["mass_kg"] - baseline["packaging"]["mass_kg"],
        "baseline_component_status": baseline_component["status"] if baseline_component else None,
        "variant_component_status": variant_component["status"] if variant_component else None,
        "baseline_component_utilization": (baseline_component or {}).get("utilization"),
        "variant_component_utilization": (variant_component or {}).get("utilization"),
        "interpretation": (
            "matched evaluation of one component substitution under one declared load case; "
            "it establishes that a free-form component is composable and scorable, and it "
            "establishes no superiority, discovery or promotion"
        ),
    }
