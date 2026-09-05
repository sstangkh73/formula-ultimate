# Work 097 Result: Generalized Meshing, Contact, and Failure Evaluation

Thai companion: `2026-09-05_097_generalized-meshing-contact-failure-evaluation-result.th.md`

## Status and outcome

Status: Completed

Work 097 bound seven exact non-primitive Work 096 candidates to deterministic reduced-order cross-method structural benchmarks. All seven passed their frozen model selection, semantic-region binding, refinement, reference-response, force/moment/energy residual, contact-law, intact failure-domain, and connection-state gates. Beam, shell, solid, and contact paths were all exercised.

This establishes evaluator coverage for the seven frozen benchmark adapters. It does not establish a general geometry-derived finite-element capability or physical validity for arbitrary topology.

## Files changed

- `config/structural/generalized_geometry_benchmarks_v1.json`
- `src/formula_ultimate/structural/generalized_geometry_benchmarks.py`
- `src/formula_ultimate/structural/__init__.py`
- `scripts/structural/run_generalized_geometry_benchmarks.py`
- `tests/test_generalized_geometry_benchmarks.py`
- `docs/contracts/GENERALIZED_GEOMETRY_BENCHMARKS_V1.md` and Thai companion
- this plan/result and Thai companions
- ignored retained pilot/replay evidence under `artifacts/work097/run_a` and `run_b`

## Decisions and evidence

- Exact Work 096 semantic-config, FreeCAD-report, and strict-comparison identities are mandatory. Source substitution, missing semantic regions, and hidden geometry repair fail closed.
- Model selection uses measured solid count, section positivity, sampled thickness-to-path ratio, contact declaration, and benchmark load-path type. The runtime covered `beam`, `shell`, `solid`, and `contact`, each with a recorded justification.
- The seven adapters compare separate analytical/refined-reference and discrete paths for curved bending, tapered bending, shell membrane response, branched bending, rib springs, annular bearing compliance, and Hertz contact.
- Discrete levels double strictly. All non-exact cases exceeded observed order `1.5`; exact rib/contact paths were marked exact rather than assigned a fabricated order. The largest fine relative error was `0.0014270788520555852`, below `0.005`; the largest last-two change was `0.0042775693130952114`, below `0.01`.
- Force, moment, and energy relative residuals were zero for the frozen baselines and below `1e-12` gates. Injected non-finite response, residual excess, and non-convergence were rejected.
- The first pilot correctly rejected the `contact_pair` 100 N baseline at yield ratio `1.376816754162322`. Before completion, its frozen baseline load was reduced to `25 N`; the resulting maximum failure ratio is `0.8792554763052145`, so the baseline is intact without post-observation repair. The separate divergence and severed-edge negative controls remain failures by construction.
- All four declared interface laws occurred: `bonded`, `sliding_friction`, `bearing_preload`, and `hertz_frictional`. They are typed benchmark states, not arbitrary 3D nonlinear-contact solutions.
- Seven severed-edge controls produced zero transmitted force/moment and retained affected path IDs. Forced solver divergence remained `invalid` with `fallback_used: false`.

## Identity evidence

- Config SHA-256: `dd74be7242b698354a124916167c4fc7efaa46bd4d505286741ce3cc31aabf8e`
- Work 096 FreeCAD report SHA-256: `96cf848f1dc1482be4b408eb146c36cca324f71b21c74a4b5b5de243412c6c08`
- Work 096 semantic comparison SHA-256: `731ba8b6c167f36703a278da959cf8f586714262995c811ede38b2892599cf7d`
- Work 097 result SHA-256, both runs: `431292b4ffde83569808af6d13a6a6ce81d3fe98683f11e2439532c55843795e`
- Cases: `7`; model coverage: `beam`, `contact`, `shell`, `solid`; evidence class: `reduced_order_cross_method_benchmark`; design use: false

## Exact validation commands

```powershell
python -m py_compile src/formula_ultimate/structural/generalized_geometry_benchmarks.py src/formula_ultimate/structural/__init__.py scripts/structural/run_generalized_geometry_benchmarks.py tests/test_generalized_geometry_benchmarks.py
# exit 0

python -m unittest tests.test_generalized_geometry_benchmarks tests.test_repository_contract -q
# exit 0; 15 tests passed in 2.191 s

python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work097/run_a/result.json
# exit 0; 7 cases passed; result SHA-256 431292b4ffde83569808af6d13a6a6ce81d3fe98683f11e2439532c55843795e

python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work097/run_b/result.json --replay-reference artifacts/work097/run_a/result.json
# exit 0; exact replay matched

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -q
# exit 0; 689 tests passed in 347.187 s; 7 expected environment-dependent skips
```

## Limitations and follow-up

The reference and discrete solvers are reduced-order benchmark adapters operating on Work 096 scalar/section summaries. They do not mesh STEP faces or resolve local stress concentration, local shell buckling, plastic redistribution, crack propagation, fretting, nonlinear contact history, or real material scatter. Thermal stress is a fully constrained upper-bound screen and fatigue is a synthetic power-law screen. Passing does not admit a vehicle design, safety claim, or arbitrary future topology. The next work must add independent geometry-derived meshing/higher-fidelity solver evidence before these unfamiliar candidates can receive stronger structural claims.
