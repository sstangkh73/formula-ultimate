from __future__ import annotations

import math
from pathlib import Path
import tempfile
import unittest

from formula_ultimate.simulation.coupling import (
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


ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE = (
    ROOT / "config" / "simulation" / "coupled_level0_architecture_v1.json"
)


def manifest(**overrides) -> ExperimentManifest:
    values = {
        "schema_version": "1.0",
        "experiment_id": "coupling-reference",
        "candidate_id": "fixed-topology-reference",
        "design_language_version": "typed-graph-v1",
        "geometry_artifacts": (
            ArtifactReference("assembly-step", "a" * 64),
            ArtifactReference("geometry-evidence", "b" * 64),
        ),
        "component_catalog_version": "component-catalog-v1",
        "circuit_profile_id": "monaco_2026",
        "regulatory_profile_version": "fu-energy-v1",
        "energy_profile_version": "technology-neutral-v1",
        "solver_profile_version": "coupled-level0-v1",
        "model_versions": (
            VersionPin("aerodynamics", "work017-aerodynamic-map-v1"),
            VersionPin("thermal", "work014-thermal-v1"),
        ),
        "architecture_fingerprint_sha256": load_coupling_architecture(
            ARCHITECTURE
        ).fingerprint_sha256,
        "source_commit": "b0292b5",
        "random_seed": 17,
        "evaluation_budget": 1_000,
        "time_step_s": 0.01,
    }
    values.update(overrides)
    return ExperimentManifest(**values)


def contact(contact_id: str, load_n: float = 1_000.0) -> ContactRuntimeState:
    return ContactRuntimeState(contact_id, load_n, 0.0, 0.0, 0.0, 0.0)


def shared_state(**overrides) -> SharedVehicleState:
    values = {
        "time_s": 0.0,
        "race_distance_m": 0.0,
        "position_m": (0.0, 0.0, 0.0),
        "velocity_mps": (0.0, 0.0, 0.0),
        "yaw_rad": 0.0,
        "yaw_rate_rad_per_s": 0.0,
        "primary_energy_j": 1.0e9,
        "recovered_energy_j": 0.0,
        "completed_laps": 0,
        "contacts": (contact("front"), contact("left"), contact("right")),
        "components": (
            ComponentHealthState("energy-store", 300.0, 0.0, 0.0, False),
        ),
    }
    values.update(overrides)
    return SharedVehicleState(**values)


class CouplingContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reference = load_coupling_architecture(ARCHITECTURE)

    def test_reference_architecture_covers_all_stages_and_replays(self) -> None:
        second = load_coupling_architecture(ARCHITECTURE)
        self.assertEqual(self.reference, second)
        self.assertEqual("coupled-level0-reference-v1", self.reference.architecture_id)
        self.assertEqual(
            COUPLING_STAGES,
            tuple(module.stage for module in self.reference.ordered_modules),
        )
        self.assertEqual(64, len(self.reference.fingerprint_sha256))
        self.assertIn(("state.next", "race_progress_solver"), self.reference.signal_producers)

    def test_module_input_permutation_compiles_identically(self) -> None:
        permuted = compile_coupling_architecture(
            architecture_id=self.reference.architecture_id,
            modules=tuple(reversed(self.reference.ordered_modules)),
            initial_signals=tuple(reversed(self.reference.initial_signals)),
        )
        self.assertEqual(self.reference, permuted)

    def test_missing_producer_is_rejected(self) -> None:
        modules = list(self.reference.ordered_modules)
        target = modules[-1]
        modules[-1] = CoupledModuleSpec(
            target.module_id,
            target.stage,
            target.model_version,
            target.consumes + ("missing.signal",),
            target.produces,
        )
        with self.assertRaisesRegex(CouplingContractError, "without a producer"):
            compile_coupling_architecture(
                architecture_id="missing-producer",
                modules=tuple(modules),
                initial_signals=self.reference.initial_signals,
            )

    def test_duplicate_output_and_identity_are_rejected(self) -> None:
        modules = list(self.reference.ordered_modules)
        duplicate_output = CoupledModuleSpec(
            "second-input",
            "inputs",
            "v1",
            (),
            (modules[0].produces[0],),
        )
        with self.assertRaisesRegex(CouplingContractError, "multiple producers"):
            compile_coupling_architecture(
                architecture_id="duplicate-output",
                modules=tuple(modules + [duplicate_output]),
                initial_signals=self.reference.initial_signals,
            )
        with self.assertRaisesRegex(CouplingContractError, "module_id values"):
            compile_coupling_architecture(
                architecture_id="duplicate-id",
                modules=tuple(modules + [modules[0]]),
                initial_signals=self.reference.initial_signals,
            )

    def test_same_or_later_stage_dependency_is_rejected(self) -> None:
        modules = list(self.reference.ordered_modules)
        input_module = modules[0]
        modules[0] = CoupledModuleSpec(
            input_module.module_id,
            input_module.stage,
            input_module.model_version,
            ("aero.force_moment",),
            input_module.produces,
        )
        with self.assertRaisesRegex(CouplingContractError, "same or a later stage"):
            compile_coupling_architecture(
                architecture_id="causal-reversal",
                modules=tuple(modules),
                initial_signals=self.reference.initial_signals,
            )

    def test_missing_required_stage_is_rejected(self) -> None:
        modules = tuple(
            module
            for module in self.reference.ordered_modules
            if module.stage != "health"
        )
        with self.assertRaisesRegex(CouplingContractError, "stages are missing"):
            compile_coupling_architecture(
                architecture_id="missing-health",
                modules=modules,
                initial_signals=self.reference.initial_signals,
            )

    def test_loader_fails_closed_on_unknown_keys_bad_json_and_types(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            unknown = root / "unknown.json"
            unknown.write_text(
                '{"schema_version":"1.0","architecture_id":"x",'
                '"initial_signals":[],"modules":[],"extra":1}',
                encoding="utf-8",
            )
            bad = root / "bad.json"
            bad.write_text("{not-json", encoding="utf-8")
            wrong_type = root / "wrong-type.json"
            wrong_type.write_text(
                '{"schema_version":"1.0","architecture_id":123,'
                '"initial_signals":[],"modules":[]}',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(CouplingContractError, "keys mismatch"):
                load_coupling_architecture(unknown)
            with self.assertRaisesRegex(CouplingContractError, "invalid coupling"):
                load_coupling_architecture(bad)
            with self.assertRaisesRegex(CouplingContractError, "must be a string"):
                load_coupling_architecture(wrong_type)

    def test_manifest_fingerprint_is_order_invariant_and_pinned(self) -> None:
        first = manifest()
        permuted = manifest(
            geometry_artifacts=tuple(reversed(first.geometry_artifacts)),
            model_versions=tuple(reversed(first.model_versions)),
        )
        self.assertEqual(first.fingerprint_sha256, permuted.fingerprint_sha256)
        self.assertEqual(64, len(first.fingerprint_sha256))
        changed_seed = manifest(random_seed=18)
        self.assertNotEqual(first.fingerprint_sha256, changed_seed.fingerprint_sha256)

    def test_invalid_manifest_contracts_are_rejected(self) -> None:
        invalid = (
            lambda: manifest(architecture_fingerprint_sha256="bad"),
            lambda: manifest(source_commit="not-a-commit"),
            lambda: manifest(random_seed=True),
            lambda: manifest(evaluation_budget=0),
            lambda: manifest(time_step_s=math.nan),
            lambda: manifest(geometry_artifacts=()),
            lambda: manifest(
                model_versions=(VersionPin("same", "v1"), VersionPin("same", "v2"))
            ),
        )
        for constructor in invalid:
            with self.subTest(constructor=constructor):
                with self.assertRaises(CouplingContractError):
                    constructor()

    def test_topology_neutral_three_contact_state_and_invalid_states(self) -> None:
        state = shared_state()
        self.assertEqual(3, len(state.contacts))
        self.assertEqual(state, shared_state())
        invalid = (
            lambda: shared_state(contacts=()),
            lambda: shared_state(contacts=(contact("same"), contact("same"))),
            lambda: shared_state(primary_energy_j=-1.0),
            lambda: shared_state(position_m=(0.0, math.nan, 0.0)),
            lambda: shared_state(completed_laps=True),
            lambda: shared_state(status="won"),
        )
        for constructor in invalid:
            with self.subTest(constructor=constructor):
                with self.assertRaises(CouplingContractError):
                    constructor()

    def test_residual_ledger_preserves_failure_without_correction(self) -> None:
        passing = ResidualEntry("force-x", "force", 0.01, "N", 0.001, 1.0e-6, 10_000.0)
        failing = ResidualEntry("energy", "energy", -2.0, "J", 0.1, 0.0, 100.0)
        ledger = ResidualLedger((passing, failing))
        self.assertTrue(passing.passed)
        self.assertFalse(failing.passed)
        self.assertEqual(-2.0, failing.value)
        self.assertEqual("invalid", ledger.status)
        self.assertEqual(("energy",), ledger.failed_residual_ids)
        with self.assertRaisesRegex(CouplingContractError, "unit must be"):
            ResidualEntry("wrong-unit", "moment", 0.0, "N", 0.0, 0.0, 1.0)

    def test_event_arbitration_localizes_time_and_resolves_ties(self) -> None:
        decision = arbitrate_event_candidates(
            (
                EventCandidate("finish", "finished", 10.0, "race"),
                EventCandidate("thermal", "thermal_failure", 10.0, "health"),
                EventCandidate("step", "step_complete", 12.0, "orchestrator"),
            )
        )
        self.assertEqual("finish", decision.winner.event_id)
        self.assertEqual(("finish", "thermal"), decision.tied_candidate_ids)
        earlier = arbitrate_event_candidates(
            (
                EventCandidate("finish", "finished", 10.0, "race"),
                EventCandidate("thermal", "thermal_failure", 9.9, "health"),
            )
        )
        self.assertEqual("thermal", earlier.winner.event_id)
        self.assertEqual(9.9, earlier.earliest_time_s)
        with self.assertRaisesRegex(CouplingContractError, "IDs must be unique"):
            arbitrate_event_candidates(
                (
                    EventCandidate("same", "finished", 1.0, "race"),
                    EventCandidate("same", "timeout", 2.0, "race"),
                )
            )


if __name__ == "__main__":
    unittest.main()
