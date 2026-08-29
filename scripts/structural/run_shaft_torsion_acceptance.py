"""Run Work 036 solid-shaft torsion acceptance and metamorphic cases."""
from __future__ import annotations

import argparse, hashlib, json, math, shutil, subprocess, sys, time, traceback
from dataclasses import replace
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from formula_ultimate.structural import (  # noqa: E402
    StructuralEvidenceError, TorsionSpec, build_torsion_calculix_input,
    parse_calculix_dat, parse_msh2,
)

def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, indent=2, sort_keys=True)+"\n", encoding="utf-8")
def run(command: list[str], cwd: Path) -> dict[str, Any]:
    started=time.time_ns(); begin=time.perf_counter(); done=subprocess.run(command,cwd=cwd,text=True,capture_output=True,check=False)
    return {"command":command,"exit_code":done.returncode,"stdout":done.stdout.strip(),"stderr":done.stderr.strip(),"started_time_ns":started,"wall_time_s":time.perf_counter()-begin}
def relative(a: float,b: float)->float: return abs(a-b)/max(abs(b),1e-300)
def geo(spec:TorsionSpec,size:float)->str:
    r=spec.radius_m
    return "\n".join(('SetFactory("OpenCASCADE");',f"Cylinder(1) = {{0, {r:.17g}, {r:.17g}, {spec.length_m:.17g}, 0, 0, {r:.17g}}};",f"Mesh.CharacteristicLengthMin = {size:.17g};",f"Mesh.CharacteristicLengthMax = {size:.17g};","Mesh.Algorithm3D = 1;","Mesh.ElementOrder = 1;","Mesh.MshFileVersion = 2.2;","Mesh.Binary = 0;","Mesh.SaveAll = 1;","Physical Volume(1) = {1};",""))
def tet(nodes,conn):
    pts=tuple(nodes[n] for n in conn); a,b,c,d=pts
    ab=tuple(b[i]-a[i] for i in range(3)); ac=tuple(c[i]-a[i] for i in range(3)); ad=tuple(d[i]-a[i] for i in range(3))
    cross=(ac[1]*ad[2]-ac[2]*ad[1],ac[2]*ad[0]-ac[0]*ad[2],ac[0]*ad[1]-ac[1]*ad[0])
    return abs(math.fsum(ab[i]*cross[i] for i in range(3)))/6, tuple(math.fsum(p[i] for p in pts)/4 for i in range(3))
def moment(origin,pos,force):
    r=tuple(pos[i]-origin[i] for i in range(3)); return (r[1]*force[2]-r[2]*force[1],r[2]*force[0]-r[0]*force[2],r[0]*force[1]-r[1]*force[0])

def solve_case(spec,mesh,run_dir,ccx,tol,mesh_path,restrained=True):
    run_dir.mkdir(parents=True,exist_ok=True)
    deck,loads,weights,fixed,loaded=build_torsion_calculix_input(spec=spec,mesh=mesh,boundary_tolerance_m=float(tol["boundary_coordinate_absolute_m"]),restrained=restrained)
    deck_path=run_dir/"shaft.inp"; deck_path.write_text(deck,encoding="ascii")
    evidence=run([str(ccx),"shaft"],run_dir); evidence["stage"]=f"calculix:{run_dir.name}"
    if not restrained:
        rejected=evidence["exit_code"]!=0
        rejection_reason="nonzero_solver_exit" if rejected else ""
        if not rejected:
            try:
                negative_parsed=parse_calculix_dat(run_dir/"shaft.dat")
                maximum_displacement=max(math.sqrt(math.fsum(value*value for value in vector)) for vector in negative_parsed["displacements"].values())
                if maximum_displacement > 100.0*spec.length_m:
                    rejected=True; rejection_reason="unbounded_rigid_body_displacement"
            except Exception:
                rejected=True; rejection_reason="incomplete_solver_evidence"
        if not rejected: raise StructuralEvidenceError("unrestrained negative control was admitted")
        return {"status":"rejected_as_required","rejection_reason":rejection_reason,"process":evidence,"deck_sha256":sha(deck_path)}, evidence
    if evidence["exit_code"]!=0: raise StructuralEvidenceError(f"CalculiX failed: {evidence}")
    dat,frd=run_dir/"shaft.dat",run_dir/"shaft.frd"
    for path in (dat,frd):
        if not path.is_file() or path.stat().st_mtime_ns<evidence["started_time_ns"]: raise StructuralEvidenceError(f"missing fresh {path.name}")
    parsed=parse_calculix_dat(dat)
    if set(loaded)-set(parsed["displacements"]) or set(fixed)-set(parsed["reactions"]): raise StructuralEvidenceError("boundary evidence omitted")
    if set(parsed["stress_tensor_by_element_pa"])!=set(mesh.tetrahedra): raise StructuralEvidenceError("stress coverage differs from mesh")
    vc={e:tet(mesh.nodes,c) for e,c in mesh.tetrahedra.items()}; volume=math.fsum(v[0] for v in vc.values())
    area=math.fsum(weights.values()); cy=math.fsum(weights[n]*mesh.nodes[n][1] for n in loaded)/area; cz=math.fsum(weights[n]*mesh.nodes[n][2] for n in loaded)/area
    denominator=math.fsum(weights[n]*((mesh.nodes[n][1]-cy)**2+(mesh.nodes[n][2]-cz)**2) for n in loaded)
    twist=math.fsum(weights[n]*((mesh.nodes[n][1]-cy)*parsed["displacements"][n][2]-(mesh.nodes[n][2]-cz)*parsed["displacements"][n][1]) for n in loaded)/denominator
    work=.5*math.fsum(math.fsum(loads[n][i]*parsed["displacements"][n][i] for i in range(3)) for n in loaded)
    total_load=tuple(math.fsum(f[i] for f in loads.values()) for i in range(3)); applied_m=tuple(math.fsum(moment((spec.length_m,cy,cz),mesh.nodes[n],loads[n])[i] for n in loaded) for i in range(3))
    reaction=parsed["total_reaction"]; rm=tuple(math.fsum(moment((0.,cy,cz),mesh.nodes[n],parsed["reactions"][n])[i] for n in fixed) for i in range(3))
    force_res=tuple(total_load[i]+reaction[i] for i in range(3)); moment_res=tuple(applied_m[i]+rm[i] for i in range(3))
    gauge=[]
    for e,(v,c) in vc.items():
        if spec.gauge_x_min_m<=c[0]<=spec.gauge_x_max_m:
            t=parsed["stress_tensor_by_element_pa"][e]; ref=spec.analytical_shear_pa(y_m=c[1],z_m=c[2]); gauge.append((v,(t[3],t[4]),ref))
    if not gauge: raise StructuralEvidenceError("empty stress gauge")
    err=math.fsum(v*((a[0]-r[0])**2+(a[1]-r[1])**2) for v,a,r in gauge); ref2=math.fsum(v*(r[0]**2+r[1]**2) for v,a,r in gauge); act2=math.fsum(v*(a[0]**2+a[1]**2) for v,a,r in gauge); cross=math.fsum(v*(a[0]*r[0]+a[1]*r[1]) for v,a,r in gauge)
    stress_error=math.sqrt(err/ref2); corr=cross/math.sqrt(act2*ref2); stress_rms=math.sqrt(act2/math.fsum(v for v,_,_ in gauge))
    force_scale=abs(spec.torque_nm)/spec.radius_m
    metrics={"twist_rad":twist,"external_work_j":work,"stress_vector_normalized_rms":stress_error,"stress_vector_signed_correlation":corr,"stress_actual_rms_pa":stress_rms,"force_closure_relative":math.sqrt(math.fsum(x*x for x in force_res))/force_scale,"moment_closure_relative":math.sqrt(math.fsum(x*x for x in moment_res))/abs(spec.torque_nm),"load_force_relative":math.sqrt(math.fsum(x*x for x in total_load))/force_scale,"load_torque_relative":relative(applied_m[0],spec.torque_nm),"twist_analytical_relative":relative(twist,spec.analytical_twist_rad),"energy_analytical_relative":relative(work,spec.analytical_energy_j),"geometry_volume_relative":relative(volume,spec.volume_m3),"applied_moment_nm":applied_m,"reaction_moment_nm":rm}
    failures=[k for k in ("load_force_relative","load_torque_relative","force_closure_relative","moment_closure_relative","twist_analytical_relative","energy_analytical_relative","stress_vector_normalized_rms") if metrics[k]>float(tol[k])]
    if corr<float(tol["stress_vector_signed_correlation_minimum"]): failures.append("stress_vector_signed_correlation")
    if metrics["geometry_volume_relative"]>.02: failures.append("geometry_volume_relative")
    if failures: raise StructuralEvidenceError(f"torsion gates failed {failures}: {metrics}")
    return {"metrics":metrics,"node_count":len(mesh.nodes),"tetrahedron_count":len(mesh.tetrahedra),"mesh_volume_m3":volume,"mesh_sha256":sha(mesh_path),"deck_sha256":sha(deck_path),"dat_sha256":sha(dat),"frd_sha256":sha(frd)},evidence

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--config",type=Path,required=True); p.add_argument("--artifact-root",type=Path,required=True); p.add_argument("--gmsh",type=Path,required=True); p.add_argument("--ccx",type=Path,required=True); a=p.parse_args()
    processes=[]; stage="configuration"
    try:
        payload=json.loads(a.config.read_text(encoding="utf-8")); spec=TorsionSpec.from_mapping(payload); tol=payload["tolerances"]; levels=payload["mesh_levels"]
        if len(levels)!=3: raise StructuralEvidenceError("exactly three mesh levels required")
        if a.artifact_root.exists(): shutil.rmtree(a.artifact_root)
        a.artifact_root.mkdir(parents=True); results=[]; meshes=[]
        for level in levels:
            ident=level["mesh_id"]; directory=a.artifact_root/ident; directory.mkdir(); gp=directory/"shaft.geo"; mp=directory/"shaft.msh"; gp.write_text(geo(spec,float(level["characteristic_size_m"])),encoding="ascii")
            stage=f"gmsh:{ident}"; ev=run([str(a.gmsh),str(gp),"-3","-format","msh2","-o",str(mp)],directory); ev["stage"]=stage; processes.append(ev)
            if ev["exit_code"]!=0 or not mp.is_file(): raise StructuralEvidenceError(f"Gmsh failed: {ev}")
            mesh=parse_msh2(mp); stage=f"calculix:{ident}"; result,ev=solve_case(spec,mesh,directory,a.ccx,tol,mp); processes.append(ev); result.update({"mesh_id":ident,"characteristic_size_m":float(level["characteristic_size_m"])}); results.append(result); meshes.append((mesh,mp))
        medium,fine=results[-2:]; convergence={"last_two_twist_relative":relative(fine["metrics"]["twist_rad"],medium["metrics"]["twist_rad"]),"last_two_energy_relative":relative(fine["metrics"]["external_work_j"],medium["metrics"]["external_work_j"]),"last_two_stress_error_absolute_change":abs(fine["metrics"]["stress_vector_normalized_rms"]-medium["metrics"]["stress_vector_normalized_rms"])}
        failed=[k for k,v in convergence.items() if v>float(tol[k])]
        if failed: raise StructuralEvidenceError(f"convergence failed {failed}: {convergence}")
        base=results[1]; metamorphic={}
        cases=(("reverse",replace(spec,torque_nm=-spec.torque_nm)),("double_torque",replace(spec,torque_nm=2*spec.torque_nm)),("double_modulus",replace(spec,youngs_modulus_pa=2*spec.youngs_modulus_pa)))
        for name,case_spec in cases:
            result,ev=solve_case(case_spec,meshes[1][0],a.artifact_root/name,a.ccx,tol,meshes[1][1]); processes.append(ev); metamorphic[name]=result
        mt=float(tol["metamorphic_relative"]); checks={"reverse_twist":relative(metamorphic["reverse"]["metrics"]["twist_rad"],-base["metrics"]["twist_rad"]),"reverse_energy":relative(metamorphic["reverse"]["metrics"]["external_work_j"],base["metrics"]["external_work_j"]),"double_twist":relative(metamorphic["double_torque"]["metrics"]["twist_rad"],2*base["metrics"]["twist_rad"]),"double_stress":relative(metamorphic["double_torque"]["metrics"]["stress_actual_rms_pa"],2*base["metrics"]["stress_actual_rms_pa"]),"double_energy":relative(metamorphic["double_torque"]["metrics"]["external_work_j"],4*base["metrics"]["external_work_j"]),"double_modulus_twist":relative(metamorphic["double_modulus"]["metrics"]["twist_rad"],.5*base["metrics"]["twist_rad"]),"double_modulus_stress":relative(metamorphic["double_modulus"]["metrics"]["stress_actual_rms_pa"],base["metrics"]["stress_actual_rms_pa"])}
        if any(v>mt for v in checks.values()): raise StructuralEvidenceError(f"metamorphic checks failed: {checks}")
        negative,ev=solve_case(spec,meshes[1][0],a.artifact_root/"unrestrained_negative_control",a.ccx,tol,meshes[1][1],restrained=False); processes.append(ev); metamorphic["unrestrained_negative_control"]=negative
        summary={"status":"passed","claim_level":spec.claim_level,"analytical_reference":{"G_pa":spec.shear_modulus_pa,"J_m4":spec.polar_second_moment_m4,"twist_rad":spec.analytical_twist_rad,"energy_j":spec.analytical_energy_j},"mesh_results":results,"mesh_convergence":convergence,"metamorphic_results":metamorphic,"metamorphic_checks":checks,"process_evidence":processes,"config_sha256":sha(a.config),"tool_sha256":{"gmsh":sha(a.gmsh),"ccx":sha(a.ccx)},"repository_commit":subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip(),"worktree_dirty_during_run":bool(subprocess.run(["git","status","--porcelain"],cwd=ROOT,text=True,capture_output=True,check=True).stdout)}
        write_json(a.artifact_root/"experiment_summary.json",summary); print(json.dumps({"status":"passed","finest_nodes":fine["node_count"],"finest_tetrahedra":fine["tetrahedron_count"],"finest_twist_rad":fine["metrics"]["twist_rad"],"finest_stress_error":fine["metrics"]["stress_vector_normalized_rms"],"summary":str(a.artifact_root/"experiment_summary.json")},sort_keys=True)); return 0
    except Exception as exc:
        write_json(a.artifact_root/"experiment_failure.json",{"status":"failed","failed_stage":stage,"error_type":type(exc).__name__,"message":str(exc),"process_evidence":processes,"traceback":traceback.format_exc()}); print(str(exc),file=sys.stderr); return 1
if __name__=="__main__": raise SystemExit(main())
