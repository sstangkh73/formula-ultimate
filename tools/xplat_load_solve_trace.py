"""Trace the normal-load solve, which feeds the first quantity that diverges.

The libm call trace showed the first cross-platform difference appearing as an
*argument* to a tyre hypot call, meaning the divergence is produced by ordinary
arithmetic upstream of it. The tyre limits are proportional to the normal load,
so this script logs the whole normal-load solve — its Gram matrix, target,
baseline projection, correction, and resulting loads — as hex literals.

    python tools/xplat_load_solve_trace.py > loads-<platform>.txt
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics import lateral  # noqa: E402


def hx(value):
    return value.hex() if isinstance(value, float) else repr(value)


def seq(values):
    return "[" + ", ".join(hx(v) for v in values) + "]"


CALLS = 0
LIMIT = 6
_original_solve = lateral._solve_three_by_three
_original_loads = lateral.solve_normal_loads if hasattr(lateral, "solve_normal_loads") else None


def traced_solve(gram, rhs):
    global CALLS
    result = _original_solve(gram, rhs)
    if CALLS < LIMIT:
        print(f"solve#{CALLS} gram_row0 {seq(gram[0])}")
        print(f"solve#{CALLS} gram_row1 {seq(gram[1])}")
        print(f"solve#{CALLS} gram_row2 {seq(gram[2])}")
        print(f"solve#{CALLS} rhs       {seq(rhs)}")
        print(f"solve#{CALLS} correction {seq(result) if result else 'None'}")
    CALLS += 1
    return result


lateral._solve_three_by_three = traced_solve

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

print("python:", sys.version.split()[0], "platform:", sys.platform)

_, _, vertical, powertrain = loaded_vertical()
linkage_raw = json.loads(
    (ROOT / "config" / "vehicle" / "geometry_linkage_motion_ratio_v1.json").read_text(encoding="utf-8")
)
application = apply_linkage_motion_ratios(
    load_linkage_motion_ratio_config(linkage_raw, geometry_section="unit_ratio_control"), vertical
)
config = application.transformed_vertical

# Geometry that feeds the Gram matrix, before any stepping.
print("\n===== contact geometry =====")
for contact in config.contacts:
    print(f"contact {contact.contact_id}")

state = initial_sprung_body_vertical_state(config, powertrain)
zero_road = tuple(0.0 for _ in config.contacts)
initial_powertrain = total_powertrain_accounted_energy_j(powertrain, state.coupled.powertrain)
initial_coupled = total_coupled_accounted_energy_j(config.transient.coupled, powertrain, state.coupled)
initial_total = conservation_accounted_energy_j(config, powertrain, state, zero_road)

print("\n===== normal-load solves during step 1 =====")
state, evidence = step_sprung_body_vertical_coupling(
    config, powertrain, state,
    initial_powertrain_energy_j=initial_powertrain,
    initial_coupled_energy_j=initial_coupled,
    initial_total_energy_j=initial_total,
    road_profiles=(), time_step_s=config.transient.coupled.time_step_s,
)

print("\n===== step 1 contact evidence =====")
for item in evidence.contacts:
    print(f"{item.contact_id} normal={hx(item.actual_normal_load_n)} "
          f"suspension_end={hx(item.suspension_end_m)}")
for item in state.coupled.contacts if hasattr(state.coupled, "contacts") else ():
    print("coupled contact", item)
print("differential_speed_rad_s", hx(state.coupled.differential_speed_rad_s))
print("longitudinal_slip_heat_j", hx(state.coupled.longitudinal_slip_heat_j))
