# Work 008 Result: Ten Real-Circuit Physics Profiles

Status: Completed

Thai companion: `2026-08-25_008_real-circuit-physics-result.th.md`

## Outcome

Implemented a deterministic, source-audited Level-0 catalogue of ten real
Formula One circuits. Vehicle generation can now receive conflicting
track-specific design pressures before design, and vehicle width can be
screened against applicable published minimum widths before race simulation.

The deliberately oversized `7.0 m` reference vehicle with `0.25 m` clearance
per side is rejected at Monaco. Missing or layout-inapplicable width evidence
returns `indeterminate`; it is never silently admitted.

## Files changed

- `src/formula_ultimate/physics/circuit.py`
- `src/formula_ultimate/physics/__init__.py`
- `config/circuits/real_circuits_v1.json`
- `scripts/validate_circuits.py`
- `tests/test_circuit.py`
- `docs/physics/CIRCUIT_MODEL.md`
- `docs/physics/CIRCUIT_MODEL.th.md`
- `docs/research/REAL_CIRCUIT_SOURCE_REPORT.md`
- `docs/research/REAL_CIRCUIT_SOURCE_REPORT.th.md`
- this Work 008 plan/result pair in English and Thai

No unrelated pre-existing Work 006 or Work 007 changes were rewritten or
removed.

## Implemented behavior

- Ten profiles: Monaco, Monza, Spa-Francorchamps, Singapore, Suzuka,
  Silverstone, Hungaroring, Mexico City, Bahrain, and Sao Paulo.
- Strict dataclasses validate identifiers, SI values, pressure bounds, source
  metadata, width-source linkage, duplicate IDs, and race-distance residuals.
- Eight coarse ordinal design-pressure axes are visibly separated from
  published circuit facts; all ten vectors are distinct.
- Static width results are `screen_passed`, `rejected`, or `indeterminate`.
- Applicable width evidence exists for Monaco `7 m`, Monza `10–12 m`, Suzuka
  `10–16 m`, and Sao Paulo `12–15 m`.
- ISA dry-air density is calculated only where sourced numerical altitude is
  present. Mexico City at `2,285 m` produces `0.9779651043911286 kg/m^3`.
- Official race distance and the rounded lap-length product remain separate;
  their difference is exposed as `race_start_offset_m`.
- The validator emits deterministic JSON suitable for later agent admission
  checks and experiment metadata.

## Decisions and corrections

1. Published fact fields and derived pressure hypotheses remain separate.
2. A width pass is explicitly only a necessary static screen, not proof that a
   vehicle can turn or avoid a wall with its swept volume.
3. Singapore uses the FIA 2025 `4.94 km`, 19-turn, 62-lap layout. The
   organizer's historical `10–15 m` width belongs to the superseded 2008
   layout, so Singapore remains indeterminate.
4. A search result initially appeared to support Bahrain `14–15 m`. Full-page
   inspection showed that the value belongs to the **Inner Track**, not the
   Formula 1 Grand Prix Track. It was removed as a hard constraint and retained
   only as non-applicable evidence. Bahrain remains indeterminate.
5. The Sao Paulo municipal circuit operator supplies the fourth applicable
   width range, `12–15 m`.
6. Unknown altitude, width, and detailed geometry are observable missing
   evidence, never substituted with plausible estimates.

## Validation evidence

### Full test suite

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`

Relevant output:

```text
Ran 42 tests in 0.228s
OK
```

The ten circuit tests include deterministic loading, exact catalogue count,
distinct bounded pressure vectors, ISA density, oversized rejection, static
pass limitations, indeterminate missing evidence, source linkage, observable
race-distance residual, and invalid-input rejection.

### Oversized envelope falsification run

```powershell
python scripts/validate_circuits.py --vehicle-width-m 7.0 --clearance-per-side-m 0.25
```

Exit status: `0`

Relevant output:

```text
"circuit_count": 10
"width_evidence_count": 4
"status_counts": {
  "indeterminate": 6,
  "rejected": 1,
  "screen_passed": 3
}
Monaco: minimum_width_m=7.0, status=rejected
Mexico City: isa_air_density_kg_per_m3=0.9779651043911286
```

### Compilation

```powershell
python -m compileall -q src scripts tests
```

Exit status: `0`; no output.

### Whitespace check

```powershell
git diff --check
```

Exit status: `0`; only existing Git line-ending warnings were emitted.

## Supporting and contradicting evidence

Supporting evidence: the oversized reference does not have universal circuit
eligibility, and every circuit has a unique pre-design pressure vector.

Contradicting evidence and alternative explanations: a static screen does not
model steering or swept volume; six profiles lack applicable published minimum
width; pressure scores are human-authored ordinal hypotheses; later lap-time
differences may arise from control quality, surface, weather, or missing
geometry rather than vehicle topology.

Confidence is high for the cited race-scale facts, medium for the four static
width screens, and low-to-medium for the pressure hypotheses until sensitivity
and telemetry comparison are completed.

## Limitations

- This work provides no surveyed 3D centerline, boundary, wall, kerb, runoff,
  camber, banking, gradient-by-station, or pit-lane model.
- `screen_passed` is not physical validation and does not authorize a vehicle
  for a race.
- ISA density is a dry reference atmosphere, not event weather.
- A single circuit profile cannot represent wet/dry state, rubber evolution,
  wind, temperature, or time-varying grip.
- Public source pages can change; the access date and layout reference must be
  preserved for deterministic replay.

## Follow-up work

1. Add versioned surveyed 3D centerlines and left/right corridor boundaries.
2. Add full-vehicle swept-volume checks using width, length, wheelbase,
   steering lock, overhang, roll, and pitch.
3. Add gradient, banking, curvature, surface, and weather distributions with
   explicit uncertainty.
4. Calibrate and attempt to falsify the ordinal pressure vectors against
   telemetry or a higher-fidelity reference simulator.
5. Feed circuit admission and pressure metadata into the vehicle-generation
   grammar before whole-car optimization begins.
