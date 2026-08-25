# Work 010 Problem Report: Survey-Grade Circuit Geometry Gap

Status: Resolved at the model and evidence boundary

Thai companion: `2026-08-25_010_survey-geometry-evidence-gap.th.md`

## Problem

The ten-circuit source package used by Work 008 contains official race-scale
facts, qualitative circuit descriptions, and a small number of published width
values. It does not contain a complete survey-grade 3D centerline plus left and
right boundaries, wall/kerb geometry, coordinate reference system, timestamp,
and quantified uncertainty for each layout.

Without those fields, a real whole-vehicle swept-volume admission result cannot
be defended. Treating a map image as a dimensional survey or filling missing
curvature, grade, banking, and width with plausible values would create false
physics evidence.

## Impact

- Vehicle length, wheelbase, steering lock, and overhang cannot yet be hard-
  screened on all ten real layouts.
- A static minimum-width pass cannot prove that a vehicle negotiates a hairpin.
- A numerical corridor solver could appear complete while authorizing designs
  from invented geometry.

## Evidence inspected

- `config/circuits/real_circuits_v1.json` provides no station coordinates or
  surveyed boundaries.
- Work 008 records applicable width evidence for only four profiles and
  explicitly marks six width profiles indeterminate.
- Official circuit summary pages and event maps referenced by Work 008 expose
  lap-scale facts or diagrams, not the complete machine-readable survey and
  uncertainty package required by this model.

This report does not claim that no private homologation or engineering survey
exists. It records that no admission-capable survey dataset is present in the
reviewed public/repository evidence.

## Root cause

Track homologation, construction, and survey data are specialized operational
assets. Public race information is designed for sporting/event use and usually
does not expose the coordinate-level boundary evidence needed for independent
vehicle collision clearance.

## Rejected shortcuts

- tracing an unscaled marketing map;
- assuming a single published width applies everywhere;
- inferring radius from corner name or apparent image shape;
- setting missing curvature, grade, or banking to zero;
- calling OpenStreetMap/GPS-style approximate geometry survey-grade without an
  uncertainty audit;
- allowing synthetic verification fixtures to authorize a real race.

## Resolution

Work 010 resolves the engineering/software problem as follows:

1. Define a versioned corridor import contract with SI units, coordinate and
   sign conventions, source identity, evidence class, and uncertainty.
2. Permit `admitted` only for an admission-capable evidence class. Approximate,
   digitized, synthetic, or missing real geometry returns `indeterminate` even
   if its mathematical checks pass.
3. Use transparent analytical straight and constant-radius fixtures to verify
   steering and swept-envelope equations independently of real-track claims.
4. Keep closure error, minimum margins, required steering, and the first failing
   segment observable.
5. Leave all unsupported real-circuit corridor records unresolved until a
   licensed survey, circuit-operator engineering export, or equivalently
   auditable source is ingested.

## Verification required to close Work 010

- synthetic mathematical pass cannot produce `admitted`;
- unsupported real profile returns `indeterminate`;
- surveyed-class analytical fixture may produce `admitted`;
- static-fit/swept-fail and steering-fail cases reject with explicit reasons;
- invalid evidence class, uncertainty, and geometry fail validation.

## Residual limitation and follow-up

The evidence gap is bounded, not converted into real geometry. Acquiring and
licensing survey-grade data remains follow-up work. When such data arrives it
must be imported under the declared contract, independently checked for
coordinate/frame correctness and closure, and versioned without changing the
meaning of earlier experiment results.
