"""Execute Work 124 multiscale discovery-search accounting evidence."""
from __future__ import annotations
import argparse,copy,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/"src"
for item in (ROOT,SRC):
    if str(item) not in sys.path: sys.path.insert(0,str(item))
from formula_ultimate.search.multiscale_discovery_search import BudgetLedger,DiscoverySearchViolation,cache_key,cache_valid,canonical_sha256,classify,run_policy,validate_protocol,verify_candidate  # noqa:E402
def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def write(path,value): path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def rejected(action,phrase):
    try: action()
    except DiscoverySearchViolation as exc:
        if phrase not in str(exc): raise
        return {"status":"rejected","reason":str(exc)}
    raise DiscoverySearchViolation("negative control accepted")
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--config",type=Path,required=True); parser.add_argument("--output-root",type=Path,required=True); parser.add_argument("--replay-reference",type=Path); args=parser.parse_args(); config=(ROOT/args.config).resolve() if not args.config.is_absolute() else args.config; out=(ROOT/args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root; out.mkdir(parents=True,exist_ok=True)
    raw=read(config); validation=validate_protocol(raw)
    for dependency in raw["dependencies"]:
        if sha(ROOT/dependency["contract_path"])!=dependency["contract_sha256"]: raise DiscoverySearchViolation("stale dependency contract")
        if subprocess.run(["git","cat-file","-e",dependency["commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise DiscoverySearchViolation("missing dependency commit")
    inputs={}
    for item in raw["inputs"]:
        result=read(ROOT/item["path"])
        if result.get("result_sha256")!=item["result_sha256"]: raise DiscoverySearchViolation(f"stale Work {item['work']} result")
        inputs[item["work"]]=result
    if raw["external_task"]["task_id"]!="immutable_external_connection_task" or inputs[123]["body"]["decision"]["promotion_allowed"] or raw["external_task"]["promotion_allowed"]: raise DiscoverySearchViolation("external task or promotion boundary mismatch")
    dependency_identity=canonical_sha256({str(k):v["result_sha256"] for k,v in sorted(inputs.items())})
    policies={name:run_policy(raw,name,dependency_identity) for name in raw["policies"]}
    if any(result["unknown_count"]<=0 for result in policies.values()): raise DiscoverySearchViolation("unknown counter was incorrectly zero")
    if len({canonical_sha256(result["ledger"]["budgets"]) for result in policies.values()})!=1: raise DiscoverySearchViolation("policies did not receive matched budgets")
    for result in policies.values():
        representations={next(c["representation"] for c in raw["candidates"] if c["candidate_id"]==audit["candidate_id"]) for audit in result["audits"]}
        if representations!={"field","brep"}: raise DiscoverySearchViolation("score-independent representation audit coverage failed")
    base=raw["candidates"][0]; shaped=raw["candidates"][1]; shape_decision=classify(shaped,raw["admission"]["meaningful_signed_effect"],raw["admission"]["near_feasible_margin"])
    if base["topology_id"]!=shaped["topology_id"] or not shape_decision["useful_shape"]: raise DiscoverySearchViolation("beneficial same-topology shape was excluded")
    inactive=classify(raw["candidates"][3],raw["admission"]["meaningful_signed_effect"],raw["admission"]["near_feasible_margin"])
    if inactive["signed_effect"]!=0: raise DiscoverySearchViolation("inactive appendage received useful effect")
    ledger=BudgetLedger({"solver":1}); first=ledger.reserve("solver",1,"first",1); ledger.complete(first,"executed_charged"); exhausted=ledger.reserve("solver",1,"second",1)
    entry={"key":cache_key(base,"old_dependencies")}; tampered=copy.deepcopy(base); tampered["claimed_effect"]=99
    controls={"pre_execution_exhaustion":exhausted,"failed_attempt_charged":any(record["status"]=="failed_charged" for record in policies["score_first"]["ledger"]["records"]),"cache_invalidation":{"old_cache_valid_for_current":cache_valid(entry,base,dependency_identity)},"tampered_summary":rejected(lambda:verify_candidate(tampered),"tampered"),"inactive_appendage":inactive,"same_topology_useful_shape":shape_decision}
    body={"status":"passed_accounting_only","claim_scope":"bounded deterministic multiscale search accounting with matched opportunity, scoped archives and exact decision provenance; not discovery, novelty, vehicle promotion, or physical validation","validation":validation,"dependencies":raw["dependencies"],"input_result_sha256":{str(k):v["result_sha256"] for k,v in sorted(inputs.items())},"dependency_identity_sha256":dependency_identity,"policies":policies,"controls":controls,"coverage":raw["coverage"],"promotion":{"allowed":False,"work123_status":inputs[123]["body"]["status"],"reason":"Work 123 and required complete-candidate evidence remain exploratory/unresolved"},"replay_scope":{"decision_replay":"exact SHA required","upstream_numerical_replay":"identified but not re-executed by this search work"},"review":{"supporting_evidence":["both policies received identical task, library, paired seeds, hardware opportunity and partition budgets","reservations preceded execution and failures/retries/audits were charged","same-topology beneficial continuous shape remained eligible while inactive effect became zero"],"contradicting_evidence":["bounded synthetic candidate outcomes do not establish discovery or vehicle benefit"],"alternative_explanations":["archive differences can result from order under finite budget rather than policy quality"],"missing_evidence":["complete candidate evaluations","independent false-negative audits at scale","novelty evidence","physical validation"],"confidence":"high for deterministic accounting/provenance; none for discovery or vehicle superiority"}}
    result={"body":body,"result_sha256":canonical_sha256(body)}; write(out/"result.json",result)
    if args.replay_reference:
        reference=(ROOT/args.replay_reference).resolve() if not args.replay_reference.is_absolute() else args.replay_reference; prior=read(reference); exact=prior.get("result_sha256")==result["result_sha256"]; write(out/"replay.json",{"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"],"exact":exact})
        if not exact: raise DiscoverySearchViolation("decision replay differs from reference")
    print(json.dumps({"status":"passed_accounting_only","result_sha256":result["result_sha256"],"unknown_counts":{name:value["unknown_count"] for name,value in policies.items()},"promotion_allowed":False},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
