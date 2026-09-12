"""Two-region bidirectional thermal-solid coupling for Work 115."""
from __future__ import annotations
import hashlib,json,math
from typing import Any,Mapping
PROTOCOL_VERSION="coupled_thermal_solid_v1"
class CoupledThermalSolidViolation(ValueError): pass
def canonical_sha256(v):
    try: b=json.dumps(v,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    except (TypeError,ValueError) as exc: raise CoupledThermalSolidViolation("evidence must be finite canonical JSON") from exc
    return hashlib.sha256(b).hexdigest()
def validate_protocol(raw:Mapping[str,Any]):
    if set(raw)!={"protocol_version","units","dependencies","geometry","materials","thermal","mechanical","time_steps_s","tolerances","experiment"} or raw.get("protocol_version")!=PROTOCOL_VERSION or raw.get("units")!="SI_m_kg_s_K_N_Pa_W_J": raise CoupledThermalSolidViolation("protocol schema, identity, or units mismatch")
    if {x.get("work") for x in raw["dependencies"]}!={111,113}: raise CoupledThermalSolidViolation("Work 111 and Work 113 dependencies are required")
    for d in raw["dependencies"]:
        if set(d)!={"work","commit","contract_path","contract_sha256"} or len(d["commit"])!=40 or len(d["contract_sha256"])!=64: raise CoupledThermalSolidViolation("dependency identity is invalid")
    if set(raw["geometry"])!={"male_volume_m3","female_volume_m3","engagement_length_m","contact_area_m2","work113_result_path","work113_result_sha256","male_step_sha256","female_step_sha256"}: raise CoupledThermalSolidViolation("geometry evidence schema is invalid")
    if set(raw["materials"])!={"male","female"}: raise CoupledThermalSolidViolation("two material regions are required")
    for m in raw["materials"].values():
        if set(m)!={"density_kg_m3","specific_heat_j_kg_k","youngs_modulus_pa","thermal_expansion_1_k","modulus_temperature_coefficient_1_k","valid_temperature_k","evidence_class"} or m["evidence_class"]!="synthetic_fixture": raise CoupledThermalSolidViolation("material thermal schema is invalid")
    if len(raw["time_steps_s"])!=3 or raw["time_steps_s"]!=sorted(raw["time_steps_s"],reverse=True): raise CoupledThermalSolidViolation("three coarse-to-fine time steps are required")
    if any(not v for v in raw["experiment"].values()): raise CoupledThermalSolidViolation("experiment registration is incomplete")
    return {"status":"passed","time_step_count":3,"protocol_sha256":canonical_sha256(raw)}
def _properties(material,temp):
    low,high=material["valid_temperature_k"]
    if not low<=temp<=high: raise CoupledThermalSolidViolation("temperature left registered property range")
    modulus=material["youngs_modulus_pa"]*(1-material["modulus_temperature_coefficient_1_k"]*(temp-293.15))
    if modulus<=0: raise CoupledThermalSolidViolation("temperature-dependent modulus became non-positive")
    return modulus,material["thermal_expansion_1_k"]*(temp-293.15)
def simulate(raw:Mapping[str,Any],dt:float,*,coupled=True,contact_area_scale=1.,contact_enabled=True,heat_input_w=None,boundary_conductance_w_k=None):
    g=raw["geometry"]; male=raw["materials"]["male"]; female=raw["materials"]["female"]; th=raw["thermal"]; mech=raw["mechanical"]
    if contact_area_scale<=0: raise CoupledThermalSolidViolation("interface area must be positive")
    cm=g["male_volume_m3"]*male["density_kg_m3"]*male["specific_heat_j_kg_k"]; cf=g["female_volume_m3"]*female["density_kg_m3"]*female["specific_heat_j_kg_k"]
    tm=tf=th["initial_temperature_k"]; ambient=th["ambient_temperature_k"]; heat=th["heat_input_w"] if heat_input_w is None else heat_input_w; hb=th["boundary_conductance_w_k"] if boundary_conductance_w_k is None else boundary_conductance_w_k; area=g["contact_area_m2"]*contact_area_scale; steps=int(round(th["duration_s"]/dt)); boundary_energy=0.; interface_energy=0.; history=[]; initial_energy=cm*tm+cf*tf
    for index in range(steps+1):
        em,exp_m=_properties(male,tm); ef,exp_f=_properties(female,tf); stiffness=mech["reference_joint_stiffness_n_m"]*.5*(em/male["youngs_modulus_pa"]+ef/female["youngs_modulus_pa"]); preload=mech["reference_preload_n"]+mech["preload_sensitivity_n_m"]*g["engagement_length_m"]*(exp_m-exp_f)
        if preload<=0: raise CoupledThermalSolidViolation("thermal expansion opened the preloaded joint")
        conductance=(th["contact_conductance_w_m2_k"]*area*(preload/mech["reference_preload_n"])**th["preload_conductance_exponent"] if contact_enabled else 0.) if coupled else th["contact_conductance_w_m2_k"]*area
        q_contact=conductance*(tm-tf); q_boundary=hb*(tf-ambient); constrained_stress=em*exp_m; history.append({"step":index,"time_s":index*dt,"male_temperature_k":tm,"female_temperature_k":tf,"interface_heat_w":q_contact,"boundary_heat_w":q_boundary,"male_free_expansion_m":g["engagement_length_m"]*exp_m,"constrained_male_stress_pa":constrained_stress,"joint_modulus_pa":em,"joint_stiffness_n_m":stiffness,"preload_n":preload,"contact_conductance_w_k":conductance})
        if index==steps: break
        tm_next=tm+dt*(heat-q_contact)/cm; tf_next=tf+dt*(q_contact-q_boundary)/cf; interface_energy+=q_contact*dt; boundary_energy+=q_boundary*dt; tm,tf=tm_next,tf_next
    stored=cm*tm+cf*tf-initial_energy; supplied=heat*steps*dt; residual=abs(stored-(supplied-boundary_energy))/max(abs(stored),abs(supplied),abs(boundary_energy),1e-30)
    return {"status":"passed","dt_s":dt,"male_final_temperature_k":tm,"female_final_temperature_k":tf,"maximum_temperature_k":max(max(x["male_temperature_k"],x["female_temperature_k"]) for x in history),"final_preload_n":history[-1]["preload_n"],"final_joint_stiffness_n_m":history[-1]["joint_stiffness_n_m"],"final_contact_conductance_w_k":history[-1]["contact_conductance_w_k"],"interface_energy_j":interface_energy,"boundary_energy_j":boundary_energy,"stored_energy_change_j":stored,"supplied_energy_j":supplied,"energy_residual_relative":residual,"history_sha256":canonical_sha256(history),"history":history}
def insulated_energy_rise(power,duration,capacity,initial): return initial+power*duration/capacity
