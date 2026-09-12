# Moving Contact Assembly V1

Thai companion: `MOVING_CONTACT_ASSEMBLY_V1.th.md`

Status: Implemented by Work 114 for a bounded two-coordinate assembly.

## Scope and dependency

This contract pins Work 113 commit `2c6434bfbc2b1776b2ed922fc9b4084c69c03ff5` and its detailed-connection contract. It consumes the threaded-reference reduced normal/tangent stiffness, `4000 N` preload and `0.25` friction without silently replacing them. A `0.2 kg` member moves only along its declared prismatic axis; tangential motion is a prescribed contact probe.

The base applies a sinusoidal reversal of amplitude `2e-6 m` at `20000 Hz` for `0.0005 s`. The tangential probe amplitude is `1e-7 m`. Explicit time steps are `5e-7`, `2.5e-7` and `1.25e-7 s`. Unilateral normal penalty contact uses the preload compression; reaction is computed from penetration. Coulomb capacity determines stick/slip. Opening, closing, slip start/recovery, normal impulse and complete deterministic histories are recorded.

## Gates and failure behavior

The axial energy ledger includes kinetic/contact/preload energy, base-boundary work and damping loss. Relative energy residual must not exceed `0.12`; constraint drift must not exceed `1e-12 m`; swept clearance must remain at least `1e-6 m`. Last-two relative changes of maximum displacement, maximum contact force and transmitted normal impulse must each be at most `0.12`.

Swept clearance is checked throughout motion. A collision blocks that assembly only. Rigid/moving conflict and severed coupling fail closed. Free rigid motion must match its analytic trajectory. Opening or slip invalidates use of the Work 113 reduced stick model outside its registered range; it does not erase the detailed event history.

This is a bounded axial dynamic model with prescribed tangential history. It is not general 3D collision/contact, flexible-body or full multibody dynamics, complete suspension, crash evidence, vehicle readiness or physical validation.
