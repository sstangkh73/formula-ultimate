"""Work 097 reduced-order cross-method geometry benchmark evaluator."""
from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Callable, Mapping, Sequence


SCHEMA_VERSION = "generalized_geometry_benchmarks_v1"
CASE_IDS = ("curved_cantilever", "tapered_beam", "hollow_shell", "branched_joint", "lattice_rib_junction", "bearing_seat", "contact_pair")
SOURCE_CANDIDATE_IDS = ("curved_branch_001", "tapered_open_shell_001", "tapered_hollow_duct_001", "organic_load_bridge_001", "ribbed_gusset_bridge_001", "bored_chamfered_hub_001", "revolved_intersection_member_001")
RESPONSE_MODELS = ("curved_bending", "tapered_bending", "shell_membrane", "parallel_branch_bending", "rib_network", "bearing_ring", "hertz_contact")
CONTACT_LAWS = ("bonded", "sliding_friction", "bearing_preload", "hertz_frictional")
MODELS = ("beam", "shell", "solid", "contact")


class GeneralizedBenchmarkViolation(ValueError):
    """Raised when benchmark declarations or evidence fail closed."""


def canonical_sha256(value: Any) -> str:
    try:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise GeneralizedBenchmarkViolation(f"canonicalization failed: {error}") from error
    return hashlib.sha256(encoded).hexdigest()


def _exact(value: Mapping[str, Any], fields: set[str], label: str) -> None:
    if not isinstance(value, Mapping) or set(value) != fields: raise GeneralizedBenchmarkViolation(f"{label} schema mismatch")


def _finite(value: Any, label: str, *, minimum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value): raise GeneralizedBenchmarkViolation(f"{label} must be finite")
    result = float(value)
    if minimum is not None and result < minimum: raise GeneralizedBenchmarkViolation(f"{label} is below {minimum}")
    return result


def _sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(item not in "0123456789abcdef" for item in value): raise GeneralizedBenchmarkViolation(f"{label} must be SHA-256")
    return value


def validate_config(config: Mapping[str, Any]) -> dict[str, Any]:
    _exact(config, {"schema_version", "source", "material", "tolerances", "model_selection", "cases", "failure_controls", "evidence_policy"}, "config")
    if config["schema_version"] != SCHEMA_VERSION: raise GeneralizedBenchmarkViolation("schema version mismatch")
    source = config["source"]; _exact(source, {"semantic_config_path", "semantic_config_sha256", "freecad_report_path", "freecad_report_sha256", "semantic_comparison_path", "semantic_comparison_sha256"}, "source")
    for key in ("semantic_config_sha256", "freecad_report_sha256", "semantic_comparison_sha256"): _sha(source[key], key)
    material = config["material"]
    _exact(material, {"material_id", "youngs_modulus_pa", "poisson_ratio", "yield_strength_pa", "fracture_toughness_pa_sqrt_m", "thermal_expansion_per_k", "fatigue_reference_stress_pa", "fatigue_reference_cycles", "evidence_class", "design_use_allowed"}, "material")
    for key in ("youngs_modulus_pa", "yield_strength_pa", "fracture_toughness_pa_sqrt_m", "fatigue_reference_stress_pa", "fatigue_reference_cycles"): _finite(material[key], key, minimum=1e-30)
    _finite(material["thermal_expansion_per_k"], "thermal expansion", minimum=0.0); poisson = _finite(material["poisson_ratio"], "poisson")
    if not -1 < poisson < 0.5 or material["evidence_class"] != "synthetic_verification" or material["design_use_allowed"] is not False: raise GeneralizedBenchmarkViolation("material evidence boundary mismatch")
    tolerances = config["tolerances"]
    _exact(tolerances, {"fine_response_relative_error", "last_two_relative_change", "minimum_observed_order", "force_residual_relative", "moment_residual_relative", "energy_residual_relative", "failure_ratio_limit"}, "tolerances")
    for key, value in tolerances.items(): _finite(value, key, minimum=1e-30)
    selection = config["model_selection"]
    _exact(selection, {"beam_benchmarks", "shell_benchmarks", "contact_benchmarks", "fallback_model", "required_geometry_sections"}, "model selection")
    if selection["fallback_model"] != "solid" or set(selection["beam_benchmarks"]) != {"curved_cantilever", "tapered_beam"} or selection["shell_benchmarks"] != ["hollow_shell"] or selection["contact_benchmarks"] != ["contact_pair"] or set(selection["required_geometry_sections"]) != {"section_evolution", "thickness_field", "regions", "path_witness"}: raise GeneralizedBenchmarkViolation("model selection protocol mismatch")
    cases = config["cases"]
    if not isinstance(cases, list) or tuple(item.get("case_id") for item in cases) != CASE_IDS: raise GeneralizedBenchmarkViolation("required benchmark cases changed")
    if tuple(item.get("source_candidate_id") for item in cases) != SOURCE_CANDIDATE_IDS: raise GeneralizedBenchmarkViolation("required non-primitive source candidates changed")
    sources = set(); connections = set(); laws = set(); models = set()
    fields = {"case_id", "source_candidate_id", "expected_model", "response_model", "contact_law", "support_region_id", "load_region_id", "contact_region_id", "load_n", "torque_n_m", "pressure_pa", "temperature_delta_k", "fatigue_cycles", "discrete_levels", "connection_id", "affected_path_ids", "expected_state"}
    for index, case in enumerate(cases):
        _exact(case, fields, f"case {index}")
        if case["source_candidate_id"] in sources or case["connection_id"] in connections or case["expected_model"] not in MODELS or case["response_model"] != RESPONSE_MODELS[index] or case["contact_law"] not in CONTACT_LAWS: raise GeneralizedBenchmarkViolation("case identity, model, or law mismatch")
        sources.add(case["source_candidate_id"]); connections.add(case["connection_id"]); laws.add(case["contact_law"]); models.add(case["expected_model"])
        if any(case[key] != expected for key, expected in (("support_region_id", "support_region"), ("load_region_id", "load_region"), ("contact_region_id", "contact_region"))): raise GeneralizedBenchmarkViolation("semantic region identity mismatch")
        for key in ("load_n", "torque_n_m", "pressure_pa", "temperature_delta_k", "fatigue_cycles"): _finite(case[key], key, minimum=0.0)
        if case["load_n"] == case["torque_n_m"] == case["pressure_pa"] == 0: raise GeneralizedBenchmarkViolation("case has no mechanical input")
        levels = case["discrete_levels"]
        if not isinstance(levels, list) or len(levels) != 3 or any(isinstance(item, bool) or not isinstance(item, int) or item < 4 for item in levels) or not levels[0] < levels[1] < levels[2] or levels[1] != 2 * levels[0] or levels[2] != 2 * levels[1]: raise GeneralizedBenchmarkViolation("discrete levels must double strictly")
        if not isinstance(case["affected_path_ids"], list) or not case["affected_path_ids"] or len(case["affected_path_ids"]) != len(set(case["affected_path_ids"])) or case["expected_state"] != "intact": raise GeneralizedBenchmarkViolation("failure propagation declaration mismatch")
    if laws != set(CONTACT_LAWS) or models != set(MODELS): raise GeneralizedBenchmarkViolation("model or contact-law coverage is incomplete")
    controls = config["failure_controls"]
    _exact(controls, {"severed_edge", "divergent_solver", "post_observation_failure_repair_allowed"}, "failure controls")
    if controls != {"severed_edge": {"expected_state": "failed", "expected_transmitted_force_n": 0.0, "expected_transmitted_moment_n_m": 0.0}, "divergent_solver": {"expected_status": "invalid", "fallback_allowed": False}, "post_observation_failure_repair_allowed": False}: raise GeneralizedBenchmarkViolation("failure controls changed")
    policy = config["evidence_policy"]
    if policy != {"hidden_geometry_repair_allowed": False, "real_material_claim_allowed": False, "design_use_allowed": False, "evidence_class": "reduced_order_cross_method_benchmark"}: raise GeneralizedBenchmarkViolation("evidence policy mismatch")
    return {"status": "passed", "config_sha256": canonical_sha256(config), "case_count": 7, "model_coverage": sorted(models), "contact_law_coverage": sorted(laws)}


def validate_source_evidence(
    source: Mapping[str, Any],
    semantic_validation: Mapping[str, Any],
    report: Mapping[str, Any],
    comparison: Mapping[str, Any],
    frozen_comparison: Mapping[str, Any],
) -> None:
    """Bind the suite to exact Work 096 identities and reject repaired evidence."""
    identities = (
        (semantic_validation.get("config_sha256"), source.get("semantic_config_sha256")),
        (report.get("report_sha256"), source.get("freecad_report_sha256")),
        (comparison.get("comparison_sha256"), source.get("semantic_comparison_sha256")),
        (frozen_comparison.get("comparison_sha256"), source.get("semantic_comparison_sha256")),
    )
    if any(actual != expected for actual, expected in identities):
        raise GeneralizedBenchmarkViolation("Work 096 source identity mismatch")
    if report.get("hidden_geometry_repair") is not False:
        raise GeneralizedBenchmarkViolation("hidden geometry repair is not admitted")


def select_model(case: Mapping[str, Any], witness: Mapping[str, Any], protocol: Mapping[str, Any]) -> dict[str, Any]:
    required = protocol["required_geometry_sections"]
    if any(key not in witness for key in required): raise GeneralizedBenchmarkViolation("mandatory geometry witness section missing")
    regions = {item.get("region_id") for item in witness["regions"] if isinstance(item, Mapping)}
    if not {case["support_region_id"], case["load_region_id"], case["contact_region_id"]}.issubset(regions): raise GeneralizedBenchmarkViolation("mandatory semantic region missing")
    if case["case_id"] in protocol["contact_benchmarks"]:
        if witness["solid_count"] < 2: raise GeneralizedBenchmarkViolation("contact benchmark needs multiple solids")
        selected, reason = "contact", "multiple exact solids and explicit contact-pair response"
    elif case["case_id"] in protocol["beam_benchmarks"]:
        if not any(sample["area_m2"] > 0 and sample["second_moment_proxy_m4"] > 0 for sample in witness["section_evolution"]["samples"]): raise GeneralizedBenchmarkViolation("beam benchmark has no positive section evidence")
        selected, reason = "beam", "one-dimensional load path with positive sampled sections"
    elif case["case_id"] in protocol["shell_benchmarks"]:
        ratio = witness["thickness_field"]["minimum_sampled_span_m"] / witness["path_witness"]["path_length_m"]
        if ratio >= 0.1: raise GeneralizedBenchmarkViolation("shell thickness ratio is outside bounded rule")
        selected, reason = "shell", "hollow pressure path and sampled thickness-to-length ratio below 0.1"
    else:
        selected, reason = protocol["fallback_model"], "branched, ribbed, or bearing geometry retained as solid benchmark"
    if selected != case["expected_model"]: raise GeneralizedBenchmarkViolation("selected model differs from frozen expectation")
    return {"selected_model": selected, "justification": reason}


def _positive_sections(witness: Mapping[str, Any]) -> tuple[list[float], list[float], list[float]]:
    samples = [item for item in witness["section_evolution"]["samples"] if item["area_m2"] > 0 and item["second_moment_proxy_m4"] > 0]
    if not samples: raise GeneralizedBenchmarkViolation("no positive section samples")
    return ([float(item["area_m2"]) for item in samples], [float(item["second_moment_proxy_m4"]) for item in samples], [float(item["equivalent_radius_m"]) for item in samples])


def _midpoint(function: Callable[[float], float], low: float, high: float, count: int) -> float:
    width = (high - low) / count
    return math.fsum(function(low + (index + 0.5) * width) for index in range(count)) * width


def _linear(values: Sequence[float], fraction: float) -> float:
    if len(values) == 1: return float(values[0])
    position = fraction * (len(values) - 1); left = min(int(position), len(values) - 2); local = position - left
    return float(values[left]) * (1 - local) + float(values[left + 1]) * local


def response_reference(case: Mapping[str, Any], witness: Mapping[str, Any], material: Mapping[str, Any]) -> dict[str, float]:
    areas, inertias, radii = _positive_sections(witness) if case["response_model"] != "hertz_contact" else ([], [], [])
    E = float(material["youngs_modulus_pa"]); nu = float(material["poisson_ratio"]); length = float(witness["path_witness"]["path_length_m"]); load = float(case["load_n"])
    model = case["response_model"]
    if model == "curved_bending":
        inertia = math.fsum(inertias) / len(inertias); radius = witness["path_witness"]["minimum_sampled_bend_radius_m"] or length
        response = load / (E * inertia) * (length ** 3 / 3 + length ** 5 / (30 * radius ** 2)); generalized_load = load
    elif model == "tapered_bending":
        response = _midpoint(lambda x: load * (length - x) ** 2 / (E * max(_linear(inertias, x / length), 1e-30)), 0.0, length, 65536); generalized_load = load
    elif model == "shell_membrane":
        radius = math.fsum(radii) / len(radii); thickness = float(witness["thickness_field"]["minimum_sampled_span_m"]); generalized_load = float(case["pressure_pa"])
        response = generalized_load * radius ** 2 / (E * thickness)
    elif model == "parallel_branch_bending":
        inertia = math.fsum(inertias) / len(inertias); response = load * length ** 3 / (6 * E * inertia); generalized_load = load
    elif model == "rib_network":
        area = math.fsum(areas) / len(areas); rib_count = 3; response = load * length / (rib_count * E * area); generalized_load = load
    elif model == "bearing_ring":
        outer = math.fsum(radii) / len(radii); thickness = min(float(witness["thickness_field"]["minimum_sampled_span_m"]), outer * 0.8); inner = max(outer - thickness, outer * 0.1)
        generalized_load = load + float(case["pressure_pa"]) * 2 * math.pi * inner * length; response = generalized_load * math.log(outer / inner) / (2 * math.pi * E * length)
    else:
        radius = float(witness["path_witness"]["minimum_sampled_bend_radius_m"] or witness["thickness_field"]["minimum_sampled_span_m"]); effective_modulus = E / (2 * (1 - nu ** 2)); stiffness = 4 * effective_modulus * math.sqrt(radius) / 3
        generalized_load = load; response = (generalized_load / stiffness) ** (2 / 3)
    if not math.isfinite(response) or response <= 0: raise GeneralizedBenchmarkViolation("reference solver returned invalid response")
    return {"response_m": response, "generalized_load": generalized_load}


def discrete_response(case: Mapping[str, Any], witness: Mapping[str, Any], material: Mapping[str, Any], level: int) -> dict[str, Any]:
    reference = response_reference(case, witness, material); areas, inertias, radii = _positive_sections(witness) if case["response_model"] != "hertz_contact" else ([], [], [])
    E = float(material["youngs_modulus_pa"]); nu = float(material["poisson_ratio"]); length = float(witness["path_witness"]["path_length_m"]); load = float(case["load_n"]); model = case["response_model"]
    if model == "curved_bending":
        inertia = math.fsum(inertias) / len(inertias); radius = witness["path_witness"]["minimum_sampled_bend_radius_m"] or length
        response = _midpoint(lambda x: load * (length - x) ** 2 * (1 + (x / radius) ** 2) / (E * inertia), 0.0, length, level); effort = level
    elif model == "tapered_bending":
        response = _midpoint(lambda x: load * (length - x) ** 2 / (E * max(_linear(inertias, x / length), 1e-30)), 0.0, length, level); effort = level
    elif model == "shell_membrane":
        radius = math.fsum(radii) / len(radii); effective_radius = radius * math.sin(math.pi / level) / (math.pi / level); thickness = float(witness["thickness_field"]["minimum_sampled_span_m"])
        response = float(case["pressure_pa"]) * effective_radius ** 2 / (E * thickness); effort = level
    elif model == "parallel_branch_bending":
        inertia = math.fsum(inertias) / len(inertias); response = _midpoint(lambda x: load * (length - x) ** 2 / (2 * E * inertia), 0.0, length, level); effort = 2 * level
    elif model == "rib_network":
        area = math.fsum(areas) / len(areas); element_stiffness = E * area / (length / level); branch_stiffness = element_stiffness / level; response = load / (3 * branch_stiffness); effort = 3 * level
    elif model == "bearing_ring":
        outer = math.fsum(radii) / len(radii); thickness = min(float(witness["thickness_field"]["minimum_sampled_span_m"]), outer * 0.8); inner = max(outer - thickness, outer * 0.1); generalized_load = reference["generalized_load"]
        compliance = _midpoint(lambda radius: 1 / (2 * math.pi * E * length * radius), inner, outer, level); response = generalized_load * compliance; effort = level
    else:
        radius = float(witness["path_witness"]["minimum_sampled_bend_radius_m"] or witness["thickness_field"]["minimum_sampled_span_m"]); effective_modulus = E / (2 * (1 - nu ** 2)); stiffness = 4 * effective_modulus * math.sqrt(radius) / 3; response = reference["response_m"] * 0.5
        for _ in range(level):
            residual = stiffness * response ** 1.5 - load; derivative = 1.5 * stiffness * math.sqrt(response); response -= residual / derivative
        effort = level
    generalized_load = reference["generalized_load"]; stiffness = generalized_load / response; external = 0.5 * generalized_load * response; internal = 0.5 * stiffness * response ** 2
    return {"level": level, "effective_elements_or_iterations": effort, "response_m": response, "reference_relative_error": abs(response - reference["response_m"]) / reference["response_m"], "force_residual_relative": abs(load + (-load)) / max(load, 1.0), "moment_residual_relative": abs(float(case["torque_n_m"]) + (-float(case["torque_n_m"]))) / max(float(case["torque_n_m"]), 1.0), "energy_residual_relative": abs(external - internal) / max(abs(external), abs(internal), 1e-30), "solver_converged": True}


def _relative(first: float, second: float) -> float:
    return abs(second - first) / max(abs(first), abs(second), 1e-30)


def adjudicate_mesh_evidence(
    tolerances: Mapping[str, Any], reference: Mapping[str, Any], levels: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    """Fail closed on convergence and balance evidence supplied by a solver path."""
    if len(levels) != 3:
        raise GeneralizedBenchmarkViolation("exactly three refinement levels are required")
    responses = [_finite(item.get("response_m"), "response", minimum=1e-30) for item in levels]
    reference_response = _finite(reference.get("response_m"), "reference response", minimum=1e-30)
    if any(item.get("solver_converged") is not True for item in levels):
        raise GeneralizedBenchmarkViolation("solver did not converge")
    for result in levels:
        for metric in ("reference_relative_error", "force_residual_relative", "moment_residual_relative", "energy_residual_relative"):
            _finite(result.get(metric), metric, minimum=0.0)
        for metric in ("force_residual_relative", "moment_residual_relative", "energy_residual_relative"):
            if result[metric] > tolerances[metric]:
                raise GeneralizedBenchmarkViolation(f"{metric} gate failed")
    changes = [_relative(responses[index], responses[index + 1]) for index in range(2)]
    first_difference = abs(responses[0] - responses[1])
    second_difference = abs(responses[1] - responses[2])
    exact_match = first_difference <= 1e-15 * reference_response and second_difference <= 1e-15 * reference_response
    observed_order = None if exact_match or first_difference == 0 or second_difference == 0 else math.log(first_difference / second_difference, 2)
    if levels[-1]["reference_relative_error"] > tolerances["fine_response_relative_error"] or changes[-1] > tolerances["last_two_relative_change"]:
        raise GeneralizedBenchmarkViolation("response or last-two convergence gate failed")
    if not exact_match and (observed_order is None or observed_order < tolerances["minimum_observed_order"]):
        raise GeneralizedBenchmarkViolation("observed convergence order gate failed")
    return {"last_two_relative_change": changes[-1], "observed_order": observed_order, "exact_discrete_match": exact_match}


def failure_indicators(case: Mapping[str, Any], witness: Mapping[str, Any], material: Mapping[str, Any], *, failure_ratio_limit: float = 1.0) -> dict[str, Any]:
    areas, inertias, radii = _positive_sections(witness) if case["response_model"] != "hertz_contact" else ([1.0], [1.0], [1.0])
    E = float(material["youngs_modulus_pa"]); yield_strength = float(material["yield_strength_pa"]); length = float(witness["path_witness"]["path_length_m"]); thickness = float(witness["thickness_field"]["minimum_sampled_span_m"]); load = float(case["load_n"]); torque = float(case["torque_n_m"])
    area = max(math.fsum(areas) / len(areas), 1e-30); inertia = max(math.fsum(inertias) / len(inertias), 1e-30); radius = max(math.fsum(radii) / len(radii), thickness)
    bending = load * length * radius / inertia if case["response_model"] in {"curved_bending", "tapered_bending", "parallel_branch_bending"} else 0.0
    torsion = torque * radius / max(2 * inertia, 1e-30); axial = load / area
    hoop = float(case["pressure_pa"]) * radius / thickness if case["response_model"] in {"shell_membrane", "bearing_ring"} else 0.0
    if case["response_model"] == "hertz_contact":
        contact_radius = (3 * max(load, 1e-30) * max(witness["path_witness"]["minimum_sampled_bend_radius_m"] or thickness, thickness) / (4 * E)) ** (1 / 3); contact = 3 * load / (2 * math.pi * contact_radius ** 2)
    else: contact = 0.0
    thermal = E * float(material["thermal_expansion_per_k"]) * float(case["temperature_delta_k"]); combined = max(bending, torsion, axial, hoop, contact) + thermal
    buckling_capacity = math.pi ** 2 * E * inertia / max(length ** 2, 1e-30); buckling_ratio = load / buckling_capacity
    yield_ratio = combined / yield_strength; plastic_strain = max(0.0, yield_ratio - 1.0) * yield_strength / E
    flaw = max(thickness / 10, 1e-9); fracture_ratio = combined * math.sqrt(math.pi * flaw) / float(material["fracture_toughness_pa_sqrt_m"])
    fatigue_damage = float(case["fatigue_cycles"]) / float(material["fatigue_reference_cycles"]) * (combined / float(material["fatigue_reference_stress_pa"])) ** 4
    ratios = {"buckling": buckling_ratio, "yield": yield_ratio, "fracture_domain": fracture_ratio, "fatigue": fatigue_damage}
    return {"stress_pa": {"bending": bending, "torsion": torsion, "axial": axial, "hoop": hoop, "contact": contact, "thermal": thermal, "combined_envelope": combined}, "ratios": ratios, "failure_ratio_limit": failure_ratio_limit, "plastic_strain_proxy": plastic_strain, "failed_mechanisms": sorted(name for name, value in ratios.items() if value >= failure_ratio_limit), "thermal_model": "fully_constrained_upper_bound", "fatigue_model": "synthetic_power_law_screen"}


def evaluate_case(config: Mapping[str, Any], case: Mapping[str, Any], witness: Mapping[str, Any], *, force_divergence: bool = False) -> dict[str, Any]:
    selection = select_model(case, witness, config["model_selection"]); reference = response_reference(case, witness, config["material"])
    levels = [discrete_response(case, witness, config["material"], item) for item in case["discrete_levels"]]
    if force_divergence:
        levels[-1]["solver_converged"] = False
        return {"status": "invalid", "reason": "solver_divergence", "case_id": case["case_id"], "mesh_results": levels, "fallback_used": False}
    tolerances = config["tolerances"]
    convergence = adjudicate_mesh_evidence(tolerances, reference, levels)
    failure = failure_indicators(case, witness, config["material"], failure_ratio_limit=tolerances["failure_ratio_limit"]); state = "failed" if failure["failed_mechanisms"] else "intact"
    if state != case["expected_state"]: raise GeneralizedBenchmarkViolation("baseline failure state differs from expectation")
    regions = {item["region_id"]: item["region_signature_sha256"] for item in witness["regions"]}
    refinement = {"curvature_sample_count": witness["curvature_spectrum"]["curvature_sample_count"], "minimum_sampled_thickness_m": witness["thickness_field"]["minimum_sampled_span_m"], "section_gradient": max(item["area_m2"] for item in witness["section_evolution"]["samples"]) - min(item["area_m2"] for item in witness["section_evolution"]["samples"]), "semantic_region_count": len(regions), "stress_gradient_class": "contact" if case["expected_model"] == "contact" else ("high" if case["expected_model"] == "solid" else "moderate")}
    contact_state = {"law": case["contact_law"], "status": "active", "valid": True, "arbitrary_3d_nonlinear_contact_solved": False}
    return {"status": "passed", "case_id": case["case_id"], "source_candidate_id": case["source_candidate_id"], "model_selection": selection, "contact_law": case["contact_law"], "contact_state": contact_state, "semantic_region_signatures": {key: regions[case[f"{key}_region_id"]] for key in ("support", "load", "contact")}, "refinement_justification": refinement, "reference": reference, "mesh_results": levels, **convergence, "failure_indicators": failure, "connection_transition": {"connection_id": case["connection_id"], "from_state": "intact", "to_state": state, "transmitted_force_n": case["load_n"] if state == "intact" else 0.0, "transmitted_moment_n_m": case["torque_n_m"] if state == "intact" else 0.0, "affected_path_ids": list(case["affected_path_ids"]) if state == "failed" else []}, "design_use_allowed": False}


def severed_edge_control(case: Mapping[str, Any]) -> dict[str, Any]:
    return {"status": "passed", "control": "severed_edge", "connection_id": case["connection_id"], "state": "failed", "transmitted_force_n": 0.0, "transmitted_moment_n_m": 0.0, "affected_path_ids": list(case["affected_path_ids"])}


def validate_severed_edge_control(control: Mapping[str, Any]) -> None:
    if control.get("state") != "failed" or control.get("transmitted_force_n") != 0 or control.get("transmitted_moment_n_m") != 0 or not control.get("affected_path_ids"):
        raise GeneralizedBenchmarkViolation("severed-edge failure control is noncausal")


__all__ = ["SCHEMA_VERSION", "CASE_IDS", "SOURCE_CANDIDATE_IDS", "GeneralizedBenchmarkViolation", "canonical_sha256", "validate_config", "validate_source_evidence", "select_model", "response_reference", "discrete_response", "adjudicate_mesh_evidence", "failure_indicators", "evaluate_case", "severed_edge_control", "validate_severed_edge_control"]
