# Free-form Vehicle Candidate v1

Thai companion: `FREEFORM_VEHICLE_CANDIDATE_V1.th.md`

Protocol version: `freeform_vehicle_candidate_v1`. Implemented by Work 139.

## 1. What this contract covers

A vehicle candidate declares components. A component is either a primitive
(`box`, `cylinder_z`) or an admitted Work 092 free-form solid referenced by
`corpus_candidate_id`. The composition is built in CadQuery, gated on the built
solids, and every component is scored by the Work 138 evaluator:

```text
declaration -> CadQuery build (primitive or admitted corpus member, placed)
  -> per-component and assembly STEP
  -> packaging measured on the built solids
  -> Work 138 evaluation per component
  -> one registered status per component, and a matched report
```

## 2. Representation rules

- Only members listed in `corpus.admitted_candidate_ids` may be referenced, and
  the corpus declaration SHA-256 is recomputed at build time.
- A corpus member is placed, never scaled or edited. Changing its geometry
  means declaring a new corpus member and passing the Work 092 gate first.
- A new free-form shape may not enter through this protocol.

## 3. Packaging gates, measured on the built solids

1. every component is one valid solid;
2. every component lies inside the declared envelope;
3. no pairwise Boolean intersection above `packaging.maximum_pairwise_intersection_m3`;
4. no keep-out region is invaded;
5. every tag in `required_function_tags` is covered by at least one component;
6. a declared mass that contradicts the built mass beyond `packaging.declared_mass_relative` is rejected.

A candidate that fails any gate is `incomplete_composition`. Substituting a
primitive for a free-form component to make a gate pass is forbidden.

## 4. Evaluation and status

Each component becomes a Work 138 `step_file` candidate with its declared
material, boundary and load case, and its built mass as the declared mass. It
carries back exactly one Work 138 status. Components with `unresolved_*` are
reported with their causes and counted; they never disappear. Any
`unsupported_representation` component makes the candidate
`incomplete_composition`.

## 5. Matched comparison

The declaration must contain one `primitive_baseline` and one
`freeform_variant` that differ in exactly one component, and the changed
component in the variant must be the free-form one. Both candidates are built,
gated and evaluated under the same materials, mesh ladder, convergence limits,
budgets and load cases.

The matched report states candidate masses, the mass difference, and the status
and utilization of the substituted component on both sides. It also states what
the pair cannot establish: one substitution under one declared load case is
evidence of composability and evaluability, not of superiority.

## 6. Claim boundary

`passed_freeform_vehicle_composition` means the declared candidates were built,
packaged and evaluated. The summary carries `discovery_claim`,
`promotion_allowed`, `race_time_claim` and `physical_validation` as false, and
a control asserts that. Materials remain synthetic geometry-only values.

## 7. Mandatory controls

`component_outside_envelope`, `components_intersect`,
`missing_required_function_tag`, `corpus_hash_mismatch`,
`unadmitted_corpus_member`, `declared_mass_contradiction`, `no_discovery_claim`
and `exact_replay`. All eight must be rejected, and a clean replay must
reproduce the result SHA-256 exactly. The manifest hash covers geometry
identity only, so the same candidate built into two different output roots
hashes identically.
