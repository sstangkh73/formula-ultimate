from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from formula_ultimate.experiments.whole_mechanical_vehicle_candidate import (
    WholeMechanicalVehicleAuditError, build_bundle, evaluate, load_evidence,
    validate_config,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/candidates/whole_mechanical_vehicle_candidate_001.json"


def raw() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


class WholeMechanicalVehicleCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = raw()
        cls.evidence = load_evidence(ROOT, cls.config)

    def test_config_valid(self):
        self.assertEqual(validate_config(self.config)["status"], "passed")

    def test_audit_is_valid_but_candidate_is_not_ready(self):
        result = evaluate(self.config, self.evidence)
        self.assertEqual(result["audit_status"], "passed")
        self.assertEqual(result["candidate_verdict"], "not_ready")
        self.assertFalse(result["level0_admitted"])
        self.assertFalse(result["level0_simulation"]["attempted"])

    def test_all_required_cases_are_blocked_and_visible(self):
        result = evaluate(self.config, self.evidence)
        self.assertEqual(len(result["admission_cases"]), 11)
        self.assertTrue(all(not case["ready"] and case["blockers"] for case in result["admission_cases"]))

    def test_source_identity_change_fails_closed(self):
        evidence = deepcopy(self.evidence)
        evidence["source_results"]["work087"]["result_sha256"] = "0" * 64
        with self.assertRaisesRegex(WholeMechanicalVehicleAuditError, "source identity"):
            evaluate(self.config, evidence)

    def test_missing_geometry_artifact_fails_closed(self):
        evidence = deepcopy(self.evidence)
        evidence["part_step_sha256"].pop("axle")
        with self.assertRaisesRegex(WholeMechanicalVehicleAuditError, "artifact coverage"):
            evaluate(self.config, evidence)

    def test_blocker_suppression_fails_closed(self):
        evidence = deepcopy(self.evidence)
        evidence["evaluation"]["blockers"].pop()
        with self.assertRaisesRegex(WholeMechanicalVehicleAuditError, "blocker suppression"):
            evaluate(self.config, evidence)

    def test_forced_level0_policy_is_rejected(self):
        config = deepcopy(self.config)
        config["evidence_policy"]["run_level0_when_blocked"] = True
        with self.assertRaisesRegex(WholeMechanicalVehicleAuditError, "cannot be relaxed"):
            validate_config(config)

    def test_synthetic_evidence_relabelling_fails(self):
        evidence = deepcopy(self.evidence)
        evidence["evaluation"]["design_use_allowed"] = True
        with self.assertRaisesRegex(WholeMechanicalVehicleAuditError, "relabelled"):
            evaluate(self.config, evidence)

    def test_case_omission_fails(self):
        config = deepcopy(self.config)
        config["required_case_ids"].pop()
        with self.assertRaisesRegex(WholeMechanicalVehicleAuditError, "admission cases"):
            validate_config(config)

    def test_unknown_field_fails(self):
        config = deepcopy(self.config)
        config["unknown"] = 1
        with self.assertRaisesRegex(WholeMechanicalVehicleAuditError, "schema"):
            validate_config(config)

    def test_bundle_is_deterministic(self):
        self.assertEqual(build_bundle(self.config, self.evidence), build_bundle(self.config, self.evidence))

    def test_bundle_contains_every_generated_report_class(self):
        bundle = build_bundle(self.config, self.evidence)
        expected_files = {
            "admission_report.json", "assembly_tree.json", "joint_dof_manifest.json",
            "material_manifest.json", "mass_com_inertia_report.json",
            "interference_report.json", "structural_load_case_report.json",
            "torque_power_energy_ledger.json", "failure_propagation_report.json",
            "deterministic_replay_manifest.json", "level0_simulation_decision.json",
            "geometry_artifact_index.json",
        }
        self.assertEqual(set(bundle), expected_files)


if __name__ == "__main__":
    unittest.main()
