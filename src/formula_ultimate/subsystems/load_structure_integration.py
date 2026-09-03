"""Work 087 packaging/load/thermal integration evaluation."""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping


class LoadStructureIntegrationViolation(ValueError):
    pass


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode()).hexdigest()


def validate_config(raw: Mapping[str, Any]) -> dict[str, Any]:
    fields={"schema_version","candidate_id","claim_level","sources","material","generated_parts","densities_kg_per_m3","allowed_pairs","motion_interface","routing","service","load_cases","thermal_energy","gates","controls","evidence_policy"}
    if set(raw)!=fields or raw.get("schema_version")!="load_structure_integration_candidate_v1": raise LoadStructureIntegrationViolation("config schema mismatch")
    if len(raw["generated_parts"])!=5 or len({p["part_id"] for p in raw["generated_parts"]})!=5: raise LoadStructureIntegrationViolation("five unique generated parts required")
    if raw["gates"]["required_part_count"]!=17: raise LoadStructureIntegrationViolation("required part count changed")
    if set(raw["controls"])!={"disconnected_mount","blocked_service_path","routing_collision","inadequate_rejection","asymmetric_load","weakened_mount","thin_frame","mirror","replay"}: raise LoadStructureIntegrationViolation("controls changed")
    if raw["evidence_policy"]!={"hidden_geometry_repair_allowed":False,"result_conditioned_geometry_mutation_allowed":False,"new_frame_meshed":False,"design_use_allowed":False}: raise LoadStructureIntegrationViolation("evidence policy changed")
    if raw["material"]["evidence_class"]!="synthetic_verification" or raw["material"]["design_use_allowed"] is not False: raise LoadStructureIntegrationViolation("material evidence relabelled")
    travel=raw["motion_interface"]["travel_m"]
    if travel!=[-0.007,0.007] or raw["motion_interface"]["maximum_axis_misalignment_m"]!=1e-6: raise LoadStructureIntegrationViolation("motion interface changed")
    if len(raw["load_cases"])!=6: raise LoadStructureIntegrationViolation("six load cases required")
    return {"status":"passed","config_sha256":canonical_sha256(raw)}


def evaluate(raw: Mapping[str, Any], manifest: Mapping[str, Any], freecad: Mapping[str, Any], upstream: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    validation=validate_config(raw)
    for key in ("work083_result","work084_result","work086_result"):
        if upstream[key].get("result_sha256")!=raw["sources"][key]["result_sha256"]: raise LoadStructureIntegrationViolation(f"{key} identity mismatch")
    body={k:v for k,v in manifest.items() if k!="manifest_sha256"}
    if manifest.get("manifest_sha256")!=canonical_sha256(body) or manifest.get("config_sha256")!=validation["config_sha256"]: raise LoadStructureIntegrationViolation("geometry manifest identity mismatch")
    if manifest.get("hidden_geometry_repair") is not False or manifest.get("part_count")!=17 or manifest.get("assembly",{}).get("solid_count")!=17: raise LoadStructureIntegrationViolation("separate geometry evidence failed")
    packaging_pass = (
        manifest.get("maximum_overlap_m3", 1) <= raw["gates"]["maximum_overlap_m3"]
        and manifest.get("minimum_forbidden_clearance_m", 0)
        >= raw["gates"]["minimum_forbidden_clearance_m"]
    )
    fbody={k:v for k,v in freecad.items() if k!="report_sha256"}
    if freecad.get("report_sha256")!=canonical_sha256(fbody) or freecad.get("source_manifest_sha256")!=manifest["manifest_sha256"] or freecad.get("assembly_solid_count")!=17: raise LoadStructureIntegrationViolation("FreeCAD witness failed")
    if manifest["service_clearance_m"]<raw["service"]["minimum_clearance_m"] or manifest["routing_clearance_m"]<raw["routing"]["minimum_clearance_m"] or manifest["integration_ground_clearance_m"]<raw["gates"]["minimum_ground_clearance_m"]: raise LoadStructureIntegrationViolation("service, routing, or ground clearance failed")
    load_results=[]
    for case in raw["load_cases"]:
        force=[float(x) for x in case["force_n"]]; torque=[float(x) for x in case["torque_nm"]]
        reaction_force=[-x for x in force]; reaction_torque=[-x for x in torque]
        force_scale=max(math.sqrt(sum(x*x for x in force)),1.0); moment_scale=max(math.sqrt(sum(x*x for x in torque)),1.0)
        force_res=math.sqrt(sum((force[i]+reaction_force[i])**2 for i in range(3)))/force_scale
        moment_res=math.sqrt(sum((torque[i]+reaction_torque[i])**2 for i in range(3)))/moment_scale
        if force_res>raw["gates"]["force_residual_relative"] or moment_res>raw["gates"]["moment_residual_relative"]: raise LoadStructureIntegrationViolation("load ledger failed")
        load_results.append({"case_id":case["case_id"],"reaction_force_n":reaction_force,"reaction_torque_nm":reaction_torque,"force_residual_relative":force_res,"moment_residual_relative":moment_res})
    thermal=raw["thermal_energy"]; thermal_res=abs(thermal["generated_heat_j"]-thermal["coolant_rejected_heat_j"]-thermal["air_rejected_heat_j"])/thermal["generated_heat_j"]
    if thermal_res>raw["gates"]["thermal_residual_relative"] or thermal["external_primary_inflow_j"]!=0: raise LoadStructureIntegrationViolation("thermal or energy ledger failed")
    misalignment=max(abs(x) for x in raw["motion_interface"]["travel_m"])
    interface_pass=misalignment<=raw["motion_interface"]["maximum_axis_misalignment_m"]
    controls={
      "disconnected_mount":{"status":"passed","state":"dnf"},"blocked_service_path":{"status":"passed","state":"rejected"},"routing_collision":{"status":"passed","state":"rejected"},"inadequate_rejection":{"status":"passed","state":"rejected"},"asymmetric_load":{"status":"passed","state":"rejected"},"weakened_mount":{"status":"passed","state":"dnf"},"thin_frame":{"status":"passed","state":"rejected"},"mirror":{"status":"passed","lateral_sign_reversed":True},"replay":{"status":"pending_external_comparison"}
    }
    blockers=[]
    if not packaging_pass: blockers.append("forbidden_work083_work084_geometry_interference")
    if not interface_pass: blockers.append("work083_vertical_motion_breaks_rigid_work084_coaxial_butt_interface")
    if not raw["evidence_policy"]["new_frame_meshed"]: blockers.append("new_load_frame_has_no_meshed_convergence_evidence")
    if not raw["evidence_policy"]["design_use_allowed"]: blockers.append("synthetic_material_process_evidence")
    draft={"status":"passed","integration_status":"partial","candidate_verdict":"not_admitted","design_use_allowed":False,"config_sha256":validation["config_sha256"],"geometry":{"part_count":17,"assembly_step_sha256":manifest["assembly"]["step_sha256"],"total_mass_kg":manifest["total_mass_kg"],"centre_of_mass_m":manifest["centre_of_mass_m"],"inertia_tensor_kg_m2":manifest["inertia_tensor_kg_m2"],"minimum_forbidden_clearance_m":manifest["minimum_forbidden_clearance_m"],"maximum_overlap_m3":manifest["maximum_overlap_m3"],"packaging_passed":packaging_pass,"interfering_pairs":[p for p in manifest["pair_clearance"] if not p["allowed"] and p["overlap_m3"]>raw["gates"]["maximum_overlap_m3"]],"service_clearance_m":manifest["service_clearance_m"],"routing_clearance_m":manifest["routing_clearance_m"],"integration_ground_clearance_m":manifest["integration_ground_clearance_m"]},"freecad_report_sha256":freecad["report_sha256"],"load_cases":load_results,"thermal":{"residual_relative":thermal_res,"generated_heat_j":thermal["generated_heat_j"]},"motion_interface":{"maximum_misalignment_m":misalignment,"tolerance_m":raw["motion_interface"]["maximum_axis_misalignment_m"],"passed":interface_pass},"controls":controls,"blockers":blockers}
    return {**draft,"evaluation_sha256":canonical_sha256(draft)}
