# Work 113 Plan: Detailed Connection Contact

Thai companion: `2026-09-12_113_detailed-connection-contact-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Completed

## Objective and scope

Implement a bounded fastening-scale connection experiment using the exact Work 111 vector-field and Work 112 physical-interface contracts. Compare a threaded reference with a topology-distinct segmented-ramp alternative under the same terminal wrench, envelope, synthetic materials, temperature assumption, preload range and friction uncertainty.

Generate actual mating CAD solids, including the reference helix/root and alternative engagement ramps. Evaluate discrete contact patches with unilateral compression, Coulomb slip capacity, preload, off-axis moment, recovered transmitted wrench and observable opening/slip. Fit a reduced joint stiffness only over the registered load/preload domain and compare it against the detailed discrete response.

## Variables, controls and files

- IV: joining geometry, contact refinement, engagement, preload, friction, clearance, axial/shear load and off-axis moment.
- DV: active contact fraction, opening, slip, tangent stiffness, displacement, transmitted force/moment, stress proxy, balance residual and reduced-model error.
- Controls: common task/materials; analytic helical geometry checks; removed/severed joint, reverse load, increased clearance and reduced engagement; unilateral/contact-friction inequalities; no fictitious supports.
- Success: CAD and semantic interface identities are pinned, threaded reference verification passes, both strategies produce causal bounded transfer evidence, three-level quantities satisfy registered change gates, negative cases fail visibly and replay is exact. A failed alternative remains an admissible negative result.

Planned files: `src/formula_ultimate/structural/detailed_connection_contact.py`, `config/development/detailed_connection_contact_v1.json`, `scripts/development/run_detailed_connection_contact.py`, `tests/test_detailed_connection_contact.py`, bilingual `docs/contracts/DETAILED_CONNECTION_CONTACT_V1*`, this bilingual plan/result and ignored `artifacts/work113/run_a|run_b`.

## Validation

```powershell
python -m unittest tests.test_detailed_connection_contact tests.test_repository_contract -v
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_detailed_connection_contact.py --config config\development\detailed_connection_contact_v1.json --output-root artifacts\work113\run_a
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_detailed_connection_contact.py --config config\development\detailed_connection_contact_v1.json --output-root artifacts\work113\run_b --replay-reference artifacts\work113\run_a\result.json
python -m compileall -q src scripts tests
```

Then run affected regressions, `git diff --check`, explicit staging, cached-scope inspection and `git diff --cached --check`; commit immediately only if every declared gate passes.

## Risks and non-goals

The discrete patch model is not a general nonlinear contact solver; stress quantities are regularized patch averages and thread-root geometry remains finite-resolution CAD. Friction is uncertain and loosening/fatigue are unresolved. Non-goals: universal thread standard, production fastener sizing, fatigue life, safety certification, manufacturing release, physical validation, push or history rewrite.
