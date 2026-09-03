"""Build and evaluate the Work 087 load-structure integration candidate."""
from __future__ import annotations
import argparse,hashlib,json,math,os,re,shutil,subprocess,sys
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/"src"))
import cadquery as cq
from formula_ultimate.subsystems.load_structure_integration import canonical_sha256,evaluate,validate_config
MM=1000.0
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canonicalize(path):
    text=path.read_text(encoding="ascii"); updated,count=re.subn(r"(FILE_NAME\('[^']*',)'[^']*'",r"\1'1970-01-01T00:00:00'",text,count=1)
    if count!=1: raise RuntimeError("STEP timestamp missing or ambiguous")
    path.write_text(updated,encoding="ascii",newline="\n")
def box(size,center): return cq.Workplane("XY").box(*(x*MM for x in size),centered=(True,True,True)).val().translate(tuple(x*MM for x in center))
def tube(p):
    x,z=p["axis_xz_m"]; length=p["y_max_m"]-p["y_min_m"]; origin=cq.Vector(x*MM,p["y_min_m"]*MM,z*MM); axis=cq.Vector(0,1,0)
    return cq.Solid.makeCylinder(p["outer_radius_m"]*MM,length*MM,origin,axis).cut(cq.Solid.makeCylinder(p["inner_radius_m"]*MM,(length+0.002)*MM,cq.Vector(x*MM,(p["y_min_m"]-0.001)*MM,z*MM),axis))
def generated_shape(part):
    p=part["parameters"]
    if part["kind"]=="box": return box(p["size_m"],p["center_m"])
    if part["kind"]=="annular_y_tube": return tube(p)
    rails=[]; sx,sz=p["rail_section_m"]
    for y in p["rail_y_m"]: rails.append(box([p["x_length_m"],sx,sz],[p["x_center_m"],y,p["z_center_m"]]))
    for x in p["crossmember_x_m"]: rails.append(box([sx,p["crossmember_y_length_m"],sz],[x,sum(p["rail_y_m"])/2,p["z_center_m"]]))
    shape=rails[0]
    for item in rails[1:]: shape=shape.fuse(item)
    return shape
def inertia(shape,density): return [[float(x)*1e-15*density for x in row] for row in cq.Shape.matrixOfInertia(shape)]
def write(path,value): path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
def main():
    p=argparse.ArgumentParser(); p.add_argument("--config",type=Path,required=True); p.add_argument("--output-root",type=Path,required=True); p.add_argument("--freecad-python",type=Path,required=True); p.add_argument("--replay-reference",type=Path); a=p.parse_args(); a.output_root=a.output_root.resolve()
    if a.output_root.exists() and any(a.output_root.iterdir()): raise SystemExit("output-root must be absent or empty")
    a.output_root.mkdir(parents=True,exist_ok=True); raw=json.loads(a.config.read_text(encoding="utf-8")); validation=validate_config(raw); shapes={}; records=[]; upstream={}
    for source_key in ("work083_result","work084_result","work086_result"):
        source=raw["sources"][source_key]; upstream[source_key]=json.loads((ROOT/source["path"]).read_text(encoding="utf-8"))
    for source_key in ("work083_result","work084_result"):
        source=raw["sources"][source_key]; manifest=json.loads((ROOT/source["manifest_path"]).read_text(encoding="utf-8"))
        if manifest["manifest_sha256"]!=source["manifest_sha256"]: raise RuntimeError("upstream manifest identity mismatch")
        for item in manifest["parts"]:
            pid=item["part_id"]
            if pid in shapes: raise RuntimeError("duplicate upstream part id")
            src=ROOT/source["step_root"]/item["step_file"]; dst=a.output_root/f"{pid}.step"
            if sha(src)!=item["step_sha256"]: raise RuntimeError("upstream STEP identity mismatch")
            shutil.copyfile(src,dst); shape=cq.importers.importStep(str(dst)).val(); shapes[pid]=shape
    for item in raw["generated_parts"]:
        pid=item["part_id"]; shape=generated_shape(item)
        if not shape.isValid() or len(shape.Solids())!=1: raise RuntimeError(f"invalid generated part {pid}")
        path=a.output_root/f"{pid}.step"; cq.exporters.export(shape,str(path),exportType="STEP"); canonicalize(path); shapes[pid]=shape
    density_map=raw["densities_kg_per_m3"]
    for pid,shape in shapes.items():
        density=density_map.get(pid,density_map["default"]); center=[x/MM for x in shape.Center().toTuple()]; mass=shape.Volume()*1e-9*density
        records.append({"part_id":pid,"step_file":f"{pid}.step","step_sha256":sha(a.output_root/f"{pid}.step"),"valid":shape.isValid(),"solid_count":len(shape.Solids()),"volume_m3":shape.Volume()*1e-9,"density_kg_per_m3":density,"mass_kg":mass,"centre_of_mass_m":center,"inertia_at_com_kg_m2":inertia(shape,density)})
    records.sort(key=lambda x:x["part_id"]); allowed={tuple(sorted(x)) for x in raw["allowed_pairs"]}; ids=sorted(shapes); max_overlap=0.0; clearances=[]; pair_clearance=[]
    for i,first in enumerate(ids):
        for second in ids[i+1:]:
            overlap=shapes[first].intersect(shapes[second]).Volume()*1e-9; distance=float(shapes[first].distance(shapes[second]))/MM; is_allowed=tuple(sorted((first,second))) in allowed
            if not is_allowed: max_overlap=max(max_overlap,overlap); clearances.append(distance)
            pair_clearance.append({"parts":[first,second],"allowed":is_allowed,"clearance_m":distance,"overlap_m3":overlap})
    total_mass=sum(r["mass_kg"] for r in records); com=[sum(r["mass_kg"]*r["centre_of_mass_m"][i] for r in records)/total_mass for i in range(3)]; total_i=[[0.0]*3 for _ in range(3)]
    for r in records:
        d=[r["centre_of_mass_m"][i]-com[i] for i in range(3)]; d2=sum(x*x for x in d)
        for i in range(3):
            for j in range(3): total_i[i][j]+=r["inertia_at_com_kg_m2"][i][j]+r["mass_kg"]*((d2 if i==j else 0)-d[i]*d[j])
    compound=cq.Compound.makeCompound([shapes[x] for x in ids]); assembly=a.output_root/"load_structure_integration_001.step"; cq.exporters.export(compound,str(assembly),exportType="STEP"); canonicalize(assembly)
    service_exclusions={"energy_store","energy_mount_adapter","converter_housing","support_block"}; service=[]
    store=shapes["energy_store"]
    for step in range(1,17):
        moved=store.translate((-0.01*step*MM,0,0)); service.extend(float(moved.distance(shape))/MM for pid,shape in shapes.items() if pid not in service_exclusions)
    route_ids={"coolant_inlet_route","coolant_outlet_route"}; routing=[]
    for rid in route_ids: routing.extend(float(shapes[rid].distance(shape))/MM for pid,shape in shapes.items() if pid not in route_ids|{"converter_housing"})
    integration_ids={p["part_id"] for p in raw["generated_parts"]}; ground=-0.139; ground_clear=min(shapes[x].BoundingBox().zmin/MM-ground for x in integration_ids)
    body={"candidate_id":raw["candidate_id"],"config_sha256":validation["config_sha256"],"hidden_geometry_repair":False,"part_count":len(records),"parts":records,"assembly":{"step_file":assembly.name,"step_sha256":sha(assembly),"solid_count":len(compound.Solids()),"valid":compound.isValid()},"pair_clearance":pair_clearance,"maximum_overlap_m3":max_overlap,"minimum_forbidden_clearance_m":min(clearances),"service_clearance_m":min(service),"routing_clearance_m":min(routing),"integration_ground_clearance_m":ground_clear,"total_mass_kg":total_mass,"centre_of_mass_m":com,"inertia_tensor_kg_m2":total_i}; manifest={**body,"manifest_sha256":canonical_sha256(body)}; mpath=a.output_root/"geometry_manifest.json"; write(mpath,manifest)
    env=os.environ.copy(); env.update({"FORMULA_ULTIMATE_W087_MANIFEST":str(mpath),"FORMULA_ULTIMATE_W087_STEP_ROOT":str(a.output_root),"FORMULA_ULTIMATE_W087_REPORT":str(a.output_root/"freecad_report.json"),"FORMULA_ULTIMATE_W087_FCSTD":str(a.output_root/"load_structure_integration_001.FCStd")}); proc=subprocess.run([str(a.freecad_python),str(ROOT/"scripts/candidates/inspect_load_structure_integration_freecad.py")],cwd=ROOT,env=env,text=True,capture_output=True)
    if proc.returncode!=0: raise RuntimeError(proc.stderr or proc.stdout)
    freecad=json.loads((a.output_root/"freecad_report.json").read_text(encoding="utf-8")); evaluation=evaluate(raw,manifest,freecad,upstream); write(a.output_root/"evaluation.json",evaluation)
    result_body={"status":"partial","candidate_id":raw["candidate_id"],"candidate_verdict":evaluation["candidate_verdict"],"design_use_allowed":False,"config_sha256":validation["config_sha256"],"manifest_sha256":manifest["manifest_sha256"],"assembly_step_sha256":manifest["assembly"]["step_sha256"],"freecad_report_sha256":freecad["report_sha256"],"evaluation_sha256":evaluation["evaluation_sha256"],"blockers":evaluation["blockers"]}; result={**result_body,"result_sha256":canonical_sha256(result_body)}; write(a.output_root/"result.json",result)
    replay=None
    if a.replay_reference:
        ref=json.loads(a.replay_reference.read_text(encoding="utf-8")); replay=ref==result; rb={"status":"passed" if replay else "failed","exact":replay,"reference_result_sha256":ref.get("result_sha256"),"replay_result_sha256":result["result_sha256"]}; write(a.output_root/"replay.json",{**rb,"replay_sha256":canonical_sha256(rb)})
        if not replay: raise RuntimeError("replay mismatch")
    print(json.dumps({"status":"partial","part_count":len(records),"assembly_solid_count":len(compound.Solids()),"maximum_overlap_m3":max_overlap,"minimum_forbidden_clearance_m":min(clearances),"service_clearance_m":min(service),"routing_clearance_m":min(routing),"ground_clearance_m":ground_clear,"motion_interface":evaluation["motion_interface"],"blockers":evaluation["blockers"],"result_sha256":result["result_sha256"],"replay_exact":replay},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
