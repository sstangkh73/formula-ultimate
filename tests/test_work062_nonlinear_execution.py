from __future__ import annotations

import unittest

from formula_ultimate.structural import (
    VehicleFrameError,
    adjudicate_nonlinear_case,
    nonlinear_gate_config_from_mapping,
)
from scripts.structural.run_whole_vehicle_nonlinear_gate import summarize_terminal_records


def raw_config() -> dict:
    return {
        "protocol_id": "whole_vehicle_geometric_nonlinearity_gate_v1",
        "claim_level": "test",
        "source_evidence": {"campaign_id": "source"},
        "execution": {
            "mesh_subdivisions": 16,
            "required_holdout_case_ids": ["a", "b"],
            "required_solver_confirmation": "nonlinear geometric",
        },
        "material": {"yield_stress_pa": 250e6},
        "thresholds": {
            "maximum_displacement_amplification": 1.1,
            "maximum_stress_amplification": 1.15,
            "minimum_yield_margin": 1.1,
        },
        "limitations": ["test_only"],
    }


def case(config, candidate, case_id, nonlinear_displacement=0.0101):
    return adjudicate_nonlinear_case(
        config,
        candidate_id=candidate,
        case_id=case_id,
        linear_displacement_m=0.01,
        linear_surface_stress_pa=100e6,
        nonlinear_displacement_m=nonlinear_displacement,
        nonlinear_surface_stress_pa=101e6,
        process_exit_code=0,
        solver_stdout="nonlinear geometric",
    )


class Work062NonlinearExecutionTests(unittest.TestCase):
    def test_summary_is_deterministic_and_counts_terminal_failures(self):
        raw = raw_config(); config = nonlinear_gate_config_from_mapping(raw)
        records = [
            {"record_type": "nonlinear_case_result", "result": case(config, "c1", "a")},
            {"record_type": "nonlinear_case_result", "result": case(config, "c1", "b")},
            {"record_type": "nonlinear_case_result", "result": case(config, "c2", "a", 0.012)},
            {"record_type": "nonlinear_case_result", "result": case(config, "c2", "b")},
        ]
        source = {"candidate_ids": ("c1", "c2")}
        kwargs = dict(config_raw=raw, source=source, records=records, ledger_fingerprint="f" * 64, identities={"x": "y"}, execution_commit="a" * 40)
        first = summarize_terminal_records(**kwargs)
        second = summarize_terminal_records(**kwargs)
        self.assertEqual(first, second)
        self.assertEqual({"failed": 1, "passed": 1}, first["terminal"]["candidate_status_counts"])
        self.assertEqual(4, first["terminal"]["case_count"])

    def test_summary_rejects_incomplete_duplicate_and_out_of_scope_records(self):
        raw = raw_config(); config = nonlinear_gate_config_from_mapping(raw)
        source = {"candidate_ids": ("c1",)}
        a = {"record_type": "nonlinear_case_result", "result": case(config, "c1", "a")}
        b = {"record_type": "nonlinear_case_result", "result": case(config, "c1", "b")}
        base = dict(config_raw=raw, source=source, ledger_fingerprint="f" * 64, identities={}, execution_commit="a" * 40)
        with self.assertRaisesRegex(VehicleFrameError, "incomplete"):
            summarize_terminal_records(records=(a,), **base)
        with self.assertRaisesRegex(VehicleFrameError, "duplicate"):
            summarize_terminal_records(records=(a, a), **base)
        outside = {"record_type": "nonlinear_case_result", "result": case(config, "c2", "b")}
        with self.assertRaisesRegex(VehicleFrameError, "out-of-scope"):
            summarize_terminal_records(records=(a, outside), **base)
        self.assertEqual("passed", summarize_terminal_records(records=(a, b), **base)["status"])


if __name__ == "__main__":
    unittest.main()
