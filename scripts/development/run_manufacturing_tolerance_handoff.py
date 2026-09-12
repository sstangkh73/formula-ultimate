"""Execute Work 130 manufacturing and tolerance handoff evidence."""
from __future__ import annotations
import argparse,copy,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/"src"
for item in (ROOT,SRC):
    if str(item) not in sys.path: sys.path.insert(0,str(item))
from formula_ultimate.assembly.manufacturing_tolerance_handoff import ManufacturingHandoffViolation,canonical_sha256,evaluate_handoff,validate_protocol  # noqa:E402
def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def write(path,value): path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def rejected(action,phrase):
    try: action()
    except ManufacturingHandoffViolation as exc:
        if phrase not in str(exc): raise
        return {"status":"rejected","reason":str(exc)}
    raise ManufacturingHandoffViolation("negative control accepted")
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--config",type=Path,required=True); parser.add_argument("--output-root",type=Path,required=True); parser.add_argument("--replay-reference",type=Path); args=parser.parse_args(); config=args.config if args.config.is_absolute() else ROOT/args.config; output=args.output_root if args.output_root.is_absolute() else ROOT/args.output_root
    raw=read(config); validation=validate_protocol(raw)
    for dependency in raw["dependencies"]:
        if sha(ROOT/dependency["contract_path"])!=dependency["contract_sha256"]: raise ManufacturingHandoffViolation("stale dependency contract")
        if subprocess.run(["git","cat-file","-e",dependency["commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise ManufacturingHandoffViolation("missing dependency commit")
    inputs={}
    for item in raw["inputs"]:
        upstream=read(ROOT/item["path"])
        if upstream.get("result_sha256")!=item["result_sha256"]: raise ManufacturingHandoffViolation(f"stale Work {item['work']} result")
        inputs[item["work"]]=upstream
    registry_path=ROOT/raw["registry"]["path"]
    if sha(registry_path)!=raw["registry"]["sha256"]: raise ManufacturingHandoffViolation("changed Work 126 registry")
    registry=read(registry_path); regions={item["region_id"] for item in registry["components"]}
    if regions!=set(raw["registration"]["required_regions"]): raise ManufacturingHandoffViolation("registry region identity mismatch")
    if inputs[129]["body"]["decision"]["selected_claims_survive"]: raise ManufacturingHandoffViolation("Work 129 evidence downgrade mismatch")
    handoff=evaluate_handoff(raw)
    inaccessible=copy.deepcopy(raw); inaccessible["routes"][6]["tool_access"]=False
    trapped=copy.deepcopy(raw); trapped["routes"][0]["trapped_internal_core"]=True
    cyclic=copy.deepcopy(raw); cyclic["assembly_steps"][0]["after"]=["inspect_final"]
    nominal=copy.deepcopy(raw); nominal["tolerance_cases"][0]["nominal_clearance_m"]=0.0003
    controls={"inaccessible_fastener":rejected(lambda:evaluate_handoff(inaccessible),"inaccessible fastener"),"trapped_core":rejected(lambda:evaluate_handoff(trapped),"trapped internal core"),"impossible_order":rejected(lambda:evaluate_handoff(cyclic),"impossible cyclic assembly order"),"nominal_only_fit":rejected(lambda:evaluate_handoff(nominal),"worst-case clearance")}
    dossier={"routes":raw["routes"],"assembly_order":handoff["assembly_order"],"inspection_plan":[{"region_id":item["region_id"],"inspection_access":item["inspection_access"],"status":handoff["route_status"][item["region_id"]]} for item in raw["routes"]],"redesign_or_evidence_blockers":raw["unresolved"]}
    write(output/"manufacturing_dossier.json",dossier); write(output/"tolerance_map.json",handoff["tolerance_results"])
    body={"status":"completed_handoff_blocked","claim_scope":"candidate-route mapping, assembly access and worst-case tolerance accounting over the Work 126 G3 registry; not manufacturing readiness, purchasing, fabrication, or certification","validation":validation,"dependencies":raw["dependencies"],"input_result_sha256":{str(k):v["result_sha256"] for k,v in sorted(inputs.items())},"registry_sha256":raw["registry"]["sha256"],"handoff":handoff,"controls":controls,"artifact_sha256":{"manufacturing_dossier.json":sha(output/"manufacturing_dossier.json"),"tolerance_map.json":sha(output/"tolerance_map.json")},"coverage":raw["coverage"],"unresolved":raw["unresolved"],"decision":{"manufacturing_ready":False,"fabrication_authorized":False,"reason":"all 12 candidate routes remain unknown without qualified process capability and native manufacturing CAD"},"review":{"supporting_evidence":["all 12 registered regions have candidate process and inspection mappings","registered worst-case clearance and preload pass","assembly dependencies are acyclic and access flags pass"],"contradicting_evidence":["no route has measured or qualified process-capability evidence","native manufacturing CAD and physical assembly trial are absent","Work 129 downgraded the critical time claim"],"alternative_explanations":["a named qualified supplier could close some purchased-part gaps","native detailed geometry may reveal new access or tolerance failures"],"missing_evidence":raw["unresolved"],"confidence":"high for registry-level handoff bookkeeping; none for manufacturing readiness"}}
    result={"body":body,"result_sha256":canonical_sha256(body)}; write(output/"result.json",result)
    if args.replay_reference:
        reference=args.replay_reference if args.replay_reference.is_absolute() else ROOT/args.replay_reference; prior=read(reference); exact=prior.get("result_sha256")==result["result_sha256"]; write(output/"replay.json",{"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"],"exact":exact})
        if not exact: raise ManufacturingHandoffViolation("decision replay differs from reference")
    print(json.dumps({"status":body["status"],"result_sha256":result["result_sha256"],"unknown_route_count":handoff["unknown_route_count"],"manufacturing_ready":False},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
