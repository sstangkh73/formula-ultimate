"""Run Work 085 arbitrary-axis force/torque structural cases with Gmsh/CalculiX."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.components.engineering_contracts import validate_material_record  # noqa: E402
from formula_ultimate.structural.acceptance import MeshData, parse_msh2  # noqa: E402
from formula_ultimate.structural.generalized_coupling import (  # noqa: E402
    adjudicate,
    canonical_sha256,
    validate_config,
)
from formula_ultimate.structural.loaded_interface import parse_loaded_interface_dat, triangle_area  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_frd_sha(path: Path) -> str:
    text = path.read_text(encoding="ascii", errors="strict")
    normalized, count = re.subn(r"(?m)^(\s*1UTIME\s+)\S+\s*$", r"\g<1>00:00:00", text)
    if count != 1:
        raise RuntimeError("CalculiX FRD time metadata is missing or ambiguous")
    return hashlib.sha256(normalized.encode("ascii")).hexdigest()


def run(command: list[str], cwd: Path) -> tuple[int, str, str, int]:
    started = time.time_ns()
    process = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    return process.returncode, process.stdout, process.stderr, started


def scaled_mesh(path: Path) -> MeshData:
    raw = parse_msh2(path)
    return MeshData(
        {node: tuple(value * 1e-3 for value in xyz) for node, xyz in raw.nodes.items()},
        raw.tetrahedra,
        raw.triangles,
    )


def gmsh_geo(step_path: Path, size_m: float) -> str:
    step = step_path.as_posix().replace('"', '\\"')
    size_mm = size_m * 1000.0
    return "\n".join((
        'SetFactory("OpenCASCADE");', f'Merge "{step}";', 'vols[] = Volume{:};',
        'If (#vols[] != 1)', ' Error("expected exactly one imported volume");', 'EndIf',
        'Physical Volume(1) = {vols[0]};',
        f'Mesh.CharacteristicLengthMin = {size_mm:.17g};',
        f'Mesh.CharacteristicLengthMax = {size_mm:.17g};',
        'Mesh.Algorithm3D = 1;', 'Mesh.ElementOrder = 1;', 'Mesh.MshFileVersion = 2.2;',
        'Mesh.Binary = 0;', 'Mesh.SaveAll = 1;', '',
    ))


def _on_plane(point: tuple[float, float, float], axis: str, coordinate: float, tolerance: float) -> bool:
    return abs(point[{"x": 0, "y": 1, "z": 2}[axis]] - coordinate) <= tolerance


def map_regions(case: dict[str, Any], mesh: MeshData, tolerance: float) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], float]:
    load_triangles: list[int] = []
    load_nodes: set[int] = set()
    support_nodes: set[int] = set()
    region = case["load_region"]
    for triangle_id, connectivity in mesh.triangles.items():
        points = [mesh.nodes[node] for node in connectivity]
        if region["kind"] == "end_plane":
            matched = all(_on_plane(point, region["axis"], region["coordinate_m"], tolerance) for point in points)
        else:
            cx, cz = region["center_xz_m"]
            matched = all(abs(math.hypot(point[0] - cx, point[2] - cz) - region["radius_m"]) <= tolerance for point in points)
        if matched:
            load_triangles.append(triangle_id)
            load_nodes.update(connectivity)
        support = case["support_region"]
        if all(_on_plane(point, support["axis"], support["coordinate_m"], tolerance) for point in points):
            support_nodes.update(connectivity)
    if not load_triangles or not load_nodes:
        raise RuntimeError(f"{case['case_id']} missing declared load surface")
    if not support_nodes:
        raise RuntimeError(f"{case['case_id']} missing declared support plane")
    if load_nodes & support_nodes:
        raise RuntimeError(f"{case['case_id']} load and support regions overlap")
    area = math.fsum(triangle_area(*(mesh.nodes[node] for node in mesh.triangles[item])) for item in load_triangles)
    if area <= 0.0:
        raise RuntimeError("mapped load surface has zero area")
    return tuple(sorted(load_triangles)), tuple(sorted(load_nodes)), tuple(sorted(support_nodes)), area


def _moment_about(nodes: dict[int, tuple[float, float, float]], vectors: dict[int, tuple[float, float, float]], center: tuple[float, float, float]) -> tuple[float, float, float]:
    return (
        math.fsum((nodes[n][1]-center[1])*f[2] - (nodes[n][2]-center[2])*f[1] for n, f in vectors.items()),
        math.fsum((nodes[n][2]-center[2])*f[0] - (nodes[n][0]-center[0])*f[2] for n, f in vectors.items()),
        math.fsum((nodes[n][0]-center[0])*f[1] - (nodes[n][1]-center[1])*f[0] for n, f in vectors.items()),
    )


def consistent_load(case: dict[str, Any], mesh: MeshData, triangles: tuple[int, ...], nodes: tuple[int, ...]) -> tuple[dict[int, tuple[float, float, float]], tuple[float, float, float]]:
    weights = {node: 0.0 for node in nodes}
    for triangle_id in triangles:
        connectivity = mesh.triangles[triangle_id]
        area = triangle_area(*(mesh.nodes[node] for node in connectivity))
        for node in connectivity:
            weights[node] += area / 3.0
    total_weight = math.fsum(weights.values())
    center = tuple(math.fsum(weights[n] * mesh.nodes[n][i] for n in nodes) / total_weight for i in range(3))
    if case["load_region"]["kind"] == "end_plane":
        center = tuple(float(x) for x in case["load_region"]["center_m"])
    else:
        cx, cz = case["load_region"]["center_xz_m"]
        center = (float(cx), center[1], float(cz))
    target_force = tuple(float(x) for x in case["force_n"])
    raw = {node: [target_force[i] * weights[node] / total_weight for i in range(3)] for node in nodes}
    target_ty = float(case["torque_nm"][1])
    base_ty = _moment_about(
        mesh.nodes, {node: tuple(value) for node, value in raw.items()}, center
    )[1]
    torque_delta = target_ty - base_ty
    if abs(torque_delta) > 1e-12:
        tangent = {node: [weights[node] * (mesh.nodes[node][2]-center[2]), 0.0, -weights[node] * (mesh.nodes[node][0]-center[0])] for node in nodes}
        net = [math.fsum(tangent[node][i] for node in nodes) for i in range(3)]
        for node in nodes:
            for i in range(3):
                tangent[node][i] -= net[i] * weights[node] / total_weight
        unit_moment = _moment_about(mesh.nodes, {node: tuple(value) for node, value in tangent.items()}, center)[1]
        if abs(unit_moment) <= 1e-20:
            raise RuntimeError("loaded surface cannot realize declared torque")
        scale = torque_delta / unit_moment
        for node in nodes:
            for i in range(3):
                raw[node][i] += scale * tangent[node][i]
    # Canonicalize arithmetic noise only; all resolved load components remain.
    result = {
        node: tuple(0.0 if abs(item) < 1e-12 else item for item in value)
        for node, value in raw.items()
    }
    actual_force = tuple(math.fsum(result[node][i] for node in nodes) for i in range(3))
    actual_torque = _moment_about(mesh.nodes, result, center)
    if any(abs(actual_force[i]-target_force[i]) > 1e-9*max(abs(target_force[i]), 1.0) for i in range(3)):
        raise RuntimeError(f"consistent force construction failed: target={target_force}, actual={actual_force}")
    if abs(actual_torque[1]-target_ty) > 1e-9*max(abs(target_ty), 1.0):
        raise RuntimeError(f"consistent torque construction failed: target={target_ty}, actual={actual_torque[1]}")
    return result, center


def nset(name: str, nodes: tuple[int, ...]) -> list[str]:
    lines = [f"*NSET, NSET={name}"]
    for start in range(0, len(nodes), 16):
        lines.append(", ".join(str(node) for node in nodes[start:start+16]))
    return lines


def build_deck(config: dict[str, Any], case: dict[str, Any], mesh: MeshData, loads: dict[int, tuple[float, float, float]], load_nodes: tuple[int, ...], support_nodes: tuple[int, ...]) -> str:
    material = config["material"]
    lines = ["*HEADING", case["case_id"], "*NODE, NSET=NALL"]
    lines.extend(f"{node}, {xyz[0]:.12g}, {xyz[1]:.12g}, {xyz[2]:.12g}" for node, xyz in sorted(mesh.nodes.items()))
    lines.append("*ELEMENT, TYPE=C3D4, ELSET=EALL")
    lines.extend(f"{element}, {', '.join(str(node) for node in connectivity)}" for element, connectivity in sorted(mesh.tetrahedra.items()))
    lines.extend(nset("LOADED_IFACE", load_nodes)); lines.extend(nset("ACTIVE_SUPPORT", support_nodes)); lines.extend(nset("SUPPORT_MOUNT", support_nodes))
    lines.extend((f"*MATERIAL, NAME={material['material_id']}", "*ELASTIC", f"{material['youngs_modulus_pa']:.17g}, {material['poisson_ratio']:.17g}", "*DENSITY", f"{material['density_kg_per_m3']:.17g}", f"*SOLID SECTION, ELSET=EALL, MATERIAL={material['material_id']}", "*BOUNDARY", "ACTIVE_SUPPORT, 1, 3, 0.0", "*STEP", "*STATIC", "*CLOAD"))
    for node, vector in sorted(loads.items()):
        for dof, value in enumerate(vector, 1):
            if abs(value) > 1e-12:
                # CalculiX 2.22 free-field tokens still have a practical width
                # limit; fixed scientific notation keeps every card parseable.
                lines.append(f"{node}, {dof}, {value:.10e}")
    lines.extend(("*NODE PRINT, NSET=LOADED_IFACE", "U", "*NODE PRINT, NSET=ACTIVE_SUPPORT, TOTALS=YES", "RF", "*NODE PRINT, NSET=SUPPORT_MOUNT, TOTALS=YES", "RF", "*EL PRINT, ELSET=EALL", "S, E, ENER, ELSE", "*NODE FILE", "U, RF", "*EL FILE", "S, E", "*END STEP", ""))
    return "\n".join(lines)


def norm(value: tuple[float, float, float]) -> float:
    return math.sqrt(math.fsum(x*x for x in value))


def moment(nodes: dict[int, tuple[float, float, float]], vectors: dict[int, tuple[float, float, float]]) -> tuple[float, float, float]:
    return _moment_about(nodes, vectors, (0.0, 0.0, 0.0))


def von_mises(tensor: tuple[float, ...]) -> float:
    xx, yy, zz, xy, xz, yz = tensor
    return math.sqrt(0.5*((xx-yy)**2+(yy-zz)**2+(zz-xx)**2)+3.0*(xy*xy+xz*xz+yz*yz))


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered)-1, max(0, math.ceil(fraction*len(ordered))-1))]


def solve_level(config: dict[str, Any], case: dict[str, Any], mesh: MeshData, run_dir: Path, ccx: Path) -> dict[str, Any]:
    triangles, loaded_nodes, support_nodes, area = map_regions(case, mesh, config["tolerances"]["surface_m"])
    loads, center = consistent_load(case, mesh, triangles, loaded_nodes)
    (run_dir / "coupling.inp").write_text(build_deck(config, case, mesh, loads, loaded_nodes, support_nodes), encoding="ascii")
    code, stdout, stderr, started = run([str(ccx), "coupling"], run_dir)
    (run_dir / "solver_stdout.txt").write_text(stdout, encoding="utf-8"); (run_dir / "solver_stderr.txt").write_text(stderr, encoding="utf-8")
    if code != 0:
        raise RuntimeError(f"CalculiX failed: {stderr[-1000:]}")
    dat = run_dir / "coupling.dat"
    if not dat.is_file() or dat.stat().st_mtime_ns < started:
        raise RuntimeError("fresh CalculiX DAT evidence is missing")
    parsed = parse_loaded_interface_dat(dat, support_set_names=("SUPPORT_MOUNT",))
    reactions = parsed["reactions"]["ACTIVE_SUPPORT"]
    applied = tuple(math.fsum(value[i] for value in loads.values()) for i in range(3))
    reaction = tuple(math.fsum(value[i] for value in reactions.values()) for i in range(3))
    applied_moment = moment(mesh.nodes, loads); reaction_moment = moment(mesh.nodes, reactions)
    force_scale = max(norm(applied), norm(tuple(float(x) for x in case["torque_nm"])) / case["characteristic_length_m"], 1.0)
    moment_scale = max(norm(applied)*case["characteristic_length_m"], norm(tuple(float(x) for x in case["torque_nm"])), 1.0)
    force_residual = norm(tuple(applied[i]+reaction[i] for i in range(3))) / force_scale
    moment_residual = norm(tuple(applied_moment[i]+reaction_moment[i] for i in range(3))) / moment_scale
    work_twice = math.fsum(math.fsum(loads[node][i]*parsed["displacements"][node][i] for i in range(3)) for node in loads)
    external = 0.5*work_twice; internal = math.fsum(parsed["element_internal_energy_j"].values())
    energy_residual = abs(external-internal)/max(abs(external), abs(internal), 1e-18)
    stresses = [von_mises(row[2]) for row in parsed["stresses"]]
    return {"mesh_id": run_dir.name, "nodes": len(mesh.nodes), "elements": len(mesh.tetrahedra), "loaded_nodes": len(loaded_nodes), "support_nodes": len(support_nodes), "loaded_area_m2": area, "load_center_m": list(center), "maximum_displacement_m": max(norm(tuple(parsed["displacements"][node])) for node in loaded_nodes), "compliance_m_per_n": work_twice/(force_scale*force_scale), "p90_von_mises_stress_pa": percentile(stresses, 0.9), "force_residual_relative": force_residual, "moment_residual_relative": moment_residual, "energy_residual_relative": energy_residual, "solver_converged": True}


def verify_sources(config: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    source = config["source"]
    result = json.loads((ROOT/source["work084_result_path"]).read_text(encoding="utf-8"))
    manifest = json.loads((ROOT/source["geometry_manifest_path"]).read_text(encoding="utf-8"))
    report = json.loads((ROOT/source["freecad_report_path"]).read_text(encoding="utf-8"))
    if result.get("result_sha256") != source["work084_result_sha256"] or manifest.get("manifest_sha256") != source["geometry_manifest_sha256"] or report.get("report_sha256") != source["freecad_report_sha256"]:
        raise RuntimeError("Work 084 upstream identity mismatch")
    result_hashes = result.get("part_step_sha256", {})
    manifest_hashes = {item["part_id"]: item["step_sha256"] for item in manifest.get("parts", [])}
    report_hashes = {item["part_id"]: item["step_sha256"] for item in report.get("parts", [])}
    for case in config["cases"]:
        expected = case["step_sha256"]
        path = ROOT/source["step_root"]/case["step_file"]
        if result_hashes.get(case["part_id"]) != expected or manifest_hashes.get(case["part_id"]) != expected or report_hashes.get(case["part_id"]) != expected or sha(path) != expected:
            raise RuntimeError(f"exact STEP identity mismatch for {case['part_id']}")
    return result, manifest, report


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--config", type=Path, required=True); parser.add_argument("--output-root", type=Path, required=True); parser.add_argument("--gmsh", type=Path, required=True); parser.add_argument("--ccx", type=Path, required=True)
    args = parser.parse_args(); args.output_root = args.output_root.resolve(); args.gmsh=args.gmsh.resolve(); args.ccx=args.ccx.resolve()
    if args.output_root.exists() and any(args.output_root.iterdir()):
        raise SystemExit("output-root must be absent or empty")
    args.output_root.mkdir(parents=True, exist_ok=True)
    config = json.loads(args.config.read_text(encoding="utf-8")); validation = validate_config(config)
    material_bundle = json.loads((ROOT/"config/materials/engineering_material_manufacturing_v1.json").read_text(encoding="utf-8")); material_result=validate_material_record(material_bundle["material"])
    if material_result["record_sha256"] != config["material"]["material_record_sha256"] or material_result["design_use_allowed"]:
        raise RuntimeError("material evidence identity/status mismatch")
    verify_sources(config)
    case_results=[]; artifact_hashes={}
    for case in config["cases"]:
        step_path=ROOT/config["source"]["step_root"]/case["step_file"]; meshes=[]; case_hashes={}
        for index,size in enumerate(case["mesh_levels_m"],1):
            level=f"mesh_{index}_{size*1000:g}mm"; run_dir=args.output_root/case["case_id"]/level; run_dir.mkdir(parents=True)
            geo=run_dir/"part.geo"; msh=run_dir/"part.msh"; geo.write_text(gmsh_geo(step_path,size),encoding="ascii")
            code,stdout,stderr,_=run([str(args.gmsh),str(geo),"-3","-format","msh2","-o",str(msh)],run_dir); (run_dir/"gmsh_stdout.txt").write_text(stdout,encoding="utf-8"); (run_dir/"gmsh_stderr.txt").write_text(stderr,encoding="utf-8")
            if code != 0: raise RuntimeError(f"Gmsh failed: {stderr[-1000:]}")
            meshes.append(solve_level(config,case,scaled_mesh(msh),run_dir,args.ccx))
            case_hashes[level]={"part.msh":sha(msh),"coupling.inp":sha(run_dir/"coupling.inp"),"coupling.dat":sha(run_dir/"coupling.dat"),"coupling.frd_canonical":canonical_frd_sha(run_dir/"coupling.frd")}
        case_results.append({"case_id":case["case_id"],"mesh_results":meshes,"severed_support_control":{"connection_state":"severed","transmitted_force_n":[0.0,0.0,0.0],"transmitted_torque_nm":[0.0,0.0,0.0],"subsystem_state":"dnf"}}); artifact_hashes[case["case_id"]]=case_hashes
    evidence={"source_identities_verified":True,"hidden_geometry_repair":False,"case_results":case_results}
    (args.output_root/"solver_evidence.json").write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    decision=adjudicate(config,evidence)
    body={"status":"passed","verdict":decision["verdict"],"design_use_allowed":False,"config_sha256":validation["config_sha256"],"work084_result_sha256":config["source"]["work084_result_sha256"],"adjudication":decision,"artifact_sha256":artifact_hashes}
    result={**body,"result_sha256":canonical_sha256(body)}; (args.output_root/"result.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":"passed","verdict":result["verdict"],"result_sha256":result["result_sha256"],"cases":decision["cases"]},sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
