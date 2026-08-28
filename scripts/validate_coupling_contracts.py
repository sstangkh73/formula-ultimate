"""Validate Work 021 coupling architecture, manifest, state, and evidence."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.simulation.coupling import (  # noqa: E402
    COUPLING_STAGES,
    ArtifactReference,
    ComponentHealthState,
    ContactRuntimeState,
    CoupledModuleSpec,
    CouplingContractError,
    EventCandidate,
    ExperimentManifest,
    ResidualEntry,
    ResidualLedger,
    SharedVehicleState,
    VersionPin,
    arbitrate_event_candidates,
    compile_coupling_architecture,
    load_coupling_architecture,
)


ARCHITECTURE = (
    ROOT / "config" / "simulation" / "coupled_level0_architecture_v1.json"
)


def expect_rejection(label, action):
    try:
        action()
    except CouplingContractError as exc:
        return {"label": label, "rejected": True, "reason": str(exc)}
    raise RuntimeError(f"invalid reference {label!r} was accepted")


def main() -> int:
    architecture = load_coupling_architecture(ARCHITECTURE)
    permuted = compile_coupling_architecture(
        architecture_id=architecture.architecture_id,
        modules=tuple(reversed(architecture.ordered_modules)),
        initial_signals=tuple(reversed(architecture.initial_signals)),
    )
    if architecture != permuted:
        raise RuntimeError("architecture permutation changed compiled evidence")

    manifest = ExperimentManifest(
        schema_version="1.0",
        experiment_id="work021-validator",
        candidate_id="fixed-topology-reference",
        design_language_version="typed-graph-v1",
        geometry_artifacts=(
            ArtifactReference("assembly-step", "a" * 64),
            ArtifactReference("geometry-evidence", "b" * 64),
        ),
        component_catalog_version="component-catalog-v1",
        circuit_profile_id="monaco_2026",
        regulatory_profile_version="fu-race-v1",
        energy_profile_version="technology-neutral-v1",
        solver_profile_version="coupled-level0-v1",
        model_versions=tuple(
            VersionPin(module.module_id, module.model_version)
            for module in architecture.ordered_modules
        ),
        architecture_fingerprint_sha256=architecture.fingerprint_sha256,
        source_commit="b0292b5",
        random_seed=17,
        evaluation_budget=1_000,
        time_step_s=0.01,
    )
    manifest_permuted = ExperimentManifest(
        schema_version=manifest.schema_version,
        experiment_id=manifest.experiment_id,
        candidate_id=manifest.candidate_id,
        design_language_version=manifest.design_language_version,
        geometry_artifacts=tuple(reversed(manifest.geometry_artifacts)),
        component_catalog_version=manifest.component_catalog_version,
        circuit_profile_id=manifest.circuit_profile_id,
        regulatory_profile_version=manifest.regulatory_profile_version,
        energy_profile_version=manifest.energy_profile_version,
        solver_profile_version=manifest.solver_profile_version,
        model_versions=tuple(reversed(manifest.model_versions)),
        architecture_fingerprint_sha256=manifest.architecture_fingerprint_sha256,
        source_commit=manifest.source_commit,
        random_seed=manifest.random_seed,
        evaluation_budget=manifest.evaluation_budget,
        time_step_s=manifest.time_step_s,
    )
    if manifest.fingerprint_sha256 != manifest_permuted.fingerprint_sha256:
        raise RuntimeError("manifest permutation changed deterministic identity")

    state = SharedVehicleState(
        time_s=0.0,
        race_distance_m=0.0,
        position_m=(0.0, 0.0, 0.0),
        velocity_mps=(0.0, 0.0, 0.0),
        yaw_rad=0.0,
        yaw_rate_rad_per_s=0.0,
        primary_energy_j=1.0e9,
        recovered_energy_j=0.0,
        completed_laps=0,
        contacts=tuple(
            ContactRuntimeState(contact_id, 1_000.0, 0.0, 0.0, 0.0, 0.0)
            for contact_id in ("front", "left", "right")
        ),
        components=(
            ComponentHealthState("energy-store", 300.0, 0.0, 0.0, False),
        ),
    )
    ledger = ResidualLedger(
        (
            ResidualEntry("force-x", "force", 0.01, "N", 0.001, 1.0e-6, 10_000.0),
            ResidualEntry("energy", "energy", -2.0, "J", 0.1, 0.0, 100.0),
        )
    )
    decision = arbitrate_event_candidates(
        (
            EventCandidate("finish", "finished", 10.0, "race"),
            EventCandidate("thermal", "thermal_failure", 10.0, "health"),
            EventCandidate("step", "step_complete", 12.0, "orchestrator"),
        )
    )

    missing_producer_modules = list(architecture.ordered_modules)
    target = missing_producer_modules[-1]
    missing_producer_modules[-1] = CoupledModuleSpec(
        target.module_id,
        target.stage,
        target.model_version,
        target.consumes + ("missing.signal",),
        target.produces,
    )
    reversed_modules = list(architecture.ordered_modules)
    first = reversed_modules[0]
    reversed_modules[0] = CoupledModuleSpec(
        first.module_id,
        first.stage,
        first.model_version,
        ("aero.force_moment",),
        first.produces,
    )
    rejections = (
        expect_rejection(
            "missing-producer",
            lambda: compile_coupling_architecture(
                architecture_id="invalid-missing",
                modules=tuple(missing_producer_modules),
                initial_signals=architecture.initial_signals,
            ),
        ),
        expect_rejection(
            "causal-reversal",
            lambda: compile_coupling_architecture(
                architecture_id="invalid-reversal",
                modules=tuple(reversed_modules),
                initial_signals=architecture.initial_signals,
            ),
        ),
        expect_rejection(
            "invalid-hash",
            lambda: ArtifactReference("broken", "not-a-sha256"),
        ),
        expect_rejection(
            "duplicate-contact",
            lambda: SharedVehicleState(
                0.0,
                0.0,
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                0.0,
                0.0,
                1.0,
                0.0,
                0,
                (
                    ContactRuntimeState("same", 1.0, 0.0, 0.0, 0.0, 0.0),
                    ContactRuntimeState("same", 1.0, 0.0, 0.0, 0.0, 0.0),
                ),
                (),
            ),
        ),
    )

    print(
        json.dumps(
            {
                "schema_version": "1.0",
                "architecture": {
                    "architecture_id": architecture.architecture_id,
                    "fingerprint_sha256": architecture.fingerprint_sha256,
                    "input_permutation_equal": architecture == permuted,
                    "stage_order": [
                        module.stage for module in architecture.ordered_modules
                    ],
                    "required_stage_order": list(COUPLING_STAGES),
                    "module_order": [
                        module.module_id for module in architecture.ordered_modules
                    ],
                    "signal_count": len(architecture.signal_producers),
                },
                "manifest": {
                    "fingerprint_sha256": manifest.fingerprint_sha256,
                    "permutation_equal": (
                        manifest.fingerprint_sha256
                        == manifest_permuted.fingerprint_sha256
                    ),
                    "seed": manifest.random_seed,
                    "evaluation_budget": manifest.evaluation_budget,
                    "time_step_s": manifest.time_step_s,
                },
                "topology_neutral_state": {
                    "contact_ids": [item.contact_id for item in state.contacts],
                    "contact_count": len(state.contacts),
                    "component_count": len(state.components),
                },
                "residual_ledger": {
                    "status": ledger.status,
                    "failed_residual_ids": ledger.failed_residual_ids,
                    "raw_energy_residual_j": ledger.entries[1].value,
                },
                "event_arbitration": {
                    "winner": decision.winner.event_id,
                    "winner_type": decision.winner.event_type,
                    "earliest_time_s": decision.earliest_time_s,
                    "tied_candidate_ids": decision.tied_candidate_ids,
                },
                "rejections": rejections,
                "physics_execution_count": 0,
                "claim_boundary": (
                    "Work 021 executable coupling contracts only; no coupled "
                    "vehicle physics or physical validation"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
