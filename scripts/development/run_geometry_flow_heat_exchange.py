"""Execute Work 121 geometry-derived flow/heat evidence."""
from __future__ import annotations
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/"src"
for item in (ROOT,SRC):
    if str(item) not in sys.path: sys.path.insert(0,str(item))
from formula_ultimate.physics.geometry_flow_heat_exchange import GeometryFlowViolation,canonical_sha256,external_flow,internal_passage,mesh_bounds,validate_protocol  # noqa:E402
def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def write(path,value): path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def gmsh_vertices(path):
    lines=Path(path).read_text(encoding="utf-8").splitlines()
    try: start=lines.index("$Nodes")+1; count=int(lines[start]); rows=lines[start+1:start+1+count]
    except (ValueError,IndexError) as exc: raise GeometryFlowViolation("invalid Gmsh node section") from exc
    return [[float(value) for value in row.split()[1:4]] for row in rows]
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--config",type=Path,required=True); parser.add_argument("--output-root",type=Path,required=True); parser.add_argument("--replay-reference",type=Path); args=parser.parse_args(); config=(ROOT/args.config).resolve() if not args.config.is_absolute() else args.config; out=(ROOT/args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root; out.mkdir(parents=True,exist_ok=True)
    raw=read(config); validation=validate_protocol(raw)
    for dependency in raw["dependencies"]:
        if sha(ROOT/dependency["contract_path"])!=dependency["contract_sha256"]: raise GeometryFlowViolation("stale dependency contract")
        if subprocess.run(["git","cat-file","-e",dependency["commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise GeometryFlowViolation("missing dependency commit")
    inputs={}
    for item in raw["inputs"]:
        result=read(ROOT/item["path"])
        if result.get("result_sha256")!=item["result_sha256"]: raise GeometryFlowViolation(f"stale Work {item['work']} result")
        inputs[item["work"]]=result
    mesh_path=ROOT/raw["mesh_source"]["path"]
    if sha(mesh_path)!=raw["mesh_source"]["sha256"]: raise GeometryFlowViolation("stale Work 110 mesh")
    source_level=inputs[110]["body"]["routes"][raw["mesh_source"]["route_id"]][-1]
    if source_level["mesh_sha256"]!=raw["mesh_source"]["sha256"] or raw["mesh_source"]["required_surface"] not in source_level["mesh"]["boundary_element_counts"]: raise GeometryFlowViolation("mesh identity or external boundary missing")
    bounds=mesh_bounds(gmsh_vertices(mesh_path)); projected_area=bounds["extents_m"][1]*bounds["extents_m"][2]
    work115_source=inputs[115]["body"]["levels"][-1]["supplied_energy_j"]/5.0
    if work115_source!=raw["internal"]["source_heat_w"]: raise GeometryFlowViolation("Work 115 heat-source identity mismatch")
    internal_levels=[]
    for segments in raw["refinement"]["internal_segments"]:
        level=internal_passage(raw,segments); profile=level.pop("profile"); profile_path=out/f"internal_profile_{segments}.json"; write(profile_path,profile); level["profile_file"]=profile_path.name; level["profile_sha256"]=canonical_sha256(profile)
        if abs(level["heat_residual_w"])>raw["tolerances"]["heat_residual_absolute_w"]: raise GeometryFlowViolation("internal heat conservation failed")
        internal_levels.append(level)
    if internal_levels[-1]["heat_capacity_relative_error"]>raw["tolerances"]["internal_last_error"]: raise GeometryFlowViolation("internal refinement gate failed")
    if not all(internal_levels[index+1]["heat_capacity_relative_error"]<internal_levels[index]["heat_capacity_relative_error"] for index in range(len(internal_levels)-1)): raise GeometryFlowViolation("internal refinement is not monotonic")
    diameter_map=[]
    for diameter in raw["refinement"]["diameter_mutations_m"]:
        value=internal_passage(raw,raw["refinement"]["internal_segments"][-1],diameter_m=diameter); value.pop("profile"); diameter_map.append(value)
    if len({x["pressure_drop_pa"] for x in diameter_map})!=len(diameter_map): raise GeometryFlowViolation("passage mutation was not causal")
    external_levels=[]
    for width in raw["refinement"]["far_field_widths_m"]:
        level=external_flow(raw,projected_area,width)
        if abs(level["force_residual_n"])>raw["tolerances"]["force_residual_absolute_n"]: raise GeometryFlowViolation("external force conservation failed")
        external_levels.append(level)
    if external_levels[-1]["domain_relative_error"]>raw["tolerances"]["external_last_domain_relative"]: raise GeometryFlowViolation("external domain-sensitivity gate failed")
    area_map=[external_flow(raw,projected_area,raw["refinement"]["far_field_widths_m"][-1],area_scale=scale) for scale in raw["refinement"]["external_area_scales"]]
    if len({x["drag_force_n"] for x in area_map})!=len(area_map): raise GeometryFlowViolation("external geometry mutation was not causal")
    blocked=internal_passage(raw,40,blocked=True); zero_flow=internal_passage(raw,40,volume_flow_m3_s=0); zero_source=internal_passage(raw,40,source_heat_w=0); zero_speed=external_flow(raw,projected_area,2,speed_m_s=0)
    controls={"blocked_passage":blocked,"zero_flow":zero_flow,"zero_heat_source":{k:v for k,v in zero_source.items() if k!="profile"},"zero_external_speed":zero_speed,"diameter_mutations":diameter_map,"external_area_mutations":area_map}
    body={"status":"passed_bounded_scopes","claim_scope":"separately gated synthetic laminar circular-passage heat/pressure and incompressible quadratic-drag references derived from registered geometry; not arbitrary cooling, CFD, whole-car aerodynamics, or physical validation","validation":validation,"dependencies":raw["dependencies"],"input_result_sha256":{str(k):v["result_sha256"] for k,v in sorted(inputs.items())},"geometry_evidence":{"work110_mesh_sha256":sha(mesh_path),"node_bounds":bounds,"projected_yz_area_m2":projected_area,"boundary_element_count":source_level["mesh"]["boundary_element_counts"][raw["mesh_source"]["required_surface"]]},"upstream":{"work115_heat_source_w":work115_source,"work116_material_claim":inputs[116]["body"]["candidate"]["claim_eligibility"]},"internal_scope":{"status":"passed","regime":"laminar circular passage only","levels":internal_levels},"external_scope":{"status":"passed","regime":raw["external"]["regime"],"levels":external_levels},"controls":controls,"coverage":raw["coverage"],"assembly_handoff":{"wall_pressure_force_n":internal_levels[-1]["wall_pressure_force_n"],"heat_rejected_w":internal_levels[-1]["heat_rejected_w"],"external_pressure_force_n":external_levels[-1]["pressure_force_n"],"external_shear_force_n":external_levels[-1]["shear_force_n"],"external_yaw_moment_n_m":external_levels[-1]["yaw_moment_n_m"]},"review":{"supporting_evidence":["Work 110 mesh identity and external boundary were checked before deriving projected bounds","internal pressure/heat references passed conservation and three-level refinement","external pressure/shear force accounting and far-field sensitivity passed independently"],"contradicting_evidence":["both fluid-property/closure sets and the external drag coefficient are synthetic"],"alternative_explanations":["bounding-box projected area and constant coefficients suppress local shape and flow-field effects"],"missing_evidence":["conforming fluid mesh","measured properties and closures","turbulence, cavitation and compressibility","conjugate 3D CFD","whole-car aerodynamic validation","physical validation"],"confidence":"high for analytic reference equations; none for real cooling or vehicle aerodynamics"}}
    result={"body":body,"result_sha256":canonical_sha256(body)}; write(out/"result.json",result)
    if args.replay_reference:
        reference=(ROOT/args.replay_reference).resolve() if not args.replay_reference.is_absolute() else args.replay_reference; prior=read(reference); exact=prior.get("result_sha256")==result["result_sha256"]; write(out/"replay.json",{"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"],"exact":exact})
        if not exact: raise GeometryFlowViolation("replay differs from reference")
    print(json.dumps({"status":"passed","result_sha256":result["result_sha256"],"projected_area_m2":projected_area,"pressure_drop_pa":internal_levels[-1]["pressure_drop_pa"],"drag_force_n":external_levels[-1]["drag_force_n"]},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
