from __future__ import annotations

import math
import unittest

from formula_ultimate.physics.energy_graph import (
    EnergyComponent,
    EnergyConnection,
    EnergyGraph,
    EnergyGraphInputError,
    EnergyPort,
    compile_energy_graph,
    converter_component,
    sink_component,
    source_component,
    transmission_component,
    tyre_component,
)


def valid_components():
    return (
        source_component("battery", carrier="electrical", maximum_power_w=500_000.0),
        converter_component(
            "motor",
            input_carrier="electrical",
            output_carrier="mechanical_rotational",
            maximum_input_power_w=480_000.0,
            maximum_output_power_w=450_000.0,
        ),
        transmission_component(
            "gearbox",
            maximum_input_power_w=440_000.0,
            maximum_output_power_w=420_000.0,
        ),
        tyre_component(
            "rear_tyre",
            maximum_input_power_w=410_000.0,
            maximum_output_power_w=400_000.0,
        ),
        sink_component(
            "road", carrier="mechanical_translational", maximum_power_w=390_000.0
        ),
    )


def valid_connections():
    return (
        EnergyConnection("c1", "battery", "power_out", "motor", "power_in"),
        EnergyConnection("c2", "motor", "power_out", "gearbox", "shaft_in"),
        EnergyConnection("c3", "gearbox", "shaft_out", "rear_tyre", "shaft_in"),
        EnergyConnection(
            "c4", "rear_tyre", "road_power_out", "road", "power_in"
        ),
    )


def graph(components=None, connections=None):
    return EnergyGraph(
        schema_version="1.0",
        graph_id="reference-powertrain",
        components=tuple(components if components is not None else valid_components()),
        connections=tuple(
            connections if connections is not None else valid_connections()
        ),
    )


class EnergyGraphTests(unittest.TestCase):
    def test_valid_chain_compiles_in_topological_order(self) -> None:
        compiled = compile_energy_graph(graph())
        self.assertEqual(
            ("battery", "motor", "gearbox", "rear_tyre", "road"),
            compiled.component_order,
        )
        capacities = {item.connection_id: item.maximum_power_w for item in compiled.connections}
        self.assertEqual(
            {"c1": 480_000.0, "c2": 440_000.0, "c3": 410_000.0, "c4": 390_000.0},
            capacities,
        )

    def test_input_permutation_compiles_identically(self) -> None:
        forward = compile_energy_graph(graph())
        reverse = compile_energy_graph(
            graph(
                components=reversed(valid_components()),
                connections=reversed(valid_connections()),
            )
        )
        self.assertEqual(forward, reverse)

    def test_carrier_mismatch_is_rejected(self) -> None:
        components = list(valid_components())
        components[0] = source_component(
            "battery", carrier="chemical", maximum_power_w=500_000.0
        )
        with self.assertRaisesRegex(EnergyGraphInputError, "carrier mismatch"):
            compile_energy_graph(graph(components=components))

    def test_wrong_port_directions_are_rejected(self) -> None:
        bad = list(valid_connections())
        bad[0] = EnergyConnection(
            "c1", "motor", "power_in", "battery", "power_out"
        )
        with self.assertRaisesRegex(EnergyGraphInputError, "source is not an output"):
            compile_energy_graph(graph(connections=bad))

    def test_missing_endpoint_is_rejected(self) -> None:
        bad = list(valid_connections())
        bad[0] = EnergyConnection("c1", "missing", "power_out", "motor", "power_in")
        with self.assertRaisesRegex(EnergyGraphInputError, "missing source port"):
            compile_energy_graph(graph(connections=bad))

    def test_implicit_fanout_is_rejected(self) -> None:
        components = (
            source_component("source", carrier="electrical", maximum_power_w=10.0),
            sink_component("sink_a", carrier="electrical", maximum_power_w=10.0),
            sink_component("sink_b", carrier="electrical", maximum_power_w=10.0),
        )
        connections = (
            EnergyConnection("a", "source", "power_out", "sink_a", "power_in"),
            EnergyConnection("b", "source", "power_out", "sink_b", "power_in"),
        )
        with self.assertRaisesRegex(EnergyGraphInputError, "implicit fan-out"):
            compile_energy_graph(graph(components, connections))

    def test_multiple_sources_into_one_input_are_rejected(self) -> None:
        components = (
            source_component("source_a", carrier="electrical", maximum_power_w=10.0),
            source_component("source_b", carrier="electrical", maximum_power_w=10.0),
            sink_component("sink", carrier="electrical", maximum_power_w=10.0),
        )
        connections = (
            EnergyConnection("a", "source_a", "power_out", "sink", "power_in"),
            EnergyConnection("b", "source_b", "power_out", "sink", "power_in"),
        )
        with self.assertRaisesRegex(EnergyGraphInputError, "multiple sources"):
            compile_energy_graph(graph(components, connections))

    def test_unconnected_required_port_is_rejected(self) -> None:
        with self.assertRaisesRegex(EnergyGraphInputError, "unconnected"):
            compile_energy_graph(graph(connections=valid_connections()[:-1]))

    def test_self_loop_and_cycle_are_rejected(self) -> None:
        component_a = converter_component(
            "a",
            input_carrier="electrical",
            output_carrier="electrical",
            maximum_input_power_w=10.0,
            maximum_output_power_w=10.0,
        )
        component_b = converter_component(
            "b",
            input_carrier="electrical",
            output_carrier="electrical",
            maximum_input_power_w=10.0,
            maximum_output_power_w=10.0,
        )
        with self.assertRaisesRegex(EnergyGraphInputError, "self-loop"):
            compile_energy_graph(
                graph(
                    (component_a,),
                    (EnergyConnection("self", "a", "power_out", "a", "power_in"),),
                )
            )
        with self.assertRaisesRegex(EnergyGraphInputError, "cycle"):
            compile_energy_graph(
                graph(
                    (component_a, component_b),
                    (
                        EnergyConnection("ab", "a", "power_out", "b", "power_in"),
                        EnergyConnection("ba", "b", "power_out", "a", "power_in"),
                    ),
                )
            )

    def test_duplicate_identities_are_rejected(self) -> None:
        duplicate_components = valid_components() + (valid_components()[0],)
        with self.assertRaisesRegex(EnergyGraphInputError, "duplicate component_id"):
            compile_energy_graph(graph(components=duplicate_components))
        duplicate_connections = valid_connections() + (valid_connections()[0],)
        with self.assertRaisesRegex(EnergyGraphInputError, "duplicate connection_id"):
            compile_energy_graph(graph(connections=duplicate_connections))
        with self.assertRaisesRegex(EnergyGraphInputError, "duplicate port_id"):
            EnergyComponent(
                "bad",
                "converter",
                (
                    EnergyPort("p", "input", "electrical", 1.0),
                    EnergyPort("p", "output", "electrical", 1.0),
                ),
            )

    def test_invalid_contract_values_are_rejected(self) -> None:
        invalid = (
            lambda: EnergyPort("p", "sideways", "electrical", 1.0),
            lambda: EnergyPort("p", "input", "magic", 1.0),
            lambda: EnergyPort("p", "input", "electrical", 0.0),
            lambda: EnergyPort("p", "input", "electrical", -1.0),
            lambda: EnergyPort("p", "input", "electrical", math.inf),
            lambda: EnergyComponent("x", "unknown", (EnergyPort("p", "input", "thermal", 1.0),)),
            lambda: EnergyGraph("2.0", "g", valid_components(), valid_connections()),
        )
        for constructor in invalid:
            with self.subTest(constructor=constructor):
                with self.assertRaises(EnergyGraphInputError):
                    constructor()

    def test_role_port_semantics_are_enforced(self) -> None:
        invalid = (
            lambda: EnergyComponent(
                "source", "source", (EnergyPort("p", "input", "electrical", 1.0),)
            ),
            lambda: EnergyComponent(
                "sink", "sink", (EnergyPort("p", "output", "thermal", 1.0),)
            ),
            lambda: EnergyComponent(
                "converter",
                "converter",
                (EnergyPort("p", "input", "electrical", 1.0),),
            ),
            lambda: EnergyComponent(
                "transmission",
                "transmission",
                (
                    EnergyPort("in", "input", "electrical", 1.0),
                    EnergyPort("out", "output", "electrical", 1.0),
                ),
            ),
            lambda: EnergyComponent(
                "tyre",
                "tyre",
                (
                    EnergyPort("in", "input", "mechanical_translational", 1.0),
                    EnergyPort("out", "output", "mechanical_rotational", 1.0),
                ),
            ),
        )
        for constructor in invalid:
            with self.subTest(constructor=constructor):
                with self.assertRaises(EnergyGraphInputError):
                    constructor()


if __name__ == "__main__":
    unittest.main()
