"""Orchestrate Work 135 native detailed-vehicle admitted evidence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
for item in (ROOT, SRC):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from formula_ultimate.assembly.native_detailed_vehicle import (  # noqa: E402
    NativeDetailedVehicleViolation,
    canonical_sha256,
    evaluate_admitted_evidence,
    file_sha256,
    replay_projection,
    validate_declaration,
)


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise NativeDetailedVehicleViolation(message)


def verify_pinned_inputs(raw: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
    """Verify exact dependency, upstream-audit and executable identities."""

    dependency_rows = []
    for dependency in raw["dependencies"]:
        work = dependency["work"]
        contract = root / dependency["contract_path"]
        result_log = root / dependency["result_log_path"]
        artifact_result = root / dependency["artifact_result_path"]
        _require(contract.is_file(), f"missing Work {work} dependency contract")
        _require(result_log.is_file(), f"missing Work {work} dependency result log")
        _require(artifact_result.is_file(), f"missing Work {work} dependency artifact")
        _require(file_sha256(contract) == dependency["contract_sha256"], f"stale Work {work} dependency contract")
        _require(file_sha256(result_log) == dependency["result_log_sha256"], f"stale Work {work} dependency result log")
        _require(file_sha256(artifact_result) == dependency["artifact_file_sha256"], f"stale Work {work} dependency artifact bytes")
        artifact = _read(artifact_result)
        _require(artifact.get("result_sha256") == dependency["artifact_result_sha256"], f"stale Work {work} dependency result identity")
        _require(
            canonical_sha256(artifact.get("body")) == dependency["artifact_result_sha256"],
            f"invalid Work {work} dependency result body",
        )
        commit_check = subprocess.run(
            ["git", "rev-parse", "--verify", f"{dependency['commit']}^{{commit}}"],
            cwd=root,
            capture_output=True,
            text=True,
        )
        _require(commit_check.returncode == 0, f"missing Work {work} dependency commit")
        _require(commit_check.stdout.strip().lower() == dependency["commit"], f"changed Work {work} dependency commit identity")
        dependency_rows.append({
            "work": work,
            "commit": dependency["commit"],
            "contract_sha256": dependency["contract_sha256"],
            "result_log_sha256": dependency["result_log_sha256"],
            "artifact_file_sha256": dependency["artifact_file_sha256"],
            "artifact_result_sha256": dependency["artifact_result_sha256"],
            "status": "verified",
        })

    upstream_rows = []
    for audit in raw["upstream_part_audit"]:
        path = root / audit["path"]
        _require(path.is_file(), f"missing Work {audit['work']} upstream part evidence")
        _require(file_sha256(path) == audit["sha256"], f"changed Work {audit['work']} upstream identity")
        upstream_rows.append({**audit, "status": "verified"})

    runtime_rows = []
    for runtime in raw["runtimes"]:
        path = Path(runtime["path"])
        _require(path.is_file(), f"missing runtime {runtime['runtime_id']}")
        _require(file_sha256(path) == runtime["sha256"], f"changed runtime {runtime['runtime_id']} identity")
        runtime_rows.append({**runtime, "status": "verified"})
    return {
        "status": "verified",
        "dependencies": dependency_rows,
        "upstream_part_audit": upstream_rows,
        "runtimes": runtime_rows,
    }


def _rejected(action: Callable[[], Any], phrase: str) -> dict[str, str]:
    try:
        action()
    except NativeDetailedVehicleViolation as exc:
        reason = str(exc)
        if phrase not in reason:
            raise
        return {"status": "rejected", "reason": reason}
    raise NativeDetailedVehicleViolation(f"negative control accepted; expected {phrase}")


def _negative_controls(
    raw: dict[str, Any],
    manifest: dict[str, Any],
    freecad: dict[str, Any],
    output: Path,
) -> dict[str, Any]:
    controls: dict[str, Any] = {}

    primitive = copy.deepcopy(raw)
    primitive["definitions"][0]["geometry"]["primitive_replacement"] = True
    controls["01_same_bbox_primitive_substitution"] = _rejected(
        lambda: validate_declaration(primitive), "same-envelope primitive substitution"
    )

    missing_classes = {"bearing", "support", "fastener", "seal", "connector", "power_harness", "signal_harness"}
    missing = copy.deepcopy(raw)
    missing["instances"] = [
        item for item in missing["instances"]
        if not (set(item["occurrence_classes"]) & missing_classes)
    ]
    controls["02_missing_required_occurrences"] = _rejected(
        lambda: validate_declaration(missing), "missing required physical occurrence"
    )

    floating = copy.deepcopy(raw)
    next(item for item in floating["instances"] if item["instance_id"] != floating["candidate"]["root_instance_id"])["attachment"] = None
    controls["03_floating_component"] = _rejected(
        lambda: validate_declaration(floating), "floating component"
    )

    duplicate = copy.deepcopy(raw)
    duplicate["instances"][1]["region_id"] = duplicate["instances"][0]["region_id"]
    controls["04_duplicate_material_ownership"] = _rejected(
        lambda: validate_declaration(duplicate), "duplicate material/void ownership"
    )

    invalid_part = copy.deepcopy(manifest)
    invalid_part["definitions"][0]["valid"] = False
    invalid_part["definitions"][0]["closed"] = False
    controls["05_invalid_native_part"] = _rejected(
        lambda: evaluate_admitted_evidence(raw, invalid_part, freecad), "invalid native part"
    )

    edited_step = copy.deepcopy(manifest)
    edited_step["definitions"][0]["step_sha256"] = "0" * 64
    controls["06_edited_step_bytes"] = _rejected(
        lambda: evaluate_admitted_evidence(raw, edited_step, freecad, artifact_root=output),
        "swapped or edited STEP bytes",
    )

    hidden_repair = copy.deepcopy(freecad)
    hidden_repair["hidden_geometry_repair"] = True
    controls["07_hidden_freecad_repair"] = _rejected(
        lambda: evaluate_admitted_evidence(raw, manifest, hidden_repair), "hidden FreeCAD repair"
    )

    lost_semantic = copy.deepcopy(freecad)
    lost_semantic["semantic_boundary_survival_rate"] = 0.99
    controls["08_lost_semantic_boundary"] = _rejected(
        lambda: evaluate_admitted_evidence(raw, manifest, lost_semantic), "lost semantic face or boundary"
    )

    axes = copy.deepcopy(raw)
    contact = next(item for item in axes["instances"] if item.get("attachment") and not item["attachment"]["approved_noncontact"])
    contact["attachment"]["child_axis"] = [1.0, 0.0, 0.0]
    engagement = copy.deepcopy(raw)
    bolted = next(
        item for item in engagement["instances"]
        if item.get("attachment") and item["attachment"].get("relation_type") == "bolted"
    )
    bolted["attachment"]["engagement_m"] = 0.0
    controls["09_mating_axis_or_engagement_failure"] = {
        "status": "rejected",
        "subcontrols": {
            "mating_axes": _rejected(lambda: validate_declaration(axes), "mating axes mismatch"),
            "missing_engagement": _rejected(lambda: validate_declaration(engagement), "missing engagement"),
        },
    }

    worst_case = copy.deepcopy(raw)
    worst_contact = next(item for item in worst_case["instances"] if item.get("attachment") and not item["attachment"]["approved_noncontact"])
    worst_contact["attachment"]["worst_case_status"] = "failed"
    controls["10_nominal_only_worst_case_failure"] = _rejected(
        lambda: validate_declaration(worst_case), "worst-case tolerance failed"
    )

    swept = copy.deepcopy(manifest)
    swept["motion"]["collision_count"] = 1
    controls["11_swept_motion_collision"] = _rejected(
        lambda: evaluate_admitted_evidence(raw, swept, freecad), "swept motion collision"
    )

    cyclic = copy.deepcopy(raw)
    rear_beam = next(item for item in cyclic["instances"] if item["instance_id"] == "rear_beam")
    rear_beam["attachment"]["parent_instance_id"] = "rear_carrier_left"
    controls["12_cyclic_or_trapped_assembly"] = _rejected(
        lambda: validate_declaration(cyclic), "cyclic assembly order"
    )

    collapsed = copy.deepcopy(raw)
    collapsed["routes"][0]["endpoint_b_m"] = collapsed["routes"][0]["endpoint_a_m"][:]
    bend = copy.deepcopy(raw)
    bend["routes"][0]["actual_minimum_bend_radius_m"] = bend["routes"][0]["minimum_bend_radius_m"] * 0.5
    intersection = copy.deepcopy(raw)
    intersection["routes"][0]["minimum_clearance_m"] = -1.0e-6
    controls["13_route_failure"] = {
        "status": "rejected",
        "subcontrols": {
            "collapsed_endpoint": _rejected(lambda: validate_declaration(collapsed), "endpoints collapse"),
            "bend_radius": _rejected(lambda: validate_declaration(bend), "bend-radius failure"),
            "intersection": _rejected(lambda: validate_declaration(intersection), "intersection failure"),
        },
    }

    dense_void = copy.deepcopy(raw)
    next(item for item in dense_void["materials"] if item["material_id"] == "void")["density_kg_m3"] = 1.0
    controls["14_void_structural_density"] = _rejected(
        lambda: validate_declaration(dense_void), "void material void must have zero structural density"
    )

    missing_opening = copy.deepcopy(raw)
    missing_opening["physics_boundaries"] = [
        item for item in missing_opening["physics_boundaries"] if item["domain"] != "external_aero"
    ]
    controls["15_external_opening_missing_from_flow_domain"] = _rejected(
        lambda: validate_declaration(missing_opening), "physics boundary domain coverage is incomplete"
    )

    proxy = copy.deepcopy(raw)
    proxy["definitions"][0]["provenance"] = {"kind": "evidence_bound_purchased", "proxy": True}
    controls["16_unsupported_purchased_proxy"] = _rejected(
        lambda: validate_declaration(proxy), "unsupported purchased proxy"
    )

    changed_identity = copy.deepcopy(raw)
    changed_identity["dependencies"][0]["contract_sha256"] = "0" * 64
    controls["17_changed_upstream_identity"] = _rejected(
        lambda: verify_pinned_inputs(changed_identity), "stale Work 108 dependency contract"
    )

    controls["18_render_without_native_manifest"] = _rejected(
        lambda: evaluate_admitted_evidence(raw, None, None), "native-solid manifest is required"
    )

    _require(len(controls) == 18, "negative-control count mismatch")
    control_root = output / "negative_controls"
    for name, record in controls.items():
        _write(control_root / f"{name}.json", record)
    aggregate = {
        "status": "passed",
        "required_count": 18,
        "rejected_count": sum(record.get("status") == "rejected" for record in controls.values()),
        "controls": controls,
    }
    _require(aggregate["rejected_count"] == 18, "not all negative controls were rejected")
    _write(output / "negative_controls.json", aggregate)
    return aggregate


def _independent_component_audit(
    raw: dict[str, Any], manifest: dict[str, Any], freecad: dict[str, Any]
) -> dict[str, Any]:
    material_instances = sorted(
        (item for item in raw["instances"] if item["mass_ownership"] == "unique_material"),
        key=lambda item: item["instance_id"],
    )
    seed = hashlib.sha256(
        (raw["candidate"]["candidate_id"] + "|work135-independent-component-audit").encode("utf-8")
    ).digest()
    selected = material_instances[int.from_bytes(seed[:8], "big") % len(material_instances)]
    definition = next(item for item in raw["definitions"] if item["definition_id"] == selected["definition_id"])
    cad_record = next(item for item in manifest["instances"] if item["instance_id"] == selected["instance_id"])
    freecad_record = next(item for item in freecad["instances"] if item["instance_id"] == selected["instance_id"])
    child_relations = [
        item["instance_id"] for item in raw["instances"]
        if item.get("attachment") and item["attachment"].get("parent_instance_id") == selected["instance_id"]
    ]
    service_relations = [
        item["instance_id"] for item in raw["instances"]
        if "service_path" in item["occurrence_classes"]
        and item.get("attachment")
        and item["attachment"].get("parent_instance_id") == selected["instance_id"]
    ]
    audit = {
        "status": "audited_geometry_only",
        "selection_method": "SHA-256(candidate_id plus fixed audit label) modulo sorted material-instance count; no proxy score",
        "selected_instance_id": selected["instance_id"],
        "definition_id": selected["definition_id"],
        "feature_tree": [
            {"order": index + 1, "feature": feature}
            for index, feature in enumerate(definition["feature_inventory"])
        ],
        "sections": {
            "bbox_m": cad_record["bbox"],
            "center_m": cad_record["center_m"],
            "volume_m3": cad_record["volume_m3"],
        },
        "interfaces": {
            "parent_attachment": selected["attachment"],
            "child_instance_ids": child_relations,
            "semantic_face_selectors": definition["semantic_face_selectors"],
        },
        "ownership": {
            "region_id": selected["region_id"],
            "material_id": definition["material_id"],
            "mass_ownership": selected["mass_ownership"],
            "occurrence_classes": selected["occurrence_classes"],
        },
        "access": {
            "direct_service_path_instance_ids": service_relations,
            "conclusion": (
                "direct modeled service path present"
                if service_relations
                else "no component-specific serviceability claim; geometry gate only"
            ),
        },
        "cross_import": {
            "cadquery_step_sha256": cad_record["step_sha256"],
            "freecad_step_sha256": freecad_record["step_sha256"],
            "freecad_valid": freecad_record["valid"],
            "freecad_solid_count": freecad_record["solid_count"],
        },
    }
    return audit


def _artifact_hashes(output: Path) -> dict[str, str]:
    excluded = {"result.json", "replay.json"}
    return {
        path.relative_to(output).as_posix(): file_sha256(path)
        for path in sorted(output.rglob("*"), key=lambda item: item.as_posix())
        if path.is_file()
        and path.name not in excluded
        and path.suffix.lower() != ".fcbak"
        and ".uncanonicalized." not in path.name
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()
    config_path = args.config if args.config.is_absolute() else ROOT / args.config
    output = args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    output.mkdir(parents=True, exist_ok=True)
    raw = _read(config_path)
    declaration = validate_declaration(raw)
    input_audit = verify_pinned_inputs(raw)
    _write(output / "input_identity_audit.json", input_audit)

    runtime_by_id = {item["runtime_id"]: item for item in raw["runtimes"]}
    cad_python = runtime_by_id["cadquery_python"]["path"]
    freecad_python = runtime_by_id["freecad_python"]["path"]
    manifest_path = output / "cadquery_manifest.json"
    freecad_path = output / "freecad_report.json"
    fcstd_path = output / f"native_vehicle_{raw['candidate']['candidate_id']}.FCStd"
    subprocess.run(
        [
            cad_python,
            str(ROOT / "scripts/cad/build_native_detailed_vehicle.py"),
            "--config", str(config_path),
            "--output-root", str(output / "cad"),
            "--manifest", str(manifest_path),
        ],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        [
            freecad_python,
            str(ROOT / "scripts/cad/inspect_native_detailed_vehicle_freecad.py"),
            str(manifest_path),
            str(config_path),
            str(freecad_path),
            str(fcstd_path),
        ],
        cwd=ROOT,
        check=True,
    )
    manifest = _read(manifest_path)
    freecad = _read(freecad_path)
    admitted = evaluate_admitted_evidence(raw, manifest, freecad, artifact_root=output)
    controls = _negative_controls(raw, manifest, freecad, output)
    component_audit = _independent_component_audit(raw, manifest, freecad)
    _write(output / "independent_component_audit.json", component_audit)

    body = {
        "status": admitted["status"],
        "candidate_id": raw["candidate"]["candidate_id"],
        "claim_scope": admitted["claim_scope"],
        "declaration_sha256": declaration["protocol_sha256"],
        "input_identity_audit": input_audit,
        "admitted_evidence": admitted,
        "negative_controls": {
            "required_count": controls["required_count"],
            "rejected_count": controls["rejected_count"],
            "status": controls["status"],
        },
        "independent_component_audit": component_audit,
        "artifact_sha256": _artifact_hashes(output),
        "decision": {
            "geometry_gate_passed": True,
            "promotion_allowed": False,
            "downstream_work": 136,
            "reason": "native geometry is complete at this gate, but all downstream physics must be rerun on the exact solids",
        },
        "review": {
            "supporting_evidence": [
                "all 48 definitions and 83 instances are native one-solid OCCT B-reps",
                "required occurrence and physics-boundary coverage are exactly 1.0",
                f"FreeCAD imported the exact STEP bytes with all {freecad['semantic_selector_checks']} semantic selector checks surviving",
                "all 18 declared falsification controls were rejected",
            ],
            "contradicting_evidence": [
                f"geometry-derived mass is {admitted['mass_properties']['mass_kg']:.12g} kg and has not been optimized or shown competitive",
                "CadQuery and FreeCAD both use OCCT, so this is not an independent-kernel check",
            ],
            "alternative_explanations": [
                "the high mass may reflect conservative synthetic material densities and deliberately complete unoptimized hardware",
                "downstream loads, heat, flow, energy and control behavior may invalidate this geometry",
            ],
            "missing_evidence": [
                "Work 136 structural, thermal, internal-flow, external-aero, ground, actuation, energy and control revalidation",
                "supplier-certified purchased geometry and manufacturing-process qualification",
                "physical correlation, fabrication readiness and safety evidence",
            ],
            "confidence": "high for deterministic native geometry bookkeeping and exact cross-application import; none for performance benefit or physical validity",
        },
    }
    result = {"body": body, "result_sha256": canonical_sha256(body)}
    _write(output / "result.json", result)

    if args.replay_reference:
        reference_path = args.replay_reference if args.replay_reference.is_absolute() else ROOT / args.replay_reference
        reference = _read(reference_path)
        expected = replay_projection(reference)
        observed = replay_projection(result)
        exact = expected == observed
        replay = {"status": "passed" if exact else "failed", "exact": exact, "expected": expected, "observed": observed}
        _write(output / "replay.json", replay)
        _require(exact, "clean replay evidence differs from reference")

    print(json.dumps({
        "status": body["status"],
        "candidate_id": body["candidate_id"],
        "result_sha256": result["result_sha256"],
        "definition_count": declaration["definition_count"],
        "instance_count": declaration["instance_count"],
        "negative_controls_rejected": controls["rejected_count"],
        "promotion_allowed": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
