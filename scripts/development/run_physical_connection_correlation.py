"""Run Work 131 offline entry and evidence audit only."""
from __future__ import annotations
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/"src"
for item in (ROOT,SRC):
    if str(item) not in sys.path: sys.path.insert(0,str(item))
from formula_ultimate.experiments.physical_connection_correlation import PhysicalConnectionCorrelationViolation,canonical_sha256,entry_gate,offline_stop,validate_protocol  # noqa:E402
def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def write(path,value): path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser(); p.add_argument("--config",type=Path,required=True); p.add_argument("--output-root",type=Path,required=True); p.add_argument("--replay-reference",type=Path); a=p.parse_args(); config=a.config if a.config.is_absolute() else ROOT/a.config; out=a.output_root if a.output_root.is_absolute() else ROOT/a.output_root
    raw=read(config); validation=validate_protocol(raw)
    for d in raw["dependencies"]:
        if sha(ROOT/d["contract_path"])!=d["contract_sha256"]: raise PhysicalConnectionCorrelationViolation("stale dependency contract")
        if subprocess.run(["git","cat-file","-e",d["commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise PhysicalConnectionCorrelationViolation("missing dependency commit")
    inputs={}
    for item in raw["inputs"]:
        value=read(ROOT/item["path"])
        if value.get("result_sha256")!=item["result_sha256"]: raise PhysicalConnectionCorrelationViolation(f"stale Work {item['work']} result")
        inputs[item["work"]]=value
    gate=entry_gate(raw); stop_controls={"overload":offline_stop({"load_n":1001,"temperature_k":300,"sensor_saturated":False},raw["registration"]),"overtemperature":offline_stop({"load_n":1,"temperature_k":331,"sensor_saturated":False},raw["registration"]),"saturation":offline_stop({"load_n":1,"temperature_k":300,"sensor_saturated":True},raw["registration"])}
    if gate["ready"]: raise PhysicalConnectionCorrelationViolation("unexpected physical readiness without supplied measured package")
    body={"status":"stopped_missing_entry_permissions_and_data","claim_scope":"validated offline entry/integrity/stop logic only; no equipment operation and no physical correlation claim","validation":validation,"dependencies":raw["dependencies"],"input_result_sha256":{str(k):v["result_sha256"] for k,v in sorted(inputs.items())},"entry_gate":gate,"stop_logic_controls":stop_controls,"coverage":raw["coverage"],"decision":{"physical_execution_authorized":False,"measured_connection_correlation_available":False,"extrapolation_allowed":False,"reason":"qualified approvals, facility/operator references, inspected specimens, calibration manifests and immutable measured observations are absent"},"review":{"supporting_evidence":["offline integrity checks and stop logic passed unit controls"],"contradicting_evidence":["no measured records or entry permission references exist","Work 130 is not manufacturing-ready"],"alternative_explanations":["a future authorized measured package may satisfy the frozen input schema"],"missing_evidence":gate["blockers"],"confidence":"high that entry is blocked; none for physical correlation"}}
    result={"body":body,"result_sha256":canonical_sha256(body)}; write(out/"result.json",result); write(out/"entry_gate.json",gate)
    if a.replay_reference:
        ref=a.replay_reference if a.replay_reference.is_absolute() else ROOT/a.replay_reference; prior=read(ref); exact=prior.get("result_sha256")==result["result_sha256"]; write(out/"replay.json",{"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"],"exact":exact})
        if not exact: raise PhysicalConnectionCorrelationViolation("decision replay differs from reference")
    print(json.dumps({"status":body["status"],"result_sha256":result["result_sha256"],"blocker_count":len(gate["blockers"]),"physical_claim":False},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
