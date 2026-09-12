import copy,json,unittest
from pathlib import Path
from formula_ultimate.experiments.physical_connection_correlation import PhysicalConnectionCorrelationViolation,analyze_records,canonical_sha256,entry_gate,offline_stop,validate_protocol
ROOT=Path(__file__).resolve().parents[1]
class PhysicalConnectionCorrelationTests(unittest.TestCase):
    def setUp(self): self.raw=json.loads((ROOT/"config/development/physical_connection_correlation_v1.json").read_text(encoding="utf-8"))
    def test_protocol_and_entry_gate_stop(self):
        self.assertEqual(validate_protocol(self.raw)["status"],"passed"); gate=entry_gate(self.raw); self.assertFalse(gate["ready"]); self.assertFalse(gate["equipment_operation_authorized"])
    def test_offline_stop_logic_without_equipment(self):
        self.assertTrue(offline_stop({"load_n":1001,"temperature_k":300,"sensor_saturated":False},self.raw["registration"])["stop"])
        self.assertTrue(offline_stop({"load_n":1,"temperature_k":300,"sensor_saturated":True},self.raw["registration"])["stop"])
    def _ready_fixture(self):
        raw=copy.deepcopy(self.raw); raw["entry_permissions"]={k:("fixture-ref" if k.endswith("_ref") else True) for k in raw["entry_permissions"]}; raw["measurement_manifest"]={"specimens":[{"id":"cal"},{"id":"val"}],"instruments":[{"id":"g1","calibration_valid":True}],"environment_records":[{"id":"env"}]}; records=[{"specimen_id":"cal","instrument_id":"g1","partition":"calibration","sensor_saturated":False,"measured_displacement_m":0.001,"predicted_displacement_m":0.001},{"specimen_id":"val","instrument_id":"g1","partition":"validation","sensor_saturated":False,"measured_displacement_m":0.0011,"predicted_displacement_m":0.001}]; raw["raw_observations"]={"records":records,"sha256":canonical_sha256(records),"editing_allowed":False}; return raw,records
    def test_fixture_analysis_and_partition(self):
        raw,records=self._ready_fixture(); self.assertEqual(analyze_records(raw,records)["validation_count"],1)
    def test_missing_calibration_swapped_and_saturation_rejected(self):
        raw,records=self._ready_fixture(); raw["measurement_manifest"]["instruments"][0]["calibration_valid"]=False
        with self.assertRaisesRegex(PhysicalConnectionCorrelationViolation,"missing calibration"): analyze_records(raw,records)
        raw,records=self._ready_fixture(); records[1]["specimen_id"]="other"; raw["raw_observations"]["sha256"]=canonical_sha256(records)
        with self.assertRaisesRegex(PhysicalConnectionCorrelationViolation,"swapped specimen"): analyze_records(raw,records)
        raw,records=self._ready_fixture(); records[1]["sensor_saturated"]=True; raw["raw_observations"]["sha256"]=canonical_sha256(records)
        with self.assertRaisesRegex(PhysicalConnectionCorrelationViolation,"sensor saturation"): analyze_records(raw,records)
    def test_edited_raw_data_rejected(self):
        raw,records=self._ready_fixture(); changed=copy.deepcopy(records); changed[1]["measured_displacement_m"]+=1
        with self.assertRaisesRegex(PhysicalConnectionCorrelationViolation,"edited raw data"): analyze_records(raw,changed)
    def test_no_measured_claim_without_entry(self):
        with self.assertRaisesRegex(PhysicalConnectionCorrelationViolation,"entry gate incomplete"): analyze_records(self.raw,[])
if __name__=="__main__": unittest.main()
