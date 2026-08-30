from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
import unittest
from formula_ultimate.topology import VehicleAssemblyViolation,declaration_sha256,from_mapping,mass_properties,validate
ROOT=Path(__file__).resolve().parents[1]
def raw(): return json.loads((ROOT/"config/vehicle/topology_neutral_vehicle_v1.json").read_text(encoding="utf-8"))
class VehicleAssemblyTests(unittest.TestCase):
    def test_fixture_has_complete_paths_and_deterministic_mass_properties(self):
        value=raw(); assembly=from_mapping(value); result=validate(assembly)
        self.assertEqual("passed",result["status"]); self.assertEqual(4,len(assembly.components)); self.assertEqual(("contact_alpha",),result["contact_components"])
        self.assertAlmostEqual(30.657168026350796,mass_properties(assembly)["mass_kg"]); self.assertEqual(declaration_sha256(value),declaration_sha256(deepcopy(value)))
    def test_floating_unmatched_energy_and_ground_fail_closed(self):
        cases=[]
        value=raw(); value["connections"]=value["connections"][:-1]; cases.append((value,"floating"))
        value=raw(); value["connections"][0]["interface_a"]="missing"; cases.append((value,"unmatched"))
        value=raw(); value["energy_edges"]=[]; cases.append((value,"energy"))
        value=raw(); value["interfaces"][-1]["local_position_m"][2]=-0.04; cases.append((value,"ground"))
        for value,reason in cases:
            with self.subTest(reason=reason),self.assertRaisesRegex(VehicleAssemblyViolation,reason): validate(from_mapping(value))
    def test_keepout_envelope_overlap_invalid_solid_and_massless_fail_closed(self):
        value=raw(); value["keep_outs"][0]={"keep_out_id":"bad","minimum_m":[-0.3,-0.06,0.09],"maximum_m":[-0.2,0.06,0.21]}
        with self.assertRaisesRegex(VehicleAssemblyViolation,"keepout"): validate(from_mapping(value))
        value=raw(); value["envelope"]["maximum_m"][0]=0.1
        with self.assertRaisesRegex(VehicleAssemblyViolation,"envelope"): validate(from_mapping(value))
        value=raw(); value["components"][0]["primitive"]["size_m"][0]=0
        with self.assertRaisesRegex(VehicleAssemblyViolation,"primitive"): from_mapping(value)
        value=raw(); value["materials"]["dense"]["density_kg_per_m3"]=0
        with self.assertRaisesRegex(VehicleAssemblyViolation,"massless"): from_mapping(value)
if __name__=="__main__": unittest.main()
