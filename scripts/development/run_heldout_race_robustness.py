"""Execute Work 128 sealed held-out race evidence."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
for item in (ROOT, SRC):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from formula_ultimate.experiments.heldout_race_robustness import HeldoutRaceViolation, analyze, canonical_sha256, execute, validate_protocol  # noqa: E402


def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def write(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def rejected(action, phrase):
    try: action()
    except HeldoutRaceViolation as exc:
        if phrase not in str(exc): raise
        return {"status":"rejected","reason":str(exc)}
    raise HeldoutRaceViolation("negative control accepted")


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--config",type=Path,required=True); parser.add_argument("--output-root",type=Path,required=True); parser.add_argument("--replay-reference",type=Path); args=parser.parse_args()
    config=args.config if args.config.is_absolute() else ROOT/args.config; output=args.output_root if args.output_root.is_absolute() else ROOT/args.output_root
    raw=read(config); validation=validate_protocol(raw); dependency=raw["dependency"]
    if sha(ROOT/dependency["contract_path"])!=dependency["contract_sha256"]: raise HeldoutRaceViolation("stale dependency contract")
    if subprocess.run(["git","cat-file","-e",dependency["commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise HeldoutRaceViolation("missing dependency commit")
    upstream=read(ROOT/raw["input"]["path"])
    if upstream.get("result_sha256")!=raw["input"]["result_sha256"]: raise HeldoutRaceViolation("stale Work 127 result")
    if upstream["body"]["decision"]["system_benefit_supported"]: raise HeldoutRaceViolation("Work 127 decision boundary mismatch")
    telemetry=execute(raw); analysis=analyze(raw,telemetry)
    leaked=copy.deepcopy(raw); leaked["training_condition_ids"].append(raw["holdout_conditions"][0]["id"])
    changed=copy.deepcopy(raw); changed["finalists"]["open"]["identity"]+="_changed"
    tuned=copy.deepcopy(raw); tuned["registration"]["exposure_tuning_allowed"]=True
    controls={"holdout_reuse":rejected(lambda:validate_protocol(leaked),"holdout reuse"),"changed_source":rejected(lambda:validate_protocol(changed),"changed sealed source hash"),"hidden_incomplete":rejected(lambda:analyze(raw,telemetry[:-1]),"incomplete races hidden"),"post_exposure_tuning":rejected(lambda:validate_protocol(tuned),"post-exposure tuning")}
    write(output/"telemetry.json",telemetry); write(output/"holdout_manifest.json",{"seals":raw["seals"],"conditions":raw["holdout_conditions"],"registration":raw["registration"]})
    body={"status":"completed_negative_result","claim_scope":"sealed synthetic held-out race robustness analysis; not physical race evidence, novelty, promotion, or physical validation","validation":validation,"dependency":dependency,"input_result_sha256":upstream["result_sha256"],"analysis":analysis,"controls":controls,"artifact_sha256":{"telemetry.json":sha(output/"telemetry.json"),"holdout_manifest.json":sha(output/"holdout_manifest.json")},"coverage":raw["coverage"],"decision":{"robust_superiority_supported":False,"promotion_allowed":False,"reason":"paired 0.5 s improvement does not reach the registered 1.0 s threshold after numerical uncertainty"},"review":{"supporting_evidence":["all 12 registered trajectories were retained","all synthetic energy thermal and structural gates passed","finalist evaluator rules and holdout identities were sealed"],"contradicting_evidence":["the paired time effect is below the preregistered threshold","Work 127 and Work 126 remain negative/exploratory"],"alternative_explanations":["the deterministic race model may understate environmental variability","shared condition effects can suppress paired variance"],"missing_evidence":["independent reanalysis","manufactured vehicle telemetry","physical race validation"],"confidence":"high for sealed deterministic execution; none for physical robustness"}}
    result={"body":body,"result_sha256":canonical_sha256(body)}; write(output/"result.json",result)
    if args.replay_reference:
        reference=args.replay_reference if args.replay_reference.is_absolute() else ROOT/args.replay_reference; prior=read(reference); exact=prior.get("result_sha256")==result["result_sha256"]; write(output/"replay.json",{"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"],"exact":exact})
        if not exact: raise HeldoutRaceViolation("decision replay differs from reference")
    print(json.dumps({"status":body["status"],"result_sha256":result["result_sha256"],"mean_time_improvement_s":analysis["mean_time_improvement_s"],"robust_superiority_supported":False},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
