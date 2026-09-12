from __future__ import annotations
import copy,json
from pathlib import Path
import unittest
from formula_ultimate.subsystems.control_hardware_realization import ControlHardwareViolation,simulate,tune,validate_protocol
ROOT=Path(__file__).resolve().parents[1]; CONFIG=ROOT/"config/development/control_hardware_realization_v1.json"
class ControlHardwareRealizationTests(unittest.TestCase):
    def setUp(self): self.raw=json.loads(CONFIG.read_text(encoding="utf-8"))
    def test_protocol_and_hardware_mass(self): self.assertGreater(validate_protocol(self.raw)["hardware_mass_kg"],1); self.assertTrue(all(x["evidence"]=="synthetic_estimated" for x in self.raw["hardware"]["sensors"]))
    def test_matched_tuning_budget(self): self.assertEqual(tune(self.raw,"common")["evaluations"],tune(self.raw,"adapted")["evaluations"])
    def test_dropout_and_disconnection_remove_commands(self):
        dropout=simulate(self.raw,80,dropout_start_s=0); disconnected=simulate(self.raw,80,signal_connected=False); self.assertEqual(dropout["dropout_count"],200); self.assertTrue(all(x["command_n_m"]==0 for x in dropout["history"])); self.assertTrue(all(x["command_n_m"]==0 for x in disconnected["history"]))
    def test_exhausted_supply_and_saturation_are_observable(self): self.assertGreater(simulate(self.raw,100,supply_energy_j=0)["supply_exhausted_steps"],0); self.assertGreater(simulate(self.raw,1000)["saturation_count"],0)
    def test_increased_delay_changes_tracking(self): self.assertNotEqual(simulate(self.raw,80,delay_steps=2)["rmse"],simulate(self.raw,80,delay_steps=10)["rmse"])
    def test_noncausal_parameter_does_not_change_trace(self): self.assertEqual(simulate(self.raw,80,noncausal_label=0)["trace_sha256"],simulate(self.raw,80,noncausal_label=999)["trace_sha256"])
    def test_broken_signal_graph_fails_closed(self):
        bad=copy.deepcopy(self.raw); bad["signal_graph"]["edges"]=[]
        with self.assertRaisesRegex(ControlHardwareViolation,"signal path"): validate_protocol(bad)
if __name__=="__main__": unittest.main()
