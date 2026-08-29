# Work 037 Result: Eigenvalue Buckling Verification

Status: Completed

Thai companion: `2026-08-30_037_eigenvalue-buckling-result.th.md`

Implemented three-mesh CalculiX `*BUCKLE` verification, a separate static reaction solve, strict factor/FRD mode parsing, Euler gates, pair-split/transverse-mode classification, and tension/unclamped negative controls. Fine `Pcr=3715.16 N` differs from Euler by `3.248%`; last-two change is `1.648%`.

Failed evidence includes missing factor parser support, coarse-mesh stiffness, invalid Euclidean orthogonality gating for a degenerate subspace, negative tension factors, and solver exit `0` for a missing-support model. The final evidence keeps orthogonality informational and rejects missing support by contract.

Validation returned exit `0`: focused `2 tests`, live Work 037, Work 034-036 regressions, full `286 tests in 35.868s`, compileall, `git diff --check`, explicit staging and `git diff --cached --check`. Limitations: ideal eigenvalue only; no nonlinear imperfection or physical capacity claim. Commit is reported in the final handoff.
