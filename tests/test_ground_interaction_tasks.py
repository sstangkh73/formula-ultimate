from __future__ import annotations

import copy
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.simulation.ground_interaction_tasks import (
    GroundInteractionViolation,
    analytic_stop,
    contact_force,
    net_wrench,
    simulate_stopping,
    validate_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/development/ground_interaction_tasks_v1.json"


class GroundInteractionTasksTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.mu = self.raw["surface"]["friction_coefficient"]

    def test_protocol_is_architecture_neutral_and_pins_dependencies(self):
        result = validate_protocol(self.raw)
        self.assertEqual(result["contact_count"], 3)
        self.assertEqual({item["work"] for item in self.raw["dependencies"]}, {114, 116})
        self.assertNotIn("wheel", json.dumps(self.raw["contacts"]).lower())

    def test_force_circle_saturates_without_exceeding_capacity(self):
        result = contact_force(1000.0, 800.0, 800.0, 0.5)
        self.assertTrue(result["saturated"])
        self.assertAlmostEqual(math.hypot(result["longitudinal_force_n"], result["lateral_force_n"]), 500.0)

    def test_zero_friction_lift_off_disconnection_and_no_interaction(self):
        cases = [
            contact_force(1000.0, 100.0, 0.0, 0.0),
            contact_force(0.0, 100.0, 0.0, self.mu),
            contact_force(1000.0, 100.0, 0.0, self.mu, actuation_connected=False),
            contact_force(1000.0, 100.0, 0.0, self.mu, interaction_enabled=False),
        ]
        for result in cases:
            with self.subTest(state=result["state"]):
                self.assertEqual(result["longitudinal_force_n"], 0.0)
                self.assertEqual(result["lateral_force_n"], 0.0)

    def test_stopping_matches_analytic_and_conserves_energy(self):
        body = self.raw["body"]
        normal = sum(port["normal_load_n"] for port in self.raw["contacts"])
        numeric = simulate_stopping(body["mass_kg"], body["initial_velocity_m_s"], normal, self.mu, 0.1, max_time_s=body["maximum_time_s"])
        expected = analytic_stop(body["mass_kg"], body["initial_velocity_m_s"], self.mu * normal)
        self.assertEqual(numeric["status"], "stopped")
        self.assertAlmostEqual(numeric["stopping_time_s"], expected["stopping_time_s"])
        self.assertAlmostEqual(numeric["stopping_distance_m"], expected["stopping_distance_m"])
        self.assertLess(numeric["energy_residual_relative"], 1e-12)

    def test_reverse_motion_has_opposite_force_and_distance(self):
        positive = simulate_stopping(300.0, 20.0, 3000.0, self.mu, 0.05, max_time_s=10.0)
        negative = simulate_stopping(300.0, -20.0, 3000.0, self.mu, 0.05, max_time_s=10.0)
        self.assertAlmostEqual(positive["stopping_distance_m"], -negative["stopping_distance_m"])
        self.assertAlmostEqual(positive["braking_force_n"], -negative["braking_force_n"])

    def test_contact_placement_changes_yaw_moment(self):
        request = self.raw["commands"]["direction"]
        placed = net_wrench(self.raw["contacts"], request, self.mu)
        centered = copy.deepcopy(self.raw["contacts"])
        centered[0]["x_m"] = 0.0
        centered_result = net_wrench(centered, request, self.mu)
        self.assertNotEqual(placed["yaw_moment_n_m"], centered_result["yaw_moment_n_m"])

    def test_unsupported_domain_and_bad_coefficient_fail_closed(self):
        unsupported = copy.deepcopy(self.raw)
        unsupported["surface"]["applicability"] = "soft_soil"
        with self.assertRaisesRegex(GroundInteractionViolation, "unsupported surface"):
            validate_protocol(unsupported)
        with self.assertRaisesRegex(GroundInteractionViolation, "non-negative"):
            contact_force(1000.0, 1.0, 0.0, -0.1)


if __name__ == "__main__":
    unittest.main()
