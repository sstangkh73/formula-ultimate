"""Generate deterministic Work 027 energy/health coupling evidence."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))

from formula_ultimate.physics.suspension_braking import (BrakeParameters,RegenerationParameters,SuspensionBrakeModule,SuspensionParameters)  # noqa:E402
from formula_ultimate.physics.thermal import ThermalParameters  # noqa:E402
from formula_ultimate.physics.tyre import TyreContactParameters  # noqa:E402
from formula_ultimate.simulation import (AerodynamicCoolingEvidence,CentralEnergyConfiguration,CentralHealthConfiguration,ComponentHealthConfiguration,ComponentHealthState,ContactCouplingConfig,ContactCouplingSpec,ContactEnergyTransfer,ContactEnergyTransfers,ContactNormalLoad,ContactRuntimeState,SharedVehicleState,StrategyStepCommand,couple_contacts,evaluate_central_energy,evaluate_central_health,load_coupling_architecture,subsystem_snapshots_from_shared_state)  # noqa:E402

def state(primary=2000.0):
    return SharedVehicleState(0,0,(0,0,0),(10,0,0),0,0,primary,0,0,
        (ContactRuntimeState("c",1000,0,0,0,10),),
        (ComponentHealthState("store",300,0,0,False),))

def transfers(drive=0,wheel=0,recovered=0,conversion=0,heat=0,duration=1):
    item=ContactEnergyTransfer("c",wheel,recovered,conversion,heat,0,1e6,drive)
    return ContactEnergyTransfers((item,),wheel,recovered,conversion,heat,drive,duration,duration)

def energy_config(aux=0): return CentralEnergyConfiguration(.9,aux,1e6)

def contact_health(current):
    thermal=ThermalParameters(1000,0,0,500,600)
    module=SuspensionBrakeModule("c",SuspensionParameters(100,10000,10,1000,.2,.2),
        BrakeParameters(.3,1,500,thermal),RegenerationParameters(500,10000,10000,1e6,.8,0))
    spec=ContactCouplingSpec("c",0,0,0,0,1,1,TyreContactParameters(2,2),module)
    return couple_contacts(config=ContactCouplingConfig((spec,),0,0,1,300),
        normal_loads=(ContactNormalLoad("c",1000),),command=StrategyStepCommand(0,0,0,0),
        shared_state=current,subsystem_states=subsystem_snapshots_from_shared_state(current))[2]

def health_config(seed=17,heat=1000):
    component=ComponentHealthConfiguration("store",ThermalParameters(100,0,0,301,302),
        heat,1,1,0,0,1,0,0,1,0)
    return CentralHealthConfiguration((component,),seed,0,300)

def health_result(seed=17):
    current=state(1e6); contact=contact_health(current)
    energy=evaluate_central_energy(config=energy_config(),transfers=transfers(),state=current)
    motion=replace(current,time_s=1,race_distance_m=10,position_m=(10,0,0))
    return evaluate_central_health(health_config=health_config(seed),energy_config=energy_config(),
        cooling=AerodynamicCoolingEvidence(1,0,0,"map","evidence"),contact_health=contact,
        energy=energy.evidence,state=current,energy_candidate=energy.candidate_state,motion_candidate=motion)

def main():
    architecture=load_coupling_architecture(ROOT/"config/simulation/coupled_level0_architecture_v3.json")
    drive=evaluate_central_energy(config=energy_config(100),transfers=transfers(drive=900),state=state())
    recovery=evaluate_central_energy(config=energy_config(),transfers=transfers(wheel=1000,recovered=700,conversion=100,heat=200),state=state())
    depletion=evaluate_central_energy(config=energy_config(100),transfers=transfers(drive=900),state=state(550))
    health=health_result(23); replay=health_result(23); other=health_result(24)
    if not all(x.status=="ok" for x in (drive,recovery,depletion,health)): raise RuntimeError("Work 027 reference failed")
    if health!=replay or health.evidence.components[0].reliability_draw==other.evidence.components[0].reliability_draw: raise RuntimeError("seed replay contract failed")
    print(json.dumps({
        "schema_version":"1.0",
        "architecture":{"architecture_id":architecture.architecture_id,"fingerprint_sha256":architecture.fingerprint_sha256},
        "drive":{"start_primary_j":2000,"end_primary_j":drive.candidate_state.primary_energy_j,"drive_wheel_j":drive.evidence.drive_wheel_energy_j,"drive_source_j":drive.evidence.drive_source_energy_j,"auxiliary_j":drive.evidence.auxiliary_energy_j,"all_residuals_passed":all(x.passed for x in drive.residuals)},
        "recovery":{"wheel_removed_j":recovery.evidence.scaled_contact_transfers.total_wheel_energy_removed_j,"recovered_j":recovery.evidence.recovered_energy_added_j,"conversion_loss_j":recovery.evidence.regeneration_conversion_loss_j,"mechanical_heat_j":recovery.evidence.mechanical_brake_heat_j,"residual_j":recovery.evidence.contact_braking_residual_j},
        "depletion":{"executed_duration_s":depletion.evidence.executed_duration_s,"end_primary_j":depletion.candidate_state.primary_energy_j,"event_type":depletion.events[0].event_type},
        "thermal_event":{"executed_duration_s":health.evidence.executed_duration_s,"winner":health.evidence.decision.winner.event_type,"end_temperature_k":health.candidate_state.components[0].temperature_k,"motion_x_m":health.candidate_state.position_m[0],"same_seed_replay":health==replay,"different_seed_changes_draw":health.evidence.components[0].reliability_draw!=other.evidence.components[0].reliability_draw},
        "claim_boundary":"Level-0 coupled energy and health evidence only; not calibrated reliability, cooling, or physical validation"
    },indent=2,sort_keys=True)); return 0

if __name__=="__main__": raise SystemExit(main())
