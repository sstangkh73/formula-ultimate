import copy,json,unittest
from pathlib import Path
from formula_ultimate.experiments.physical_subsystem_correlation import PhysicalSubsystemViolation,analyze_records,entry_gate,validate_protocol
ROOT=Path(__file__).resolve().parents[1]
class PhysicalSubsystemCorrelationTests(unittest.TestCase):
    def setUp(self): self.raw=json.loads((ROOT/"config/development/physical_subsystem_correlation_v1.json").read_text(encoding="utf-8")); self.records=[{"run_id":"c1","configuration_id":"cfg","partition":"calibration","boundary_power_in_w":100.0,"boundary_power_out_w":90.0,"aborted":False,"abort_reason":None,"sensor_a":1.0,"sensor_b":1.01,"cycles":10},{"run_id":"v1","configuration_id":"cfg","partition":"validation","boundary_power_in_w":100.0,"boundary_power_out_w":88.0,"aborted":False,"abort_reason":None,"sensor_a":1.0,"sensor_b":1.01,"cycles":100}]
    def test_protocol_and_stopped_entry(self): self.assertEqual(validate_protocol(self.raw)["status"],"passed"); self.assertFalse(entry_gate(self.raw,"stopped_missing_entry_permissions_and_data")["ready"])
    def test_fixture_analysis_is_bounded(self): self.assertFalse(analyze_records(self.raw,self.records)["lifetime_extrapolation_allowed"])
    def test_missing_boundary_power_rejected(self):
        x=copy.deepcopy(self.records); x[1]["boundary_power_in_w"]=None
        with self.assertRaisesRegex(PhysicalSubsystemViolation,"missing boundary power"): analyze_records(self.raw,x)
    def test_replacement_and_leakage_rejected(self):
        x=copy.deepcopy(self.records); x[1]["configuration_id"]="other"
        with self.assertRaisesRegex(PhysicalSubsystemViolation,"undocumented replacement"): analyze_records(self.raw,x)
        x=copy.deepcopy(self.records); x[1]["run_id"]="c1"
        with self.assertRaisesRegex(PhysicalSubsystemViolation,"calibration leakage"): analyze_records(self.raw,x)
    def test_censored_abort_rejected(self):
        x=copy.deepcopy(self.records); x[1]["aborted"]=True
        with self.assertRaisesRegex(PhysicalSubsystemViolation,"censored abort"): analyze_records(self.raw,x)
    def test_sensor_disagreement_rejected(self):
        x=copy.deepcopy(self.records); x[1]["sensor_b"]=2.0
        with self.assertRaisesRegex(PhysicalSubsystemViolation,"sensor disagreement"): analyze_records(self.raw,x)
if __name__=="__main__": unittest.main()
