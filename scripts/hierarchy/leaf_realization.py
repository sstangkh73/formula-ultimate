#!/usr/bin/env python3
"""Execute hierarchy leaf programs in CadQuery and export metre-scale STL.

Run under the pinned CadQuery runtime. The program is executed with the
existing Work 091 loop executor and Work 092 candidate executor (which work in
millimetres internally); the tessellation is divided by 1000 and written as a
deterministic binary STL. The exported mesh is re-read and must be closed and
consistently oriented; nothing is repaired.

Command line (for tests and inspection):
    python leaf_realization.py PROGRAM_JSON STL_PATH DENSITY_KG_M3
prints the measured mass properties as JSON.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
for entry in (str(ROOT / "src"), str(ROOT)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import numpy as np  # noqa: E402

from formula_ultimate.hierarchy.leaf_geometry import (  # noqa: E402
    MeshError,
    measure_mesh,
    read_binary_stl,
    stl_bytes,
    validate_leaf_program,
)
from scripts.cad.generate_freeform_solid_corpus import MM, execute_candidate  # noqa: E402

try:  # OCP global switch; keep boolean and meshing kernels single-threaded.
    from OCP.BOPAlgo import BOPAlgo_Options  # noqa: E402

    BOPAlgo_Options.SetParallelMode_s(False)
except Exception:  # pragma: no cover - older OCP builds
    pass


def build_shape(program: Mapping[str, Any]):
    validate_leaf_program(program)
    profiles = {program["profile"]["profile_id"]: program["profile"]}
    shape, _trace = execute_candidate(program["candidate"], profiles)
    return shape


def tessellate_m(shape, program: Mapping[str, Any]) -> np.ndarray:
    tess = program["tessellation"]
    vertices, triangles = shape.tessellate(tess["linear_tolerance_m"] * MM, tess["angular_tolerance_rad"])
    if not triangles:
        raise MeshError("tessellation produced no triangles")
    points = np.array([[v.x, v.y, v.z] for v in vertices], dtype=np.float64) / MM
    return points[np.asarray(triangles, dtype=np.int64)]


def realize_leaf(program: Mapping[str, Any], stl_path: Path, density_kg_m3: float) -> dict[str, Any]:
    """Build, export and measure one leaf; raises on any invalid geometry."""

    shape = build_shape(program)
    triangles = tessellate_m(shape, program)
    stl_path = Path(stl_path)
    stl_path.parent.mkdir(parents=True, exist_ok=True)
    stl_path.write_bytes(stl_bytes(triangles))
    return measure_mesh(read_binary_stl(stl_path), density_kg_m3)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    program = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    result = realize_leaf(program, Path(argv[1]), float(argv[2]))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
