from __future__ import annotations
import copy,json,math
from pathlib import Path
import unittest
from formula_ultimate.structural.material_failure_scope import MaterialFailureViolation,applicability,combine_without_law,euler_buckling,validate_protocol,yield_margin
ROOT=Path(__file__).resolve().parents[1]; CONFIG=ROOT/"config/development/material_failure_scope_v1.json"
class MaterialFailureScopeTests(unittest.TestCase):
    def setUp(self): self.raw=json.loads(CONFIG.read_text(encoding="utf-8")); self.mat=self.raw["materials"]["synthetic_joint_aluminium"]
    def test_protocol_and_diagnostic_scope(self): self.assertEqual(validate_protocol(self.raw)["material_count"],2); self.assertEqual(applicability(self.mat,300,.001,"unspecified_fixture")["scope"],"diagnostic_reference_only")
    def test_safe_and_failed_yield_fixtures(self): self.assertEqual(yield_margin(self.mat,100e6)["state"],"safe_fixture"); self.assertEqual(yield_margin(self.mat,300e6)["state"],"failed_fixture")
    def test_euler_reference_and_imperfection_sensitivity(self):
        ref=self.raw["materials"]["analytic_column_reference"]; g=self.raw["buckling_fixture"]["geometry"]; expected=math.pi**2*ref["youngs_modulus_pa"]*(g["width_m"]*g["height_m"]**3/12)/g["length_m"]**2; a=euler_buckling(ref,g,expected*.5,0); b=euler_buckling(ref,g,expected*.5,.0005); self.assertAlmostEqual(a["euler_critical_load_n"],expected); self.assertLess(b["imperfection_adjusted_lower_capacity_n"],a["imperfection_adjusted_lower_capacity_n"])
    def test_range_process_relabel_and_mixture_fail_closed(self):
        cases=[(lambda:applicability(self.mat,450,.001,"unspecified_fixture"),"temperature"),(lambda:applicability(self.mat,300,1.,"unspecified_fixture"),"strain rate"),(lambda:applicability(self.mat,300,.001,"forged"),"process"),(lambda:applicability(self.mat,300,.001,"unspecified_fixture","measured_survival"),"relabeling"),(lambda:combine_without_law([self.mat,self.mat]),"mixture")]
        for action,phrase in cases:
            with self.subTest(phrase=phrase),self.assertRaisesRegex(MaterialFailureViolation,phrase): action()
    def test_missing_units_and_extension_promotion_fail(self):
        bad=copy.deepcopy(self.raw); del bad["materials"]["synthetic_joint_aluminium"]["units"]
        with self.assertRaisesRegex(MaterialFailureViolation,"provenance or units"): validate_protocol(bad)
        promoted=copy.deepcopy(self.raw); promoted["extension_slots"]["fatigue"]="implemented"
        with self.assertRaisesRegex(MaterialFailureViolation,"promoted"): validate_protocol(promoted)
if __name__=="__main__": unittest.main()
