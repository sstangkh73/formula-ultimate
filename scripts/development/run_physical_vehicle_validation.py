"""Run Work 133 offline whole-vehicle program entry audit only."""
from __future__ import annotations
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/"src"
for x in (ROOT,SRC):
    if str(x) not in sys.path:sys.path.insert(0,str(x))
from formula_ultimate.experiments.physical_vehicle_validation import PhysicalVehicleViolation,canonical_sha256,entry_gate,validate_protocol  # noqa:E402
def read(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def write(p,v):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument("--config",type=Path,required=True);p.add_argument("--output-root",type=Path,required=True);p.add_argument("--replay-reference",type=Path);a=p.parse_args();c=a.config if a.config.is_absolute() else ROOT/a.config;o=a.output_root if a.output_root.is_absolute() else ROOT/a.output_root;raw=read(c);validation=validate_protocol(raw)
    for d in raw["dependencies"]:
        if sha(ROOT/d["contract_path"])!=d["contract_sha256"] or subprocess.run(["git","cat-file","-e",d["commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode:raise PhysicalVehicleViolation("stale dependency")
    inputs={}
    for item in raw["inputs"]:
        v=read(ROOT/item["path"])
        if v.get("result_sha256")!=item["result_sha256"]:raise PhysicalVehicleViolation(f"stale Work {item['work']} result")
        inputs[item["work"]]=v
    prerequisites={"work128_robust_superiority":inputs[128]["body"]["decision"]["robust_superiority_supported"],"work129_selected_claims":inputs[129]["body"]["decision"]["selected_claims_survive"],"work130_manufacturing_ready":inputs[130]["body"]["decision"]["manufacturing_ready"],"work131_connection_correlation":inputs[131]["body"]["decision"]["measured_connection_correlation_available"],"work132_subsystem_correlation":inputs[132]["body"]["decision"]["subsystem_correlation_available"]}
    gate=entry_gate(raw,prerequisites)
    if gate["ready"]:raise PhysicalVehicleViolation("unexpected vehicle readiness")
    body={"status":"stopped_no_physical_vehicle_entry","claim_scope":"offline whole-vehicle staged-program gate only; no vehicle operation, tested scope, safety certification, or superiority claim","validation":validation,"dependencies":raw["dependencies"],"input_result_sha256":{str(k):v["result_sha256"] for k,v in sorted(inputs.items())},"prerequisites":prerequisites,"entry_gate":gate,"coverage":raw["coverage"],"decision":{"vehicle_operation_authorized":False,"physical_vehicle_validated":False,"promotion_allowed":False,"reason":"digital superiority/manufacturing gates and local/subsystem measured evidence are absent, along with vehicle approvals/configuration/plans/telemetry"},"review":{"supporting_evidence":["offline controls cover stage expansion configuration changes incident concealment energy completeness and extrapolation"],"contradicting_evidence":["Works 128-130 do not support promotion or manufacturing readiness","Works 131-132 stopped without measurements","no whole-vehicle authorization or telemetry exists"],"alternative_explanations":["a future professionally reviewed staged program could create new tested-scope evidence"],"missing_evidence":gate["blockers"],"confidence":"high that physical vehicle entry is blocked; none for physical validation"}}
    result={"body":body,"result_sha256":canonical_sha256(body)};write(o/"result.json",result);write(o/"program_entry_gate.json",gate)
    if a.replay_reference:
        r=a.replay_reference if a.replay_reference.is_absolute() else ROOT/a.replay_reference;prior=read(r);exact=prior.get("result_sha256")==result["result_sha256"];write(o/"replay.json",{"exact":exact,"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"]})
        if not exact:raise PhysicalVehicleViolation("decision replay differs")
    print(json.dumps({"status":body["status"],"result_sha256":result["result_sha256"],"blocker_count":len(gate["blockers"]),"physical_vehicle_validated":False},sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
