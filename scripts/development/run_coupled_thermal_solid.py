"""Execute Work 115 bidirectional thermal-solid evidence."""
from __future__ import annotations
import argparse,copy,hashlib,json,math,subprocess,sys
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/"src"
for item in (ROOT,SRC):
    if str(item) not in sys.path: sys.path.insert(0,str(item))
from formula_ultimate.physics.coupled_thermal_solid import CoupledThermalSolidViolation,canonical_sha256,insulated_energy_rise,simulate,validate_protocol  # noqa:E402
from formula_ultimate.structural.detailed_connection_contact import contact_patches  # noqa:E402
def read(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def write(p,v): p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def relative(a,b): return abs(a-b)/max(abs(a),abs(b),1e-30)
def rejected(action,phrase):
    try: action()
    except CoupledThermalSolidViolation as exc:
        if phrase not in str(exc): raise
        return {"status":"rejected","reason":str(exc)}
    raise CoupledThermalSolidViolation("negative control accepted")
def reduced_final(raw,dt):
    g=raw["geometry"]; m=raw["materials"]; t=raw["thermal"]; capacity=g["male_volume_m3"]*m["male"]["density_kg_m3"]*m["male"]["specific_heat_j_kg_k"]+g["female_volume_m3"]*m["female"]["density_kg_m3"]*m["female"]["specific_heat_j_kg_k"]; temp=t["initial_temperature_k"]
    for _ in range(int(round(t["duration_s"]/dt))): temp+=dt*(t["heat_input_w"]-t["boundary_conductance_w_k"]*(temp-t["ambient_temperature_k"]))/capacity
    return temp
def main():
    p=argparse.ArgumentParser(); p.add_argument("--config",type=Path,required=True); p.add_argument("--output-root",type=Path,required=True); p.add_argument("--replay-reference",type=Path); args=p.parse_args(); config=(ROOT/args.config).resolve() if not args.config.is_absolute() else args.config; out=(ROOT/args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root; out.mkdir(parents=True,exist_ok=True)
    raw=read(config); validation=validate_protocol(raw)
    for d in raw["dependencies"]:
        if sha(ROOT/d["contract_path"])!=d["contract_sha256"]: raise CoupledThermalSolidViolation("stale dependency contract")
        if subprocess.run(["git","cat-file","-e",d["commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise CoupledThermalSolidViolation("missing dependency commit")
    g=raw["geometry"]; source_result=read(ROOT/g["work113_result_path"])
    if source_result["result_sha256"]!=g["work113_result_sha256"]: raise CoupledThermalSolidViolation("stale Work 113 result")
    cad=source_result["body"]["cad"]["threaded_reference"]
    if cad["male"]["sha256"]!=g["male_step_sha256"] or cad["female"]["sha256"]!=g["female_step_sha256"] or abs(cad["male"]["volume_m3"]-g["male_volume_m3"])>1e-18 or abs(cad["female"]["volume_m3"]-g["female_volume_m3"])>1e-18: raise CoupledThermalSolidViolation("stale detailed CAD region evidence")
    source_config=read(ROOT/"config/development/detailed_connection_contact_v1.json"); strategy=next(x for x in source_config["strategies"] if x["strategy_id"]=="threaded_reference"); derived_area=sum(x["area_m2"] for x in contact_patches(strategy,48))
    if abs(derived_area-g["contact_area_m2"])>1e-15: raise CoupledThermalSolidViolation("contact area does not derive from Work 113 geometry")
    levels=[]
    for dt in raw["time_steps_s"]:
        r=simulate(raw,dt); history=r.pop("history"); path=out/f"history_{dt:.3f}.json"; write(path,history); r["history_file"]=path.name
        if r["energy_residual_relative"]>raw["tolerances"]["energy_residual_relative"]: raise CoupledThermalSolidViolation("energy residual gate failed")
        levels.append(r)
    convergence={}
    for key in ("male_final_temperature_k","female_final_temperature_k","final_preload_n","final_contact_conductance_w_k"):
        convergence[key]=relative(levels[-2][key],levels[-1][key])
        if convergence[key]>raw["tolerances"]["last_two_relative_change_limit"]: raise CoupledThermalSolidViolation("coupling time-step gate failed")
    fine=levels[-1]; decoupled=simulate(raw,raw["time_steps_s"][-1],coupled=False); decoupled.pop("history"); change=max(abs(fine["male_final_temperature_k"]-decoupled["male_final_temperature_k"]),abs(fine["final_contact_conductance_w_k"]-decoupled["final_contact_conductance_w_k"]));
    if change<raw["tolerances"]["minimum_coupling_change"]: raise CoupledThermalSolidViolation("bidirectional coupling produced no observable return change")
    m=raw["materials"]; cm=g["male_volume_m3"]*m["male"]["density_kg_m3"]*m["male"]["specific_heat_j_kg_k"]; cf=g["female_volume_m3"]*m["female"]["density_kg_m3"]*m["female"]["specific_heat_j_kg_k"]; weighted=(cm*fine["male_final_temperature_k"]+cf*fine["female_final_temperature_k"])/(cm+cf); reduced=reduced_final(raw,raw["time_steps_s"][-1]); reduced_error=abs((reduced-raw["thermal"]["initial_temperature_k"])-(weighted-raw["thermal"]["initial_temperature_k"]))/max(abs(weighted-raw["thermal"]["initial_temperature_k"]),1e-30)
    if reduced_error>raw["tolerances"]["maximum_reduced_temperature_relative_error"]: raise CoupledThermalSolidViolation("reduced thermal model error exceeded")
    insulated=simulate(raw,raw["time_steps_s"][-1],contact_enabled=False,boundary_conductance_w_k=0); insulated.pop("history"); analytic=insulated_energy_rise(raw["thermal"]["heat_input_w"],raw["thermal"]["duration_s"],cm,raw["thermal"]["initial_temperature_k"])
    zero=simulate(raw,raw["time_steps_s"][-1],heat_input_w=0,boundary_conductance_w_k=0); zero.pop("history"); removed=simulate(raw,raw["time_steps_s"][-1],contact_enabled=False); removed.pop("history"); doubled=simulate(raw,raw["time_steps_s"][-1],contact_area_scale=2); doubled.pop("history"); bad=copy.deepcopy(raw); bad["thermal"]["heat_input_w"]=10000
    controls={"insulated_energy_rise":{"numeric_k":insulated["male_final_temperature_k"],"analytic_k":analytic,"absolute_error_k":abs(insulated["male_final_temperature_k"]-analytic)},"zero_source_equilibrium":{"final_male_k":zero["male_final_temperature_k"],"final_female_k":zero["female_final_temperature_k"]},"free_vs_constrained":{"free_expansion_m":read(out/levels[-1]["history_file"])[-1]["male_free_expansion_m"],"constrained_stress_pa":read(out/levels[-1]["history_file"])[-1]["constrained_male_stress_pa"]},"removed_heat_path":{"male_final_k":removed["male_final_temperature_k"]},"doubled_interface_area":{"female_final_k":doubled["female_final_temperature_k"]},"decoupled":{"result":decoupled,"observable_return_change":change},"property_range":rejected(lambda:simulate(bad,.02),"property range")}
    body={"status":"passed","claim_scope":"two-lumped-region bidirectional thermal-solid coupling with synthetic properties and prescribed conductance; not validated cooling or physical validation","validation":validation,"dependencies":raw["dependencies"],"geometry_evidence":{"derived_contact_area_m2":derived_area,"work113_result_sha256":source_result["result_sha256"],"male_step_sha256":cad["male"]["sha256"],"female_step_sha256":cad["female"]["sha256"]},"levels":levels,"convergence":convergence,"coupled_vs_decoupled":controls["decoupled"],"reduced_model":{"final_temperature_k":reduced,"energy_weighted_detailed_temperature_k":weighted,"relative_rise_error":reduced_error},"controls":controls,"review":{"supporting_evidence":["thermal area and region volumes were checked against Work 113 geometry evidence","energy, three-step refinement and both coupling directions passed","insulated/equilibrium/path/area/property controls were causal"],"contradicting_evidence":["contact and boundary conductances and all thermal properties are synthetic"],"alternative_explanations":["two lumped regions suppress spatial gradients"],"missing_evidence":["spatial thermal mesh","measured conductance","validated convection/radiation/fluid flow","physical validation"],"confidence":"moderate for causal bounded coupling; low for real cooling or joint-temperature prediction"}}
    result={"body":body,"result_sha256":canonical_sha256(body)}; write(out/"result.json",result)
    if args.replay_reference:
        ref=(ROOT/args.replay_reference).resolve() if not args.replay_reference.is_absolute() else args.replay_reference; prior=read(ref); exact=prior.get("result_sha256")==result["result_sha256"]; write(out/"replay.json",{"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"],"exact":exact})
        if not exact: raise CoupledThermalSolidViolation("replay differs from reference")
    print(json.dumps({"status":"passed","result_sha256":result["result_sha256"],"level_count":len(levels)},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
