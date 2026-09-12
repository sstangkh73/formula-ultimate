import copy
import json
import unittest
from pathlib import Path

from formula_ultimate.assembly.detailed_vehicle_closure import DetailedVehicleClosureViolation, evaluate_closure, validate_protocol

ROOT = Path(__file__).resolve().parents[1]


class DetailedVehicleClosureTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads((ROOT / "config/development/detailed_vehicle_closure_v1.json").read_text(encoding="utf-8"))

    def test_protocol_pins_dependencies_and_g3_boundary(self):
        self.assertEqual(validate_protocol(self.raw)["status"], "passed")
        self.assertEqual(self.raw["coverage"]["native_CAD"], "unresolved")
        self.assertFalse(self.raw["coverage"]["promotion_ready"])

    def test_complete_candidate_ledgers_paths_and_motion(self):
        result = evaluate_closure(self.raw)
        self.assertTrue(result["all_paths_closed"])
        self.assertEqual(result["component_count"], 12)
        self.assertFalse(result["motion_collisions"])
        self.assertAlmostEqual(result["computed_ledgers"]["mass_kg"], 60.0)

    def test_removed_fastener_support_seal_and_signal_fail(self):
        for role in ("fastener", "support", "seal", "signal"):
            mutated = copy.deepcopy(self.raw)
            mutated["components"] = [item for item in mutated["components"] if item["role"] != role]
            with self.subTest(role=role), self.assertRaisesRegex(DetailedVehicleClosureViolation, "missing required hardware role"):
                evaluate_closure(mutated)

    def test_double_mass_and_hidden_void_fail(self):
        duplicate = copy.deepcopy(self.raw)
        duplicate["components"][1]["region_id"] = duplicate["components"][0]["region_id"]
        with self.assertRaisesRegex(DetailedVehicleClosureViolation, "double mass ownership"):
            evaluate_closure(duplicate)
        void = copy.deepcopy(self.raw)
        void["components"][0]["center_m"][0] = -4.0
        with self.assertRaisesRegex(DetailedVehicleClosureViolation, "hidden void"):
            evaluate_closure(void)

    def test_interference_and_stale_envelope_fail(self):
        collision = copy.deepcopy(self.raw)
        collision["components"][1]["center_m"] = collision["components"][0]["center_m"][:]
        with self.assertRaisesRegex(DetailedVehicleClosureViolation, "assembly interference"):
            evaluate_closure(collision)
        stale = copy.deepcopy(self.raw)
        stale["components"][0]["envelope_revision"] = "old"
        with self.assertRaisesRegex(DetailedVehicleClosureViolation, "stale subsystem envelope"):
            evaluate_closure(stale)

    def test_open_signal_path_fails(self):
        mutated = copy.deepcopy(self.raw)
        mutated["networks"]["signal"]["edges"] = []
        with self.assertRaisesRegex(DetailedVehicleClosureViolation, "open energy, signal, heat, or load path"):
            evaluate_closure(mutated)


if __name__ == "__main__":
    unittest.main()
