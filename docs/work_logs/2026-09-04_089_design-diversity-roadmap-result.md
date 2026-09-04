# Work 089 Result: Design-Diversity Roadmap

Thai companion: `2026-09-04_089_design-diversity-roadmap-result.th.md`

## Status and outcome

Status: Completed

The new roadmap defines twelve implementation works, Work 090–101, in six two-work batches. It addresses the actual restriction rather than treating fillets as design freedom: the present whole-vehicle search mutates five scalar dimensions on a fixed primitive graph, B-rep Grammar V1 exposes only four starting profile types, and the recent subsystem builders are hand-authored box/cylinder procedures.

The roadmap expands measurement, free-form wire/solid representation, typed topology genomes, topology mutation, manufacturing-valid construction, semantic STEP inspection, generalized meshing/contact/failure evaluation, compute fairness, quality-diversity search, subsystem discovery trials, and final free-topology integration. It freezes the claim boundary that unusual appearance is not functional discovery.

The earliest milestone for curved non-primitive solids is Work 092. The first defensible opportunity for an unfamiliar functional part is after Work 097, with a preregistered discovery trial in Work 100. Whole-candidate research admission remains Work 101 and still does not imply physical validation.

## Files changed

- `docs/reports/GEOMETRIC_DESIGN_DIVERSITY_ROADMAP_V1.md`
- `docs/reports/GEOMETRIC_DESIGN_DIVERSITY_ROADMAP_V1.th.md`
- this result and its Thai companion
- the Work 089 plan and Thai companion, changed to `Completed`

## Decisions and evidence

- Installed CadQuery version: `2.8.0`; local API inspection confirmed `spline`, `splineApprox`, `threePointArc`, `sweep`, `loft`, `fillet`, and `chamfer` are available.
- The roadmap therefore treats the repository representation/search interface—not the CAD kernel—as the first bottleneck.
- Diversity is measured after removing translation, rotation, naming, and uniform-scale equivalences.
- Novelty ranking is downstream of mandatory functional/evidence gates and can never compensate for failure.
- Compute is accounted by attempts, CAD calls, mesh elements, nonlinear iterations, solver time, and total compute so complex families do not lose through invisible cost bias.
- Repair is allowed only as preregistered deterministic pre-evaluation construction and becomes part of candidate identity; result-conditioned repair remains prohibited.

## Exact validation commands and results

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe -c `
  'import cadquery as cq; print(cq.__version__); print({n: hasattr(cq.Workplane,n) for n in ["spline","splineApprox","threePointArc","sweep","loft","fillet","chamfer"]})'
# exit 0; CadQuery 2.8.0; all seven capabilities True

# EN/TH structure comparison
# exit 0; both files: 334 lines, 60 headings, Work 090–101 present in the same order

python -m unittest tests.test_repository_contract -v
# exit 0; Ran 6 tests in 6.350s; OK

git diff --check
# exit 0
```

## Limitations and follow-up

This work is a plan, not an implementation. It does not expand the grammar, mutate topology, generate a novel part, run FEA, or establish discovery. Implementation should proceed in the declared two-work batches beginning with Work 090–091. Starting the discovery trial before Work 097 would recreate the current bias because novel geometry would still lack a general evaluator.
