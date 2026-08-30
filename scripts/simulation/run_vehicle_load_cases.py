#!/usr/bin/env python3
"""Run the Work 048 whole-vehicle load-case acceptance experiment."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import traceback


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.simulation.vehicle_load_cases import (  # noqa: E402
    VehicleLoadCaseError,
    canonical_sha256,
    evaluate_all_load_cases,
    validate_protocol,
)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(stage: str, command: list[str]) -> dict:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    evidence = {
        "stage": stage,
        "command": command,
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    if completed.returncode:
        raise VehicleLoadCaseError(f"{stage} failed with exit {completed.returncode}: {completed.stderr.strip()}")
    return evidence


def rejected(control_id: str, action, text: str) -> dict:
    try:
        action()
    except (KeyError, TypeError, ValueError, VehicleLoadCaseError) as exc:
        if text.lower() not in str(exc).lower():
            raise
        return {"control_id": control_id, "status": "rejected_as_expected", "reason": str(exc)}
    raise VehicleLoadCaseError(f"negative control {control_id} was admitted")


def maximum_relative_mass_error(actual: dict, expected: dict) -> float:
    pairs = [(actual["mass_kg"], expected["mass_kg"])]
    pairs.extend(zip(actual["centre_of_mass_m"], expected["centre_of_mass_m"]))
    pairs.extend(zip(actual["inertia_kg_m2"], expected["inertia_kg_m2"]))
    return max(abs(float(a) - float(b)) / max(abs(float(b)), 1.0e-300) for a, b in pairs)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=ROOT / "config/vehicle/whole_vehicle_load_cases_v1.json")
    parser.add_argument("--assembly", type=Path, default=ROOT / "config/vehicle/topology_neutral_vehicle_v1.json")
    parser.add_argument("--failure", type=Path, default=ROOT / "config/simulation/structural_failure_coupling_v1.json")
    parser.add_argument("--artifact-root", type=Path, default=ROOT / "artifacts/work048")
    parser.add_argument("--cadquery-python", type=Path, default=ROOT / ".tools/cadquery-mcp/Scripts/python.exe")
    parser.add_argument("--freecad-python", type=Path, default=Path(r"C:\Program Files\FreeCAD 1.1\bin\python.exe"))
    args = parser.parse_args()
    args.artifact_root.mkdir(parents=True, exist_ok=True)
    stage = "load"
    try:
        protocol = read_json(args.protocol)
        assembly_raw = read_json(args.assembly)
        failure_raw = read_json(args.failure)
        cad_root = args.artifact_root / "cad"
        cad_manifest = cad_root / "manifest.json"
        process = []
        stage = "cadquery"
        process.append(run(stage, [
            str(args.cadquery_python), str(ROOT / "scripts/cad/generate_vehicle_assembly.py"),
            "--config", str(args.assembly), "--output-root", str(cad_root), "--manifest", str(cad_manifest),
        ]))
        generated = read_json(cad_manifest)
        stage = "freecad"
        freecad_report_path = args.artifact_root / "freecad_report.json"
        process.append(run(stage, [
            str(args.freecad_python), str(ROOT / "scripts/cad/inspect_vehicle_assembly_freecad.py"),
            str(cad_manifest), str(args.assembly), str(freecad_report_path),
        ]))
        freecad = read_json(freecad_report_path)
        stage = "identity"
        assembly = validate_protocol(
            protocol,
            assembly_raw,
            assembly_config_sha256=sha(args.assembly),
            assembly_step_sha256=generated["assembly"]["step_sha256"],
            failure_config_sha256=sha(args.failure),
        )
        mass_error = maximum_relative_mass_error(freecad["mass_properties"], protocol["assembly_identity"]["mass_properties"])
        if mass_error > float(protocol["tolerances"]["mass_property_relative"]):
            raise VehicleLoadCaseError("current FreeCAD mass properties differ from pinned evidence")
        stage = "load_cases"
        results = evaluate_all_load_cases(protocol, assembly, failure_raw)
        replay = evaluate_all_load_cases(protocol, assembly, failure_raw)
        ready_results = [asdict(item) for item in results]
        if ready_results != [asdict(item) for item in replay]:
            raise VehicleLoadCaseError("same-input load-case replay differs")
        nominal = [item for item in results if item.partition in {"training", "holdout"}]
        control = next(item for item in results if item.partition == "control")
        if {item.outcome for item in nominal} != {"running"} or control.outcome != "DNF":
            raise VehicleLoadCaseError("nominal/control outcome gate failed")
        import copy
        controls = []
        controls.append(rejected("geometry_identity", lambda: validate_protocol(
            protocol, assembly_raw, assembly_config_sha256="0" * 64,
            assembly_step_sha256=generated["assembly"]["step_sha256"], failure_config_sha256=sha(args.failure),
        ), "config_sha256"))
        controls.append(rejected("step_identity", lambda: validate_protocol(
            protocol, assembly_raw, assembly_config_sha256=sha(args.assembly),
            assembly_step_sha256="0" * 64, failure_config_sha256=sha(args.failure),
        ), "assembly_step_sha256"))
        missing = copy.deepcopy(protocol); del missing["cases"][0]["evidence"]["contact"]
        controls.append(rejected("missing_contact_evidence", lambda: validate_protocol(
            missing, assembly_raw, assembly_config_sha256=sha(args.assembly),
            assembly_step_sha256=generated["assembly"]["step_sha256"], failure_config_sha256=sha(args.failure),
        ), "evidence"))
        unbalanced = copy.deepcopy(protocol); unbalanced["cases"][0]["contact_wrench_at_com"][0] += 1.0
        controls.append(rejected("unbalanced_wrench", lambda: evaluate_all_load_cases(unbalanced, assembly, failure_raw), "equilibrium"))
        overlap = copy.deepcopy(protocol); overlap["partitions"]["holdout"].append("straight_acceleration")
        controls.append(rejected("partition_overlap", lambda: validate_protocol(
            overlap, assembly_raw, assembly_config_sha256=sha(args.assembly),
            assembly_step_sha256=generated["assembly"]["step_sha256"], failure_config_sha256=sha(args.failure),
        ), "overlaps"))
        bad_aero = copy.deepcopy(protocol); bad_aero["cases"][0]["aero_component_id"] = "unknown"
        controls.append(rejected("unknown_aero_target", lambda: evaluate_all_load_cases(bad_aero, assembly, failure_raw), "unknown"))
        controls.append(rejected("failure_identity", lambda: validate_protocol(
            protocol, assembly_raw, assembly_config_sha256=sha(args.assembly),
            assembly_step_sha256=generated["assembly"]["step_sha256"], failure_config_sha256="0" * 64,
        ), "failure config"))
        training_ids = tuple(protocol["partitions"]["training"])
        holdout_ids = tuple(protocol["partitions"]["holdout"])
        summary = {
            "status": "passed",
            "claim_level": protocol["claim_level"],
            "protocol_sha256": sha(args.protocol),
            "assembly_config_sha256": sha(args.assembly),
            "assembly_step_sha256": generated["assembly"]["step_sha256"],
            "failure_config_sha256": sha(args.failure),
            "mass_property_maximum_relative_error": mass_error,
            "partitions": {
                "training": list(training_ids), "training_sha256": canonical_sha256(training_ids),
                "holdout": list(holdout_ids), "holdout_sha256": canonical_sha256(holdout_ids),
            },
            "results": ready_results,
            "maximum_global_residual": max(max(abs(x) for x in item.global_residual) for item in results),
            "maximum_component_residual": max(item.maximum_component_residual for item in results),
            "maximum_interface_residual": max(item.maximum_interface_residual for item in results),
            "deliberate_overload_outcome": control.outcome,
            "replay": {"status": "exact", "result_set_sha256": canonical_sha256(ready_results)},
            "negative_controls": controls,
            "process_evidence": process,
            "repository_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(),
            "worktree_dirty_during_run": bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout),
            "review": {
                "supporting_evidence": [
                    "all frozen nominal snapshots balanced globally and per component",
                    "current deterministic STEP and independent FreeCAD mass properties matched pinned Work 047 identity",
                    "the deliberate overload crossed the declared connection capacity and Work 046 returned DNF",
                    "training and holdout memberships were disjoint and hashed before search",
                ],
                "contradicting_evidence": [
                    "no whole-vehicle stress FEA or independent refined structural evaluator is present",
                ],
                "alternative_explanations": [
                    "balanced rigid-body cut loads can coexist with unresolved local stress concentrations or contact effects",
                ],
                "missing_evidence": [
                    "transient dynamics, vibration, contact/preload/friction, arbitrary geometry meshing, and physical tests",
                ],
                "confidence": "high for algebraic load traceability; low for whole-vehicle stress or physical failure",
            },
        }
        write_json(args.artifact_root / "experiment_summary.json", summary)
        print(json.dumps({
            "status": "passed", "cases": len(results), "nominal": len(nominal),
            "overload": control.outcome, "max_global_residual": summary["maximum_global_residual"],
            "max_component_residual": summary["maximum_component_residual"],
            "mass_property_error": mass_error, "replay": "exact",
            "negative_controls": len(controls), "summary": str(args.artifact_root / "experiment_summary.json"),
        }, sort_keys=True))
        return 0
    except Exception as exc:
        write_json(args.artifact_root / "experiment_failure.json", {
            "status": "failed", "failed_stage": stage, "error_type": type(exc).__name__,
            "message": str(exc), "traceback": traceback.format_exc(),
        })
        print(json.dumps({"status": "failed", "stage": stage, "message": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
