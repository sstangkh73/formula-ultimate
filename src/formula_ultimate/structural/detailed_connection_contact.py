"""Bounded fastening-scale discrete contact model for Work 113."""
from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping


PROTOCOL_VERSION = "detailed_connection_contact_v1"


class DetailedConnectionViolation(ValueError):
    pass


def canonical_sha256(value: Any) -> str:
    try: encoded=json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode()
    except (TypeError,ValueError) as exc: raise DetailedConnectionViolation("evidence must be finite canonical JSON") from exc
    return hashlib.sha256(encoded).hexdigest()


def validate_protocol(raw: Mapping[str,Any]) -> dict[str,Any]:
    required={"protocol_version","units","dependencies","task","material","contact","strategies","refinement_patch_counts","acceptance","experiment"}
    if set(raw)!=required or raw.get("protocol_version")!=PROTOCOL_VERSION or raw.get("units")!="SI_m_kg_s_K_N_Pa_W_rad": raise DetailedConnectionViolation("protocol schema, identity, or units mismatch")
    if len(raw["dependencies"])!=2 or {x.get("work") for x in raw["dependencies"]}!={111,112}: raise DetailedConnectionViolation("Work 111 and Work 112 dependencies are required")
    for item in raw["dependencies"]:
        if set(item)!={"work","commit","contract_path","contract_sha256"} or len(item["commit"])!=40 or len(item["contract_sha256"])!=64: raise DetailedConnectionViolation("dependency identity is invalid")
    task=raw["task"]
    if set(task)!={"envelope_diameter_m","envelope_length_m","temperature_k","axial_tension_n","shear_n","off_axis_moment_nm","allowed_motion"} or task["allowed_motion"]!="rigid_when_engaged": raise DetailedConnectionViolation("connection task schema is invalid")
    if any(not isinstance(task[k],(int,float)) or isinstance(task[k],bool) or not math.isfinite(task[k]) for k in set(task)-{"allowed_motion"}): raise DetailedConnectionViolation("task values must be finite")
    material=raw["material"]
    if set(material)!={"material_id","youngs_modulus_pa","poisson_ratio","evidence_class"} or material["evidence_class"]!="synthetic_fixture" or material["youngs_modulus_pa"]<=0 or not -1<material["poisson_ratio"]<.5: raise DetailedConnectionViolation("material fixture is invalid")
    contact=raw["contact"]
    if set(contact)!={"law","preload_range_n","friction_range","clearance_range_m","characteristic_depth_m","post_slip_stiffness_fraction"} or contact["law"]!="unilateral_coulomb": raise DetailedConnectionViolation("contact law schema is invalid")
    if len(raw["strategies"])!=2 or {x.get("kind") for x in raw["strategies"]}!={"threaded_helix","segmented_ramp"}: raise DetailedConnectionViolation("reference and alternative strategies are required")
    for strategy in raw["strategies"]:
        common={"strategy_id","kind","contact_radius_m","root_radius_m","outer_radius_m","sleeve_outer_radius_m","engagement_length_m","contact_width_m"}
        specific={"pitch_m"} if strategy["kind"]=="threaded_helix" else {"lug_count","ramp_arc_m"}
        if set(strategy)!=common|specific: raise DetailedConnectionViolation("strategy geometry schema is invalid")
        numeric=[value for key,value in strategy.items() if key not in {"strategy_id","kind","lug_count"}]
        if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or x<=0 for x in numeric): raise DetailedConnectionViolation("strategy dimensions must be positive finite")
        if not strategy["root_radius_m"]<strategy["contact_radius_m"]<strategy["outer_radius_m"]<strategy["sleeve_outer_radius_m"]<=task["envelope_diameter_m"]/2 or strategy["engagement_length_m"]>task["envelope_length_m"]: raise DetailedConnectionViolation("strategy geometry exceeds envelope or radial ordering")
        if strategy["kind"]=="segmented_ramp" and (not isinstance(strategy["lug_count"],int) or strategy["lug_count"]<3): raise DetailedConnectionViolation("segmented ramp count is invalid")
    levels=raw["refinement_patch_counts"]
    if len(levels)!=3 or levels!=sorted(levels) or any(not isinstance(x,int) or x<6 for x in levels): raise DetailedConnectionViolation("three ordered contact refinements are required")
    if any(not values for values in raw["experiment"].values()): raise DetailedConnectionViolation("experiment registration is incomplete")
    return {"status":"passed","strategy_count":2,"refinement_count":3,"protocol_sha256":canonical_sha256(raw)}


def contact_patches(strategy: Mapping[str,Any], count: int, engagement_fraction: float=1.0) -> list[dict[str,float]]:
    if not 0<engagement_fraction<=1 or count<3: raise DetailedConnectionViolation("joint is severed or engagement is invalid")
    radius=float(strategy["contact_radius_m"]); length=float(strategy["engagement_length_m"])*engagement_fraction
    if strategy["kind"]=="threaded_helix":
        turns=length/strategy["pitch_m"]; helix_angle=math.atan(strategy["pitch_m"]/(2*math.pi*radius)); total_area=2*math.pi*radius*length*strategy["contact_width_m"]/strategy["pitch_m"]/math.cos(helix_angle)
        return [{"theta_rad":2*math.pi*turns*(i+.5)/count,"z_m":length*(i+.5)/count,"area_m2":total_area/count,"lever_m":radius*math.sin(2*math.pi*turns*(i+.5)/count)} for i in range(count)]
    lugs=int(strategy["lug_count"]); total_area=lugs*strategy["ramp_arc_m"]*strategy["contact_width_m"]*engagement_fraction
    return [{"theta_rad":2*math.pi*(i+.5)/count,"z_m":length*((i%lugs)+.5)/lugs,"area_m2":total_area/count,"lever_m":radius*math.sin(2*math.pi*(i+.5)/count)} for i in range(count)]


def _normal_distribution(patches, total_compression, moment):
    if total_compression<=0: return [0.0]*len(patches)
    active=list(range(len(patches))); result=[0.0]*len(patches)
    while len(active)>=2:
        ys=[patches[i]["lever_m"] for i in active]; s1=sum(ys); s2=sum(y*y for y in ys); determinant=len(active)*s2-s1*s1
        if determinant<=1e-30: raise DetailedConnectionViolation("contact patch moment basis is singular")
        a=(total_compression*s2-moment*s1)/determinant; b=(moment*len(active)-total_compression*s1)/determinant; values={i:a+b*patches[i]["lever_m"] for i in active}; negative=[i for i,v in values.items() if v<0]
        if not negative:
            for i,v in values.items(): result[i]=v
            return result
        active.remove(min(negative,key=lambda i:values[i]))
    raise DetailedConnectionViolation("off-axis load opened all stable contact paths")


def evaluate(strategy: Mapping[str,Any], material: Mapping[str,Any], contact: Mapping[str,Any], task: Mapping[str,Any], *, patch_count:int, preload_n:float, friction:float, clearance_m:float, engagement_fraction:float=1.0, joint_present:bool=True) -> dict[str,Any]:
    if not joint_present: raise DetailedConnectionViolation("joint removed; no load path")
    if not contact["preload_range_n"][0]<=preload_n<=contact["preload_range_n"][1] or not contact["friction_range"][0]<=friction<=contact["friction_range"][1] or not contact["clearance_range_m"][0]<=clearance_m<=contact["clearance_range_m"][1]: raise DetailedConnectionViolation("contact input is outside registered range")
    patches=contact_patches(strategy,patch_count,engagement_fraction); compression=preload_n-task["axial_tension_n"]
    normal=_normal_distribution(patches,compression,task["off_axis_moment_nm"]); active=[i for i,x in enumerate(normal) if x>1e-12]
    if not active: raise DetailedConnectionViolation("contact opened; no transmitted load path")
    area=sum(patches[i]["area_m2"] for i in active); effective_modulus=material["youngs_modulus_pa"]/(1-material["poisson_ratio"]**2); normal_stiffness=effective_modulus*area/contact["characteristic_depth_m"]
    tangent_stiffness=.4*normal_stiffness; friction_capacity=friction*sum(normal); slip=abs(task["shear_n"])>friction_capacity+1e-12; transmitted_shear=math.copysign(min(abs(task["shear_n"]),friction_capacity),task["shear_n"])
    shear_displacement=transmitted_shear/tangent_stiffness
    if slip: shear_displacement+=math.copysign((abs(task["shear_n"])-friction_capacity)/(tangent_stiffness*contact["post_slip_stiffness_fraction"]),task["shear_n"])
    axial_displacement=clearance_m+task["axial_tension_n"]/normal_stiffness; recovered_moment=sum(n*p["lever_m"] for n,p in zip(normal,patches)); maximum_pressure=max((n/p["area_m2"] for n,p in zip(normal,patches)),default=0)
    force_residual=abs(transmitted_shear-math.copysign(min(abs(task["shear_n"]),friction_capacity),task["shear_n"]))/max(abs(task["shear_n"]),1.0); moment_residual=abs(recovered_moment-task["off_axis_moment_nm"])/max(abs(task["off_axis_moment_nm"]),1.0)
    return {"status":"slip" if slip else "stick","patch_count":patch_count,"active_patch_count":len(active),"active_fraction":len(active)/len(patches),"opening":len(active)<len(patches),"friction_capacity_n":friction_capacity,"transmitted_shear_n":transmitted_shear,"recovered_moment_nm":recovered_moment,"normal_stiffness_n_m":normal_stiffness,"tangent_stiffness_n_m":tangent_stiffness,"axial_displacement_m":axial_displacement,"shear_displacement_m":shear_displacement,"maximum_patch_pressure_pa":maximum_pressure,"force_residual_relative":force_residual,"moment_residual_relative":moment_residual,"minimum_normal_reaction_n":min(normal),"contact_field_sha256":canonical_sha256(normal),"contact_patches":patches,"normal_reactions_n":normal}


def reduced_prediction(reference: Mapping[str,Any], task: Mapping[str,Any], clearance_m:float) -> dict[str,float]:
    return {"axial_displacement_m":clearance_m+task["axial_tension_n"]/reference["normal_stiffness_n_m"],"shear_displacement_m":task["shear_n"]/reference["tangent_stiffness_n_m"]}
