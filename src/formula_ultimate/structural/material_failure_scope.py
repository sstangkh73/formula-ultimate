"""Material provenance gates and bounded yield/buckling references for Work 116."""
from __future__ import annotations
import hashlib,json,math
from typing import Any,Mapping
PROTOCOL_VERSION="material_failure_scope_v1"
class MaterialFailureViolation(ValueError): pass
def canonical_sha256(v):
    try: b=json.dumps(v,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    except (TypeError,ValueError) as exc: raise MaterialFailureViolation("evidence must be finite canonical JSON") from exc
    return hashlib.sha256(b).hexdigest()
def validate_protocol(raw:Mapping[str,Any]):
    if set(raw)!={"protocol_version","units","dependencies","inputs","materials","yield_fixture","buckling_fixture","extension_slots","acceptance","experiment"} or raw.get("protocol_version")!=PROTOCOL_VERSION or raw.get("units")!="SI_m_kg_s_K_N_Pa": raise MaterialFailureViolation("protocol schema, identity, or units mismatch")
    if {x.get("work") for x in raw["dependencies"]}!={111,114,115}: raise MaterialFailureViolation("Work 111, 114 and 115 dependencies are required")
    for d in raw["dependencies"]:
        if set(d)!={"work","commit","contract_path","contract_sha256"} or len(d["commit"])!=40 or len(d["contract_sha256"])!=64: raise MaterialFailureViolation("dependency identity is invalid")
    if set(raw["extension_slots"])!={"fatigue","fracture","wear"} or any(x!="unresolved_missing_tested_data" for x in raw["extension_slots"].values()): raise MaterialFailureViolation("unsupported failure domain was promoted")
    for identity,record in raw["materials"].items(): validate_material(identity,record)
    if any(not x for x in raw["experiment"].values()): raise MaterialFailureViolation("experiment registration is incomplete")
    return {"status":"passed","material_count":len(raw["materials"]),"protocol_sha256":canonical_sha256(raw)}
def validate_material(identity,record):
    required={"evidence_class","source","units","temperature_range_k","strain_rate_range_1_s","process","uncertainty_relative","youngs_modulus_pa","yield_stress_pa","density_kg_m3","allowed_uses"}
    if set(record)!=required or record["evidence_class"] not in {"synthetic_fixture","analytic_reference","measured"} or not record["source"] or set(record["units"])!={"youngs_modulus","yield_stress","density"} or record["units"]!={"youngs_modulus":"Pa","yield_stress":"Pa","density":"kg_m3"}: raise MaterialFailureViolation("material provenance or units are incomplete")
    if any(not isinstance(record[k],(int,float)) or isinstance(record[k],bool) or not math.isfinite(record[k]) or record[k]<=0 for k in ("youngs_modulus_pa","yield_stress_pa","density_kg_m3")): raise MaterialFailureViolation("material property is invalid")
    if not 0<=record["uncertainty_relative"]<1 or len(record["temperature_range_k"])!=2 or len(record["strain_rate_range_1_s"])!=2: raise MaterialFailureViolation("material range or uncertainty is invalid")
def applicability(record,temp,rate,process,requested_evidence="diagnostic"):
    validate_material("material",record)
    if requested_evidence=="measured_survival" and record["evidence_class"]!="measured": raise MaterialFailureViolation("synthetic-to-measured relabeling is prohibited")
    if not record["temperature_range_k"][0]<=temp<=record["temperature_range_k"][1]: raise MaterialFailureViolation("temperature outside material range")
    if not record["strain_rate_range_1_s"][0]<=rate<=record["strain_rate_range_1_s"][1]: raise MaterialFailureViolation("strain rate outside material range")
    if process!=record["process"]: raise MaterialFailureViolation("material process is not applicable")
    return {"status":"eligible","scope":"measured_survival" if record["evidence_class"]=="measured" else "diagnostic_reference_only"}
def yield_margin(record,stress_pa):
    if stress_pa<0 or not math.isfinite(stress_pa): raise MaterialFailureViolation("stress must be nonnegative finite")
    lower=record["yield_stress_pa"]*(1-record["uncertainty_relative"]); margin=math.inf if stress_pa==0 else lower/stress_pa-1
    return {"lower_yield_stress_pa":lower,"stress_pa":stress_pa,"margin":margin,"state":"safe_fixture" if margin>=0 else "failed_fixture"}
def euler_buckling(record,geometry,load_n,imperfection_m):
    if set(geometry)!={"length_m","width_m","height_m","effective_length_factor"} or any(geometry[k]<=0 for k in geometry) or load_n<0 or imperfection_m<0: raise MaterialFailureViolation("buckling input is invalid")
    area=geometry["width_m"]*geometry["height_m"]; inertia=geometry["width_m"]*geometry["height_m"]**3/12; radius=math.sqrt(inertia/area); pcr=math.pi**2*record["youngs_modulus_pa"]*inertia/(geometry["effective_length_factor"]*geometry["length_m"])**2; capacity=pcr/(1+imperfection_m/radius); lower=capacity*(1-record["uncertainty_relative"]); margin=math.inf if load_n==0 else lower/load_n-1
    return {"euler_critical_load_n":pcr,"imperfection_adjusted_lower_capacity_n":lower,"radius_of_gyration_m":radius,"margin":margin,"state":"safe_fixture" if margin>=0 else "failed_fixture"}
def combine_without_law(records):
    if len(records)>1: raise MaterialFailureViolation("unjustified material mixture")
    return records[0]
