import copy
import json
from pathlib import Path
import unittest

from formula_ultimate.experiments.main_campaign_protocol import (
    MainCampaignProtocolError,
    validate_main_campaign_protocol,
)


ROOT = Path(__file__).resolve().parents[1]


def protocol_fixture():
    return json.loads((ROOT / "config/experiments/bounded_whole_vehicle_main_campaign_v1.json").read_text(encoding="utf-8"))


def protocol_v2_fixture():
    return json.loads((ROOT / "config/experiments/bounded_whole_vehicle_main_campaign_v2.json").read_text(encoding="utf-8"))


def protocol_v3_fixture():
    return json.loads((ROOT / "config/experiments/bounded_whole_vehicle_main_campaign_v3.json").read_text(encoding="utf-8"))


class MainCampaignProtocolTests(unittest.TestCase):
    def test_v2_changes_identity_and_remediation_only(self):
        v1, v2 = protocol_fixture(), protocol_v2_fixture()
        for protocol in (v1, v2):
            validate_main_campaign_protocol(protocol)
        for name in ("protocol_id", "campaign_id", "frozen_source_commit"):
            v1.pop(name)
            v2.pop(name)
        remediation = v2.pop("supersedes")
        self.assertEqual(v1, v2)
        self.assertFalse(remediation["scientific_rules_changed"])
        self.assertFalse(remediation["v1_observations_reused"])

    def test_v2_remediation_scope_and_hashes_fail_closed(self):
        protocol = protocol_v2_fixture()
        protocol["supersedes"]["scientific_rules_changed"] = True
        with self.assertRaisesRegex(MainCampaignProtocolError, "scientific"):
            validate_main_campaign_protocol(protocol)
        protocol = protocol_v2_fixture()
        protocol["supersedes"]["v1_stage_ledger_sha256"] = "invalid"
        with self.assertRaisesRegex(MainCampaignProtocolError, "SHA-256"):
            validate_main_campaign_protocol(protocol)

    def test_v3_changes_identity_and_remediation_only(self):
        v1, v3 = protocol_fixture(), protocol_v3_fixture()
        validate_main_campaign_protocol(v3)
        for protocol in (v1, v3):
            for name in ("protocol_id", "campaign_id", "frozen_source_commit"):
                protocol.pop(name)
        remediation = v3.pop("supersedes")
        self.assertEqual(v1, v3)
        self.assertEqual("060", remediation["stopped_work"])
        self.assertFalse(remediation["scientific_rules_changed"])
        self.assertFalse(remediation["v2_observations_reused"])

    def test_v3_remediation_scope_fails_closed(self):
        protocol = protocol_v3_fixture()
        protocol["supersedes"]["reason"] = "change physics"
        with self.assertRaisesRegex(MainCampaignProtocolError, "remediation scope"):
            validate_main_campaign_protocol(protocol)

    def test_frozen_protocol_has_balanced_non_repeating_budget(self):
        protocol = protocol_fixture()
        summary = validate_main_campaign_protocol(protocol)
        self.assertEqual(12, len(summary.paired_seeds))
        self.assertEqual(80, summary.attempts_per_treatment_seed)
        self.assertEqual(960, summary.attempts_per_treatment)
        self.assertEqual(2880, summary.total_attempts)
        self.assertEqual(1024, summary.grid_capacity)
        self.assertEqual(960, summary.grid_unique_opportunities)
        self.assertEqual(72, summary.maximum_promotions)
        self.assertEqual("paired_seed", summary.inferential_unit)
        self.assertEqual(summary, validate_main_campaign_protocol(protocol))

    def test_duplicate_or_excluded_seed_fails_closed(self):
        protocol = protocol_fixture()
        protocol["design"]["paired_seeds"][-1] = protocol["design"]["paired_seeds"][0]
        with self.assertRaisesRegex(MainCampaignProtocolError, "unique"):
            validate_main_campaign_protocol(protocol)
        protocol = protocol_fixture()
        protocol["design"]["paired_seeds"][0] = 101
        with self.assertRaisesRegex(MainCampaignProtocolError, "overlap"):
            validate_main_campaign_protocol(protocol)

    def test_grid_overflow_or_repeat_fails_closed(self):
        protocol = protocol_fixture()
        protocol["design"]["grid"]["combination_capacity"] = 900
        with self.assertRaisesRegex(MainCampaignProtocolError, "capacity"):
            validate_main_campaign_protocol(protocol)
        protocol = protocol_fixture()
        protocol["design"]["grid"]["wrap_or_repeat_allowed"] = True
        with self.assertRaisesRegex(MainCampaignProtocolError, "prohibited"):
            validate_main_campaign_protocol(protocol)

    def test_budget_and_failure_exploits_fail_closed(self):
        protocol = protocol_fixture()
        protocol["design"]["total_attempted_evaluations"] -= 1
        with self.assertRaisesRegex(MainCampaignProtocolError, "arithmetic"):
            validate_main_campaign_protocol(protocol)
        protocol = protocol_fixture()
        protocol["design"]["failure_consumes_attempt"] = False
        with self.assertRaisesRegex(MainCampaignProtocolError, "failure_consumes_attempt"):
            validate_main_campaign_protocol(protocol)
        protocol = protocol_fixture()
        protocol["failure_policy"]["failed_attempt_retry_allowed"] = True
        with self.assertRaisesRegex(MainCampaignProtocolError, "must be false"):
            validate_main_campaign_protocol(protocol)

    def test_holdout_leakage_and_mutable_refinement_fail_closed(self):
        protocol = protocol_fixture()
        protocol["promotion"]["holdout_is_never_used_for_training_or_parent_selection"] = False
        with self.assertRaisesRegex(MainCampaignProtocolError, "leakage"):
            validate_main_campaign_protocol(protocol)
        protocol = protocol_fixture()
        protocol["promotion"]["refined_evaluator"]["thresholds_mutable_during_campaign"] = True
        with self.assertRaisesRegex(MainCampaignProtocolError, "immutable"):
            validate_main_campaign_protocol(protocol)

    def test_attempt_level_pseudoreplication_fails_closed(self):
        protocol = protocol_fixture()
        protocol["outcomes"]["inferential_unit"] = "attempt"
        with self.assertRaisesRegex(MainCampaignProtocolError, "paired_seed"):
            validate_main_campaign_protocol(protocol)
        protocol = protocol_fixture()
        protocol["outcomes"]["attempts_are_independent_replicates"] = True
        with self.assertRaisesRegex(MainCampaignProtocolError, "pseudo-replication"):
            validate_main_campaign_protocol(protocol)

    def test_physical_claim_or_missing_replication_rule_fails_closed(self):
        protocol = protocol_fixture()
        protocol["claim_level"] = "physical validation"
        with self.assertRaisesRegex(MainCampaignProtocolError, "claim boundary"):
            validate_main_campaign_protocol(protocol)
        protocol = protocol_fixture()
        protocol["analysis"]["algorithm_superiority_requires_both"] = ["positive_primary_supported_finisher_rate_effect"]
        with self.assertRaisesRegex(MainCampaignProtocolError, "replication"):
            validate_main_campaign_protocol(protocol)
        protocol = protocol_fixture()
        protocol["prohibited_claims"].remove("engineering_discovery")
        with self.assertRaisesRegex(MainCampaignProtocolError, "claim set"):
            validate_main_campaign_protocol(protocol)


if __name__ == "__main__":
    unittest.main()
