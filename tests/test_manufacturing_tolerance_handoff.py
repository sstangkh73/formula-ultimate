import copy
import json
import unittest
from pathlib import Path

from formula_ultimate.assembly.manufacturing_tolerance_handoff import ManufacturingHandoffViolation, evaluate_handoff, validate_protocol

ROOT = Path(__file__).resolve().parents[1]


class ManufacturingToleranceHandoffTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads((ROOT / "config/development/manufacturing_tolerance_handoff_v1.json").read_text(encoding="utf-8"))

    def test_protocol_maps_all_regions_and_dependencies(self):
        self.assertEqual(validate_protocol(self.raw)["status"], "passed")
        self.assertEqual(len(self.raw["routes"]), 12)

    def test_tolerances_and_order_pass_but_readiness_is_blocked(self):
        result = evaluate_handoff(self.raw)
        self.assertTrue(all(item["passed"] for item in result["tolerance_results"]))
        self.assertFalse(result["manufacturing_ready"])
        self.assertEqual(result["unknown_route_count"], 12)

    def test_inaccessible_fastener_and_trapped_core_fail(self):
        inaccessible = copy.deepcopy(self.raw); inaccessible["routes"][6]["tool_access"] = False
        with self.assertRaisesRegex(ManufacturingHandoffViolation, "inaccessible fastener"):
            evaluate_handoff(inaccessible)
        trapped = copy.deepcopy(self.raw); trapped["routes"][0]["trapped_internal_core"] = True
        with self.assertRaisesRegex(ManufacturingHandoffViolation, "trapped internal core"):
            evaluate_handoff(trapped)

    def test_impossible_assembly_order_fails(self):
        cyclic = copy.deepcopy(self.raw); cyclic["assembly_steps"][0]["after"] = ["inspect_final"]
        with self.assertRaisesRegex(ManufacturingHandoffViolation, "impossible cyclic assembly order"):
            evaluate_handoff(cyclic)

    def test_nominal_only_clearance_and_preload_fail(self):
        clearance = copy.deepcopy(self.raw); clearance["tolerance_cases"][0]["nominal_clearance_m"] = 0.0003
        with self.assertRaisesRegex(ManufacturingHandoffViolation, "worst-case clearance"):
            evaluate_handoff(clearance)
        preload = copy.deepcopy(self.raw); preload["tolerance_cases"][1]["preload_tolerance_n"] = 200.0
        with self.assertRaisesRegex(ManufacturingHandoffViolation, "worst-case clearance or preload"):
            evaluate_handoff(preload)

    def test_missing_region_route_fails(self):
        missing = copy.deepcopy(self.raw); missing["routes"] = missing["routes"][:-1]
        with self.assertRaisesRegex(ManufacturingHandoffViolation, "region route mapping"):
            validate_protocol(missing)


if __name__ == "__main__":
    unittest.main()
