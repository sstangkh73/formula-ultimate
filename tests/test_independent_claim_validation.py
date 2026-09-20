import copy
import json
import unittest
from pathlib import Path

from formula_ultimate.experiments.independent_claim_validation import IndependentClaimViolation, detect_known_omission, independent_analysis, validate_protocol
from tests.artifact_requirements import requires_artifacts

ROOT = Path(__file__).resolve().parents[1]


@requires_artifacts("artifacts/work128/run_a/telemetry.json")
class IndependentClaimValidationTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads((ROOT / "config/development/independent_claim_validation_v1.json").read_text(encoding="utf-8"))
        self.telemetry = json.loads((ROOT / self.raw["telemetry"]["path"]).read_text(encoding="utf-8"))

    def test_protocol_pins_claims_and_independence(self):
        self.assertEqual(validate_protocol(self.raw)["status"], "passed")
        self.assertFalse(self.raw["independence"]["institutionally_independent"])

    def test_independent_boundary_reduces_effect_and_downgrades_claim(self):
        result = independent_analysis(self.raw, self.telemetry)
        self.assertLess(result["independent_mean_s"], result["raw_mean_s"])
        self.assertEqual(result["discrepancy_class"], "explained_model_boundary")
        self.assertFalse(result["time_superiority_survives"])

    def test_energy_and_margins_are_recomputed(self):
        result = independent_analysis(self.raw, self.telemetry)
        self.assertLessEqual(max(result["energy_max_j"].values()), self.raw["registration"]["energy_cap_j"])
        self.assertGreaterEqual(min(result["thermal_min_k"].values()), 0)
        self.assertGreaterEqual(min(result["structural_min"].values()), 0)

    def test_shared_function_wrapper_is_rejected(self):
        shared = copy.deepcopy(self.raw)
        shared["independence"]["independent_source_module"] = shared["independence"]["upstream_source_module"]
        with self.assertRaisesRegex(IndependentClaimViolation, "shared-function wrapper"):
            validate_protocol(shared)

    def test_known_omission_is_detected(self):
        result = detect_known_omission(self.raw, self.telemetry)
        self.assertTrue(result["detected"])
        missed = copy.deepcopy(self.raw)
        missed["registration"]["open_boundary_penalty_s_per_severity"] = 0.0
        with self.assertRaisesRegex(IndependentClaimViolation, "known modeling omission"):
            detect_known_omission(missed, self.telemetry)

    def test_changed_or_incomplete_telemetry_fails(self):
        with self.assertRaisesRegex(IndependentClaimViolation, "record count"):
            independent_analysis(self.raw, self.telemetry[:-1])


if __name__ == "__main__":
    unittest.main()
