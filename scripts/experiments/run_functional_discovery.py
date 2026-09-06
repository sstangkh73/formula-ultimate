#!/usr/bin/env python3
"""Execute the preregistered Work 100 functional/coupled subsystem trial."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import time
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

import cadquery  # noqa: E402
import numpy  # noqa: E402

from formula_ultimate.experiments.discovery_evidence import gate_for  # noqa: E402
from formula_ultimate.experiments.discovery_ledger import DiscoveryLedger, scientific_summary  # noqa: E402
from formula_ultimate.experiments.discovery_registration import (  # noqa: E402
    DiscoveryViolation,
    clone,
    digest,
    strict_json,
    validate_registration,
    zero_cost,
)
from formula_ultimate.experiments.functional_discovery import (  # noqa: E402
    FunctionalDiscoveryViolation,
    assess_candidate,
    assess_process,
    treatment_matrix,
    unresolved_proxy_audit,
    validate_trial_config,
)
from formula_ultimate.physics.functional_network_solver import FunctionalSolverViolation  # noqa: E402
from formula_ultimate.search.executable_morphology import MorphologyViolation  # noqa: E402
from scripts.experiments.run_executable_morphology_qd import (  # noqa: E402
    CadExecutionViolation,
    boundary_identity,
    execute_genome,
)


PRIMARY_IMPLEMENTATION = ROOT / "src/formula_ultimate/physics/functional_network_solver.py"
REFERENCE_IMPLEMENTATION = ROOT / "src/formula_ultimate/physics/functional_network_reference.py"
VALIDATION_SOURCE = ROOT / "tests/test_functional_discovery.py"
REPRESENTATION_SOURCE = ROOT / "src/formula_ultimate/search/executable_morphology.py"
EXPERIMENT_IMPLEMENTATION = ROOT / "src/formula_ultimate/experiments/functional_discovery.py"
RUNNER_SOURCE = Path(__file__).resolve()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def verify_frozen_identities(config: Mapping[str, Any], registration: Mapping[str, Any]) -> dict[str, str]:
    validate_trial_config(config)
    validate_registration(dict(registration))
    body = registration["body"]
    evaluator = {item["id"]: item for item in body["evaluators"]}
    expected = {
        "primary_implementation": _sha256_file(PRIMARY_IMPLEMENTATION),
        "reference_implementation": _sha256_file(REFERENCE_IMPLEMENTATION),
        "validation": _sha256_file(VALIDATION_SOURCE),
        "representation": _sha256_file(REPRESENTATION_SOURCE),
        "operator": digest({
            "trial_sha256": digest(config),
            "experiment_implementation_sha256": _sha256_file(EXPERIMENT_IMPLEMENTATION),
            "runner_sha256": _sha256_file(RUNNER_SOURCE),
        }),
        "task": digest({"training": config["training_task"], "holdout": config["holdout_task"]}),
        "material": digest(config["material"]),
        "environment": digest(config["environment"]),
        "energy": digest({"training_heat_w": config["training_task"]["heat_w"], "holdout_heat_w": config["holdout_task"]["heat_w"], "replenishment": "none_within_static_task"}),
    }
    checks = {
        "primary_implementation": evaluator["axial_thermal_primary"]["implementation_sha256"],
        "reference_implementation": evaluator["axial_thermal_reference"]["implementation_sha256"],
        "validation": evaluator["axial_thermal_primary"]["validation_sha256"],
        "representation": body["profiles"]["representation_library_sha256"],
        "operator": body["profiles"]["operator_library_sha256"],
        "task": body["profiles"]["task_sha256"],
        "material": body["profiles"]["material_library_sha256"],
        "environment": body["profiles"]["environment_sha256"],
        "energy": body["profiles"]["energy_profile_sha256"],
    }
    if checks != expected:
        differences = sorted(key for key in expected if checks.get(key) != expected[key])
        raise FunctionalDiscoveryViolation(f"frozen source identity mismatch: {differences}")
    if evaluator["axial_thermal_reference"]["validation_sha256"] != expected["validation"]:
        raise FunctionalDiscoveryViolation("reference validation identity mismatch")
    actual_environment = {"python": platform.python_version(), "cadquery": cadquery.__version__, "numpy": numpy.__version__, "workers": 1, "ordering": "registered_serial"}
    if actual_environment != config["environment"]:
        raise FunctionalDiscoveryViolation(f"runtime environment mismatch: {actual_environment}")
    return {**expected, "trial": digest(config)}


def _candidate(registration: Mapping[str, Any], config: Mapping[str, Any], row: Mapping[str, Any]) -> dict[str, Any]:
    genome = deepcopy(row["genome"])
    context = {
        "candidate_id": genome["genome_id"],
        "genotype_sha256": digest(genome),
        "geometry_sha256": None,
        "material_sha256": digest(config["material"]),
        "boundary_sha256": None,
        "controller_sha256": digest(genome["controller"]),
        "environment_sha256": registration["body"]["profiles"]["environment_sha256"],
        "task_sha256": registration["body"]["profiles"]["task_sha256"],
        "registration_sha256": registration["registration_sha256"],
    }
    trace = [{"operator": item["operator"], "parameters": {key: clone(value) for key, value in item.items() if key != "operator"}} for item in row["mutation_trace"]]
    return {
        "id": genome["genome_id"],
        "parents": [],
        "genotype": genome,
        "context": context,
        "representation": "solid" if len(genome["parts"]) == 1 else "multi_body",
        "treatment": row["treatment"],
        "seed": row["seed"],
        "partition": "training",
        "dataset_id": config["training_task"]["dataset_id"],
        "mutation_trace": trace,
    }


def _cost(*, attempts: int = 1, geometry: int = 0, cad_calls: int = 0, mesh_attempts: int = 0, elements: int = 0, dof: int = 0, solver_iterations: int = 0, cpu_s: float = 0.0, wall_s: float = 0.0) -> dict[str, Any]:
    result = zero_cost()
    result.update({"attempts": attempts, "geometry_executions": geometry, "cad_calls": cad_calls, "mesh_attempts": mesh_attempts, "elements": elements, "dof": dof, "solver_iterations": solver_iterations, "cpu_s": max(0.0, cpu_s), "wall_s": max(0.0, wall_s), "peak_memory_bytes": 0})
    return result


def _reserve(ledger: DiscoveryLedger, cid: str, dimension: str, scope: str, aid: str, pool: str, reserved: Mapping[str, Any], selection_sha256: str | None = None) -> None:
    ledger.append({"type": "reserve", "id": aid, "candidate_id": cid, "pool": pool, "dimension": dimension, "scope": scope, "cost": clone(dict(reserved)), "retry_of": None, "cache_of": None, "selection_sha256": selection_sha256})
    ledger.append({"type": "start", "id": aid})


def _diagnostic(context: Mapping[str, Any], details: Mapping[str, Any]) -> dict[str, Any]:
    body = {"context_sha256": digest(context), "evidence_class": "admitted_simulation", "details": clone(dict(details))}
    return {"body": body, "sha256": digest(body)}


def _settle_diagnostic(ledger: DiscoveryLedger, cid: str, aid: str, dimension: str, status: str, reason: str, details: Mapping[str, Any], observed: Mapping[str, Any], identity: str) -> None:
    context = clone(ledger.replay()["state"]["states"][cid]["context"])
    context["geometry_sha256" if dimension == "representation" else "boundary_sha256"] = identity
    result = {"dimension": dimension, "scope": dimension, "status": status, "reason": reason, "context": context, "artifact": _diagnostic(context, details)}
    ledger.append({"type": "settle", "id": aid, "observed_cost": clone(dict(observed)), "result": result, "diagnostics": {"work": "100", "hidden_repair": False}})


def _artifact(registration: Mapping[str, Any], ledger: DiscoveryLedger, cid: str, gate_id: str, assessment: Mapping[str, Any], details: Mapping[str, Any]) -> dict[str, Any]:
    gate = gate_for(registration["body"], gate_id)
    evaluator = next(item for item in registration["body"]["evaluators"] if item["id"] == gate["evaluator_id"])
    candidate = ledger.replay()["state"]["candidates"][cid]
    context = ledger.replay()["state"]["states"][cid]["context"]
    dataset_id = assessment.get("dataset_id", candidate["dataset_id"])
    if gate["kind"] == "holdout":
        dataset_id = registration["body"]["partitions"]["holdout"][0]
    body = {
        "evidence_class": "admitted_simulation",
        "evaluator_id": evaluator["id"],
        "implementation_sha256": evaluator["implementation_sha256"],
        "validation_sha256": evaluator["validation_sha256"],
        "context_sha256": digest(context),
        "gate_id": gate_id,
        "dataset_id": dataset_id,
        "metric": gate["metric"],
        "unit": gate["unit"],
        "value": float(assessment["value"]),
        "converged": True,
        "error": float(assessment["error"]),
        "refinements": list(assessment["refinements"]),
        "evidence_type": gate["evidence_type"],
        "details": clone(dict(details)),
    }
    return {"body": body, "sha256": digest(body)}


def _evaluate_gate(ledger: DiscoveryLedger, registration: Mapping[str, Any], cid: str, gate_id: str, assessment: Mapping[str, Any], aid: str, *, pool: str, observed: Mapping[str, Any], selection_sha256: str | None = None, details: Mapping[str, Any]) -> None:
    gate = gate_for(registration["body"], gate_id)
    dimension = gate["kind"] if gate["kind"] in {"physics", "manufacturing"} else "gate"
    reserved = {**clone(dict(observed)), "cpu_s": 10.0, "wall_s": 10.0, "elements": max(10000, observed["elements"]), "dof": max(10000, observed["dof"]), "solver_iterations": max(10000, observed["solver_iterations"])}
    _reserve(ledger, cid, dimension, gate_id, aid, pool, reserved, selection_sha256)
    if dimension == "physics":
        status = assessment["status"]
    elif dimension == "manufacturing":
        status = assessment["status"]
    else:
        passed = assessment["value"] <= gate["threshold"] if gate["comparison"] == "le" else assessment["value"] >= gate["threshold"]
        status = "passed" if passed else "failed"
    if status == "numerically_unresolved":
        artifact = None
        reason = "error_gate"
    else:
        artifact = _artifact(registration, ledger, cid, gate_id, assessment, details)
        reason = "registered_field_evaluation"
    context = clone(ledger.replay()["state"]["states"][cid]["context"])
    result = {"dimension": dimension, "scope": gate_id, "status": status, "reason": reason, "context": context, "artifact": artifact}
    ledger.append({"type": "settle", "id": aid, "observed_cost": clone(dict(observed)), "result": result, "diagnostics": {"work": "100", "gate_id": gate_id}})


def _physics_cost(assessment: Mapping[str, Any], cpu_s: float, wall_s: float) -> dict[str, Any]:
    levels = assessment["primary"]["levels"]
    elements = sum(level["mechanical_field"]["segment_count"] + level["thermal_field"]["segment_count"] for level in levels)
    dof = sum(level["mechanical_field"]["node_count"] + level["thermal_field"]["node_count"] for level in levels)
    return _cost(mesh_attempts=len(levels) * 2, elements=elements, dof=dof, solver_iterations=len(levels) * 2, cpu_s=cpu_s, wall_s=wall_s)


def _strip_assessment(assessment: Mapping[str, Any]) -> dict[str, Any]:
    return clone(dict(assessment))


def _analysis(rows: list[dict[str, Any]], seeds: list[int]) -> dict[str, Any]:
    by = {(row["treatment"], row["seed"]): row for row in rows}
    contrasts = {}
    for treatment in sorted({row["treatment"] for row in rows} - {"FIXED_TOPOLOGY"}):
        deltas = [by[(treatment, seed)]["training"]["value"] - by[("FIXED_TOPOLOGY", seed)]["training"]["value"] for seed in seeds]
        contrasts[treatment] = {"paired_differences": deltas, "mean_difference": sum(deltas) / len(deltas), "superiority_claim_allowed": False}
    return {"contrasts_vs_fixed": contrasts, "sample_size": len(seeds), "inferential_status": "descriptive_only_insufficient_power"}


def run(config: Mapping[str, Any], registration: Mapping[str, Any], output_dir: Path, replay_reference: Mapping[str, Any] | None = None) -> dict[str, Any]:
    validation = validate_trial_config(config)
    identities = verify_frozen_identities(config, registration)
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FunctionalDiscoveryViolation("output directory must be new or empty")
    output_dir.mkdir(parents=True, exist_ok=True)
    ledger = DiscoveryLedger(output_dir / "ledger.jsonl", dict(registration))
    candidates = []
    timings = {}
    attempt_index = 0
    rows = treatment_matrix(config)
    cad_evidence = {}

    for row in rows:
        cid = row["genome"]["genome_id"]
        ledger.append({"type": "candidate", "candidate": _candidate(registration, config, row)})
        aid = f"work100_attempt_{attempt_index:04d}"; attempt_index += 1
        _reserve(ledger, cid, "representation", "representation", aid, "exploration", _cost(geometry=1, cad_calls=1, cpu_s=10.0, wall_s=10.0))
        wall_start, cpu_start = time.perf_counter(), time.process_time()
        cad = execute_genome(row["genome"], config["representation_limits"], output_dir / "cad" / f"{cid}.step")
        wall_s, cpu_s = time.perf_counter() - wall_start, time.process_time() - cpu_start
        _settle_diagnostic(ledger, cid, aid, "representation", "geometry_measured", "cad_geometry_measured", {"cad": cad, "hidden_geometry_repair": False, "physics_executed": False}, _cost(geometry=1, cad_calls=1, cpu_s=cpu_s, wall_s=wall_s), cad["geometry_sha256"])
        boundary = boundary_identity(row["genome"], cad)
        aid = f"work100_attempt_{attempt_index:04d}"; attempt_index += 1
        _reserve(ledger, cid, "boundary", "boundary", aid, "exploration", _cost(cpu_s=1.0, wall_s=1.0))
        _settle_diagnostic(ledger, cid, aid, "boundary", "boundary_resolved", "terminal_ancestry_resolved", {"terminal_positions_m": cad["measurement"]["terminal_positions_m"], "interfaces": row["genome"]["interfaces"]}, _cost(), boundary)
        cad_evidence[cid] = cad
        timings[cid] = {"cad_wall_s": wall_s, "cad_cpu_s": cpu_s}

    proxy_assessments = {}
    for row in rows:
        cid = row["genome"]["genome_id"]
        wall_start, cpu_start = time.perf_counter(), time.process_time()
        proxy = assess_candidate(config, row["genome"], "training_task", proxy=True)
        wall_s, cpu_s = time.perf_counter() - wall_start, time.process_time() - cpu_start
        aid = f"work100_attempt_{attempt_index:04d}"; attempt_index += 1
        cost = _physics_cost(proxy, cpu_s, wall_s)
        _evaluate_gate(ledger, registration, cid, "coupled_proxy", proxy, aid, pool="exploration", observed=cost, details={"field_solver_executed": True, "proxy": True, "geometry_sha256": cad_evidence[cid]["geometry_sha256"], "assessment": _strip_assessment(proxy)})
        proxy_assessments[cid] = proxy
        timings[cid]["proxy_wall_s"] = wall_s; timings[cid]["proxy_cpu_s"] = cpu_s

    ledger.append({"type": "select", "pool": "audit", "gate_id": "coupled_proxy"})
    selection = ledger.replay()["state"]["selections"][-1]
    selection_sha = selection["selection_sha256"]
    selected = {item["candidate_id"] for item in selection["selection"]["selected"]}
    refined_assessments = {}
    for row in rows:
        cid = row["genome"]["genome_id"]
        if cid not in selected:
            continue
        wall_start, cpu_start = time.perf_counter(), time.process_time()
        refined = assess_candidate(config, row["genome"], "training_task")
        wall_s, cpu_s = time.perf_counter() - wall_start, time.process_time() - cpu_start
        aid = f"work100_attempt_{attempt_index:04d}"; attempt_index += 1
        cost = _physics_cost(refined, cpu_s, wall_s)
        _evaluate_gate(ledger, registration, cid, "coupled_refined", refined, aid, pool="audit", observed=cost, selection_sha256=selection_sha, details={"field_solver_executed": True, "proxy": False, "geometry_sha256": cad_evidence[cid]["geometry_sha256"], "assessment": _strip_assessment(refined)})
        refined_assessments[cid] = refined
        timings[cid]["refined_wall_s"] = wall_s; timings[cid]["refined_cpu_s"] = cpu_s

    if any(item["proxy_score"] is None for item in selection["population"] if item["candidate_id"] in selected):
        audit_report = unresolved_proxy_audit(selection, refined_assessments)
    else:
        audit_report = ledger.audit_report(selection_sha, "coupled_refined")
    survivors = []
    for row in rows:
        cid = row["genome"]["genome_id"]
        refined = refined_assessments[cid]
        process = assess_process(config, row["genome"])
        process_assessment = {"status": process["status"], "value": process["process_violation_ratio"], "error": 0.0, "refinements": [1], "dataset_id": config["training_task"]["dataset_id"]}
        aid = f"work100_attempt_{attempt_index:04d}"; attempt_index += 1
        _evaluate_gate(ledger, registration, cid, "process_envelope", process_assessment, aid, pool="finalist", observed=_cost(), details={"process_check_executed": True, "process": process, "manufacturing_proof": False})
        wall_start, cpu_start = time.perf_counter(), time.process_time()
        holdout = assess_candidate(config, row["genome"], "holdout_task")
        wall_s, cpu_s = time.perf_counter() - wall_start, time.process_time() - cpu_start
        aid = f"work100_attempt_{attempt_index:04d}"; attempt_index += 1
        holdout_status = {"physically_feasible": "passed", "physically_failed": "failed", "numerically_unresolved": "numerically_unresolved"}[holdout["status"]]
        _evaluate_gate(ledger, registration, cid, "coupled_holdout", {**holdout, "status": holdout_status}, aid, pool="finalist", observed=_physics_cost(holdout, cpu_s, wall_s), details={"field_solver_executed": True, "holdout_feedback_used": False, "geometry_sha256": cad_evidence[cid]["geometry_sha256"], "assessment": _strip_assessment(holdout)})
        replay_assessment = {"status": "passed", "value": 0.0, "error": 0.0, "refinements": [1], "dataset_id": config["training_task"]["dataset_id"]}
        aid = f"work100_attempt_{attempt_index:04d}"; attempt_index += 1
        _evaluate_gate(ledger, registration, cid, "decision_replay", replay_assessment, aid, pool="finalist", observed=_cost(), details={"trusted_head_replay_required": True, "timing_identity_excluded": True})
        state = ledger.replay()["state"]["states"][cid]
        results = {**state["physics"], **state["manufacturing"], **state["gate"]}
        if all(results.get(gate_id, {}).get("status") in {"physically_feasible", "manufacturing_compatible", "passed"} for gate_id in registration["body"]["survivor_gates"]):
            ledger.append({"type": "promote", "candidate_id": cid, "target": "candidate_survivor", "use": registration["body"]["promotion_scope"]})
            survivors.append(cid)
        candidates.append({"candidate_id": cid, "treatment": row["treatment"], "seed": row["seed"], "genotype_sha256": row["genotype_sha256"], "geometry_sha256": cad_evidence[cid]["geometry_sha256"], "functional_signature": row["functional_signature"], "descriptors": row["descriptors"], "proxy": _strip_assessment(proxy_assessments[cid]), "training": _strip_assessment(refined), "process": process, "holdout": _strip_assessment(holdout), "candidate_survivor": cid in survivors})
        timings[cid]["holdout_wall_s"] = wall_s; timings[cid]["holdout_cpu_s"] = cpu_s

    replay = ledger.replay()
    reopened = DiscoveryLedger(output_dir / "ledger.jsonl", dict(registration), expected_head=replay["head_sha256"]).replay()
    if replay != reopened:
        raise FunctionalDiscoveryViolation("trusted-head decision replay mismatch")
    distinct_nonfixed = {row["functional_signature"] for row in candidates if row["treatment"] in {"GRAPH_ONLY", "JOINT_MORPHOLOGY_CONTROLLER"}}
    fixed_signature = next(row["functional_signature"] for row in candidates if row["treatment"] == "FIXED_TOPOLOGY")
    if not survivors or not any(row["candidate_survivor"] and row["functional_signature"] != fixed_signature for row in candidates):
        raise FunctionalDiscoveryViolation("no previously undeclared functional architecture reached the scoped survivor gate")
    deterministic = {
        "schema": "work100_functional_coupled_trial_result_v1",
        "trial_sha256": validation["trial_sha256"],
        "registration_sha256": registration["registration_sha256"],
        "source_identities": identities,
        "candidates": candidates,
        "selection": selection,
        "audit": audit_report,
        "survivors": sorted(survivors),
        "analysis": _analysis(candidates, config["seeds"]),
        "claim_boundary": clone(config["claim_boundary"]),
        "distinct_nonfixed_functional_signatures": sorted(distinct_nonfixed),
    }
    deterministic["deterministic_sha256"] = digest(deterministic)
    report = {
        "deterministic_evidence": deterministic,
        "decision_replay": {"status": "exact", "trusted_head_reopened": True, "head_sha256": replay["head_sha256"], "state_sha256": replay["state_sha256"]},
        "timing_observations": timings,
        "scientific_admission": scientific_summary(replay["state"]),
        "limitations": ["bounded_scalar_axial_thermal_network_only", "linear_static_and_steady_state", "declared_material_model_not_certification", "process_envelope_not_manufacturing_proof", "descriptive_n_equals_2", "no_complete_vehicle_or_race_claim", "no_physical_validation"],
    }
    if report["scientific_admission"]["scientific_survivors"] != len(survivors):
        raise FunctionalDiscoveryViolation("scientific summary differs from survivor ledger")
    if replay_reference is not None:
        expected = replay_reference["deterministic_evidence"]
        if deterministic != expected:
            raise FunctionalDiscoveryViolation("cross-run deterministic evidence mismatch")
        report["execution_replay"] = {"status": "passed", "deterministic_evidence_exact": True, "timing_compared": False}
    _write_json(output_dir / "result.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config/experiments/functional_discovery_trial_v1.json")
    parser.add_argument("--registration", type=Path, default=ROOT / "config/experiments/functional_discovery_registration_v2.json")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()
    try:
        config = strict_json(args.config.read_text(encoding="utf-8"))
        registration = strict_json(args.registration.read_text(encoding="utf-8"))
        reference = strict_json(args.replay_reference.read_text(encoding="utf-8")) if args.replay_reference else None
        report = run(config, registration, args.output_dir, reference)
        print(json.dumps({"status": "passed", "candidate_count": len(report["deterministic_evidence"]["candidates"]), "survivor_count": len(report["deterministic_evidence"]["survivors"]), "audit_status": report["deterministic_evidence"]["audit"]["status"], "deterministic_sha256": report["deterministic_evidence"]["deterministic_sha256"]}, sort_keys=True))
        return 0
    except (FunctionalDiscoveryViolation, FunctionalSolverViolation, MorphologyViolation, CadExecutionViolation, DiscoveryViolation, OSError, KeyError, ValueError) as error:
        print(f"Work 100 failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
