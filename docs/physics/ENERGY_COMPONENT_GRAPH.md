# Typed Energy Component Graph

Status: Implemented for Work 012

Thai companion: `ENERGY_COMPONENT_GRAPH.th.md`

## Purpose and claim boundary

Work 012 defines and compiles the directed interfaces of an energy/powertrain
topology before any simulation is allowed to use it. A valid reference chain is:

```text
battery -> motor -> gearbox -> rear_tyre -> road
```

Compilation proves only that component roles, port directions, carriers,
connectivity, and directed acyclic order satisfy this interface contract. It
does not calculate operating power, joules, efficiency, depletion, heat, or
conservation and is not physical validation.

## SI and type contract

Every port declares:

- a unique component-local `port_id`;
- direction `input` or `output`;
- one carrier: `chemical`, `electrical`, `mechanical_rotational`,
  `mechanical_translational`, or `thermal`;
- finite positive `maximum_power_w` in watts.

A connection carries positive directed power from one output to one input. Its
carrier must match on both ends. Compiled connection capacity is:

```text
maximum_connection_power_w = min(source_port_capacity, target_port_capacity)
```

This is an interface ceiling, not an operating point.

## Component roles

| Role | Required port semantics |
|---|---|
| `source` | Output ports only |
| `converter` | At least one input and one output; may change carrier |
| `transmission` | Input and output; all ports `mechanical_rotational` |
| `tyre` | `mechanical_rotational` input and `mechanical_translational` output |
| `sink` | Input ports only |

Factories construct the baseline source, converter, transmission, tyre, and
sink roles. Generic components remain subject to the same role validation.

## Fail-closed graph rules

Work 012 rejects:

- unsupported or incompatible carriers;
- an input used as a source or output used as a target;
- missing endpoints, blank/duplicate identities, and self-loops;
- more than one source connection into an input;
- implicit output fan-out;
- any required unconnected port;
- directed cycles;
- invalid or non-finite capacities.

All ports are required and one-to-one. Output fan-out is not silently treated as
power duplication. A future splitter must explicitly allocate one input among
multiple outputs and be audited for conservation.

## Deterministic compilation

The compiler uses lexical tie-breaking in Kahn topological sorting. Compiled
connections use lexical endpoint ordering. Permuting the input component and
connection tuples therefore produces exactly equal compiled metadata.

The reference chain has these connection ceilings:

| Connection | Carrier | Maximum power |
|---|---|---:|
| `c1` battery → motor | electrical | `480000 W` |
| `c2` motor → gearbox | mechanical rotational | `440000 W` |
| `c3` gearbox → rear tyre | mechanical rotational | `410000 W` |
| `c4` rear tyre → road | mechanical translational | `390000 W` |

Run:

```powershell
python scripts/validate_energy_graph.py
python -m unittest tests.test_energy_graph -v
```

## Limitations and next work

- Capacity compatibility does not assign actual power.
- No efficiency, loss port, storage state, energy integration, or residual is
  present in Work 012.
- The graph is acyclic and one-to-one; regenerative loops, splitters, mergers,
  and multiple shafts require explicit later semantics.
- Work 013 will independently audit declared per-step energy transfers and must
  invalidate hidden or double-counted energy rather than assuming a compiled
  topology conserves energy.
