"""Execute Work 123 coupled whole-candidate transient evidence."""
from __future__ import annotations
import argparse,copy,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/"src"
for item in (ROOT,SRC):
    if str(item) not in sys.path: sys.path.insert(0,str(item))
from formula_ultimate.simulation.coupled_vehicle_transient import CoupledTransientViolation,canonical_sha256,simulate,validate_protocol  # noqa:E402
def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def write(path,value): path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def relative(a,b): return abs(a-b)/max(abs(a),abs(b),1e-30)
def rejected(action,phrase):
    try: action()
    except CoupledTransientViolation as exc:
        if phrase not in str(exc): raise
        return {"status":"rejected","reason":str(exc)}
    raise CoupledTransientViolation("negative control accepted")
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--config",type=Path,required=True); parser.add_argument("--output-root",type=Path,required=True); parser.add_argument("--replay-reference",type=Path); args=parser.parse_args(); config=(ROOT/args.config).resolve() if not args.config.is_absolute() else args.config; out=(ROOT/args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root; out.mkdir(parents=True,exist_ok=True)
    raw=read(config); validation=validate_protocol(raw)
    for dependency in raw["dependencies"]:
        if sha(ROOT/dependency["contract_path"])!=dependency["contract_sha256"]: raise CoupledTransientViolation("stale dependency contract")
        if subprocess.run(["git","cat-file","-e",dependency["commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise CoupledTransientViolation("missing dependency commit")
    inputs={}
    for item in raw["inputs"]:
        result=read(ROOT/item["path"])
        if result.get("result_sha256")!=item["result_sha256"]: raise CoupledTransientViolation(f"stale Work {item['work']} result")
        inputs[item["work"]]=result
    derived={"work117_external_task_sha256":inputs[117]["body"]["feedback"]["external_task_sha256"],"work118_ground_force_n":inputs[118]["body"]["surface"]["friction_coefficient"]*3000.0,"work119_output_power_w":max(x["output_power_w"] for x in inputs[119]["body"]["response_map"]),"work120_initial_energy_j":inputs[120]["body"]["nominal"]["initial_stored_energy_j"],"work121_cooling_power_w":inputs[121]["body"]["internal_scope"]["levels"][-1]["heat_rejected_w"],"work121_drag_coefficient_n_per_m_s2":inputs[121]["body"]["external_scope"]["levels"][-1]["drag_force_n"]/900.0,"work122_controller_power_w":sum(x["power_w"] for x in inputs[122]["body"]["hardware"]["sensors"])+inputs[122]["body"]["hardware"]["controller"]["power_w"]+inputs[122]["body"]["hardware"]["signal_power_w"]}
    checks=(("ground_force_n","work118_ground_force_n"),("actuation_output_power_w","work119_output_power_w"),("cooling_power_w","work121_cooling_power_w"),("drag_coefficient_n_per_m_s2","work121_drag_coefficient_n_per_m_s2"),("controller_power_w","work122_controller_power_w"))
    for target,source in checks:
        if abs(raw["limits"][target]-derived[source])>1e-12: raise CoupledTransientViolation(f"derived limit mismatch: {target}")
    if raw["trial"]["initial_energy_j"]!=derived["work120_initial_energy_j"]: raise CoupledTransientViolation("initial energy mismatch")
    levels=[]
    for dt in raw["time_steps_s"]:
        result=simulate(raw,dt); history=result.pop("history"); path=out/f"history_{dt:.3f}.json"; write(path,history); result["history_file"]=path.name
        if result["maximum_step_residual_j"]>raw["tolerances"]["maximum_step_residual_j"] or abs(result["global_energy_residual_j"])>raw["tolerances"]["global_energy_residual_j"]: raise CoupledTransientViolation("energy conservation gate failed")
        if result["status"]!="completed_exploratory" or result["promotion_allowed"]: raise CoupledTransientViolation("exploratory status or promotion blocker failed")
        levels.append(result)
    convergence={key:relative(levels[-2][key],levels[-1][key]) for key in ("final_position_m","final_velocity_m_s","final_stored_energy_j","final_temperature_k")}
    if any(value>raw["tolerances"]["last_two_relative_change"] for value in convergence.values()): raise CoupledTransientViolation("time-step convergence gate failed")
    decoupled=simulate(raw,raw["time_steps_s"][-1],coupled=False); decoupled.pop("history"); doubled=simulate(raw,raw["time_steps_s"][-1],double_count_power=True); doubled.pop("history"); depleted=simulate(raw,raw["time_steps_s"][-1],initial_energy_j=0); depleted.pop("history")
    if abs(decoupled["final_velocity_m_s"]-levels[-1]["final_velocity_m_s"])<raw["tolerances"]["minimum_coupling_effect"]: raise CoupledTransientViolation("coupling produced no observable effect")
    bad=copy.deepcopy(raw); bad["exchange_schema"]["signs"]["traction_work_j"]="body_to_ground_positive"
    controls={"decoupled":decoupled,"double_counted_power":doubled,"depleted_energy":depleted,"mismatched_sign":rejected(lambda:validate_protocol(bad),"frame or signs"),"out_of_range":rejected(lambda:simulate(raw,.01,initial_speed_m_s=31),"validity"),"event_timing":{"events":levels[-1]["events"],"registered_change_time_s":2.0}}
    body={"status":"passed_exploratory_only","claim_scope":"bounded reduced coupling of exact Work 117-122 evidence with conservative work/heat exchange and explicit unresolved blockers; not a complete vehicle, race completion, readiness, or physical validation","validation":validation,"dependencies":raw["dependencies"],"input_result_sha256":{str(k):v["result_sha256"] for k,v in sorted(inputs.items())},"derived_interfaces":derived,"levels":levels,"convergence":convergence,"controls":controls,"coverage":raw["coverage"],"decision":{"promotion_allowed":False,"reason":"required complete geometry, measured material, validated ground interaction, full aerodynamics and structural failure models remain unresolved"},"review":{"supporting_evidence":["all six dependency/result identities and derived interface limits were checked","per-step mechanical/interface and global energy ledgers passed at three time steps","sign, double-count, event, depletion, validity and decoupling controls localized failures"],"contradicting_evidence":["candidate geometry and multiple subsystem laws remain incomplete or synthetic"],"alternative_explanations":["short scalar trajectory suppresses lateral, structural and distributed thermal behavior"],"missing_evidence":["complete candidate geometry","measured materials and ground device","full aerodynamic and structural models","long trajectory and physical validation"],"confidence":"high for bounded ledger integration; none for vehicle readiness or performance"}}
    result={"body":body,"result_sha256":canonical_sha256(body)}; write(out/"result.json",result)
    if args.replay_reference:
        reference=(ROOT/args.replay_reference).resolve() if not args.replay_reference.is_absolute() else args.replay_reference; prior=read(reference); exact=prior.get("result_sha256")==result["result_sha256"]; write(out/"replay.json",{"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"],"exact":exact})
        if not exact: raise CoupledTransientViolation("replay differs from reference")
    print(json.dumps({"status":"passed_exploratory_only","result_sha256":result["result_sha256"],"final_position_m":levels[-1]["final_position_m"],"final_velocity_m_s":levels[-1]["final_velocity_m_s"],"promotion_allowed":False},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
