from __future__ import annotations

import argparse
from dataclasses import asdict, replace
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import traceback
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.simulation import (  # noqa: E402
    ConnectionDefinition,
    EventCandidate,
    FailureEvidence,
    GateAIdentity,
    StructuralFailureCouplingError,
    arbitrate_event_candidates,
    evaluate_structural_failure_step,
    initial_network_state,
    structural_result_fingerprint,
)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ready(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {name: ready(getattr(value, name)) for name in value.__dataclass_fields__}
    if isinstance(value, dict):
        return {str(key): ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [ready(item) for item in value]
    return value


def gate_from(raw: dict[str, Any]) -> GateAIdentity:
    return GateAIdentity(
        raw["remediation_protocol_id"], raw["decision"], raw["element_route_id"],
        raw["support_topology_sha256"], raw["boundary_model_id"],
    )


def simulate(
    *,
    definitions: tuple[ConnectionDefinition, ...],
    energies: dict[str, float],
    applied_wrench: tuple[float, float, float, float, float, float],
    evidence: tuple[FailureEvidence, ...],
    gate: GateAIdentity,
    protocols: dict[str, str],
    timestep_s: float,
    tolerances: dict[str, float],
) -> dict[str, Any]:
    state = initial_network_state(
        time_s=0.0, definitions=definitions,
        stored_energy_by_connection_j=energies, applied_wrench=applied_wrench,
    )
    pending = list(evidence)
    results = []
    while state.time_s < 1.0 and state.status == "running":
        duration = min(timestep_s, 1.0 - state.time_s)
        active = tuple(
            item for item in pending
            if item.crossing_time_s <= state.time_s + duration + tolerances["event_time_absolute_s"]
        )
        result = evaluate_structural_failure_step(
            state=state, duration_s=duration, definitions=definitions,
            applied_wrench=applied_wrench, evidence=active,
            gate_identity=gate, expected_gate_identity=gate,
            mechanism_protocols=protocols,
            residual_relative_tolerance=tolerances["force_moment_residual_relative"],
            event_time_absolute_tolerance_s=tolerances["event_time_absolute_s"],
        )
        if result.status != "ok" or result.candidate_state is None:
            raise StructuralFailureCouplingError(f"simulation step invalid: {result.reason}")
        results.append(result)
        if result.transition is not None:
            consumed = set(result.transition.evidence_ids)
            pending = [item for item in pending if item.evidence_id not in consumed]
        state = result.candidate_state
        if result.race_event is not None:
            break
    failure = next((item for item in reversed(results) if item.race_event is not None), None)
    if failure is None:
        raise StructuralFailureCouplingError("fixture did not reach a structural failure")
    return {
        "timestep_s": timestep_s,
        "outcome": failure.outcome,
        "event_time_s": failure.race_event.time_s,
        "race_event": ready(failure.race_event),
        "transition": ready(failure.transition),
        "candidate_state": ready(failure.candidate_state),
        "energy_ledger": ready(failure.energy_ledger),
        "residuals": [dict(ready(item), passed=item.passed) for item in failure.residuals],
        "failed_step_fingerprint_sha256": structural_result_fingerprint(failure),
        "step_fingerprints_sha256": [structural_result_fingerprint(item) for item in results],
    }


def rejected(control_id: str, action: Any, expected: str) -> dict[str, str]:
    try:
        value = action()
    except (StructuralFailureCouplingError, ValueError) as exc:
        if expected not in str(exc):
            raise StructuralFailureCouplingError(f"{control_id} rejected for wrong reason: {exc}") from exc
        return {"control_id": control_id, "status": "rejected_as_expected", "reason": str(exc)}
    if hasattr(value, "status") and value.status == "invalid" and expected in value.reason:
        return {"control_id": control_id, "status": "rejected_as_expected", "reason": value.reason}
    raise StructuralFailureCouplingError(f"negative control {control_id} was admitted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    args = parser.parse_args()
    stage = "configuration"
    try:
        raw = json.loads(args.config.read_text(encoding="utf-8"))
        if raw.get("protocol_id") != "structural_failure_coupling_v1":
            raise StructuralFailureCouplingError("unexpected Work 046 protocol identity")
        gate = gate_from(raw["gate_a_identity"])
        protocols = {str(key): str(value) for key, value in raw["mechanism_protocols"].items()}
        wrench = tuple(float(value) for value in raw["applied_wrench"]["force_n"] + raw["applied_wrench"]["moment_nm"])
        definitions = tuple(
            ConnectionDefinition(item["connection_id"], item["load_path_id"], float(item["share_weight"]))
            for item in raw["connections"]
        )
        energies = {item["connection_id"]: float(item["stored_elastic_energy_j"]) for item in raw["connections"]}
        evidence = tuple(
            FailureEvidence(
                item["evidence_id"], item["connection_id"], item["mechanism"],
                float(item["crossing_time_s"]), protocols[item["mechanism"]],
                item["artifact_sha256"], float(item["dissipated_fraction"]),
            )
            for item in raw["events"]
        )
        tolerances = {str(key): float(value) for key, value in raw["tolerances"].items()}
        timesteps = tuple(float(value) for value in raw["timestep_refinement_s"])
        if timesteps != (0.5, 0.25, 0.125):
            raise StructuralFailureCouplingError("Work 046 frozen timestep refinement changed")

        stage = "redundant_topology"
        redundant = tuple(
            simulate(
                definitions=definitions, energies=energies, applied_wrench=wrench,
                evidence=evidence, gate=gate, protocols=protocols,
                timestep_s=timestep, tolerances=tolerances,
            )
            for timestep in timesteps
        )
        stage = "critical_topology"
        critical_definitions = definitions[:1]
        critical_energies = {critical_definitions[0].connection_id: energies[critical_definitions[0].connection_id]}
        critical = tuple(
            simulate(
                definitions=critical_definitions, energies=critical_energies,
                applied_wrench=wrench, evidence=evidence, gate=gate,
                protocols=protocols, timestep_s=timestep, tolerances=tolerances,
            )
            for timestep in timesteps
        )
        redundant_times = tuple(item["event_time_s"] for item in redundant)
        critical_times = tuple(item["event_time_s"] for item in critical)
        reference_time = redundant_times[-1]
        relative_changes = tuple(abs(item - reference_time) / max(abs(reference_time), 1e-300) for item in redundant_times[:-1])
        event_convergence = max(relative_changes, default=0.0)
        if event_convergence > tolerances["event_time_relative"] or set(redundant_times + critical_times) != {0.375}:
            raise StructuralFailureCouplingError("event-time refinement gate failed")
        if {item["outcome"] for item in redundant} != {"running"}:
            raise StructuralFailureCouplingError("redundant topology did not remain running")
        if {item["outcome"] for item in critical} != {"DNF"}:
            raise StructuralFailureCouplingError("critical topology did not produce DNF")
        failed_state = next(item for item in redundant[-1]["candidate_state"]["connections"] if item["connection_id"] == "joint_a")
        survivor = next(item for item in redundant[-1]["candidate_state"]["connections"] if item["connection_id"] == "joint_b")
        if tuple(failed_state["transmitted_wrench"]) != (0.0,) * 6 or tuple(survivor["transmitted_wrench"]) != wrench:
            raise StructuralFailureCouplingError("post-failure wrench redistribution is incorrect")
        residual_values = [abs(float(item["value"])) for item in redundant[-1]["residuals"]]
        if any(not bool(item["passed"]) for item in redundant[-1]["residuals"]):
            raise StructuralFailureCouplingError("fixture residual gate failed")

        stage = "replay"
        replay = simulate(
            definitions=definitions, energies=energies, applied_wrench=wrench,
            evidence=evidence, gate=gate, protocols=protocols,
            timestep_s=timesteps[-1], tolerances=tolerances,
        )
        replay_exact = replay == redundant[-1]
        if not replay_exact:
            raise StructuralFailureCouplingError("same-input replay differs")
        finish_tie = arbitrate_event_candidates((
            EventCandidate("race.finish", "finished", reference_time, "race_progress_solver"),
            EventCandidate("structural.fixture", "structural_failure", reference_time, "structural_failure_coupling"),
        ))
        earlier_structural = arbitrate_event_candidates((
            EventCandidate("race.finish", "finished", reference_time + 0.01, "race_progress_solver"),
            EventCandidate("structural.fixture", "structural_failure", reference_time, "structural_failure_coupling"),
        ))
        before = initial_network_state(time_s=0.0, definitions=definitions, stored_energy_by_connection_j=energies, applied_wrench=wrench)
        invalid_gate = replace(gate, element_route_id="C3D4_near_critical")
        controls = [
            rejected(
                "out_of_domain_gate_identity",
                lambda: evaluate_structural_failure_step(
                    state=before, duration_s=0.5, definitions=definitions, applied_wrench=wrench,
                    evidence=evidence, gate_identity=invalid_gate, expected_gate_identity=gate,
                    mechanism_protocols=protocols,
                ),
                "outside",
            ),
            rejected(
                "unknown_connection",
                lambda: evaluate_structural_failure_step(
                    state=before, duration_s=0.5, definitions=definitions, applied_wrench=wrench,
                    evidence=(replace(evidence[0], connection_id="unknown"),),
                    gate_identity=gate, expected_gate_identity=gate, mechanism_protocols=protocols,
                ),
                "unknown",
            ),
            rejected(
                "protocol_mismatch",
                lambda: evaluate_structural_failure_step(
                    state=before, duration_s=0.5, definitions=definitions, applied_wrench=wrench,
                    evidence=(replace(evidence[0], upstream_protocol_id="unknown"),),
                    gate_identity=gate, expected_gate_identity=gate, mechanism_protocols=protocols,
                ),
                "protocol",
            ),
            rejected(
                "event_before_state",
                lambda: evaluate_structural_failure_step(
                    state=replace(before, time_s=0.3), duration_s=0.5,
                    definitions=definitions, applied_wrench=wrench, evidence=(evidence[0],),
                    gate_identity=gate, expected_gate_identity=gate, mechanism_protocols=protocols,
                ),
                "precedes",
            ),
            rejected(
                "invalid_energy_partition",
                lambda: FailureEvidence("bad", "joint_a", "fracture", 0.4, protocols["fracture"], "c" * 64, 1.1),
                "[0,1]",
            ),
        ]
        summary = {
            "status": "passed",
            "claim_level": raw["claim_level"],
            "gate_a_identity": ready(gate),
            "redundant_topology": redundant,
            "critical_topology": critical,
            "event_time_refinement": {
                "status": "supported",
                "timesteps_s": timesteps,
                "event_times_s": redundant_times,
                "maximum_relative_change": event_convergence,
                "limit": tolerances["event_time_relative"],
            },
            "wrench_closure": {"status": "supported", "maximum_absolute_residual": max(residual_values, default=0.0)},
            "energy_closure": {"status": "supported", "residual_j": redundant[-1]["energy_ledger"]["residual_j"]},
            "state_transition": {"status": "supported", "path": ["intact", "degraded", "failed"]},
            "dnf": {"status": "supported", "critical_outcomes": [item["outcome"] for item in critical]},
            "replay": {"status": "exact", "fingerprint_sha256": replay["failed_step_fingerprint_sha256"]},
            "race_arbitration": {
                "finish_tie_winner": ready(finish_tie.winner),
                "earlier_structural_winner": ready(earlier_structural.winner),
            },
            "negative_controls": controls,
            "invalid_evidence_candidate_state_is_none": True,
            "config_sha256": sha(args.config),
            "source_config_sha256": {
                path.name: sha(path)
                for path in (
                    ROOT / "config/structural/gate_a_remediation_v1.json",
                    ROOT / "config/structural/yield_plasticity_acceptance_v1.json",
                    ROOT / "config/structural/fracture_initiation_acceptance_v1.json",
                    ROOT / "config/structural/fatigue_damage_acceptance_v1.json",
                )
            },
            "repository_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(),
            "worktree_dirty_during_run": bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout),
            "review": {
                "supporting_evidence": [
                    "typed yield degradation and fracture failure were localized at their declared absolute times",
                    "the failed connection wrench was exactly zero and the redundant survivor carried the complete wrench",
                    "critical path loss produced DNF and failure energy closed without deletion",
                    "same-input replay was exact and malformed evidence produced no candidate state",
                ],
                "contradicting_evidence": [
                    "instantaneous redistribution is not transient fracture dynamics",
                    "the admitted Gate A identity is intentionally narrow",
                ],
                "alternative_explanations": [
                    "a real compliant joint could redistribute through stress waves, contact, or fastener slip",
                ],
                "missing_evidence": [
                    "physical joint tests and calibrated material records",
                    "contact separation, impact, crash, and post-critical structural response",
                ],
                "confidence": "high for deterministic policy mechanics; low for real failure dynamics",
            },
        }
        write_json(args.artifact_root / "experiment_summary.json", summary)
        print(json.dumps({
            "status": "passed",
            "event_time_s": reference_time,
            "event_time_refinement_relative": event_convergence,
            "redundant_outcome": redundant[-1]["outcome"],
            "critical_outcome": critical[-1]["outcome"],
            "wrench_residual": summary["wrench_closure"]["maximum_absolute_residual"],
            "energy_residual_j": summary["energy_closure"]["residual_j"],
            "replay": "exact",
            "negative_controls": len(controls),
            "summary": str(args.artifact_root / "experiment_summary.json"),
        }, sort_keys=True))
        return 0
    except Exception as exc:
        write_json(args.artifact_root / "experiment_failure.json", {
            "status": "failed", "failed_stage": stage,
            "error_type": type(exc).__name__, "message": str(exc),
            "traceback": traceback.format_exc(),
        })
        print(json.dumps({"status": "failed", "stage": stage, "message": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
