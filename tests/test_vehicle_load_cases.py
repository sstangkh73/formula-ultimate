import copy
import hashlib
import json
from pathlib import Path
import unittest

from formula_ultimate.simulation.vehicle_load_cases import (
    VehicleLoadCaseError,
    evaluate_all_load_cases,
    evaluate_load_case,
    validate_protocol,
)


ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


class VehicleLoadCaseTests(unittest.TestCase):
    def setUp(self):
        self.protocol = load("config/vehicle/whole_vehicle_load_cases_v1.json")
        self.assembly_raw = load("config/vehicle/topology_neutral_vehicle_v1.json")
        self.failure = load("config/simulation/structural_failure_coupling_v1.json")
        self.kw = dict(
            assembly_config_sha256=sha("config/vehicle/topology_neutral_vehicle_v1.json"),
            assembly_step_sha256=self.protocol["assembly_identity"]["assembly_step_sha256"],
            failure_config_sha256=sha("config/simulation/structural_failure_coupling_v1.json"),
        )

    def assembly(self, protocol=None, assembly_raw=None):
        return validate_protocol(protocol or self.protocol, assembly_raw or self.assembly_raw, **self.kw)

    def test_nominal_partitions_balance_and_control_dnf(self):
        results = evaluate_all_load_cases(self.protocol, self.assembly(), self.failure)
        nominal = [item for item in results if item.partition in {"training", "holdout"}]
        self.assertEqual(7, len(nominal))
        self.assertEqual({"running"}, {item.outcome for item in nominal})
        self.assertLessEqual(max(max(abs(x) for x in item.global_residual) for item in results), 1e-5)
        self.assertLessEqual(max(item.maximum_component_residual for item in results), 1e-5)
        control = next(item for item in results if item.partition == "control")
        self.assertEqual("DNF", control.outcome)
        self.assertEqual("ok", control.failure_contract_status)
        self.assertIn("core_contact", [x.connection_id for x in control.connection_loads if x.health_state == "failed"])

    def test_same_snapshot_replays_exactly(self):
        assembly = self.assembly()
        a = evaluate_load_case(self.protocol, assembly, self.failure, "combined_manoeuvre")
        b = evaluate_load_case(self.protocol, assembly, self.failure, "combined_manoeuvre")
        self.assertEqual(a, b)

    def test_identity_and_missing_evidence_fail_closed(self):
        altered = copy.deepcopy(self.assembly_raw)
        altered["candidate_id"] = "changed"
        with self.assertRaisesRegex(VehicleLoadCaseError, "declaration"):
            self.assembly(assembly_raw=altered)
        missing = copy.deepcopy(self.protocol)
        del missing["cases"][0]["evidence"]["contact"]
        with self.assertRaisesRegex(VehicleLoadCaseError, "evidence"):
            self.assembly(protocol=missing)

    def test_unbalanced_and_overlapping_partition_fail_closed(self):
        assembly = self.assembly()
        unbalanced = copy.deepcopy(self.protocol)
        unbalanced["cases"][0]["contact_wrench_at_com"][0] += 1.0
        with self.assertRaisesRegex(VehicleLoadCaseError, "force equilibrium"):
            evaluate_load_case(unbalanced, assembly, self.failure, "straight_acceleration")
        overlap = copy.deepcopy(self.protocol)
        overlap["partitions"]["holdout"].append("straight_acceleration")
        with self.assertRaisesRegex(VehicleLoadCaseError, "overlaps"):
            self.assembly(protocol=overlap)


if __name__ == "__main__":
    unittest.main()
