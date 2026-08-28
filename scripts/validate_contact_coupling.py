"""Generate deterministic Work 025 contact-coupling evidence."""
from __future__ import annotations
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from formula_ultimate.physics.suspension_braking import (BrakeParameters,RegenerationParameters,SuspensionBrakeModule,SuspensionBrakeState,SuspensionParameters)  # noqa:E402
from formula_ultimate.physics.thermal import ThermalParameters  # noqa:E402
from formula_ultimate.physics.tyre import TyreContactParameters  # noqa:E402
from formula_ultimate.simulation import (ComponentHealthState,ContactCouplingConfig,
    ContactCouplingSpec,ContactNormalLoad,ContactRuntimeState,ContactSubsystemSnapshot,
    SharedVehicleState,StrategyStepCommand,couple_contacts)  # noqa:E402
def module(cid,preload): return SuspensionBrakeModule(cid,SuspensionParameters(100,10000,10,preload,.2,.2),BrakeParameters(.3,1,500,ThermalParameters(1000,10,0,500,600)),RegenerationParameters(500,10000,10000,1e6,.8,1))
def main():
    ids=("front","left","right"); normal=(100.,1300.,1300.)
    specs=tuple(ContactCouplingSpec(cid,x,y,.1,2000,1/3,1/3,TyreContactParameters(1,1),module(cid,n)) for cid,x,y,n in zip(ids,(1,-.5,-.5),(0,.7,-.7),normal))
    config=ContactCouplingConfig(specs,3000,3000,.01,300)
    state=SharedVehicleState(0,0,(0,0,0),(20,0,0),0,0,1e6,0,0,tuple(ContactRuntimeState(cid,n,0,0,0,20) for cid,n in zip(ids,normal)),(ComponentHealthState("store",300,0,0,False),))
    snapshots=tuple(ContactSubsystemSnapshot(cid,SuspensionBrakeState(0,0,0,300,0)) for cid in ids)
    load_records=tuple(ContactNormalLoad(cid,n) for cid,n in zip(ids,normal))
    drive=couple_contacts(config=config,normal_loads=load_records,command=StrategyStepCommand(1,0,0,0),shared_state=state,subsystem_states=snapshots)
    brake=couple_contacts(config=config,normal_loads=load_records,command=StrategyStepCommand(0,1,1,1),shared_state=state,subsystem_states=snapshots)
    if drive != couple_contacts(config=config,normal_loads=load_records,command=StrategyStepCommand(1,0,0,0),shared_state=state,subsystem_states=snapshots): raise RuntimeError("replay mismatch")
    force,energy,health,residuals=brake
    if not all(r.passed for r in residuals): raise RuntimeError("contact residual failure")
    consistency=[]
    for item,transfer,spec in zip(force.contacts,energy.contacts,specs):
        expected=abs(item.tyre_result.applied_longitudinal_force_n)*spec.subsystem.brake.effective_radius_m*20*.01
        consistency.append(abs(expected-transfer.wheel_energy_removed_j)<=1e-9)
    evidence={"schema_version":"1.0","claim_boundary":"Work 025 Level-0 contact coupling; not calibrated physical validation","topology_contact_count":3,
        "drive":{"requested_total_n":3000,"applied_total_body_n":drive[0].total_body_longitudinal_force_n,"front_unserved_n":drive[0].contacts[0].unserved_local_longitudinal_force_n,"redistributed":False},
        "brake":{"recovered_energy_j":energy.total_recovered_storage_energy_j,"mechanical_heat_j":energy.total_mechanical_brake_heat_j,"wheel_energy_j":energy.total_wheel_energy_removed_j,"per_contact_energy_force_consistency":consistency,"unserved_torque_n_m":[x.unserved_brake_torque_n_m for x in energy.contacts]},
        "health":{"failure_modes":[x.failure_mode for x in health.contacts]},"residual_count":len(residuals),"all_residuals_passed":all(r.passed for r in residuals),"replay_equal":True}
    print(json.dumps(evidence,indent=2,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
