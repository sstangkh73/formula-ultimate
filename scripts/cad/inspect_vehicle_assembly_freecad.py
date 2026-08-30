"""Independently measure Work 047 STEP artifacts with FreeCAD."""
from __future__ import annotations
import hashlib,json,math,os,sys
import FreeCAD as App
import Part
def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()
def aggregate(rows):
    mass=math.fsum(x["mass_kg"] for x in rows); centre=[math.fsum(x["mass_kg"]*x["centre_of_mass_m"][i] for x in rows)/mass for i in range(3)]; I=[0.]*6
    for x in rows:
        dx,dy,dz=[x["centre_of_mass_m"][i]-centre[i] for i in range(3)]; m=x["mass_kg"]; q=(m*(dy*dy+dz*dz),m*(dx*dx+dz*dz),m*(dx*dx+dy*dy),-m*dx*dy,-m*dx*dz,-m*dy*dz)
        I=[I[i]+x["centroidal_inertia_kg_m2"][i]+q[i] for i in range(6)]
    return {"mass_kg":mass,"centre_of_mass_m":centre,"inertia_kg_m2":I}
def main():
    if len(sys.argv)<4: raise SystemExit("pass MANIFEST CONFIG OUTPUT")
    manifest_path,config_path,output_path=sys.argv[-3:]; manifest=json.load(open(manifest_path,encoding="utf-8")); config=json.load(open(config_path,encoding="utf-8")); rows=[]
    for record in manifest["components"]:
        shape=Part.Shape(); shape.read(record["step_path"])
        if len(shape.Solids)!=1 or not shape.isValid(): raise RuntimeError("FreeCAD component import is invalid")
        solid=shape.Solids[0]; density=float(record["density_kg_per_m3"]); volume=solid.Volume*1e-9; mass=volume*density; c=solid.CenterOfMass; M=solid.MatrixOfInertia
        inertia=[M.A11*density*1e-15,M.A22*density*1e-15,M.A33*density*1e-15,M.A12*density*1e-15,M.A13*density*1e-15,M.A23*density*1e-15]
        rows.append({"component_id":record["component_id"],"step_sha256":sha(record["step_path"]),"valid":True,"solid_count":1,"volume_m3":volume,"mass_kg":mass,"centre_of_mass_m":[c.x*1e-3,c.y*1e-3,c.z*1e-3],"centroidal_inertia_kg_m2":inertia})
    assembly=Part.Shape(); assembly.read(manifest["assembly"]["step_path"])
    if len(assembly.Solids)!=len(rows) or not assembly.isValid(): raise RuntimeError("FreeCAD assembly solid count/validity failed")
    report={"status":"passed","freecad_version":".".join(str(x) for x in App.Version()[:3]),"components":rows,"mass_properties":aggregate(rows),"assembly":{"step_sha256":sha(manifest["assembly"]["step_path"]),"solid_count":len(assembly.Solids),"valid":True,"volume_m3":assembly.Volume*1e-9}}
    os.makedirs(os.path.dirname(output_path),exist_ok=True); json.dump(report,open(output_path,"w",encoding="utf-8"),indent=2,sort_keys=True); open(output_path,"a",encoding="utf-8").write("\n"); print(json.dumps({"status":"passed","solid_count":len(rows),"mass_kg":report["mass_properties"]["mass_kg"]},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
