"""Create a seventeen-object FreeCAD witness from exact Work 087 STEP files."""
from __future__ import annotations
import hashlib,json,os
from pathlib import Path
import sys
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/"src"))
from formula_ultimate.subsystems.load_structure_integration import canonical_sha256
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def main():
    manifest=json.loads(Path(os.environ["FORMULA_ULTIMATE_W087_MANIFEST"]).read_text(encoding="utf-8")); root=Path(os.environ["FORMULA_ULTIMATE_W087_STEP_ROOT"]); report_path=Path(os.environ["FORMULA_ULTIMATE_W087_REPORT"]); fcstd=Path(os.environ["FORMULA_ULTIMATE_W087_FCSTD"])
    doc=App.newDocument("LoadStructureIntegration001"); records=[]
    for part in manifest["parts"]:
        path=root/part["step_file"]
        if sha(path)!=part["step_sha256"]: raise RuntimeError(f"identity mismatch {part['part_id']}")
        shape=Part.Shape(); shape.read(os.fspath(path))
        if not shape.isValid() or len(shape.Solids)!=1: raise RuntimeError(f"invalid separate solid {part['part_id']}")
        obj=doc.addObject("Part::Feature",part["part_id"]); obj.Label=part["part_id"]; obj.Shape=shape.Solids[0]
        records.append({"part_id":part["part_id"],"step_sha256":part["step_sha256"],"valid":True,"solid_count":1,"volume_m3":float(shape.Volume)*1e-9})
    apath=root/manifest["assembly"]["step_file"]
    if sha(apath)!=manifest["assembly"]["step_sha256"]: raise RuntimeError("assembly identity mismatch")
    assembly=Part.Shape(); assembly.read(os.fspath(apath))
    if not assembly.isValid() or len(assembly.Solids)!=17: raise RuntimeError("assembly did not retain seventeen solids")
    doc.recompute(); fcstd.parent.mkdir(parents=True,exist_ok=True); doc.saveAs(os.fspath(fcstd))
    version=App.Version(); body={"source_manifest_sha256":manifest["manifest_sha256"],"freecad_version":".".join(str(x) for x in version[:3]),"occt_version":str(getattr(Part,"OCC_VERSION","unavailable")),"hidden_geometry_repair":False,"parts":records,"assembly_solid_count":len(assembly.Solids),"assembly_step_sha256":manifest["assembly"]["step_sha256"]}; report={**body,"report_sha256":canonical_sha256(body)}; report_path.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8"); App.closeDocument(doc.Name); print(json.dumps({"status":"passed","part_count":len(records),"report_sha256":report["report_sha256"]},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
