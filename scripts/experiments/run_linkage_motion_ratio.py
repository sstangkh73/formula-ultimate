"""Run Work 075 geometry-derived linkage motion-ratio evidence."""

from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
from typing import Any

from formula_ultimate.simulation.coupled_planar_differential import load_coupled_planar_config
from formula_ultimate.simulation.differential_drive_coupling import load_differential_drive_config
from formula_ultimate.simulation.linkage_motion_ratio import (
    LinkageMotionRatioError,
    application_to_mapping,
    apply_linkage_motion_ratios,
    derive_motion_ratio,
    load_linkage_motion_ratio_config,
)
from formula_ultimate.simulation.planar_support_gate import load_support_gate_config, materialize_architecture_variant
from formula_ultimate.simulation.powertrain_dynamics import load_powertrain_config
from formula_ultimate.simulation.sprung_body_vertical_coupling import (
    load_sprung_body_vertical_config,
    result_to_mapping,
    run_sprung_body_vertical_coupling,
)
from formula_ultimate.simulation.transient_suspension_coupling import load_transient_suspension_config
from formula_ultimate.topology.functional_vehicle import functional_declaration_sha256


WORK073_REFERENCE_SHA256 = "802330a0566c746d00beb3f5a6cddb725cfee4a9e9f85e08a8bd509b4a6ce973"


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--vehicle-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    raw = json.loads(args.config.read_text(encoding="utf-8"))
    vertical_raw = json.loads((args.vehicle_root / raw["sprung_body_vertical_source"]).read_text(encoding="utf-8"))
    transient_raw = json.loads((args.vehicle_root / vertical_raw["transient_suspension_source"]).read_text(encoding="utf-8"))
    coupled_raw = json.loads((args.vehicle_root / transient_raw["coupled_planar_source"]).read_text(encoding="utf-8"))
    differential_raw = json.loads((args.vehicle_root / coupled_raw["differential_source"]).read_text(encoding="utf-8"))
    variant_raw = json.loads((args.vehicle_root / differential_raw["architecture_variant_source"]).read_text(encoding="utf-8"))
    base_raw = json.loads((args.vehicle_root / variant_raw["base_architecture_source"]).read_text(encoding="utf-8"))
    support_raw = json.loads((args.vehicle_root / differential_raw["support_gate_source"]).read_text(encoding="utf-8"))
    powertrain_raw = json.loads((args.vehicle_root / differential_raw["powertrain_source"]).read_text(encoding="utf-8"))
    architecture = materialize_architecture_variant(base_raw, variant_raw)
    support = load_support_gate_config(support_raw)
    powertrain = load_powertrain_config(powertrain_raw)
    differential = load_differential_drive_config(differential_raw, powertrain=powertrain, architecture_raw=architecture, support_config=support)
    coupled = load_coupled_planar_config(coupled_raw, differential=differential, architecture_raw=architecture, support_config=support)
    transient = load_transient_suspension_config(transient_raw, coupled=coupled, architecture_raw=architecture)
    vertical = load_sprung_body_vertical_config(vertical_raw, transient=transient, architecture_raw=architecture)

    config = load_linkage_motion_ratio_config(raw)
    application = apply_linkage_motion_ratios(config, vertical)
    replay_application = apply_linkage_motion_ratios(config, vertical)
    reference = run_sprung_body_vertical_coupling(application.transformed_vertical, powertrain, sample_stride=25)
    replay = run_sprung_body_vertical_coupling(replay_application.transformed_vertical, powertrain, sample_stride=25)
    unit_config = load_linkage_motion_ratio_config(raw, geometry_section="unit_ratio_control")
    unit_application = apply_linkage_motion_ratios(unit_config, vertical)
    unit_result = run_sprung_body_vertical_coupling(unit_application.transformed_vertical, powertrain, sample_stride=25)
    fixed = run_sprung_body_vertical_coupling(vertical, powertrain, sample_stride=25)

    mutated_raw = deepcopy(raw)
    mutated_raw["linkages"][0]["spring_pickup_m"] = [0.18, 0.0, 0.0]
    mutated_application = apply_linkage_motion_ratios(load_linkage_motion_ratio_config(mutated_raw), vertical)
    mutated_result = run_sprung_body_vertical_coupling(mutated_application.transformed_vertical, powertrain, sample_stride=25)
    base_linkage = config.linkages[0]
    axis_scaled_ratio = derive_motion_ratio(replace(
        base_linkage, rotation_axis=tuple(5.0 * item for item in base_linkage.rotation_axis)
    )).motion_ratio
    degenerate_rejected = False
    try:
        derive_motion_ratio(replace(base_linkage, wheel_pickup_m=base_linkage.pivot_m))
    except LinkageMotionRatioError:
        degenerate_rejected = True

    ratios = {item.contact_id: item.motion_ratio for item in application.evidence}
    checks = {
        "ratios_geometry_derived": ratios == {"left_ground_contact": 0.7999999999999999, "rear_ground_contact": 1.0, "right_ground_contact": 0.7999999999999999},
        "virtual_work_scaling": all(item.stiffness_scale == item.motion_ratio ** 2 and item.damping_scale == item.motion_ratio ** 2 and item.travel_scale == 1.0 / item.motion_ratio for item in application.evidence),
        "reference_finished": reference.status == "passed" and reference.outcome == "finished",
        "exact_replay": application == replay_application and reference == replay,
        "fixed_work073_unchanged": fixed.result_sha256 == WORK073_REFERENCE_SHA256,
        "unit_ratio_preserves_work073": unit_result.result_sha256 == WORK073_REFERENCE_SHA256 and all(item.motion_ratio == 1.0 for item in unit_application.evidence),
        "geometry_mutation_changes_identity": mutated_application.application_sha256 != application.application_sha256 and mutated_result.result_sha256 != reference.result_sha256,
        "axis_normalization": abs(axis_scaled_ratio - application.evidence[0].motion_ratio) <= config.ratio_absolute_tolerance,
        "degenerate_rejected": degenerate_rejected,
        "energy": reference.maximum_total_global_relative_energy_residual <= config.energy_relative_tolerance,
    }
    payload = {
        "model_version": raw["model_version"],
        "protocol_id": raw["protocol_id"],
        "claim_level": raw["claim_level"],
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "declaration_sha256": _sha256(raw),
        "materialized_architecture_sha256": functional_declaration_sha256(architecture),
        "application": application_to_mapping(application),
        "reference": result_to_mapping(reference),
        "unit_ratio_control": application_to_mapping(unit_application),
        "unit_ratio_result": result_to_mapping(unit_result),
        "geometry_mutation_application": application_to_mapping(mutated_application),
        "geometry_mutation_result": result_to_mapping(mutated_result),
    }
    payload["evidence_sha256"] = _sha256(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(_canonical({
        "status": payload["status"],
        "evidence_sha256": payload["evidence_sha256"],
        "application_sha256": application.application_sha256,
        "result_sha256": reference.result_sha256,
        "motion_ratios": ratios,
        "maximum_heave_m": reference.maximum_abs_heave_m,
        "maximum_travel_m": reference.maximum_abs_suspension_travel_m,
        "minimum_load_n": reference.minimum_actual_normal_load_n,
        "maximum_energy_residual": reference.maximum_total_global_relative_energy_residual,
        "unit_ratio_result_sha256": unit_result.result_sha256,
    }))
    return 0 if payload["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
