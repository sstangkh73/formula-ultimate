"""Execute Work 120 onboard-energy realization evidence."""
from __future__ import annotations
import argparse,copy,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/"src"
for item in (ROOT,SRC):
    if str(item) not in sys.path: sys.path.insert(0,str(item))
from formula_ultimate.subsystems.onboard_energy_realization import OnboardEnergyViolation,canonical_sha256,operate,validate_protocol  # noqa:E402
def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def write(path,value): path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def rejected(action,phrase):
    try: action()
    except OnboardEnergyViolation as exc:
        if phrase not in str(exc): raise
        return {"status":"rejected","reason":str(exc)}
    raise OnboardEnergyViolation("negative control accepted")
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--config",type=Path,required=True); parser.add_argument("--output-root",type=Path,required=True); parser.add_argument("--replay-reference",type=Path); args=parser.parse_args(); config=(ROOT/args.config).resolve() if not args.config.is_absolute() else args.config; out=(ROOT/args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root; out.mkdir(parents=True,exist_ok=True)
    raw=read(config); validation=validate_protocol(raw)
    for dependency in raw["dependencies"]:
        if sha(ROOT/dependency["contract_path"])!=dependency["contract_sha256"]: raise OnboardEnergyViolation("stale dependency contract")
        if subprocess.run(["git","cat-file","-e",dependency["commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise OnboardEnergyViolation("missing dependency commit")
    inputs={}
    for item in raw["inputs"]:
        result=read(ROOT/item["path"])
        if result.get("result_sha256")!=item["result_sha256"]: raise OnboardEnergyViolation(f"stale Work {item['work']} result")
        inputs[item["work"]]=result
    temperature=inputs[115]["body"]["levels"][-1]["male_final_temperature_k"]
    if temperature!=raw["operating_cases"]["initial_temperature_k"]: raise OnboardEnergyViolation("thermal input identity mismatch")
    available_actuation_power=max(x["output_power_w"] for x in inputs[119]["body"]["response_map"])
    nominal_spec=raw["operating_cases"]["nominal"]
    if nominal_spec["requested_output_power_w"]>available_actuation_power: raise OnboardEnergyViolation("nominal energy port exceeds realized actuation map")
    nominal=operate(raw,nominal_spec["requested_output_power_w"],nominal_spec["duration_s"],temperature)
    excessive_spec=raw["operating_cases"]["excessive"]; excessive=operate(raw,excessive_spec["requested_output_power_w"],excessive_spec["duration_s"],temperature)
    thermal_spec=raw["operating_cases"]["thermal"]; thermal=operate(raw,thermal_spec["requested_output_power_w"],thermal_spec["duration_s"],329.0)
    empty=operate(raw,nominal_spec["requested_output_power_w"],60,temperature,initial_fraction=0); disconnected=operate(raw,nominal_spec["requested_output_power_w"],60,temperature,connected=False)
    for case in (nominal,excessive,thermal,empty,disconnected):
        if abs(case["energy_residual_j"])>raw["tolerances"]["energy_residual_absolute_j"]: raise OnboardEnergyViolation("energy residual gate failed")
    if nominal["state"]!="admitted" or excessive["state"]!="rate_limited" or thermal["state"]!="thermal_limited" or empty["state"]!="empty" or disconnected["state"]!="disconnected": raise OnboardEnergyViolation("limiting-state control failed")
    omitted=copy.deepcopy(raw); del omitted["hardware"]["containment"]; bad_boundary=copy.deepcopy(raw); bad_boundary["energy_boundary"]["external_replenishment"]="allowed"
    controls={"empty_storage":empty,"excessive_demand":excessive,"disconnected_converter":disconnected,"thermal_limit":thermal,"omitted_containment":rejected(lambda:validate_protocol(omitted),"containment"),"hidden_replenishment":rejected(lambda:operate(raw,8000,60,temperature,external_replenishment_w=1),"replenishment"),"energy_boundary":rejected(lambda:validate_protocol(bad_boundary),"boundary")}
    body={"status":"passed","claim_scope":"one synthetic stored-electric/DC onboard energy route with geometry-derived hardware mass and closed state/loss ledger; not chemistry safety, build authorization, technology superiority, or physical validation","validation":validation,"dependencies":raw["dependencies"],"input_result_sha256":{str(k):v["result_sha256"] for k,v in sorted(inputs.items())},"upstream":{"work115_temperature_k":temperature,"work116_material_claim":inputs[116]["body"]["candidate"]["claim_eligibility"],"work119_available_output_power_w":available_actuation_power,"work119_hardware_mass_kg":inputs[119]["body"]["validation"]["hardware_mass_kg"]},"nominal":nominal,"controls":controls,"coverage":raw["coverage"],"review":{"supporting_evidence":["active, enclosure, insulation, connector, mount and converter masses derive from registered geometry or counted hardware","stored-energy decrease equals delivered energy plus conversion and connector loss","empty, rate, thermal, disconnection, containment, replenishment and boundary controls were causal"],"contradicting_evidence":["storage, conversion and thermal properties are synthetic"],"alternative_explanations":["lumped adiabatic temperature rise omits spatial gradients and heat rejection"],"missing_evidence":["chemistry and containment safety","measured capacity/rate/efficiency","aging and fault propagation","physical validation"],"confidence":"high for deterministic mass/energy bookkeeping; none for real storage safety or performance"}}
    result={"body":body,"result_sha256":canonical_sha256(body)}; write(out/"result.json",result)
    if args.replay_reference:
        reference=(ROOT/args.replay_reference).resolve() if not args.replay_reference.is_absolute() else args.replay_reference; prior=read(reference); exact=prior.get("result_sha256")==result["result_sha256"]; write(out/"replay.json",{"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"],"exact":exact})
        if not exact: raise OnboardEnergyViolation("replay differs from reference")
    print(json.dumps({"status":"passed","result_sha256":result["result_sha256"],"complete_mass_kg":validation["assembly"]["complete_mass_kg"],"usable_capacity_j":validation["assembly"]["usable_capacity_j"]},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
