# Generalized Meshed Structural Coupling V1

Thai companion: `GENERALIZED_MESHED_STRUCTURAL_COUPLING_V1.th.md`

## Purpose and boundary

This contract extends exact-geometry Gmsh/CalculiX verification from Work 082's single `z`-axis hole and `x` support plane to arbitrary principal-axis end planes, `y`-axis cylindrical surfaces, combined force/couple loads, and arbitrary principal-axis support planes. It is synthetic meshed software evidence, not physical or design validation.

## Required identities and cases

Every run must verify the frozen Work 084 result, geometry-manifest, canonical FreeCAD-report, and per-part STEP identities before meshing. The required cases are:

- `output_shaft_combined`: `415.3846153846154 N` radial force plus `22.8 Nm` torque;
- `support_block_bearing`: `384.6153846153847 N` bore load; and
- `converter_housing_mount`: `8 Nm` bore couple.

Each case uses three strictly decreasing characteristic lengths declared before execution. Loaded and supported nodes must be non-empty and disjoint.

## Load and evidence rules

Triangle area contributes one third of its force weight to each vertex. A torque about `y` uses area-weighted tangential nodal forces, removes net-force roundoff, and scales the resulting couple to the declared torque. Values below `1e-12 N` are canonical arithmetic zero. CalculiX load values use fixed-width scientific notation to stay inside its free-field token limit.

The solver reports loaded/support node count, loaded area, displacement, compliance, p90 von Mises stress, force residual, moment residual, and external-versus-internal energy residual. Raw runtime metadata in FRD is canonicalised only for hashing; physical output is not altered.

## Gates and failure semantics

- force residual `<=1e-5`;
- moment residual `<=1e-5`;
- energy residual `<=1e-4`;
- last-two-mesh relative change `<=12%` independently for maximum displacement, compliance, and p90 stress.

A missing identity/surface/support, solver failure, non-finite metric, residual excess, or any one convergence excess fails the run. The gate is not averaged across metrics or cases. A severed support must set transmitted force and torque to zero and cause `dnf`.

The only possible passing verdict is `synthetic_meshed_verification_only` with `design_use_allowed=false`. No fatigue, fracture, contact, fastener, bearing-life, manufacturing, safety, or physical claim follows.
