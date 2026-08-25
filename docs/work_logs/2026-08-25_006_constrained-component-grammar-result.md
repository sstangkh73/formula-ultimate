# Work 006 Result: Constrained 3D Component Grammar and Evidence Loop

Status: Completed

Thai companion: `2026-08-25_006_constrained-component-grammar-result.th.md`

## Outcome

Work 006 implemented `mounting_plate_v1` and completed the controlled local
loop:

```text
constrained SI-unit JSON
  -> pre-CAD grammar gate
  -> CadQuery 2.8.0 B-rep
  -> hashed STEP
  -> FreeCAD 1.1.3 independent import and measurement
  -> analytical/CadQuery/FreeCAD evidence gates
  -> FreeCAD-derived constant-density mass
  -> existing Level 0 longitudinal point-mass kernel
```

All three predeclared valid candidates passed. The deliberately invalid fourth
candidate was rejected before CadQuery execution. The four predeclared
monotonic checks passed. This supports local pipeline coherence only; it is not
physical validation of a component.

## Files Changed

### Grammar and Level 0 contract

- `src/formula_ultimate/components/grammar.py`
  - defines `mounting_plate_v1`, `Material`, `MountingPlateSpec`, analytical
    volume, symmetric mounting ports, and observable `GrammarViolation` errors;
  - enforces dimensional bounds, finite values, schema/version identity,
    minimum edge ligaments, minimum hole-to-hole web, and minimum central-cut
    web before any CAD call.
- `src/formula_ultimate/components/__init__.py`
  - exports the public grammar types.
- `src/formula_ultimate/experiments/cad_level0.py`
  - defines strict independent-CAD measurement and Level 0 control contracts;
  - rejects invalid topology, non-finite values, malformed types/vectors,
    bounding-box disagreement, and excessive volume residuals;
  - derives component mass only from the admitted measurement volume.
- `src/formula_ultimate/experiments/__init__.py`
  - exports the CAD-to-Level-0 evidence API.

### Configuration and executable loop

- `config/work006_mounting_plate.json`
  - records experiment ID, grammar version, seed `6001`, constant-density
    aluminium assumption `2700 kg/m^3`, common geometry, candidates, Level 0
    controls, and tolerances.
- `scripts/cad/generate_mounting_plate.py`
  - validates one declared candidate, generates one CadQuery solid, exports
    STEP, and records CadQuery measurement, tool version, size, header, and
    SHA-256;
  - writes explicit pre-CAD failure evidence and returns exit code `2` for a
    grammar rejection.
- `scripts/cad/inspect_step_freecad.py`
  - runs with FreeCAD's bundled Python, imports the exact STEP, and reports
    FreeCAD version, hash, validity, solid count, volume, bounds, and centre of
    mass.
- `scripts/cad/aggregate_work006.py`
  - verifies identity and hashes, gates analytical/CadQuery/FreeCAD evidence,
    feeds FreeCAD volume into Level 0, checks the controlled hypothesis, and
    writes the replay summary.
- `scripts/run_work006.ps1`
  - performs the complete local sequence and rejects missing evidence even if
    an external process returns success.

### Tests and documentation

- `tests/test_component_grammar.py`
  - tests valid production, mapping round-trip, version/schema rejection,
    finite/range gates, material constraints, all implemented ligament/web
    rules, and monotonic analytical volume.
- `tests/test_cad_level0.py`
  - tests measurement admission, FreeCAD-derived mass, analytical Level 0
    outcome, malformed evidence, topology/validity failures, volume disagreement,
    bounds disagreement, and invalid controls.
- `docs/3d/CONSTRAINED_COMPONENT_GRAMMAR.md`
- `docs/3d/CONSTRAINED_COMPONENT_GRAMMAR.th.md`
  - define the production, SI units, coordinates, constraints, equations,
    evidence loop, experiment, invocation, and claim limits.
- matching Work 006 plan/result records in English and Thai.

Generated evidence is intentionally ignored by Git under `artifacts/work006/`.

## Key Decisions

1. **Keep version 1 narrow.** The only production is a rounded prismatic plate,
   four fixed-interface holes, an optional circular centre cut, and one declared
   density. No arbitrary generated Python or free topology enters the grammar.
2. **Use SI at the domain boundary.** Conversion to millimetres occurs only in
   the CadQuery adapter; CAD outputs are converted back to SI before admission.
3. **Use independent imported volume for Level 0.** Analytical and CadQuery
   volumes are gates. The component mass used by Level 0 is strictly
   `FreeCAD STEP volume * declared density`.
4. **Make failures observable.** There is no parameter clipping, silent topology
   repair, or analytical substitution for missing CAD evidence.
5. **Treat the mounting pattern as interface geometry.** The four ports remain
   symmetric and controlled while only the centre-cut radius changes.
6. **Use FreeCAD's bundled Python runtime.** On this installed 1.1.3 build,
   `FreeCADCmd` returned exit code `0` without executing `.py` or staged
   `.FCMacro` inputs. The bundled `bin/python.exe` imports the same FreeCAD and
   Part modules, executes deterministically, handles paths containing spaces,
   and exposes a reliable process exit code.
7. **Require an output evidence file as well as exit code `0`.** This directly
   prevents the observed `FreeCADCmd` false-success mode from passing the loop.

## Controlled Experiment

### Variables and controls

- Independent variable: `lightening_radius_m = 0, 0.025, 0.040`.
- Dependent variables: CAD volume/residuals, density-derived mass, Level 0 final
  speed, and Level 0 final distance.
- Controlled: every other dimension, the four mounting ports, material density,
  seed, software route, base vehicle mass `300 kg`, traction `1200 N`, duration
  `5 s`, and timestep `0.05 s`.
- Negative case: radius `0.055 m`, expected to violate the `0.006 m` minimum
  outer-edge ligament before CAD.

### Final evidence

| Candidate | FreeCAD volume (`m^3`) | CQ-to-FreeCAD residual (`m^3`) | Analytical relative residual | Mass (`kg`) | Final speed (`m/s`) | Final distance (`m`) |
|---|---:|---:|---:|---:|---:|---:|
| `solid_reference` | `0.00018970477868423448` | `5.9631119486702744e-19` | `3.2862443081460257e-15` | `0.51220290244743305` | `19.965911340870651` | `49.914778352176597` |
| `relief_25mm` | `0.00017399681541628494` | `5.4210108624275222e-20` | `3.1155805061476737e-16` | `0.46979140162396932` | `19.968729541866246` | `49.921823854665597` |
| `relief_40mm` | `0.00014949239271828358` | `-9.2157184661267877e-19` | `6.3459878036240901e-15` | `0.40362946033936564` | `19.973127524386776` | `49.932818810966978` |

All imported bounding boxes were exactly `0.2 x 0.12 x 0.008 m` at the recorded
precision. FreeCAD reported one valid solid for every STEP.

The final STEP evidence from the recorded run was:

| Candidate | Bytes | SHA-256 |
|---|---:|---|
| `solid_reference` | `50828` | `0BDDBDC39F0FEF749B158B7033EF7DA684BEAB5E623492442BCACB1101162936` |
| `relief_25mm` | `55774` | `EB635ECDA1F22CABDC8F906853C1AE3862F025E8BB8503CF2090EC69EB28B909` |
| `relief_40mm` | `55770` | `341A69FBD8DA42C3352AF53DAF7F78C7CC59C0E92F8120FDA01614301FFD0A4D` |

The invalid evidence was:

```text
candidate_id: invalid_relief_55mm
stage: grammar_validation_before_cad
cadquery_executed: false
error_type: GrammarViolation
message: lightening cut violates the minimum outer-edge ligament
generator exit code: 2 (expected)
```

All monotonic checks were `true`:

- FreeCAD volume strictly decreased;
- component mass strictly decreased;
- Level 0 final speed strictly increased;
- Level 0 final distance strictly increased.

### Falsification review

- Supporting evidence: three valid candidates passed analytical, CadQuery, and
  FreeCAD gates; FreeCAD measured the exact STEP hashes; the controlled trend
  passed; the deliberately invalid candidate was rejected at the intended
  boundary.
- Contradicting evidence: none within the predeclared Work 006 metrics.
- Alternative explanations: the Level 0 trend follows the already declared
  point-mass equation and says nothing about whether removing material is
  structurally useful; CadQuery and FreeCAD both depend on OCCT-family geometry.
- Missing evidence: loads, boundary conditions, material allowables, FEA,
  convergence, fatigue, joints, manufacturing, assembly, collision, uncertainty,
  and empirical measurement.
- Confidence: high for this local pipeline run; none for physical suitability.

## Replay Metadata and Artifacts

- Repository commit present during the run:
  `f59879976f5cd56b57de7532ec6748c2da71d0ee`
- Worktree dirty during run: `true`, because Work 006 itself was uncommitted.
- Seed: `6001`.
- CadQuery: `2.8.0`.
- FreeCAD: `1.1.3`.
- Config SHA-256:
  `0EBE4E9CBBC99AFCFFD3237817CAB2B9C50ABE73139EA6438C40B89A2D86A6F4`.
- Final summary:
  `artifacts/work006/experiment_summary.json`.
- Final summary SHA-256:
  `23563ABBCC232E5A08C47798A514FDE27833EDFFF5D0030D5FC484AF69AA769F`.

Because the run occurred in a dirty worktree, the summary also records exact
SHA-256 values for the executed source surface:

| Source | SHA-256 |
|---|---|
| `src/formula_ultimate/components/grammar.py` | `8DDDFECDB6F4934BBFBA1A8E618F8D65242AF49BD62005280DA8EDBD94B7482E` |
| `src/formula_ultimate/experiments/cad_level0.py` | `D65CD624D9CA4BDB5962529CA55A96355AF859E6B4ED943D451481301D35FACD` |
| `scripts/cad/generate_mounting_plate.py` | `1302445A9B6F1E0568795105188D01D93E586289EFC5CF2072A93831B8AE79B4` |
| `scripts/cad/inspect_step_freecad.py` | `8B036B0512E233C770A3C33373E2AD28851E9B610B50BB6A78609189CAE62DED` |
| `scripts/cad/aggregate_work006.py` | `D98C1DD9883C857265F57AB8BDF9F9DDEE0EA42383B729FA0E1C6158B4F7A100` |
| `scripts/run_work006.ps1` | `C214EE1A544AF737636F9CA3046B7B57DAB9EDCDEFC9531A999835144B0C4F5F` |

The STEP hash authenticates one recorded exchange artifact but is not expected
to be identical across reruns because the STEP exporter writes run metadata
such as timestamps. Deterministic replay is therefore judged by declared inputs,
valid topology, dimensions, and measured physical properties within tolerance,
not byte-identical STEP serialization.

## Exact Validation Commands and Results

### Final combined validation

Command:

```powershell
py -3.14 -m unittest discover -s tests -v
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work006.ps1
py -3.14 -m compileall -q src scripts tests
git diff --check
```

Exit status: `0` for every command.

Relevant output:

```text
Ran 32 tests in 0.159s
OK
candidate_count: 3
status: passed
component_mass_strictly_decreases: true
freecad_volume_strictly_decreases: true
level0_final_distance_strictly_increases: true
level0_final_speed_strictly_increases: true
```

`compileall` and `git diff --check` produced no errors. Git emitted only the
existing Windows line-ending warning for two modified `__init__.py` files.

### Relevant failed attempts retained as evidence

1. The first focused unit run returned exit code `1` because the test used a
   `0.020 m` pitch while the computed required pitch was only `0.018 m`. The
   test was corrected to `0.015 m`; the rule implementation did not change.
2. Initial full-loop attempts using `FreeCADCmd` returned overall exit code `1`.
   FreeCAD printed `Unknown extension` for an 8.3 `.PY` path but itself returned
   `0`; no measurement file existed.
3. Staging a lowercase `.py` or `.FCMacro` path still produced no executed
   evidence on this build. The launcher now uses FreeCAD's bundled Python and
   also checks the output file.
4. The first bundled-Python import run returned exit code `1` because the
   top-level imported STEP compound lacked `CenterOfMass`. The adapter now first
   requires exactly one solid and reads `shape.Solids[0].CenterOfMass`; no CAD
   value was substituted or repaired.

## Deviations from Plan

- Added `config/work006_mounting_plate.json` and
  `scripts/cad/aggregate_work006.py` to keep variables/controls declarative and
  make the evidence admission step independently testable.
- Replaced planned `FreeCADCmd` invocation with the installed FreeCAD bundled
  Python after recording the false-success behavior described above.
- No Fusion or community FreeCAD MCP work was added.

## Limitations

- Level 0 uses only added point mass under constant traction. The speed and
  distance differences are mathematically coherent but are not evidence of
  lap-time or component performance.
- Constant density `2700 kg/m^3` is an assumption, not a material certificate.
- The grammar's `0.006 m` ligament/web rules are syntax constraints chosen for
  this experiment, not stress-derived design allowables.
- CadQuery and FreeCAD are separate programs but not independent geometric
  kernels in the strongest sense because both use OCCT-family technology.
- No byte-identical STEP replay guarantee is made.
- No Level 1/2/3 simulation or scientific validation was performed.

## Follow-up Work

1. Add named loads, attachment semantics, manufacturing process, and material
   allowables before any structural question is asked.
2. Define a separate planned work item for mesh generation, boundary-condition
   audit, solver convergence, and an FEA baseline that tries to falsify the
   lightening preference.
3. Compare fixed and free topology only after equalizing component library,
   constraints, seeds, candidate evaluations, and measured compute budget.
4. Preserve the Work 006 solid plate as the fixed-topology geometry baseline;
   do not treat the lightest plate as promoted until stronger evidence exists.
