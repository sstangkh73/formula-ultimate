from __future__ import annotations
import copy,json
from pathlib import Path
import unittest
from formula_ultimate.physics.coupled_thermal_solid import CoupledThermalSolidViolation,insulated_energy_rise,simulate,validate_protocol
ROOT=Path(__file__).resolve().parents[1]; CONFIG=ROOT/"config/development/coupled_thermal_solid_v1.json"
class CoupledThermalSolidTests(unittest.TestCase):
    def setUp(self): self.raw=json.loads(CONFIG.read_text(encoding="utf-8")); self.dt=self.raw["time_steps_s"][-1]
    def test_protocol_pins_dependencies_and_three_steps(self): self.assertEqual(validate_protocol(self.raw)["time_step_count"],3)
    def test_insulated_energy_rise_is_analytic(self): self.assertAlmostEqual(insulated_energy_rise(10,5,2,300),325)
    def test_zero_source_equilibrium_and_energy_balance(self):
        r=simulate(self.raw,self.dt,heat_input_w=0,boundary_conductance_w_k=0); self.assertEqual(r["male_final_temperature_k"],self.raw["thermal"]["initial_temperature_k"]); self.assertEqual(r["energy_residual_relative"],0)
    def test_temperature_changes_mechanics_and_returns_conductance(self):
        c=simulate(self.raw,self.dt,coupled=True); d=simulate(self.raw,self.dt,coupled=False); self.assertNotEqual(c["final_preload_n"],self.raw["mechanical"]["reference_preload_n"]); self.assertNotEqual(c["final_contact_conductance_w_k"],d["final_contact_conductance_w_k"]); self.assertNotEqual(c["male_final_temperature_k"],d["male_final_temperature_k"])
    def test_heat_path_and_area_mutations_are_causal(self):
        base=simulate(self.raw,self.dt); removed=simulate(self.raw,self.dt,contact_enabled=False); doubled=simulate(self.raw,self.dt,contact_area_scale=2); self.assertGreater(removed["male_final_temperature_k"],base["male_final_temperature_k"]); self.assertNotEqual(doubled["female_final_temperature_k"],base["female_final_temperature_k"])
    def test_free_and_constrained_expansion_and_range_failure(self):
        r=simulate(self.raw,self.dt); last=r["history"][-1]; self.assertGreater(last["male_free_expansion_m"],0); self.assertGreater(last["constrained_male_stress_pa"],0)
        bad=copy.deepcopy(self.raw); bad["thermal"]["heat_input_w"]=10000
        with self.assertRaisesRegex(CoupledThermalSolidViolation,"property range"): simulate(bad,.02)
if __name__=="__main__": unittest.main()
