"""Generate deterministic Work 030 integration release evidence."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics.circuit import load_circuit_catalog  # noqa: E402
from formula_ultimate.simulation import (  # noqa: E402
    create_integration_release_review,
    evaluate_promotion_gate,
    load_baseline_campaign_protocol,
    load_coupling_architecture,
    load_integration_gate_protocol,
    run_baseline_campaign,
    run_baseline_refinement_matrix,
    run_transaction_falsification_suite,
    verify_baseline_campaign_result,
)


def main() -> int:
    gate = load_integration_gate_protocol(
        ROOT / "config/simulation/integration_promotion_gate_v1.json"
    )
    baseline_protocol = load_baseline_campaign_protocol(
        ROOT / "config/simulation/fixed_topology_baseline_protocol_v1.json"
    )
    architecture = load_coupling_architecture(
        ROOT / "config/simulation/coupled_level0_architecture_v4.json"
    )
    profiles = load_circuit_catalog(ROOT / "config/circuits/real_circuits_v1.json")
    campaign = run_baseline_campaign(
        protocol=baseline_protocol,
        architecture=architecture,
        profiles=profiles,
    )
    identity_valid, identity_reasons = verify_baseline_campaign_result(campaign)
    falsification = run_transaction_falsification_suite(
        protocol=gate, architecture=architecture
    )
    refinement = run_baseline_refinement_matrix(
        gate_protocol=gate,
        baseline_protocol=baseline_protocol,
        architecture=architecture,
        profiles=profiles,
    )
    decision = evaluate_promotion_gate(
        candidate_id="fixed-four-steady-drag-v1",
        protocol=gate,
        campaign=campaign,
        falsification=falsification,
        refinement=refinement,
        cross_model_evidence=(),
    )
    review = create_integration_release_review(
        protocol=gate,
        campaign=campaign,
        falsification=falsification,
        refinement=refinement,
        promotion=decision,
    )
    if not (
        identity_valid
        and campaign.all_runs_finished
        and falsification.all_required_faults_detected
        and refinement.status == "passed"
        and decision.status == "blocked"
        and review.level0_infrastructure_ready
        and review.gated_level0_experimentation_authorized
        and not review.discovery_claim_allowed
        and not review.real_circuit_claim_allowed
    ):
        raise RuntimeError("Work 030 release gates did not produce the expected boundary")

    print(
        json.dumps(
            {
                "schema_version": "1.0",
                "gate": {
                    "gate_id": gate.gate_id,
                    "fingerprint_sha256": gate.fingerprint_sha256,
                },
                "campaign": {
                    "model_version": campaign.model_version,
                    "result_fingerprint_sha256": campaign.result_fingerprint_sha256,
                    "identity_valid": identity_valid,
                    "identity_reasons": list(identity_reasons),
                    "completed_runs": campaign.completed_run_count,
                    "completed_profiles": campaign.completed_profile_count,
                    "real_circuit_admitted": campaign.real_circuit_admitted,
                },
                "falsification": {
                    "control_status": falsification.control_status,
                    "detected_cases": falsification.detected_case_count,
                    "required_cases": falsification.required_case_count,
                    "all_rolled_back": all(case.rolled_back for case in falsification.cases),
                    "fingerprint_sha256": falsification.fingerprint_sha256,
                    "cases": [
                        {
                            "case_id": case.case_id,
                            "expected_code": case.expected_failure_code,
                            "observed_code": case.observed_failure_code,
                            "detected": case.detected,
                            "rolled_back": case.rolled_back,
                        }
                        for case in falsification.cases
                    ],
                },
                "refinement": {
                    "status": refinement.status,
                    "timesteps_s": list(gate.refinement.timesteps_s),
                    "sample_count": len(refinement.samples),
                    "max_relative_time_variation": refinement.max_relative_time_variation,
                    "max_relative_energy_variation": refinement.max_relative_energy_variation,
                    "max_absolute_finish_residual_m": refinement.max_absolute_finish_residual_m,
                    "convergence_order_estimated": refinement.convergence_order_estimated,
                    "fingerprint_sha256": refinement.fingerprint_sha256,
                    "claim_boundary": refinement.claim_boundary,
                },
                "promotion": {
                    "status": decision.status,
                    "blocking_reasons": list(decision.blocking_reasons),
                    "discovery_claim_allowed": decision.discovery_claim_allowed,
                    "automatic_promotion": decision.automatic_promotion,
                    "fingerprint_sha256": decision.fingerprint_sha256,
                },
                "release_review": {
                    "status": review.status,
                    "level0_infrastructure_ready": review.level0_infrastructure_ready,
                    "gated_level0_experimentation_authorized": review.gated_level0_experimentation_authorized,
                    "real_circuit_claim_allowed": review.real_circuit_claim_allowed,
                    "discovery_claim_allowed": review.discovery_claim_allowed,
                    "safety_claim_allowed": review.safety_claim_allowed,
                    "manufacturability_claim_allowed": review.manufacturability_claim_allowed,
                    "fingerprint_sha256": review.fingerprint_sha256,
                    "claim_boundary": review.claim_boundary,
                },
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
