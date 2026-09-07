"""Confirm that math.tanh is the origin of the cross-platform difference.

`ground_force_request` computes the requested longitudinal force as

    capacity * math.tanh(longitudinal_stiffness * slip_ratio / capacity)

`tanh` is not required by IEEE 754 to be correctly rounded, so two C libraries
may return results that differ in the last place. This script prints tanh at the
arguments the model actually uses, plus a sweep, as hex literals.

    python tools/xplat_tanh_check.py > tanh-<platform>.txt
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

print("python:", sys.version.split()[0], "platform:", sys.platform)

print("\n===== tanh sweep =====")
SWEEP = [i / 64.0 for i in range(1, 65)] + [1.5, 2.0, 3.0, 5.0, 7.5, 10.0, 20.0]
for value in SWEEP:
    print(f"tanh({value.hex()}) = {math.tanh(value).hex()}")

print("\n===== tanh as the model calls it =====")
# Record every tanh call made during the first simulation step.
CALLS: list[tuple[float, float]] = []
_original_tanh = math.tanh


def traced(value):
    result = _original_tanh(value)
    CALLS.append((value, result))
    return result


math.tanh = traced

import json  # noqa: E402
from tests.test_sprung_body_vertical_coupling import loaded as loaded_vertical  # noqa: E402
from formula_ultimate.simulation.linkage_motion_ratio import (  # noqa: E402
    apply_linkage_motion_ratios,
    load_linkage_motion_ratio_config,
)
from formula_ultimate.simulation.sprung_body_vertical_coupling import (  # noqa: E402
    initial_sprung_body_vertical_state,
    step_sprung_body_vertical_coupling,
    conservation_accounted_energy_j,
    total_coupled_accounted_energy_j,
    total_powertrain_accounted_energy_j,
)

_, _, vertical, powertrain = loaded_vertical()
linkage_raw = json.loads(
    (ROOT / "config" / "vehicle" / "geometry_linkage_motion_ratio_v1.json").read_text(encoding="utf-8")
)
application = apply_linkage_motion_ratios(
    load_linkage_motion_ratio_config(linkage_raw, geometry_section="unit_ratio_control"), vertical
)
config = application.transformed_vertical
state = initial_sprung_body_vertical_state(config, powertrain)
zero_road = tuple(0.0 for _ in config.contacts)

state, _ = step_sprung_body_vertical_coupling(
    config, powertrain, state,
    initial_powertrain_energy_j=total_powertrain_accounted_energy_j(powertrain, state.coupled.powertrain),
    initial_coupled_energy_j=total_coupled_accounted_energy_j(config.transient.coupled, powertrain, state.coupled),
    initial_total_energy_j=conservation_accounted_energy_j(config, powertrain, state, zero_road),
    road_profiles=(), time_step_s=config.transient.coupled.time_step_s,
)

print(f"tanh calls in step 1: {len(CALLS)}")
for index, (argument, result) in enumerate(CALLS[:40]):
    print(f"call{index:03d} tanh({argument.hex()}) = {result.hex()}")
