"""Deterministic multiscale search and reserve-before-execute accounting for Work 124."""
from __future__ import annotations
import hashlib,json
from typing import Any,Mapping
PROTOCOL_VERSION="multiscale_discovery_search_v1"
class DiscoverySearchViolation(ValueError): pass
def canonical_sha256(value):
    try: payload=json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    except (TypeError,ValueError) as exc: raise DiscoverySearchViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()
class BudgetLedger:
    def __init__(self,budgets): self.budgets=dict(budgets); self.used={key:0 for key in budgets}; self.records=[]
    def reserve(self,partition,units,candidate_id,attempt):
        if partition not in self.budgets or units<=0: raise DiscoverySearchViolation("invalid budget reservation")
        if self.used[partition]+units>self.budgets[partition]:
            record={"partition":partition,"units":units,"candidate_id":candidate_id,"attempt":attempt,"status":"not_evaluated_budget_exhausted"}; self.records.append(record); return record
        self.used[partition]+=units; record={"partition":partition,"units":units,"candidate_id":candidate_id,"attempt":attempt,"status":"reserved_before_execute"}; self.records.append(record); return record
    def complete(self,record,status):
        if record["status"]!="reserved_before_execute": raise DiscoverySearchViolation("execution lacked prior reservation")
        record["status"]=status
    def snapshot(self): return {"budgets":self.budgets,"used":self.used,"remaining":{key:self.budgets[key]-self.used[key] for key in self.budgets},"records":self.records}
def candidate_admission(candidate):
    value={key:item for key,item in candidate.items() if key!="admission_sha256"}; return canonical_sha256(value)
def verify_candidate(candidate):
    if candidate.get("admission_sha256")!=candidate_admission(candidate): raise DiscoverySearchViolation("tampered admission summary")
    return True
def cache_key(candidate,dependency_identity): return canonical_sha256({"candidate":candidate["candidate_id"],"admission":candidate["admission_sha256"],"dependencies":dependency_identity})
def cache_valid(entry,candidate,dependency_identity): return entry.get("key")==cache_key(candidate,dependency_identity)
def signed_effect(candidate): return candidate["claimed_effect"] if candidate["functional_active"] else 0.0
def classify(candidate,meaningful_effect,near_margin):
    effect=signed_effect(candidate); useful=effect-candidate["uncertainty"]>=meaningful_effect
    if candidate["unresolved"]: archive="unresolved"
    elif candidate["constraint_margin"]>=0: archive="feasible"
    elif candidate["constraint_margin"]>=-near_margin: archive="near_feasible"
    else: archive="unresolved"
    return {"archive":archive,"signed_effect":effect,"useful_shape":useful,"graph_novelty_required":False,"topology_id":candidate["topology_id"],"shape_descriptor":candidate["shape_descriptor"]}
def validate_protocol(raw:Mapping[str,Any]):
    required={"protocol_version","units","dependencies","inputs","external_task","budgets","stage_costs","policies","candidates","audits","admission","coverage","experiment"}
    if set(raw)!=required or raw.get("protocol_version")!=PROTOCOL_VERSION: raise DiscoverySearchViolation("protocol schema or identity mismatch")
    if raw.get("units")!="registered_compute_units": raise DiscoverySearchViolation("accounting unit mismatch")
    if {x.get("work") for x in raw["dependencies"]}!={109,117,123}: raise DiscoverySearchViolation("Work 109, 117 and 123 dependencies are required")
    if set(raw["budgets"])!={"cad","mesh","solver","tuning","audit"} or any(value<=0 for value in raw["budgets"].values()): raise DiscoverySearchViolation("budget partitions are invalid")
    candidate_ids={candidate["candidate_id"] for candidate in raw["candidates"]}
    if any(set(order)!=candidate_ids for order in raw["policies"].values()): raise DiscoverySearchViolation("policies lack matched library opportunity")
    if any(candidate["seed"] not in raw["external_task"]["paired_seeds"] for candidate in raw["candidates"]): raise DiscoverySearchViolation("candidate seed is not paired")
    if any(not values for values in raw["experiment"].values()): raise DiscoverySearchViolation("experiment registration is incomplete")
    return {"status":"passed","candidate_count":len(candidate_ids),"protocol_sha256":canonical_sha256(raw)}
def run_policy(raw:Mapping[str,Any],policy_name:str,dependency_identity:str):
    validate_protocol(raw); ledger=BudgetLedger(raw["budgets"]); by_id={c["candidate_id"]:c for c in raw["candidates"]}; archives={"feasible":[],"near_feasible":[],"unresolved":[]}; not_evaluated=[]
    for candidate_id in raw["policies"][policy_name]:
        candidate=by_id[candidate_id]; verify_candidate(candidate); completed=False
        for attempt,outcome in enumerate(candidate["attempt_outcomes"],start=1):
            exhausted=False
            for stage in ("cad","mesh","solver"):
                reservation=ledger.reserve(stage,raw["stage_costs"][stage],candidate_id,attempt)
                if reservation["status"].startswith("not_evaluated"):
                    exhausted=True; not_evaluated.append({"candidate_id":candidate_id,"stage":stage,"attempt":attempt}); break
                ledger.complete(reservation,"failed_charged" if stage=="solver" and outcome=="failed" else "executed_charged")
                if stage=="solver" and outcome=="failed": break
            if exhausted: break
            if outcome=="failed": continue
            tuning=ledger.reserve("tuning",raw["stage_costs"]["tuning"],candidate_id,attempt)
            if tuning["status"].startswith("not_evaluated"):
                not_evaluated.append({"candidate_id":candidate_id,"stage":"tuning","attempt":attempt}); break
            ledger.complete(tuning,"executed_charged"); decision=classify(candidate,raw["admission"]["meaningful_signed_effect"],raw["admission"]["near_feasible_margin"]); archives[decision["archive"]].append({"candidate_id":candidate_id,"decision":decision,"admission_sha256":candidate["admission_sha256"],"cache_key":cache_key(candidate,dependency_identity)}); completed=True; break
        if not completed and not any(item["candidate_id"]==candidate_id for item in not_evaluated): not_evaluated.append({"candidate_id":candidate_id,"stage":"solver","reason":"all attempts failed"})
    audit_records=[]
    for candidate_id in raw["audits"]["score_independent_candidate_ids"]:
        reservation=ledger.reserve("audit",raw["stage_costs"]["audit"],candidate_id,1)
        if reservation["status"]=="reserved_before_execute": ledger.complete(reservation,"executed_charged_score_independent"); audit_records.append({"candidate_id":candidate_id,"selection_basis":"registered_representation_not_score"})
    snapshot=ledger.snapshot(); unknown_count=len(archives["unresolved"])+len(not_evaluated)
    return {"policy":policy_name,"archives":archives,"not_evaluated":not_evaluated,"audits":audit_records,"ledger":snapshot,"unknown_count":unknown_count,"decision_sha256":canonical_sha256({"archives":archives,"not_evaluated":not_evaluated,"ledger":snapshot})}
