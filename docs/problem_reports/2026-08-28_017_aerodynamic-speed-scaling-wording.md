# Work 017 Problem Report: Aerodynamic Speed-Scaling Wording

Status: Resolved

Thai companion: `2026-08-28_017_aerodynamic-speed-scaling-wording.th.md`

## Problem

The initial Work 017 plan described the aerodynamic force check as
"inverse-square force scaling." That phrase is physically wrong for the
declared quasi-steady coefficient model. At fixed density, reference geometry,
and coefficient, aerodynamic force is proportional to airspeed squared, not
the inverse square of airspeed.

## Root cause

The intended phrase was "speed-squared scaling" but the word "inverse" was
introduced while drafting the test scope. The equations in the same plan
already used the correct dynamic pressure `q = 0.5*rho*V^2`.

## Fix

Both language plans now say "speed-squared force scaling." The implementation
and tests use the declared `V^2` relationship, with no inverse-speed law.

## Verification

The Work 017 analytical test and validator must compare otherwise identical
points at `20 m/s` and `40 m/s`: force and moment magnitudes must have ratio
`4`, while ram-air mass flow must have ratio `2`.

This wording issue was found before the aerodynamic implementation was written;
no incorrect physics code or generated evidence existed.
