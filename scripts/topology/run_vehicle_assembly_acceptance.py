from __future__ import annotations
import argparse,copy,hashlib,json,math,shutil,subprocess,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/"src"))
from formula_ultimate.topology import VehicleAssemblyViolation,declaration_sha256,from_mapping,mass_properties,validate
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def run(cmd):
    started=time.time_ns(); tick=time.perf_counter(); x=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,check=False); return {"command":cmd,"exit_code":x.returncode,"stdout":x.stdout,"stderr":x.stderr,"started_time_ns":started,"wall_time_s":time.perf_counter()-tick}
def rel(a,b): return abs(float(a)-float(b))/max(abs(float(b)),1e-300)
def rejected(cid,action,expected):
    try: action()
    except Exception as e:
        if expected not in str(e): raise VehicleAssemblyViolation(f"{cid} wrong rejection: {e}") from e
        return {"control_id":cid,"status":"rejected_as_expected","reason":str(e)}
    raise VehicleAssemblyViolation(f"negative control {cid} admitted")
def main():
    p=argparse.ArgumentParser(); p.add_argument("--config",type=Path,required=True); p.add_argument("--artifact-root",type=Path,required=True); p.add_argument("--cadquery-python",type=Path,required=True); p.add_argument("--freecad-python",type=Path,required=True); a=p.parse_args(); processes=[]; stage="configuration"
    try:
        raw=json.loads(a.config.read_text(encoding="utf-8")); assembly=from_mapping(raw); grammar=validate(assembly); analytical=mass_properties(assembly)
        if raw.get("failure_contract")!="structural_failure_coupling_v1": raise VehicleAssemblyViolation("Work 046 failure contract mismatch")
        if a.artifact_root.exists(): shutil.rmtree(a.artifact_root)
        a.artifact_root.mkdir(parents=True)
        manifests=[]
        for identity in ("replay_a","replay_b"):
            root=a.artifact_root/identity; manifest=root/"manifest.json"; stage=f"cadquery:{identity}"
            proc=run([str(a.cadquery_python),str(ROOT/"scripts/cad/generate_vehicle_assembly.py"),"--config",str(a.config),"--output-root",str(root),"--manifest",str(manifest)]); proc["stage"]=stage; processes.append(proc)
            if proc["exit_code"]: raise VehicleAssemblyViolation(f"CadQuery failed: {proc['stderr']}")
            manifests.append(json.loads(manifest.read_text(encoding="utf-8")))
        first,second=manifests
        hashes_a={x["component_id"]:x["step_sha256"] for x in first["components"]}; hashes_b={x["component_id"]:x["step_sha256"] for x in second["components"]}
        replay_exact=first["declaration_sha256"]==second["declaration_sha256"] and first["assembly"]["step_sha256"]==second["assembly"]["step_sha256"] and hashes_a==hashes_b
        if not replay_exact: raise VehicleAssemblyViolation("STEP replay identity differs")
        stage="freecad"; report_path=a.artifact_root/"freecad_report.json"; proc=run([str(a.freecad_python),str(ROOT/"scripts/cad/inspect_vehicle_assembly_freecad.py"),str(a.artifact_root/"replay_a/manifest.json"),str(a.config),str(report_path)]); proc["stage"]=stage; processes.append(proc)
        if proc["exit_code"]: raise VehicleAssemblyViolation(f"FreeCAD failed: {proc['stderr']}")
        freecad=json.loads(report_path.read_text(encoding="utf-8")); tolerance=float(raw["tolerances"]["mass_property_relative"])
        errors={"mass":rel(freecad["mass_properties"]["mass_kg"],analytical["mass_kg"]),"centre":max(rel(a,b) if b else abs(a-b) for a,b in zip(freecad["mass_properties"]["centre_of_mass_m"],analytical["centre_of_mass_m"])),"inertia":max(rel(a,b) if b else abs(a-b) for a,b in zip(freecad["mass_properties"]["inertia_kg_m2"],analytical["inertia_kg_m2"]))}
        if max(errors.values())>tolerance: raise VehicleAssemblyViolation(f"mass-property cross-check failed: {errors}")
        def invalid(mutator): value=copy.deepcopy(raw); mutator(value); return lambda: validate(from_mapping(value))
        controls=[
            rejected("floating_component",invalid(lambda x:x["connections"].pop()),"floating"),
            rejected("protected_overlap",invalid(lambda x:x["keep_outs"].__setitem__(0,{"keep_out_id":"bad","minimum_m":[-0.3,-0.06,0.09],"maximum_m":[-0.2,0.06,0.21]})),"keepout"),
            rejected("unmatched_interface",invalid(lambda x:x["connections"][0].__setitem__("interface_a","missing")),"unmatched"),
            rejected("disconnected_energy",invalid(lambda x:x.__setitem__("energy_edges",[])),"energy"),
            rejected("invalid_solid",invalid(lambda x:x["components"][0]["primitive"]["size_m"].__setitem__(0,0)),"primitive"),
            rejected("massless_energy",invalid(lambda x:x["materials"]["dense"].__setitem__("density_kg_per_m3",0)),"massless"),
            rejected("envelope_violation",invalid(lambda x:x["envelope"]["maximum_m"].__setitem__(0,0.1)),"envelope"),
            rejected("undeclared_ground",invalid(lambda x:x["interfaces"][-1]["local_position_m"].__setitem__(2,-0.04)),"ground"),
        ]
        summary={"status":"passed","claim_level":"geometric assembly admission only","candidate_id":assembly.candidate_id,"declaration_sha256":declaration_sha256(raw),"grammar_validation":grammar,"analytical_mass_properties":analytical,"freecad_mass_properties":freecad["mass_properties"],"mass_property_relative_errors":errors,"cadquery":first,"freecad":freecad,"replay":{"status":"exact","assembly_step_sha256":first["assembly"]["step_sha256"],"component_step_sha256":hashes_a},"negative_controls":controls,"process_evidence":processes,"config_sha256":sha(a.config),"repository_commit":subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip(),"worktree_dirty_during_run":bool(subprocess.run(["git","status","--porcelain"],cwd=ROOT,text=True,capture_output=True,check=True).stdout),"review":{"supporting_evidence":["four valid explicit solids and one declared contact passed the grammar","energy and external-load paths were explicit","FreeCAD independently matched mass, centre, and inertia","two exports had identical STEP hashes"],"contradicting_evidence":["the first cylinder export doubled height and was rejected by FreeCAD mass evidence"],"alternative_explanations":["agreement is expected for analytic primitives and is not an arbitrary-CAD proof"],"missing_evidence":["rotations, curved free-form geometry, joints/contact, FEA, aero, thermal, manufacturing, and physical testing"],"confidence":"high for this primitive fixture; low outside grammar v1"}}
        write(a.artifact_root/"experiment_summary.json",summary); print(json.dumps({"status":"passed","solid_count":first["assembly"]["solid_count"],"mass_kg":analytical["mass_kg"],"max_mass_property_error":max(errors.values()),"replay":"exact","negative_controls":len(controls),"summary":str(a.artifact_root/"experiment_summary.json")},sort_keys=True)); return 0
    except Exception as e:
        write(a.artifact_root/"experiment_failure.json",{"status":"failed","stage":stage,"error_type":type(e).__name__,"message":str(e),"process_evidence":processes,"traceback":traceback.format_exc()}); print(json.dumps({"status":"failed","stage":stage,"message":str(e)},sort_keys=True),file=sys.stderr); return 1
if __name__=="__main__": raise SystemExit(main())
