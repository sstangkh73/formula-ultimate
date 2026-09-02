# Work 073 Result: Sprung-Body, Road, and Tyre Vertical Coupling

Status: Completed

Thai companion: `2026-09-01_073_sprung-body-road-tyre-vertical-result.th.md`

## Outcome

Implemented and falsified a geometry-identified six-DOF vertical system for sprung heave/pitch/roll and three unsprung contact states. Suspension and tyre compliance, deterministic road motion, actual-load feedback to Work 071, vertical energy accounting, contact loss, and travel failure are now explicit. All declared gates passed. This is Level-0 software feasibility evidence, not physical validation or race readiness.

## Files changed

- `config/vehicle/sprung_body_road_tyre_vertical_v1.json`
- `src/formula_ultimate/simulation/sprung_body_vertical_coupling.py`
- `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_sprung_body_vertical_coupling.py`
- `tests/test_sprung_body_vertical_coupling.py`
- `docs/research/SPRUNG_BODY_ROAD_TYRE_VERTICAL_V1.md`
- `docs/research/SPRUNG_BODY_ROAD_TYRE_VERTICAL_V1.th.md`
- this bilingual Work 073 plan/result record set

Ignored deterministic evidence was generated under `artifacts/work073/`.

## Decisions and evidence

- Derived sprung mass `245.95200000000003 kg`, roll inertia `4.218672483307425 kg m2`, and pitch inertia `46.253188363933454 kg m2` from non-ground architecture components.
- Used an implicit-midpoint `6 x 6` solve and evaluated actual tyre loads inside the existing acceleration/load fixed point.
- Preserved initial total energy exactly at `50,000,000 J`; explicit ledgers retain suspension heat, tyre heat, inertial work, and road work.
- Preserved Work 072 result SHA-256 `2e70e32766915af2237b92cee20aa9ee415f65bfc5ab14e56fd02d1bf41628ad`.
- The reference finished `500` steps. Load range was `298.98159710209535` to `1763.2457662772727 N`; maximum heave/pitch/roll were `0.0033467120741574362 m`, `0.019441673288686227 rad`, and `0.03707142724764741 rad`; maximum suspension travel was `0.01138991675295634 m`.
- Maximum generalized-equation, vertical-energy, and combined relative energy residuals were `5.115907697472721e-12`, `1.9463597400459776e-15 J`, and `5.043254643678665e-9`.
- The bump supplied `0.7534111876506473 J` road work. Steering/bump mirror residuals were at most `1.11022302462516e-16` / `1.33226762955019e-15`. Maximum half-step difference was `0.0037196002671815395`.
- Road drop returned uncommitted `contact_loss` at step `23`; the large ramp also met contact loss first at step `192`, contradicting the narrower travel-first expectation. The separate initial-state control returned `suspension_travel` at step `2` with `0.0506249708792031 m`. Values were retained without clipping or relabelling.
- Reference result SHA-256: `802330a0566c746d00beb3f5a6cddb725cfee4a9e9f85e08a8bd509b4a6ce973`.
- Canonical evidence SHA-256: `84c0911f35ef12036fd5dde2dc05183bf727a1bf3f25927c6a2febafd15ea2e3`.
- Primary/replay evidence file SHA-256: `EF22581D6DE1172BFA7181A31E5EFD77B9FFF0FB4959C5521527D1C73CF5BA07`.

## Validation record

```text
python -m unittest tests.test_sprung_body_vertical_coupling -v
Exit: 0
Ran 12 tests in 55.051s — OK

python scripts/experiments/run_sprung_body_vertical_coupling.py --config config/vehicle/sprung_body_road_tyre_vertical_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work073/materialized_architecture_v3.json --output artifacts/work073/experiment_evidence.json
Exit: 0
status=passed; evidence_sha256=84c0911f35ef12036fd5dde2dc05183bf727a1bf3f25927c6a2febafd15ea2e3

python scripts/experiments/run_sprung_body_vertical_coupling.py --config config/vehicle/sprung_body_road_tyre_vertical_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work073/replay/materialized_architecture_v3.json --output artifacts/work073/replay/experiment_evidence.json
Exit: 0
primary SHA-256 = replay SHA-256 = EF22581D6DE1172BFA7181A31E5EFD77B9FFF0FB4959C5521527D1C73CF5BA07

python -m unittest discover -s tests -v
Exit: 0
Ran 454 tests in 126.422s — OK

python -m compileall -q src scripts/experiments/run_sprung_body_vertical_coupling.py tests/test_sprung_body_vertical_coupling.py
Exit: 0

python -m unittest tests.test_repository_contract -v
Exit: 0
Ran 6 tests in 1.635s — OK
```

The final repository-contract, staged-diff, commit, and post-commit checks are reported in the handoff.

## Limitations and follow-up

The model remains linear, small-angle, and synthetic. It omits CAD linkage motion ratios, nonlinear tyre contact, bump stops, chassis flex, anti-dive/squat, measured road spectra, identified parameters, aerodynamic load, wheel gyroscopic effects, and exact sub-step event localization. Shared implementation can hide common-mode equation/ledger mistakes despite mirror and refinement controls.

Next work should add a closed-loop path/circuit controller only after explicitly deciding whether CAD linkage kinematics and nonlinear contact must precede it. Neither path following nor a completed-lap claim exists yet.
