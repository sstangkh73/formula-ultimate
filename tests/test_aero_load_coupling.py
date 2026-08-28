from __future__ import annotations

import math
import unittest

from formula_ultimate.physics.aerodynamics import (
    AerodynamicCoefficientMap, AerodynamicCoefficientSample, AerodynamicEvidence,
    AerodynamicReference, AerodynamicStateGrid,
)
from formula_ultimate.physics.lateral import PlanarContact, PlanarVehicle, PlanarVehicleParameters
from formula_ultimate.physics.tyre import TyreContactParameters
from formula_ultimate.simulation import (
    AdapterReadView, AerodynamicChassisWrench, AerodynamicMapAdapter,
    AerodynamicReferenceOrigin, ComponentHealthState, ContactRuntimeState,
    EnvironmentStepInputs, NormalLoadCouplingAdapter, RuntimeSignal,
    SharedVehicleState, TrafficStepEvidence, WeatherStepEvidence,
    AeroLoadCouplingError, couple_wrench_to_normal_loads, moist_air_density_kg_per_m3,
)

TYRE = TyreContactParameters(1.2, 1.1)

def aero_map(speed=30.0):
    return AerodynamicCoefficientMap("fixture", (speed,), (.05,), (0.0,),
        (AerodynamicStateGrid("nominal", (AerodynamicCoefficientSample(.5,0,1,0,0,.2),)),),
        AerodynamicEvidence("fixture", "synthetic_reference", "analytical"))

REFERENCE = AerodynamicReference(2.0, 3.0, .1, 1005.0, .5)

def contact(cid,x,y,load): return PlanarContact(cid,x,y,load,0,20000,0,TYRE)

def vehicle4():
    mass=1000.; load=mass*9.81/4
    return PlanarVehicle("four", PlanarVehicleParameters(mass,1500,.4), (
        contact("fl",1,.8,load), contact("fr",1,-.8,load),
        contact("rl",-1,.8,load), contact("rr",-1,-.8,load)))

def shared(vehicle, velocity=(30.,0.,0.), yaw=0.):
    return SharedVehicleState(0,0,(0,0,0),velocity,yaw,0,1e6,0,0,
        tuple(ContactRuntimeState(c.contact_id,c.baseline_normal_load_n,0,0,0,0) for c in vehicle.contacts),
        (ComponentHealthState("store",320,0,0,False),))

def environment(cid="fixture"):
    weather=WeatherStepEvidence(cid,"observed","fixture",300,101325,.5,(0,0,0),"local_enu",0,310)
    traffic=TrafficStepEvidence(cid,"isolated_control","fixture",0)
    return EnvironmentStepInputs(weather,traffic)

class AeroLoadCouplingTests(unittest.TestCase):
    def test_moist_air_density_is_finite_and_humidity_reduces_density(self):
        dry=moist_air_density_kg_per_m3(300,101325,0)
        humid=moist_air_density_kg_per_m3(300,101325,1)
        self.assertGreater(dry,humid); self.assertGreater(humid,0)

    def test_aero_adapter_signs_cooling_and_replay(self):
        adapter=AerodynamicMapAdapter(aero_map(),REFERENCE,AerodynamicReferenceOrigin((0,0,0)),.05,"nominal",350)
        current=shared(vehicle4())
        view=AdapterReadView("aerodynamic_map",current,(RuntimeSignal("environment.step_inputs",environment()),RuntimeSignal("state.current",current)))
        first=adapter.execute(view); second=adapter.execute(view)
        self.assertEqual(first,second); self.assertEqual("ok",first.status)
        values={s.signal_id:s.value for s in first.signals}; wrench=values["aero.force_moment"]
        self.assertLess(wrench.force_body_n[0],0); self.assertLess(wrench.force_body_n[2],0)
        self.assertGreater(values["aero.cooling_evidence"].heat_rejection_w,0)

    def test_local_enu_wind_is_rotated_to_body_axes(self):
        adapter=AerodynamicMapAdapter(aero_map(),REFERENCE,AerodynamicReferenceOrigin((0,0,0)),.05,"nominal",350)
        current=shared(vehicle4(),velocity=(0,30,0),yaw=math.pi/2)
        view=AdapterReadView("aerodynamic_map",current,(RuntimeSignal("environment.step_inputs",environment()),RuntimeSignal("state.current",current)))
        output=adapter.execute(view)
        self.assertEqual("ok",output.status)
        wrench=next(signal.value for signal in output.signals if signal.signal_id == "aero.force_moment")
        self.assertIn("yaw_angle",wrench.query_evidence.numerically_snapped_axes)
        self.assertNotEqual(wrench.query_evidence.raw_yaw_angle_rad,0.0)
        self.assertEqual(wrench.query_evidence.queried_yaw_angle_rad,0.0)

    def test_unsupported_map_query_is_invalid_with_zero_writes(self):
        adapter=AerodynamicMapAdapter(aero_map(),REFERENCE,AerodynamicReferenceOrigin((0,0,0)),.05,"nominal",350)
        current=shared(vehicle4(),velocity=(40,0,0))
        view=AdapterReadView("aerodynamic_map",current,(RuntimeSignal("environment.step_inputs",environment()),RuntimeSignal("state.current",current)))
        output=adapter.execute(view); self.assertEqual("invalid",output.status); self.assertEqual((),output.signals)

    def test_symmetric_downforce_increases_all_four_loads_and_closes(self):
        vehicle=vehicle4(); wrench=AerodynamicChassisWrench((-100,0,-4000),(0,0,0),"m","e")
        result=couple_wrench_to_normal_loads(vehicle=vehicle,wrench=wrench)
        self.assertEqual("ok",result.status)
        for item,base in zip(result.contact_loads,vehicle.contacts): self.assertAlmostEqual(base.baseline_normal_load_n+1000,item.normal_load_n)
        self.assertTrue(all(entry.passed for entry in result.residuals.entries()))

    def test_forward_downforce_origin_shifts_load_forward(self):
        vehicle=vehicle4(); down=4000.
        wrench=AerodynamicChassisWrench((0,0,-down),(0,down,0),"m","e")
        result=couple_wrench_to_normal_loads(vehicle=vehicle,wrench=wrench)
        front=sum(x.normal_load_n for x in result.contact_loads[:2]); rear=sum(x.normal_load_n for x in result.contact_loads[2:])
        self.assertGreater(front,rear); self.assertAlmostEqual(vehicle.parameters.mass_kg*9.81+down,front+rear)

    def test_three_contact_topology_is_supported(self):
        mass=900.; weight=mass*9.81
        vehicle=PlanarVehicle("three",PlanarVehicleParameters(mass,1000,.3),(
            contact("f",1,0,.4*weight),contact("l",-2/3,.7,.3*weight),contact("r",-2/3,-.7,.3*weight)))
        result=couple_wrench_to_normal_loads(vehicle=vehicle,wrench=AerodynamicChassisWrench((0,0,-900),(0,0,0),"m","e"))
        self.assertEqual("ok",result.status); self.assertEqual(3,len(result.contact_loads))

    def test_rank_deficiency_and_contact_lift_are_observable(self):
        mass=1000.; load=mass*9.81/2
        collinear=PlanarVehicle("line",PlanarVehicleParameters(mass,1000,.4),(contact("f",1,0,load),contact("r",-1,0,load)))
        rank=couple_wrench_to_normal_loads(vehicle=collinear,wrench=AerodynamicChassisWrench((0,0,0),(0,0,0),"m","e"))
        self.assertEqual("invalid",rank.status); self.assertIn("rank-deficient",rank.reason)
        lift=couple_wrench_to_normal_loads(vehicle=vehicle4(),wrench=AerodynamicChassisWrench((0,0,0),(0,100000,0),"m","e"))
        self.assertEqual("invalid",lift.status); self.assertIn("contact lift",lift.reason)

    def test_normal_load_adapter_matches_contacts_and_emits_exact_outputs(self):
        vehicle=vehicle4(); current=shared(vehicle)
        view=AdapterReadView("normal_load_solver",current,(RuntimeSignal("aero.force_moment",AerodynamicChassisWrench((0,0,-1000),(0,0,0),"m","e")),RuntimeSignal("state.current",current)))
        output=NormalLoadCouplingAdapter(vehicle).execute(view)
        self.assertEqual("ok",output.status); self.assertEqual({"chassis.balance_residuals","chassis.normal_loads"},{s.signal_id for s in output.signals})
        wrong=shared(vehicle); wrong=SharedVehicleState(wrong.time_s,wrong.race_distance_m,wrong.position_m,wrong.velocity_mps,wrong.yaw_rad,wrong.yaw_rate_rad_per_s,wrong.primary_energy_j,wrong.recovered_energy_j,wrong.completed_laps,(ContactRuntimeState("other",1,0,0,0,0),),wrong.components)
        badview=AdapterReadView("normal_load_solver",wrong,(RuntimeSignal("aero.force_moment",AerodynamicChassisWrench((0,0,0),(0,0,0),"m","e")),RuntimeSignal("state.current",wrong)))
        self.assertEqual("invalid",NormalLoadCouplingAdapter(vehicle).execute(badview).status)

    def test_invalid_wrench_declarations_are_rejected(self):
        with self.assertRaises(AeroLoadCouplingError):
            AerodynamicChassisWrench((math.nan,0,0),(0,0,0),"m","e")
        with self.assertRaises(AeroLoadCouplingError):
            AerodynamicChassisWrench((0,0,0),(0,0),"m","e")

if __name__ == "__main__": unittest.main()
