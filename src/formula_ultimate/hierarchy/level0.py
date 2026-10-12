"""Level-0 race coupling for a generated (goal v2) vehicle package.

The vehicle enters the existing ``physics/race.py`` kernel (``race-level0-v1``)
as a lumped point mass equal to the manifest root ``mass_kg`` and a drag area
bounded by the leaf-mesh frontal (y-z) box. Circuit, tractive force, energy
budget and control settings come from a versioned JSON config. All values are
SI. This is outcome evidence only: no lap time, aerodynamics or physical
validation is claimed.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping

import numpy as np

from formula_ultimate.physics.circuit import CircuitProfile, load_circuit_catalog
from formula_ultimate.physics.longitudinal import VehicleParameters
from formula_ultimate.physics.race import RaceControl, RaceVehicle, run_full_race
from formula_ultimate.physics.thermal import ThermalParameters

from .leaf_geometry import read_binary_stl


RACE_KERNEL_ID = "race-level0-v1"
OUTPUT_FIELDS = (
    "manifest_sha256",
    "mass_kg",
    "drag_area_m2",
    "outcome",
    "race_time_s",
    "consumed_energy_j",
    "terminal_energy_boundary_residual_j",
    "circuit_id",
    "race_kernel",
)


class Level0InputError(ValueError):
    """Raised when a manifest or config cannot be evaluated."""


def load_config(path: str | Path) -> dict[str, Any]:
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    if config.get("race_kernel") != RACE_KERNEL_ID:
        raise Level0InputError(f"config race_kernel must be {RACE_KERNEL_ID!r}")
    return config


def root_mass_kg(manifest: Mapping[str, Any]) -> float:
    nodes = {node["id"]: node for node in manifest["nodes"]}
    if manifest.get("root") not in nodes:
        raise Level0InputError("manifest root is not a node")
    mass = float(nodes[manifest["root"]]["mass_kg"])
    if not math.isfinite(mass) or mass <= 0.0:
        raise Level0InputError(f"root mass_kg must be finite and > 0; received {mass!r}")
    return mass


def leaf_points(manifest: Mapping[str, Any], package_dir: str | Path) -> np.ndarray:
    """All leaf mesh vertices in metres; mesh paths must stay inside the package."""

    base = Path(package_dir).resolve()
    chunks = []
    for node in manifest["nodes"]:
        if node.get("kind") != "part":
            continue
        path = (base / node["mesh"]).resolve()
        if base not in path.parents:
            raise Level0InputError(f"{node['id']}: mesh path escapes the package")
        chunks.append(read_binary_stl(path).reshape(-1, 3))
    if not chunks:
        raise Level0InputError("manifest has no part leaves")
    return np.concatenate(chunks)


def frontal_extent_m(points: np.ndarray) -> tuple[float, float]:
    """Return the (y, z) extent of the points, the frontal box for travel along x."""

    extent = points.max(axis=0) - points.min(axis=0)
    return float(extent[1]), float(extent[2])


def drag_area_m2(points: np.ndarray, config: Mapping[str, Any]) -> float:
    coefficient = float(config["drag"]["frontal_box_coefficient"])
    if not 0.0 < coefficient <= 1.5:
        raise Level0InputError("frontal_box_coefficient must be in (0, 1.5]")
    extent_y, extent_z = frontal_extent_m(points)
    area = coefficient * extent_y * extent_z
    if not math.isfinite(area) or area <= 0.0:
        raise Level0InputError(f"frontal box area must be finite and > 0; received {area!r}")
    return area


def select_circuit(config: Mapping[str, Any], root: str | Path) -> CircuitProfile:
    circuits = load_circuit_catalog(Path(root) / config["circuit_catalog"])
    for circuit in circuits:
        if circuit.circuit_id == config["circuit_id"]:
            return circuit
    raise Level0InputError(f"circuit {config['circuit_id']!r} is not in the catalogue")


def race_inputs(
    *, vehicle_id: str, mass_kg: float, drag_area: float, config: Mapping[str, Any]
) -> tuple[RaceVehicle, RaceControl]:
    spec = config["vehicle"]
    thermal = spec["thermal"]
    vehicle = RaceVehicle(
        vehicle_id=vehicle_id,
        longitudinal=VehicleParameters(
            mass_kg, drag_area, float(spec["rolling_resistance_coefficient"])
        ),
        commanded_tractive_force_n=float(spec["commanded_tractive_force_n"]),
        initial_onboard_energy_j=float(spec["initial_onboard_energy_j"]),
        waste_heat_power_w=float(spec["waste_heat_power_w"]),
        auxiliary_power_w=float(spec["auxiliary_power_w"]),
        thermal_parameters=ThermalParameters(
            float(thermal["heat_capacity_j_per_k"]),
            float(thermal["passive_conductance_w_per_k"]),
            float(thermal["active_conductance_w_per_k"]),
            float(thermal["derating_start_temperature_k"]),
            float(thermal["failure_temperature_k"]),
        ),
        initial_temperature_k=float(spec["initial_temperature_k"]),
    )
    control_spec = config["control"]
    control = RaceControl(
        time_step_s=float(control_spec["time_step_s"]),
        timeout_s=float(control_spec["timeout_s"]),
        ambient_temperature_k=float(control_spec["ambient_temperature_k"]),
        active_cooling_command=float(control_spec["active_cooling_command"]),
        random_seed=int(control_spec["random_seed"]),
        event_bisection_iterations=int(control_spec["event_bisection_iterations"]),
    )
    return vehicle, control


def evaluate_manifest(
    manifest_path: str | Path, config: Mapping[str, Any], root: str | Path
) -> dict[str, Any]:
    """Race the packaged vehicle once and return exactly ``OUTPUT_FIELDS``."""

    manifest_path = Path(manifest_path)
    raw = manifest_path.read_bytes()
    manifest = json.loads(raw.decode("utf-8"))
    mass = root_mass_kg(manifest)
    area = drag_area_m2(leaf_points(manifest, manifest_path.parent), config)
    circuit = select_circuit(config, root)
    digest = hashlib.sha256(raw).hexdigest()
    vehicle, control = race_inputs(
        vehicle_id=f"manifest-{digest[:16]}", mass_kg=mass, drag_area=area, config=config
    )
    result = run_full_race(circuit=circuit, vehicle=vehicle, control=control)
    if result.replay.model_version != RACE_KERNEL_ID:
        raise Level0InputError(f"race kernel reported {result.replay.model_version!r}")
    return {
        "manifest_sha256": digest,
        "mass_kg": mass,
        "drag_area_m2": area,
        "outcome": result.outcome,
        "race_time_s": result.final_state.time_s,
        "consumed_energy_j": result.consumed_energy_j,
        "terminal_energy_boundary_residual_j": result.terminal_energy_boundary_residual_j,
        "circuit_id": circuit.circuit_id,
        "race_kernel": result.replay.model_version,
    }


def result_bytes(result: Mapping[str, Any]) -> bytes:
    return (json.dumps(dict(result), indent=2, sort_keys=True) + "\n").encode("utf-8")
