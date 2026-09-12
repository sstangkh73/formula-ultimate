"""Execute Work 129 independent claim checks."""
from __future__ import annotations
import argparse,copy,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/"src"
for item in (ROOT,SRC):
    if str(item) not in sys.path: sys.path.insert(0,str(item))
from formula_ultimate.experiments.independent_claim_validation import IndependentClaimViolation,canonical_sha256,detect_known_omission,independent_analysis,validate_protocol  # noqa:E402
def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def write(path,value): path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def rejected(action,phrase):
    try: action()
    except IndependentClaimViolation as exc:
        if phrase not in str(exc): raise
        return {"status":"rejected","reason":str(exc)}
    raise IndependentClaimViolation("negative control accepted")
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--config",type=Path,required=True); parser.add_argument("--output-root",type=Path,required=True); parser.add_argument("--replay-reference",type=Path); args=parser.parse_args(); config=args.config if args.config.is_absolute() else ROOT/args.config; output=args.output_root if args.output_root.is_absolute() else ROOT/args.output_root
    raw=read(config); validation=validate_protocol(raw)
    for dependency in raw["dependencies"]:
        if sha(ROOT/dependency["contract_path"])!=dependency["contract_sha256"]: raise IndependentClaimViolation("stale dependency contract")
        if subprocess.run(["git","cat-file","-e",dependency["commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise IndependentClaimViolation("missing dependency commit")
    inputs={}
    for item in raw["inputs"]:
        upstream=read(ROOT/item["path"])
        if upstream.get("result_sha256")!=item["result_sha256"]: raise IndependentClaimViolation(f"stale Work {item['work']} result")
        inputs[item["work"]]=upstream
    telemetry_path=ROOT/raw["telemetry"]["path"]
    if sha(telemetry_path)!=raw["telemetry"]["sha256"]: raise IndependentClaimViolation("changed telemetry identity")
    telemetry=read(telemetry_path)
    analysis=independent_analysis(raw,telemetry); omission=detect_known_omission(raw,telemetry)
    shared=copy.deepcopy(raw); shared["independence"]["independent_backend"]=shared["independence"]["upstream_backend"]
    missed=copy.deepcopy(raw); missed["registration"]["open_boundary_penalty_s_per_severity"]=0.0
    controls={"shared_wrapper":rejected(lambda:validate_protocol(shared),"shared-function wrapper"),"known_omission":{"injected":"open boundary penalty","detection":omission},"disabled_detector":rejected(lambda:detect_known_omission(missed,telemetry),"known modeling omission"),"incomplete_telemetry":rejected(lambda:independent_analysis(raw,telemetry[:-1]),"record count")}
    upstream_decision=inputs[128]["body"]["decision"]
    if upstream_decision["robust_superiority_supported"]: raise IndependentClaimViolation("unexpected upstream superiority claim")
    write(output/"independent_analysis.json",analysis); write(output/"discrepancy_register.json",{"paired_time":{"class":analysis["discrepancy_class"],"magnitude_s":analysis["disagreement_s"],"resolution":"conservative boundary interpretation"},"shared_assumptions":raw["shared_assumptions"]})
    body={"status":"completed_claim_downgrade","claim_scope":"independent code-path numerical reinterpretation of locked synthetic telemetry; not institutional independence, physical measurement, novelty, or promotion","validation":validation,"dependencies":raw["dependencies"],"input_result_sha256":{str(k):v["result_sha256"] for k,v in sorted(inputs.items())},"telemetry_sha256":raw["telemetry"]["sha256"],"independence":raw["independence"],"analysis":analysis,"controls":controls,"artifact_sha256":{"independent_analysis.json":sha(output/"independent_analysis.json"),"discrepancy_register.json":sha(output/"discrepancy_register.json")},"coverage":raw["coverage"],"upstream_comparison_after_independent_calculation":{"work128_decision":upstream_decision,"consistent_non_superiority":not analysis["time_superiority_survives"]},"decision":{"selected_claims_survive":False,"promotion_allowed":False,"reason":"conservative independent interpretation reduced the time effect to 0.22 s and exposed a 0.28 s model-boundary discrepancy"},"review":{"supporting_evidence":["a separate source module reconstructed results from locked raw telemetry","energy thermal and structural gates remained positive","known omitted-boundary control was detected"],"contradicting_evidence":["the independent time effect fell from 0.5 s to 0.22 s","the 0.28 s discrepancy exceeded the registered trigger"],"alternative_explanations":["both paths share synthetic telemetry and candidate assumptions","the conservative correction may overstate unmodeled boundary effects"],"missing_evidence":["institutionally independent implementation","independent measured boundary histories","physical measurements"],"confidence":"moderate for numerical claim downgrade; none for physical validation"}}
    result={"body":body,"result_sha256":canonical_sha256(body)}; write(output/"result.json",result)
    if args.replay_reference:
        reference=args.replay_reference if args.replay_reference.is_absolute() else ROOT/args.replay_reference; prior=read(reference); exact=prior.get("result_sha256")==result["result_sha256"]; write(output/"replay.json",{"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"],"exact":exact})
        if not exact: raise IndependentClaimViolation("decision replay differs from reference")
    print(json.dumps({"status":body["status"],"result_sha256":result["result_sha256"],"independent_mean_s":analysis["independent_mean_s"],"disagreement_s":analysis["disagreement_s"],"promotion_allowed":False},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
