# Work 148 Plan: Hierarchical Free-Form Composition Auto-Loop

Thai companion: `2026-10-11_148_hierarchical-composition-auto-loop-plan.th.md`

Date: 2026-10-11

Status: Completed

## Objective

Prepare the untracked `auto-loop/` Claude + Codex runner so it can work
unattended on the project owner's stated goal: the system designs free-form
parts at every scale and composes them bottom-up, so small parts become
subassemblies, subassemblies become systems, and systems become the whole
vehicle. This must hold for every function of the vehicle, not only the
energy converter. No conventional part list (piston, injector, bolt) may be
prescribed.

This work only prepares the loop. It writes the goal, the acceptance
specification, the verifier and the runner, and it does not implement the
generator. It does not run the loop.

## Scope

- Replace the template's BAHTTEXT demo goal, source and tests with a goal and a
  protected acceptance suite for hierarchical free-form composition.
- Adapt the runner to this repository and to `AGENTS.md`:
  - run from the repository root, never `git init` a nested repository;
  - refuse to run on `main`, and work on a dedicated `loop/...` branch;
  - never use blanket staging; the agent stages explicit files and commits
    only after its declared validation passes;
  - each iteration is one numbered work item with bilingual plan/result
    records;
  - stop when a protected file changes, including any test that existed at
    loop start.
- Define the verifier as three gates: the material publication-boundary check,
  the full repository unittest suite, and the acceptance suite.
- Write English and Thai documentation for the loop.

## Acceptance specification (what "done" means for the loop)

An entry point
`scripts/hierarchy/generate_hierarchical_vehicle.py --seed S --out DIR`, run
under the pinned CadQuery runtime `.tools/cadquery-mcp/Scripts/python.exe`,
must write `DIR/manifest.json` and one STL mesh per leaf part, in metres. The
acceptance tests run under the system Python and check the output
independently of the generator's own claims:

1. Replay: the same seed gives byte-identical manifest and meshes. The
   manifest carries the design-language version, seed, config hash and git
   commit.
2. Hierarchy: the part tree is acyclic and has a single root. It has at least
   4 levels and at least 150 leaf parts. The characteristic sizes of the leaf
   parts span at least a factor of 100.
3. Every function: each of the nine technology-neutral capabilities in
   `functional_vehicle.REQUIRED_CAPABILITIES` is realized by an assembly
   subtree that is at least 2 levels deep and has at least 5 leaf parts.
4. Geometry: every leaf mesh is closed, consistently oriented and of positive
   volume. Leaf mass equals mesh volume times declared density. Assembly mass
   equals the sum of its children. Vehicle mass and centre of mass agree with a
   recomputation from the meshes.
5. Free form: at most 25 % of the leaves fill their axis-aligned bounding box,
   meaning they are boxes. Each leaf records the program that generated it,
   with a hash that matches.
6. Interfaces: inside every assembly, the children are connected by declared
   interfaces whose kind is one of the technology-neutral joint kinds from Work
   140. Each interface is backed by measured mesh contact within the declared
   tolerance (at most 0.5 mm). Sampled points show no leaf penetrating another
   beyond tolerance or a declared interference.
7. No fixed template: three different seeds give pairwise distinct tree
   topologies, and each capability shows at least two distinct subtree
   topologies across those seeds.

## Planned files

- `auto-loop/README.md`, `auto-loop/README.th.md`
- `auto-loop/GOAL.md`, `auto-loop/GOAL.th.md`
- `auto-loop/PROMPT.md`, `auto-loop/PROMPT.th.md`
- `auto-loop/progress.md`, `auto-loop/progress.th.md`
- `auto-loop/run-loop.ps1`, `auto-loop/verify.ps1`, `auto-loop/tools/codex.sh`,
  `auto-loop/.gitignore`
- `auto-loop/acceptance/__init__.py`,
  `auto-loop/acceptance/test_hierarchical_composition.py`
- delete the demo `auto-loop/src/bahttext.py` and `auto-loop/tests/test_bahttext.py`
- this plan, its Thai companion, and the matching Work 148 result records

## Validation

1. Self-check the acceptance suite against fixtures in the scratchpad: a small
   synthetic valid package must pass every check, and deliberately broken
   packages (open mesh, wrong mass, missing capability, interpenetration,
   non-deterministic output, single template) must each fail the intended
   test. The fixture generator is injected through an environment variable
   that `verify.ps1` clears.
2. Run `pwsh -NoProfile -File auto-loop/verify.ps1` on the real repository.
   The expected result is that gates 1 and 2 pass and gate 3 fails because the
   generator does not exist yet. That is the loop's starting state.
3. Parse-check `run-loop.ps1` with the PowerShell parser, and dry-run its
   preflight logic (branch guard, protected-file hashing) without invoking
   `claude`.
4. Run the full unittest suite and the publication-boundary validator.
5. Stage only Work 148 files, run `git diff --cached --check`, commit once and
   report the hash.

## Success criteria

- The acceptance suite fails on the current repository for the stated reason,
  and passes or fails correctly on every self-check fixture.
- The runner cannot `git init`, cannot run on `main`, does not run blanket
  staging, and stops on protected-file changes.
- The goal states plainly that passing is a geometry and assembly
  representation gate, not physical validation.
- All existing tests still pass.

## Risks

- Mesh-based interference checks sample vertices and triangle centroids, so
  some crossing overlaps can be missed. This limitation is recorded in the
  goal.
- The box-fraction metric is a proxy for free form, not proof of novelty.
- Diversity across three seeds shows that the decomposition is not one fixed
  template. It does not show that the decompositions are useful.
- CadQuery generation of more than 150 parts per seed, run four times, may be
  slow. The acceptance suite allows 20 minutes per run.
- An unattended agent can still write weak code that passes. Protected
  acceptance tests and human review of every committed work item are the
  mitigations.

## Explicit non-goals

- Do not implement the generator or any physics model.
- Do not run the loop or spend Claude or Codex API budget on it.
- Do not couple the hierarchy to race simulation yet. That is a later goal.
- Do not touch `/private/` material data. The acceptance tests read densities
  only from generated, gitignored artifacts.
- Do not push, publish or rewrite history.
