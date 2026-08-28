# Problem Report: Health Adapter Re-emitted Energy Residual IDs

Status: Resolved

Thai companion: `2026-08-29_028_duplicate-energy-residual-ownership.th.md`

## Problem

The Work 027 health calculation retained truncated energy residuals and its adapter re-emitted them as transaction evidence after the energy adapter had already published the same `energy.*` IDs.

## Impact

The first complete eight-stage transaction failed with `evidence_identity_duplicate` despite every numerical residual passing.

## Fix

Keep truncated-energy residuals inside `CentralHealthEvidence` for inspection, but publish only adapter-owned `health.*` residuals from `health_event_solver`. Invalidity still fails closed through the health result status.
