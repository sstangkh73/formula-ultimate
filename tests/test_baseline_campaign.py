from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest

from formula_ultimate.physics.circuit import load_circuit_catalog
from formula_ultimate.simulation import (
    BaselineCampaignError,
    load_baseline_campaign_protocol,
    load_coupling_architecture,
    run_baseline_campaign,
)


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "config/simulation/fixed_topology_baseline_protocol_v1.json"
ARCHITECTURE = load_coupling_architecture(
    ROOT / "config/simulation/coupled_level0_architecture_v4.json"
)
PROFILES = load_circuit_catalog(ROOT / "config/circuits/real_circuits_v1.json")


class BaselineCampaignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = load_baseline_campaign_protocol(PROTOCOL_PATH)
        cls.result = run_baseline_campaign(
            protocol=cls.protocol,
            architecture=ARCHITECTURE,
            profiles=PROFILES,
        )

    def test_protocol_pins_fair_opportunity_and_holdout(self):
        controls = self.protocol.controls
        self.assertEqual(1, controls.design_evaluation_budget)
        self.assertEqual((17, 29, 43), controls.random_seeds)
        self.assertEqual(7, len(controls.calibration_circuit_ids))
        self.assertEqual(3, len(controls.holdout_circuit_ids))
        self.assertFalse(self.protocol.real_circuit_admission)
        self.assertEqual(1, len(self.protocol.reference_families))
        family = self.protocol.reference_families[0]
        self.assertEqual(4, len(family.contacts))
        self.assertGreater(family.initial_primary_energy_j, 0)
        self.assertEqual(64, controls.evaluation_budget_per_run)

    def test_reference_family_finishes_all_ten_profiles_for_all_seeds(self):
        result = self.result
        self.assertTrue(result.all_runs_finished)
        self.assertEqual((30, 30), (result.completed_run_count, result.expected_run_count))
        self.assertEqual((10, 10), (result.completed_profile_count, result.total_profile_count))
        self.assertTrue(result.all_residuals_passed)
        self.assertTrue(result.all_runs_within_budget)
        self.assertTrue(result.partition_complete)
        self.assertFalse(result.real_circuit_admitted)
        self.assertTrue(all(run.finish_distance_residual_m == 0 for run in result.runs))
        self.assertTrue(all(run.attempted_steps <= 31 for run in result.runs))
        self.assertTrue(all(run.primary_energy_used_j > 0 for run in result.runs))
        self.assertTrue(all(not run.real_circuit_admitted for run in result.runs))

    def test_seed_identity_changes_replay_but_not_controlled_metrics(self):
        by_circuit = {}
        for run in self.result.runs:
            by_circuit.setdefault(run.circuit_id, []).append(run)
        for records in by_circuit.values():
            self.assertEqual(3, len(records))
            metrics = {
                (
                    item.outcome,
                    item.final_time_s,
                    item.final_distance_m,
                    item.primary_energy_used_j,
                    item.attempted_steps,
                )
                for item in records
            }
            self.assertEqual(1, len(metrics))
            self.assertEqual(3, len({item.race_replay_fingerprint_sha256 for item in records}))

    def test_partition_counts_and_static_width_evidence_remain_explicit(self):
        calibration = [run for run in self.result.runs if run.partition == "calibration"]
        holdout = [run for run in self.result.runs if run.partition == "holdout"]
        self.assertEqual((21, 9), (len(calibration), len(holdout)))
        self.assertEqual(
            {"screen_passed", "indeterminate"},
            {run.static_width_status for run in self.result.runs},
        )
        self.assertTrue(
            all(run.evidence_grade == "profile-distance-analytical-proxy" for run in self.result.runs)
        )

    def test_catalog_permutation_replays_on_reduced_campaign(self):
        selected = (PROFILES[0], PROFILES[-1])
        controls = replace(
            self.protocol.controls,
            random_seeds=(17,),
            calibration_circuit_ids=(selected[0].circuit_id,),
            holdout_circuit_ids=(selected[1].circuit_id,),
        )
        protocol = replace(self.protocol, controls=controls)
        first = run_baseline_campaign(
            protocol=protocol, architecture=ARCHITECTURE, profiles=selected
        )
        second = run_baseline_campaign(
            protocol=protocol,
            architecture=ARCHITECTURE,
            profiles=tuple(reversed(selected)),
        )
        self.assertEqual(first, second)

    def test_incomplete_or_overlapping_partitions_fail_closed(self):
        with self.assertRaisesRegex(BaselineCampaignError, "overlap"):
            replace(
                self.protocol.controls,
                holdout_circuit_ids=(self.protocol.controls.calibration_circuit_ids[0],),
            )
        controls = replace(
            self.protocol.controls,
            calibration_circuit_ids=(PROFILES[0].circuit_id,),
            holdout_circuit_ids=(PROFILES[1].circuit_id,),
        )
        with self.assertRaisesRegex(BaselineCampaignError, "partition/catalog mismatch"):
            run_baseline_campaign(
                protocol=replace(self.protocol, controls=controls),
                architecture=ARCHITECTURE,
                profiles=PROFILES,
            )

    def test_insufficient_common_budget_is_observable_not_silently_extended(self):
        selected = (PROFILES[0], PROFILES[-1])
        controls = replace(
            self.protocol.controls,
            random_seeds=(17,),
            evaluation_budget_per_run=1,
            calibration_circuit_ids=(selected[0].circuit_id,),
            holdout_circuit_ids=(selected[1].circuit_id,),
        )
        result = run_baseline_campaign(
            protocol=replace(self.protocol, controls=controls),
            architecture=ARCHITECTURE,
            profiles=selected,
        )
        self.assertFalse(result.all_runs_finished)
        self.assertTrue(all(run.outcome == "timeout" for run in result.runs))
        self.assertTrue(all(run.attempted_steps == 1 for run in result.runs))
        self.assertTrue(all("budget" in run.reason for run in result.runs))

    def test_proxy_protocol_cannot_claim_real_circuit_admission(self):
        with self.assertRaisesRegex(BaselineCampaignError, "real-circuit"):
            replace(self.protocol, real_circuit_admission=True)
        with self.assertRaisesRegex(BaselineCampaignError, "evidence grade"):
            replace(self.protocol, evidence_grade="measured-real-circuit")

    def test_loader_rejects_hidden_fields_and_implicit_integer_coercion(self):
        raw = json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "protocol.json"
            hidden = dict(raw)
            hidden["undeclared_advantage"] = True
            path.write_text(json.dumps(hidden), encoding="utf-8")
            with self.assertRaisesRegex(BaselineCampaignError, "unexpected"):
                load_baseline_campaign_protocol(path)
            mutated = json.loads(json.dumps(raw))
            mutated["controls"]["evaluation_budget_per_run"] = 64.0
            path.write_text(json.dumps(mutated), encoding="utf-8")
            with self.assertRaisesRegex(BaselineCampaignError, "positive integer"):
                load_baseline_campaign_protocol(path)

    def test_component_opportunity_mutation_changes_protocol_identity(self):
        family = self.protocol.reference_families[0]
        mutated = replace(family, initial_primary_energy_j=family.initial_primary_energy_j + 1)
        changed = replace(self.protocol, reference_families=(mutated,))
        self.assertNotEqual(self.protocol.fingerprint_sha256, changed.fingerprint_sha256)
        self.assertNotEqual(
            family.opportunity_fingerprint_sha256,
            mutated.opportunity_fingerprint_sha256,
        )


if __name__ == "__main__":
    unittest.main()
