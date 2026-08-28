# Work 024 Problem Report: Three-Contact Fixture Baseline Imbalance

Status: Resolved

Thai companion: `2026-08-28_024_three-contact-fixture-balance.th.md`

## Problem and impact

The first three-contact Work 024 test used rear longitudinal positions
`-0.667 m`. Decimal rounding made the declared baseline loads produce a real
pitch residual of `-1.7658 N*m`, so the existing `PlanarVehicle` contract
rejected the fixture before coupling. Production coupling code was not at fault.

## Fix and verification

Use the exact analytical coordinate `-2/3 m`, which closes the baseline pitch
moment for the `40%/30%/30%` load split. The three-contact aero/load coupling
then passes with three outputs and the full Work 024 suite passes 10/10.
