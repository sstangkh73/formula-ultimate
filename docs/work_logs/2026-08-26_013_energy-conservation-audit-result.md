# Work 013 Result: Independent Energy-Conservation Audit

Status: Completed

Thai companion: `2026-08-26_013_energy-conservation-audit-result.th.md`

## Outcome and files

Work 013 is complete. `energy_audit.py` adds strict balance/transfer/tolerance
contracts and a deterministic graph audit; `test_energy_audit.py` adds 9
reference/falsification tests; `validate_energy_audit.py` records valid, hidden-
energy, and double-loss outcomes; the bilingual model, queue, and work logs were
updated. Public exports were added in `physics/__init__.py`.

The valid lossy chain closes at `0.0 J`. Hidden energy returns `invalid` with
`-5.0 J`; double-counted loss returns `invalid` with `-10.0 J`. Residuals are not
corrected.

## Decisions and experiment review

- SI joules; nonnegative input/output/loss/transfer; signed storage change.
- Independent component balance, input-interface, and output-interface
  residuals use one scaled tolerance and remain observable.
- Missing, extra, duplicate, or endpoint-mismatched evidence invalidates audit.
- Preferred hypothesis supported: a type-correct graph alone accepts no joule
  claim, while this audit catches deliberate energy creation/loss duplication.
- Controls: identical compiled graph, deterministic order, fixed conventions.
- Alternative explanation excluded by separately matching connection evidence.
- Missing evidence: correctness of upstream equations and time integration.
- Confidence: high for declared algebra; no physical-validation claim.

No material problem requiring a separate report occurred. Missing/duplicate
evidence and numerical tolerances were planned cases and are tested.

## Validation

Run from `C:\Formula Ultimate` with fail-fast handling:

```powershell
python -m unittest tests.test_energy_audit -v
python -m unittest discover -s tests -v
python scripts/validate_energy_audit.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status: `0` for every command. Work-specific output: `Ran 9 tests`, `OK`.
Full-suite output: `Ran 89 tests`, `OK`. Validator: valid chain `0.0 J`; hidden
case `invalid/-5.0 J`; double-loss case `invalid/-10.0 J`;
`residuals_corrected=false`. The staged check is rerun before commit.

## Limitations and follow-up

The audit does not generate energy evidence or validate component physics. Work
014 adds explicit thermal state, cooling, derating, and failure behavior.
