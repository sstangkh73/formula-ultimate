"""Mesh a STEP solid, or the Work 138 benchmark box, into MSH 2.2 tetrahedra."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.structural.element_verification import parse_element_msh2  # noqa: E402
from formula_ultimate.structural.geometry_general_evaluator import (  # noqa: E402
    GeometryEvaluationError,
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def step_geo(step_path: Path, size_factor: float) -> str:
    # Gmsh derives its own sizes from the imported solid, so the registered
    # ladder scales them and refines every candidate the same way.
    return "\n".join((
        'SetFactory("OpenCASCADE");',
        f'Merge "{step_path.as_posix()}";',
        f"Mesh.MeshSizeFactor = {size_factor:.12g};",
        "Mesh.ElementOrder = 2;",
        "Mesh.SecondOrderIncomplete = 0;",
        # Straight-sided quadratic tetrahedra. Curving midside nodes onto a
        # curved boundary produced inverted elements that CalculiX rejects as
        # a nonpositive jacobian; the cost is a faceted curved surface.
        "Mesh.SecondOrderLinear = 1;",
        "Mesh.Algorithm3D = 1;",
        "Mesh.Optimize = 1;",
        "",
    ))


def box_geo(length: float, width: float, height: float, size_factor: float) -> str:
    coarsest = min(width, height) / 2.0
    return "\n".join((
        'SetFactory("OpenCASCADE");',
        f"Box(1) = {{0, 0, 0, {length:.12g}, {width:.12g}, {height:.12g}}};",
        f"Mesh.CharacteristicLengthMax = {coarsest:.12g};",
        f"Mesh.MeshSizeFactor = {size_factor:.12g};",
        "Mesh.ElementOrder = 2;",
        "Mesh.SecondOrderIncomplete = 0;",
        # Straight-sided quadratic tetrahedra. Curving midside nodes onto a
        # curved boundary produced inverted elements that CalculiX rejects as
        # a nonpositive jacobian; the cost is a faceted curved surface.
        "Mesh.SecondOrderLinear = 1;",
        "Mesh.Algorithm3D = 1;",
        "Mesh.Optimize = 1;",
        "",
    ))


def run_gmsh(gmsh: Path, geo_path: Path, mesh_path: Path, *, timeout_s: float) -> dict[str, Any]:
    """Run Gmsh once and return its process evidence; never raise on solver refusal."""

    started = time.perf_counter()
    try:
        completed = subprocess.run(
            [str(gmsh), str(geo_path.resolve()), "-3", "-format", "msh2", "-o", str(mesh_path.resolve()), "-v", "2"],
            cwd=geo_path.parent, capture_output=True, text=True, timeout=timeout_s, check=False,
        )
        exit_code, stdout, stderr = completed.returncode, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired:
        exit_code, stdout, stderr = None, "", f"gmsh exceeded {timeout_s} s"
    return {
        "tool": "gmsh",
        "exit_code": exit_code,
        "wall_time_s": time.perf_counter() - started,
        "stdout_tail": stdout.strip()[-800:],
        "stderr_tail": stderr.strip()[-800:],
        "mesh_exists": mesh_path.is_file(),
        "mesh_sha256": file_sha256(mesh_path) if mesh_path.is_file() else None,
    }


def mesh_solid(
    *,
    gmsh: Path,
    geometry: dict[str, Any],
    size_factor: float,
    work_dir: Path,
    timeout_s: float,
) -> tuple[dict[str, Any], Path]:
    work_dir.mkdir(parents=True, exist_ok=True)
    geo_path = work_dir / "part.geo"
    mesh_path = work_dir / "part.msh"
    if mesh_path.exists():
        mesh_path.unlink()
    if geometry["kind"] == "step_file":
        step_path = Path(geometry["path"])
        if not step_path.is_absolute():
            step_path = ROOT / step_path
        if not step_path.is_file():
            raise GeometryEvaluationError(f"declared STEP file is missing: {step_path}")
        geo_path.write_text(step_geo(step_path, size_factor), encoding="ascii")
    else:
        geo_path.write_text(
            box_geo(geometry["length_m"], geometry["width_m"], geometry["height_m"], size_factor),
            encoding="ascii",
        )
    evidence = run_gmsh(gmsh, geo_path, mesh_path, timeout_s=timeout_s)
    evidence["geo_sha256"] = file_sha256(geo_path)
    evidence["size_factor"] = size_factor
    return evidence, mesh_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gmsh", type=Path, required=True)
    parser.add_argument("--step", type=Path, required=True)
    parser.add_argument("--size-factor", type=float, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--timeout-s", type=float, default=600.0)
    args = parser.parse_args()

    evidence, mesh_path = mesh_solid(
        gmsh=args.gmsh,
        geometry={"kind": "step_file", "path": str(args.step)},
        size_factor=args.size_factor,
        work_dir=args.work_dir,
        timeout_s=args.timeout_s,
    )
    if evidence["exit_code"] != 0 or not evidence["mesh_exists"]:
        print(json.dumps({"status": "unresolved_mesh", "evidence": evidence}, sort_keys=True))
        return 1
    mesh = parse_element_msh2(mesh_path, expected_order=2)
    print(json.dumps({
        "status": "meshed",
        "node_count": len(mesh.nodes),
        "tetrahedron_count": len(mesh.tetrahedra),
        "triangle_count": len(mesh.triangles),
        "mesh_sha256": evidence["mesh_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
