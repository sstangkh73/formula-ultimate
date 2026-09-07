"""Trace every libm call made while stepping the coupled model.

Each call is printed as `name(arg_hex, ...) -> result_hex`, so diffing the
output of two platforms names the exact call whose result differs, together
with the arguments that produced it.

    python tools/xplat_call_trace.py > trace-<platform>.txt
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

CALLS: list[str] = []
TRACING = False


def hx(value):
    if isinstance(value, float):
        return value.hex()
    if hasattr(value, "__next__"):
        # fsum takes a generator; its repr carries a memory address that is not
        # comparable across runs, so name it by shape instead.
        return "<gen>"
    return repr(value)


def wrap(name):
    original = getattr(math, name)

    def traced(*args):
        result = original(*args)
        if TRACING:
            CALLS.append(f"{name}({', '.join(hx(a) for a in args)}) -> {hx(result)}")
        return result

    return traced


TRACKED = ("sin", "cos", "tan", "atan", "atan2", "exp", "log", "log1p", "expm1",
           "sqrt", "hypot", "pow", "fsum", "ceil", "floor", "fmod", "copysign")
for _name in TRACKED:
    if hasattr(math, _name):
        setattr(math, _name, wrap(_name))

# `**` on floats also goes through the platform's pow(); trace it separately by
# wrapping the operands the model uses most.
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
import json  # noqa: E402

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
initial_powertrain = total_powertrain_accounted_energy_j(powertrain, state.coupled.powertrain)
initial_coupled = total_coupled_accounted_energy_j(config.transient.coupled, powertrain, state.coupled)
initial_total = conservation_accounted_energy_j(config, powertrain, state, zero_road)
dt = config.transient.coupled.time_step_s

print("python:", sys.version.split()[0], "platform:", sys.platform)

for index in range(1, 5):
    CALLS.clear()
    TRACING = True
    state, evidence = step_sprung_body_vertical_coupling(
        config, powertrain, state,
        initial_powertrain_energy_j=initial_powertrain,
        initial_coupled_energy_j=initial_coupled,
        initial_total_energy_j=initial_total,
        road_profiles=(), time_step_s=dt,
    )
    TRACING = False
    print(f"\n===== step {index}: {len(CALLS)} libm calls =====")
    for line in CALLS:
        print(f"s{index} {line}")
    print(f"s{index} RESULT differential_speed_rad_s {hx(state.coupled.differential_speed_rad_s)}")
    print(f"s{index} RESULT longitudinal_slip_heat_j {hx(state.coupled.longitudinal_slip_heat_j)}")
