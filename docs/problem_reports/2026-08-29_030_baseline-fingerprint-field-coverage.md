# Problem Report: Baseline Fingerprints Did Not Cover Every Promotion-Relevant Field

Status: Resolved

Thai companion: `2026-08-29_030_baseline-fingerprint-field-coverage.th.md`

## Problem

The Work 029 run fingerprint payload omitted promotion-relevant fields including `real_circuit_admitted` and static-width status. The campaign fingerprint also did not independently verify aggregate consistency.

## Impact

An in-memory record could be altered after construction while retaining a stale fingerprint, allowing a promotion gate to trust evidence whose visible admission fields no longer matched its identity.

## Fix

Bumped baseline campaign evidence to `work029-baseline-campaign-v2`, fingerprinted every run/result field except the fingerprint field itself, and added `verify_baseline_campaign_result` to recompute identities and aggregate invariants. Work 030 rejects campaign evidence when verification fails.
