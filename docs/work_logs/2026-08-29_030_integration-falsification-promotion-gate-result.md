# Work 030 Result: Integration Falsification and Promotion Gate

Status: Completed

Thai companion: `2026-08-29_030_integration-falsification-promotion-gate-result.th.md`

## Outcome

Closed the coupled Level-0 implementation queue with a fingerprinted release gate, six deliberate transaction faults, bounded timestep-refinement evidence, typed cross-model requirements, and a fail-closed promotion review. The current repository status is `level0_experimentation_ready_promotion_blocked`: controlled Level-0 candidate experiments may proceed, but no candidate may be called a discovery, real-circuit performer, physically validated design, safe design, or manufacturable design from this evidence.

The Work 029 campaign remains complete at `30/30` runs across ten profiles and three seeds. Its evidence identity is upgraded to `work029-baseline-campaign-v2`, and the promotion gate recomputes identities and aggregate invariants before trusting it.

## Files Changed

- Added `config/simulation/integration_promotion_gate_v1.json`.
- Added `src/formula_ultimate/simulation/integration_release.py` and its public exports.
- Strengthened `src/formula_ultimate/simulation/baseline_campaign.py` with complete field fingerprints and independent result verification.
- Added ten focused tests in `tests/test_integration_release.py`.
- Added `scripts/validate_integration_release.py`.
- Added the bilingual integration falsification/promotion model record.
- Added one bilingual resolved problem report, this plan/result pair, and completed the bilingual implementation queue.
- Updated the bilingual Work 029 campaign record to distinguish its historical v1 fingerprint from the current verified v2 evidence.

## Resolved Problem

The Work 029 run fingerprint omitted promotion-relevant visible fields, including real-circuit admission and static-width status, while the campaign fingerprint did not independently prove aggregate consistency. An altered in-memory record could therefore retain a stale identity. Work 030 now fingerprints every evidence field except each fingerprint field itself and verifies run identity, campaign identity, counts, family/seed matrix, partitions, budgets, residual flags, and real-circuit aggregation before promotion review.

## Decisions

- Require the control transaction to commit and every declared injected fault to produce its expected observable code with no committed state.
- Pin refinement to timesteps `(2000, 1000, 500) s`, seed `17`, one calibration profile, one holdout profile, and a common `128`-step budget.
- Do not estimate convergence order from an exactly invariant steady analytical reference.
- Require independent passing evidence at `level1` or higher for geometry/mass/inertia, surveyed circuit corridor, aerodynamics, structural safety, thermal reliability, and quantified uncertainty.
- Require real-circuit admission separately from cross-model evidence.
- Permit only `eligible_for_independent_review` when all test evidence is present; automatic discovery remains forbidden.
- Authorize only gated Level-0 experimentation while promotion is blocked.

## Experiment and Falsification Result

- Independent variables: six injected fault classes and three timestep values.
- Dependent evidence: failure code, rollback state, detection coverage, finish time, primary energy, finish residual, sensitivity, missing evidence, promotion status, and release status.
- Controls: architecture v4, transaction start state/signals, adapter versions/outputs, Work 029 reference family and opportunity, calibration/holdout profiles, seed `17`, environment/energy controls, timeout, and common run budget.
- Control result: `committed`.
- Fault result: `6/6` detected and rolled back—missing adapter, version mismatch, duplicate residual identity, failed residual, undeclared output, and time regression.
- Refinement result: six samples finished; maximum relative time variation `0.0`; maximum relative primary-energy variation `1.5466148595436325e-14`; maximum absolute finish residual `0.0 m`; convergence order not claimed.
- Promotion result: `blocked` by six missing/invalid independent evidence types plus missing real-circuit admission.
- Relaxed test fixture result: complete independent evidence reaches only `eligible_for_independent_review`, never discovery.
- Supporting evidence: transaction enforcement, deterministic replay, identity verification, budget closure, and explicit claim denial all passed.
- Contradicting evidence: none for the declared software gates; absence of physical evidence contradicts any broader performance or validation claim and is retained as the promotion blocker.
- Alternative explanation: timestep invariance follows the steady drag-balanced analytical control and does not demonstrate nonlinear or higher-fidelity agreement.
- Missing evidence: surveyed circuit corridors and conditions, geometry-derived mass/inertia, independent aero, structural/safety, thermal/reliability, quantified uncertainty, and physical tests.
- Confidence: high for the deterministic software/falsification gates; low for physical or real-circuit performance, which remains explicitly unadmitted.

## Validation Commands and Evidence

All commands returned exit status `0`:

```powershell
python -m unittest tests.test_baseline_campaign tests.test_integration_release -v
python -m unittest tests.test_coupling_contracts tests.test_coupled_transaction tests.test_whole_race tests.test_baseline_campaign tests.test_integration_release -v
python scripts/validate_coupling_contracts.py
python scripts/validate_coupled_transaction.py
python scripts/validate_whole_race.py
python scripts/validate_baseline_campaign.py
python scripts/validate_integration_release.py
python -m compileall -q src scripts tests
python -m unittest discover -s tests -v
git diff --check
git diff --cached --check
```

- final targeted baseline/release regression: 20 passed in `21.195 s`;
- focused Work 021/022/028/029/030 regression: 50 passed in `21.479 s`;
- repository documentation contract: 6 passed in `0.192 s`;
- full repository suite: 262 passed in `21.997 s`;
- campaign result fingerprint v2: `79a03587e6bbeb17101c89a59c7fe61053571f493a29fbe356322418726d2a9b`;
- gate fingerprint: `ad629075e69001b17eaf8b8e9371ecb72fc52a4e07a762c4546096daf9d23814`;
- falsification fingerprint: `a6c0b5a1a30abda519ed230114ca5c49b5754bb2bd763e505ae0f2f77ec15f4b`;
- refinement fingerprint: `fdb02195f1a77709b9f43f5d1b1d86736f73e0862dbb9d605f56017a28462af2`;
- blocked promotion fingerprint: `bf78fcb402c43e633399342d3e93a3473d3f2c4defa2e1447163bc34d059400f`;
- release-review fingerprint: `783e156bb2a8d8dcad356033b6767fb2b2cbef9b9f0f3d1f94df13a83ab94f29`.

## Limitations

The injected adapters isolate transaction enforcement and do not exercise every possible domain defect. The refinement matrix covers a steady Level-0 analytical reference, not nonlinear track dynamics. Completion of the implementation queue is software readiness for gated research, not completion of the Formula Ultimate research program or evidence of a successful vehicle.

## Follow-up

The next research phase should acquire or derive the six independent evidence classes and real-circuit admission data, then submit candidates to higher-fidelity falsification and physical review. Candidate topology remains open-ended; evidence requirements constrain claims rather than prescribe a conventional vehicle layout.
