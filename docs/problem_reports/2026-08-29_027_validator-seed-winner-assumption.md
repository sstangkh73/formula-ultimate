# Problem Report: Validator Assumed Every Seed Changes the Winning Event Time

Status: Resolved

Thai companion: `2026-08-29_027_validator-seed-winner-assumption.th.md`

## Problem

The first Work 027 validator required different seeds to produce different final execution times even when an earlier deterministic thermal failure won both runs.

## Impact

A correct event arbitration result was reported as a validation failure.

## Fix

Keep the same-seed exact replay assertion, but test different seeds against the component reliability draw. The winning time is allowed to remain equal when another earlier event dominates.
