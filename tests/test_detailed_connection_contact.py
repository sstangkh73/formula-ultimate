from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from formula_ultimate.structural.detailed_connection_contact import DetailedConnectionViolation, contact_patches, evaluate, reduced_prediction, validate_protocol

ROOT=Path(__file__).resolve().parents[1]; CONFIG=ROOT/"config/development/detailed_connection_contact_v1.json"


class DetailedConnectionContactTests(unittest.TestCase):
    def setUp(self):
        self.raw=json.loads(CONFIG.read_text(encoding="utf-8")); self.thread=self.raw["strategies"][0]; self.alt=self.raw["strategies"][1]; a=self.raw["acceptance"]; self.kw={"patch_count":24,"preload_n":a["baseline_preload_n"],"friction":a["baseline_friction"],"clearance_m":a["baseline_clearance_m"]}

    def solve(self,strategy=None,task=None,**kwargs):
        values={**self.kw,**kwargs}; return evaluate(strategy or self.thread,self.raw["material"],self.raw["contact"],task or self.raw["task"],**values)

    def test_protocol_pins_both_dependencies_and_three_levels(self):
        result=validate_protocol(self.raw); self.assertEqual(result["strategy_count"],2); self.assertEqual(result["refinement_count"],3)
        invalid=copy.deepcopy(self.raw); invalid["units"]="mm_N_MPa"
        with self.assertRaisesRegex(DetailedConnectionViolation,"units"): validate_protocol(invalid)

    def test_thread_patches_follow_helix_and_preserve_area(self):
        patches=contact_patches(self.thread,48); self.assertEqual(len(patches),48); self.assertGreater(patches[-1]["theta_rad"],2*3.14159); self.assertGreater(patches[-1]["z_m"],patches[0]["z_m"]); self.assertTrue(all(p["area_m2"]>0 for p in patches))

    def test_contact_inequality_balance_and_reduced_stick_response(self):
        result=self.solve(); self.assertEqual(result["status"],"stick"); self.assertGreaterEqual(result["minimum_normal_reaction_n"],0); self.assertLess(result["moment_residual_relative"],1e-12)
        reduced=reduced_prediction(result,self.raw["task"],self.kw["clearance_m"]); self.assertAlmostEqual(reduced["axial_displacement_m"],result["axial_displacement_m"],places=15); self.assertAlmostEqual(reduced["shear_displacement_m"],result["shear_displacement_m"],places=15)

    def test_friction_clearance_engagement_and_reverse_are_causal(self):
        base=self.solve(); high_clearance=self.solve(clearance_m=self.raw["contact"]["clearance_range_m"][1]); reduced=self.solve(engagement_fraction=.5); low_preload=self.solve(preload_n=2000.0)
        reverse=self.solve(task={**self.raw["task"],"shear_n":-self.raw["task"]["shear_n"]})
        self.assertGreater(high_clearance["axial_displacement_m"],base["axial_displacement_m"]); self.assertLess(reduced["normal_stiffness_n_m"],base["normal_stiffness_n_m"]); self.assertEqual(low_preload["status"],"slip"); self.assertAlmostEqual(reverse["shear_displacement_m"],-base["shear_displacement_m"])

    def test_removed_severed_and_open_joint_fail_closed(self):
        with self.assertRaisesRegex(DetailedConnectionViolation,"joint removed"): self.solve(joint_present=False)
        with self.assertRaisesRegex(DetailedConnectionViolation,"engagement"): self.solve(engagement_fraction=0)
        with self.assertRaisesRegex(DetailedConnectionViolation,"opened"): self.solve(task={**self.raw["task"],"axial_tension_n":5000.0})

    def test_alternative_is_not_forced_to_match_thread(self):
        thread=self.solve(); alternative=self.solve(self.alt); self.assertNotEqual(thread["contact_field_sha256"],alternative["contact_field_sha256"]); self.assertNotEqual(thread["normal_stiffness_n_m"],alternative["normal_stiffness_n_m"])


if __name__=="__main__": unittest.main()
