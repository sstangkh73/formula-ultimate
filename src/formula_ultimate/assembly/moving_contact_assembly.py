"""Explicit moving unilateral-contact assembly for Work 114."""
from __future__ import annotations
import hashlib,json,math
from typing import Any,Mapping

PROTOCOL_VERSION="moving_contact_assembly_v1"
class MovingAssemblyViolation(ValueError): pass
def canonical_sha256(value):
    try: data=json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    except (TypeError,ValueError) as exc: raise MovingAssemblyViolation("history must be finite canonical JSON") from exc
    return hashlib.sha256(data).hexdigest()

def validate_protocol(raw:Mapping[str,Any]):
    if set(raw)!={"protocol_version","units","dependency","assembly","motion","time_steps_s","tolerances","experiment"} or raw.get("protocol_version")!=PROTOCOL_VERSION or raw.get("units")!="SI_m_kg_s_N_J_rad": raise MovingAssemblyViolation("protocol schema, identity, or units mismatch")
    d=raw["dependency"]
    if set(d)!={"work113_commit","contract_path","contract_sha256","source_config","strategy_id"} or len(d["work113_commit"])!=40 or len(d["contract_sha256"])!=64: raise MovingAssemblyViolation("Work 113 dependency identity is invalid")
    a=raw["assembly"]
    if set(a)!={"moving_mass_kg","normal_stiffness_n_m","tangent_stiffness_n_m","axial_damping_n_s_m","preload_n","friction","swept_clearance_m","allowed_motion"} or a["allowed_motion"]!="prismatic_axial": raise MovingAssemblyViolation("assembly schema or allowed motion is invalid")
    if any(isinstance(a[k],bool) or not isinstance(a[k],(int,float)) or not math.isfinite(a[k]) or a[k]<=0 for k in set(a)-{"allowed_motion"}): raise MovingAssemblyViolation("assembly values must be positive finite")
    m=raw["motion"]
    if set(m)!={"duration_s","base_amplitude_m","frequency_hz","tangential_amplitude_m","tangential_phase_rad","initial_position_m","initial_velocity_m_s"}: raise MovingAssemblyViolation("motion schema is invalid")
    levels=raw["time_steps_s"]
    if len(levels)!=3 or levels!=sorted(levels,reverse=True) or any(x<=0 for x in levels): raise MovingAssemblyViolation("three coarse-to-fine time steps are required")
    if any(not v for v in raw["experiment"].values()): raise MovingAssemblyViolation("experiment registration is incomplete")
    return {"status":"passed","time_step_count":3,"protocol_sha256":canonical_sha256(raw)}

def simulate(assembly:Mapping[str,Any],motion:Mapping[str,Any],dt:float,*,joint_present=True,allowed_motion=None):
    if not joint_present: raise MovingAssemblyViolation("severed coupling has no load path")
    actual=allowed_motion or assembly["allowed_motion"]
    if actual!="prismatic_axial" and motion["base_amplitude_m"]!=0: raise MovingAssemblyViolation("incompatible rigid/moving constraints")
    mass=assembly["moving_mass_kg"]; stiffness=assembly["normal_stiffness_n_m"]; damping=assembly["axial_damping_n_s_m"]; preload=assembly["preload_n"]; c0=preload/stiffness; omega=2*math.pi*motion["frequency_hz"]
    steps=int(round(motion["duration_s"]/dt)); q=motion["initial_position_m"]; v=motion["initial_velocity_m_s"]; base_prev=motion["base_amplitude_m"]*math.sin(0); initial_pen=max(0,c0+base_prev-q); energy0=.5*mass*v*v+.5*stiffness*initial_pen**2+preload*q; work=0.; loss=0.; impulse=0.; history=[]; prior_contact=initial_pen>0; prior_slip=False; events=[]; min_clear=math.inf; maxq=0.; maxforce=0.
    for index in range(steps+1):
        t=index*dt; base=motion["base_amplitude_m"]*math.sin(omega*t); pen=max(0.,c0+base-q); normal=stiffness*pen; contact=pen>0
        tangential=motion["tangential_amplitude_m"]*math.sin(omega*t+motion["tangential_phase_rad"]); trial=assembly["tangent_stiffness_n_m"]*tangential; capacity=assembly["friction"]*normal; slip=abs(trial)>capacity+1e-12; friction_force=math.copysign(min(abs(trial),capacity),trial) if trial else 0.
        if contact!=prior_contact: events.append({"step":index,"time_s":t,"event":"close" if contact else "open"})
        if slip!=prior_slip: events.append({"step":index,"time_s":t,"event":"slip_start" if slip else "stick_recover"})
        if index:
            work+=normal*(base-base_prev); loss+=damping*v*v*dt; impulse+=normal*dt
        acceleration=(normal-preload-damping*v)/mass; v+=acceleration*dt; q+=v*dt; base_prev=base; prior_contact=contact; prior_slip=slip; min_clear=min(min_clear,assembly["swept_clearance_m"]-abs(q)); maxq=max(maxq,abs(q)); maxforce=max(maxforce,normal)
        history.append({"step":index,"time_s":t,"position_m":q,"velocity_m_s":v,"base_m":base,"normal_force_n":normal,"friction_force_n":friction_force,"contact":contact,"slip":slip})
    pen=max(0,c0+base_prev-q); energy=.5*mass*v*v+.5*stiffness*pen**2+preload*q; residual=abs((energy-energy0)-(work-loss))/max(abs(energy-energy0),abs(work),abs(loss),1e-30)
    return {"status":"passed" if min_clear>=0 else "blocked_collision","dt_s":dt,"step_count":steps,"maximum_abs_position_m":maxq,"maximum_contact_force_n":maxforce,"minimum_swept_clearance_m":min_clear,"transmitted_normal_impulse_n_s":impulse,"energy_change_j":energy-energy0,"boundary_work_j":work,"damping_loss_j":loss,"energy_residual_relative":residual,"constraint_drift_m":0.,"event_count":len(events),"events":events,"history_sha256":canonical_sha256(history),"history":history}

def free_rigid_motion(position,velocity,duration,dt):
    steps=int(round(duration/dt)); final=position+velocity*steps*dt
    return {"final_position_m":final,"analytic_position_m":position+velocity*duration,"error_m":abs(final-(position+velocity*duration))}
