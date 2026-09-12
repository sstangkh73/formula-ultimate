from __future__ import annotations
import copy,json
from pathlib import Path
import unittest
from formula_ultimate.subsystems.onboard_energy_realization import OnboardEnergyViolation,assembly,operate,validate_protocol
ROOT=Path(__file__).resolve().parents[1]; CONFIG=ROOT/"config/development/onboard_energy_realization_v1.json"
class OnboardEnergyRealizationTests(unittest.TestCase):
    def setUp(self): self.raw=json.loads(CONFIG.read_text(encoding="utf-8")); self.temp=self.raw["operating_cases"]["initial_temperature_k"]
    def test_protocol_and_geometry_derived_mass_energy(self):
        result=validate_protocol(self.raw); data=result["assembly"]; self.assertGreater(data["complete_mass_kg"],40); self.assertEqual(data["nominal_energy_j"],28_800_000); self.assertAlmostEqual(data["complete_mass_kg"],sum(data["component_masses"].values()))
    def test_nominal_energy_and_loss_ledger_closes(self):
        result=operate(self.raw,8000,600,self.temp); self.assertEqual(result["state"],"admitted"); self.assertLess(abs(result["energy_residual_j"]),1e-8); self.assertAlmostEqual(-result["stored_energy_change_j"],result["delivered_energy_j"]+result["total_loss_j"]); self.assertGreater(result["final_temperature_k"],self.temp)
    def test_empty_rate_limit_and_disconnection(self):
        empty=operate(self.raw,8000,60,self.temp,initial_fraction=0); limited=operate(self.raw,25000,60,self.temp); disconnected=operate(self.raw,8000,60,self.temp,connected=False)
        self.assertEqual(empty["state"],"empty"); self.assertEqual(empty["delivered_energy_j"],0); self.assertEqual(limited["state"],"rate_limited"); self.assertEqual(limited["delivered_power_w"],15000); self.assertEqual(disconnected["stored_energy_change_j"] if "stored_energy_change_j" in disconnected else disconnected["final_stored_energy_j"]-disconnected["initial_stored_energy_j"],0)
    def test_thermal_limit_is_explicit(self):
        result=operate(self.raw,15000,3600,329.0); self.assertEqual(result["state"],"thermal_limited"); self.assertAlmostEqual(result["final_temperature_k"],330.0)
    def test_hidden_replenishment_and_temperature_fail_closed(self):
        with self.assertRaisesRegex(OnboardEnergyViolation,"replenishment"): operate(self.raw,8000,60,self.temp,external_replenishment_w=1)
        with self.assertRaisesRegex(OnboardEnergyViolation,"temperature"): operate(self.raw,8000,60,350)
    def test_omitted_containment_and_bad_boundary_fail_closed(self):
        omitted=copy.deepcopy(self.raw); del omitted["hardware"]["containment"]
        with self.assertRaisesRegex(OnboardEnergyViolation,"containment"): validate_protocol(omitted)
        bad=copy.deepcopy(self.raw); bad["energy_boundary"]["external_replenishment"]="allowed"
        with self.assertRaisesRegex(OnboardEnergyViolation,"boundary"): validate_protocol(bad)
if __name__=="__main__": unittest.main()
