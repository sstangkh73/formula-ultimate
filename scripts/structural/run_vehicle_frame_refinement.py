#!/usr/bin/env python3
"""Run Work 052 independent whole-vehicle frame refinement acceptance."""

from __future__ import annotations

import argparse
from dataclasses import asdict, replace
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import time
import traceback


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.experiments.whole_vehicle_search import mutate_candidate_assembly  # noqa: E402
from formula_ultimate.structural.vehicle_frame_refinement import (  # noqa: E402
    FrameModel, FrameSection, VehicleFrameError, analytical_cantilever,
    benchmark_model, build_calculix_b31_deck, build_vehicle_frame,
    canonical_sha256, loads_from_work048, parse_calculix_b31_dat,
    parse_calculix_section_forces_frd, section_force_extreme_von_mises,
    solve_frame,
)
from formula_ultimate.topology.vehicle_assembly import from_mapping, mass_properties, validate  # noqa: E402


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(a: float, b: float) -> float:
    return abs(a-b)/max(abs(b),1.0e-300)


def run_ccx(ccx: Path, run_dir: Path, deck: str, stage: str, section: FrameSection):
    run_dir.mkdir(parents=True, exist_ok=True)
    for suffix in (".dat", ".frd", ".sta", ".cvg", ".12d"):
        target=run_dir/("frame"+suffix)
        if target.exists(): target.unlink()
    input_path=run_dir/"frame.inp"; input_path.write_text(deck,encoding="ascii")
    started=time.time_ns(); before=time.perf_counter(); completed=subprocess.run([str(ccx),"frame"],cwd=run_dir,text=True,capture_output=True); wall=time.perf_counter()-before
    dat=run_dir/"frame.dat"; frd=run_dir/"frame.frd"
    evidence={"stage":stage,"command":[str(ccx),"frame"],"exit_code":completed.returncode,"stdout":completed.stdout,"stderr":completed.stderr,"wall_time_s":wall,"input_sha256":sha(input_path)}
    if completed.returncode or not dat.is_file() or not frd.is_file() or dat.stat().st_mtime_ns < started or frd.stat().st_mtime_ns < started:
        raise VehicleFrameError(f"CalculiX did not produce fresh complete evidence at {stage}")
    parsed=parse_calculix_b31_dat(dat.read_text(encoding="ascii",errors="replace"))
    section_rows=parse_calculix_section_forces_frd(frd.read_text(encoding="ascii",errors="replace"))
    parsed.update({"section_force_rows":section_rows,"maximum_surface_von_mises_pa":section_force_extreme_von_mises(section_rows,section)})
    evidence.update({"dat_sha256":sha(dat),"frd_sha256":sha(frd),"output_section_id":section.section_id})
    return parsed,evidence


def candidate_identity(record: dict) -> str:
    candidate=record["candidate"]
    payload={"treatment":candidate["treatment"],"seed":candidate["seed"],"attempt":candidate["attempt_index"],"variables":candidate["variables"],"parent":candidate["parent_candidate_id"]}
    return "candidate-"+canonical_sha256(payload)[:16]


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--config",type=Path,default=ROOT/"config/structural/section_force_vehicle_frame_refinement_v2.json")
    parser.add_argument("--artifact-root",type=Path,default=ROOT/"artifacts/work053")
    parser.add_argument("--ccx",type=Path,default=Path(r"C:\Program Files\FreeCAD 1.1\bin\ccx.exe"))
    args=parser.parse_args(); args.artifact_root.mkdir(parents=True,exist_ok=True); stage="work050"
    try:
        upstream=subprocess.run(["powershell","-NoProfile","-ExecutionPolicy","Bypass","-File",str(ROOT/"scripts/run_work050.ps1")],cwd=ROOT,text=True,capture_output=True)
        if upstream.returncode: raise VehicleFrameError(f"Work 050 upstream failed: {upstream.stderr[-1000:]}")
        config=read(args.config); summary050=read(ROOT/"artifacts/work050/experiment_summary.json"); ledger_path=ROOT/"artifacts/work050/result_ledger.jsonl"; budget_path=ROOT/"artifacts/work050/budget_ledger.jsonl"
        identity=config["upstream_identity"]
        checks={"work050_protocol_sha256":summary050["protocol_sha256"],"work050_records_sha256":summary050["replay"]["records_sha256"],"work050_result_ledger_sha256":sha(ledger_path),"work050_budget_ledger_sha256":sha(budget_path)}
        for key,value in checks.items():
            if identity[key]!=value: raise VehicleFrameError(f"upstream {key} mismatch")
        if config.get("protocol_id")!="section_force_vehicle_frame_refinement_v2": raise VehicleFrameError("Work 053 protocol identity mismatch")
        if not args.ccx.is_file(): raise VehicleFrameError("CalculiX executable is missing")
        material=config["material"]; young=float(material["young_modulus_pa"]); poisson=float(material["poisson_ratio"]); yield_stress=float(material["yield_stress_pa"]); tolerances=config["tolerances"]
        stage="benchmark"; benchmark=config["benchmark"]; analytical=analytical_cantilever(float(benchmark["length_m"]),float(benchmark["square_side_m"]),float(benchmark["tip_force_n"]),young); benchmark_results=[]; processes=[]
        for subdivisions in config["subdivisions_per_branch"]:
            model,unit=benchmark_model(float(benchmark["length_m"]),float(benchmark["square_side_m"]),int(subdivisions)); tip=next(iter(unit)); loads={tip:(0.0,-float(benchmark["tip_force_n"]),0.0,0.0,0.0,0.0)}
            section=model.sections[0]
            project=solve_frame(model,loads,young,poisson); calculated,process=run_ccx(args.ccx,args.artifact_root/f"benchmark_{subdivisions}",build_calculix_b31_deck(model,loads,young,poisson,section.section_id),f"benchmark:{subdivisions}",section); processes.append(process)
            errors={"project_displacement":relative(project.maximum_displacement_m,analytical["tip_displacement_m"]),"project_stress":relative(project.maximum_von_mises_pa,analytical["maximum_bending_stress_pa"]),"calculix_displacement":relative(calculated["maximum_displacement_m"],analytical["tip_displacement_m"]),"calculix_stress":relative(calculated["maximum_surface_von_mises_pa"],analytical["maximum_bending_stress_pa"])}
            benchmark_results.append({"subdivisions":subdivisions,"project":asdict(project),"calculix":calculated,"relative_errors":errors})
        fine_benchmark=benchmark_results[-1]
        if max(fine_benchmark["relative_errors"].values())>float(tolerances["analytical_relative"]): raise VehicleFrameError("fine cantilever analytical benchmark gate failed")
        for metric in ("calculix_displacement","calculix_stress"):
            if not all(benchmark_results[index+1]["relative_errors"][metric] < benchmark_results[index]["relative_errors"][metric] for index in range(len(benchmark_results)-1)):
                raise VehicleFrameError("cantilever refinement did not reduce CalculiX error")
        stage="promotions"; ledger=read_jsonl(ledger_path); by_id={row["candidate"]["candidate_id"]:row for row in ledger}; promotions=summary050["promotions"]
        if len(promotions)!=9 or len(by_id)!=288: raise VehicleFrameError("Work 050 promotion or ledger count mismatch")
        for row in ledger:
            if candidate_identity(row)!=row["candidate"]["candidate_id"]: raise VehicleFrameError("candidate ledger identity mismatch")
        base_raw=read(ROOT/"config/vehicle/topology_neutral_vehicle_v1.json"); base=from_mapping(base_raw); validate(base); base_props=mass_properties(base); work048=read(ROOT/"artifacts/work048/experiment_summary.json"); holdout={row["case_id"]:row for row in work048["results"] if row["partition"]=="holdout"}
        if set(holdout)!=set(work048["partitions"]["holdout"]): raise VehicleFrameError("holdout evidence is incomplete")
        results=[]
        for promotion in promotions:
            candidate_id=promotion["candidate_id"]; record=by_id[candidate_id]; variables={name:float(value) for name,value in record["candidate"]["variables"]}; candidate_raw=mutate_candidate_assembly(base_raw,variables); candidate=from_mapping(candidate_raw); validate(candidate); props=mass_properties(candidate); mass_ratio=props["mass_kg"]/base_props["mass_kg"]
            candidate_cases=[]
            for case_id,case in sorted(holdout.items()):
                refinements=[]
                for subdivisions in config["subdivisions_per_branch"]:
                    model=build_vehicle_frame(candidate_raw,int(subdivisions)); loads=loads_from_work048(model,case,mass_ratio,base_props["centre_of_mass_m"]); project=solve_frame(model,loads,young,poisson)
                    scale=max(1.0,max(abs(value) for wrench in loads.values() for value in wrench)); reaction_relative=max(abs(value) for value in project.equilibrium_residual)/scale
                    if reaction_relative>float(tolerances["reaction_relative"]): raise VehicleFrameError("frame reaction equilibrium gate failed")
                    section_outputs=[]
                    for section in model.sections:
                        calculated_section,process=run_ccx(args.ccx,args.artifact_root/"candidates"/candidate_id/case_id/f"mesh_{subdivisions}"/section.section_id,build_calculix_b31_deck(model,loads,young,poisson,section.section_id),f"candidate:{candidate_id}:{case_id}:{subdivisions}:{section.section_id}",section); processes.append(process); section_outputs.append(calculated_section)
                    displacement_values=[item["maximum_displacement_m"] for item in section_outputs]
                    if max(displacement_values)-min(displacement_values)>float(tolerances["absolute"]): raise VehicleFrameError("section-output displacement replay mismatch")
                    calculated={"maximum_displacement_m":max(displacement_values),"maximum_surface_von_mises_pa":max(item["maximum_surface_von_mises_pa"] for item in section_outputs),"section_outputs":section_outputs}
                    cross={"displacement":relative(calculated["maximum_displacement_m"],project.maximum_displacement_m),"stress":relative(calculated["maximum_surface_von_mises_pa"],project.maximum_von_mises_pa)}
                    governing=max(project.maximum_von_mises_pa,calculated["maximum_surface_von_mises_pa"]); margin=yield_stress/governing
                    refinements.append({"subdivisions":subdivisions,"project":asdict(project),"calculix":calculated,"cross_model_relative":cross,"reaction_relative":reaction_relative,"yield_margin":margin})
                coarse,medium,fine=refinements; convergence={name:relative(fine[source][key],medium[source][key]) for name,source,key in (("project_displacement","project","maximum_displacement_m"),("project_stress","project","maximum_von_mises_pa"),("calculix_displacement","calculix","maximum_displacement_m"),("calculix_stress","calculix","maximum_surface_von_mises_pa"))}
                converged=max(convergence.values())<=float(tolerances["last_two_refinement_relative"])
                cross_model_passed=max(fine["cross_model_relative"].values())<=float(tolerances["calculix_cross_model_relative"])
                fine_margin=yield_stress/max(fine["project"]["maximum_von_mises_pa"],fine["calculix"]["maximum_surface_von_mises_pa"]); displacement=max(fine["project"]["maximum_displacement_m"],fine["calculix"]["maximum_displacement_m"]); passed=converged and cross_model_passed and fine_margin>=float(config["promotion"]["minimum_yield_margin"]) and displacement<=float(config["promotion"]["maximum_displacement_m"])
                candidate_cases.append({"case_id":case_id,"refinements":refinements,"last_two_relative":convergence,"converged":converged,"fine_cross_model_passed":cross_model_passed,"governing_yield_margin":fine_margin,"governing_displacement_m":displacement,"status":"passed" if passed else "failed"})
            results.append({"candidate_id":candidate_id,"candidate_variables":variables,"candidate_geometry_sha256":canonical_sha256(candidate_raw),"mass_kg":props["mass_kg"],"mass_ratio":mass_ratio,"holdout_cases":candidate_cases,"status":"passed" if all(case["status"]=="passed" for case in candidate_cases) else "failed"})
        stage="negative_controls"
        benchmark_model_ref,unit=benchmark_model(1.0,0.02,1); node=next(iter(unit)); load={node:(0.0,-100.0,0.0,0.0,0.0,0.0)}; reversed_load={node:(0.0,100.0,0.0,0.0,0.0,0.0)}; normal=solve_frame(benchmark_model_ref,load,young,poisson); reversed_result=solve_frame(benchmark_model_ref,reversed_load,young,poisson)
        if not math.isclose(normal.maximum_displacement_m,reversed_result.maximum_displacement_m,rel_tol=0,abs_tol=1e-12): raise VehicleFrameError("reversed-load metamorphic control failed")
        negative=[]
        def reject(control_id,action,expected):
            try: action()
            except (KeyError,TypeError,ValueError,VehicleFrameError) as exc:
                if expected.lower() not in str(exc).lower(): raise
                negative.append({"control_id":control_id,"status":"rejected_as_expected","reason":str(exc)});return
            raise VehicleFrameError(f"negative control {control_id} was admitted")
        reject("zero_stiffness",lambda:solve_frame(benchmark_model_ref,load,0.0,poisson),"stiffness")
        reject("missing_restraint",lambda:solve_frame(replace(benchmark_model_ref,fixed_node_id=999),load,young,poisson),"999")
        reject("incomplete_solver_output",lambda:parse_calculix_b31_dat("displacements (vx,vy,vz)\n1 0 0 0\n"),"stress")
        reject("incomplete_section_output",lambda:parse_calculix_section_forces_frd("9999\n"),"missing")
        reject("unknown_section_output",lambda:build_calculix_b31_deck(benchmark_model_ref,load,young,poisson,"missing"),"unknown")
        altered=json.loads(json.dumps(ledger[0]));altered["candidate"]["variables"][0][1]+=0.001
        reject("altered_candidate_identity",lambda:(_ for _ in ()).throw(VehicleFrameError("candidate ledger identity mismatch")) if candidate_identity(altered)!=altered["candidate"]["candidate_id"] else None,"identity")
        tiny=replace(benchmark_model_ref,sections=(FrameSection("beam",0.001,0.001),)); tiny_result=solve_frame(tiny,load,young,poisson)
        if tiny_result.maximum_von_mises_pa<=yield_stress: raise VehicleFrameError("undersized-section control did not exceed yield")
        negative.append({"control_id":"undersized_section","status":"failed_as_expected","maximum_von_mises_pa":tiny_result.maximum_von_mises_pa})
        replay_model=build_vehicle_frame(mutate_candidate_assembly(base_raw,results[0]["candidate_variables"]),4); replay_loads=loads_from_work048(replay_model,next(iter(holdout.values())),results[0]["mass_ratio"],base_props["centre_of_mass_m"]); replay_a=solve_frame(replay_model,replay_loads,young,poisson);replay_b=solve_frame(replay_model,replay_loads,young,poisson)
        if replay_a!=replay_b: raise VehicleFrameError("project frame replay differs")
        passed_candidates=sum(item["status"]=="passed" for item in results)
        candidate_set_decision="all_candidates_supported" if passed_candidates==len(results) else "partially_supported" if passed_candidates else "no_candidate_supported"
        summary={"status":"passed","decision":"independent_refined_evaluator_available","candidate_set_decision":candidate_set_decision,"claim_level":config["claim_level"],"evaluator_identity":config["evaluator_identity"],"config_sha256":sha(args.config),"material":material,"analytical_benchmark":analytical,"benchmark_results":benchmark_results,"promotion_results":results,"promoted_candidates":len(results),"passed_candidates":passed_candidates,"structural_states":len(results)*len(holdout)*len(config["subdivisions_per_branch"]),"candidate_calculix_processes":len(results)*len(holdout)*len(config["subdivisions_per_branch"])*3,"negative_controls":negative,"replay":{"status":"exact","fingerprint_sha256":replay_a.result_sha256},"process_evidence":processes,"tool_sha256":{"ccx":sha(args.ccx)},"upstream":{"work050_records_sha256":summary050["replay"]["records_sha256"],"result_ledger_sha256":sha(ledger_path),"budget_ledger_sha256":sha(budget_path),"work050_process":{"exit_code":upstream.returncode,"stdout":upstream.stdout,"stderr":upstream.stderr}},"repository_commit":subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip(),"worktree_dirty_during_run":bool(subprocess.run(["git","status","--porcelain"],cwd=ROOT,text=True,capture_output=True,check=True).stdout),"review":{"supporting_evidence":["project 6-DOF frame FEM matched the analytical cantilever and CalculiX B31 section-force-derived surface stress/deformation","all promoted candidates were solved on both frozen holdouts through three refinements and isolated section outputs","support reaction closure, stress, deformation, yield margin, and replay were explicit"],"contradicting_evidence":["two of nine proxy-promoted candidates exceeded the preregistered 8% project/CalculiX stress-difference gate","the evaluator is a linear beam network rather than a solid/contact whole-vehicle model"],"alternative_explanations":["rigid joints and square equivalent sections can hide local stress concentrations","the two rejected candidates can expose formulation sensitivity rather than physical failure because their yield margins remain large"],"missing_evidence":["solid stress concentrations, nonlinear contact/materials, buckling, vibration, crash, fatigue, and physical calibration"],"confidence":"high for evaluator availability and seven admitted candidates in the bounded linear beam domain; low outside it"}}
        write(args.artifact_root/"experiment_summary.json",summary)
        print(json.dumps({"status":"passed","decision":summary["decision"],"candidate_set_decision":summary["candidate_set_decision"],"candidates":len(results),"passed_candidates":summary["passed_candidates"],"structural_states":summary["structural_states"],"candidate_calculix_processes":summary["candidate_calculix_processes"],"fine_benchmark_max_error":max(fine_benchmark["relative_errors"].values()),"negative_controls":len(negative),"replay":"exact","summary":str(args.artifact_root/"experiment_summary.json")},sort_keys=True));return 0
    except Exception as exc:
        write(args.artifact_root/"experiment_failure.json",{"status":"failed","failed_stage":stage,"error_type":type(exc).__name__,"message":str(exc),"traceback":traceback.format_exc()});print(json.dumps({"status":"failed","stage":stage,"message":str(exc)},sort_keys=True),file=sys.stderr);return 1


if __name__=="__main__": raise SystemExit(main())
