# Work 012 Result: Typed Energy and Powertrain Component Graph

Status: Completed

Thai companion: `2026-08-26_012_typed-energy-graph-result.th.md`

## Outcome

Work 012 is complete. The repository now has a fail-closed typed component graph
for source, converter, transmission, tyre, and sink power interfaces. The
reference chain compiles deterministically as:

```text
battery -> motor -> gearbox -> rear_tyre -> road
```

Reversing both component and connection input order produces exactly equal
compiled metadata. Carrier mismatch, direction mismatch, missing endpoint,
duplicate identity, unconnected required port, implicit fan-out, multiple input
sources, self-loop, role violation, and directed cycle are rejected.

This result validates topology/interface rules only. It makes no energy
conservation or physical-validation claim.

## Files changed

- `src/formula_ultimate/physics/energy_graph.py`: typed ports, components,
  connections, factories, deterministic compiler, and invalid-topology errors.
- `src/formula_ultimate/physics/__init__.py`: public energy-graph API exports.
- `tests/test_energy_graph.py`: 12 valid, permutation, type, role, connectivity,
  topology, capacity, and invalid-input tests.
- `scripts/validate_energy_graph.py`: valid-chain replay and mismatch rejection
  evidence.
- `docs/physics/ENERGY_COMPONENT_GRAPH.md` and `.th.md`: SI/type contract,
  fail-closed rules, deterministic order, boundary, and limitations.
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md` and `.th.md`: Work 012 status.
- this Work 012 plan/result pair in English and Thai.

## Decisions

1. Carrier vocabulary is closed to chemical, electrical, mechanical rotational,
   mechanical translational, and thermal.
2. Every port has direction, carrier, and finite positive capacity in watts.
3. Source roles contain outputs only; sinks inputs only; converters have both;
   transmissions remain rotational; tyres map rotational input to translational
   output.
4. All ports are required and one-to-one. Fan-out and multiple-source input fail
   instead of implying duplication or addition.
5. Connections require matching carriers and output-to-input direction.
6. Compiled connection capacity is the smaller endpoint capacity.
7. Lexical Kahn sorting makes component order independent of input tuple order;
   compiled connections use lexical endpoint ordering.

## Experiment review

- Independent variables: component roles/IDs, port types/directions/capacities,
  endpoints, and input permutation.
- Dependent variables: compile status/reason, component order, connection order,
  and capacity.
- Controls: fixed vocabulary and factories, lexical tie-break, required
  one-to-one ports, no randomness or repair.
- Supporting evidence: the five-component reference compiles identically under
  reverse input permutation, with connection ceilings `480000`, `440000`,
  `410000`, and `390000 W`.
- Contradicting/falsifying evidence: direct chemical-to-rotational connection,
  output fan-out, two sources into one input, disconnection, self-loop, and
  two-converter cycle all fail.
- Alternative explanation excluded: deterministic equality is structural
  dataclass equality, not only a visually similar print order.
- Missing evidence: instantaneous power, stored energy, losses, efficiency,
  depletion, regenerative flow, and conservation residuals.
- Confidence: high for topology/type compilation; none for conservation or
  physical performance until later laws are applied.

## Problems encountered

No material problem requiring a separate problem report was found. Internal
review identified that generic components also needed role-specific port checks;
those checks were added and covered by the planned invalid-contract tests before
validation.

## Validation evidence

All commands ran from `C:\Formula Ultimate` with fail-fast exit handling.

```powershell
python -m unittest tests.test_energy_graph -v
```

Exit status: `0`. Relevant output: `Ran 12 tests`; `OK`.

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`. Relevant output: `Ran 80 tests`; `OK`.

```powershell
python scripts/validate_energy_graph.py
```

Exit status: `0`. Relevant output:

```text
component_order: battery, motor, gearbox, rear_tyre, road
permutation_replay_equal: true
carrier_mismatch_rejected: true
claim_boundary: topology compiled; no energy conservation claim
```

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status: `0` for each command. The staged check is rerun after explicit
staging and before commit.

## Limitations and follow-up

- No operating power or energy is calculated.
- No branches, mergers, regenerative cycles, or dynamic controls are admitted.
- Capacity is an interface ceiling, not a predicted operating point.
- Work 013 will add an independent per-step conservation audit that invalidates
  hidden or double-counted energy.
