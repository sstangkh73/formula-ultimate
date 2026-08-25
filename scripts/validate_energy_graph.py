"""Validate Work 012 typed energy-graph compilation."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics.energy_graph import (  # noqa: E402
    EnergyConnection,
    EnergyGraph,
    EnergyGraphInputError,
    compile_energy_graph,
    converter_component,
    sink_component,
    source_component,
    transmission_component,
    tyre_component,
)


def reference_graph(reverse: bool = False) -> EnergyGraph:
    components = [
        source_component("battery", carrier="electrical", maximum_power_w=500_000.0),
        converter_component(
            "motor",
            input_carrier="electrical",
            output_carrier="mechanical_rotational",
            maximum_input_power_w=480_000.0,
            maximum_output_power_w=450_000.0,
        ),
        transmission_component(
            "gearbox", maximum_input_power_w=440_000.0, maximum_output_power_w=420_000.0
        ),
        tyre_component(
            "rear_tyre", maximum_input_power_w=410_000.0, maximum_output_power_w=400_000.0
        ),
        sink_component("road", carrier="mechanical_translational", maximum_power_w=390_000.0),
    ]
    connections = [
        EnergyConnection("c1", "battery", "power_out", "motor", "power_in"),
        EnergyConnection("c2", "motor", "power_out", "gearbox", "shaft_in"),
        EnergyConnection("c3", "gearbox", "shaft_out", "rear_tyre", "shaft_in"),
        EnergyConnection("c4", "rear_tyre", "road_power_out", "road", "power_in"),
    ]
    if reverse:
        components.reverse()
        connections.reverse()
    return EnergyGraph("1.0", "reference-powertrain", tuple(components), tuple(connections))


def main() -> int:
    compiled = compile_energy_graph(reference_graph())
    replay = compile_energy_graph(reference_graph(reverse=True))
    if compiled != replay:
        raise RuntimeError("input permutation changed compiled graph")

    mismatch_rejected = False
    try:
        compile_energy_graph(
            EnergyGraph(
                "1.0",
                "mismatch",
                (
                    source_component("fuel", carrier="chemical", maximum_power_w=10.0),
                    sink_component("shaft", carrier="mechanical_rotational", maximum_power_w=10.0),
                ),
                (EnergyConnection("bad", "fuel", "power_out", "shaft", "power_in"),),
            )
        )
    except EnergyGraphInputError:
        mismatch_rejected = True
    if not mismatch_rejected:
        raise RuntimeError("carrier mismatch was not rejected")

    print(
        json.dumps(
            {
                "schema_version": compiled.schema_version,
                "graph_id": compiled.graph_id,
                "component_order": compiled.component_order,
                "connections": [
                    {
                        "connection_id": item.connection_id,
                        "carrier": item.carrier,
                        "maximum_power_w": item.maximum_power_w,
                    }
                    for item in compiled.connections
                ],
                "permutation_replay_equal": compiled == replay,
                "carrier_mismatch_rejected": mismatch_rejected,
                "claim_boundary": "topology compiled; no energy conservation claim",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
