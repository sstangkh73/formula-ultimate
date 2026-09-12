import copy
import json
import unittest
from pathlib import Path

from formula_ultimate.experiments.optimized_vehicle_controls import OptimizedVehicleControlsViolation, run_comparison, validate_protocol

ROOT = Path(__file__).resolve().parents[1]


class OptimizedVehicleControlsTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads((ROOT / "config/development/optimized_vehicle_controls_v1.json").read_text(encoding="utf-8"))

    def test_protocol_pins_dependencies_and_equal_budgets(self):
        self.assertEqual(validate_protocol(self.raw)["status"], "passed")
        self.assertEqual(len({tuple(x.values()) for x in self.raw["budgets"].values()}), 1)

    def test_all_arms_optimized_and_retuned_at_equal_cost(self):
        result = run_comparison(self.raw)
        self.assertEqual(set(result["tuning"]), set(self.raw["arms"]))
        self.assertEqual(len(set(result["complete_costs"].values())), 1)
        self.assertTrue(all(item["search_evaluations"] == 4 for item in result["tuning"].values()))

    def test_transferred_burdens_block_meaningful_benefit(self):
        result = run_comparison(self.raw)
        self.assertLess(result["mean_effect"], self.raw["registration"]["meaningful_system_effect"])
        self.assertFalse(result["system_benefit_gate"])

    def test_untuned_baseline_and_free_controller_fail(self):
        untuned = copy.deepcopy(self.raw)
        untuned["arms"]["fixed_topology"]["baseline_tuned"] = False
        with self.assertRaisesRegex(OptimizedVehicleControlsViolation, "untuned baseline"):
            validate_protocol(untuned)
        free = copy.deepcopy(self.raw)
        free["budgets"]["reference"]["controller_tuning"] = 0
        with self.assertRaisesRegex(OptimizedVehicleControlsViolation, "search or tuning budgets are unequal|free controller"):
            validate_protocol(free)

    def test_omitted_cooling_and_unequal_energy_fail(self):
        omitted = copy.deepcopy(self.raw)
        del omitted["arms"]["open_candidate"]["burdens"]["cooling_mass_kg"]
        with self.assertRaisesRegex(OptimizedVehicleControlsViolation, "incomplete burden ledger"):
            validate_protocol(omitted)
        unequal = copy.deepcopy(self.raw)
        unequal["arms"]["open_candidate"]["source_energy_j"] += 1.0
        with self.assertRaisesRegex(OptimizedVehicleControlsViolation, "source energy is unequal"):
            validate_protocol(unequal)

    def test_fixed_control_does_not_constrain_open_layout(self):
        self.assertNotIn("topology", self.raw["arms"]["open_candidate"])
        self.assertIn("fixed_topology", self.raw["arms"])


if __name__ == "__main__":
    unittest.main()
