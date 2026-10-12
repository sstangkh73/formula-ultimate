#!/usr/bin/env python3
"""Generate a functional (goal v2) vehicle package for one seed.

Run under the pinned CadQuery runtime:

    python generate_functional_vehicle.py --seed S --out DIR

Writes ``DIR/manifest.json`` and one metre-scale binary STL per leaf under
``DIR/meshes/``. Leaf masses, centres of mass and the vehicle inertia tensor
are measured from the re-read exported meshes. The same seed and commit give a
byte-identical package. Representation only, not physical validation.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for entry in (str(ROOT / "src"), str(ROOT), str(Path(__file__).resolve().parent)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

from formula_ultimate.hierarchy.composition import (  # noqa: E402
    DEFAULT_COMPOSITION_CONFIG,
    DEFAULT_MATERIAL_CATALOGUE,
    build_manifest,
    composition_config_sha256,
    load_leaf_materials,
    manifest_bytes,
    mesh_path,
    plan_vehicle,
)
from formula_ultimate.hierarchy.decomposition import DEFAULT_CONFIG  # noqa: E402
from formula_ultimate.hierarchy.functional import (  # noqa: E402
    build_functional_manifest,
    config_sha256_v2,
    mesh_inertia,
)
from formula_ultimate.hierarchy.layout import DEFAULT_LAYOUT_CONFIG  # noqa: E402
from formula_ultimate.hierarchy.leaf_geometry import read_binary_stl  # noqa: E402
from leaf_realization import realize_leaf  # noqa: E402


def git_head() -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout.strip()


def generate(seed: int, out: Path) -> dict:
    catalogue = load_leaf_materials(ROOT / DEFAULT_MATERIAL_CATALOGUE)
    plan = plan_vehicle(seed, catalogue)
    for note in plan.rejected:
        print(f"rejected plan: {note}", file=sys.stderr)
    out.mkdir(parents=True, exist_ok=True)
    measurements = {}
    for leaf in plan.layout.leaves:
        measurements[leaf.id] = realize_leaf(leaf.program, out / mesh_path(leaf.id),
                                             plan.materials[leaf.id].density_kg_m3)
    v1_config = composition_config_sha256(DEFAULT_CONFIG, DEFAULT_LAYOUT_CONFIG,
                                          DEFAULT_COMPOSITION_CONFIG, catalogue)
    v1_manifest = build_manifest(plan, measurements, v1_config, git_head())
    _mass, _com, inertia = mesh_inertia(
        (read_binary_stl(out / mesh_path(leaf.id)), plan.materials[leaf.id].density_kg_m3)
        for leaf in plan.layout.leaves)
    # Skeleton (Work 155): no motion or capability evidence is claimed yet.
    manifest = build_functional_manifest(v1_manifest, motions=[], function_evidence={},
                                         inertia_kg_m2=inertia, config_sha256=config_sha256_v2(v1_config))
    (out / "manifest.json").write_bytes(manifest_bytes(manifest))
    return manifest


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest = generate(args.seed, args.out)
    leaves = sum(1 for n in manifest["nodes"] if n["kind"] == "part")
    print(f"seed {args.seed}: {leaves} leaves, {len(manifest['interfaces'])} interfaces, "
          f"{len(manifest['motions'])} motions -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
