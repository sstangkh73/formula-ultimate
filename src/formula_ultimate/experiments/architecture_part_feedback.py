"""Bounded bidirectional architecture-to-part regeneration for Work 117."""
from __future__ import annotations
import hashlib,json,math
from typing import Any,Mapping
PROTOCOL_VERSION="architecture_part_feedback_v1"
class ArchitectureFeedbackViolation(ValueError): pass
def canonical_sha256(v):
    try: b=json.dumps(v,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    except (TypeError,ValueError) as exc: raise ArchitectureFeedbackViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(b).hexdigest()
def validate_protocol(raw:Mapping[str,Any]):
    if set(raw)!={"protocol_version","units","dependencies","inputs","external_task","initial_internal_task","coefficients","resource_cap","feedback_rules","model_coverage","experiment"} or raw.get("protocol_version")!=PROTOCOL_VERSION or raw.get("units")!="SI_m_kg_s_K_N_Pa_W": raise ArchitectureFeedbackViolation("protocol schema, identity, or units mismatch")
    if {x.get("work") for x in raw["dependencies"]}!={112,114,115}: raise ArchitectureFeedbackViolation("Work 112, 114 and 115 dependencies are required")
    for d in raw["dependencies"]:
        if set(d)!={"work","commit","contract_path","contract_sha256"} or len(d["commit"])!=40 or len(d["contract_sha256"])!=64: raise ArchitectureFeedbackViolation("dependency identity is invalid")
    cap=raw["resource_cap"]
    if set(cap)!={"iterations","evaluations_per_iteration","seeds"} or cap["iterations"]!=len(cap["seeds"]) or cap["evaluations_per_iteration"]<1: raise ArchitectureFeedbackViolation("resource cap is invalid")
    required={"allowable_stress_pa","density_kg_m3","conductance_w_m2_k","allowed_temperature_rise_k","region_length_m","minimum_area_m2"}
    if set(raw["coefficients"])!=required or any(raw["coefficients"][x]<=0 for x in required): raise ArchitectureFeedbackViolation("missing or invalid required coefficient")
    if any(not x for x in raw["experiment"].values()): raise ArchitectureFeedbackViolation("experiment registration is incomplete")
    return {"status":"passed","iterations":cap["iterations"],"protocol_sha256":canonical_sha256(raw)}
def propose_task(previous:Mapping[str,Any],conditions:Mapping[str,float],version:int):
    return {"task_id":f"internal_v{version}","parent_task_sha256":canonical_sha256(previous),"version":version,"load_n":max(previous["load_n"],conditions["assembly_load_n"]),"heat_w":max(previous["heat_w"],conditions["assembly_heat_w"]),"motion_envelope_m":max(previous["motion_envelope_m"],conditions["assembly_motion_m"]),"envelope_m":previous["envelope_m"],"unknowns":sorted(set(previous["unknowns"])|set(conditions.get("unknowns",[])))}
def generate_candidate(task:Mapping[str,Any],coefficients:Mapping[str,float],seed:int):
    for key in ("allowable_stress_pa","density_kg_m3","conductance_w_m2_k","allowed_temperature_rise_k","region_length_m","minimum_area_m2"):
        if key not in coefficients: raise ArchitectureFeedbackViolation("invented missing coefficient is prohibited")
    structural=max(coefficients["minimum_area_m2"],task["load_n"]/coefficients["allowable_stress_pa"]); thermal=max(coefficients["minimum_area_m2"],task["heat_w"]/(coefficients["conductance_w_m2_k"]*coefficients["allowed_temperature_rise_k"])); shape_factor=1+((seed%7)-3)*.01; area=structural*shape_factor; width=math.sqrt(area); geometry={"length_m":coefficients["region_length_m"],"width_m":width,"height_m":area/width,"interface_area_m2":thermal,"motion_keepout_m":task["motion_envelope_m"]}; mass=coefficients["density_kg_m3"]*area*coefficients["region_length_m"]
    return {"candidate_id":f"candidate_v{task['version']}_s{seed}","task_sha256":canonical_sha256(task),"geometry":geometry,"geometry_sha256":canonical_sha256(geometry),"mass_kg":mass,"structural_margin":coefficients["allowable_stress_pa"]*area/task["load_n"]-1,"thermal_margin":coefficients["conductance_w_m2_k"]*thermal*coefficients["allowed_temperature_rise_k"]/task["heat_w"]-1}
def merge_region_mass(regions):
    cells={}
    for region in regions:
        for cell in region["cells"]:
            if cell in cells and cells[cell]!=region["density_kg_m3"]: raise ArchitectureFeedbackViolation("overlapping multifunctional regions have incompatible material")
            cells[cell]=region["density_kg_m3"]
    volume=regions[0]["cell_volume_m3"]
    if any(r["cell_volume_m3"]!=volume for r in regions): raise ArchitectureFeedbackViolation("region cell volumes are incompatible")
    return sum(density*volume for density in cells.values())
def run_loop(raw:Mapping[str,Any],conditions:Mapping[str,float],feedback_enabled:bool):
    external_hash=canonical_sha256(raw["external_task"]); task=dict(raw["initial_internal_task"]); records=[]; invalidations=[]; cap=raw["resource_cap"]
    for iteration,seed in enumerate(cap["seeds"]):
        if feedback_enabled and iteration>0:
            updated=propose_task(task,conditions,iteration); invalidations.append({"iteration":iteration,"invalidated_task_sha256":canonical_sha256(task),"reason":"assembly-derived internal task changed"}); task=updated
        candidate=generate_candidate(task,raw["coefficients"],seed); incomplete=sorted(k for k,v in raw["model_coverage"].items() if v!="implemented")
        records.append({"iteration":iteration,"seed":seed,"task":task,"candidate":candidate,"missing_models":incomplete,"complete_feasibility":False,"evaluation_count":cap["evaluations_per_iteration"]})
    if canonical_sha256(raw["external_task"])!=external_hash: raise ArchitectureFeedbackViolation("external task changed")
    return {"mode":"feedback" if feedback_enabled else "frozen","external_task_sha256":external_hash,"records":records,"invalidations":invalidations,"total_evaluations":sum(x["evaluation_count"] for x in records),"result_sha256":canonical_sha256(records)}
