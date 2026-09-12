"""Architecture-neutral bounded ground interaction references for Work 118."""
from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping, Sequence

PROTOCOL_VERSION = "ground_interaction_tasks_v1"


class GroundInteractionViolation(ValueError):
    """Raised when ground-interaction evidence is outside the registered scope."""


def canonical_sha256(value: Any) -> str:
    try:
        payload = json.dumps(
            value, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise GroundInteractionViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()


def validate_protocol(raw: Mapping[str, Any]) -> dict:
    required = {
        "protocol_version",
        "units",
        "dependencies",
        "inputs",
        "surface",
        "route",
        "body",
        "contacts",
        "commands",
        "time_steps_s",
        "tolerances",
        "coverage",
        "experiment",
    }
    if set(raw) != required or raw.get("protocol_version") != PROTOCOL_VERSION:
        raise GroundInteractionViolation("protocol schema or identity mismatch")
    if raw.get("units") != "SI_m_kg_s_N_J_W_Pa":
        raise GroundInteractionViolation("protocol units mismatch")
    if {item.get("work") for item in raw["dependencies"]} != {114, 116}:
        raise GroundInteractionViolation("Work 114 and Work 116 dependencies are required")
    for dependency in raw["dependencies"]:
        if set(dependency) != {"work", "commit", "contract_path", "contract_sha256"}:
            raise GroundInteractionViolation("dependency schema mismatch")
        if len(dependency["commit"]) != 40 or len(dependency["contract_sha256"]) != 64:
            raise GroundInteractionViolation("dependency identity is invalid")
    surface = raw["surface"]
    if set(surface) != {
        "surface_id",
        "provenance",
        "applicability",
        "friction_coefficient",
        "friction_range",
        "normal_load_range_n",
        "speed_range_m_s",
    }:
        raise GroundInteractionViolation("surface record is incomplete")
    if surface["provenance"] != "synthetic" or surface["applicability"] != "rigid_dry_coulomb":
        raise GroundInteractionViolation("unsupported surface applicability")
    mu = surface["friction_coefficient"]
    if not surface["friction_range"][0] <= mu <= surface["friction_range"][1]:
        raise GroundInteractionViolation("friction coefficient outside registered range")
    if not raw["time_steps_s"] or any(step <= 0 for step in raw["time_steps_s"]):
        raise GroundInteractionViolation("time-step registration is invalid")
    if sorted(raw["time_steps_s"], reverse=True) != raw["time_steps_s"]:
        raise GroundInteractionViolation("time steps must be coarse-to-fine")
    if raw["body"]["mass_kg"] <= 0 or raw["body"]["yaw_inertia_kg_m2"] <= 0:
        raise GroundInteractionViolation("body properties must be positive")
    if len({contact["port_id"] for contact in raw["contacts"]}) != len(raw["contacts"]):
        raise GroundInteractionViolation("contact-port identity is ambiguous")
    if any(not values for values in raw["experiment"].values()):
        raise GroundInteractionViolation("experiment registration is incomplete")
    unresolved = {key for key, value in raw["coverage"].items() if value.startswith("unresolved")}
    if not {"tire", "soft_soil", "non_tire_adapter"}.issubset(unresolved):
        raise GroundInteractionViolation("unsupported domain was silently promoted")
    return {
        "status": "passed",
        "contact_count": len(raw["contacts"]),
        "time_step_count": len(raw["time_steps_s"]),
        "protocol_sha256": canonical_sha256(raw),
    }


def contact_force(
    normal_load_n: float,
    requested_longitudinal_n: float,
    requested_lateral_n: float,
    friction_coefficient: float,
    *,
    interaction_enabled: bool = True,
    actuation_connected: bool = True,
) -> dict:
    values = (
        normal_load_n,
        requested_longitudinal_n,
        requested_lateral_n,
        friction_coefficient,
    )
    if any(not math.isfinite(value) for value in values):
        raise GroundInteractionViolation("contact input must be finite")
    if friction_coefficient < 0:
        raise GroundInteractionViolation("friction coefficient must be non-negative")
    if not interaction_enabled:
        return {
            "longitudinal_force_n": 0.0,
            "lateral_force_n": 0.0,
            "capacity_n": 0.0,
            "saturated": False,
            "state": "no_physical_interaction",
        }
    if normal_load_n <= 0:
        return {
            "longitudinal_force_n": 0.0,
            "lateral_force_n": 0.0,
            "capacity_n": 0.0,
            "saturated": False,
            "state": "lift_off",
        }
    if not actuation_connected:
        return {
            "longitudinal_force_n": 0.0,
            "lateral_force_n": 0.0,
            "capacity_n": friction_coefficient * normal_load_n,
            "saturated": False,
            "state": "disconnected_actuation",
        }
    capacity = friction_coefficient * normal_load_n
    demand = math.hypot(requested_longitudinal_n, requested_lateral_n)
    scale = min(1.0, capacity / demand) if demand > 0 else 1.0
    return {
        "longitudinal_force_n": requested_longitudinal_n * scale,
        "lateral_force_n": requested_lateral_n * scale,
        "capacity_n": capacity,
        "saturated": demand > capacity,
        "state": "saturated" if demand > capacity else "admitted",
    }


def net_wrench(
    contacts: Sequence[Mapping[str, float]],
    requests: Mapping[str, Mapping[str, float]],
    friction_coefficient: float,
    *,
    interaction_enabled: bool = True,
    actuation_connected: bool = True,
) -> dict:
    results = []
    total_longitudinal = 0.0
    total_lateral = 0.0
    yaw_moment = 0.0
    for port in contacts:
        request = requests.get(port["port_id"], {})
        force = contact_force(
            port["normal_load_n"],
            request.get("longitudinal_force_n", 0.0),
            request.get("lateral_force_n", 0.0),
            friction_coefficient,
            interaction_enabled=interaction_enabled,
            actuation_connected=actuation_connected,
        )
        total_longitudinal += force["longitudinal_force_n"]
        total_lateral += force["lateral_force_n"]
        moment = (
            port["x_m"] * force["lateral_force_n"]
            - port["y_m"] * force["longitudinal_force_n"]
        )
        yaw_moment += moment
        results.append({"port_id": port["port_id"], "force": force, "yaw_moment_n_m": moment})
    return {
        "ports": results,
        "longitudinal_force_n": total_longitudinal,
        "lateral_force_n": total_lateral,
        "yaw_moment_n_m": yaw_moment,
    }


def simulate_stopping(
    mass_kg: float,
    initial_velocity_m_s: float,
    normal_load_n: float,
    friction_coefficient: float,
    dt_s: float,
    *,
    max_time_s: float,
    interaction_enabled: bool = True,
) -> dict:
    if mass_kg <= 0 or dt_s <= 0 or max_time_s <= 0:
        raise GroundInteractionViolation("stopping mass and time bounds must be positive")
    if normal_load_n < 0:
        raise GroundInteractionViolation("normal load must be non-negative")
    speed_sign = 1.0 if initial_velocity_m_s >= 0 else -1.0
    speed = abs(initial_velocity_m_s)
    capacity = contact_force(
        normal_load_n,
        -speed_sign * 1e300,
        0.0,
        friction_coefficient,
        interaction_enabled=interaction_enabled,
    )["capacity_n"]
    acceleration = capacity / mass_kg
    initial_energy = 0.5 * mass_kg * speed * speed
    distance = 0.0
    dissipated = 0.0
    elapsed = 0.0
    history = []
    while speed > 0 and elapsed < max_time_s and acceleration > 0:
        step = min(dt_s, max_time_s - elapsed, speed / acceleration)
        segment = speed * step - 0.5 * acceleration * step * step
        distance += speed_sign * segment
        dissipated += capacity * segment
        speed = max(0.0, speed - acceleration * step)
        elapsed += step
        history.append(
            {
                "time_s": elapsed,
                "position_m": distance,
                "velocity_m_s": speed_sign * speed,
                "dissipated_energy_j": dissipated,
                "dissipated_power_w": capacity * speed,
            }
        )
    final_energy = 0.5 * mass_kg * speed * speed
    residual = initial_energy - final_energy - dissipated
    return {
        "status": "stopped" if speed == 0 else "not_stopped_within_bound",
        "dt_s": dt_s,
        "stopping_time_s": elapsed,
        "stopping_distance_m": distance,
        "initial_energy_j": initial_energy,
        "final_energy_j": final_energy,
        "dissipated_energy_j": dissipated,
        "energy_residual_j": residual,
        "energy_residual_relative": abs(residual) / max(initial_energy, 1e-30),
        "braking_force_n": -speed_sign * capacity,
        "history": history,
    }


def analytic_stop(mass_kg: float, speed_m_s: float, force_n: float) -> dict:
    if mass_kg <= 0 or force_n <= 0:
        raise GroundInteractionViolation("analytic stop requires positive mass and force")
    speed = abs(speed_m_s)
    return {
        "stopping_time_s": mass_kg * speed / force_n,
        "stopping_distance_m": mass_kg * speed * speed / (2.0 * force_n),
        "dissipated_energy_j": 0.5 * mass_kg * speed * speed,
    }
