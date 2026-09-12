"""Run Work 132 offline subsystem entry audit only."""
from __future__ import annotations
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/"src"
for x in (ROOT,SRC):
    if str(x) not in sys.path: sys.path.insert(0,str(x))
from formula_ultimate.experiments.physical_subsystem_correlation import PhysicalSubsystemViolation,canonical_sha256,entry_gate,validate_protocol  # noqa:E402
def read(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def write(p,v): p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument("--config",type=Path,required=True);p.add_argument("--output-root",type=Path,required=True);p.add_argument("--replay-reference",type=Path);a=p.parse_args();c=a.config if a.config.is_absolute() else ROOT/a.config;o=a.output_root if a.output_root.is_absolute() else ROOT/a.output_root;raw=read(c);validation=validate_protocol(raw);d=raw["dependency"]
    if sha(ROOT/d["contract_path"])!=d["contract_sha256"] or subprocess.run(["git","cat-file","-e",d["commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise PhysicalSubsystemViolation("stale dependency")
    upstream=read(ROOT/raw["input"]["path"])
    if upstream.get("result_sha256")!=raw["input"]["result_sha256"]: raise PhysicalSubsystemViolation("stale Work 131 result")
    upstream_status="measured_connection_correlation_available" if upstream["body"]["decision"]["measured_connection_correlation_available"] else upstream["body"]["status"]
    gate=entry_gate(raw,upstream_status)
    if gate["ready"]: raise PhysicalSubsystemViolation("unexpected subsystem readiness")
    body={"status":"stopped_missing_authorized_subsystem_evidence","claim_scope":"offline subsystem entry and integrity logic only; no equipment operation, measured endurance, or lifetime claim","validation":validation,"dependency":d,"input_result_sha256":upstream["result_sha256"],"entry_gate":gate,"coverage":raw["coverage"],"decision":{"physical_execution_authorized":False,"subsystem_correlation_available":False,"lifetime_claim":False,"reason":"Work 131 measured applicability and subsystem authorization/configuration/instrument/data records are absent"},"review":{"supporting_evidence":["offline boundary-power replacement leakage abort and sensor controls passed"],"contradicting_evidence":["upstream physical connection work is stopped","no subsystem measurements exist"],"alternative_explanations":["a future separately authorized program may provide valid records"],"missing_evidence":gate["blockers"],"confidence":"high that entry is blocked; none for subsystem endurance"}}
    result={"body":body,"result_sha256":canonical_sha256(body)};write(o/"result.json",result);write(o/"entry_gate.json",gate)
    if a.replay_reference:
        r=a.replay_reference if a.replay_reference.is_absolute() else ROOT/a.replay_reference;prior=read(r);exact=prior.get("result_sha256")==result["result_sha256"];write(o/"replay.json",{"exact":exact,"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"]})
        if not exact: raise PhysicalSubsystemViolation("decision replay differs")
    print(json.dumps({"status":body["status"],"result_sha256":result["result_sha256"],"blocker_count":len(gate["blockers"]),"physical_claim":False},sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
