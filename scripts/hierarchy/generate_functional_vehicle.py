#!/usr/bin/env python3
"""Generate a functional (goal v2) vehicle package for one seed.

Run under the pinned CadQuery runtime:

    python generate_functional_vehicle.py --seed S --out DIR

Writes ``DIR/manifest.json`` and one metre-scale binary STL per leaf under
``DIR/meshes/``. The v1 cluster is realized first; the mechanism layer
(Work 160) is planned around the cluster box measured from its re-read meshes,
with wheel-and-brake ground-contact corners on the deck (Work 161).
Leaf masses, centres of mass and the vehicle inertia tensor are measured from
the re-read exported meshes. The same seed and commit give a
byte-identical package. Representation only, not physical validation.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import replace
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
from formula_ultimate.hierarchy.fasteners import (  # noqa: E402
    DEFAULT_FASTENER_CONFIG,
    add_fasteners,
    fastener_config_record,
    fastener_problems,
)
from formula_ultimate.hierarchy.functional import (  # noqa: E402
    V2_DECOMPOSITION_CONFIG,
    build_functional_manifest,
    config_sha256_v2,
    mesh_inertia,
    with_leaf_grammar_versions,
    with_threaded_axes,
)
from formula_ultimate.hierarchy.ground_contacts import (  # noqa: E402
    DEFAULT_GROUND_CONTACT_CONFIG,
    add_ground_contacts,
    ground_contact_config_record,
    ground_contact_problems,
)
from formula_ultimate.hierarchy.layout import DEFAULT_LAYOUT_CONFIG  # noqa: E402
from formula_ultimate.hierarchy.leaf_geometry import read_binary_stl  # noqa: E402
from formula_ultimate.hierarchy.mechanisms import (  # noqa: E402
    DEFAULT_MECHANISM_CONFIG,
    measure_cluster,
    mechanism_config_record,
    mechanism_problems,
    merge_mechanism_layer,
    plan_mechanisms,
)
from formula_ultimate.hierarchy.leaf_refinement import (  # noqa: E402
    DEFAULT_REFINEMENT_CONFIG,
    refine_layout,
    refinement_config_record,
    refinement_problems,
)
from functional_realization import realize_program  # noqa: E402


def git_head() -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout.strip()


def generate(seed: int, out: Path) -> dict:
    catalogue = load_leaf_materials(ROOT / DEFAULT_MATERIAL_CATALOGUE)
    plan = plan_vehicle(seed, catalogue, V2_DECOMPOSITION_CONFIG)
    for note in plan.rejected:
        print(f"rejected plan: {note}", file=sys.stderr)
    refined = refine_layout(plan.layout, DEFAULT_REFINEMENT_CONFIG)
    problems = refinement_problems(plan.layout, refined)
    if problems:
        raise RuntimeError(f"seed {seed}: leaf refinement re-check failed: {problems[:5]}")
    plan = replace(plan, layout=refined)
    fastened = add_fasteners(plan, catalogue, DEFAULT_FASTENER_CONFIG)
    problems = fastener_problems(plan, fastened, DEFAULT_FASTENER_CONFIG)
    if problems:
        raise RuntimeError(f"seed {seed}: fastener re-check failed: {problems[:5]}")
    plan = fastened.plan
    out.mkdir(parents=True, exist_ok=True)
    measurements, meshes, densities = {}, {}, {}
    for leaf in plan.layout.leaves:
        measurements[leaf.id] = realize_program(leaf.program, out / mesh_path(leaf.id),
                                                plan.materials[leaf.id].density_kg_m3)
        meshes[leaf.id] = read_binary_stl(out / mesh_path(leaf.id))
        densities[leaf.id] = plan.materials[leaf.id].density_kg_m3
    bounds = measure_cluster(meshes)
    layer = plan_mechanisms(seed, bounds, catalogue, DEFAULT_MECHANISM_CONFIG)
    layer = add_ground_contacts(layer, seed, catalogue, DEFAULT_GROUND_CONTACT_CONFIG)
    problems = mechanism_problems(layer, bounds, list(meshes)) + ground_contact_problems(
        layer, DEFAULT_GROUND_CONTACT_CONFIG)
    if problems:
        raise RuntimeError(f"seed {seed}: mechanism layer re-check failed: {problems[:5]}")
    for part in layer.parts:
        measurements[part.id] = realize_program(part.program, out / mesh_path(part.id),
                                                part.material.density_kg_m3)
        meshes[part.id] = read_binary_stl(out / mesh_path(part.id))
        densities[part.id] = part.material.density_kg_m3
    v1_config = composition_config_sha256(V2_DECOMPOSITION_CONFIG, DEFAULT_LAYOUT_CONFIG,
                                          DEFAULT_COMPOSITION_CONFIG, catalogue)
    v1_manifest = with_threaded_axes(
        with_leaf_grammar_versions(build_manifest(plan, measurements, v1_config, git_head())), fastened.axes)
    merged = merge_mechanism_layer(v1_manifest, layer, measurements, mesh_path)
    _mass, _com, inertia = mesh_inertia((meshes[i], densities[i]) for i in sorted(meshes))
    manifest = build_functional_manifest(merged, motions=list(layer.motions),
                                         function_evidence=layer.evidence,
                                         inertia_kg_m2=inertia,
                                         config_sha256=config_sha256_v2(
                                             v1_config, refinement_config_record(DEFAULT_REFINEMENT_CONFIG),
                                             fastener_config_record(DEFAULT_FASTENER_CONFIG),
                                             {**mechanism_config_record(DEFAULT_MECHANISM_CONFIG),
                                              "ground_contacts": ground_contact_config_record(
                                                  DEFAULT_GROUND_CONTACT_CONFIG)}))
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
