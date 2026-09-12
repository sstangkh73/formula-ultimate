"""Execute Work 114 moving contact assembly evidence."""
from __future__ import annotations
import argparse,copy,hashlib,json,subprocess,sys
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/"src"
for item in (ROOT,SRC):
    if str(item) not in sys.path: sys.path.insert(0,str(item))
from formula_ultimate.assembly.moving_contact_assembly import MovingAssemblyViolation,canonical_sha256,free_rigid_motion,simulate,validate_protocol  # noqa:E402
from formula_ultimate.structural.detailed_connection_contact import evaluate  # noqa:E402
def read(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def write(p,v): p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def relative(a,b): return abs(a-b)/max(abs(a),abs(b),1e-30)
def rejected(action,phrase):
    try: action()
    except MovingAssemblyViolation as exc:
        if phrase not in str(exc): raise
        return {"status":"rejected","reason":str(exc)}
    raise MovingAssemblyViolation("negative control accepted")
def main():
    p=argparse.ArgumentParser(); p.add_argument("--config",type=Path,required=True); p.add_argument("--output-root",type=Path,required=True); p.add_argument("--replay-reference",type=Path); args=p.parse_args(); config=(ROOT/args.config).resolve() if not args.config.is_absolute() else args.config; out=(ROOT/args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root; out.mkdir(parents=True,exist_ok=True)
    raw=read(config); validation=validate_protocol(raw); d=raw["dependency"]
    if sha(ROOT/d["contract_path"])!=d["contract_sha256"]: raise MovingAssemblyViolation("stale Work 113 contract")
    if subprocess.run(["git","cat-file","-e",d["work113_commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise MovingAssemblyViolation("missing Work 113 commit")
    source=read(ROOT/d["source_config"]); strategy=next(x for x in source["strategies"] if x["strategy_id"]==d["strategy_id"]); a=source["acceptance"]; joint=evaluate(strategy,source["material"],source["contact"],source["task"],patch_count=source["refinement_patch_counts"][-1],preload_n=a["baseline_preload_n"],friction=a["baseline_friction"],clearance_m=a["baseline_clearance_m"])
    for key,field in (("normal_stiffness_n_m","normal_stiffness_n_m"),("tangent_stiffness_n_m","tangent_stiffness_n_m"),("preload_n","baseline_preload_n"),("friction","baseline_friction")):
        expected=a[field] if field in a else joint[field]
        if abs(raw["assembly"][key]-expected)>1e-9*max(abs(expected),1): raise MovingAssemblyViolation("stale Work 113 reduced joint value")
    levels=[]
    for dt in raw["time_steps_s"]:
        result=simulate(raw["assembly"],raw["motion"],dt); history=result.pop("history"); path=out/f"history_{dt:.9f}.json"; write(path,history); result["history_file"]=path.name
        if result["status"]!="passed" or result["constraint_drift_m"]>raw["tolerances"]["constraint_drift_m"] or result["minimum_swept_clearance_m"]<raw["tolerances"]["minimum_swept_clearance_m"] or result["energy_residual_relative"]>raw["tolerances"]["energy_residual_relative"]: raise MovingAssemblyViolation("motion clearance, constraint, or energy gate failed")
        levels.append(result)
    convergence={}
    for key in ("maximum_abs_position_m","maximum_contact_force_n","transmitted_normal_impulse_n_s"):
        convergence[key]=relative(levels[-2][key],levels[-1][key])
        if convergence[key]>raw["tolerances"]["last_two_relative_change_limit"]: raise MovingAssemblyViolation("time-step refinement gate failed")
    free=free_rigid_motion(.01,2.,.0005,raw["time_steps_s"][-1]); collision={**raw["assembly"],"swept_clearance_m":1e-8}; collision_result=simulate(collision,raw["motion"],raw["time_steps_s"][-1]); finest_history=read(out/levels[-1]["history_file"]); outside=any((not row["contact"]) or row["slip"] for row in finest_history)
    if free["error_m"]>1e-15 or collision_result["status"]!="blocked_collision" or not outside: raise MovingAssemblyViolation("falsification control failed")
    controls={"free_rigid_motion":{"status":"passed",**free},"rigid_moving_conflict":rejected(lambda:simulate(raw["assembly"],raw["motion"],raw["time_steps_s"][0],allowed_motion="rigid"),"incompatible"),"severed_coupling":rejected(lambda:simulate(raw["assembly"],raw["motion"],raw["time_steps_s"][0],joint_present=False),"severed"),"collision":{"status":"blocked_locally","minimum_swept_clearance_m":collision_result["minimum_swept_clearance_m"]},"reduced_range":{"status":"invalid_outside_registered_stick_contact","opening_or_slip_observed":outside},"reactions":{"status":"computed_from_penetration_history","finest_history_sha256":levels[-1]["history_sha256"]}}
    body={"status":"passed","claim_scope":"bounded axial dynamic and prescribed tangential contact-history evidence; not full multibody/flexible dynamics or physical validation","validation":validation,"dependency":d,"levels":levels,"convergence":convergence,"controls":controls,"review":{"supporting_evidence":["three time steps preserved computed contact/reaction histories and passed registered gates","opening/slip/reversal events and swept clearance were evaluated across motion","rigid conflict, severed path and collision failed locally"],"contradicting_evidence":["tangential motion is prescribed rather than dynamically coupled"],"alternative_explanations":["regular penalty contact and strong damping simplify the response"],"missing_evidence":["flexible modes","general 3D collision/contact","measured dynamics","physical validation"],"confidence":"moderate for the admitted two-coordinate history; low for vehicle-scale dynamics"}}
    result={"body":body,"result_sha256":canonical_sha256(body)}; write(out/"result.json",result)
    if args.replay_reference:
        ref=(ROOT/args.replay_reference).resolve() if not args.replay_reference.is_absolute() else args.replay_reference; prior=read(ref); exact=prior.get("result_sha256")==result["result_sha256"]; write(out/"replay.json",{"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"],"exact":exact})
        if not exact: raise MovingAssemblyViolation("replay differs from reference")
    print(json.dumps({"status":"passed","result_sha256":result["result_sha256"],"level_count":len(levels)},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
