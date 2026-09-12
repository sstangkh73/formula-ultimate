"""Realized bounded rotary actuation-chain reference for Work 119."""
from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping

PROTOCOL_VERSION = "realized_actuation_chain_v1"


class ActuationChainViolation(ValueError):
    """Raised when a response is unsupported or outside its registered envelope."""


def canonical_sha256(value: Any) -> str:
    try:
        payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    except (TypeError, ValueError) as exc:
        raise ActuationChainViolation("state must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()


def cylinder_mass(member: Mapping[str, float]) -> float:
    return member["density_kg_m3"] * math.pi * member["diameter_m"] ** 2 * member["length_m"] / 4.0


def containment_mass(containment: Mapping[str, Any]) -> float:
    x, y, z = containment["outer_dimensions_m"]
    thickness = containment["wall_thickness_m"]
    if thickness <= 0 or min(x, y, z) <= 2 * thickness:
        raise ActuationChainViolation("containment geometry is invalid")
    volume = x * y * z - (x - 2 * thickness) * (y - 2 * thickness) * (z - 2 * thickness)
    return volume * containment["density_kg_m3"]


def torsional_stiffness(member: Mapping[str, float]) -> float:
    polar_moment = math.pi * member["diameter_m"] ** 4 / 32.0
    return member["shear_modulus_pa"] * polar_moment / member["length_m"]


def validate_protocol(raw: Mapping[str, Any]) -> dict:
    required = {"protocol_version", "units", "dependencies", "inputs", "ports", "envelope", "hardware", "loss_law", "map", "tolerances", "coverage", "experiment"}
    if set(raw) != required or raw.get("protocol_version") != PROTOCOL_VERSION:
        raise ActuationChainViolation("protocol schema or identity mismatch")
    if raw.get("units") != "SI_m_kg_s_K_N_Pa_W_J_rad":
        raise ActuationChainViolation("protocol units mismatch")
    if {item.get("work") for item in raw["dependencies"]} != {114, 115, 116}:
        raise ActuationChainViolation("Work 114, 115 and 116 dependencies are required")
    hardware = raw["hardware"]
    if set(hardware) != {"route_id", "ratio", "members", "supports", "containment", "coupler_mass_kg", "reaction_arm_m"}:
        raise ActuationChainViolation("hardware coverage is incomplete")
    if hardware["ratio"] <= 0 or len(hardware["members"]) != 2 or len(hardware["supports"]) < 2:
        raise ActuationChainViolation("hardware path or supports are incomplete")
    for member in hardware["members"]:
        keys = {"member_id", "diameter_m", "length_m", "density_kg_m3", "shear_modulus_pa"}
        if set(member) != keys or any(member[key] <= 0 for key in keys - {"member_id"}):
            raise ActuationChainViolation("transfer-member geometry or properties are invalid")
    if any(support.get("mass_kg", 0) <= 0 for support in hardware["supports"]):
        raise ActuationChainViolation("support geometry is missing")
    containment_mass(hardware["containment"])
    envelope = raw["envelope"]
    if envelope["maximum_abs_input_torque_n_m"] <= 0 or envelope["maximum_abs_input_speed_rad_s"] <= 0:
        raise ActuationChainViolation("port envelope is invalid")
    if not envelope["temperature_range_k"][0] < envelope["temperature_range_k"][1]:
        raise ActuationChainViolation("temperature range is invalid")
    if any(not values for values in raw["experiment"].values()):
        raise ActuationChainViolation("experiment registration is incomplete")
    return {
        "status": "passed",
        "hardware_mass_kg": hardware_mass(hardware),
        "protocol_sha256": canonical_sha256(raw),
    }


def hardware_mass(hardware: Mapping[str, Any]) -> float:
    return (
        sum(cylinder_mass(member) for member in hardware["members"])
        + sum(support["mass_kg"] for support in hardware["supports"])
        + containment_mass(hardware["containment"])
        + hardware["coupler_mass_kg"]
    )


def evaluate(
    raw: Mapping[str, Any],
    input_torque_n_m: float,
    input_speed_rad_s: float,
    temperature_k: float,
    *,
    connected: bool = True,
    output_locked: bool = False,
) -> dict:
    values = (input_torque_n_m, input_speed_rad_s, temperature_k)
    if any(not math.isfinite(value) for value in values):
        raise ActuationChainViolation("operating state must be finite")
    validation = validate_protocol(raw)
    if not connected:
        return {
            "state": "disconnected",
            "accepted_input_power_w": 0.0,
            "output_power_w": 0.0,
            "loss_power_w": 0.0,
            "output_torque_n_m": 0.0,
            "output_speed_rad_s": 0.0,
            "energy_residual_w": 0.0,
            "hardware_mass_kg": validation["hardware_mass_kg"],
        }
    envelope = raw["envelope"]
    if abs(input_speed_rad_s) > envelope["maximum_abs_input_speed_rad_s"]:
        raise ActuationChainViolation("input speed outside registered envelope")
    low_temperature, high_temperature = envelope["temperature_range_k"]
    if not low_temperature <= temperature_k <= high_temperature:
        raise ActuationChainViolation("temperature outside registered envelope")
    if input_torque_n_m * input_speed_rad_s < 0:
        raise ActuationChainViolation("unsupported generating quadrant")
    torque_limit = envelope["maximum_abs_input_torque_n_m"]
    accepted_torque = math.copysign(min(abs(input_torque_n_m), torque_limit), input_torque_n_m)
    saturated = abs(input_torque_n_m) > torque_limit
    input_power = accepted_torque * input_speed_rad_s
    ratio = raw["hardware"]["ratio"]
    output_speed = 0.0 if output_locked else input_speed_rad_s / ratio
    law = raw["loss_law"]
    if input_power == 0:
        modeled_loss = 0.0
    elif output_locked:
        modeled_loss = input_power
    else:
        modeled_loss = min(
            input_power,
            law["fractional_loss"] * input_power
            + law["fixed_loss_w"]
            + law["speed_loss_w_per_rad_s"] * abs(input_speed_rad_s)
            + law["torque_loss_w_per_n_m"] * abs(accepted_torque)
            + law["temperature_loss_w_per_k"] * abs(temperature_k - law["reference_temperature_k"]),
        )
    output_power = input_power - modeled_loss
    if output_locked:
        output_torque = accepted_torque * ratio
    elif output_speed == 0:
        output_torque = 0.0
    else:
        output_torque = output_power / output_speed
    members = raw["hardware"]["members"]
    input_stiffness = torsional_stiffness(members[0])
    output_stiffness = torsional_stiffness(members[1])
    input_twist = accepted_torque / input_stiffness
    output_twist = output_torque / output_stiffness
    input_stress = 16.0 * abs(accepted_torque) / (math.pi * members[0]["diameter_m"] ** 3)
    output_stress = 16.0 * abs(output_torque) / (math.pi * members[1]["diameter_m"] ** 3)
    radial_reaction = abs(output_torque) / raw["hardware"]["reaction_arm_m"]
    support_count = len(raw["hardware"]["supports"])
    return {
        "state": "locked_output" if output_locked else ("saturated" if saturated else "admitted"),
        "accepted_input_torque_n_m": accepted_torque,
        "input_speed_rad_s": input_speed_rad_s,
        "accepted_input_power_w": input_power,
        "output_torque_n_m": output_torque,
        "output_speed_rad_s": output_speed,
        "output_power_w": output_power,
        "loss_power_w": modeled_loss,
        "heat_rate_w": modeled_loss,
        "energy_residual_w": input_power - output_power - modeled_loss,
        "input_member_stiffness_n_m_rad": input_stiffness,
        "output_member_stiffness_n_m_rad": output_stiffness,
        "total_output_twist_rad": ratio * input_twist + output_twist,
        "input_member_stress_pa": input_stress,
        "output_member_stress_pa": output_stress,
        "radial_reaction_per_support_n": radial_reaction / support_count,
        "torque_reaction_per_support_n_m": -output_torque / support_count,
        "hardware_mass_kg": validation["hardware_mass_kg"],
        "hardware_sha256": canonical_sha256(raw["hardware"]),
    }
