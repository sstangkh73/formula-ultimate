from __future__ import annotations

import unittest

from formula_ultimate.structural import (
    VehicleFrameError,
    adjudicate_nonlinear_case,
    aggregate_candidate_nonlinear_gate,
    benchmark_model,
    build_calculix_b31_deck,
    nonlinear_gate_config_from_mapping,
)


def raw_config() -> dict:
    return {
        "protocol_id": "whole_vehicle_geometric_nonlinearity_gate_v1",
        "execution": {
            "mesh_subdivisions": 16,
            "required_holdout_case_ids": ["a", "b"],
            "required_solver_confirmation": "nonlinear geometric",
        },
        "material": {"yield_stress_pa": 250e6},
        "thresholds": {
            "maximum_displacement_amplification": 1.10,
            "maximum_stress_amplification": 1.15,
            "minimum_yield_margin": 1.10,
        },
    }


def case(config, case_id="a", **overrides):
    values = {
        "candidate_id": "candidate-x",
        "case_id": case_id,
        "linear_displacement_m": 0.01,
        "linear_surface_stress_pa": 100e6,
        "nonlinear_displacement_m": 0.0105,
        "nonlinear_surface_stress_pa": 105e6,
        "process_exit_code": 0,
        "solver_stdout": "Nonlinear geometric effects enabled",
    }
    values.update(overrides)
    return adjudicate_nonlinear_case(config, **values)


class VehicleNonlinearGateTests(unittest.TestCase):
    def test_linear_deck_default_is_unchanged_and_nonlinear_is_explicit(self):
        model, loads = benchmark_model(1.0, 0.02, 2)
        linear = build_calculix_b31_deck(model, loads, 70e9, 0.3)
        nonlinear = build_calculix_b31_deck(model, loads, 70e9, 0.3, geometric_nonlinear=True)
        self.assertIn("*STEP\n*STATIC\n*BOUNDARY", linear)
        self.assertNotIn("NLGEOM", linear)
        self.assertIn("*STEP,NLGEOM\n*STATIC\n1.000000E-01,1.000000E+00,1.000000E-05,1.000000E-01", nonlinear)

    def test_config_rejects_identity_invalid_threshold_and_duplicate_case(self):
        self.assertEqual(16, nonlinear_gate_config_from_mapping(raw_config()).mesh_subdivisions)
        bad = raw_config(); bad["protocol_id"] = "wrong"
        with self.assertRaisesRegex(VehicleFrameError, "identity"):
            nonlinear_gate_config_from_mapping(bad)
        bad = raw_config(); bad["thresholds"]["minimum_yield_margin"] = 0
        with self.assertRaisesRegex(VehicleFrameError, "positive"):
            nonlinear_gate_config_from_mapping(bad)
        bad = raw_config(); bad["execution"]["required_holdout_case_ids"] = ["a", "a"]
        with self.assertRaisesRegex(VehicleFrameError, "unique"):
            nonlinear_gate_config_from_mapping(bad)

    def test_case_passes_and_hash_replays_exactly(self):
        config = nonlinear_gate_config_from_mapping(raw_config())
        first = case(config)
        second = case(config)
        self.assertEqual(first, second)
        self.assertEqual("passed", first["status"])
        self.assertAlmostEqual(1.05, first["displacement_amplification"])
        self.assertAlmostEqual(2.5e8 / 1.05e8, first["yield_margin"])

    def test_each_falsification_boundary_fails_closed(self):
        config = nonlinear_gate_config_from_mapping(raw_config())
        scenarios = (
            ({"process_exit_code": 1}, "nonlinear_process_failure"),
            ({"solver_stdout": "linear static"}, "nonlinear_confirmation_missing"),
            ({"nonlinear_displacement_m": 0.01101}, "nonlinear_displacement_amplification"),
            ({"nonlinear_surface_stress_pa": 116e6}, "nonlinear_stress_amplification"),
            ({"nonlinear_surface_stress_pa": 230e6}, "nonlinear_yield_margin"),
            ({"nonlinear_surface_stress_pa": float("nan")}, "invalid_nonlinear_evidence"),
        )
        for overrides, expected in scenarios:
            with self.subTest(expected=expected):
                result = case(config, **overrides)
                self.assertEqual("failed", result["status"])
                self.assertIn(expected, result["failure_codes"])

    def test_aggregate_requires_exact_terminal_case_set_and_hashes(self):
        config = nonlinear_gate_config_from_mapping(raw_config())
        a, b = case(config, "a"), case(config, "b")
        result = aggregate_candidate_nonlinear_gate(config, candidate_id="candidate-x", case_results=(a, b))
        self.assertEqual("passed", result["status"])
        self.assertEqual(result, aggregate_candidate_nonlinear_gate(config, candidate_id="candidate-x", case_results=(a, b)))
        with self.assertRaisesRegex(VehicleFrameError, "case set"):
            aggregate_candidate_nonlinear_gate(config, candidate_id="candidate-x", case_results=(a,))
        with self.assertRaisesRegex(VehicleFrameError, "duplicate"):
            aggregate_candidate_nonlinear_gate(config, candidate_id="candidate-x", case_results=(a, a))
        tampered = dict(b); tampered["status"] = "failed"
        with self.assertRaisesRegex(VehicleFrameError, "hash"):
            aggregate_candidate_nonlinear_gate(config, candidate_id="candidate-x", case_results=(a, tampered))


if __name__ == "__main__":
    unittest.main()
