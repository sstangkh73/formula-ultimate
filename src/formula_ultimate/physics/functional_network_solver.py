"""Geometry-derived axial-load and thermal-network field solver for Work 100."""

from __future__ import annotations

import math
from typing import Any, Mapping

import numpy as np

from formula_ultimate.search.executable_morphology import validate_genome


SOLVER_VERSION = "functional_axial_thermal_network_v1"


class FunctionalSolverViolation(ValueError):
    """Raised when a declared network cannot produce trustworthy field evidence."""


def _finite(value: Any, label: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise FunctionalSolverViolation(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0.0):
        raise FunctionalSolverViolation(f"{label} is outside its finite domain")
    return result


class _UnionFind:
    def __init__(self, labels: list[str]):
        self.parent = {label: label for label in labels}

    def find(self, label: str) -> str:
        parent = self.parent[label]
        if parent != label:
            self.parent[label] = self.find(parent)
        return self.parent[label]

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        keep, remove = sorted((ra, rb))
        self.parent[remove] = keep


def _network(genome: Mapping[str, Any], limits: Mapping[str, Any]) -> dict[str, Any]:
    validate_genome(genome, limits)
    labels = [f"{part['part_id']}/{node['node_id']}" for part in genome["parts"] for node in part["nodes"]]
    points = {f"{part['part_id']}/{node['node_id']}": tuple(float(x) for x in node["point_m"]) for part in genome["parts"] for node in part["nodes"]}
    radii = {f"{part['part_id']}/{node['node_id']}": float(node["radius_m"]) for part in genome["parts"] for node in part["nodes"]}
    union = _UnionFind(labels)
    for interface in genome["interfaces"]:
        if interface["kind"] != "fixed" or not {"load", "thermal"}.issubset(interface["domains"]):
            raise FunctionalSolverViolation("only fixed load-and-thermal interfaces are supported at this fidelity")
        union.union(f"{interface['part_a']}/{interface['node_a']}", f"{interface['part_b']}/{interface['node_b']}")
    roots = sorted({union.find(label) for label in labels})
    edges = []
    for part in genome["parts"]:
        for edge in part["edges"]:
            a_label = f"{part['part_id']}/{edge['a']}"
            b_label = f"{part['part_id']}/{edge['b']}"
            a, b = union.find(a_label), union.find(b_label)
            if a == b:
                raise FunctionalSolverViolation("an interface collapsed a material edge")
            length = math.dist(points[a_label], points[b_label])
            edges.append({"edge_id": f"{part['part_id']}/{edge['edge_id']}", "a": a, "b": b, "length_m": length, "radius_a_m": radii[a_label], "radius_b_m": radii[b_label]})
    terminals = {}
    for terminal in genome["terminals"]:
        terminals[terminal["role"]] = union.find(f"{terminal['part_id']}/{terminal['node_id']}")
    if set(terminals) != {"source", "sink"} or terminals["source"] == terminals["sink"]:
        raise FunctionalSolverViolation("exactly one distinct source and sink are required")
    return {"nodes": roots, "edges": edges, "source": terminals["source"], "sink": terminals["sink"]}


def _solve_field(network: Mapping[str, Any], *, subdivisions: int, coefficient: float, input_value: float) -> dict[str, Any]:
    if isinstance(subdivisions, bool) or not isinstance(subdivisions, int) or subdivisions < 1:
        raise FunctionalSolverViolation("subdivisions must be a positive integer")
    coefficient = _finite(coefficient, "field coefficient", positive=True)
    input_value = _finite(input_value, "field input", positive=True)
    expanded_edges = []
    nodes = set(network["nodes"])
    for edge in network["edges"]:
        chain = [edge["a"]] + [f"{edge['edge_id']}@{index}/{subdivisions}" for index in range(1, subdivisions)] + [edge["b"]]
        nodes.update(chain)
        segment_length = edge["length_m"] / subdivisions
        for index, (a, b) in enumerate(zip(chain, chain[1:])):
            fraction = (index + 0.5) / subdivisions
            radius = edge["radius_a_m"] + fraction * (edge["radius_b_m"] - edge["radius_a_m"])
            area = math.pi * radius * radius
            resistance = segment_length / (coefficient * area)
            expanded_edges.append({"edge_id": edge["edge_id"], "segment": index, "a": a, "b": b, "radius_m": radius, "area_m2": area, "length_m": segment_length, "resistance": resistance})
    ordered = sorted(nodes)
    index_of = {label: index for index, label in enumerate(ordered)}
    matrix = np.zeros((len(ordered), len(ordered)), dtype=float)
    for edge in expanded_edges:
        a, b = index_of[edge["a"]], index_of[edge["b"]]
        conductance = 1.0 / edge["resistance"]
        matrix[a, a] += conductance
        matrix[b, b] += conductance
        matrix[a, b] -= conductance
        matrix[b, a] -= conductance
    rhs = np.zeros(len(ordered), dtype=float)
    rhs[index_of[network["sink"]]] = input_value
    fixed = index_of[network["source"]]
    free = [index for index in range(len(ordered)) if index != fixed]
    try:
        condition = float(np.linalg.cond(matrix[np.ix_(free, free)]))
        if not math.isfinite(condition) or condition > 1e14:
            raise FunctionalSolverViolation(f"network matrix condition number is unsupported: {condition}")
        values = np.zeros(len(ordered), dtype=float)
        values[free] = np.linalg.solve(matrix[np.ix_(free, free)], rhs[free])
    except np.linalg.LinAlgError as error:
        raise FunctionalSolverViolation("network field solve is singular") from error
    residual = matrix @ values - rhs
    reaction = float(residual[fixed])
    free_residual = max((abs(float(residual[index])) for index in free), default=0.0) / max(abs(input_value), 1e-30)
    equilibrium_residual = abs(reaction + input_value) / max(abs(input_value), 1e-30)
    flows = []
    dissipation = 0.0
    for edge in expanded_edges:
        delta = float(values[index_of[edge["b"]]] - values[index_of[edge["a"]]])
        flow = delta / edge["resistance"]
        dissipation += flow * flow * edge["resistance"]
        flows.append({**edge, "flow": flow, "delta": delta})
    external_power = input_value * float(values[index_of[network["sink"]]])
    energy_residual = abs(external_power - dissipation) / max(abs(external_power), 1e-30)
    return {
        "subdivisions": subdivisions,
        "node_count": len(ordered),
        "segment_count": len(expanded_edges),
        "condition_number": condition,
        "values": {label: float(values[index]) for label, index in index_of.items()},
        "segments": flows,
        "source_reaction": reaction,
        "free_residual_relative": free_residual,
        "equilibrium_residual_relative": equilibrium_residual,
        "energy_residual_relative": energy_residual,
        "external_power": external_power,
        "dissipation": dissipation,
    }


def _relative(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1e-30)


def evaluate_functional_network(
    genome: Mapping[str, Any],
    limits: Mapping[str, Any],
    material: Mapping[str, Any],
    task: Mapping[str, Any],
    refinement_levels: list[int],
) -> dict[str, Any]:
    """Return full scalar fields and conservative margins at every refinement."""
    if len(refinement_levels) != 3 or any(isinstance(level, bool) or not isinstance(level, int) for level in refinement_levels) or not refinement_levels[0] < refinement_levels[1] < refinement_levels[2]:
        raise FunctionalSolverViolation("three strictly increasing refinement levels are required")
    youngs = _finite(material.get("youngs_modulus_pa"), "Young's modulus", positive=True)
    conductivity = _finite(material.get("thermal_conductivity_w_per_m_k"), "thermal conductivity", positive=True)
    density = _finite(material.get("density_kg_per_m3"), "density", positive=True)
    yield_strength = _finite(material.get("yield_strength_pa"), "yield strength", positive=True)
    force = _finite(task.get("force_n"), "force", positive=True)
    heat = _finite(task.get("heat_w"), "heat input", positive=True)
    displacement_limit = _finite(task.get("maximum_displacement_m"), "displacement limit", positive=True)
    temperature_limit = _finite(task.get("maximum_temperature_rise_k"), "temperature limit", positive=True)
    network = _network(genome, limits)
    levels = []
    volume = sum(edge["length_m"] * math.pi * (edge["radius_a_m"] ** 2 + edge["radius_a_m"] * edge["radius_b_m"] + edge["radius_b_m"] ** 2) / 3.0 for edge in network["edges"])
    for refinement in refinement_levels:
        mechanical = _solve_field(network, subdivisions=refinement, coefficient=youngs, input_value=force)
        thermal = _solve_field(network, subdivisions=refinement, coefficient=conductivity, input_value=heat)
        displacement = mechanical["values"][network["sink"]]
        temperature = thermal["values"][network["sink"]]
        edge_minimum_area = {
            edge["edge_id"]: math.pi * min(edge["radius_a_m"], edge["radius_b_m"]) ** 2
            for edge in network["edges"]
        }
        maximum_stress = max(
            abs(segment["flow"]) / edge_minimum_area[segment["edge_id"]]
            for segment in mechanical["segments"]
        )
        ratios = {
            "displacement": displacement / displacement_limit,
            "stress": maximum_stress / yield_strength,
            "temperature": temperature / temperature_limit,
        }
        utilization = max(ratios.values())
        levels.append({
            "refinement": refinement,
            "coupled_utilization_ratio": utilization,
            "maximum_displacement_m": displacement,
            "maximum_axial_stress_pa": maximum_stress,
            "maximum_temperature_rise_k": temperature,
            "utilization_components": ratios,
            "mechanical_field": mechanical,
            "thermal_field": thermal,
        })
    fine = levels[-1]
    penultimate = levels[-2]
    convergence = max(_relative(fine[key], penultimate[key]) for key in ("coupled_utilization_ratio", "maximum_displacement_m", "maximum_axial_stress_pa", "maximum_temperature_rise_k"))
    maximum_residual = max(level[field][residual] for level in levels for field in ("mechanical_field", "thermal_field") for residual in ("free_residual_relative", "equilibrium_residual_relative", "energy_residual_relative"))
    failure_component = max(fine["utilization_components"], key=fine["utilization_components"].get)
    result = {
        "solver_version": SOLVER_VERSION,
        "status": "physically_feasible" if fine["coupled_utilization_ratio"] <= 1.0 else "physically_failed",
        "failure_component": None if fine["coupled_utilization_ratio"] <= 1.0 else failure_component,
        "levels": levels,
        "last_two_relative_change": convergence,
        "maximum_conservation_residual": maximum_residual,
        "fine": {key: fine[key] for key in ("coupled_utilization_ratio", "maximum_displacement_m", "maximum_axial_stress_pa", "maximum_temperature_rise_k", "utilization_components")},
        "geometry_derived_volume_m3": volume,
        "geometry_derived_mass_kg": volume * density,
        "vehicle_feedback": {
            "added_mass_kg": volume * density,
            "mass_fraction_of_reference_vehicle": volume * density / _finite(task.get("reference_vehicle_mass_kg"), "reference vehicle mass", positive=True),
            "subsystem_task_completed": fine["coupled_utilization_ratio"] <= 1.0,
            "controller_gain_observed_not_causal": float(genome["controller"]["gain"]),
        },
    }
    return result


def process_envelope(genome: Mapping[str, Any], limits: Mapping[str, Any], process: Mapping[str, Any]) -> dict[str, Any]:
    validate_genome(genome, limits)
    minimum_diameter = min(2.0 * float(node["radius_m"]) for part in genome["parts"] for node in part["nodes"])
    coordinates = [float(value) for part in genome["parts"] for node in part["nodes"] for value in node["point_m"]]
    span = max(coordinates) - min(coordinates)
    ratios = {
        "minimum_feature": _finite(process.get("minimum_diameter_m"), "process minimum diameter", positive=True) / minimum_diameter,
        "part_count": len(genome["parts"]) / _finite(process.get("maximum_parts"), "process maximum parts", positive=True),
        "span": span / _finite(process.get("maximum_span_m"), "process maximum span", positive=True),
    }
    violation = max(ratios.values())
    return {"status": "manufacturing_compatible" if violation <= 1.0 else "manufacturing_incompatible", "process_violation_ratio": violation, "ratios": ratios, "minimum_diameter_m": minimum_diameter, "span_m": span, "claim": "declared_process_envelope_check_only"}
