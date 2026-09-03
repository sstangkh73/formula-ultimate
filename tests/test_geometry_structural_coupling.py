from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.structural.geometry_coupling import (
    GeometryStructuralViolation,
    adjudicate_solver_evidence,
    canonical_sha256,
    propagate_connection_state,
    validate_coupling_config,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/structural/geometry_structural_coupling_v1.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def evidence(config: dict) -> dict:
    rows = []
    for index, mesh in enumerate(config["mesh_levels"]):
        factor = (1.0, 1.02, 1.04)[index]
        rows.append({
            "mesh_id": mesh["mesh_id"], "nodes": 100 * (index + 1), "elements": 400 * (index + 1),
            "maximum_displacement_m": 1.0e-5 * factor,
            "compliance_m_per_n": 2.0e-8 * factor,
            "p90_von_mises_stress_pa": 4.0e6 * factor,
            "force_residual_relative": 1e-8, "moment_residual_relative": 1e-8, "energy_residual_relative": 1e-8,
        })
    geometry = config["geometry"]
    return {
        "geometry_identities": {key: geometry[key] for key in ("step_sha256", "freecad_report_sha256", "loaded_surface_signature_sha256")},
        "mesh_results": rows, "solver_converged": True, "hidden_geometry_repair": False,
    }


class GeometryStructuralCouplingTests(unittest.TestCase):
    def assert_code(self, code: str, config: dict, raw: dict) -> None:
        with self.assertRaises(GeometryStructuralViolation) as caught:
            adjudicate_solver_evidence(config, raw)
        self.assertEqual(code, caught.exception.code)

    def test_reference_config_and_evidence_pass_as_synthetic_only(self) -> None:
        config = load_config()
        self.assertEqual("passed", validate_coupling_config(config)["status"])
        result = adjudicate_solver_evidence(config, evidence(config))
        self.assertEqual("elastic", result["structural_state"])
        self.assertFalse(result["design_use_allowed"])
        self.assertEqual(["fracture", "fatigue"], result["unsupported_failure_modes"])

    def test_mapping_key_order_is_canonical(self) -> None:
        config = load_config()
        reversed_config = {key: config[key] for key in reversed(tuple(config))}
        self.assertEqual(canonical_sha256(config), canonical_sha256(reversed_config))

    def test_exact_geometry_identities_are_required(self) -> None:
        config = load_config(); raw = evidence(config)
        raw["geometry_identities"]["step_sha256"] = "0" * 64
        self.assert_code("geometry_identity_mismatch", config, raw)

    def test_solver_nonconvergence_and_hidden_repair_fail_closed(self) -> None:
        config = load_config(); raw = evidence(config); raw["solver_converged"] = False
        self.assert_code("solver_nonconvergence", config, raw)
        raw = evidence(config); raw["hidden_geometry_repair"] = True
        self.assert_code("hidden_geometry_repair", config, raw)

    def test_force_moment_and_energy_residuals_fail_closed(self) -> None:
        config = load_config()
        for key in ("force_residual_relative", "moment_residual_relative", "energy_residual_relative"):
            raw = evidence(config); raw["mesh_results"][1][key] = config["tolerances"][key] * 2
            with self.subTest(key=key): self.assert_code("residual_gate_failed", config, raw)

    def test_each_last_two_mesh_metric_must_converge(self) -> None:
        config = load_config()
        for key in ("maximum_displacement_m", "compliance_m_per_n", "p90_von_mises_stress_pa"):
            raw = evidence(config); raw["mesh_results"][-1][key] *= 1.2
            with self.subTest(key=key): self.assert_code("mesh_nonconvergence", config, raw)

    def test_nonfinite_and_missing_mesh_evidence_fail_closed(self) -> None:
        config = load_config(); raw = evidence(config); raw["mesh_results"][0]["maximum_displacement_m"] = math.nan
        self.assert_code("invalid_numeric_value", config, raw)
        raw = evidence(config); raw["mesh_results"].pop()
        self.assert_code("invalid_refinement", config, raw)

    def test_synthetic_evidence_cannot_be_relabelled_for_design_use(self) -> None:
        config = load_config(); config["material"]["evidence_status"] = "sourced"
        with self.assertRaisesRegex(GeometryStructuralViolation, "synthetic"):
            validate_coupling_config(config)
        config = load_config(); config["claim_boundary"]["design_use_allowed"] = True
        with self.assertRaisesRegex(GeometryStructuralViolation, "design use"):
            validate_coupling_config(config)

    def test_failure_classification_uses_measured_stress_domain(self) -> None:
        config = load_config(); raw = evidence(config)
        raw["mesh_results"][-2]["p90_von_mises_stress_pa"] = 260e6
        raw["mesh_results"][-1]["p90_von_mises_stress_pa"] = 265e6
        self.assertEqual("yield_domain_exceeded", adjudicate_solver_evidence(config, raw)["structural_state"])
        raw["mesh_results"][-2]["p90_von_mises_stress_pa"] = 320e6
        raw["mesh_results"][-1]["p90_von_mises_stress_pa"] = 325e6
        self.assertEqual("ultimate_domain_exceeded", adjudicate_solver_evidence(config, raw)["structural_state"])

    def test_critical_failure_removes_wrench_and_causes_dnf(self) -> None:
        config = load_config()
        intact = propagate_connection_state(config, "elastic")
        failed = propagate_connection_state(config, "severed_load_path")
        self.assertEqual(config["load_case"]["force_n"], intact["transmitted_force_n"])
        self.assertEqual([0.0, 0.0, 0.0], failed["transmitted_force_n"])
        self.assertEqual("failed", failed["connection_state"])
        self.assertEqual("dnf", failed["subsystem_state"])


if __name__ == "__main__":
    unittest.main()
