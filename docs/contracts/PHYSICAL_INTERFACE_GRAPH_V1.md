# Physical Interface Graph V1

Thai companion: `PHYSICAL_INTERFACE_GRAPH_V1.th.md`

Status: Implemented by Work 112 for a bounded semantic corpus.

## Scope and dependency

This contract binds typed physical terminals to exact Work 108 material/void regions while preserving owner grouping, frames, surface names, roles, domains, variables, SI units, allowed motion, direction, constitutive-law references and parallel-edge multiplicity. It pins Work 108 commit `9e5249d343389a702d229a2cc090c71a12f13a4b` and the English spatial contract SHA-256.

The corpus covers mechanical force (`N`), heat flow (`W`) and angular velocity (`rad_s`). A binding is semantic declared evidence, not measured CAD contact. This descriptor is not sole proof of a mechanism, contact response, solver field, vehicle feasibility or physical validity.

## Compatibility and conservation

Each terminal has an orthonormal origin/normal/reference frame in metres and a non-empty named mating surface. Connected terminals must have the same domain, variable and unit; their origins must differ by at most `1e-6 m` and normal dot product must be at most `-0.999`. Directed edges must agree with source/sink roles. Rigid/moving conflicts fail unless a free terminal explicitly permits the relation. Each edge exchange pair must sum within `1e-12` in its registered unit.

The graph retains typed multiedges. Connectivity is evaluated without joining disconnected components. Missing regions/surfaces, incompatible units/domains, role-direction conflicts, invalid frames, unsupported laws/motion and conservation failures are observable rejections.

## Identity and geometry revision

Exact canonical identity enumerates terminal permutations only up to eight terminals. It removes terminal, edge and owner names but preserves the owner partition and every physical attribute and edge. Oversize graphs return `unresolved`; they never fall back to identifier-derived identity. Identifier-only rename must preserve identity, while source/sink reversal, parallel-edge deletion and owner regrouping remain distinct.

Split/merge transfer requires exactly one target claiming the original surface. A unique target rewrites the binding and invalidates dependent evidence for recomputation. Missing or multiple matches retain the old binding and emit an ambiguity invalidation event. Exact replay requires the same result SHA-256.
