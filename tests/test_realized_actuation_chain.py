from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from formula_ultimate.subsystems.realized_actuation_chain import (
    ActuationChainViolation,
    evaluate,
    validate_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/development/realized_actuation_chain_v1.json"


class RealizedActuationChainTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads(CONFIG.read_text(encoding="utf-8"))

    def test_protocol_pins_hardware_and_dependencies(self):
        result = validate_protocol(self.raw)
        self.assertGreater(result["hardware_mass_kg"], 0)
        self.assertEqual({item["work"] for item in self.raw["dependencies"]}, {114, 115, 116})

    def test_energy_geometry_and_reactions_are_observable(self):
        result = evaluate(self.raw, 30.0, 100.0, 300.0)
        self.assertAlmostEqual(result["accepted_input_power_w"], result["output_power_w"] + result["loss_power_w"])
        self.assertGreater(result["hardware_mass_kg"], 0)
        self.assertGreater(result["total_output_twist_rad"], 0)
        self.assertLess(result["torque_reaction_per_support_n_m"], 0)

    def test_disconnected_and_locked_destinations(self):
        disconnected = evaluate(self.raw, 30.0, 100.0, 300.0, connected=False)
        locked = evaluate(self.raw, 30.0, 100.0, 300.0, output_locked=True)
        self.assertEqual(disconnected["output_power_w"], 0.0)
        self.assertEqual(disconnected["loss_power_w"], 0.0)
        self.assertEqual(locked["output_power_w"], 0.0)
        self.assertEqual(locked["accepted_input_power_w"], locked["loss_power_w"])

    def test_reverse_operation_is_symmetric(self):
        forward = evaluate(self.raw, 30.0, 100.0, 300.0)
        reverse = evaluate(self.raw, -30.0, -100.0, 300.0)
        self.assertAlmostEqual(forward["output_power_w"], reverse["output_power_w"])
        self.assertAlmostEqual(forward["output_torque_n_m"], -reverse["output_torque_n_m"])
        self.assertAlmostEqual(forward["output_speed_rad_s"], -reverse["output_speed_rad_s"])

    def test_saturation_and_envelope_fail_closed(self):
        saturated = evaluate(self.raw, 120.0, 100.0, 300.0)
        self.assertEqual(saturated["state"], "saturated")
        self.assertEqual(saturated["accepted_input_torque_n_m"], 80.0)
        with self.assertRaisesRegex(ActuationChainViolation, "speed"):
            evaluate(self.raw, 10.0, 400.0, 300.0)
        with self.assertRaisesRegex(ActuationChainViolation, "temperature"):
            evaluate(self.raw, 10.0, 100.0, 400.0)

    def test_removed_support_and_hardware_fail_closed(self):
        unsupported = copy.deepcopy(self.raw)
        unsupported["hardware"]["supports"] = []
        with self.assertRaisesRegex(ActuationChainViolation, "supports"):
            validate_protocol(unsupported)
        missing_member = copy.deepcopy(self.raw)
        missing_member["hardware"]["members"] = []
        with self.assertRaisesRegex(ActuationChainViolation, "hardware path"):
            validate_protocol(missing_member)


if __name__ == "__main__":
    unittest.main()
