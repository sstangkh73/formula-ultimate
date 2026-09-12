from __future__ import annotations
import copy,json
from pathlib import Path
import unittest
from formula_ultimate.simulation.coupled_vehicle_transient import CoupledTransientViolation,simulate,validate_protocol
ROOT=Path(__file__).resolve().parents[1]; CONFIG=ROOT/"config/development/coupled_vehicle_transient_v1.json"
class CoupledVehicleTransientTests(unittest.TestCase):
    def setUp(self): self.raw=json.loads(CONFIG.read_text(encoding="utf-8"))
    def test_protocol_pins_six_dependencies_and_owners(self): self.assertEqual(validate_protocol(self.raw)["dependency_count"],6)
    def test_coupled_run_conserves_and_blocks_promotion(self):
        result=simulate(self.raw,.01); self.assertEqual(result["status"],"completed_exploratory"); self.assertLess(abs(result["global_energy_residual_j"]),1e-7); self.assertFalse(result["promotion_allowed"]); self.assertTrue(result["unresolved_domains"])
    def test_event_timing_and_depletion_are_observable(self):
        result=simulate(self.raw,.01); self.assertIn(2.0,[x["time_s"] for x in result["events"]]); self.assertEqual(simulate(self.raw,.01,initial_energy_j=0)["status"],"energy_depleted")
    def test_double_count_and_decoupled_controls(self): self.assertEqual(simulate(self.raw,.01,double_count_power=True)["status"],"invalid_energy_accounting"); self.assertNotEqual(simulate(self.raw,.01)["history_sha256"],simulate(self.raw,.01,coupled=False)["history_sha256"])
    def test_mismatched_signs_fail_closed(self):
        bad=copy.deepcopy(self.raw); bad["exchange_schema"]["signs"]["traction_work_j"]="body_to_ground_positive"
        with self.assertRaisesRegex(CoupledTransientViolation,"frame or signs"): validate_protocol(bad)
    def test_out_of_range_reduced_model_fails(self):
        with self.assertRaisesRegex(CoupledTransientViolation,"validity"): simulate(self.raw,.01,initial_speed_m_s=31)
if __name__=="__main__": unittest.main()
