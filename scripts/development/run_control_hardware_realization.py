"""Execute Work 122 control-hardware realization evidence."""
from __future__ import annotations
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/"src"
for item in (ROOT,SRC):
    if str(item) not in sys.path: sys.path.insert(0,str(item))
from formula_ultimate.subsystems.control_hardware_realization import ControlHardwareViolation,canonical_sha256,simulate,tune,validate_protocol  # noqa:E402
def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def write(path,value): path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def compact(result): value=dict(result); value.pop("history",None); return value
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--config",type=Path,required=True); parser.add_argument("--output-root",type=Path,required=True); parser.add_argument("--replay-reference",type=Path); args=parser.parse_args(); config=(ROOT/args.config).resolve() if not args.config.is_absolute() else args.config; out=(ROOT/args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root; out.mkdir(parents=True,exist_ok=True)
    raw=read(config); validation=validate_protocol(raw)
    for dependency in raw["dependencies"]:
        if sha(ROOT/dependency["contract_path"])!=dependency["contract_sha256"]: raise ControlHardwareViolation("stale dependency contract")
        if subprocess.run(["git","cat-file","-e",dependency["commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise ControlHardwareViolation("missing dependency commit")
    inputs={}
    for item in raw["inputs"]:
        result=read(ROOT/item["path"])
        if result.get("result_sha256")!=item["result_sha256"]: raise ControlHardwareViolation(f"stale Work {item['work']} result")
        inputs[item["work"]]=result
    authority=inputs[119]["body"]["bounds"]["maximum_output_torque_n_m"]
    supply=inputs[120]["body"]["nominal"]["initial_stored_energy_j"]
    if raw["models"]["actuator_limit_n_m"]>authority or raw["models"]["available_supply_energy_j"]>supply: raise ControlHardwareViolation("registered authority or supply exceeds upstream evidence")
    common=tune(raw,"common"); adapted=tune(raw,"adapted")
    if common["evaluations"]!=adapted["evaluations"] or common["evaluations"]!=raw["tuning"]["evaluations_per_mode"]: raise ControlHardwareViolation("tuning opportunity is not matched")
    nominal=simulate(raw,adapted["best_gain"]); delayed=simulate(raw,adapted["best_gain"],delay_steps=10); dropout=simulate(raw,adapted["best_gain"],dropout_start_s=1); disconnected=simulate(raw,adapted["best_gain"],signal_connected=False); exhausted=simulate(raw,adapted["best_gain"],supply_energy_j=0); saturated=simulate(raw,1000); causal=simulate(raw,adapted["best_gain"],noncausal_label=0); noncausal=simulate(raw,adapted["best_gain"],noncausal_label=999)
    if abs(delayed["rmse"]-nominal["rmse"])<raw["tolerances"]["minimum_delay_effect"]: raise ControlHardwareViolation("increased delay had no causal effect")
    if causal["trace_sha256"]!=noncausal["trace_sha256"]: raise ControlHardwareViolation("noncausal parameter changed physical trace")
    if not dropout["dropout_count"] or not exhausted["supply_exhausted_steps"] or not saturated["saturation_count"]: raise ControlHardwareViolation("fault or saturation control was not observable")
    for name,result in (("nominal",nominal),("delayed",delayed),("dropout",dropout)):
        write(out/f"{name}_history.json",result["history"])
    controls={"increased_delay":compact(delayed),"sensor_dropout":compact(dropout),"disconnected_signal":compact(disconnected),"exhausted_supply":compact(exhausted),"saturated_actuator":compact(saturated),"noncausal_mutation":{"baseline_trace_sha256":causal["trace_sha256"],"mutated_trace_sha256":noncausal["trace_sha256"],"useful_mutation":False}}
    body={"status":"passed","claim_scope":"bounded synthetic sampled sensor-controller-actuator hardware path with finite authority, energy, noise, delay and matched tuning; not ideal observation, safety certification, or physical validation","validation":validation,"dependencies":raw["dependencies"],"input_result_sha256":{str(k):v["result_sha256"] for k,v in sorted(inputs.items())},"upstream":{"work119_available_torque_n_m":authority,"work120_available_initial_energy_j":supply},"hardware":raw["hardware"],"signal_graph":raw["signal_graph"],"tuning":{"common":common,"adapted":adapted,"matched_evaluations":common["evaluations"]},"nominal":compact(nominal),"controls":controls,"coverage":raw["coverage"],"review":{"supporting_evidence":["sensor, controller, harness, connectors, mounts and actuator interface have explicit mass/power accounting","actuator and supply limits are bounded by exact Work 119/120 evidence","common and adapted modes each used four charged evaluations"],"contradicting_evidence":["plant, sensor noise, latency and all hardware data are synthetic"],"alternative_explanations":["scalar reference dynamics omit multivariable coupling and scheduling"],"missing_evidence":["measured sensors/noise/delay","real electronics and EMI","closed-loop physical tests","safety certification"],"confidence":"high for deterministic accounting/fault controls; none for real controller performance"}}
    result={"body":body,"result_sha256":canonical_sha256(body)}; write(out/"result.json",result)
    if args.replay_reference:
        reference=(ROOT/args.replay_reference).resolve() if not args.replay_reference.is_absolute() else args.replay_reference; prior=read(reference); exact=prior.get("result_sha256")==result["result_sha256"]; write(out/"replay.json",{"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"],"exact":exact})
        if not exact: raise ControlHardwareViolation("replay differs from reference")
    print(json.dumps({"status":"passed","result_sha256":result["result_sha256"],"hardware_mass_kg":validation["hardware_mass_kg"],"best_gain":adapted["best_gain"],"rmse":nominal["rmse"]},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
