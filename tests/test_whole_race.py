from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import unittest

from formula_ultimate.physics.aerodynamics import (
    AerodynamicCoefficientMap,
    AerodynamicCoefficientSample,
    AerodynamicEvidence,
    AerodynamicReference,
    AerodynamicStateGrid,
)
from formula_ultimate.physics.circuit import load_circuit_catalog
from formula_ultimate.physics.lateral import PlanarContact,PlanarVehicle,PlanarVehicleParameters
from formula_ultimate.physics.suspension_braking import (
    BrakeParameters,RegenerationParameters,SuspensionBrakeModule,SuspensionParameters,
)
from formula_ultimate.physics.thermal import ThermalParameters
from formula_ultimate.physics.tyre import TyreContactParameters
from formula_ultimate.simulation import (
    AerodynamicMapAdapter,AerodynamicReferenceOrigin,CentralEnergyAuditAdapter,
    CentralEnergyConfiguration,CentralHealthConfiguration,CentralHealthEventAdapter,
    CircuitEnvironmentInputAdapter,CircuitInputScenario,ComponentHealthConfiguration,
    ComponentHealthState,ContactCouplingConfig,ContactCouplingSpec,ContactLimitCouplingAdapter,
    ContactRuntimeState,MotionConfiguration,MotionCorridorReference,NormalLoadCouplingAdapter,
    RaceProgressAdapter,RaceProgressConfiguration,SharedVehicleState,SpatialStepEvidence,
    StrategyStepCommand,TrafficStepEvidence,VehicleMotionCouplingAdapter,WeatherStepEvidence,
    WholeRaceConfiguration,WholeRaceError,load_coupling_architecture,run_whole_race,
)


ROOT=Path(__file__).resolve().parents[1]
ARCHITECTURE=load_coupling_architecture(ROOT/"config/simulation/coupled_level0_architecture_v4.json")
PROFILE=load_circuit_catalog(ROOT/"config/circuits/real_circuits_v1.json")[0]
TYRE=TyreContactParameters(2,2)


def vehicle():
    mass=1000.; load=mass*9.81/4
    contacts=(PlanarContact("fl",1,.8,load,0,20000,0,TYRE),PlanarContact("fr",1,-.8,load,0,20000,0,TYRE),PlanarContact("rl",-1,.8,load,0,20000,0,TYRE),PlanarContact("rr",-1,-.8,load,0,20000,0,TYRE))
    return PlanarVehicle("fixed-four",PlanarVehicleParameters(mass,1500,.4),contacts)


def aero_map():
    sample=AerodynamicCoefficientSample(0,0,0,0,0,0)
    return AerodynamicCoefficientMap("zero-aero",(10.,),(.05,),(0.,),(AerodynamicStateGrid("nominal",(sample,)),),AerodynamicEvidence("analytical-zero","synthetic_reference","Work 028 fixture"))


def brake_module(cid,preload):
    return SuspensionBrakeModule(cid,SuspensionParameters(100,10000,10,preload,.2,.2),
        BrakeParameters(.3,1,500,ThermalParameters(1000,0,0,500,600)),
        RegenerationParameters(500,10000,10000,1e6,.8,0))


@dataclass
class ReferenceFixture:
    target:float=30.0
    timeout:float=10.0
    budget:int=20
    primary:float=1e6
    auxiliary_w:float=0.0
    central_heat_w:float=0.0
    reliability_hazard:float=0.0
    corridor_width:float=100.0
    reverse_registration:bool=False
    omit_adapter:bool=False
    seed:int=17

    def __post_init__(self):
        self.planar=vehicle(); self.load=self.planar.parameters.mass_kg*9.81/4
        self.initial=SharedVehicleState(0,0,(0,0,0),(10,0,0),0,0,self.primary,0,0,
            tuple(ContactRuntimeState(c.contact_id,self.load,0,0,0,10/.3) for c in self.planar.contacts),
            (ComponentHealthState("store",300,0,0,False),))
        self.energy=CentralEnergyConfiguration(.9,self.auxiliary_w,1e6)

    def scenario(self,step,state):
        cid=PROFILE.circuit_id
        return CircuitInputScenario(PROFILE,state.race_distance_m,
            SpatialStepEvidence(cid,"available","analytical-fixture","straight",0,0,0,self.corridor_width,self.corridor_width,0),
            WeatherStepEvidence(cid,"observed","analytical-fixture",300,101325,.5,(0,0,0),"local_enu",0,300),
            TrafficStepEvidence(cid,"isolated_control","analytical-fixture",0))

    def strategy(self,step,state): return StrategyStepCommand(0,0,0,0)

    def adapters(self,step,state,duration):
        specs=tuple(ContactCouplingSpec(c.contact_id,c.x_position_m,c.y_position_m,0,0,.25,.25,TYRE,brake_module(c.contact_id,self.load)) for c in self.planar.contacts)
        component=ComponentHealthConfiguration("store",ThermalParameters(100,0,0,301,302),
            self.central_heat_w,1,1,0,0,1,0,0,1,self.reliability_hazard)
        values=(
            CircuitEnvironmentInputAdapter(),
            AerodynamicMapAdapter(aero_map(),AerodynamicReference(1,1,.1,1005,.5),AerodynamicReferenceOrigin((0,0,0)),.05,"nominal",state.components[0].temperature_k),
            NormalLoadCouplingAdapter(self.planar),
            ContactLimitCouplingAdapter(ContactCouplingConfig(specs,0,0,duration,300)),
            VehicleMotionCouplingAdapter(MotionConfiguration(1000,1500,duration,1.8),MotionCorridorReference(PROFILE.circuit_id,"straight",state.race_distance_m,(state.race_distance_m,0,0),0)),
            CentralEnergyAuditAdapter(self.energy),
            CentralHealthEventAdapter(CentralHealthConfiguration((component,),self.seed,step,300),self.energy),
            RaceProgressAdapter(RaceProgressConfiguration(self.target,10,self.timeout)),
        )
        if self.omit_adapter: values=values[:-1]
        return tuple(reversed(values)) if self.reverse_registration else values

    def config(self):
        return WholeRaceConfiguration(ARCHITECTURE,self.initial,1,self.target,self.timeout,self.budget,self.seed,self.scenario,self.strategy,self.adapters)


class WholeRaceTests(unittest.TestCase):
    def test_fixed_topology_reference_finishes_through_all_eight_stages(self):
        result=run_whole_race(ReferenceFixture().config())
        self.assertEqual("finished",result.outcome); self.assertEqual(30,result.final_state.race_distance_m)
        self.assertEqual(3,result.final_state.time_s); self.assertEqual(3,len(result.telemetry))
        self.assertTrue(all(len(x.traces)==8 for x in result.telemetry))
        self.assertTrue(all(x.transaction_status=="committed" for x in result.telemetry))
        self.assertEqual(0,result.finish_distance_residual_m)

    def test_same_seed_and_reversed_registration_replay_exactly(self):
        first=run_whole_race(ReferenceFixture().config())
        second=run_whole_race(ReferenceFixture().config())
        reversed_result=run_whole_race(ReferenceFixture(reverse_registration=True).config())
        self.assertEqual(first,second); self.assertEqual(first,reversed_result)
        self.assertEqual(first.replay_fingerprint_sha256,second.replay_fingerprint_sha256)

    def test_provenance_is_complete_per_step(self):
        result=run_whole_race(ReferenceFixture().config())
        self.assertEqual(ARCHITECTURE.fingerprint_sha256,result.replay.architecture_fingerprint_sha256)
        self.assertEqual(8,len(result.replay.model_versions)); self.assertEqual(3,len(result.replay.scenario_fingerprints))
        self.assertTrue(all(len(x.scenario_fingerprint_sha256)==64 and len(x.start_state_sha256)==64 and len(x.end_state_sha256)==64 for x in result.telemetry))
        self.assertTrue(all(x.published_signal_ids for x in result.telemetry))
        self.assertTrue(all(all(r.passed for r in x.residuals) for x in result.telemetry))

    def test_depletion_thermal_failure_timeout_and_budget_stop(self):
        depleted=run_whole_race(ReferenceFixture(target=100,primary=5,auxiliary_w=10).config())
        failed=run_whole_race(ReferenceFixture(target=100,central_heat_w=1000).config())
        timeout=run_whole_race(ReferenceFixture(target=100,timeout=1.5).config())
        budget=run_whole_race(ReferenceFixture(target=100,timeout=100,budget=2).config())
        self.assertEqual(("depleted",.5,0),(depleted.outcome,depleted.final_state.time_s,depleted.final_state.primary_energy_j))
        self.assertEqual(("failed",.2),(failed.outcome,failed.final_state.time_s))
        self.assertEqual(("timeout",1.5),(timeout.outcome,timeout.final_state.time_s))
        self.assertEqual("evaluation budget exhausted",budget.reason); self.assertEqual(2,budget.final_state.time_s)

    def test_invalid_corridor_and_missing_adapter_roll_back(self):
        corridor=run_whole_race(ReferenceFixture(corridor_width=.5).config())
        missing=run_whole_race(ReferenceFixture(omit_adapter=True).config())
        self.assertEqual("invalid",corridor.outcome); self.assertEqual(0,corridor.final_state.time_s)
        self.assertIsNone(corridor.telemetry[0].end_state_sha256)
        self.assertEqual("invalid",missing.outcome); self.assertIn("adapter_coverage",missing.reason)
        self.assertEqual(0,missing.final_state.race_distance_m)

    def test_exact_finish_depletion_tie_finishes_and_retains_both_events(self):
        result=run_whole_race(ReferenceFixture(primary=30,auxiliary_w=10).config())
        self.assertEqual("finished",result.outcome)
        final_events=result.telemetry[-1].events
        self.assertTrue(any(x.event_type=="energy_depletion" for x in final_events))
        self.assertTrue(any(x.event_type=="finished" for x in final_events))
        race_evidence=next(x for x in result.telemetry[-1].traces if x.module_id=="race_progress_solver")
        self.assertEqual("ok",race_evidence.status)

    def test_terminal_initial_state_and_invalid_configuration_are_rejected(self):
        fixture=ReferenceFixture()
        with self.assertRaises(WholeRaceError):
            WholeRaceConfiguration(ARCHITECTURE,replace(fixture.initial,status="finished"),1,30,10,10,1,fixture.scenario,fixture.strategy,fixture.adapters)
        with self.assertRaises(WholeRaceError): WholeRaceConfiguration(ARCHITECTURE,fixture.initial,0,30,10,10,1,fixture.scenario,fixture.strategy,fixture.adapters)


if __name__=="__main__": unittest.main()
