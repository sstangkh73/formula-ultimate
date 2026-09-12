import copy,json,unittest
from pathlib import Path
from formula_ultimate.experiments.physical_vehicle_validation import PhysicalVehicleViolation,audit_telemetry,entry_gate,validate_protocol
ROOT=Path(__file__).resolve().parents[1]
class PhysicalVehicleValidationTests(unittest.TestCase):
    def setUp(self): self.raw=json.loads((ROOT/"config/development/physical_vehicle_validation_v1.json").read_text(encoding="utf-8")); self.fixture={"stage":"static_inspection","configuration_sha256":"cfg","failed":False,"incident_recorded":False,"energy_in_j":10.0,"energy_out_j":8.0,"loss_j":2.0,"claim_scope":"tested_stage_only"}
    def test_protocol_and_stopped_entry(self):
        self.assertEqual(validate_protocol(self.raw)["status"],"passed"); self.assertFalse(entry_gate(self.raw,{"work128":True,"work129":False,"work130":False,"work131":False,"work132":False})["ready"])
    def _fixture_raw(self): x=copy.deepcopy(self.raw);x["entry"]["configuration_sha256"]="cfg";return x
    def test_bounded_fixture_audit(self): self.assertFalse(audit_telemetry(self._fixture_raw(),[self.fixture])["safety_certification"])
    def test_unapproved_stage_and_changed_configuration_rejected(self):
        x=copy.deepcopy(self.fixture);x["stage"]="road_race"
        with self.assertRaisesRegex(PhysicalVehicleViolation,"unapproved stage"):audit_telemetry(self._fixture_raw(),[x])
        x=copy.deepcopy(self.fixture);x["configuration_sha256"]="other"
        with self.assertRaisesRegex(PhysicalVehicleViolation,"changed hardware"):audit_telemetry(self._fixture_raw(),[x])
    def test_hidden_failure_rejected(self):
        x=copy.deepcopy(self.fixture);x["failed"]=True
        with self.assertRaisesRegex(PhysicalVehicleViolation,"missing failure"):audit_telemetry(self._fixture_raw(),[x])
    def test_incomplete_energy_rejected(self):
        x=copy.deepcopy(self.fixture);x["loss_j"]=None
        with self.assertRaisesRegex(PhysicalVehicleViolation,"incomplete energy"):audit_telemetry(self._fixture_raw(),[x])
    def test_improper_extrapolation_rejected(self):
        x=copy.deepcopy(self.fixture);x["claim_scope"]="all_conditions"
        with self.assertRaisesRegex(PhysicalVehicleViolation,"improper extrapolation"):audit_telemetry(self._fixture_raw(),[x])
if __name__=="__main__":unittest.main()
