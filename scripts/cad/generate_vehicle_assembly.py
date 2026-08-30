"""Generate deterministic per-component and assembly STEP evidence for Work 047."""
from __future__ import annotations
import argparse,hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/"src"))
import cadquery as cq
from formula_ultimate.topology import declaration_sha256,from_mapping,validate
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def canonicalize(p):
    text=p.read_text(encoding="ascii"); updated,count=re.subn(r"(FILE_NAME\('[^']*',)'[^']*'",r"\1'1970-01-01T00:00:00'",text,count=1)
    if count!=1: raise RuntimeError("STEP timestamp missing or ambiguous")
    p.write_text(updated,encoding="ascii",newline="\n")
def shape_for(c):
    mm=1000.; x,y,z=(v*mm for v in c.position)
    if c.kind=="box": shape=cq.Workplane("XY").box(*(v*mm for v in c.dims)).val()
    else: shape=cq.Solid.makeCylinder(c.dims[0]*mm,c.dims[1]*mm,cq.Vector(0,0,-c.dims[1]*mm/2))
    return shape.translate((x,y,z))
def main():
    p=argparse.ArgumentParser(); p.add_argument("--config",type=Path,required=True); p.add_argument("--output-root",type=Path,required=True); p.add_argument("--manifest",type=Path,required=True); a=p.parse_args()
    raw=json.loads(a.config.read_text(encoding="utf-8")); assembly=from_mapping(raw); validation=validate(assembly); a.output_root.mkdir(parents=True,exist_ok=True)
    shapes=[]; records=[]
    for component in sorted(assembly.components,key=lambda x:x.component_id):
        shape=shape_for(component)
        if not shape.isValid() or len(shape.Solids())!=1: raise RuntimeError(f"component {component.component_id} is not one valid solid")
        path=a.output_root/f"{component.component_id}.step"; cq.exporters.export(shape,str(path),exportType="STEP"); canonicalize(path); shapes.append(shape)
        records.append({"component_id":component.component_id,"material_id":component.material_id,"density_kg_per_m3":component.density,"volume_m3":shape.Volume()*1e-9,"centre_of_mass_m":[v*1e-3 for v in shape.Center().toTuple()],"step_sha256":sha(path),"step_path":str(path),"valid":True,"solid_count":1})
    compound=cq.Compound.makeCompound(shapes); assembly_path=a.output_root/"assembly.step"; cq.exporters.export(compound,str(assembly_path),exportType="STEP"); canonicalize(assembly_path)
    manifest={"status":"passed","protocol_id":assembly.protocol_id,"candidate_id":assembly.candidate_id,"grammar_version":raw["grammar_version"],"declaration_sha256":declaration_sha256(raw),"cadquery_version":cq.__version__,"components":records,"assembly":{"step_path":str(assembly_path),"step_sha256":sha(assembly_path),"solid_count":len(compound.Solids()),"valid":compound.isValid(),"volume_m3":compound.Volume()*1e-9},"grammar_validation":validation}
    a.manifest.parent.mkdir(parents=True,exist_ok=True); a.manifest.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8"); print(json.dumps({"status":"passed","assembly_sha256":manifest["assembly"]["step_sha256"],"solid_count":manifest["assembly"]["solid_count"]},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
