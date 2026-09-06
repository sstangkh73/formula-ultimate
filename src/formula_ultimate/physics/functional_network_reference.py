"""Closed-form edge-resistance reference for the Work 100 network solver."""

from __future__ import annotations

import math
from typing import Any, Mapping

import numpy as np

from formula_ultimate.search.executable_morphology import validate_genome


REFERENCE_VERSION = "functional_network_exact_resistance_reference_v1"


class ReferenceViolation(ValueError):
    """Raised when the independent formula cannot apply to a candidate."""


def _network(genome: Mapping[str, Any], limits: Mapping[str, Any]) -> dict[str, Any]:
    validate_genome(genome, limits)
    parent: dict[str, str] = {}
    points = {}
    radii = {}
    for part in genome["parts"]:
        for node in part["nodes"]:
            label = f"{part['part_id']}/{node['node_id']}"
            parent[label] = label
            points[label] = tuple(float(x) for x in node["point_m"])
            radii[label] = float(node["radius_m"])

    def find(label: str) -> str:
        while parent[label] != label:
            parent[label] = parent[parent[label]]
            label = parent[label]
        return label

    for interface in genome["interfaces"]:
        if interface["kind"] != "fixed" or not {"load", "thermal"}.issubset(interface["domains"]):
            raise ReferenceViolation("reference only covers fixed load-and-thermal interfaces")
        a = find(f"{interface['part_a']}/{interface['node_a']}")
        b = find(f"{interface['part_b']}/{interface['node_b']}")
        keep, remove = sorted((a, b))
        parent[remove] = keep
    edges = []
    for part in genome["parts"]:
        for edge in part["edges"]:
            raw_a = f"{part['part_id']}/{edge['a']}"
            raw_b = f"{part['part_id']}/{edge['b']}"
            a, b = find(raw_a), find(raw_b)
            if a == b:
                raise ReferenceViolation("reference edge collapsed")
            edges.append({"a": a, "b": b, "length_m": math.dist(points[raw_a], points[raw_b]), "radius_a_m": radii[raw_a], "radius_b_m": radii[raw_b]})
    terminals = {terminal["role"]: find(f"{terminal['part_id']}/{terminal['node_id']}") for terminal in genome["terminals"]}
    if set(terminals) != {"source", "sink"} or terminals["source"] == terminals["sink"]:
        raise ReferenceViolation("reference needs distinct source and sink")
    return {"nodes": sorted({find(label) for label in parent}), "edges": edges, **terminals}


def _exact_field(network: Mapping[str, Any], coefficient: float, applied: float) -> dict[str, Any]:
    nodes = network["nodes"]
    index = {label: position for position, label in enumerate(nodes)}
    matrix = np.zeros((len(nodes), len(nodes)))
    edge_rows = []
    for edge in network["edges"]:
        resistance = edge["length_m"] / (coefficient * math.pi * edge["radius_a_m"] * edge["radius_b_m"])
        conductance = 1.0 / resistance
        a, b = index[edge["a"]], index[edge["b"]]
        matrix[a, a] += conductance
        matrix[b, b] += conductance
        matrix[a, b] -= conductance
        matrix[b, a] -= conductance
        edge_rows.append((edge, resistance))
    rhs = np.zeros(len(nodes))
    rhs[index[network["sink"]]] = applied
    fixed = index[network["source"]]
    free = [item for item in range(len(nodes)) if item != fixed]
    try:
        values = np.zeros(len(nodes))
        values[free] = np.linalg.solve(matrix[np.ix_(free, free)], rhs[free])
    except np.linalg.LinAlgError as error:
        raise ReferenceViolation("reference matrix is singular") from error
    reaction = float((matrix @ values - rhs)[fixed])
    flows = []
    for edge, resistance in edge_rows:
        flow = float(values[index[edge["b"]]] - values[index[edge["a"]]]) / resistance
        flows.append({**edge, "resistance": resistance, "flow": flow})
    return {"sink_value": float(values[index[network["sink"]]]), "source_reaction": reaction, "flows": flows}


def evaluate_reference(genome: Mapping[str, Any], limits: Mapping[str, Any], material: Mapping[str, Any], task: Mapping[str, Any]) -> dict[str, Any]:
    network = _network(genome, limits)
    mechanical = _exact_field(network, float(material["youngs_modulus_pa"]), float(task["force_n"]))
    thermal = _exact_field(network, float(material["thermal_conductivity_w_per_m_k"]), float(task["heat_w"]))
    maximum_stress = max(abs(edge["flow"]) / (math.pi * min(edge["radius_a_m"], edge["radius_b_m"]) ** 2) for edge in mechanical["flows"])
    components = {
        "displacement": mechanical["sink_value"] / float(task["maximum_displacement_m"]),
        "stress": maximum_stress / float(material["yield_strength_pa"]),
        "temperature": thermal["sink_value"] / float(task["maximum_temperature_rise_k"]),
    }
    return {
        "reference_version": REFERENCE_VERSION,
        "coupled_utilization_ratio": max(components.values()),
        "maximum_displacement_m": mechanical["sink_value"],
        "maximum_axial_stress_pa": maximum_stress,
        "maximum_temperature_rise_k": thermal["sink_value"],
        "utilization_components": components,
        "mechanical_source_reaction_n": mechanical["source_reaction"],
        "thermal_source_reaction_w": thermal["source_reaction"],
    }
