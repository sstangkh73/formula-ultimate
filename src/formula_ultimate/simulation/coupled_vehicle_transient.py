"""Bounded conservative whole-candidate transient harness for Work 123."""
from __future__ import annotations
import hashlib,json,math
from typing import Any,Mapping
PROTOCOL_VERSION="coupled_vehicle_transient_v1"
class CoupledTransientViolation(ValueError): pass
def canonical_sha256(value):
    try: payload=json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    except (TypeError,ValueError) as exc: raise CoupledTransientViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()
def validate_protocol(raw:Mapping[str,Any]):
    required={"protocol_version","units","dependencies","inputs","candidate","exchange_schema","trial","limits","coupling","time_steps_s","tolerances","coverage","experiment"}
    if set(raw)!=required or raw.get("protocol_version")!=PROTOCOL_VERSION: raise CoupledTransientViolation("protocol schema or identity mismatch")
    if raw.get("units")!="SI_m_kg_s_K_N_W_J": raise CoupledTransientViolation("protocol units mismatch")
    if {x.get("work") for x in raw["dependencies"]}!={117,118,119,120,121,122}: raise CoupledTransientViolation("Work 117 through 122 dependencies are required")
    expected={"traction_work_j":"ground_to_body_positive","drag_work_j":"body_to_air_positive","storage_draw_j":"storage_out_positive","heat_generated_j":"subsystems_to_thermal_positive","cooling_removed_j":"thermal_to_ambient_positive"}
    if raw["exchange_schema"]["signs"]!=expected or raw["exchange_schema"]["frame"]!="route_x_forward": raise CoupledTransientViolation("mismatched exchange frame or signs")
    owners=raw["exchange_schema"]["state_owners"]
    if set(owners)!={"position_velocity","stored_energy","temperature","controller_delay"}: raise CoupledTransientViolation("state ownership is incomplete")
    if sorted(raw["time_steps_s"],reverse=True)!=raw["time_steps_s"] or len(raw["time_steps_s"])<3: raise CoupledTransientViolation("time-step ladder is invalid")
    if any(value<=0 for value in (raw["trial"]["mass_kg"],raw["trial"]["duration_s"],raw["limits"]["ground_force_n"],raw["limits"]["actuation_output_power_w"],raw["limits"]["thermal_capacity_j_k"])): raise CoupledTransientViolation("trial or limits are invalid")
    if not 0<raw["limits"]["actuation_efficiency"]<=1: raise CoupledTransientViolation("actuation efficiency is invalid")
    if any(not values for values in raw["experiment"].values()): raise CoupledTransientViolation("experiment registration is incomplete")
    return {"status":"passed","protocol_sha256":canonical_sha256(raw),"dependency_count":6}
def target_at(schedule,time_s):
    target=schedule[0]["target_speed_m_s"]
    for event in schedule:
        if time_s>=event["time_s"]: target=event["target_speed_m_s"]
    return target
def simulate(raw:Mapping[str,Any],dt_s:float,*,coupled=True,initial_energy_j=None,double_count_power=False,initial_speed_m_s=None):
    validate_protocol(raw)
    if dt_s<=0: raise CoupledTransientViolation("time step must be positive")
    trial=raw["trial"]; limits=raw["limits"]; position=0.0; velocity=trial["initial_speed_m_s"] if initial_speed_m_s is None else initial_speed_m_s; stored=trial["initial_energy_j"] if initial_energy_j is None else initial_energy_j; temperature=trial["initial_temperature_k"]; initial_stored=stored; initial_ke=.5*trial["mass_kg"]*velocity**2; history=[]; events=[]; traction_total=drag_total=heat_total=cooling_total=control_total=0.0; max_step_residual=0.0; max_iterations=0; previous_target=None
    steps=int(round(trial["duration_s"]/dt_s))
    for index in range(steps):
        time=index*dt_s
        if velocity<0 or velocity>limits["external_speed_max_m_s"]: raise CoupledTransientViolation("state outside reduced-model validity")
        target=target_at(trial["target_schedule"],time)
        if target!=previous_target: events.append({"event":"target_change","time_s":time,"target_speed_m_s":target}); previous_target=target
        if stored<=0: events.append({"event":"energy_depleted","time_s":time}); break
        demand=max(0.0,limits["controller_gain_n_per_m_s"]*(target-velocity)); estimate=velocity; force=0.0; iterations=1
        for iteration in range(raw["coupling"]["maximum_iterations"] if coupled else 1):
            power_force=limits["actuation_output_power_w"]/max(estimate,limits["power_regularization_speed_m_s"]); force=min(demand,limits["ground_force_n"],power_force); drag=limits["drag_coefficient_n_per_m_s2"]*estimate**2; acceleration=(force-drag)/trial["mass_kg"]; new_velocity=max(0.0,velocity+acceleration*dt_s); new_estimate=.5*(velocity+new_velocity); iterations=iteration+1
            if abs(new_estimate-estimate)<=raw["coupling"]["velocity_tolerance_m_s"]: estimate=new_estimate; break
            estimate=new_estimate
        max_iterations=max(max_iterations,iterations); drag=limits["drag_coefficient_n_per_m_s2"]*estimate**2; acceleration=(force-drag)/trial["mass_kg"]; new_velocity=max(0.0,velocity+acceleration*dt_s); dx=.5*(velocity+new_velocity)*dt_s; traction_work=force*dx; drag_work=drag*dx; delta_ke=.5*trial["mass_kg"]*(new_velocity**2-velocity**2); control_energy=limits["controller_power_w"]*dt_s; actuation_loss=traction_work*(1/limits["actuation_efficiency"]-1); storage_draw=traction_work+actuation_loss+control_energy+(traction_work if double_count_power else 0.0)
        if storage_draw>stored: events.append({"event":"energy_depleted","time_s":time}); break
        heat_generated=actuation_loss+control_energy; thermal_above=max(0.0,(temperature-trial["ambient_temperature_k"])*limits["thermal_capacity_j_k"]); cooling=min(limits["cooling_power_w"]*dt_s,thermal_above+heat_generated); temperature+=(heat_generated-cooling)/limits["thermal_capacity_j_k"]; stored-=storage_draw; position+=dx; velocity=new_velocity
        interface_residual=storage_draw-traction_work-actuation_loss-control_energy; mechanical_residual=traction_work-drag_work-delta_ke; max_step_residual=max(max_step_residual,abs(interface_residual),abs(mechanical_residual)); traction_total+=traction_work; drag_total+=drag_work; heat_total+=heat_generated; cooling_total+=cooling; control_total+=control_energy
        history.append({"time_s":time+dt_s,"position_m":position,"velocity_m_s":velocity,"stored_energy_j":stored,"temperature_k":temperature,"target_speed_m_s":target,"traction_force_n":force,"drag_force_n":drag,"coupling_iterations":iterations,"interface_residual_j":interface_residual,"mechanical_residual_j":mechanical_residual})
    storage_decrease=initial_stored-stored; final_ke=.5*trial["mass_kg"]*velocity**2; global_residual=storage_decrease-(final_ke-initial_ke)-drag_total-heat_total
    unresolved=sorted(key for key,value in raw["coverage"].items() if value.startswith("unresolved"))
    return {"status":"invalid_energy_accounting" if double_count_power else ("energy_depleted" if any(x["event"]=="energy_depleted" for x in events) else "completed_exploratory"),"dt_s":dt_s,"coupled":coupled,"final_position_m":position,"final_velocity_m_s":velocity,"final_stored_energy_j":stored,"final_temperature_k":temperature,"storage_decrease_j":storage_decrease,"traction_work_j":traction_total,"drag_work_j":drag_total,"heat_generated_j":heat_total,"cooling_removed_j":cooling_total,"controller_energy_j":control_total,"global_energy_residual_j":global_residual,"maximum_step_residual_j":max_step_residual,"maximum_coupling_iterations":max_iterations,"events":events,"unresolved_domains":unresolved,"promotion_allowed":False,"history":history,"history_sha256":canonical_sha256(history)}
