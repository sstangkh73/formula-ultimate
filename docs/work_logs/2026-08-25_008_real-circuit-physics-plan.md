# Work 008 Plan: Ten Real-Circuit Physics Profiles

Status: Completed

Thai companion: `2026-08-25_008_real-circuit-physics-plan.th.md`

## Objective

Build the first versioned circuit-physics boundary from ten real racing
circuits with materially different strengths and weaknesses. Circuit evidence
must be available before an agent designs a vehicle, so vehicle dimensions,
packaging, energy, cooling, downforce, braking, traction, and control choices
respond to the physical race environment rather than an abstract uniform track.

## Scope

- Select ten real Formula One circuits that jointly expose substantially
  different design pressures, including narrow street geometry, high-speed
  efficiency, altitude, elevation change, thermal load, heavy braking, low-speed
  traction, fast lateral loading, and short/long lap structure.
- Record source-backed circuit identity and race facts in SI units, including at
  least layout length, lap count, race distance, direction, altitude or
  elevation evidence where available, and a declared track-width/corridor
  constraint where an authoritative source supports it.
- Never invent missing circuit dimensions. Each field must carry provenance,
  evidence quality, and uncertainty or remain explicitly unavailable.
- Define a Level-0/Level-1 circuit profile that can influence physics before a
  full surveyed 3D centreline exists.
- Implement a conservative vehicle-envelope clearance gate so a candidate that
  exceeds a circuit's declared drivable corridor cannot enter race simulation.
- Encode track-character load shares or indices only when their construction is
  explicit, versioned, bounded, and distinguished from measured facts.
- Record track-specific design pressures and failure risks without prescribing
  the vehicle solution.
- Add tests for schemas, units, derived race distance, evidence requirements,
  envelope rejection, deterministic loading, and invalid/non-finite data.
- Maintain all Markdown in separate English and Thai companions.

## Planned Files

- `src/formula_ultimate/physics/circuit.py`
- `src/formula_ultimate/physics/__init__.py`
- `config/circuits/real_circuits_v1.json`
- `scripts/validate_circuits.py`
- `tests/test_circuit.py`
- `docs/physics/CIRCUIT_MODEL.md`
- `docs/physics/CIRCUIT_MODEL.th.md`
- `docs/research/REAL_CIRCUIT_SOURCE_REPORT.md`
- `docs/research/REAL_CIRCUIT_SOURCE_REPORT.th.md`
- matching Work 008 plan/result records in English and Thai

The exact file list may shrink if a smaller interface proves sufficient. Any
deviation will be recorded in the result.

## Model Boundary

### Measured or published facts

- circuit/layout name and country;
- official layout length and race lap count;
- derived and/or official race distance;
- direction and altitude/elevation facts when source-backed;
- width/corridor evidence when source-backed;
- source URL, publisher, publication/access context, and evidence quality.

### Derived screening inputs

- reference air density from declared altitude and atmospheric assumptions;
- conservative maximum vehicle width from the narrowest supported corridor,
  required lateral clearance, and uncertainty margin;
- normalized design-pressure indices for straights, low-speed corners,
  high-speed corners, braking, traction, elevation, thermal environment, and
  street-circuit confinement.

Derived indices are research controls, not claims that replace telemetry or a
surveyed 3D track.

### Future fidelity

- full 3D centreline, curvature, grade, banking, kerbs, walls, runoff, surface
  friction map, roughness, drainage, wind field, weather distribution, and
  time-varying grip remain later work unless authoritative data is available
  and can be validated in this work item.

## Experiment Definition

### Preferred hypothesis

A versioned set of physically different circuit profiles will reject at least
some globally oversized or environmentally mismatched vehicle envelopes and
will produce different predeclared design-pressure vectors, giving an agent
meaningful race-environment information before design generation.

### Independent variables

- selected real circuit profile;
- candidate vehicle width in the envelope-gate reference test.

### Dependent variables

- envelope admission/rejection and reason;
- reference air density;
- circuit design-pressure vector;
- derived race distance residual against the official value when both exist.

### Controls

- circuit-schema version;
- atmospheric equation and constants;
- lateral-clearance and uncertainty policy;
- normalized-index range and construction method;
- candidate envelope used for cross-circuit comparison;
- validation tolerance and software version.

### Falsification and failure criteria

- Attempt to admit a deliberately oversized vehicle to the narrowest supported
  circuit and require observable rejection.
- Reject missing provenance for hard geometric constraints.
- Reject non-finite, negative, out-of-range, duplicate, or internally
  inconsistent circuit data.
- Report rather than fill any missing real-world width, altitude, or geometry.
- Treat a profile set with no meaningful cross-circuit variation as a failed
  research input, not a successful catalog.

## Validation

Planned commands include:

```powershell
py -3.14 -m unittest discover -s tests -v
py -3.14 scripts\validate_circuits.py
py -3.14 -m compileall -q src scripts tests
git diff --check
```

Source review will use current official FIA, Formula 1, circuit-operator, or
government/organizer material where possible. Secondary material may only be
used as explicitly lower-confidence context and not as an unmarked hard
clearance constraint.

## Success Criteria

- Exactly ten real circuits load deterministically from one versioned dataset.
- The set contains materially different physical/design-pressure profiles.
- Every hard real-world field used by physics has source and quality metadata.
- At least one real circuit has a defensible conservative corridor gate, and
  unknown widths remain observable rather than guessed.
- An oversized reference vehicle is rejected before race simulation.
- SI units and atmospheric assumptions are explicit.
- Tests, validation script, compilation, bilingual repository contract, and
  whitespace checks pass.
- Documentation states what the profiles can and cannot prove.

## Risks

- Public official circuit pages often omit minimum width, banking, or detailed
  elevation. A map image is not automatically a dimensional survey.
- Published circuit length may change with layout revision; every profile must
  name and version the layout.
- “Corner count” definitions vary and are not enough to reconstruct curvature.
- A single altitude cannot model a circuit with large elevation change.
- Qualitative track descriptions can bias agent design if presented as measured
  physics; derived indices must remain visibly separate.
- A conservative width gate based on incomplete evidence may be too strict or
  too permissive; uncertainty margin and limitations must be preserved.

## Explicit Non-Goals

- No claim of laser-scan, FIA Grade-1 homologation geometry, or centimetre-level
  clearance accuracy.
- No complete 3D track mesh, racing line, CFD wind field, tyre surface map, or
  lap-time optimizer.
- No vehicle design or optimization in this work item.
- No hard-coded preferred solution for any circuit.
- No silent extraction of dimensions from an unscaled marketing map.
- No physical-validation claim from Level-0 circuit profiles alone.
