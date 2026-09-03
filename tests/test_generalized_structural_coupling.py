from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from formula_ultimate.structural.generalized_coupling import (
    GeneralizedCouplingViolation,
    adjudicate,
    canonical_sha256,
    validate_config,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/structural/generalized_meshed_torsion_bearing_housing_v1.json"


def raw_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def evidence() -> dict:
    metric = {
        "solver_converged": True,
        "loaded_nodes": 12,
        "support_nodes": 8,
        "maximum_displacement_m": 1e-5,
        "compliance_m_per_n": 2e-8,
        "p90_von_mises_stress_pa": 4e6,
        "force_residual_relative": 1e-8,
        "moment_residual_relative": 2e-8,
        "energy_residual_relative": 3e-8,
    }
    control = {
        "connection_state": "severed",
        "transmitted_force_n": [0.0, 0.0, 0.0],
        "transmitted_torque_nm": [0.0, 0.0, 0.0],
        "subsystem_state": "dnf",
    }
    return {
        "source_identities_verified": True,
        "hidden_geometry_repair": False,
        "case_results": [
            {"case_id": case_id, "mesh_results": [deepcopy(metric) for _ in range(3)], "severed_support_control": deepcopy(control)}
            for case_id in ("output_shaft_combined", "support_block_bearing", "converter_housing_mount")
        ],
    }


class GeneralizedStructuralCouplingTests(unittest.TestCase):
    def test_reference_config_is_valid(self) -> None:
        result = validate_config(raw_config())
        self.assertEqual(result["status"], "passed")
        self.assertEqual(len(result["case_ids"]), 3)

    def test_unknown_field_fails_closed(self) -> None:
        raw = raw_config(); raw["extra"] = True
        with self.assertRaisesRegex(GeneralizedCouplingViolation, "fields mismatch"):
            validate_config(raw)

    def test_material_cannot_be_relabelled(self) -> None:
        raw = raw_config(); raw["material"]["design_use_allowed"] = True
        with self.assertRaisesRegex(GeneralizedCouplingViolation, "synthetic-only"):
            validate_config(raw)

    def test_mesh_levels_must_strictly_refine(self) -> None:
        raw = raw_config(); raw["cases"][0]["mesh_levels_m"] = [0.002, 0.003, 0.001]
        with self.assertRaisesRegex(GeneralizedCouplingViolation, "refine strictly"):
            validate_config(raw)

    def test_required_case_set_cannot_change(self) -> None:
        raw = raw_config(); raw["cases"][0]["case_id"] = "replacement"
        with self.assertRaisesRegex(GeneralizedCouplingViolation, "cases changed"):
            validate_config(raw)

    def test_reference_fabricated_solver_evidence_passes_as_synthetic_only(self) -> None:
        result = adjudicate(raw_config(), evidence())
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["verdict"], "synthetic_meshed_verification_only")
        self.assertFalse(result["design_use_allowed"])

    def test_last_two_mesh_change_fails_closed(self) -> None:
        data = evidence(); data["case_results"][2]["mesh_results"][2]["maximum_displacement_m"] = 2e-5
        with self.assertRaisesRegex(GeneralizedCouplingViolation, "mesh convergence"):
            adjudicate(raw_config(), data)

    def test_equilibrium_residual_fails_closed(self) -> None:
        data = evidence(); data["case_results"][0]["mesh_results"][1]["moment_residual_relative"] = 2e-5
        with self.assertRaisesRegex(GeneralizedCouplingViolation, "residual"):
            adjudicate(raw_config(), data)

    def test_noncausal_severed_support_fails_closed(self) -> None:
        data = evidence(); data["case_results"][1]["severed_support_control"]["subsystem_state"] = "operational"
        with self.assertRaisesRegex(GeneralizedCouplingViolation, "not causal"):
            adjudicate(raw_config(), data)

    def test_source_identity_failure_is_observable(self) -> None:
        data = evidence(); data["source_identities_verified"] = False
        with self.assertRaisesRegex(GeneralizedCouplingViolation, "source identity"):
            adjudicate(raw_config(), data)

    def test_nonfinite_solver_metric_fails_closed(self) -> None:
        data = evidence(); data["case_results"][0]["mesh_results"][0]["p90_von_mises_stress_pa"] = float("nan")
        with self.assertRaisesRegex(GeneralizedCouplingViolation, "finite domain"):
            adjudicate(raw_config(), data)

    def test_canonical_hash_ignores_mapping_order(self) -> None:
        self.assertEqual(canonical_sha256({"a": 1, "b": 2}), canonical_sha256({"b": 2, "a": 1}))


if __name__ == "__main__":
    unittest.main()
