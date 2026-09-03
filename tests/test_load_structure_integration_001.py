from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
import unittest
from formula_ultimate.subsystems.load_structure_integration import LoadStructureIntegrationViolation,canonical_sha256,evaluate,validate_config
ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/"config/candidates/load_structure_integration_001.json"
def raw(): return json.loads(CONFIG.read_text(encoding="utf-8"))
def fixtures(packaging=True):
    c=raw(); body={"candidate_id":c["candidate_id"],"config_sha256":canonical_sha256(c),"hidden_geometry_repair":False,"part_count":17,"parts":[],"assembly":{"step_sha256":"a"*64,"solid_count":17},"pair_clearance":[],"maximum_overlap_m3":0.0 if packaging else 1e-5,"minimum_forbidden_clearance_m":0.001 if packaging else 0.0,"service_clearance_m":0.012,"routing_clearance_m":0.002,"integration_ground_clearance_m":0.0697,"total_mass_kg":3.0,"centre_of_mass_m":[0,0,0],"inertia_tensor_kg_m2":[[1,0,0],[0,1,0],[0,0,1]]}; m={**body,"manifest_sha256":canonical_sha256(body)}; fbody={"source_manifest_sha256":m["manifest_sha256"],"assembly_solid_count":17}; f={**fbody,"report_sha256":canonical_sha256(fbody)}; u={k:{"result_sha256":v["result_sha256"]} for k,v in c["sources"].items()}; return c,m,f,u
class IntegrationTests(unittest.TestCase):
    def test_config_valid(self): self.assertEqual(validate_config(raw())["status"],"passed")
    def test_unknown_field_fails(self):
        c=raw(); c["x"]=1
        with self.assertRaisesRegex(LoadStructureIntegrationViolation,"schema"): validate_config(c)
    def test_synthetic_evidence_cannot_be_relabelled(self):
        c=raw(); c["material"]["design_use_allowed"]=True
        with self.assertRaisesRegex(LoadStructureIntegrationViolation,"relabelled"): validate_config(c)
    def test_missing_control_fails(self):
        c=raw(); c["controls"].pop()
        with self.assertRaisesRegex(LoadStructureIntegrationViolation,"controls"): validate_config(c)
    def test_reference_fixture_reports_motion_and_evidence_blockers(self):
        c,m,f,u=fixtures(); result=evaluate(c,m,f,u); self.assertEqual(result["integration_status"],"partial"); self.assertFalse(result["motion_interface"]["passed"]); self.assertIn("synthetic_material_process_evidence",result["blockers"])
    def test_forbidden_overlap_is_a_visible_blocker(self):
        c,m,f,u=fixtures(False); result=evaluate(c,m,f,u); self.assertFalse(result["geometry"]["packaging_passed"]); self.assertIn("forbidden_work083_work084_geometry_interference",result["blockers"])
    def test_upstream_identity_change_fails_closed(self):
        c,m,f,u=fixtures(); u["work086_result"]["result_sha256"]="0"*64
        with self.assertRaisesRegex(LoadStructureIntegrationViolation,"identity"): evaluate(c,m,f,u)
    def test_freecad_wrong_solid_count_fails(self):
        c,m,f,u=fixtures(); f["assembly_solid_count"]=1; body={k:v for k,v in f.items() if k!="report_sha256"}; f["report_sha256"]=canonical_sha256(body)
        with self.assertRaisesRegex(LoadStructureIntegrationViolation,"FreeCAD"): evaluate(c,m,f,u)
    def test_blocked_service_path_fails(self):
        c,m,f,u=fixtures(); m["service_clearance_m"]=0; body={k:v for k,v in m.items() if k!="manifest_sha256"}; m["manifest_sha256"]=canonical_sha256(body); fbody={k:v for k,v in f.items() if k!="report_sha256"}; fbody["source_manifest_sha256"]=m["manifest_sha256"]; f={**fbody,"report_sha256":canonical_sha256(fbody)}
        with self.assertRaisesRegex(LoadStructureIntegrationViolation,"service"): evaluate(c,m,f,u)
    def test_thermal_heat_cannot_be_discarded(self):
        c,m,f,u=fixtures(); c["thermal_energy"]["air_rejected_heat_j"]=0; m["config_sha256"]=canonical_sha256(c); body={k:v for k,v in m.items() if k!="manifest_sha256"}; m["manifest_sha256"]=canonical_sha256(body); fbody={k:v for k,v in f.items() if k!="report_sha256"}; fbody["source_manifest_sha256"]=m["manifest_sha256"]; f={**fbody,"report_sha256":canonical_sha256(fbody)}
        with self.assertRaisesRegex(LoadStructureIntegrationViolation,"thermal"): evaluate(c,m,f,u)
if __name__=="__main__": unittest.main()
