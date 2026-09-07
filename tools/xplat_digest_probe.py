"""Locate where a run's digest starts to differ between platforms.

Run this on two platforms and diff the output. Every number is printed as a
float hex literal, so a one-ULP difference is visible rather than hidden by
decimal rounding.

    python tools/xplat_digest_probe.py > probe-<platform>.txt

The output is ordered from the most primitive layer upward: libm probes, then
the loaded configuration, then the simulation state after a growing number of
steps. The first line that differs names the layer that is responsible.

This tool found the cross-platform difference recorded in EVIDENCE.md: the
wheel slip law used math.tanh, which the Windows and Linux C libraries round
differently. Keep it for the next time a digest fails to reproduce elsewhere.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()[:16]


def hx(value: float) -> str:
    return value.hex() if isinstance(value, float) else repr(value)


def flatten(value, prefix=""):
    """Yield (path, value) for every leaf under a nested dict/list structure."""
    if isinstance(value, dict):
        for key in sorted(value):
            yield from flatten(value[key], f"{prefix}.{key}" if prefix else str(key))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            yield from flatten(item, f"{prefix}[{index}]")
    else:
        yield prefix, value


def dump_state(label, state):
    for path, item in flatten(asdict(state)):
        if isinstance(item, float):
            print(f"{label} {path} {item.hex()}")


def section(title: str) -> None:
    print(f"\n===== {title} =====")


# --------------------------------------------------------------------------
# Layer 0: the platform itself
# --------------------------------------------------------------------------
section("platform")
print("python      :", sys.version.split()[0])
print("implementation:", platform.python_implementation())
print("system      :", platform.system(), platform.machine())
print("float_repr  :", sys.float_repr_style)
print("maxsize     :", sys.maxsize)
try:
    import numpy

    print("numpy       :", numpy.__version__)
except Exception as error:  # pragma: no cover - numpy may be absent
    print("numpy       : unavailable", error)


# --------------------------------------------------------------------------
# Layer 1: libm. These are the functions that are NOT correctly rounded by
# IEEE 754 and are therefore allowed to differ between platforms.
# --------------------------------------------------------------------------
section("libm")
ARGS = (0.1, 0.5, 1.0, 1.5, 2.0, 3.141592653589793, 0.017453292519943295,
        123.456, 1e-8, 0.9999999999999999)
for name in ("sin", "cos", "tan", "atan", "exp", "log", "sqrt", "expm1", "log1p"):
    fn = getattr(math, name)
    values = []
    for arg in ARGS:
        try:
            values.append(hx(fn(arg)))
        except ValueError:
            values.append("domain")
    print(f"{name:6}", " ".join(values))
print("atan2 ", " ".join(hx(math.atan2(a, 1.7)) for a in ARGS))
print("hypot ", " ".join(hx(math.hypot(a, 1.7)) for a in ARGS))
print("pow   ", " ".join(hx(a ** 1.7) for a in ARGS))
print("fsum  ", hx(math.fsum(ARGS)))


# --------------------------------------------------------------------------
# Layer 2: the configuration as parsed from disk
# --------------------------------------------------------------------------
section("config")
from tests.test_sprung_body_vertical_coupling import loaded as loaded_vertical  # noqa: E402

raw, architecture, vertical, powertrain = loaded_vertical()
print("raw_json         :", digest(raw))
print("architecture_json:", digest(architecture))
print("vertical_config  :", digest(asdict(vertical)))
print("powertrain_config:", digest(asdict(powertrain)))
print("sprung_mass_kg   :", hx(vertical.sprung_mass_kg))

linkage_path = ROOT / "config" / "vehicle" / "geometry_linkage_motion_ratio_v1.json"
linkage_raw = json.loads(linkage_path.read_text(encoding="utf-8"))
print("linkage_json     :", digest(linkage_raw))

from formula_ultimate.simulation.linkage_motion_ratio import (  # noqa: E402
    apply_linkage_motion_ratios,
    load_linkage_motion_ratio_config,
)

linkage_config = load_linkage_motion_ratio_config(linkage_raw, geometry_section="unit_ratio_control")
application = apply_linkage_motion_ratios(linkage_config, vertical)
print("linkage_applied  :", digest(asdict(application)))
for item in application.evidence:
    print(f"  ratio {item.contact_id:24}", hx(item.motion_ratio))


# --------------------------------------------------------------------------
# Layer 3: the simulation, step by step
# --------------------------------------------------------------------------
section("vertical coupling, step by step")
from formula_ultimate.simulation.sprung_body_vertical_coupling import (  # noqa: E402
    initial_sprung_body_vertical_state,
    step_sprung_body_vertical_coupling,
    conservation_accounted_energy_j,
    total_coupled_accounted_energy_j,
    total_powertrain_accounted_energy_j,
    run_sprung_body_vertical_coupling,
)

config = application.transformed_vertical
state = initial_sprung_body_vertical_state(config, powertrain)
print("initial_state    :", digest(asdict(state)))

zero_road = tuple(0.0 for _ in config.contacts)
initial_powertrain = total_powertrain_accounted_energy_j(powertrain, state.coupled.powertrain)
initial_coupled = total_coupled_accounted_energy_j(config.transient.coupled, powertrain, state.coupled)
initial_total = conservation_accounted_energy_j(config, powertrain, state, zero_road)
print("initial_powertrain_j:", hx(initial_powertrain))
print("initial_coupled_j   :", hx(initial_coupled))
print("initial_total_j     :", hx(initial_total))

dt = config.transient.coupled.time_step_s
MARKS = {1, 2, 3, 5, 10, 25, 50, 100, 250, 500, 1000}
walk = state
for index in range(1, 1001):
    walk, evidence = step_sprung_body_vertical_coupling(
        config, powertrain, walk,
        initial_powertrain_energy_j=initial_powertrain,
        initial_coupled_energy_j=initial_coupled,
        initial_total_energy_j=initial_total,
        road_profiles=(), time_step_s=dt,
    )
    if index in MARKS:
        print(f"step {index:5}  state={digest(asdict(walk))}  "
              f"heave={hx(evidence.body_heave_m)}  "
              f"resid={hx(evidence.maximum_abs_equation_residual)}")
    if index in (3, 4, 5, 6):
        dump_state(f"FIELD step{index}", walk)
    if walk.outcome == "DNF":
        print(f"step {index:5}  DNF {walk.dnf_reason}")
        break


# --------------------------------------------------------------------------
# Layer 4: the digests the failing tests actually assert on
# --------------------------------------------------------------------------
section("asserted digests")
result = run_sprung_body_vertical_coupling(
    application.transformed_vertical, powertrain, sample_stride=25
)
print("WORK073 result_sha256      :", result.result_sha256)
print("  recorded reference       : 2ca3d0da5e128b3bdb6462472b0f5fa9d60afaa4d948a688356b2d2cb9974b8d")
print("  executed_steps           :", result.executed_steps)
print("  maximum_abs_heave_m      :", hx(result.maximum_abs_heave_m))
print("  max_equation_residual    :", hx(result.maximum_abs_equation_residual))
print("  max_global_energy_resid  :", hx(result.maximum_abs_total_global_energy_residual_j))

try:
    from tests.test_integrated_lap_gate import loaded as loaded_gate

    raw_gate, controller_raw, _, gate_config, gate_linkage, corridors, gate_powertrain = loaded_gate()
    from formula_ultimate.simulation.closed_loop_corridor_controller import (
        load_closed_loop_controller_config,
        run_closed_loop_controller,
    )

    short = run_closed_loop_controller(
        load_closed_loop_controller_config(controller_raw),
        vertical, gate_powertrain,
        corridors[controller_raw["reference_corridor_id"]],
        sample_stride=25,
    )
    print("WORK074 result_sha256      :", short.result_sha256)
    print("  recorded reference       : ab4470e28004cc78f87288a4ab2a7828881514362d8dffbb7d5326cdff5a8c6d")
    print("WORK075 application_sha256 :", gate_linkage.application_sha256)
except Exception as error:  # pragma: no cover - shape of loaded() may differ
    print("lap gate probe skipped:", type(error).__name__, error)
