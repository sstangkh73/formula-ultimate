"""Execute Work 113 detailed connection/contact evidence."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
from typing import Any

ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/"src"
for item in (ROOT,SRC):
    if str(item) not in sys.path: sys.path.insert(0,str(item))

import cadquery as cq  # noqa: E402
from formula_ultimate.structural.detailed_connection_contact import DetailedConnectionViolation, canonical_sha256, evaluate, reduced_prediction, validate_protocol  # noqa: E402
from scripts.cad.generate_freeform_solid_corpus import canonicalize_step  # noqa: E402


def read(path:Path): return json.loads(path.read_text(encoding="utf-8"))
def write(path:Path,value:Any): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(path:Path): return hashlib.sha256(path.read_bytes()).hexdigest()
def relative(a,b): return abs(a-b)/max(abs(a),abs(b),1e-30)


def export(shape,path):
    cq.exporters.export(shape,str(path),exportType="STEP"); canonicalize_step(path); return {"file":path.name,"sha256":sha(path),"volume_m3":shape.val().Volume()*1e-9,"valid":shape.val().isValid()}


def build_threaded(strategy):
    scale=1000; root=strategy["root_radius_m"]*scale; radius=strategy["contact_radius_m"]*scale; sleeve=strategy["sleeve_outer_radius_m"]*scale; length=strategy["engagement_length_m"]*scale; pitch=strategy["pitch_m"]*scale; width=strategy["contact_width_m"]*scale
    helix=cq.Wire.makeHelix(pitch,length,radius); ridge=cq.Workplane("XZ").center(radius,0).circle(width/2).sweep(helix,isFrenet=True); groove=cq.Workplane("XZ").center(radius,0).circle(width*.75).sweep(helix,isFrenet=True)
    male=cq.Workplane("XY").circle(root).extrude(length).union(ridge); female=cq.Workplane("XY").circle(sleeve).circle(root+width*.7).extrude(length).cut(groove)
    return male,female,{"helix_turns":length/pitch,"root_radius_m":root/scale,"ridge_radius_m":width/(2*scale)}


def build_segmented(strategy):
    scale=1000; root=strategy["root_radius_m"]*scale; radius=strategy["contact_radius_m"]*scale; sleeve=strategy["sleeve_outer_radius_m"]*scale; length=strategy["engagement_length_m"]*scale; width=strategy["contact_width_m"]*scale; tangential=strategy["ramp_arc_m"]*scale; radial=2*(radius-root)
    male=cq.Workplane("XY").circle(root).extrude(length); female=cq.Workplane("XY").circle(sleeve).circle(root+width*.4).extrude(length)
    for index in range(strategy["lug_count"]):
        angle=360*index/strategy["lug_count"]; lug=cq.Workplane("XY").box(radial,tangential,width,centered=(True,True,True)).translate((root+radial/2,0,length*(index+.5)/strategy["lug_count"])).rotate((0,0,0),(0,0,1),angle)
        pocket=cq.Workplane("XY").box(radial+width,tangential+width,width*1.5,centered=(True,True,True)).translate((root+radial/2,0,length*(index+.5)/strategy["lug_count"])).rotate((0,0,0),(0,0,1),angle)
        male=male.union(lug); female=female.cut(pocket)
    return male,female,{"lug_count":strategy["lug_count"],"root_radius_m":root/scale,"radial_engagement_m":radial/scale}


def rejected(action,phrase):
    try: action()
    except DetailedConnectionViolation as exc:
        if phrase not in str(exc): raise
        return {"status":"rejected","reason":str(exc)}
    raise DetailedConnectionViolation("negative control was accepted")


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--config",type=Path,required=True); parser.add_argument("--output-root",type=Path,required=True); parser.add_argument("--replay-reference",type=Path)
    args=parser.parse_args(); config=(ROOT/args.config).resolve() if not args.config.is_absolute() else args.config; output=(ROOT/args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root; output.mkdir(parents=True,exist_ok=True)
    raw=read(config); validation=validate_protocol(raw)
    for dependency in raw["dependencies"]:
        if sha(ROOT/dependency["contract_path"])!=dependency["contract_sha256"]: raise DetailedConnectionViolation("stale dependency contract")
        if subprocess.run(["git","cat-file","-e",dependency["commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise DetailedConnectionViolation("missing dependency commit")
    cad={}; strategies={}; acceptance=raw["acceptance"]
    for strategy in raw["strategies"]:
        male,female,geometry=(build_threaded(strategy) if strategy["kind"]=="threaded_helix" else build_segmented(strategy)); overlap=male.intersect(female).val().Volume()*1e-9
        if not male.val().isValid() or not female.val().isValid() or overlap>1e-12: raise DetailedConnectionViolation("mating CAD is invalid or interferes")
        prefix=strategy["strategy_id"]; cad[prefix]={"male":export(male,output/f"{prefix}_male.step"),"female":export(female,output/f"{prefix}_female.step"),"engagement_geometry":geometry,"overlap_m3":overlap}
        levels=[]
        for count in raw["refinement_patch_counts"]:
            result=evaluate(strategy,raw["material"],raw["contact"],raw["task"],patch_count=count,preload_n=acceptance["baseline_preload_n"],friction=acceptance["baseline_friction"],clearance_m=acceptance["baseline_clearance_m"])
            fields={"patches":result.pop("contact_patches"),"normal_reactions_n":result.pop("normal_reactions_n"),"contact_field_sha256":result["contact_field_sha256"]}; field_path=output/f"{prefix}_{count}_contact.json"; write(field_path,fields); result["field_file"]=field_path.name
            if result["force_residual_relative"]>acceptance["force_residual_relative"] or result["moment_residual_relative"]>acceptance["moment_residual_relative"] or result["minimum_normal_reaction_n"]<0: raise DetailedConnectionViolation("contact inequality or balance gate failed")
            levels.append(result)
        convergence={}
        for key in ("normal_stiffness_n_m","shear_displacement_m","maximum_patch_pressure_pa"):
            convergence[key]=relative(levels[-2][key],levels[-1][key])
            if convergence[key]>acceptance["last_two_relative_change_limit"]: raise DetailedConnectionViolation("local contact refinement gate failed")
        samples=[]; maximum_error=0
        reference=levels[-1]
        for axial,shear in ((400.,200.),(600.,350.),(800.,500.)):
            task={**raw["task"],"axial_tension_n":axial,"shear_n":shear}; detailed=evaluate(strategy,raw["material"],raw["contact"],task,patch_count=raw["refinement_patch_counts"][-1],preload_n=acceptance["baseline_preload_n"],friction=acceptance["baseline_friction"],clearance_m=acceptance["baseline_clearance_m"]); predicted=reduced_prediction(reference,task,acceptance["baseline_clearance_m"])
            error=max(relative(detailed[k],predicted[k]) for k in ("axial_displacement_m","shear_displacement_m")); maximum_error=max(maximum_error,error); samples.append({"axial_tension_n":axial,"shear_n":shear,"maximum_displacement_relative_error":error})
        if maximum_error>acceptance["maximum_reduced_displacement_relative_error"]: raise DetailedConnectionViolation("reduced model applicability error exceeded")
        strategies[prefix]={"levels":levels,"convergence":convergence,"reduced_model":{"maximum_displacement_relative_error":maximum_error,"samples":samples,"domain":"registered stick cases only"}}
    baseline_strategy=raw["strategies"][0]; base=strategies[baseline_strategy["strategy_id"]]["levels"][-1]
    low_preload=evaluate(baseline_strategy,raw["material"],raw["contact"],raw["task"],patch_count=48,preload_n=2000,friction=.2,clearance_m=acceptance["baseline_clearance_m"]); half=evaluate(baseline_strategy,raw["material"],raw["contact"],raw["task"],patch_count=48,preload_n=acceptance["baseline_preload_n"],friction=acceptance["baseline_friction"],clearance_m=acceptance["baseline_clearance_m"],engagement_fraction=.5); clear=evaluate(baseline_strategy,raw["material"],raw["contact"],raw["task"],patch_count=48,preload_n=acceptance["baseline_preload_n"],friction=acceptance["baseline_friction"],clearance_m=raw["contact"]["clearance_range_m"][1]); reverse=evaluate(baseline_strategy,raw["material"],raw["contact"],{**raw["task"],"shear_n":-raw["task"]["shear_n"]},patch_count=48,preload_n=acceptance["baseline_preload_n"],friction=acceptance["baseline_friction"],clearance_m=acceptance["baseline_clearance_m"])
    controls={"removed_joint":rejected(lambda:evaluate(baseline_strategy,raw["material"],raw["contact"],raw["task"],patch_count=48,preload_n=4000,friction=.25,clearance_m=1e-5,joint_present=False),"joint removed"),"severed_joint":rejected(lambda:evaluate(baseline_strategy,raw["material"],raw["contact"],raw["task"],patch_count=48,preload_n=4000,friction=.25,clearance_m=1e-5,engagement_fraction=0),"engagement"),"low_preload_friction":{"status":low_preload["status"],"friction_capacity_n":low_preload["friction_capacity_n"]},"reduced_engagement":{"baseline_stiffness_n_m":base["normal_stiffness_n_m"],"reduced_stiffness_n_m":half["normal_stiffness_n_m"]},"clearance":{"baseline_displacement_m":base["axial_displacement_m"],"increased_displacement_m":clear["axial_displacement_m"]},"reverse_load":{"forward_shear_displacement_m":base["shear_displacement_m"],"reverse_shear_displacement_m":reverse["shear_displacement_m"]}}
    if low_preload["status"]!="slip" or half["normal_stiffness_n_m"]>=base["normal_stiffness_n_m"] or clear["axial_displacement_m"]<=base["axial_displacement_m"] or abs(reverse["shear_displacement_m"]+base["shear_displacement_m"])>1e-15: raise DetailedConnectionViolation("causal controls failed")
    body={"status":"passed","claim_scope":"bounded discrete unilateral/Coulomb contact and deterministic CAD evidence; not a general nonlinear solve or physical validation","validation":validation,"dependencies":raw["dependencies"],"cad":cad,"strategies":strategies,"controls":controls,"review":{"supporting_evidence":["both strategies produced noninterfering mating CAD and three-level contact fields","force/moment/contact inequalities and deterministic replay gates passed","preload, clearance, engagement and reverse-load controls were causal"],"contradicting_evidence":["contact is discretized into regularized patches and no dedicated nonlinear solver cross-check exists"],"alternative_explanations":["bounded stick cases make the reduced stiffness comparison nearly exact"],"missing_evidence":["thread flank plasticity","loosening and fatigue","measured friction/preload","physical validation"],"confidence":"moderate for bounded initialization and reduced-model handoff; low for production joint strength or life"}}
    result={"body":body,"result_sha256":canonical_sha256(body)}; write(output/"result.json",result)
    if args.replay_reference:
        path=(ROOT/args.replay_reference).resolve() if not args.replay_reference.is_absolute() else args.replay_reference; prior=read(path); exact=prior.get("result_sha256")==result["result_sha256"]; write(output/"replay.json",{"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"],"exact":exact})
        if not exact: raise DetailedConnectionViolation("replay differs from reference")
    print(json.dumps({"status":"passed","result_sha256":result["result_sha256"],"strategy_count":len(strategies)},sort_keys=True)); return 0


if __name__=="__main__": raise SystemExit(main())
