"""Run Work 045 through CAD, STEP, FreeCAD, Gmsh, and CalculiX."""

from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.structural import (  # noqa: E402
    CylindricalInterface,
    LoadedInterfacePlateSpec,
    MappedInterface,
    MeshData,
    StructuralEvidenceError,
    build_loaded_interface_deck,
    loaded_interface_spec_from_mapping,
    map_cylindrical_interfaces,
    parse_loaded_interface_dat,
    parse_msh2,
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_process(command: list[str], cwd: Path) -> dict[str, Any]:
    started = time.time_ns(); monotonic = time.perf_counter()
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    return {"command": command, "exit_code": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr, "started_time_ns": started, "wall_time_s": time.perf_counter() - monotonic}


def relative(actual: float, expected: float) -> float:
    return abs(actual - expected) / max(abs(expected), 1e-300)


def vector_norm(vector: tuple[float, float, float]) -> float:
    return math.sqrt(math.fsum(value * value for value in vector))


def add(left: tuple[float, float, float], right: tuple[float, float, float]) -> tuple[float, float, float]:
    return tuple(left[i] + right[i] for i in range(3))  # type: ignore[return-value]


def moment(nodes: dict[int, tuple[float, float, float]], vectors: dict[int, tuple[float, float, float]]) -> tuple[float, float, float]:
    return (
        math.fsum(nodes[node][1] * force[2] - nodes[node][2] * force[1] for node, force in vectors.items()),
        math.fsum(nodes[node][2] * force[0] - nodes[node][0] * force[2] for node, force in vectors.items()),
        math.fsum(nodes[node][0] * force[1] - nodes[node][1] * force[0] for node, force in vectors.items()),
    )


def von_mises(tensor: tuple[float, ...]) -> float:
    sxx, syy, szz, sxy, sxz, syz = tensor
    return math.sqrt(0.5 * ((sxx - syy) ** 2 + (syy - szz) ** 2 + (szz - sxx) ** 2) + 3.0 * (sxy * sxy + sxz * sxz + syz * syz))


def rejected(control_id: str, action: Callable[[], object], expected: str) -> dict[str, str]:
    try:
        action()
    except StructuralEvidenceError as exc:
        if expected not in str(exc):
            raise StructuralEvidenceError(f"{control_id} rejected for wrong reason: {exc}") from exc
        return {"control_id": control_id, "status": "rejected_as_expected", "reason": str(exc)}
    raise StructuralEvidenceError(f"negative control {control_id} was admitted")


def scaled_mesh(path: Path) -> MeshData:
    raw = parse_msh2(path)
    return MeshData({node: tuple(value * 1e-3 for value in xyz) for node, xyz in raw.nodes.items()}, raw.tetrahedra, raw.triangles)


def geo(step_path: Path, mesh_size_m: float) -> str:
    step = step_path.as_posix().replace('"', '\\"')
    size_mm = mesh_size_m * 1000.0
    return "\n".join(("SetFactory(\"OpenCASCADE\");", f"Merge \"{step}\";", "vols[] = Volume{:};", "Physical Volume(1) = {vols[]};", f"Mesh.CharacteristicLengthMin = {size_mm:.17g};", f"Mesh.CharacteristicLengthMax = {size_mm:.17g};", "Mesh.Algorithm3D = 1;", "Mesh.ElementOrder = 1;", "Mesh.MshFileVersion = 2.2;", "Mesh.Binary = 0;", "Mesh.SaveAll = 1;", ""))


def solve_case(spec: LoadedInterfacePlateSpec, mesh: MeshData, mapped: dict[str, MappedInterface], *, support_ids: tuple[str, ...], run_dir: Path, ccx: Path, tolerances: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    run_dir.mkdir(parents=True, exist_ok=True)
    deck, loads, support_nodes = build_loaded_interface_deck(spec, mesh, mapped, support_interface_ids=support_ids)
    deck_path = run_dir / "interface.inp"; deck_path.write_text(deck, encoding="ascii")
    process = run_process([str(ccx), "interface"], run_dir)
    (run_dir / "solver_stdout.txt").write_text(process["stdout"], encoding="utf-8")
    (run_dir / "solver_stderr.txt").write_text(process["stderr"], encoding="utf-8")
    if process["exit_code"] != 0:
        raise StructuralEvidenceError(f"CalculiX failed in {run_dir.name}: {process['stderr'][-2000:]}")
    dat_path, frd_path = run_dir / "interface.dat", run_dir / "interface.frd"
    for evidence in (dat_path, frd_path):
        if not evidence.is_file() or evidence.stat().st_mtime_ns < process["started_time_ns"]:
            raise StructuralEvidenceError(f"missing fresh {evidence.name} in {run_dir.name}")
    support_names = tuple(item.interface_id.upper() for item in spec.support_interfaces)
    parsed = parse_loaded_interface_dat(dat_path, support_set_names=support_names)
    missing_loaded = set(loads) - set(parsed["displacements"])
    if missing_loaded:
        raise StructuralEvidenceError(f"loaded displacement evidence omitted nodes: {sorted(missing_loaded)}")
    active_reactions = parsed["reactions"]["ACTIVE_SUPPORT"]
    missing_support = set(support_nodes) - set(active_reactions)
    if missing_support:
        raise StructuralEvidenceError(f"active reaction evidence omitted nodes: {sorted(missing_support)}")
    applied_force = tuple(math.fsum(force[axis] for force in loads.values()) for axis in range(3))
    reaction_force = tuple(math.fsum(force[axis] for force in active_reactions.values()) for axis in range(3))
    force_residual = add(applied_force, reaction_force)
    applied_moment = moment(mesh.nodes, loads); reaction_moment = moment(mesh.nodes, active_reactions)
    moment_residual = add(applied_moment, reaction_moment)
    load_magnitude = vector_norm(applied_force)
    force_residual_relative = vector_norm(force_residual) / load_magnitude
    moment_residual_relative = vector_norm(moment_residual) / (load_magnitude * spec.length_m)
    load_work_twice = math.fsum(math.fsum(loads[node][axis] * parsed["displacements"][node][axis] for axis in range(3)) for node in loads)
    external_work = 0.5 * load_work_twice
    internal_energy = math.fsum(parsed["element_internal_energy_j"].values())
    energy_residual_relative = abs(external_work - internal_energy) / max(abs(external_work), abs(internal_energy), 1e-12)
    for name, value, limit in (("force", force_residual_relative, tolerances["force_residual_relative"]), ("moment", moment_residual_relative, tolerances["moment_residual_relative"]), ("energy", energy_residual_relative, tolerances["energy_residual_relative"])):
        if value > float(limit):
            raise StructuralEvidenceError(f"{run_dir.name} {name} residual gate failed: {value}")
    if {row[0] for row in parsed["stresses"]} != set(mesh.tetrahedra):
        raise StructuralEvidenceError("stress field does not cover every tetrahedron")
    force_squared = math.fsum(value * value for value in applied_force)
    compliance = load_work_twice / force_squared
    shares = {}
    for interface in spec.support_interfaces:
        rows = parsed["reactions"][interface.interface_id.upper()]
        interface_force = tuple(math.fsum(force[axis] for force in rows.values()) for axis in range(3))
        shares[interface.interface_id] = {"reaction_force_n": interface_force, "axial_load_share": -interface_force[0] / spec.load_force_n[0]}
    loaded_interface = spec.loaded_interface
    metrics = {
        "support_interface_ids": support_ids, "applied_force_n": applied_force, "reaction_force_n": reaction_force,
        "force_residual_n": force_residual, "force_residual_relative": force_residual_relative,
        "applied_moment_nm": applied_moment, "reaction_moment_nm": reaction_moment,
        "moment_residual_nm": moment_residual, "moment_residual_relative": moment_residual_relative,
        "compliance_m_per_n": compliance, "conjugate_displacement_m": load_work_twice / load_magnitude,
        "external_work_j": external_work, "solver_internal_energy_j": internal_energy, "energy_residual_relative": energy_residual_relative,
        "maximum_von_mises_stress_pa": max(von_mises(row[2]) for row in parsed["stresses"]),
        "nominal_bearing_stress_pa": load_magnitude / (2 * loaded_interface.radius_m * spec.thickness_m),
        "nominal_net_section_stress_pa": load_magnitude / ((spec.width_m - 2 * loaded_interface.radius_m) * spec.thickness_m),
        "support_load_share": shares,
    }
    evidence = {path.name: sha(path) for path in (deck_path, dat_path, frd_path)}
    return {"metrics": metrics, "evidence_sha256": evidence, "solver_wall_time_s": process["wall_time_s"]}, process


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True); parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--cadquery-python", type=Path, required=True); parser.add_argument("--freecad-python", type=Path, required=True)
    parser.add_argument("--gmsh", type=Path, required=True); parser.add_argument("--ccx", type=Path, required=True)
    args = parser.parse_args(); stage = "configuration"; processes: list[dict[str, Any]] = []
    try:
        payload = json.loads(args.config.read_text(encoding="utf-8")); spec = loaded_interface_spec_from_mapping(payload)
        mesh_levels = payload["mesh_levels"]; tolerances = payload["tolerances"]
        sizes = tuple(float(item["characteristic_size_m"]) for item in mesh_levels)
        if sizes != (0.006, 0.004, 0.003):
            raise StructuralEvidenceError("Work 045 frozen mesh levels changed")
        for executable in (args.cadquery_python, args.freecad_python, args.gmsh, args.ccx):
            if not executable.is_file(): raise StructuralEvidenceError(f"required executable is missing: {executable}")
        if args.artifact_root.exists(): shutil.rmtree(args.artifact_root)
        args.artifact_root.mkdir(parents=True)
        step_path = args.artifact_root / "loaded_interface_plate.step"; manifest_path = args.artifact_root / "cadquery_manifest.json"; freecad_path = args.artifact_root / "freecad_interfaces.json"
        stage = "cadquery"
        process = run_process([str(args.cadquery_python), str(ROOT / "scripts/cad/generate_loaded_interface_plate.py"), "--config", str(args.config), "--output-step", str(step_path), "--manifest", str(manifest_path)], ROOT); process["stage"] = stage; processes.append(process)
        if process["exit_code"] != 0: raise StructuralEvidenceError(f"CadQuery failed: {process['stderr']}")
        stage = "freecad"
        process = run_process([str(args.freecad_python), str(ROOT / "scripts/cad/inspect_loaded_interface_freecad.py"), str(step_path), str(args.config), str(freecad_path)], ROOT); process["stage"] = stage; processes.append(process)
        if process["exit_code"] != 0: raise StructuralEvidenceError(f"FreeCAD inspection failed: {process['stderr']} {process['stdout']}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8")); freecad = json.loads(freecad_path.read_text(encoding="utf-8"))
        step_hash = sha(step_path)
        if manifest["step"]["sha256"] != step_hash or freecad["step_sha256"] != step_hash:
            raise StructuralEvidenceError("STEP identity differs across CAD and FreeCAD")
        expected_ids = {item.interface_id for item in spec.interfaces}
        if {item["interface_id"] for item in manifest["interfaces"]} != expected_ids or {item["interface_id"] for item in freecad["interfaces"]} != expected_ids:
            raise StructuralEvidenceError("interface identity differs across CAD and FreeCAD")
        for item in freecad["interfaces"]:
            declared = next(value for value in spec.interfaces if value.interface_id == item["interface_id"])
            expected_area = 2 * math.pi * declared.radius_m * spec.thickness_m
            if relative(float(item["area_m2"]), expected_area) > float(tolerances["freecad_area_relative"]):
                raise StructuralEvidenceError(f"FreeCAD interface area differs for {declared.interface_id}")
        analytical_volume = spec.length_m * spec.width_m * spec.thickness_m - math.fsum(math.pi * item.radius_m**2 * spec.thickness_m for item in spec.interfaces)
        if relative(float(manifest["volume_m3"]), analytical_volume) > 1e-8 or relative(float(freecad["volume_m3"]), analytical_volume) > 1e-8:
            raise StructuralEvidenceError("CAD/FreeCAD volume differs from declared geometry")
        mesh_results = []
        baseline_supports = tuple(payload["support_policies"]["baseline"]); sensitivity_supports = tuple(payload["support_policies"]["sensitivity"])
        for level in mesh_levels:
            mesh_id = str(level["mesh_id"]); run_dir = args.artifact_root / mesh_id; run_dir.mkdir()
            geo_path = run_dir / "plate.geo"; msh_path = run_dir / "plate.msh"; geo_path.write_text(geo(step_path, float(level["characteristic_size_m"])), encoding="ascii")
            stage = f"gmsh:{mesh_id}"; process = run_process([str(args.gmsh), str(geo_path), "-3", "-format", "msh2", "-o", str(msh_path)], run_dir); process["stage"] = stage; processes.append(process)
            if process["exit_code"] != 0: raise StructuralEvidenceError(f"Gmsh failed for {mesh_id}: {process['stderr']}")
            mesh = scaled_mesh(msh_path); mapped = map_cylindrical_interfaces(spec, mesh, radial_tolerance_m=float(tolerances["interface_radial_m"]))
            if set(mapped) != expected_ids: raise StructuralEvidenceError("mesh interface identities are incomplete")
            stage = f"calculix:{mesh_id}:baseline"
            solve, process = solve_case(spec, mesh, mapped, support_ids=baseline_supports, run_dir=run_dir / "baseline", ccx=args.ccx, tolerances=tolerances); process["stage"] = stage; processes.append(process)
            mesh_results.append({"mesh_id": mesh_id, "characteristic_size_m": float(level["characteristic_size_m"]), "nodes": len(mesh.nodes), "tetrahedra": len(mesh.tetrahedra), "boundary_triangles": len(mesh.triangles), "mesh_sha256": sha(msh_path), "mapped_interfaces": {name: {"triangle_count": len(item.triangle_ids), "node_count": len(item.node_ids), "faceted_area_m2": item.faceted_area_m2} for name, item in mapped.items()}, **solve})
            if mesh_id == mesh_levels[-1]["mesh_id"]:
                stage = "calculix:fine:sensitivity"
                sensitivity, process = solve_case(spec, mesh, mapped, support_ids=sensitivity_supports, run_dir=run_dir / "sensitivity", ccx=args.ccx, tolerances=tolerances); process["stage"] = stage; processes.append(process)
        medium, fine = mesh_results[-2:]
        compliance_change = relative(fine["metrics"]["compliance_m_per_n"], medium["metrics"]["compliance_m_per_n"])
        resultant_change = relative(vector_norm(tuple(fine["metrics"]["reaction_force_n"])), vector_norm(tuple(medium["metrics"]["reaction_force_n"])))
        convergence_status = "supported" if compliance_change <= float(tolerances["last_two_compliance_relative"]) and resultant_change <= float(tolerances["last_two_resultant_relative"]) else "rejected"
        sensitivity_change = relative(sensitivity["metrics"]["compliance_m_per_n"], fine["metrics"]["compliance_m_per_n"])
        transferability_status = "supported" if sensitivity_change <= float(tolerances["maximum_transferability_change_relative"]) else "rejected"
        stage = "negative_controls"
        base_load = spec.loaded_interface; base_support = spec.support_interfaces[0]
        controls = [
            rejected("missing_support", lambda: build_loaded_interface_deck(spec, scaled_mesh(args.artifact_root / mesh_levels[0]["mesh_id"] / "plate.msh"), {item.interface_id: MappedInterface(item.interface_id, (1,), (1,), 1.0) for item in spec.interfaces}, support_interface_ids=()), "missing"),
            rejected("duplicated_support_selection", lambda: build_loaded_interface_deck(spec, scaled_mesh(args.artifact_root / mesh_levels[0]["mesh_id"] / "plate.msh"), {item.interface_id: MappedInterface(item.interface_id, (1,), (1,), 1.0) for item in spec.interfaces}, support_interface_ids=(base_support.interface_id, base_support.interface_id)), "duplicated"),
            rejected("zero_area_interface", lambda: MappedInterface("bad", (1,), (1,), 0.0), "zero"),
            rejected("duplicated_load_tag", lambda: replace(spec, interfaces=(base_load, replace(base_support, interface_id=base_load.interface_id))), "duplicated"),
            rejected("broken_ligament", lambda: replace(spec, interfaces=(replace(base_load, center_x_m=spec.length_m - base_load.radius_m), *spec.support_interfaces)), "ligament"),
            rejected("disconnected_solid", lambda: MeshData({1:(0,0,0),2:(1,0,0),3:(0,1,0),4:(0,0,1),5:(3,0,0),6:(4,0,0),7:(3,1,0),8:(3,0,1)}, {1:(1,2,3,4),2:(5,6,7,8)}, {1:(1,2,3)}), "disconnected"),
        ]
        preferred = "supported" if convergence_status == transferability_status == "supported" else "rejected"
        summary = {
            "status": "passed", "claim_level": payload["claim_level"], "preferred_hypothesis": preferred,
            "interface_identity": {"status": "passed", "ids": sorted(expected_ids), "step_sha256": step_hash, "cadquery_manifest_sha256": sha(manifest_path), "freecad_report_sha256": sha(freecad_path)},
            "mesh_results": mesh_results,
            "mesh_convergence": {"status": convergence_status, "last_two_compliance_relative": compliance_change, "last_two_integrated_reaction_resultant_relative": resultant_change},
            "boundary_sensitivity": {"status": transferability_status, "baseline_supports": baseline_supports, "sensitivity_supports": sensitivity_supports, "compliance_change_relative": sensitivity_change, "fine_sensitivity_result": sensitivity},
            "negative_controls": controls, "process_evidence": processes, "config_sha256": sha(args.config),
            "tool_sha256": {"cadquery_python": sha(args.cadquery_python), "freecad_python": sha(args.freecad_python), "gmsh": sha(args.gmsh), "ccx": sha(args.ccx)},
            "repository_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip(),
            "worktree_dirty_during_run": bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout),
            "review": {"supporting_evidence": ["one exact STEP and three interface signatures survived CAD, FreeCAD, mesh, deck, and results", "every solve closed force, moment, and internal/external energy", "all malformed controls failed closed"], "contradicting_evidence": [item for item, status in (("mesh convergence exceeded its gate", convergence_status), ("support-boundary sensitivity exceeded transferability gate", transferability_status)) if status == "rejected"], "alternative_explanations": ["rigid bonded hole constraints idealize contact and can dominate compliance"], "missing_evidence": ["pin/contact/preload/friction and nonlinear bearing", "plasticity/fracture/fatigue coupling", "arbitrary joint topology"], "confidence": "high for this declared solver load path; low for transfer to other joints"},
        }
        write_json(args.artifact_root / "experiment_summary.json", summary)
        print(json.dumps({"status": "passed", "preferred_hypothesis": preferred, "mesh_convergence": summary["mesh_convergence"], "boundary_sensitivity": summary["boundary_sensitivity"]["status"], "sensitivity_change_relative": sensitivity_change, "negative_controls": len(controls), "summary": str(args.artifact_root / "experiment_summary.json")}, sort_keys=True))
        return 0
    except Exception as exc:
        failure = {"status": "failed", "failed_stage": stage, "error_type": type(exc).__name__, "message": str(exc), "process_evidence": processes, "traceback": traceback.format_exc()}
        write_json(args.artifact_root / "experiment_failure.json", failure)
        print(json.dumps(failure, sort_keys=True), file=sys.stderr); return 1


if __name__ == "__main__": raise SystemExit(main())
