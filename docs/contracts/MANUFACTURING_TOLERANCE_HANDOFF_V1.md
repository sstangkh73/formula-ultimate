# Manufacturing Tolerance Handoff V1

Thai companion: `MANUFACTURING_TOLERANCE_HANDOFF_V1.th.md`

Status: Implemented by Work 130 as a route, access and worst-case tolerance gate.

## Evidence boundary

Every Work 126 region must map exactly once to a candidate process route, stock/source assumption, tool access and inspection access. Assembly dependencies must form an executable acyclic order. Trapped internal cores, inaccessible required features and unknown assembly references fail closed.

Clearance is evaluated as nominal clearance minus both registered feature tolerances. Preload is evaluated as nominal preload minus registered preload tolerance. Nominal-only fit cannot establish readiness. A route is supported only by measured process-capability or qualified-supplier evidence; heuristic minimum-feature checks and supplier identity placeholders remain `unknown_missing_capability_evidence`, not globally impossible.

Manufacturing readiness additionally requires native manufacturing CAD, complete access and passing worst-case tolerances. Exact replay requires the same result SHA-256. This contract authorizes no purchasing, fabrication, supplier qualification, safety certification or physical validation.
