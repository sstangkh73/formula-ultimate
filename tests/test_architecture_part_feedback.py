from __future__ import annotations
import copy,json
from pathlib import Path
import unittest
from formula_ultimate.experiments.architecture_part_feedback import ArchitectureFeedbackViolation,generate_candidate,merge_region_mass,propose_task,run_loop,validate_protocol
ROOT=Path(__file__).resolve().parents[1]; CONFIG=ROOT/"config/development/architecture_part_feedback_v1.json"
class ArchitecturePartFeedbackTests(unittest.TestCase):
    def setUp(self): self.raw=json.loads(CONFIG.read_text(encoding="utf-8")); self.conditions={"assembly_load_n":19196.8,"assembly_heat_w":10.,"assembly_motion_m":7.1e-6,"unknowns":["measured_material"]}
    def test_protocol_and_equal_resource_loops(self):
        self.assertEqual(validate_protocol(self.raw)["iterations"],3); a=run_loop(self.raw,self.conditions,True); b=run_loop(self.raw,self.conditions,False); self.assertEqual(a["total_evaluations"],b["total_evaluations"])
    def test_feedback_changes_task_and_geometry_and_invalidates(self):
        r=run_loop(self.raw,self.conditions,True); self.assertNotEqual(r["records"][0]["task"],r["records"][1]["task"]); self.assertNotEqual(r["records"][0]["candidate"]["geometry_sha256"],r["records"][1]["candidate"]["geometry_sha256"]); self.assertEqual(len(r["invalidations"]),2); self.assertTrue(all(not x["complete_feasibility"] for x in r["records"]))
    def test_frozen_task_does_not_absorb_assembly_load(self):
        r=run_loop(self.raw,self.conditions,False); self.assertTrue(all(x["task"]["load_n"]==10000 for x in r["records"])); self.assertFalse(r["invalidations"])
    def test_multifunctional_merge_deduplicates_mass(self):
        regions=[{"cells":[(0,0,0),(1,0,0)],"density_kg_m3":1000.,"cell_volume_m3":1e-6},{"cells":[(1,0,0),(2,0,0)],"density_kg_m3":1000.,"cell_volume_m3":1e-6}]; self.assertAlmostEqual(merge_region_mass(regions),.003)
    def test_missing_coefficient_and_conflicting_overlap_fail(self):
        coeff=copy.deepcopy(self.raw["coefficients"]); del coeff["density_kg_m3"]
        with self.assertRaisesRegex(ArchitectureFeedbackViolation,"missing coefficient"): generate_candidate(self.raw["initial_internal_task"],coeff,7)
        regions=[{"cells":[(0,0,0)],"density_kg_m3":1000.,"cell_volume_m3":1e-6},{"cells":[(0,0,0)],"density_kg_m3":2000.,"cell_volume_m3":1e-6}]
        with self.assertRaisesRegex(ArchitectureFeedbackViolation,"incompatible material"): merge_region_mass(regions)
    def test_external_task_is_not_part_of_internal_proposal(self):
        before=copy.deepcopy(self.raw["external_task"]); propose_task(self.raw["initial_internal_task"],self.conditions,1); self.assertEqual(before,self.raw["external_task"])
if __name__=="__main__": unittest.main()
