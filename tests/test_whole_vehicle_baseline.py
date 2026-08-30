import copy
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import unittest

from formula_ultimate.experiments.whole_vehicle_baseline import (
    WholeVehicleBaselineError,
    convergence_metrics,
    evaluate_baseline,
    evaluate_reference_matrix,
    validate_baseline_inputs,
)
from formula_ultimate.simulation.vehicle_load_cases import (
    canonical_sha256,
    evaluate_all_load_cases,
    validate_protocol as validate_load_protocol,
)


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class WholeVehicleBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = read("config/vehicle/fixed_topology_end_to_end_baseline_v1.json")
        load_protocol = read("config/vehicle/whole_vehicle_load_cases_v1.json")
        assembly_raw = read("config/vehicle/topology_neutral_vehicle_v1.json")
        failure = read("config/simulation/structural_failure_coupling_v1.json")
        assembly = validate_load_protocol(
            load_protocol, assembly_raw,
            assembly_config_sha256=hashlib.sha256((ROOT / "config/vehicle/topology_neutral_vehicle_v1.json").read_bytes()).hexdigest(),
            assembly_step_sha256=load_protocol["assembly_identity"]["assembly_step_sha256"],
            failure_config_sha256=hashlib.sha256((ROOT / "config/simulation/structural_failure_coupling_v1.json").read_bytes()).hexdigest(),
        )
        ready = [asdict(item) for item in evaluate_all_load_cases(load_protocol, assembly, failure)]
        cls.work048 = {
            "assembly_step_sha256": load_protocol["assembly_identity"]["assembly_step_sha256"],
            "partitions": {
                "training": load_protocol["partitions"]["training"],
                "training_sha256": canonical_sha256(tuple(load_protocol["partitions"]["training"])),
                "holdout": load_protocol["partitions"]["holdout"],
                "holdout_sha256": canonical_sha256(tuple(load_protocol["partitions"]["holdout"])),
            },
            "results": ready,
            "replay": {"result_set_sha256": canonical_sha256(ready)},
        }

    def validate(self, protocol=None, work048=None):
        validate_baseline_inputs(
            protocol or self.protocol, work048 or self.work048,
            load_case_protocol_sha256=hashlib.sha256((ROOT / "config/vehicle/whole_vehicle_load_cases_v1.json").read_bytes()).hexdigest(),
            work048_source_commit=self.protocol["upstream_identity"]["work048_source_commit"],
        )

    def test_reference_matrix_finishes_and_converges(self):
        self.validate()
        matrix = evaluate_reference_matrix(self.protocol, self.work048)
        self.assertEqual(9, len(matrix))
        self.assertEqual({"finished"}, {item.outcome for item in matrix})
        metrics = convergence_metrics(self.protocol, matrix)
        self.assertEqual("passed", metrics["status"])

    def test_failure_and_heavy_controls(self):
        common = dict(timestep_s=0.5, structural_resolution_id="bounded_reference")
        weak = evaluate_baseline(self.protocol, self.work048, variant_id="weak_control", **common)
        disconnected = evaluate_baseline(self.protocol, self.work048, variant_id="disconnected_control", **common)
        heavy = evaluate_baseline(self.protocol, self.work048, variant_id="heavy_feasible_control", **common)
        reference = evaluate_baseline(self.protocol, self.work048, variant_id="reference", **common)
        self.assertEqual(("DNF", "DNF", "finished"), (weak.outcome, disconnected.outcome, heavy.outcome))
        self.assertGreater(heavy.finish_time_s, reference.finish_time_s)
        self.assertGreater(heavy.energy_used_j, reference.energy_used_j)

    def test_exact_replay_and_complete_case_records(self):
        args = dict(variant_id="reference", timestep_s=0.25, structural_resolution_id="bounded_high")
        first = evaluate_baseline(self.protocol, self.work048, **args)
        second = evaluate_baseline(self.protocol, self.work048, **args)
        self.assertEqual(first, second)
        self.assertEqual(7, len(first.case_records))
        self.assertEqual({"training", "holdout"}, {item.partition for item in first.case_records})

    def test_identity_and_missing_evidence_fail_closed(self):
        altered = copy.deepcopy(self.work048)
        altered["assembly_step_sha256"] = "0" * 64
        with self.assertRaisesRegex(WholeVehicleBaselineError, "assembly_step"):
            self.validate(work048=altered)
        missing = copy.deepcopy(self.protocol)
        missing["variants"][0]["evidence"].pop()
        with self.assertRaisesRegex(WholeVehicleBaselineError, "evidence"):
            self.validate(protocol=missing)


if __name__ == "__main__":
    unittest.main()
