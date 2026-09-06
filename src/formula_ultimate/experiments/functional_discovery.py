"""Preregistered treatment construction and evidence assessment for Work 100."""

from __future__ import annotations

from copy import deepcopy
import math
from typing import Any, Mapping

from formula_ultimate.experiments.discovery_registration import digest
from formula_ultimate.physics.functional_network_reference import evaluate_reference
from formula_ultimate.physics.functional_network_solver import evaluate_functional_network, process_envelope
from formula_ultimate.search.executable_morphology import OPERATORS, mutate, root_genome, validate_genome


TRIAL_SCHEMA = "functional_coupled_discovery_trial_v1"
TREATMENTS = ("FIXED_TOPOLOGY", "RANDOM_CONTROL", "GRAPH_ONLY", "MORPHOLOGY_ONLY", "JOINT_MORPHOLOGY_CONTROLLER")


class FunctionalDiscoveryViolation(ValueError):
    """Raised when the Work 100 trial or evidence changes after registration."""


def _exact(value: Mapping[str, Any], fields: set[str], label: str) -> None:
    if not isinstance(value, Mapping) or set(value) != fields:
        raise FunctionalDiscoveryViolation(f"{label} schema mismatch")


def _number(value: Any, label: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise FunctionalDiscoveryViolation(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0.0):
        raise FunctionalDiscoveryViolation(f"{label} is outside finite bounds")
    return result


def validate_trial_config(config: Mapping[str, Any]) -> dict[str, Any]:
    _exact(config, {"schema", "seeds", "treatments", "representation_limits", "material", "process", "proxy_refinement_levels", "refinement_levels", "training_task", "holdout_task", "tolerances", "analysis", "environment", "claim_boundary"}, "trial")
    if config["schema"] != TRIAL_SCHEMA:
        raise FunctionalDiscoveryViolation("trial schema mismatch")
    if tuple(config["treatments"]) != TREATMENTS:
        raise FunctionalDiscoveryViolation("treatment set or order changed")
    seeds = config["seeds"]
    if not isinstance(seeds, list) or len(seeds) < 2 or len(set(seeds)) != len(seeds) or any(isinstance(seed, bool) or not isinstance(seed, int) for seed in seeds):
        raise FunctionalDiscoveryViolation("paired integer seeds are required")
    validate_genome(root_genome(seeds[0]), config["representation_limits"])
    material = config["material"]
    _exact(material, {"material_id", "density_kg_per_m3", "youngs_modulus_pa", "yield_strength_pa", "thermal_conductivity_w_per_m_k", "model_scope"}, "material")
    for key in ("density_kg_per_m3", "youngs_modulus_pa", "yield_strength_pa", "thermal_conductivity_w_per_m_k"):
        _number(material[key], key, positive=True)
    if material["model_scope"] != "declared_linear_isotropic_study_model_not_material_certification":
        raise FunctionalDiscoveryViolation("material model scope is too broad")
    process = config["process"]
    _exact(process, {"process_id", "minimum_diameter_m", "maximum_parts", "maximum_span_m", "claim"}, "process")
    _number(process["minimum_diameter_m"], "minimum diameter", positive=True)
    _number(process["maximum_parts"], "maximum parts", positive=True)
    _number(process["maximum_span_m"], "maximum span", positive=True)
    if process["claim"] != "computational_envelope_only_not_manufacturing_proof":
        raise FunctionalDiscoveryViolation("process claim boundary changed")
    for key in ("proxy_refinement_levels", "refinement_levels"):
        levels = config[key]
        if not isinstance(levels, list) or len(levels) != 3 or any(isinstance(level, bool) or not isinstance(level, int) or level < 1 for level in levels) or not levels[0] < levels[1] < levels[2]:
            raise FunctionalDiscoveryViolation(f"{key} must contain three increasing integers")
    for label in ("training_task", "holdout_task"):
        task = config[label]
        _exact(task, {"task_id", "dataset_id", "force_n", "heat_w", "maximum_displacement_m", "maximum_temperature_rise_k", "reference_vehicle_mass_kg", "external_source_ancestry", "external_sink_ancestry"}, label)
        for key in ("force_n", "heat_w", "maximum_displacement_m", "maximum_temperature_rise_k", "reference_vehicle_mass_kg"):
            _number(task[key], f"{label}.{key}", positive=True)
        if task["external_source_ancestry"] != "external_source" or task["external_sink_ancestry"] != "external_sink":
            raise FunctionalDiscoveryViolation("external task terminal ancestry changed")
    if config["training_task"]["dataset_id"] == config["holdout_task"]["dataset_id"] or config["training_task"]["task_id"] == config["holdout_task"]["task_id"]:
        raise FunctionalDiscoveryViolation("training and holdout tasks must be distinct")
    tolerances = config["tolerances"]
    _exact(tolerances, {"maximum_refinement_relative_change", "maximum_reference_relative_error", "maximum_conservation_residual"}, "tolerances")
    for key, value in tolerances.items():
        if not 0.0 < _number(value, key, positive=True) <= 0.05:
            raise FunctionalDiscoveryViolation("numerical tolerance is outside the bounded study range")
    analysis = config["analysis"]
    _exact(analysis, {"primary_metric", "direction", "minimum_effect", "test", "alpha", "multiplicity", "sample_size_rationale", "controller_policy"}, "analysis")
    if analysis["primary_metric"] != "coupled_utilization_ratio" or analysis["direction"] != "minimize":
        raise FunctionalDiscoveryViolation("primary analysis changed")
    _number(analysis["minimum_effect"], "minimum effect", positive=True)
    alpha = _number(analysis["alpha"], "alpha", positive=True)
    if alpha >= 1.0:
        raise FunctionalDiscoveryViolation("alpha must be below one")
    environment = config["environment"]
    _exact(environment, {"python", "cadquery", "numpy", "workers", "ordering"}, "environment")
    if environment["workers"] != 1 or environment["ordering"] != "registered_serial":
        raise FunctionalDiscoveryViolation("execution environment is not deterministic serial")
    boundary = config["claim_boundary"]
    _exact(boundary, {"survivor_scope", "admitted_claims", "prohibited_claims"}, "claim boundary")
    required_prohibitions = {"complete_vehicle_feasibility", "race_superiority", "technology_novelty", "promotion_ready", "physical_validation"}
    if boundary["survivor_scope"] != "bounded_axial_thermal_subsystem_simulation_v1" or not required_prohibitions.issubset(boundary["prohibited_claims"]):
        raise FunctionalDiscoveryViolation("claim boundary is incomplete")
    return {"status": "passed", "trial_sha256": digest(config), "seed_count": len(seeds), "treatment_count": len(TREATMENTS)}


def build_treatment(config: Mapping[str, Any], treatment: str, seed: int) -> dict[str, Any]:
    validate_trial_config(config)
    if treatment not in TREATMENTS or seed not in config["seeds"]:
        raise FunctionalDiscoveryViolation("unregistered treatment or seed")
    genome = root_genome(seed)
    trace = []

    def apply(operator: str, step: int) -> None:
        nonlocal genome
        proposal = mutate(genome, operator, seed=seed, step=step, limits=config["representation_limits"])
        genome = proposal["child"]
        trace.append(proposal["trace"])

    if treatment == "RANDOM_CONTROL":
        apply(("perturb_node", "mutate_radius_field")[seed % 2], 1)
    elif treatment == "GRAPH_ONLY":
        apply("grow_branch", 1)
        apply("split_part", 2)
    elif treatment == "MORPHOLOGY_ONLY":
        apply("perturb_node", 1)
        apply("mutate_radius_field", 2)
    elif treatment == "JOINT_MORPHOLOGY_CONTROLLER":
        apply("grow_branch", 1)
        apply("split_part", 2)
        apply("mutate_controller", 3)
    for part in genome["parts"]:
        part["material_id"] = config["material"]["material_id"]
    genome["genome_id"] = f"trial_{treatment.lower()}_{seed}"
    validation = validate_genome(genome, config["representation_limits"])
    return {"treatment": treatment, "seed": seed, "genome": genome, "mutation_trace": trace, "genotype_sha256": validation["genotype_sha256"], "functional_signature": validation["functional_signature"], "descriptors": validation["descriptors"]}


def _relative(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1e-30)


def _validate_task_and_material_binding(config: Mapping[str, Any], genome: Mapping[str, Any], task: Mapping[str, Any]) -> None:
    source = [terminal for terminal in genome["terminals"] if terminal["role"] == "source"]
    sink = [terminal for terminal in genome["terminals"] if terminal["role"] == "sink"]
    if len(source) != 1 or len(sink) != 1:
        raise FunctionalDiscoveryViolation("exactly one source and sink terminal are required")
    if task["external_source_ancestry"] not in source[0]["ancestry"]:
        raise FunctionalDiscoveryViolation("source terminal ancestry does not match the registered task")
    if task["external_sink_ancestry"] not in sink[0]["ancestry"]:
        raise FunctionalDiscoveryViolation("sink terminal ancestry does not match the registered task")
    material_ids = {part["material_id"] for part in genome["parts"]}
    if material_ids != {config["material"]["material_id"]}:
        raise FunctionalDiscoveryViolation("candidate material identity does not match the registered study model")


def assess_candidate(config: Mapping[str, Any], genome: Mapping[str, Any], task_name: str, *, proxy: bool = False) -> dict[str, Any]:
    validate_trial_config(config)
    if task_name not in {"training_task", "holdout_task"}:
        raise FunctionalDiscoveryViolation("unknown task partition")
    task = config[task_name]
    _validate_task_and_material_binding(config, genome, task)
    levels = config["proxy_refinement_levels"] if proxy else config["refinement_levels"]
    primary = evaluate_functional_network(genome, config["representation_limits"], config["material"], task, levels)
    reference = evaluate_reference(genome, config["representation_limits"], config["material"], task)
    reference_error = max(_relative(primary["fine"][key], reference[key]) for key in ("coupled_utilization_ratio", "maximum_displacement_m", "maximum_axial_stress_pa", "maximum_temperature_rise_k"))
    error = max(primary["last_two_relative_change"], primary["maximum_conservation_residual"], reference_error)
    tolerances = config["tolerances"]
    numerical_pass = primary["last_two_relative_change"] <= tolerances["maximum_refinement_relative_change"] and primary["maximum_conservation_residual"] <= tolerances["maximum_conservation_residual"] and reference_error <= tolerances["maximum_reference_relative_error"]
    status = primary["status"] if numerical_pass else "numerically_unresolved"
    return {
        "status": status,
        "task_id": task["task_id"],
        "dataset_id": task["dataset_id"],
        "proxy": proxy,
        "value": primary["fine"]["coupled_utilization_ratio"],
        "error": error,
        "refinements": list(levels),
        "primary": primary,
        "reference": reference,
        "reference_relative_error": reference_error,
        "numerical_pass": numerical_pass,
    }


def assess_process(config: Mapping[str, Any], genome: Mapping[str, Any]) -> dict[str, Any]:
    validate_trial_config(config)
    return process_envelope(genome, config["representation_limits"], config["process"])


def unresolved_proxy_audit(selection: Mapping[str, Any], refined: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    """Report an unestimable audit without inventing Boolean proxy labels."""
    selected = [row["candidate_id"] for row in selection["selection"]["selected"]]
    population = {row["candidate_id"]: row for row in selection["population"]}
    if not selected or set(selected) != set(refined) or not set(selected) <= set(population):
        raise FunctionalDiscoveryViolation("unresolved proxy audit coverage mismatch")
    proxy_known = sum(population[cid]["proxy_score"] is not None for cid in selected)
    reference_statuses = [refined[cid]["status"] for cid in selected]
    allowed = {"physically_feasible", "physically_failed", "numerically_unresolved"}
    if not set(reference_statuses) <= allowed:
        raise FunctionalDiscoveryViolation("unresolved proxy audit has unknown refined status")
    return {
        "status": "not_estimable_due_to_unresolved_proxy_labels",
        "selection_sha256": selection["selection_sha256"],
        "sampled": len(selected),
        "proxy_boolean_count": proxy_known,
        "proxy_unresolved_count": len(selected) - proxy_known,
        "refined_feasible_count": reference_statuses.count("physically_feasible"),
        "refined_failed_count": reference_statuses.count("physically_failed"),
        "refined_unresolved_count": reference_statuses.count("numerically_unresolved"),
        "false_negative_rate": None,
        "false_positive_rate": None,
        "reason": "Work 098 audit rates require Boolean proxy labels; unresolved labels remain unknown.",
    }


def treatment_matrix(config: Mapping[str, Any]) -> list[dict[str, Any]]:
    validate_trial_config(config)
    return [build_treatment(config, treatment, seed) for treatment in TREATMENTS for seed in config["seeds"]]
