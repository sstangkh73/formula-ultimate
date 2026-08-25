from __future__ import annotations

from dataclasses import replace
import math
import unittest

from formula_ultimate.physics.energy_audit import (
    ComponentEnergyBalance,
    ConnectionEnergyTransfer,
    EnergyAuditInputError,
    EnergyAuditTolerance,
    audit_energy_conservation,
)
from formula_ultimate.physics.energy_graph import (
    EnergyConnection,
    EnergyGraph,
    compile_energy_graph,
    converter_component,
    sink_component,
    source_component,
)


def compiled_reference():
    return compile_energy_graph(
        EnergyGraph(
            "1.0",
            "audit-reference",
            (
                source_component("battery", carrier="electrical", maximum_power_w=1_000.0),
                converter_component(
                    "motor",
                    input_carrier="electrical",
                    output_carrier="mechanical_rotational",
                    maximum_input_power_w=1_000.0,
                    maximum_output_power_w=1_000.0,
                ),
                sink_component("road", carrier="mechanical_rotational", maximum_power_w=1_000.0),
            ),
            (
                EnergyConnection("c1", "battery", "power_out", "motor", "power_in"),
                EnergyConnection("c2", "motor", "power_out", "road", "power_in"),
            ),
        )
    )


def valid_balances():
    return (
        ComponentEnergyBalance("battery", 0.0, 100.0, 0.0, -100.0),
        ComponentEnergyBalance("motor", 100.0, 90.0, 10.0, 0.0),
        ComponentEnergyBalance("road", 90.0, 0.0, 0.0, 90.0),
    )


def valid_transfers():
    return (
        ConnectionEnergyTransfer("c1", "battery", "motor", 100.0),
        ConnectionEnergyTransfer("c2", "motor", "road", 90.0),
    )


class EnergyAuditTests(unittest.TestCase):
    def audit(self, balances=None, transfers=None, tolerance=EnergyAuditTolerance()):
        return audit_energy_conservation(
            graph=compiled_reference(),
            balances=tuple(balances if balances is not None else valid_balances()),
            transfers=tuple(transfers if transfers is not None else valid_transfers()),
            tolerance=tolerance,
        )

    def test_lossy_reference_chain_is_valid(self) -> None:
        result = self.audit()
        self.assertEqual("valid", result.status)
        self.assertEqual(0.0, result.total_balance_residual_j)
        self.assertFalse(result.violations)
        self.assertTrue(all(item.status == "valid" for item in result.component_audits))

    def test_lossless_source_to_sink_chain_is_valid(self) -> None:
        graph = compile_energy_graph(
            EnergyGraph(
                "1.0",
                "lossless",
                (
                    source_component("source", carrier="electrical", maximum_power_w=10.0),
                    sink_component("sink", carrier="electrical", maximum_power_w=10.0),
                ),
                (EnergyConnection("c", "source", "power_out", "sink", "power_in"),),
            )
        )
        result = audit_energy_conservation(
            graph=graph,
            balances=(
                ComponentEnergyBalance("source", 0.0, 5.0, 0.0, -5.0),
                ComponentEnergyBalance("sink", 5.0, 0.0, 0.0, 5.0),
            ),
            transfers=(ConnectionEnergyTransfer("c", "source", "sink", 5.0),),
        )
        self.assertEqual("valid", result.status)

    def test_hidden_energy_creation_is_invalid(self) -> None:
        balances = list(valid_balances())
        balances[1] = replace(balances[1], energy_out_j=95.0)
        balances[2] = replace(balances[2], energy_in_j=95.0, stored_energy_change_j=95.0)
        transfers = list(valid_transfers())
        transfers[1] = replace(transfers[1], energy_j=95.0)
        result = self.audit(balances, transfers)
        self.assertEqual("invalid", result.status)
        motor = next(item for item in result.component_audits if item.component_id == "motor")
        self.assertEqual(-5.0, motor.balance_residual_j)

    def test_double_counted_loss_is_invalid(self) -> None:
        balances = list(valid_balances())
        balances[1] = replace(balances[1], declared_loss_j=20.0)
        result = self.audit(balances)
        self.assertEqual("invalid", result.status)
        self.assertEqual(-10.0, result.total_balance_residual_j)

    def test_connection_endpoint_and_energy_mismatch_are_visible(self) -> None:
        transfers = list(valid_transfers())
        transfers[1] = replace(transfers[1], target_component_id="battery")
        result = self.audit(transfers=transfers)
        self.assertEqual("invalid", result.status)
        self.assertTrue(any("endpoint mismatch" in item for item in result.violations))
        road = next(item for item in result.component_audits if item.component_id == "road")
        self.assertEqual(90.0, road.input_interface_residual_j)

    def test_missing_extra_and_duplicate_evidence_are_invalid(self) -> None:
        cases = (
            self.audit(balances=valid_balances()[:-1]),
            self.audit(balances=valid_balances() + (ComponentEnergyBalance("extra", 0.0, 0.0, 0.0, 0.0),)),
            self.audit(transfers=valid_transfers()[:-1]),
            self.audit(transfers=valid_transfers() + (valid_transfers()[0],)),
        )
        self.assertTrue(all(result.status == "invalid" for result in cases))

    def test_scaled_tolerance_accepts_small_residual_and_exposes_it(self) -> None:
        balances = (
            ComponentEnergyBalance("battery", 0.0, 1_000_000.0, 0.0, -1_000_000.0),
            ComponentEnergyBalance("motor", 1_000_000.0, 900_000.0, 100_000.0000001, 0.0),
            ComponentEnergyBalance("road", 900_000.0, 0.0, 0.0, 900_000.0),
        )
        transfers = (
            ConnectionEnergyTransfer("c1", "battery", "motor", 1_000_000.0),
            ConnectionEnergyTransfer("c2", "motor", "road", 900_000.0),
        )
        result = self.audit(
            balances,
            transfers,
            EnergyAuditTolerance(absolute_j=0.0, relative=1.0e-12),
        )
        self.assertEqual("valid", result.status)
        self.assertNotEqual(0.0, result.total_balance_residual_j)

    def test_invalid_values_are_rejected(self) -> None:
        invalid = (
            lambda: ComponentEnergyBalance("x", -1.0, 0.0, 0.0, 0.0),
            lambda: ComponentEnergyBalance("x", 0.0, math.inf, 0.0, 0.0),
            lambda: ConnectionEnergyTransfer("c", "a", "b", -1.0),
            lambda: EnergyAuditTolerance(relative=-1.0),
            lambda: EnergyAuditTolerance(relative=0.01),
        )
        for constructor in invalid:
            with self.subTest(constructor=constructor):
                with self.assertRaises(EnergyAuditInputError):
                    constructor()

    def test_replay_is_deterministic(self) -> None:
        self.assertEqual(self.audit(), self.audit())


if __name__ == "__main__":
    unittest.main()
