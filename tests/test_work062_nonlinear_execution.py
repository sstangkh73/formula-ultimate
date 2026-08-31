from __future__ import annotations

import unittest
import json
from pathlib import Path
import tempfile

from formula_ultimate.structural import (
    VehicleFrameError,
    adjudicate_nonlinear_case,
    nonlinear_gate_config_from_mapping,
)
from scripts.structural.run_whole_vehicle_nonlinear_gate import (
    json_compatible,
    summarize_terminal_records,
    validate_execution_protocol,
)


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


def execution_protocol() -> dict:
    return {
        "protocol_id": "work062_finalist_nonlinear_execution_v2",
        "campaign_id": "FU-NLG-002",
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
        kwargs = dict(config_raw=raw, source=source, records=records, ledger_fingerprint="f" * 64, identities={"x": "y"}, execution_commit="a" * 40, execution_protocol=execution_protocol())
        first = json_compatible(summarize_terminal_records(**kwargs))
        second = json_compatible(summarize_terminal_records(**kwargs))
        self.assertEqual(first, second)
        self.assertEqual({"failed": 1, "passed": 1}, first["terminal"]["candidate_status_counts"])
        self.assertEqual(4, first["terminal"]["case_count"])

    def test_summary_rejects_incomplete_duplicate_and_out_of_scope_records(self):
        raw = raw_config(); config = nonlinear_gate_config_from_mapping(raw)
        source = {"candidate_ids": ("c1",)}
        a = {"record_type": "nonlinear_case_result", "result": case(config, "c1", "a")}
        b = {"record_type": "nonlinear_case_result", "result": case(config, "c1", "b")}
        base = dict(config_raw=raw, source=source, ledger_fingerprint="f" * 64, identities={}, execution_commit="a" * 40, execution_protocol=execution_protocol())
        with self.assertRaisesRegex(VehicleFrameError, "incomplete"):
            summarize_terminal_records(records=(a,), **base)
        with self.assertRaisesRegex(VehicleFrameError, "duplicate"):
            summarize_terminal_records(records=(a, a), **base)
        outside = {"record_type": "nonlinear_case_result", "result": case(config, "c2", "b")}
        with self.assertRaisesRegex(VehicleFrameError, "out-of-scope"):
            summarize_terminal_records(records=(a, outside), **base)
        self.assertEqual("passed", summarize_terminal_records(records=(a, b), **base)["status"])

    def test_strict_json_round_trip_replays_tuple_bearing_summary(self):
        raw = raw_config(); config = nonlinear_gate_config_from_mapping(raw)
        records = (
            {"record_type": "nonlinear_case_result", "result": case(config, "c1", "a")},
            {"record_type": "nonlinear_case_result", "result": case(config, "c1", "b")},
        )
        calculated = json_compatible(summarize_terminal_records(
            config_raw=raw,
            source={"candidate_ids": ("c1",)},
            records=records,
            ledger_fingerprint="f" * 64,
            identities={},
            execution_commit="a" * 40,
            execution_protocol=execution_protocol(),
        ))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "summary.json"
            path.write_text(json.dumps(calculated, allow_nan=False), encoding="utf-8")
            recorded = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(recorded, calculated)

    def test_v2_protocol_identity_and_unchanged_science_are_required(self):
        raw = {
            "protocol_id": "work062_finalist_nonlinear_execution_v2",
            "campaign_id": "FU-NLG-002",
            "gate_config_sha256": "g",
            "remediation": {"scientific_rules_changed": False, "work064_observations_reused": False},
        }
        self.assertEqual(
            ("work062_finalist_nonlinear_execution_v2", "FU-NLG-002"),
            validate_execution_protocol(raw, gate_config_sha256="g"),
        )
        changed = dict(raw); changed["remediation"] = dict(raw["remediation"], scientific_rules_changed=True)
        with self.assertRaisesRegex(VehicleFrameError, "unchanged-science"):
            validate_execution_protocol(changed, gate_config_sha256="g")


if __name__ == "__main__":
    unittest.main()
