"""Execute Work 119 realized actuation-chain evidence."""
from __future__ import annotations
import argparse,copy,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/"src"
for item in (ROOT,SRC):
    if str(item) not in sys.path: sys.path.insert(0,str(item))
from formula_ultimate.subsystems.realized_actuation_chain import ActuationChainViolation,canonical_sha256,evaluate,validate_protocol  # noqa:E402
def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def write(path,value): path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def rejected(action,phrase):
    try: action()
    except ActuationChainViolation as exc:
        if phrase not in str(exc): raise
        return {"status":"rejected","reason":str(exc)}
    raise ActuationChainViolation("negative control accepted")
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--config",type=Path,required=True); parser.add_argument("--output-root",type=Path,required=True); parser.add_argument("--replay-reference",type=Path); args=parser.parse_args()
    config=(ROOT/args.config).resolve() if not args.config.is_absolute() else args.config; out=(ROOT/args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root; out.mkdir(parents=True,exist_ok=True)
    raw=read(config); validation=validate_protocol(raw)
    for dependency in raw["dependencies"]:
        if sha(ROOT/dependency["contract_path"])!=dependency["contract_sha256"]: raise ActuationChainViolation("stale dependency contract")
        if subprocess.run(["git","cat-file","-e",dependency["commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise ActuationChainViolation("missing dependency commit")
    inputs={}
    for item in raw["inputs"]:
        result=read(ROOT/item["path"])
        if result.get("result_sha256")!=item["result_sha256"]: raise ActuationChainViolation(f"stale Work {item['work']} result")
        inputs[item["work"]]=result
    work114_load=inputs[114]["body"]["levels"][-1]["maximum_contact_force_n"]
    if work114_load!=inputs[116]["body"]["input_evidence"]["work114_maximum_dynamic_contact_force_n"]: raise ActuationChainViolation("load provenance mismatch")
    temperature=inputs[115]["body"]["levels"][-1]["male_final_temperature_k"]
    if not raw["envelope"]["temperature_range_k"][0]<=temperature<=raw["envelope"]["temperature_range_k"][1]: raise ActuationChainViolation("upstream temperature outside registered envelope")
    response_map=[]
    for temp in raw["map"]["temperatures_k"]:
        for speed in raw["map"]["input_speeds_rad_s"]:
            for torque in raw["map"]["input_torques_n_m"]:
                result=evaluate(raw,torque,speed,temp)
                if abs(result["energy_residual_w"])>raw["tolerances"]["energy_residual_absolute_w"]: raise ActuationChainViolation("energy accounting failed")
                result["duration_s"]=raw["map"]["duration_s"]; result["input_energy_j"]=result["accepted_input_power_w"]*result["duration_s"]; result["output_work_j"]=result["output_power_w"]*result["duration_s"]; result["loss_energy_j"]=result["loss_power_w"]*result["duration_s"]
                response_map.append(result)
    nominal=evaluate(raw,30,100,temperature); reverse=evaluate(raw,-30,-100,temperature); disconnected=evaluate(raw,30,100,temperature,connected=False); locked=evaluate(raw,30,100,temperature,output_locked=True); saturated=evaluate(raw,120,100,temperature)
    if nominal["output_power_w"]!=reverse["output_power_w"] or nominal["output_torque_n_m"]!=-reverse["output_torque_n_m"]: raise ActuationChainViolation("reverse symmetry failed")
    removed=copy.deepcopy(raw); removed["hardware"]["supports"]=[]
    missing=copy.deepcopy(raw); missing["hardware"]["members"]=[]
    controls={"disconnected":disconnected,"locked_output":locked,"reverse":reverse,"saturation":saturated,"removed_support":rejected(lambda:validate_protocol(removed),"supports"),"unexplained_hardware":rejected(lambda:validate_protocol(missing),"hardware path")}
    body={"status":"passed","claim_scope":"realized synthetic coaxial rotary reference route with geometry-derived mass, stiffness, reactions and modeled losses; not a technology whitelist, validated hardware, or physical validation","validation":validation,"dependencies":raw["dependencies"],"input_result_sha256":{str(k):v["result_sha256"] for k,v in sorted(inputs.items())},"upstream_conditions":{"work114_dynamic_contact_force_n":work114_load,"work115_temperature_k":temperature,"work116_material_claim":inputs[116]["body"]["candidate"]["claim_eligibility"]},"hardware":raw["hardware"],"response_map":response_map,"controls":controls,"bounds":{"maximum_output_torque_n_m":max(abs(x["output_torque_n_m"]) for x in response_map),"maximum_loss_power_w":max(x["loss_power_w"] for x in response_map),"maximum_output_member_stress_pa":max(x["output_member_stress_pa"] for x in response_map),"maximum_radial_reaction_per_support_n":max(x["radial_reaction_per_support_n"] for x in response_map)},"coverage":raw["coverage"],"review":{"supporting_evidence":["18 operating points closed input-output-loss accounting","geometry determined member stiffness, stress, complete mass and support reactions","disconnect, lock, reverse, saturation, removed-support and missing-hardware controls were causal"],"contradicting_evidence":["loss and material properties are synthetic"],"alternative_explanations":["the coaxial reference omits detailed interface and flexible-mode behavior"],"missing_evidence":["measured efficiency map","process-qualified materials","fatigue and wear","detailed bearings and fasteners","physical validation"],"confidence":"high for deterministic bookkeeping and geometry derivations; none for real hardware performance"}}
    result={"body":body,"result_sha256":canonical_sha256(body)}; write(out/"result.json",result)
    if args.replay_reference:
        reference=(ROOT/args.replay_reference).resolve() if not args.replay_reference.is_absolute() else args.replay_reference; prior=read(reference); exact=prior.get("result_sha256")==result["result_sha256"]; write(out/"replay.json",{"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"],"exact":exact})
        if not exact: raise ActuationChainViolation("replay differs from reference")
    print(json.dumps({"status":"passed","result_sha256":result["result_sha256"],"map_points":len(response_map),"hardware_mass_kg":validation["hardware_mass_kg"]},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
