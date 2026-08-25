# Work 013 Plan: Independent Energy-Conservation Audit

Status: Completed

Thai companion: `2026-08-26_013_energy-conservation-audit-plan.th.md`

## Objective

Add an independent joule-domain audit over a compiled Work 012 graph. The audit
must compare every connection transfer, every component input/output, declared
loss, and stored-energy change, expose all residuals, and invalidate hidden or
double-counted energy.

## Scope and equation

For each component over one interval:

```text
r = E_in - E_out - E_loss - delta_E_stored
tolerance = absolute_tolerance_j + relative_tolerance * scale
```

`E_in`, `E_out`, and `E_loss` are nonnegative joules. `delta_E_stored` is signed:
positive stores energy and negative releases it. Scale is the largest magnitude
among declared terms. The audit also requires declared component input/output
to equal sums of matching connection transfers within scaled tolerance.

- Define strict component-balance, connection-transfer, tolerance, violation,
  and audit-result contracts.
- Require exact component/connection coverage of a compiled graph.
- Detect endpoint mismatch, hidden source/sink energy, transfer mismatch,
  component residual, duplicated loss, invalid values, and replay drift.
- Validate lossless and lossy reference chains plus deliberately falsified
  hidden-energy and double-loss cases.
- Add tests, validator, bilingual model/result docs, and a separate commit.

## Planned files

- `src/formula_ultimate/physics/energy_audit.py`
- `src/formula_ultimate/physics/__init__.py`
- `scripts/validate_energy_audit.py`
- `tests/test_energy_audit.py`
- `docs/physics/ENERGY_CONSERVATION_AUDIT.md` and `.th.md`
- queue status and this bilingual plan/result pair
- a separate bilingual problem report only if a material problem is found

## Experiment definition

- Preferred hypothesis: an independent audit catches energy creation or loss
  duplication that a type-correct graph alone cannot detect.
- Independent variables: transfer joules, declared input/output/loss/storage
  change, and tolerance.
- Dependent variables: per-component balance/interface residuals, tolerance,
  violations, total residual, and valid/invalid status.
- Controls: the same compiled graph, SI joules, signed-storage convention,
  deterministic ordering, and scaled tolerance.
- Falsification: lossless and explicitly lossy chains must pass; adding output
  without source/storage release and counting a loss twice must fail; missing or
  extra evidence must fail; residuals must remain visible.

## Validation

```powershell
python -m unittest tests.test_energy_audit -v
python -m unittest discover -s tests -v
python scripts/validate_energy_audit.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

## Success criteria

Reference balances close within scaled tolerance; falsifying cases are invalid;
all residuals and violations are observable; full validation, bilingual
contract, explicit staging, commit, and post-commit verification pass.

## Risks and non-goals

An algebraic audit cannot prove the underlying component equations are correct.
It audits declared interval energy only, not instantaneous power integration,
thermal state, uncertainty propagation, or physical validation. Work 014 must
model thermal state separately. No Work 014 implementation or remote push.
