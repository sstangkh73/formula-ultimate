from __future__ import annotations
from dataclasses import replace
import unittest

from formula_ultimate.physics.suspension_braking import (BrakeParameters,
    RegenerationParameters,SuspensionBrakeModule,SuspensionBrakeState,SuspensionParameters)
from formula_ultimate.physics.thermal import ThermalParameters
from formula_ultimate.physics.tyre import TyreContactParameters
from formula_ultimate.simulation import (AdapterReadView,ComponentHealthState,
    ContactCouplingConfig,ContactCouplingError,ContactCouplingSpec,
    ContactLimitCouplingAdapter,ContactNormalLoad,ContactRuntimeState,
    ContactSubsystemSnapshot,RuntimeSignal,SharedVehicleState,StrategyStepCommand,
    couple_contacts)

def module(cid,preload=1000):
    return SuspensionBrakeModule(cid,SuspensionParameters(100,10000,10,preload,.2,.2),
        BrakeParameters(.3,1,500,ThermalParameters(1000,10,0,500,600)),
        RegenerationParameters(500,10000,10000,1e6,.8,1))
def spec(cid,x,y,drive=.25,brake=.25,preload=1000,mu=1):
    return ContactCouplingSpec(cid,x,y,.1,2000,drive,brake,TyreContactParameters(mu,mu),module(cid,preload))
def config(specs,total_drive=2000,total_brake=800,duration=.01):
    return ContactCouplingConfig(tuple(specs),total_drive,total_brake,duration,300)
def shared(specs,loads=None,omega=20):
    loads=loads or [1000]*len(specs)
    return SharedVehicleState(0,0,(0,0,0),(20,0,0),0,0,1e6,0,0,
        tuple(ContactRuntimeState(s.contact_id,n,0,0,0,omega) for s,n in zip(specs,loads)),
        (ComponentHealthState("store",300,0,0,False),))
def snapshots(specs): return tuple(ContactSubsystemSnapshot(s.contact_id,SuspensionBrakeState(0,0,0,300,0)) for s in specs)
def loads(specs,values=None): return tuple(ContactNormalLoad(s.contact_id,n) for s,n in zip(specs,values or [1000]*len(specs)))
def four(): return (spec("fl",1,.8),spec("fr",1,-.8),spec("rl",-1,.8),spec("rr",-1,-.8))

class ContactCouplingTests(unittest.TestCase):
    def test_drive_allocation_closes_and_replays(self):
        specs=four(); args=dict(config=config(specs),normal_loads=loads(specs),command=StrategyStepCommand(1,0,0,0),shared_state=shared(specs),subsystem_states=snapshots(specs))
        first=couple_contacts(**args); second=couple_contacts(**args)
        self.assertEqual(first,second); force=first[0]
        self.assertAlmostEqual(2000,force.total_body_longitudinal_force_n)
        self.assertTrue(all(x.requested_local_longitudinal_force_n==500 for x in force.contacts))

    def test_zero_recovery_uses_mechanical_heat(self):
        specs=four(); _,energy,_,_=couple_contacts(config=config(specs),normal_loads=loads(specs),command=StrategyStepCommand(0,1,0,0),shared_state=shared(specs),subsystem_states=snapshots(specs))
        self.assertEqual(0,energy.total_recovered_storage_energy_j)
        self.assertGreater(energy.total_mechanical_brake_heat_j,0)

    def test_central_recovery_request_produces_recovered_energy(self):
        specs=four(); _,energy,_,residuals=couple_contacts(config=config(specs),normal_loads=loads(specs),command=StrategyStepCommand(0,1,0,1),shared_state=shared(specs),subsystem_states=snapshots(specs))
        self.assertGreater(energy.total_recovered_storage_energy_j,0)
        self.assertTrue(all(x.passed for x in residuals))

    def test_combined_brake_projection_recomputes_energy_at_applied_force(self):
        specs=four(); duration=.01; omega=20
        force,energy,_,_=couple_contacts(config=config(specs,total_brake=4000,duration=duration),normal_loads=loads(specs),command=StrategyStepCommand(0,1,1,1),shared_state=shared(specs,omega=omega),subsystem_states=snapshots(specs))
        self.assertTrue(all(item.tyre_result.saturated for item in force.contacts))
        for item,transfer,s in zip(force.contacts,energy.contacts,specs):
            transmitted_torque=abs(item.tyre_result.applied_longitudinal_force_n)*s.subsystem.brake.effective_radius_m
            self.assertAlmostEqual(transmitted_torque*omega*duration,transfer.wheel_energy_removed_j)
            self.assertGreater(transfer.unserved_brake_torque_n_m,0)

    def test_combined_tyre_saturation_is_per_contact(self):
        specs=four(); force,_,_,_=couple_contacts(config=config(specs,total_drive=8000),normal_loads=loads(specs),command=StrategyStepCommand(1,0,1,0),shared_state=shared(specs),subsystem_states=snapshots(specs))
        self.assertTrue(all(x.tyre_result.saturated for x in force.contacts))
        self.assertTrue(all(x.unserved_local_longitudinal_force_n>0 for x in force.contacts))

    def test_unserved_force_is_not_redistributed(self):
        specs=four(); values=[100,1300,1300,1300]
        force,_,_,_=couple_contacts(config=config(specs,total_drive=4000),normal_loads=loads(specs,values),command=StrategyStepCommand(1,0,0,0),shared_state=shared(specs,values),subsystem_states=snapshots(specs))
        self.assertAlmostEqual(3100,force.total_body_longitudinal_force_n)
        self.assertAlmostEqual(900,force.contacts[0].unserved_local_longitudinal_force_n)
        self.assertTrue(all(x.requested_local_longitudinal_force_n==1000 for x in force.contacts))

    def test_arbitrary_three_contact_topology(self):
        specs=(spec("f",1,0,1/3,1/3),spec("l",-.5,.7,1/3,1/3),spec("r",-.5,-.7,1/3,1/3))
        force,energy,health,_=couple_contacts(config=config(specs),normal_loads=loads(specs),command=StrategyStepCommand(.5,0,.2,0),shared_state=shared(specs),subsystem_states=snapshots(specs))
        self.assertEqual(3,len(force.contacts)); self.assertEqual(3,len(energy.contacts)); self.assertEqual(3,len(health.contacts))

    def test_bad_allocation_and_conflicting_command_are_rejected(self):
        specs=list(four()); specs[0]=replace(specs[0],drive_allocation_fraction=.2)
        with self.assertRaisesRegex(ContactCouplingError,"sum to 1"): config(specs)
        good=four()
        with self.assertRaisesRegex(ContactCouplingError,"simultaneous"):
            couple_contacts(config=config(good),normal_loads=loads(good),command=StrategyStepCommand(.5,.5,0,0),shared_state=shared(good),subsystem_states=snapshots(good))

    def test_contact_mismatch_negative_speed_and_time_mismatch_fail(self):
        specs=four()
        with self.assertRaises(ContactCouplingError): couple_contacts(config=config(specs),normal_loads=loads(specs)[:-1],command=StrategyStepCommand(1,0,0,0),shared_state=shared(specs),subsystem_states=snapshots(specs))
        negative=shared(specs); negative=replace(negative,contacts=(replace(negative.contacts[0],angular_speed_rad_per_s=-1),*negative.contacts[1:]))
        with self.assertRaisesRegex(ContactCouplingError,"negative wheel"):
            couple_contacts(config=config(specs),normal_loads=loads(specs),command=StrategyStepCommand(1,0,0,0),shared_state=negative,subsystem_states=snapshots(specs))
        badstates=list(snapshots(specs)); badstates[0]=replace(badstates[0],state=replace(badstates[0].state,time_s=1))
        with self.assertRaisesRegex(ContactCouplingError,"time"):
            couple_contacts(config=config(specs),normal_loads=loads(specs),command=StrategyStepCommand(1,0,0,0),shared_state=shared(specs),subsystem_states=tuple(badstates))

    def test_physical_suspension_failure_is_retained_not_invalid(self):
        specs=four(); states=list(snapshots(specs)); states[0]=replace(states[0],state=replace(states[0].state,suspension_velocity_m_per_s=100))
        _,_,health,_=couple_contacts(config=config(specs,duration=.01),normal_loads=loads(specs),command=StrategyStepCommand(0,0,0,0),shared_state=shared(specs),subsystem_states=tuple(states))
        self.assertEqual("suspension_travel",health.contacts[0].failure_mode)

    def test_adapter_emits_exact_outputs_and_invalid_has_zero_writes(self):
        specs=four(); current=shared(specs); adapter=ContactLimitCouplingAdapter(config(specs),snapshots(specs))
        view=AdapterReadView("contact_limit_solver",current,(RuntimeSignal("chassis.normal_loads",loads(specs)),RuntimeSignal("control.step_command",StrategyStepCommand(.5,0,0,0)),RuntimeSignal("state.current",current)))
        output=adapter.execute(view); self.assertEqual("ok",output.status)
        self.assertEqual({"contact.energy_transfers","contact.force_moment","contact.health_inputs"},{x.signal_id for x in output.signals})
        bad=AdapterReadView("contact_limit_solver",current,(RuntimeSignal("chassis.normal_loads",loads(specs)[:-1]),RuntimeSignal("control.step_command",StrategyStepCommand(.5,0,0,0)),RuntimeSignal("state.current",current)))
        invalid=adapter.execute(bad); self.assertEqual("invalid",invalid.status); self.assertEqual((),invalid.signals)

if __name__=="__main__": unittest.main()
