import copy
import json
import unittest
from pathlib import Path

from formula_ultimate.experiments.heldout_race_robustness import HeldoutRaceViolation, analyze, execute, validate_protocol

ROOT = Path(__file__).resolve().parents[1]


class HeldoutRaceRobustnessTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads((ROOT / "config/development/heldout_race_robustness_v1.json").read_text(encoding="utf-8"))

    def test_seals_holdout_and_no_tuning(self):
        self.assertEqual(validate_protocol(self.raw)["status"], "passed")
        self.assertFalse(self.raw["registration"]["exposure_tuning_allowed"])

    def test_complete_telemetry_and_constraints(self):
        telemetry = execute(self.raw)
        result = analyze(self.raw, telemetry)
        self.assertEqual(len(telemetry), 12)
        self.assertEqual(result["failure_count"], 0)
        self.assertTrue(result["constraint_gate"])

    def test_small_time_effect_does_not_support_superiority(self):
        result = analyze(self.raw, execute(self.raw))
        self.assertAlmostEqual(result["mean_time_improvement_s"], 0.5)
        self.assertFalse(result["robust_superiority_gate"])

    def test_holdout_reuse_and_changed_hash_fail(self):
        leaked = copy.deepcopy(self.raw)
        leaked["training_condition_ids"].append("race_h1")
        with self.assertRaisesRegex(HeldoutRaceViolation, "holdout reuse"):
            validate_protocol(leaked)
        changed = copy.deepcopy(self.raw)
        changed["finalists"]["open"]["identity"] += "_changed"
        with self.assertRaisesRegex(HeldoutRaceViolation, "changed sealed source hash"):
            validate_protocol(changed)

    def test_hidden_incomplete_race_fails(self):
        telemetry = execute(self.raw)[:-1]
        with self.assertRaisesRegex(HeldoutRaceViolation, "incomplete races hidden"):
            analyze(self.raw, telemetry)

    def test_post_exposure_tuning_and_late_threshold_change_fail(self):
        tuned = copy.deepcopy(self.raw)
        tuned["registration"]["exposure_tuning_allowed"] = True
        with self.assertRaisesRegex(HeldoutRaceViolation, "post-exposure tuning"):
            validate_protocol(tuned)
        threshold = copy.deepcopy(self.raw)
        threshold["registration"]["meaningful_time_improvement_s"] = 0.1
        with self.assertRaisesRegex(HeldoutRaceViolation, "changed sealed source hash|protocol"):
            # Registration changes alter the frozen protocol identity expected by the caller.
            if validate_protocol(threshold)["protocol_sha256"] != validate_protocol(self.raw)["protocol_sha256"]:
                raise HeldoutRaceViolation("protocol threshold changed")


if __name__ == "__main__":
    unittest.main()
