"""Run Work 082 from exact Work 081 STEP evidence through Gmsh/CalculiX."""

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
from formula_ultimate.structural.geometry_coupling import (  # noqa: E402
    adjudicate_solver_evidence,
    canonical_sha256,
    propagate_connection_state,
    validate_coupling_config,
)
from formula_ultimate.structural.loaded_interface import (  # noqa: E402
    parse_loaded_interface_dat,
    triangle_area,
)


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
        {node: tuple(value * 1.0e-3 for value in xyz) for node, xyz in raw.nodes.items()},
        raw.tetrahedra,
        raw.triangles,
    )


def gmsh_geo(step_path: Path, size_m: float) -> str:
    step = step_path.as_posix().replace('"', '\\"')
    size_mm = size_m * 1000.0
    return "\n".join((
        'SetFactory("OpenCASCADE");',
        f'Merge "{step}";',
        'vols[] = Volume{:};',
        'If (#vols[] != 1)',
        '  Error("expected exactly one imported volume");',
        'EndIf',
        'Physical Volume(1) = {vols[0]};',
        f'Mesh.CharacteristicLengthMin = {size_mm:.17g};',
        f'Mesh.CharacteristicLengthMax = {size_mm:.17g};',
        'Mesh.Algorithm3D = 1;',
        'Mesh.ElementOrder = 1;',
        'Mesh.MshFileVersion = 2.2;',
        'Mesh.Binary = 0;',
        'Mesh.SaveAll = 1;',
        '',
    ))


def map_regions(config: dict[str, Any], mesh: MeshData) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    geometry = config["geometry"]
    radial_tol = config["tolerances"]["interface_radial_m"]
    plane_tol = config["tolerances"]["support_plane_m"]
    cx, cy, _ = geometry["hole_center_m"]
    radius = geometry["hole_radius_m"]
    support_x = geometry["support_plane_x_m"]
    load_triangles = []
    support_triangles = []
    load_nodes = set()
    support_nodes = set()
    for triangle_id, connectivity in mesh.triangles.items():
        points = [mesh.nodes[node] for node in connectivity]
        if all(abs(math.hypot(point[0] - cx, point[1] - cy) - radius) <= radial_tol for point in points):
            load_triangles.append(triangle_id); load_nodes.update(connectivity)
        if all(abs(point[0] - support_x) <= plane_tol for point in points):
            support_triangles.append(triangle_id); support_nodes.update(connectivity)
    if not load_triangles or not load_nodes:
        raise RuntimeError("missing loaded cylindrical surface in mesh")
    if not support_triangles or not support_nodes:
        raise RuntimeError("missing support plane in mesh")
    if load_nodes & support_nodes:
        raise RuntimeError("load and support regions overlap")
    return tuple(sorted(load_triangles)), tuple(sorted(load_nodes)), tuple(sorted(support_nodes))


def consistent_load(config: dict[str, Any], mesh: MeshData, triangles: tuple[int, ...], nodes: tuple[int, ...]) -> dict[int, tuple[float, float, float]]:
    areas = {item: triangle_area(*(mesh.nodes[node] for node in mesh.triangles[item])) for item in triangles}
    total_area = math.fsum(areas.values())
    if total_area <= 0.0:
        raise RuntimeError("loaded surface has zero area")
    raw = {node: [0.0, 0.0, 0.0] for node in nodes}
    target = config["load_case"]["force_n"]
    for triangle_id, area in areas.items():
        for node in mesh.triangles[triangle_id]:
            for axis in range(3):
                raw[node][axis] += target[axis] * area / (3.0 * total_area)
    result = {node: tuple(vector) for node, vector in raw.items()}
    totals = [math.fsum(vector[i] for vector in result.values()) for i in range(3)]
    if any(abs(totals[i] - target[i]) > 1e-10 * max(abs(target[i]), 1.0) for i in range(3)):
        raise RuntimeError("consistent load does not close")
    return result


def nset(name: str, nodes: tuple[int, ...]) -> list[str]:
    lines = [f"*NSET, NSET={name}"]
    for start in range(0, len(nodes), 16):
        lines.append(", ".join(str(node) for node in nodes[start : start + 16]))
    return lines


def build_deck(config: dict[str, Any], mesh: MeshData, loads: dict[int, tuple[float, float, float]], load_nodes: tuple[int, ...], support_nodes: tuple[int, ...]) -> str:
    material = config["material"]
    lines = ["*HEADING", config["experiment_id"], "*NODE, NSET=NALL"]
    lines.extend(f"{node}, {xyz[0]:.12g}, {xyz[1]:.12g}, {xyz[2]:.12g}" for node, xyz in sorted(mesh.nodes.items()))
    lines.append("*ELEMENT, TYPE=C3D4, ELSET=EALL")
    lines.extend(f"{element}, {', '.join(str(node) for node in connectivity)}" for element, connectivity in sorted(mesh.tetrahedra.items()))
    lines.extend(nset("LOADED_IFACE", load_nodes)); lines.extend(nset("ACTIVE_SUPPORT", support_nodes)); lines.extend(nset("SUPPORT_MOUNT", support_nodes))
    lines.extend((
        f"*MATERIAL, NAME={material['material_id']}", "*ELASTIC",
        f"{material['youngs_modulus_pa']:.17g}, {material['poisson_ratio']:.17g}",
        "*DENSITY", f"{material['density_kg_per_m3']:.17g}",
        f"*SOLID SECTION, ELSET=EALL, MATERIAL={material['material_id']}",
        "*BOUNDARY", "ACTIVE_SUPPORT, 1, 3, 0.0", "*STEP", "*STATIC", "*CLOAD",
    ))
    for node, vector in sorted(loads.items()):
        for dof, value in enumerate(vector, 1):
            if value:
                lines.append(f"{node}, {dof}, {value:.17g}")
    lines.extend((
        "*NODE PRINT, NSET=LOADED_IFACE", "U",
        "*NODE PRINT, NSET=ACTIVE_SUPPORT, TOTALS=YES", "RF",
        "*NODE PRINT, NSET=SUPPORT_MOUNT, TOTALS=YES", "RF",
        "*EL PRINT, ELSET=EALL", "S, E, ENER, ELSE",
        "*NODE FILE", "U, RF", "*EL FILE", "S, E", "*END STEP", "",
    ))
    return "\n".join(lines)


def norm(value: tuple[float, float, float]) -> float:
    return math.sqrt(math.fsum(item * item for item in value))


def moment(nodes: dict[int, tuple[float, float, float]], vectors: dict[int, tuple[float, float, float]]) -> tuple[float, float, float]:
    return (
        math.fsum(nodes[node][1] * f[2] - nodes[node][2] * f[1] for node, f in vectors.items()),
        math.fsum(nodes[node][2] * f[0] - nodes[node][0] * f[2] for node, f in vectors.items()),
        math.fsum(nodes[node][0] * f[1] - nodes[node][1] * f[0] for node, f in vectors.items()),
    )


def von_mises(tensor: tuple[float, ...]) -> float:
    xx, yy, zz, xy, xz, yz = tensor
    return math.sqrt(0.5 * ((xx - yy) ** 2 + (yy - zz) ** 2 + (zz - xx) ** 2) + 3.0 * (xy * xy + xz * xz + yz * yz))


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, max(0, math.ceil(fraction * len(ordered)) - 1))]


def solve_level(config: dict[str, Any], mesh: MeshData, run_dir: Path, ccx: Path) -> dict[str, Any]:
    triangles, loaded_nodes, support_nodes = map_regions(config, mesh)
    loads = consistent_load(config, mesh, triangles, loaded_nodes)
    deck = build_deck(config, mesh, loads, loaded_nodes, support_nodes)
    deck_path = run_dir / "coupling.inp"; deck_path.write_text(deck, encoding="ascii")
    code, stdout, stderr, started = run([str(ccx), "coupling"], run_dir)
    (run_dir / "solver_stdout.txt").write_text(stdout, encoding="utf-8")
    (run_dir / "solver_stderr.txt").write_text(stderr, encoding="utf-8")
    if code != 0:
        raise RuntimeError(f"CalculiX failed: {stderr[-1000:]}")
    dat_path = run_dir / "coupling.dat"
    if not dat_path.is_file() or dat_path.stat().st_mtime_ns < started:
        raise RuntimeError("fresh CalculiX DAT evidence is missing")
    parsed = parse_loaded_interface_dat(dat_path, support_set_names=("SUPPORT_MOUNT",))
    reactions = parsed["reactions"]["ACTIVE_SUPPORT"]
    applied = tuple(math.fsum(value[i] for value in loads.values()) for i in range(3))
    reaction = tuple(math.fsum(value[i] for value in reactions.values()) for i in range(3))
    force_residual = norm(tuple(applied[i] + reaction[i] for i in range(3))) / norm(applied)
    applied_moment = moment(mesh.nodes, loads); reaction_moment = moment(mesh.nodes, reactions)
    moment_residual = norm(tuple(applied_moment[i] + reaction_moment[i] for i in range(3))) / (norm(applied) * config["geometry"]["characteristic_length_m"])
    load_work_twice = math.fsum(math.fsum(loads[node][i] * parsed["displacements"][node][i] for i in range(3)) for node in loads)
    external_energy = 0.5 * load_work_twice
    internal_energy = math.fsum(parsed["element_internal_energy_j"].values())
    energy_residual = abs(external_energy - internal_energy) / max(abs(external_energy), abs(internal_energy), 1e-18)
    displacement = max(norm(tuple(parsed["displacements"][node])) for node in loaded_nodes)
    stresses = [von_mises(row[2]) for row in parsed["stresses"]]
    return {
        "mesh_id": run_dir.name,
        "nodes": len(mesh.nodes),
        "elements": len(mesh.tetrahedra),
        "maximum_displacement_m": displacement,
        "compliance_m_per_n": load_work_twice / (norm(applied) ** 2),
        "p90_von_mises_stress_pa": percentile(stresses, 0.90),
        "force_residual_relative": force_residual,
        "moment_residual_relative": moment_residual,
        "energy_residual_relative": energy_residual,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--geometry-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--gmsh", type=Path, required=True)
    parser.add_argument("--ccx", type=Path, required=True)
    args = parser.parse_args()
    args.config = args.config.resolve()
    args.geometry_root = args.geometry_root.resolve()
    args.output_root = args.output_root.resolve()
    args.gmsh = args.gmsh.resolve()
    args.ccx = args.ccx.resolve()
    if args.output_root.exists() and any(args.output_root.iterdir()):
        raise SystemExit("output-root must be absent or empty to prevent stale evidence")
    args.output_root.mkdir(parents=True, exist_ok=True)
    config = json.loads(args.config.read_text(encoding="utf-8")); validation = validate_coupling_config(config)
    material_bundle = json.loads((ROOT / "config/materials/engineering_material_manufacturing_v1.json").read_text(encoding="utf-8"))
    material_result = validate_material_record(material_bundle["material"])
    if material_result["record_sha256"] != config["material"]["material_record_sha256"] or material_result["design_use_allowed"]:
        raise RuntimeError("material identity/status differs from Work 079")
    source_manifest = json.loads((args.geometry_root / "source_manifest.json").read_text(encoding="utf-8"))
    report = json.loads((args.geometry_root / "run_a/freecad_report.json").read_text(encoding="utf-8"))
    geometry = config["geometry"]
    if report["report_sha256"] != geometry["freecad_report_sha256"]:
        raise RuntimeError("FreeCAD report identity mismatch")
    measured = next(item for item in report["parts"] if item["part_id"] == geometry["part_id"])
    surface = next((item for item in measured["cylindrical_surfaces"] if item["surface_signature_sha256"] == geometry["loaded_surface_signature_sha256"]), None)
    if surface is None or measured["step_sha256"] != geometry["step_sha256"]:
        raise RuntimeError("exact geometry/interface identity is missing")
    step_path = args.geometry_root / "source_step" / geometry["step_file"]
    if sha(step_path) != geometry["step_sha256"] or source_manifest["manifest_sha256"] != report["source_manifest_sha256"]:
        raise RuntimeError("source STEP/manifest identity mismatch")
    mesh_results = []
    artifact_hashes = {}
    for level in config["mesh_levels"]:
        run_dir = args.output_root / level["mesh_id"]; run_dir.mkdir()
        geo_path = run_dir / "part.geo"; mesh_path = run_dir / "part.msh"
        geo_path.write_text(gmsh_geo(step_path, level["characteristic_size_m"]), encoding="ascii")
        code, stdout, stderr, _ = run([str(args.gmsh), str(geo_path), "-3", "-format", "msh2", "-o", str(mesh_path)], run_dir)
        (run_dir / "gmsh_stdout.txt").write_text(stdout, encoding="utf-8"); (run_dir / "gmsh_stderr.txt").write_text(stderr, encoding="utf-8")
        if code != 0:
            raise RuntimeError(f"Gmsh failed: {stderr[-1000:]}")
        mesh = scaled_mesh(mesh_path)
        result = solve_level(config, mesh, run_dir, args.ccx)
        mesh_results.append(result)
        artifact_hashes[level["mesh_id"]] = {
            "part.msh": sha(run_dir / "part.msh"),
            "coupling.inp": sha(run_dir / "coupling.inp"),
            "coupling.dat": sha(run_dir / "coupling.dat"),
            "coupling.frd_canonical": canonical_frd_sha(run_dir / "coupling.frd"),
        }
    evidence = {
        "geometry_identities": {key: geometry[key] for key in ("step_sha256", "freecad_report_sha256", "loaded_surface_signature_sha256")},
        "mesh_results": mesh_results,
        "solver_converged": True,
        "hidden_geometry_repair": False,
    }
    adjudication = adjudicate_solver_evidence(config, evidence)
    reference_connection = propagate_connection_state(config, adjudication["structural_state"])
    failed_connection = propagate_connection_state(config, "severed_load_path")
    body = {"status": "passed", "config_sha256": validation["config_sha256"], "geometry_step_sha256": geometry["step_sha256"], "material_record_sha256": config["material"]["material_record_sha256"], "adjudication": adjudication, "reference_connection": reference_connection, "critical_failure_control": failed_connection, "artifact_sha256": artifact_hashes, "design_use_allowed": False}
    result = {**body, "result_sha256": canonical_sha256(body)}
    (args.output_root / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "result_sha256": result["result_sha256"], "structural_state": adjudication["structural_state"], "mesh_results": mesh_results, "critical_failure_state": failed_connection["subsystem_state"], "design_use_allowed": False}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
