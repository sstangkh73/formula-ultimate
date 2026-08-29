# Work 031 Result: Research Experiment Protocol and Candidate 001

Status: Completed

Thai companion: `2026-08-29_031_research-experiment-protocol-candidate-001-result.th.md`

## Outcome

Created the versioned
`formula_ultimate_research_experiment_protocol_v1` contract and executed
`FU-C0001` through the complete local route:

```text
candidate declaration
  -> CadQuery constrained 3D B-rep
  -> hashed STEP
  -> FreeCAD 1.1.3 import and measurement
  -> analytical/CadQuery/FreeCAD evidence admission
  -> FreeCAD-derived mass
  -> Level 0 point-mass evaluation
  -> falsification review
```

All six required stages passed. This result supports geometry-to-Level-0
pipeline coherence only. `FU-C0001` is a bounded component geometry specimen,
not a complete vehicle or physically validated race design.

## Files Changed

### Protocol and candidate declarations

- `config/experiments/research_experiment_protocol_v1.json`
- `config/experiments/candidate_fu-c0001.json`

These predeclare identity, stage order, claim boundary, silent-correction
policy, hypothesis, variables, controls, tolerances, and failure criteria.

### Evidence contract and executable route

- `src/formula_ultimate/experiments/research_protocol.py`
- `src/formula_ultimate/experiments/__init__.py`
- `scripts/cad/run_research_candidate.py`
- `scripts/run_candidate_001.ps1`
- `scripts/cad/generate_mounting_plate.py`

The generator now accepts either the existing Work 006 multi-candidate config
or one declared candidate. The new runner preserves the failing boundary as
`experiment_failure.json`, authenticates the STEP at both CadQuery and FreeCAD
boundaries, and records config/source/repository/tool/process evidence.

### Tests and documentation

- `tests/test_research_protocol.py`
- `docs/research/RESEARCH_EXPERIMENT_PROTOCOL.md`
- `docs/research/RESEARCH_EXPERIMENT_PROTOCOL.th.md`
- matching Work 031 plan/result records in English and Thai

Generated evidence remains ignored under `artifacts/work031/FU-C0001/`.

## Key Decisions

1. **Start with a geometry-evidence specimen, not a claimed whole vehicle.**
   The repository has no complete-vehicle grammar, assembly-interface solver,
   or packaging/collision system yet.
2. **Keep the protocol technology- and layout-neutral.** The bounded mounting
   plate is an initial test surface, not a prescription for future vehicle
   architecture.
3. **Use the exact FreeCAD-imported STEP measurement for Level 0 mass.**
   Analytical and CadQuery properties are gates, never substitutes for absent
   FreeCAD evidence.
4. **Make failed boundaries data.** The runner records stage, exception,
   process command, output, exit code, and wall time rather than silently
   repairing or retrying geometry.
5. **Separate artifact authentication from semantic replay.** Each run records
   the exact STEP hash, while cross-run geometry/property agreement is judged
   within tolerance because STEP exporter metadata can alter bytes.

## Candidate 001 Experiment

### Predeclared design

- Candidate: `FU-C0001`
- Class: `bounded_component_geometry_specimen`
- Grammar: `mounting_plate_v1`
- Seed: `31001`
- Envelope: `0.200 x 0.120 x 0.008 m`
- Central lightening radius: `0.025 m`
- Density assumption: `2700 kg/m^3`
- Level 0 controls: base mass `300 kg`, force `1200 N`, duration `5 s`,
  timestep `0.05 s`

Preferred hypothesis: the declared candidate can cross all evidence boundaries
without hidden repair or analytical substitution. Because this run contains
one candidate, it does not estimate an independent-variable effect or rank
designs.

### Final recorded evidence

| Evidence | Value |
|---|---:|
| Status | `passed` |
| CadQuery solid count / validity | `1 / true` |
| FreeCAD solid count / validity | `1 / true` |
| STEP bytes | `55,774` |
| STEP SHA-256 | `13881EC14571A6AA8BC8EC3911E46D38C0364ED5691B002B6AB12BF0A0462383` |
| CadQuery volume | `0.0001739968154162849 m^3` |
| FreeCAD volume | `0.00017399681541628494 m^3` |
| FreeCAD minus CadQuery volume | `5.421010862427522e-20 m^3` |
| FreeCAD analytical relative residual | `3.1155805061476737e-16` |
| FreeCAD-derived component mass | `0.4697914016239693 kg` |
| Total Level 0 mass | `300.469791401624 kg` |
| Level 0 final speed | `19.968729541866246 m/s` |
| Level 0 final distance | `49.9218238546656 m` |

FreeCAD version was `1.1.3`. The final run recorded CadQuery generation wall
time `7.05679349997081 s` and FreeCAD import wall time
`0.643542799982242 s`. Machine-readable evidence is at
`artifacts/work031/FU-C0001/experiment_result.json`.

Replay identity from the final run:

- protocol config SHA-256:
  `BBF71CE921E4BFB1B876DC690D2FC5D216F72A3EE13879A3D59BC3D2E8A418E2`
- candidate config SHA-256:
  `1CC3AD2E9083F1502D997367F22CA05B8D83DADE4A23ED2C77291653B2642267`
- repository commit present during the run:
  `557f20570158b96bdcd60f5d3a5da69726e0cb05`
- worktree dirty during the run: `true`, because Work 031 was not committed yet

The result additionally records exact SHA-256 values for all executed source
files, so the dirty-worktree run remains attributable.

## Falsification Review

- Supporting evidence: CadQuery produced one valid solid; FreeCAD imported the
  exact STEP hash as one valid solid; analytical/CadQuery/FreeCAD measurements
  passed declared tolerances; Level 0 consumed FreeCAD-derived mass.
- Contradicting evidence: none within the predeclared pipeline-coherence
  metrics.
- Alternative explanations: CadQuery and FreeCAD share OCCT-family geometry
  technology; the Level 0 trend follows an added-point-mass equation and says
  nothing about structural utility.
- Missing evidence: complete-vehicle geometry/assembly, loads, FEA, fatigue,
  CFD, thermal, manufacturing, safety, empirical evidence, multiple candidates,
  and fair optimized baselines.
- Confidence: high for this local pipeline execution; none for physical
  suitability or race performance.

## Exact Validation Commands and Results

### Focused protocol tests

Command:

```powershell
py -3.14 -m unittest tests.test_research_protocol -v
```

Exit code: `0`

Result: `Ran 6 tests ... OK`. Coverage includes protocol/declaration admission,
silent-repair rejection, internal ID mismatch, missing preregistration,
non-finite tolerance, exact STEP/FreeCAD mass admission, and hash mismatch.

### Candidate 001 pipeline

Command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_candidate_001.ps1
```

Exit code: `0`

Result: candidate `FU-C0001`, status `passed`, claim level
`geometry-to-level0 pipeline coherence only`, STEP SHA-256
`13881EC14571A6AA8BC8EC3911E46D38C0364ED5691B002B6AB12BF0A0462383`.

### Full repository regression

Command:

```powershell
py -3.14 -m unittest discover -s tests -q
```

Exit code: `0`

Result: final rerun `Ran 268 tests in 36.036s ... OK`.

### Work 006 backward-compatibility regression

Command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work006.ps1
```

Exit code: `0`

Result: all three valid candidates passed, the deliberate invalid candidate
was rejected before CadQuery, and all four monotonic checks remained `true`.

### Static and repository checks

Commands:

```powershell
py -3.14 -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit codes: `0`, `0`, and `0` in the final validation/staging sequence.

Result: Python compiled, no whitespace errors were found, and the staged scope
contained only explicit Work 031 files.

## Claims Supported

- The repository now has a versioned, machine-readable research experiment
  protocol and a candidate-specific evidence runner.
- `FU-C0001` passed the exact local `3D -> STEP -> FreeCAD -> Level 0` route.
- The result can be replayed and audited from configs, hashes, versions, process
  evidence, source identity, and structured review.

## Claims Explicitly Unsupported

- `FU-C0001` is not a complete vehicle, optimized design, discovery, or
  physically validated component.
- Level 0 does not establish structural, aerodynamic, thermal, manufacturing,
  assembly, collision, safety, or real race performance.
- CadQuery/FreeCAD agreement is not fully independent geometric theory because
  both use OCCT-family technology.
- No fair multi-candidate or optimized-baseline comparison was performed.

## Deviations from Plan

No material objective changed. The focused protocol suite contains six tests
rather than an unspecified count. The existing generator was minimally
generalized to accept a single-candidate declaration while retaining and
re-running the complete Work 006 route.

## Follow-up Work

1. Define component interface/load semantics and a solver-ready promotion
   contract before asking a structural question.
2. Add a second predeclared candidate only with an explicit baseline role,
   equal compute budget, comparison metric, and falsification target.
3. Build complete-vehicle geometry/assembly/packaging contracts before calling
   any future `FU-Cxxxx` specimen a vehicle candidate.
4. Promote only selected evidence-complete candidates to independent higher
   fidelity; never infer discovery from Level 0 alone.
