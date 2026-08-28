"""Work 025 per-contact tyre, suspension, brake, and regen coupling."""

from __future__ import annotations
from dataclasses import dataclass, field, replace
import math

from formula_ultimate.physics.suspension_braking import (
    SuspensionBrakeModule, SuspensionBrakeState, SuspensionBrakeStepInput,
    SuspensionBrakeStepResult, evaluate_suspension_brake_step,
)
from formula_ultimate.physics.tyre import (
    TyreContactParameters, TyreForceRequest, TyreForceResult, resolve_tyre_force,
)
from .aero_load_coupling import ContactNormalLoad
from .coupling import ResidualEntry, SharedVehicleState
from .step_inputs import StrategyStepCommand
from .transaction import AdapterOutput, AdapterReadView, RuntimeSignal

CONTACT_ADAPTER_VERSION="work011-work018-contact-v1"

class ContactCouplingError(ValueError): pass
def _finite(name,value):
    if not isinstance(value,(int,float)) or isinstance(value,bool) or not math.isfinite(value): raise ContactCouplingError(f"{name} must be finite")
def _nonnegative(name,value):
    _finite(name,value)
    if value < 0: raise ContactCouplingError(f"{name} must be non-negative")

@dataclass(frozen=True,slots=True)
class ContactCouplingSpec:
    contact_id:str; x_position_m:float; y_position_m:float
    maximum_steer_angle_rad:float; maximum_lateral_request_n:float
    drive_allocation_fraction:float
    brake_allocation_fraction:float; tyre:TyreContactParameters
    subsystem:SuspensionBrakeModule
    def __post_init__(self):
        if not self.contact_id.strip() or self.subsystem.module_id != self.contact_id: raise ContactCouplingError("contact/subsystem IDs must match and be nonblank")
        for name in ("x_position_m","y_position_m","maximum_steer_angle_rad"): _finite(name,getattr(self,name))
        for name in ("maximum_lateral_request_n","drive_allocation_fraction","brake_allocation_fraction"): _nonnegative(name,getattr(self,name))
        if not isinstance(self.tyre,TyreContactParameters): raise ContactCouplingError("tyre parameters required")

@dataclass(frozen=True,slots=True)
class ContactCouplingConfig:
    specs:tuple[ContactCouplingSpec,...]; total_maximum_drive_force_n:float
    total_maximum_brake_torque_n_m:float
    duration_s:float; ambient_temperature_k:float; active_cooling_command:float=0
    def __post_init__(self):
        if not self.specs: raise ContactCouplingError("at least one contact spec required")
        ids=[x.contact_id for x in self.specs]
        if len(ids)!=len(set(ids)): raise ContactCouplingError("contact spec IDs must be unique")
        _nonnegative("total maximum drive force",self.total_maximum_drive_force_n)
        _nonnegative("total maximum brake torque",self.total_maximum_brake_torque_n_m)
        _finite("duration_s",self.duration_s); _finite("ambient_temperature_k",self.ambient_temperature_k)
        if self.duration_s<=0 or self.ambient_temperature_k<=0: raise ContactCouplingError("duration and ambient temperature must be positive")
        if not 0<=self.active_cooling_command<=1: raise ContactCouplingError("cooling command must be in [0,1]")
        for label,total in (("drive",math.fsum(x.drive_allocation_fraction for x in self.specs)),("brake",math.fsum(x.brake_allocation_fraction for x in self.specs))):
            if not math.isclose(total,1,rel_tol=0,abs_tol=1e-12): raise ContactCouplingError(f"{label} allocation fractions must sum to 1; received {total!r}")

@dataclass(frozen=True,slots=True)
class ContactSubsystemSnapshot:
    contact_id:str; state:SuspensionBrakeState

@dataclass(frozen=True,slots=True)
class CoupledContactForce:
    contact_id:str; x_position_m:float; y_position_m:float; steer_angle_rad:float
    normal_load_n:float; requested_local_longitudinal_force_n:float
    requested_local_lateral_force_n:float; applied_body_longitudinal_force_n:float
    applied_body_lateral_force_n:float; applied_yaw_moment_n_m:float
    unserved_local_longitudinal_force_n:float; unserved_local_lateral_force_n:float
    tyre_result:TyreForceResult

@dataclass(frozen=True,slots=True)
class ContactForceMoment:
    contacts:tuple[CoupledContactForce,...]; total_body_longitudinal_force_n:float
    total_body_lateral_force_n:float; total_yaw_moment_n_m:float

@dataclass(frozen=True,slots=True)
class ContactEnergyTransfer:
    contact_id:str; wheel_energy_removed_j:float; recovered_storage_energy_j:float
    regenerative_conversion_loss_j:float; mechanical_brake_heat_j:float
    unserved_brake_torque_n_m:float; storage_capacity_margin_j:float

@dataclass(frozen=True,slots=True)
class ContactEnergyTransfers:
    contacts:tuple[ContactEnergyTransfer,...]; total_wheel_energy_removed_j:float
    total_recovered_storage_energy_j:float; total_conversion_loss_j:float
    total_mechanical_brake_heat_j:float

@dataclass(frozen=True,slots=True)
class ContactHealthInput:
    contact_id:str; end_state:SuspensionBrakeState; failure_mode:str
    failure_time_s:float|None; suspension_result:SuspensionBrakeStepResult

@dataclass(frozen=True,slots=True)
class ContactHealthInputs:
    contacts:tuple[ContactHealthInput,...]

def couple_contacts(*,config:ContactCouplingConfig,normal_loads:tuple[ContactNormalLoad,...],
        command:StrategyStepCommand,shared_state:SharedVehicleState,
        subsystem_states:tuple[ContactSubsystemSnapshot,...]):
    if command.throttle_fraction>0 and command.brake_fraction>0: raise ContactCouplingError("simultaneous throttle and brake are undefined")
    expected={x.contact_id for x in config.specs}
    collections=(("normal loads",[x.contact_id for x in normal_loads]),("shared contacts",[x.contact_id for x in shared_state.contacts]),("subsystem states",[x.contact_id for x in subsystem_states]))
    for label,ids in collections:
        if len(ids)!=len(set(ids)) or set(ids)!=expected: raise ContactCouplingError(f"{label} must match contact specs exactly")
    loads={x.contact_id:x.normal_load_n for x in normal_loads}; runtime={x.contact_id:x for x in shared_state.contacts}; states={x.contact_id:x.state for x in subsystem_states}
    forces=[]; energy=[]; health=[]; residuals=[]
    for spec in config.specs:
        contact_state=runtime[spec.contact_id]; subsystem_state=states[spec.contact_id]
        if subsystem_state.time_s != shared_state.time_s: raise ContactCouplingError("subsystem state time must equal shared-state time")
        if contact_state.angular_speed_rad_per_s < 0: raise ContactCouplingError("negative wheel speed requires an explicit reverse model")
        brake_request=config.total_maximum_brake_torque_n_m*command.brake_fraction*spec.brake_allocation_fraction
        regen=spec.subsystem.regeneration
        limited_regen=replace(regen,maximum_regen_torque_n_m=min(regen.maximum_regen_torque_n_m,brake_request*command.recovery_fraction))
        module=replace(spec.subsystem,regeneration=limited_regen)
        result=evaluate_suspension_brake_step(module=module,state=subsystem_state,step_input=SuspensionBrakeStepInput(
            config.duration_s,loads[spec.contact_id],contact_state.angular_speed_rad_per_s,
            brake_request,config.ambient_temperature_k,config.active_cooling_command))
        if result.status=="invalid": raise ContactCouplingError(f"contact {spec.contact_id} invalid: {result.reason}")
        drive=config.total_maximum_drive_force_n*command.throttle_fraction*spec.drive_allocation_fraction
        brake_force=0 if result.applied_total_brake_torque_n_m is None else -result.applied_total_brake_torque_n_m/spec.subsystem.brake.effective_radius_m
        requested_fx=drive+brake_force
        requested_fy=spec.maximum_lateral_request_n*command.steering_request
        tyre=resolve_tyre_force(parameters=spec.tyre,normal_load_n=loads[spec.contact_id],request=TyreForceRequest(requested_fx,requested_fy))
        if brake_request > 0 and tyre.saturation_scale < 1:
            projected_brake_torque=abs(tyre.applied_longitudinal_force_n)*spec.subsystem.brake.effective_radius_m
            result=evaluate_suspension_brake_step(module=module,state=subsystem_state,step_input=SuspensionBrakeStepInput(
                config.duration_s,loads[spec.contact_id],contact_state.angular_speed_rad_per_s,
                projected_brake_torque,config.ambient_temperature_k,config.active_cooling_command))
            if result.status=="invalid": raise ContactCouplingError(f"contact {spec.contact_id} projected brake invalid: {result.reason}")
            final_force=0 if result.applied_total_brake_torque_n_m is None else -result.applied_total_brake_torque_n_m/spec.subsystem.brake.effective_radius_m
            if not math.isclose(final_force,tyre.applied_longitudinal_force_n,rel_tol=1e-10,abs_tol=1e-10):
                raise ContactCouplingError("projected brake torque did not replay through subsystem")
        steer=spec.maximum_steer_angle_rad*command.steering_request; cosine=math.cos(steer); sine=math.sin(steer)
        body_fx=cosine*tyre.applied_longitudinal_force_n-sine*tyre.applied_lateral_force_n
        body_fy=sine*tyre.applied_longitudinal_force_n+cosine*tyre.applied_lateral_force_n
        yaw=spec.x_position_m*body_fy-spec.y_position_m*body_fx
        forces.append(CoupledContactForce(spec.contact_id,spec.x_position_m,spec.y_position_m,steer,loads[spec.contact_id],requested_fx,requested_fy,body_fx,body_fy,yaw,tyre.residual_longitudinal_force_n,tyre.residual_lateral_force_n,tyre))
        final_brake_torque=result.applied_total_brake_torque_n_m or 0
        original_unserved_brake=max(0,brake_request-final_brake_torque)
        energy.append(ContactEnergyTransfer(spec.contact_id,result.wheel_energy_removed_j or 0,result.recovered_storage_energy_j or 0,result.regenerative_conversion_loss_j or 0,result.mechanical_brake_heat_j or 0,original_unserved_brake,result.residuals.storage_capacity_margin_j if result.residuals else 0))
        health.append(ContactHealthInput(spec.contact_id,result.end_state,result.failure_mode,result.failure_time_s,result))
        if result.residuals:
            residuals.extend((ResidualEntry(f"{spec.contact_id}.suspension-force","force",result.residuals.suspension_force_n,"N",1e-6,1e-10,max(1,loads[spec.contact_id])),ResidualEntry(f"{spec.contact_id}.brake-torque","moment",result.residuals.brake_torque_n_m,"N*m",1e-9,1e-10,max(1,brake_request)),ResidualEntry(f"{spec.contact_id}.brake-energy","energy",result.residuals.brake_energy_j,"J",1e-6,1e-10,max(1,result.wheel_energy_removed_j or 0))))
    force_signal=ContactForceMoment(tuple(forces),math.fsum(x.applied_body_longitudinal_force_n for x in forces),math.fsum(x.applied_body_lateral_force_n for x in forces),math.fsum(x.applied_yaw_moment_n_m for x in forces))
    energy_signal=ContactEnergyTransfers(tuple(energy),math.fsum(x.wheel_energy_removed_j for x in energy),math.fsum(x.recovered_storage_energy_j for x in energy),math.fsum(x.regenerative_conversion_loss_j for x in energy),math.fsum(x.mechanical_brake_heat_j for x in energy))
    return force_signal,energy_signal,ContactHealthInputs(tuple(health)),tuple(residuals)

@dataclass(frozen=True,slots=True)
class ContactLimitCouplingAdapter:
    config:ContactCouplingConfig; subsystem_states:tuple[ContactSubsystemSnapshot,...]
    module_id:str=field(default="contact_limit_solver",init=False)
    model_version:str=field(default=CONTACT_ADAPTER_VERSION,init=False)
    def execute(self,view:AdapterReadView)->AdapterOutput:
        loads=view.read("chassis.normal_loads"); command=view.read("control.step_command"); state=view.read("state.current")
        if not isinstance(loads,tuple) or not all(isinstance(x,ContactNormalLoad) for x in loads) or not isinstance(command,StrategyStepCommand) or not isinstance(state,SharedVehicleState): return AdapterOutput(self.module_id,"invalid",(),reason="contact adapter payload types are invalid")
        try: force,energy,health,residuals=couple_contacts(config=self.config,normal_loads=loads,command=command,shared_state=state,subsystem_states=self.subsystem_states)
        except (ArithmeticError,ValueError) as exc: return AdapterOutput(self.module_id,"invalid",(),reason=str(exc))
        if any(not x.passed for x in residuals): return AdapterOutput(self.module_id,"invalid",(),reason="contact residual failed",residuals=residuals)
        return AdapterOutput(self.module_id,"ok",(RuntimeSignal("contact.energy_transfers",energy),RuntimeSignal("contact.force_moment",force),RuntimeSignal("contact.health_inputs",health)),residuals=residuals)
