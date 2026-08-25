"""Validate Work 013 independent conservation references."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics.energy_audit import (  # noqa: E402
    ComponentEnergyBalance,
    ConnectionEnergyTransfer,
    audit_energy_conservation,
)
from formula_ultimate.physics.energy_graph import (  # noqa: E402
    EnergyConnection,
    EnergyGraph,
    compile_energy_graph,
    converter_component,
    sink_component,
    source_component,
)


def graph():
    return compile_energy_graph(EnergyGraph("1.0", "audit-reference", (
        source_component("battery", carrier="electrical", maximum_power_w=1000.0),
        converter_component("motor", input_carrier="electrical", output_carrier="mechanical_rotational", maximum_input_power_w=1000.0, maximum_output_power_w=1000.0),
        sink_component("road", carrier="mechanical_rotational", maximum_power_w=1000.0),
    ), (
        EnergyConnection("c1", "battery", "power_out", "motor", "power_in"),
        EnergyConnection("c2", "motor", "power_out", "road", "power_in"),
    )))


def audit(motor_out: float, motor_loss: float):
    return audit_energy_conservation(graph=graph(), balances=(
        ComponentEnergyBalance("battery", 0.0, 100.0, 0.0, -100.0),
        ComponentEnergyBalance("motor", 100.0, motor_out, motor_loss, 0.0),
        ComponentEnergyBalance("road", motor_out, 0.0, 0.0, motor_out),
    ), transfers=(
        ConnectionEnergyTransfer("c1", "battery", "motor", 100.0),
        ConnectionEnergyTransfer("c2", "motor", "road", motor_out),
    ))


def main() -> int:
    valid = audit(90.0, 10.0)
    hidden = audit(95.0, 10.0)
    double_loss = audit(90.0, 20.0)
    if valid.status != "valid" or hidden.status != "invalid" or double_loss.status != "invalid":
        raise RuntimeError("energy audit reference status mismatch")
    print(json.dumps({
        "valid_lossy_chain": {"status": valid.status, "total_residual_j": valid.total_balance_residual_j},
        "hidden_energy_case": {"status": hidden.status, "total_residual_j": hidden.total_balance_residual_j, "violations": hidden.violations},
        "double_loss_case": {"status": double_loss.status, "total_residual_j": double_loss.total_balance_residual_j, "violations": double_loss.violations},
        "residuals_corrected": False,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
