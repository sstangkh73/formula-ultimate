# Loop Goal: Hierarchical Free-Form Composition v1

Thai companion: `GOAL.th.md`

Protected: the loop stops if this file changes. Set by Work 148.

## What the project owner wants

The system designs parts freely, with no prescribed shapes. It designs them
from the smallest parts upward and composes them, so small parts become
subassemblies, subassemblies become systems, and systems become the vehicle.
An engine-like converter, for example, would have chambers, moving members,
metering parts and fasteners. This must hold for **every** part of the
vehicle, not only the energy converter. The system is **not** required to
reproduce a conventional engine or any conventional part list. Whatever
decomposition it chooses must be its own, and it must be measurable.

## Done means

`pwsh -NoProfile -File auto-loop/verify.ps1` exits 0 on a clean, committed tree:

1. Gate 1: `scripts/validation/check_material_publication_boundary.py` passes.
2. Gate 2: the whole repository suite `python -m unittest discover -s tests` passes.
3. Gate 3: `python -m unittest discover -s auto-loop/acceptance` passes.

## The contract Gate 3 checks

Entry point, run under the pinned CadQuery runtime:

```text
.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_hierarchical_vehicle.py --seed S --out DIR
```

`DIR` may not exist yet. The generator creates it, exits 0 within 20 minutes,
and writes:

- `DIR/manifest.json`
- one STL mesh (binary or ASCII) per leaf part, in **metres**, placed in
  vehicle coordinates and referenced by a relative path inside `DIR`.

`manifest.json` has exactly these top-level fields:

| Field | Meaning |
|---|---|
| `design_language_version` | non-empty string |
| `seed` | the integer passed in |
| `config_sha256` | 64-hex hash of the configuration used |
| `git_commit` | `git rev-parse HEAD` at run time |
| `length_unit`, `mass_unit` | `"m"`, `"kg"` |
| `contact_tolerance_m` | `0 < tol <= 5e-4` |
| `root` | id of the vehicle assembly node |
| `nodes` | list of assembly and part nodes |
| `interfaces` | list of joints between leaf parts |

An assembly node has exactly `id, kind="assembly", children, functions, mass_kg,
center_of_mass_m`. A part node has exactly `id, kind="part", mesh,
material_id, density_kg_m3, mass_kg, center_of_mass_m, generator`, where
`generator = {grammar_version, program, program_sha256}` and `program_sha256`
is the SHA-256 of canonical JSON (`sort_keys`, separators `(",", ":")`,
`ensure_ascii`, no NaN) of `program`. An interface has `id, a, b, kind` and an
optional `interference_m`. `a` and `b` are leaf parts. `kind` is one of
`threaded, welded, bonded, interference, integral` (Work 140). `interference_m`
is allowed only for `interference`, with `0 < x <= 1e-4`.

Acceptance criteria, checked independently from the meshes:

1. **Replay.** The same seed gives a byte-identical file set. Metadata fields
   are valid, and `git_commit` equals HEAD.
2. **Hierarchy.** There is a single root, every node has one parent, there are
   no cycles, and every node is reachable. There are at least **4 levels** and
   at least **150 leaf parts**. The largest leaf's bounding-box diagonal is at
   least **100x** the smallest.
3. **Every function.** Each of the nine capabilities in
   `formula_ultimate.topology.functional_vehicle.REQUIRED_CAPABILITIES` is
   named in `functions` of an assembly whose subtree height is at least 2 and
   which has at least 5 leaves.
4. **Geometry and mass.** Every leaf mesh is closed and consistently oriented,
   with positive volume. Leaf `mass_kg` equals mesh volume times
   `density_kg_m3` within a relative 1e-5. Centre of mass is within 1e-5 m.
   Assembly mass and centre of mass roll up exactly from the children.
5. **Free form.** At most 25 % of leaves fill at least 99.9 % of their
   axis-aligned bounding box. Every leaf's program hash matches.
6. **Interfaces.** Inside every assembly, the children are connected through
   interfaces. Every interface shows measured surface contact within
   `contact_tolerance_m`. No sampled point of one leaf lies inside another
   deeper than the tolerance, or deeper than the declared `interference_m`.
7. **No fixed template.** Seeds 11, 23 and 37 give pairwise different tree
   topologies, and every capability has at least two distinct subtree
   topologies across them.

## Boundaries the loop must respect

- `AGENTS.md` applies in full: one numbered work item per iteration,
  bilingual plan/result records, explicit staging, a commit only after
  validation passes, SI units, tests with every new model.
- Materials come from the catalog only, with no new compositions. Real
  material values stay in gitignored `/private/`. Never commit them, and never
  print them into tracked files. Densities in generated artifacts are fine
  because `artifacts/` is gitignored. Synthetic placeholder materials must be
  labelled synthetic and `design_use_allowed=false`.
- Reuse the existing free-form grammar (`components/freeform_solid_grammar.py`,
  `scripts/cad/*`), the part-resolution and joint gates (`assembly/part_resolution.py`)
  and the functional vocabulary (`topology/functional_vehicle.py`). Do not
  replace them with something unrelated.
- No conventional part names may be hard-coded as required building blocks.
  The decomposition must come from a declared generative or search procedure
  driven by the seed and the declared constraints.

## What passing does NOT mean

Passing is a **geometry and assembly representation gate**. It is not
physical validation. It does not show that the parts work, carry load,
survive heat, or make the car faster, and it does not show that the
decompositions are useful. Coupling the hierarchy to Level-0 physics and the
race kernel is a later goal.

Known limitations of the checks:

- Interpenetration samples vertices and triangle centroids, so some crossing
  overlaps can escape detection.
- The box fraction is a proxy for free form.
- Topology diversity across three seeds rules out one fixed template. It does
  not measure usefulness.

## Suggested milestones (the loop may reorder them)

1. A recursive part-tree data model with validation and tests (pure Python,
   no CAD).
2. A seed-driven decomposition procedure over the nine capabilities that does
   not depend on a part catalogue.
3. A leaf-geometry realization through the existing free-form grammar and
   CadQuery, with STL export in metres and mass from the exported mesh.
4. Interface placement that produces measurable contact without
   interpenetration.
5. A generator CLI, a manifest, and replay determinism (CadQuery parallel
   booleans off).
6. Scale-up to at least 150 leaves and at least a 100x size span, and
   satisfying Gate 3 on all three seeds.
