"""Execute Work 116 material provenance and scoped failure evidence."""
from __future__ import annotations
import argparse,copy,hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/"src"
for x in (ROOT,SRC):
    if str(x) not in sys.path: sys.path.insert(0,str(x))
from formula_ultimate.structural.material_failure_scope import MaterialFailureViolation,applicability,canonical_sha256,combine_without_law,euler_buckling,validate_protocol,yield_margin  # noqa:E402
def read(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def write(p,v): p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rejected(action,phrase):
    try: action()
    except MaterialFailureViolation as exc:
        if phrase not in str(exc): raise
        return {"status":"rejected","reason":str(exc)}
    raise MaterialFailureViolation("negative control accepted")
def main():
    p=argparse.ArgumentParser(); p.add_argument("--config",type=Path,required=True); p.add_argument("--output-root",type=Path,required=True); p.add_argument("--replay-reference",type=Path); a=p.parse_args(); config=(ROOT/a.config).resolve() if not a.config.is_absolute() else a.config; out=(ROOT/a.output_root).resolve() if not a.output_root.is_absolute() else a.output_root; out.mkdir(parents=True,exist_ok=True); raw=read(config); validation=validate_protocol(raw)
    for d in raw["dependencies"]:
        if sha(ROOT/d["contract_path"])!=d["contract_sha256"]: raise MaterialFailureViolation("stale dependency contract")
        if subprocess.run(["git","cat-file","-e",d["commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise MaterialFailureViolation("missing dependency commit")
    inputs={}
    for item in raw["inputs"]:
        evidence=read(ROOT/item["path"])
        if evidence["result_sha256"]!=item["result_sha256"]: raise MaterialFailureViolation("stale input result")
        inputs[item["work"]]=evidence
    stress=inputs[111]["body"]["unfamiliar_levels"][-1]["p90_von_mises_stress_pa"]; dynamic_load=inputs[114]["body"]["levels"][-1]["maximum_contact_force_n"]; temperature=inputs[115]["body"]["levels"][-1]["male_final_temperature_k"]
    if abs(temperature-raw["acceptance"]["candidate_temperature_k"])>1e-12: raise MaterialFailureViolation("registered candidate temperature is stale")
    candidate=raw["materials"]["synthetic_joint_aluminium"]; eligibility=applicability(candidate,temperature,raw["acceptance"]["candidate_strain_rate_1_s"],raw["acceptance"]["candidate_process"]); candidate_yield=yield_margin(candidate,stress)
    yf=raw["yield_fixture"]; yield_controls={"safe":yield_margin(candidate,yf["safe_stress_pa"]),"failed":yield_margin(candidate,yf["failed_stress_pa"])}
    ref=raw["materials"]["analytic_column_reference"]; bf=raw["buckling_fixture"]; g=bf["geometry"]; inertia=g["width_m"]*g["height_m"]**3/12; analytic=math.pi**2*ref["youngs_modulus_pa"]*inertia/(g["effective_length_factor"]*g["length_m"])**2; buckling=[]
    for imperfection in bf["imperfections_m"]: buckling.append({"imperfection_m":imperfection,**euler_buckling(ref,g,analytic*bf["safe_load_fraction"],imperfection)})
    if abs(buckling[0]["euler_critical_load_n"]-analytic)/analytic>raw["acceptance"]["reference_relative_error"] or any(b["imperfection_adjusted_lower_capacity_n"]>=a["imperfection_adjusted_lower_capacity_n"] for a,b in zip(buckling,buckling[1:])): raise MaterialFailureViolation("Euler reference or imperfection sensitivity failed")
    buckling_failed=euler_buckling(ref,g,analytic*bf["failed_load_fraction"],0)
    controls={"yield":yield_controls,"buckling_safe_imperfection":buckling,"buckling_failed":buckling_failed,"temperature_range":rejected(lambda:applicability(candidate,450,.001,"unspecified_fixture"),"temperature"),"rate_range":rejected(lambda:applicability(candidate,300,1.,"unspecified_fixture"),"strain rate"),"process":rejected(lambda:applicability(candidate,300,.001,"forged"),"process"),"synthetic_relabel":rejected(lambda:applicability(candidate,300,.001,"unspecified_fixture","measured_survival"),"relabeling"),"mixture":rejected(lambda:combine_without_law([candidate,candidate]),"mixture")}
    body={"status":"passed","claim_scope":"mathematical yield/buckling references and diagnostic synthetic candidate margins only; not physical survival","validation":validation,"dependencies":raw["dependencies"],"input_evidence":{"work111_p90_stress_pa":stress,"work114_maximum_dynamic_contact_force_n":dynamic_load,"work115_temperature_k":temperature,"result_sha256s":{str(k):v["result_sha256"] for k,v in inputs.items()}},"candidate":{"eligibility":eligibility,"yield_diagnostic":candidate_yield,"claim_eligibility":"blocked_no_measured_process-qualified_material"},"controls":controls,"extension_slots":raw["extension_slots"],"missing_domains":["measured process-qualified yield law","geometry-applicable buckling member mapping","fatigue","fracture","wear","manufacturing variability","physical correlation"],"review":{"supporting_evidence":["yield and Euler references reproduced safe/failed fixtures","imperfection monotonically reduced column capacity","temperature/rate/process/provenance/mixture controls failed closed"],"contradicting_evidence":["candidate inputs and strength are synthetic rather than measured"],"alternative_explanations":["large diagnostic margin primarily reflects the low Level-0 stress fixture"],"missing_evidence":["measured coupons","process qualification","fatigue/fracture/wear","physical validation"],"confidence":"high for applicability gating and analytic references; none for candidate physical survival"}}
    result={"body":body,"result_sha256":canonical_sha256(body)}; write(out/"result.json",result)
    if a.replay_reference:
        refp=(ROOT/a.replay_reference).resolve() if not a.replay_reference.is_absolute() else a.replay_reference; prior=read(refp); exact=prior.get("result_sha256")==result["result_sha256"]; write(out/"replay.json",{"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"],"exact":exact})
        if not exact: raise MaterialFailureViolation("replay differs from reference")
    print(json.dumps({"status":"passed","result_sha256":result["result_sha256"],"candidate_claim":body["candidate"]["claim_eligibility"]},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
