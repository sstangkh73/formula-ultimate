# Bounded Main Campaign v2 Admission

Thai companion: `BOUNDED_MAIN_CAMPAIGN_V2_ADMISSION.th.md`

Status: Burn-in accepted; admitted main execution remains conditional on the committed clean-tree replay.

## Why v2 exists

Protocol v1 stopped during excluded-seed burn-in after all 240 training opportunities. Promotion values were unchanged, but an in-memory tuple was compared directly with its JSON list representation. Strict replay rejected the representation mismatch before any holdout or main-seed evaluation. The v1 ledgers and failure hashes remain immutable.

Protocol `bounded_whole_vehicle_main_campaign_v2`, campaign `FU-BMC-002`, changes only identity and remediation provenance. A regression check proves the entire scientific-rule subtree equals v1. The implementation canonicalizes promotion evidence through a strict JSON round trip before append and replay comparison; candidate generation, opportunity budgets, material, loads, thresholds, partitions, physics, hypotheses, outcomes, and analysis are unchanged. No v1 observation enters v2.

## Fresh v2 burn-in result

The isolated process-resume probe stopped one process after reserving `candidate-52a6df50771f058c`; a second process completed exactly that candidate. Reservation/result/pending counts were `1/1/0`.

Seed `55999` then produced:

| Evidence | Result |
|---|---:|
| Training reservations/results/pending | `240 / 240 / 0` |
| Attempts by GRID/RANDOM/EVOLUTION | `80 / 80 / 80` |
| Unique GRID opportunities | `80` |
| Feasible / structural-failure training outcomes | `189 / 51` |
| Promotion streams/candidates/shortfall | `3 / 6 / 0` |
| Terminal holdout/refinement/CAD records | `6 / 6 / 6` |
| Refinement passed | `6 / 6` |
| STEP/FreeCAD witness passed | `6 / 6` |
| Treatment/seed streams with supported finisher | `3 / 3` |
| External solver/CAD processes | `123` |

The training combined fingerprint is `52de5c3a44423b126e6e05b50c594a0a70c4956d084bc4bc2a02b3c4fa9b3054`; the downstream stage fingerprint is `cd019afbe7b85b10e6fc5bc744314b16b281e4dd1701b0eab0c94681f7978e97`. Verify-only replay returned exact.

## Admission boundary

The burn-in decision is `burn_in_accepted_for_admitted_main_campaign`. It authorizes the committed exact implementation to request main execution only after clean-tree verification matches protocol, upstream, CalculiX, CadQuery Python, FreeCAD Python, and implementation hashes. Any later code/config change invalidates admission and stops `FU-BMC-002`.

This result demonstrates bounded pipeline execution, not physical validation. Level 0 is a selection gate; refinement is a linear-elastic beam network; STEP/FreeCAD proves exact primitive geometry transfer. Solid/contact/nonlinear behavior, physical materials, tolerances, manufacturing, hardware safety, and independent replication remain missing.
