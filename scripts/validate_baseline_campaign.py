"""Generate deterministic Work 029 ten-circuit baseline evidence."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics.circuit import load_circuit_catalog  # noqa: E402
from formula_ultimate.simulation import (  # noqa: E402
    load_baseline_campaign_protocol,
    load_coupling_architecture,
    run_baseline_campaign,
)


def main() -> int:
    protocol = load_baseline_campaign_protocol(
        ROOT / "config/simulation/fixed_topology_baseline_protocol_v1.json"
    )
    architecture = load_coupling_architecture(
        ROOT / "config/simulation/coupled_level0_architecture_v4.json"
    )
    profiles = load_circuit_catalog(ROOT / "config/circuits/real_circuits_v1.json")
    result = run_baseline_campaign(
        protocol=protocol,
        architecture=architecture,
        profiles=profiles,
    )
    if not (
        result.all_runs_finished
        and result.all_residuals_passed
        and result.all_runs_within_budget
        and result.partition_complete
        and not result.real_circuit_admitted
    ):
        raise RuntimeError("Work 029 campaign completion gates failed")
    if result.completed_run_count != 30 or result.completed_profile_count != 10:
        raise RuntimeError("Work 029 expected 30 runs across ten profiles")

    circuit_rows = []
    for circuit_id in sorted({run.circuit_id for run in result.runs}):
        records = tuple(run for run in result.runs if run.circuit_id == circuit_id)
        metrics = {
            (
                run.outcome,
                run.final_time_s,
                run.final_distance_m,
                run.primary_energy_used_j,
                run.attempted_steps,
            )
            for run in records
        }
        if len(metrics) != 1 or len(records) != len(protocol.controls.random_seeds):
            raise RuntimeError(f"seed-controlled metrics differ for {circuit_id}")
        outcome, time_s, distance_m, energy_j, steps = next(iter(metrics))
        circuit_rows.append(
            {
                "circuit_id": circuit_id,
                "partition": records[0].partition,
                "seed_count": len(records),
                "outcome": outcome,
                "final_time_s": time_s,
                "final_distance_m": distance_m,
                "primary_energy_used_j": energy_j,
                "attempted_steps": steps,
                "static_width_status": records[0].static_width_status,
                "real_circuit_admitted": records[0].real_circuit_admitted,
            }
        )

    print(
        json.dumps(
            {
                "schema_version": "1.0",
                "campaign_id": result.campaign_id,
                "model_version": result.model_version,
                "protocol_fingerprint_sha256": result.protocol_fingerprint_sha256,
                "controls_fingerprint_sha256": result.controls_fingerprint_sha256,
                "architecture_fingerprint_sha256": result.architecture_fingerprint_sha256,
                "result_fingerprint_sha256": result.result_fingerprint_sha256,
                "reference_family_ids": [
                    family.family_id for family in protocol.reference_families
                ],
                "random_seeds": list(protocol.controls.random_seeds),
                "design_evaluation_budget": protocol.controls.design_evaluation_budget,
                "evaluation_budget_per_run": protocol.controls.evaluation_budget_per_run,
                "expected_run_count": result.expected_run_count,
                "completed_run_count": result.completed_run_count,
                "completed_profile_count": result.completed_profile_count,
                "all_residuals_passed": result.all_residuals_passed,
                "all_runs_within_budget": result.all_runs_within_budget,
                "partition_complete": result.partition_complete,
                "real_circuit_admitted": result.real_circuit_admitted,
                "circuits": circuit_rows,
                "claim_boundary": result.claim_boundary,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
