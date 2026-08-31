# Work 064 Plan: Work 062 Finalist Nonlinear Execution

Status: Stopped — deterministic verify-only replay compared tuple-valued in-memory evidence with list-valued strict-JSON evidence

Thai companion: `2026-08-31_064_work062-finalist-nonlinear-execution-plan.th.md`

## Objective

Apply committed gate `whole_vehicle_geometric_nonlinearity_gate_v1` to all and only the 51 Work 062 candidates that passed frozen holdout, Work 053 refinement, and STEP/FreeCAD witness. Preserve every nonlinear case as append-only, hash-chained evidence and adjudicate without retry or silent repair.

## Experimental design

- Independent variable: exact Work 062 finalist geometry; no new search or geometry change.
- Dependent variables: CalculiX nonlinear convergence/confirmation, maximum displacement, maximum surface von Mises stress, linear-reference amplification ratios, yield margin, case status, and candidate status.
- Controls: Work 062 stage fingerprint, exact two holdout cases, 16 B31 subdivisions per branch, Work 053 synthetic material, fixed boundary/load mapping, CalculiX identity, and frozen Work 063 thresholds.
- Inclusion: candidate IDs must equal the exact intersection represented by Work 062 refinement-passed and CAD-witness-passed evidence, with expected cardinality 51. Outcomes cannot alter the set.
- Failure: missing/tampered source evidence, identity mismatch, nonzero process exit, missing `nonlinear geometric` confirmation, non-finite output, threshold violation, incomplete terminal ledger, or replay mismatch remains visible and fails closed.

## Scope and planned files

- Add `scripts/structural/run_whole_vehicle_nonlinear_gate.py` with execution, resume, chained ledger, deterministic summary, and verify-only replay.
- Add focused runner tests.
- Generate ignored evidence under `artifacts/work064/`.
- After execution, add bilingual research result and Work 064 result documents and update this plan status.

## Validation and success criteria

Success requires exact source fingerprints, 51 unique included candidates, 102 unique terminal case results, 51 terminal candidate adjudications, exact replay fingerprint, explicit pass/failure distributions, focused and full tests, compilation, bilingual records, and post-result-commit clean-tree verify-only replay. Zero passing candidates is a valid outcome if evidence is complete.

## Commit structure

This work intentionally uses two commits. The first freezes this plan, runner, and tests before candidate execution so the run begins from a clean committed tree. The second records the terminal bilingual result after validation. No threshold, inclusion rule, code, or config change is permitted between those commits; any such change stops this execution and requires a new work item/protocol identity.

## Risks and non-goals

Risks are nonlinear solver nonconvergence, output/parser ambiguity, partial interruption, and low-load insensitivity. Resume may continue missing cases but never retry a consumed terminal case. This execution does not claim buckling certification, solid/contact/material-nonlinear behavior, fracture, fatigue, physical validation, safety, manufacturability, or algorithm superiority. Independent search replication remains a later work item.
