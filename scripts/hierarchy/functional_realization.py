#!/usr/bin/env python3
"""Realize one v1, bored, socketed or mechanism (goal v2) leaf program as a metre-scale binary STL.

Run under the pinned CadQuery runtime:

    python functional_realization.py PROGRAM.json OUT.stl DENSITY_KG_M3

The program is checked by ``fasteners.validate_v2_program`` (or
``mechanisms.validate_mechanism_program`` for mechanism prisms), then
built with the unchanged Work 092 executor and tessellated like a v1 leaf.
Mass and centre of mass are measured from the re-read float32 STL.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
for entry in (str(ROOT / "src"), str(ROOT), str(Path(__file__).resolve().parent)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

from formula_ultimate.hierarchy.leaf_geometry import measure_mesh, read_binary_stl, stl_bytes  # noqa: E402
from formula_ultimate.hierarchy.fasteners import validate_v2_program  # noqa: E402
from formula_ultimate.hierarchy.mechanisms import (  # noqa: E402
    MECHANISM_GRAMMAR_VERSION,
    validate_mechanism_program,
)
from leaf_realization import execute_candidate, tessellate_m  # noqa: E402


def build_program_shape(program: Mapping[str, Any]):
    if program.get("leaf_grammar_version") == MECHANISM_GRAMMAR_VERSION:
        validate_mechanism_program(program)
    else:
        validate_v2_program(program)
    profiles = {program["profile"]["profile_id"]: program["profile"]}
    shape, _trace = execute_candidate(program["candidate"], profiles)
    return shape


def realize_program(program: Mapping[str, Any], stl_path: Path, density_kg_m3: float) -> dict[str, Any]:
    """Build, export and measure one leaf; raises on any invalid geometry."""

    triangles = tessellate_m(build_program_shape(program), program)
    stl_path = Path(stl_path)
    stl_path.parent.mkdir(parents=True, exist_ok=True)
    stl_path.write_bytes(stl_bytes(triangles))
    return measure_mesh(read_binary_stl(stl_path), density_kg_m3)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    program = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    print(json.dumps(realize_program(program, Path(argv[1]), float(argv[2])), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
