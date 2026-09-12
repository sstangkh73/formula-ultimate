"""Bounded realized sensor-controller-actuator path for Work 122."""
from __future__ import annotations
import hashlib,json,math
from typing import Any,Mapping
PROTOCOL_VERSION="control_hardware_realization_v1"
class ControlHardwareViolation(ValueError): pass
def canonical_sha256(value):
    try: payload=json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    except (TypeError,ValueError) as exc: raise ControlHardwareViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()
def hardware_mass(hardware):
    return sum(x["mass_kg"] for x in hardware["sensors"])+hardware["controller"]["mass_kg"]+hardware["harness"]["length_m"]*hardware["harness"]["linear_density_kg_m"]+hardware["connector_count"]*hardware["connector_mass_each_kg"]+hardware["mount_count"]*hardware["mount_mass_each_kg"]+hardware["actuator_interface_mass_kg"]
def validate_protocol(raw:Mapping[str,Any]):
    required={"protocol_version","units","dependencies","inputs","task","hardware","signal_graph","models","tuning","tolerances","coverage","experiment"}
    if set(raw)!=required or raw.get("protocol_version")!=PROTOCOL_VERSION: raise ControlHardwareViolation("protocol schema or identity mismatch")
    if raw.get("units")!="SI_m_kg_s_N_W_J_rad": raise ControlHardwareViolation("protocol units mismatch")
    if {x.get("work") for x in raw["dependencies"]}!={119,120}: raise ControlHardwareViolation("Work 119 and Work 120 dependencies are required")
    hardware=raw["hardware"]
    if not hardware["sensors"] or hardware["controller"]["mass_kg"]<=0 or hardware["harness"]["length_m"]<=0 or hardware["mount_count"]<1 or hardware_mass(hardware)<=0: raise ControlHardwareViolation("hardware coverage is incomplete")
    nodes={x["node_id"] for x in raw["signal_graph"]["nodes"]}; edges=raw["signal_graph"]["edges"]
    if {"sensor","controller","actuator"}-nodes or not all(edge["source"] in nodes and edge["target"] in nodes for edge in edges): raise ControlHardwareViolation("signal path is disconnected or ambiguous")
    if not any(edge["source"]=="sensor" and edge["target"]=="controller" for edge in edges) or not any(edge["source"]=="controller" and edge["target"]=="actuator" for edge in edges): raise ControlHardwareViolation("signal path is disconnected or ambiguous")
    models=raw["models"]
    if models["sample_interval_s"]<=0 or models["duration_s"]<=0 or models["actuator_limit_n_m"]<=0 or models["plant_time_constant_s"]<=0: raise ControlHardwareViolation("model limits are invalid")
    if raw["tuning"]["evaluations_per_mode"]<1 or any(len(values)!=raw["tuning"]["evaluations_per_mode"] for values in raw["tuning"]["gain_candidates"].values()): raise ControlHardwareViolation("tuning opportunity is not matched")
    if any(not values for values in raw["experiment"].values()): raise ControlHardwareViolation("experiment registration is incomplete")
    return {"status":"passed","hardware_mass_kg":hardware_mass(hardware),"protocol_sha256":canonical_sha256(raw)}
def simulate(raw:Mapping[str,Any],gain:float,*,delay_steps=None,noise_scale=1.0,dropout_start_s=None,signal_connected=True,supply_energy_j=None,actuator_limit_n_m=None,noncausal_label=0.0):
    validation=validate_protocol(raw); models=raw["models"]; task=raw["task"]; dt=models["sample_interval_s"]; steps=int(round(models["duration_s"]/dt)); delay=models["latency_steps"] if delay_steps is None else delay_steps; limit=models["actuator_limit_n_m"] if actuator_limit_n_m is None else actuator_limit_n_m
    if gain<0 or delay<0 or limit<=0: raise ControlHardwareViolation("controller or finite authority is invalid")
    supply=models["available_supply_energy_j"] if supply_energy_j is None else supply_energy_j
    state=task["initial_state"]; queue=[state]*(delay+1); history=[]; squared=0.0; energy=0.0; saturation_count=0; dropout_count=0; exhausted_count=0
    base_power=sum(x["power_w"] for x in raw["hardware"]["sensors"])+raw["hardware"]["controller"]["power_w"]+raw["hardware"]["signal_power_w"]
    for index in range(steps):
        time=index*dt; dropout=dropout_start_s is not None and time>=dropout_start_s; noise=models["noise_amplitude"]*noise_scale*math.sin((index+1)*1.61803398875+models["noise_seed"]); measured=state+noise; queue.append(measured); delayed=queue.pop(0); error=task["target_state"]-delayed
        requested=gain*error; command=max(-limit,min(limit,requested)); saturation_count+=int(command!=requested)
        if dropout or not signal_connected: command=0.0; dropout_count+=int(dropout)
        actuation_power=abs(command)*models["actuator_reference_speed_rad_s"]; step_energy=(base_power+actuation_power)*dt
        if energy+step_energy>supply: command=0.0; actuation_power=0.0; step_energy=base_power*dt; exhausted_count+=1
        energy+=step_energy; state+=dt*(models["plant_input_gain_per_n_m"]*command-state)/models["plant_time_constant_s"]; actual_error=task["target_state"]-state; squared+=actual_error*actual_error
        history.append({"time_s":time+dt,"state":state,"measurement":measured,"command_n_m":command,"cumulative_energy_j":energy,"dropout":dropout})
    return {"gain":gain,"noncausal_label":noncausal_label,"rmse":math.sqrt(squared/steps),"final_error":task["target_state"]-state,"energy_j":energy,"saturation_count":saturation_count,"dropout_count":dropout_count,"supply_exhausted_steps":exhausted_count,"hardware_mass_kg":validation["hardware_mass_kg"],"history":history,"trace_sha256":canonical_sha256(history)}
def tune(raw:Mapping[str,Any],mode:str):
    gains=raw["tuning"]["gain_candidates"][mode]; records=[]
    for gain in gains:
        result=simulate(raw,gain); result.pop("history"); records.append(result)
    best=min(records,key=lambda x:(x["rmse"],x["gain"]))
    return {"mode":mode,"evaluations":len(records),"records":records,"best_gain":best["gain"],"best_rmse":best["rmse"]}
