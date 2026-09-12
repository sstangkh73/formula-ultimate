from __future__ import annotations
import copy,json
from pathlib import Path
import unittest
from formula_ultimate.physics.geometry_flow_heat_exchange import GeometryFlowViolation,external_flow,internal_passage,mesh_bounds,validate_protocol
ROOT=Path(__file__).resolve().parents[1]; CONFIG=ROOT/"config/development/geometry_flow_heat_exchange_v1.json"
class GeometryFlowHeatExchangeTests(unittest.TestCase):
    def setUp(self): self.raw=json.loads(CONFIG.read_text(encoding="utf-8"))
    def test_protocol_keeps_scopes_separate(self): self.assertEqual(len(validate_protocol(self.raw)["scopes"]),2); self.assertEqual(self.raw["coverage"]["whole_car_aerodynamics"],"unresolved")
    def test_mesh_bounds_create_projected_geometry(self): self.assertEqual(mesh_bounds([(0,0,0),(1,2,3)])["extents_m"],[1,2,3])
    def test_internal_reference_conserves_and_refines(self):
        coarse=internal_passage(self.raw,10); fine=internal_passage(self.raw,40); self.assertLess(abs(fine["heat_residual_w"]),1e-10); self.assertLess(fine["heat_capacity_relative_error"],coarse["heat_capacity_relative_error"]); self.assertLess(fine["reynolds"],2300)
    def test_blocked_zero_flow_and_zero_source(self):
        blocked=internal_passage(self.raw,20,blocked=True); zero=internal_passage(self.raw,20,volume_flow_m3_s=0); source=internal_passage(self.raw,20,source_heat_w=0); self.assertEqual(blocked["heat_rejected_w"],0); self.assertEqual(zero["pressure_drop_pa"],0); self.assertEqual(source["heat_rejected_w"],0)
    def test_passage_geometry_changes_pressure(self): self.assertGreater(internal_passage(self.raw,40,diameter_m=.006)["pressure_drop_pa"],internal_passage(self.raw,40,diameter_m=.01)["pressure_drop_pa"])
    def test_external_force_conserves_and_geometry_is_causal(self):
        base=external_flow(self.raw,.001,2); changed=external_flow(self.raw,.001,2,area_scale=1.3); zero=external_flow(self.raw,.001,2,speed_m_s=0); self.assertAlmostEqual(base["drag_force_n"],base["pressure_force_n"]+base["shear_force_n"]); self.assertGreater(changed["drag_force_n"],base["drag_force_n"]); self.assertEqual(zero["drag_force_n"],0)
    def test_regime_boundary_and_domain_fail_closed(self):
        fast=copy.deepcopy(self.raw); fast["internal"]["volume_flow_m3_s"]=.001
        with self.assertRaisesRegex(GeometryFlowViolation,"laminar"): internal_passage(fast,20)
        bad=copy.deepcopy(self.raw); del bad["boundaries"]["external"]["far_field"]
        with self.assertRaisesRegex(GeometryFlowViolation,"boundary"): validate_protocol(bad)
        with self.assertRaisesRegex(GeometryFlowViolation,"far-field"): external_flow(self.raw,.001,.1)
if __name__=="__main__": unittest.main()
