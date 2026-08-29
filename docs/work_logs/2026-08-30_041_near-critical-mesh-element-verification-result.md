# Work 041 Result: Near-Critical Mesh and Element Verification

Status: Completed

Thai companion: `2026-08-30_041_near-critical-mesh-element-verification-result.th.md`

## Outcome

The declared experiment executed successfully, while the preferred combined convergence hypothesis was rejected. C3D4 last-two-mesh changes were `0.702%`, `1.694%`, and `4.323%`, all within `5%`. Refined C3D4/C3D10 differences were `1.455%`, `3.512%`, and `9.213%`; the highest-load result exceeded `5%`. Gate A therefore remains open and post-buckling promotion remains blocked.

## Files changed

- `config/structural/near_critical_element_verification_v1.json`
- `src/formula_ultimate/structural/element_verification.py`
- `src/formula_ultimate/structural/__init__.py`
- `scripts/structural/run_near_critical_element_verification.py`
- `scripts/run_work041.ps1`
- `tests/test_element_verification.py`
- `docs/physics/NEAR_CRITICAL_ELEMENT_VERIFICATION.md`
- `docs/physics/NEAR_CRITICAL_ELEMENT_VERIFICATION.th.md`
- the matching Work 041 bilingual plan and result records

Ignored evidence was generated under `artifacts/work041/`. Mesh-only pilot files remain under `artifacts/work041_pilot/`.

## Decisions and evidence

- Froze C3D10 `1.4 mm` before observing any C3D10 solver result. Pilot node counts were `65,835` for C3D4 `0.65 mm` and `57,426` for C3D10 `1.4 mm`.
- Added MSH2 support for Gmsh linear/quadratic tetrahedra and triangles, the verified Gmsh-to-CalculiX C3D10 final edge-node conversion, and exact consistent TRI6 face loading.
- Preserved multiple integration-point stress records instead of silently replacing them.
- The first solver attempt was not admitted: buckling-deck filtering accidentally removed `*NODE FILE`, so FRD mode vectors were absent. The transformation was corrected, focused tests were rerun, and only the subsequent complete run was admitted.
- Execution gates, reaction closure, mode identity, compute comparability, secant checks, and C3D4 refinement passed. The cross-family high-load convergence gate failed as designed.

## Validation

```powershell
py -3.14 -m unittest tests.test_element_verification tests.test_eigenvalue_buckling_acceptance tests.test_nonlinear_imperfect_column -v
# exit 0; Ran 11 tests; OK

.\scripts\run_work041.ps1
# exit 0; status=passed; convergence_hypothesis.status=rejected

.\scripts\run_work039.ps1
# exit 0; status=passed; its previously rejected hypotheses remained observable

py -3.14 -m unittest discover -s tests -v
# exit 0; Ran 295 tests in 19.614s; OK

py -3.14 -m compileall -q src scripts
# exit 0
```

Repository-contract checks, `git diff --cached --check`, the explicit commit, and the clean-tree Work 041 replay are recorded in the final handoff after the commit exists.

## Limitations and follow-up

Strain energy is explicitly `not_requested` because Work 041 has no independently validated energy parser. Memory evidence is a deterministic node-count proxy, not measured process peak RSS. Comparable node count does not establish equal discretization error. There is no material nonlinearity, fracture, fatigue, post-critical continuation, physical coupon, or whole-vehicle evidence here.

The next roadmap work may start Work 042 plasticity as an independent stream. Gate A cannot close until a separately planned remedial element/asymptotic refinement study resolves or bounds the `9.213%` disagreement.
