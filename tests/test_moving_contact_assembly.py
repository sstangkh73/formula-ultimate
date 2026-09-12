from __future__ import annotations
import copy,json
from pathlib import Path
import unittest
from formula_ultimate.assembly.moving_contact_assembly import MovingAssemblyViolation,free_rigid_motion,simulate,validate_protocol

ROOT=Path(__file__).resolve().parents[1]; CONFIG=ROOT/"config/development/moving_contact_assembly_v1.json"
class MovingContactAssemblyTests(unittest.TestCase):
    def setUp(self): self.raw=json.loads(CONFIG.read_text(encoding="utf-8"))
    def test_protocol_registers_three_time_steps(self): self.assertEqual(validate_protocol(self.raw)["time_step_count"],3)
    def test_motion_has_computed_contact_history_and_clearance(self):
        r=simulate(self.raw["assembly"],self.raw["motion"],self.raw["time_steps_s"][-1]); self.assertTrue(r["events"]); self.assertGreater(r["transmitted_normal_impulse_n_s"],0); self.assertGreater(r["minimum_swept_clearance_m"],0); self.assertEqual(r["constraint_drift_m"],0)
    def test_free_rigid_motion_matches_analytic(self): self.assertLess(free_rigid_motion(.1,2.,.03,1e-4)["error_m"],1e-15)
    def test_incompatible_and_severed_fail_closed(self):
        with self.assertRaisesRegex(MovingAssemblyViolation,"incompatible"): simulate(self.raw["assembly"],self.raw["motion"],self.raw["time_steps_s"][0],allowed_motion="rigid")
        with self.assertRaisesRegex(MovingAssemblyViolation,"severed"): simulate(self.raw["assembly"],self.raw["motion"],self.raw["time_steps_s"][0],joint_present=False)
    def test_collision_blocks_only_mutated_assembly(self):
        bad={**self.raw["assembly"],"swept_clearance_m":1e-8}; self.assertEqual(simulate(bad,self.raw["motion"],self.raw["time_steps_s"][-1])["status"],"blocked_collision")
    def test_time_step_changes_history_identity(self):
        a=simulate(self.raw["assembly"],self.raw["motion"],self.raw["time_steps_s"][0]); b=simulate(self.raw["assembly"],self.raw["motion"],self.raw["time_steps_s"][-1]); self.assertNotEqual(a["history_sha256"],b["history_sha256"])
if __name__=="__main__": unittest.main()
