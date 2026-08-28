# Work 023 Plan: Typed Circuit and Environment Step Inputs

Status: Completed

Thai companion: `2026-08-28_023_typed-step-inputs-plan.th.md`

## Objective

Implement deterministic typed circuit, spatial, weather, traffic, and strategy
inputs for the ten real-circuit profiles and connect them to the Work 022 input
adapter boundary. Missing evidence must remain explicit and must never become a
silent neutral condition.

## Scope

- Define immutable SI records for local circuit geometry, atmosphere/weather,
  traffic, and strategy commands with source/provenance identity.
- Define an input scenario and resolution result with exact missing-evidence
  fields and deterministic fingerprint.
- Resolve all ten catalog profiles at a requested race distance.
- Treat absent surveyed spatial evidence and absent weather observations as
  incomplete, not zero curvature, sea-level air, zero wind, dry track, or clear
  traffic.
- Allow an explicitly declared isolated-traffic control; distinguish it from
  unknown traffic.
- Implement the `input_bridge` adapter so ready scenarios emit the four declared
  signals while incomplete scenarios return atomic invalidity with zero writes.
- Add falsification tests, validator, bilingual model/result documents, queue
  updates, problem reports if needed, and one verified commit.

## Planned files

- `src/formula_ultimate/simulation/step_inputs.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_step_inputs.py`
- `scripts/validate_step_inputs.py`
- `docs/simulation/TYPED_STEP_INPUTS.md` and `.th.md`
- `docs/integration/COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.md` and `.th.md`
- this bilingual plan/result pair and any required problem reports

## Experiment definition

- Preferred hypothesis: one typed resolver can deterministically expose which
  of ten circuit scenarios are ready or evidence-incomplete without fabricating
  neutral environment values.
- Independent variables: circuit profile, race distance, spatial/weather/
  traffic evidence, strategy command, evidence identity, and registration order.
- Dependent variables: readiness, missing fields, fingerprint, adapter status,
  emitted signal types, and rollback/publication behavior.
- Controls: existing versioned ten-circuit catalog, SI units, exact circuit-ID
  matching, explicit evidence status, Work 022 atomic transaction contract.
- Success criteria: all ten profiles resolve deterministically; current catalog
  gaps are listed exactly; a complete fixture emits four typed input signals;
  every missing/mismatched/non-finite case fails closed with zero partial writes.
- Failure criteria: a missing field becomes zero/default, fingerprints change on
  replay, scenario evidence crosses circuit IDs, or incomplete inputs reach a
  physics-stage output.
- Falsification: remove each evidence group, use unknown traffic, mismatch
  circuit IDs, inject non-finite/out-of-range SI values, replay/reorder profiles,
  and execute ready versus incomplete input adapters.

## Risks

- The ten catalog profiles are circuit-level facts, not surveyed local racing
  lines; they cannot supply curvature/bank/width at an arbitrary distance.
- Weather and traffic are event-time variables and cannot be inferred from a
  circuit's country or design-pressure score.
- A complete analytical fixture validates the input contract, not a real race.

## Explicit non-goals

- No web refresh of circuit facts, no fabricated real-circuit corridor/weather,
  no aero/contact/motion/energy coupling, no whole-race simulation, no optimizer,
  no physical-validation claim, no README change, and no remote push.

## Validation

```powershell
python -m unittest tests.test_step_inputs -v
python -m unittest discover -s tests -v
python scripts/validate_step_inputs.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```
