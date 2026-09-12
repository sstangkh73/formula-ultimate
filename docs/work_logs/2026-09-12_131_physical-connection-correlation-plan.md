# Work 131 Plan: Physical Connection Correlation

Thai companion: `2026-09-12_131_physical-connection-correlation-plan.th.md`

Date: 2026-09-12 (Asia/Bangkok)

Status: Stopped — missing qualified permissions, inspected/calibrated manifests and measured raw observations

## Objective and scope

Implement and exercise an offline-only entry, integrity and correlation gate for authorized material/connection measurements. Pin Works 113, 116 and 130; require qualified approval, facility, inspected specimens, calibrated instruments, separated calibration/validation sets and immutable raw observations before any physical claim.

No equipment will be energized or controlled. Because no approval references or measured dataset are currently supplied, the expected bounded outcome is a documented stop at the entry gate, not fabricated physical correlation.

## Variables, controls and files

- IV: approved specimen/joint identity and bounded test condition.
- DV: measured response, uncertainty and model discrepancy when valid records exist.
- Controls: missing calibration, swapped specimen ID, saturation, edited raw hash and stop-condition logic.
- Success: offline gate rejects every incomplete/altered path, exact replay, explicit blocker list and no physical claim without measured data.

Planned files: `src/formula_ultimate/experiments/physical_connection_correlation.py`, `config/development/physical_connection_correlation_v1.json`, `scripts/development/run_physical_connection_correlation.py`, `tests/test_physical_connection_correlation.py`, bilingual `docs/contracts/PHYSICAL_CONNECTION_CORRELATION_V1*`, this bilingual plan/result, and ignored `artifacts/work131/run_a|run_b`.

## Validation

Run the proposed unit, runner/replay, affected Work 113/116/130 regressions, compile and explicit staged-diff checks. The runner analyzes records only and must stop safely when entry permissions/data are absent.

## Risks and non-goals

No autonomous equipment operation, destructive testing, purchasing, fabrication, safety certification, invented approvals or synthetic data relabelled as measured evidence.
