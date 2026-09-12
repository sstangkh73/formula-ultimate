"""Preregistered bounded detailed-part comparison for Work 125."""
from __future__ import annotations
import hashlib,json,math,statistics
from typing import Any,Mapping
PROTOCOL_VERSION="detailed_part_comparison_v1"
class DetailedPartComparisonViolation(ValueError): pass
def canonical_sha256(value):
    try: payload=json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    except (TypeError,ValueError) as exc: raise DetailedPartComparisonViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()
def validate_protocol(raw:Mapping[str,Any]):
    required={"protocol_version","units","dependencies","inputs","registration","arms","conditions","budgets","audits","coverage","experiment"}
    if set(raw)!=required or raw.get("protocol_version")!=PROTOCOL_VERSION: raise DetailedPartComparisonViolation("protocol schema or identity mismatch")
    if raw.get("units")!="dimensionless_utility_with_SI_burdens": raise DetailedPartComparisonViolation("protocol units mismatch")
    if {x.get("work") for x in raw["dependencies"]}!={113,114,115,116,124}: raise DetailedPartComparisonViolation("Work 113, 114, 115, 116 and 124 dependencies are required")
    train=set(raw["conditions"]["training"]); holdout=set(raw["conditions"]["holdout"])
    if train & holdout: raise DetailedPartComparisonViolation("holdout leakage detected")
    if len(holdout)!=raw["registration"]["holdout_sample_size"]: raise DetailedPartComparisonViolation("holdout sample size differs from registration")
    if set(raw["arms"])!={"fixed_family","existing_grammar","open_material","random_control"}: raise DetailedPartComparisonViolation("comparison arms are incomplete")
    if len(set(raw["budgets"].values()))!=1: raise DetailedPartComparisonViolation("arm budgets are not matched")
    if any(not values for values in raw["experiment"].values()): raise DetailedPartComparisonViolation("experiment registration is incomplete")
    return {"status":"passed","holdout_count":len(holdout),"protocol_sha256":canonical_sha256(raw)}
def utility(raw,arm_name,parameter,condition,fidelity="fine",*,active=True,hardware_complete=True):
    if not hardware_complete: return {"status":"invalid_omitted_hardware","utility":None}
    arm=raw["arms"][arm_name]; condition_effect=raw["conditions"]["effects"][condition]; value=arm[f"{fidelity}_base"]+arm["parameter_effects"][str(parameter)]+condition_effect
    if arm_name=="open_material" and not active: value-=arm["active_coupling_effect"]
    return {"status":"valid","utility":value,"mass_kg":arm["mass_kg"],"energy_j":arm["energy_j"],"constraint_pass":arm["constraint_pass"]}
def optimize(raw,arm_name):
    arm=raw["arms"][arm_name]; records=[]
    for parameter in arm["parameters"]:
        values=[utility(raw,arm_name,parameter,condition,"coarse")["utility"] for condition in raw["conditions"]["training"]]; records.append({"parameter":parameter,"mean_training_utility":statistics.fmean(values)})
    best=max(records,key=lambda x:(x["mean_training_utility"],-x["parameter"]))
    return {"arm":arm_name,"evaluations":len(records),"records":records,"best_parameter":best["parameter"]}
def paired_study(raw,fidelity="fine"):
    tuned={name:optimize(raw,name) for name in raw["arms"]}; results={}
    for name,item in tuned.items(): results[name]=[utility(raw,name,item["best_parameter"],condition,fidelity) for condition in raw["conditions"]["holdout"]]
    control=max((name for name in raw["arms"] if name!="open_material"),key=lambda name:statistics.fmean(x["utility"] for x in results[name])); differences=[open_item["utility"]-control_item["utility"] for open_item,control_item in zip(results["open_material"],results[control])]; mean=statistics.fmean(differences); sem=statistics.stdev(differences)/math.sqrt(len(differences)) if len(differences)>1 else 0; half=raw["registration"]["t_multiplier"]*sem
    constraints=all(x["constraint_pass"] for x in results["open_material"]); claim=constraints and mean-half>=raw["registration"]["meaningful_effect"]
    return {"fidelity":fidelity,"tuning":tuned,"results":results,"best_control":control,"paired_effects":differences,"mean_effect":mean,"interval":[mean-half,mean+half],"constraints_pass":constraints,"discovery_benefit_gate":claim,"total_evaluations_by_arm":{name:tuned[name]["evaluations"]+len(raw["conditions"]["holdout"]) for name in tuned}}
