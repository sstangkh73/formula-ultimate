from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.experiments.functional_discovery import (
    FunctionalDiscoveryViolation,
    TREATMENTS,
    assess_candidate,
    assess_process,
    build_treatment,
    treatment_matrix,
    unresolved_proxy_audit,
    validate_trial_config,
)
from formula_ultimate.experiments.discovery_registration import digest, validate_registration
from formula_ultimate.physics.functional_network_reference import evaluate_reference
from formula_ultimate.physics.functional_network_solver import FunctionalSolverViolation, evaluate_functional_network
from formula_ultimate.search.executable_morphology import GENOME_VERSION, functional_signature, root_genome, validate_genome


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/experiments/functional_discovery_trial_v1.json"
REGISTRATION = ROOT / "config/experiments/functional_discovery_registration_v2.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def parallel_genome(seed: int = 7) -> dict:
    return {
        "version": GENOME_VERSION,
        "genome_id": "parallel_fixture",
        "seed": seed,
        "parts": [{
            "part_id": "network",
            "material_id": "material_hypothesis_001",
            "nodes": [
                {"node_id": "source_node", "point_m": [0.0, 0.0, 0.0], "radius_m": 0.01},
                {"node_id": "upper", "point_m": [0.1, 0.05, 0.0], "radius_m": 0.01},
                {"node_id": "lower", "point_m": [0.1, -0.05, 0.0], "radius_m": 0.01},
                {"node_id": "sink_node", "point_m": [0.2, 0.0, 0.0], "radius_m": 0.01},
            ],
            "edges": [
                {"edge_id": "upper_a", "a": "source_node", "b": "upper"},
                {"edge_id": "upper_b", "a": "upper", "b": "sink_node"},
                {"edge_id": "lower_a", "a": "source_node", "b": "lower"},
                {"edge_id": "lower_b", "a": "lower", "b": "sink_node"},
            ],
        }],
        "interfaces": [],
        "terminals": [
            {"terminal_id": "source", "part_id": "network", "node_id": "source_node", "role": "source", "domains": ["load", "thermal"], "ancestry": ["external_source"]},
            {"terminal_id": "sink", "part_id": "network", "node_id": "sink_node", "role": "sink", "domains": ["load", "thermal"], "ancestry": ["external_sink"]},
        ],
        "controller": {"enabled": False, "gain": 1.0, "sensor_terminal_id": None, "actuator_terminal_id": None},
    }


class FunctionalNetworkSolverTests(unittest.TestCase):
    def test_constant_radius_parallel_network_matches_closed_form(self) -> None:
        config = load_config()
        genome = parallel_genome()
        validate_genome(genome, config["representation_limits"])
        result = evaluate_functional_network(genome, config["representation_limits"], config["material"], config["training_task"], [1, 2, 4])
        length = math.dist([0.0, 0.0, 0.0], [0.1, 0.05, 0.0]) * 2.0
        area = math.pi * 0.01 ** 2
        expected_displacement = config["training_task"]["force_n"] * (length / (config["material"]["youngs_modulus_pa"] * area)) / 2.0
        expected_temperature = config["training_task"]["heat_w"] * (length / (config["material"]["thermal_conductivity_w_per_m_k"] * area)) / 2.0
        self.assertAlmostEqual(expected_displacement, result["fine"]["maximum_displacement_m"], places=14)
        self.assertAlmostEqual(expected_temperature, result["fine"]["maximum_temperature_rise_k"], places=10)
        self.assertLess(result["maximum_conservation_residual"], 1e-12)
        self.assertLess(result["last_two_relative_change"], 1e-12)

    def test_midpoint_refinement_converges_to_separate_exact_radius_reference(self) -> None:
        config = load_config()
        genome = root_genome(7)
        result = evaluate_functional_network(genome, config["representation_limits"], config["material"], config["training_task"], config["refinement_levels"])
        reference = evaluate_reference(genome, config["representation_limits"], config["material"], config["training_task"])
        for key in ("coupled_utilization_ratio", "maximum_displacement_m", "maximum_axial_stress_pa", "maximum_temperature_rise_k"):
            error = abs(result["fine"][key] - reference[key]) / max(abs(reference[key]), 1e-30)
            self.assertLess(error, config["tolerances"]["maximum_reference_relative_error"], key)
        self.assertLess(result["last_two_relative_change"], config["tolerances"]["maximum_refinement_relative_change"])
        self.assertLess(result["maximum_conservation_residual"], config["tolerances"]["maximum_conservation_residual"])

    def test_fields_reactions_energy_and_vehicle_feedback_are_observable(self) -> None:
        config = load_config()
        result = evaluate_functional_network(root_genome(7), config["representation_limits"], config["material"], config["training_task"], config["refinement_levels"])
        fine = result["levels"][-1]
        for field, applied in (("mechanical_field", config["training_task"]["force_n"]), ("thermal_field", config["training_task"]["heat_w"])):
            evidence = fine[field]
            self.assertAlmostEqual(-applied, evidence["source_reaction"], places=8)
            self.assertLess(evidence["free_residual_relative"], 1e-10)
            self.assertLess(evidence["equilibrium_residual_relative"], 1e-10)
            self.assertLess(evidence["energy_residual_relative"], 1e-10)
            self.assertTrue(evidence["values"])
            self.assertTrue(evidence["segments"])
        self.assertGreater(result["geometry_derived_mass_kg"], 0.0)
        self.assertIn("mass_fraction_of_reference_vehicle", result["vehicle_feedback"])
        self.assertFalse(result["vehicle_feedback"]["controller_gain_observed_not_causal"] == 0.0)

    def test_unsupported_interface_is_numerical_applicability_failure_not_physical_failure(self) -> None:
        config = load_config()
        genome = root_genome(7)
        genome["interfaces"][0]["kind"] = "revolute"
        genome["interfaces"][0]["domains"] = ["load", "motion"]
        with self.assertRaisesRegex(FunctionalSolverViolation, "only fixed"):
            evaluate_functional_network(genome, config["representation_limits"], config["material"], config["training_task"], config["refinement_levels"])

    def test_stricter_physical_limit_returns_measured_failure_with_fields(self) -> None:
        config = load_config()
        task = deepcopy(config["training_task"])
        task["maximum_temperature_rise_k"] = 1.0
        result = evaluate_functional_network(root_genome(7), config["representation_limits"], config["material"], task, config["refinement_levels"])
        self.assertEqual("physically_failed", result["status"])
        self.assertEqual("temperature", result["failure_component"])
        self.assertTrue(result["levels"][-1]["thermal_field"]["segments"])


class FunctionalDiscoveryProtocolTests(unittest.TestCase):
    def test_registration_is_valid_and_binds_final_sources_and_profiles(self) -> None:
        config = load_config()
        registration = json.loads(REGISTRATION.read_text(encoding="utf-8"))
        body = validate_registration(registration)
        evaluators = {item["id"]: item for item in body["evaluators"]}
        file_hash = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual("admitted_simulation", body["evidence_class"])
        self.assertEqual(file_hash(ROOT / "src/formula_ultimate/physics/functional_network_solver.py"), evaluators["axial_thermal_primary"]["implementation_sha256"])
        self.assertEqual(file_hash(ROOT / "src/formula_ultimate/physics/functional_network_reference.py"), evaluators["axial_thermal_reference"]["implementation_sha256"])
        self.assertEqual(file_hash(Path(__file__)), evaluators["axial_thermal_primary"]["validation_sha256"])
        self.assertEqual(digest({
            "trial_sha256": digest(config),
            "experiment_implementation_sha256": file_hash(ROOT / "src/formula_ultimate/experiments/functional_discovery.py"),
            "runner_sha256": file_hash(ROOT / "scripts/experiments/run_functional_discovery.py"),
        }), body["profiles"]["operator_library_sha256"])
        self.assertEqual(digest({"training": config["training_task"], "holdout": config["holdout_task"]}), body["profiles"]["task_sha256"])
        self.assertEqual(config["claim_boundary"]["survivor_scope"], body["promotion_scope"])
        self.assertNotIn("safety_margin", body["survivor_gates"])
        self.assertIn("safety_margin", body["promotion_gates"])
        self.assertIn("independent_exact", body["promotion_gates"])

    def test_trial_config_freezes_scope_treatments_partitions_and_thresholds(self) -> None:
        config = load_config()
        result = validate_trial_config(config)
        self.assertEqual("passed", result["status"])
        self.assertEqual(5, result["treatment_count"])
        self.assertEqual(2, result["seed_count"])
        self.assertNotEqual(config["training_task"]["dataset_id"], config["holdout_task"]["dataset_id"])
        self.assertIn("physical_validation", config["claim_boundary"]["prohibited_claims"])

    def test_treatment_matrix_is_deterministic_paired_and_causally_distinct(self) -> None:
        config = load_config()
        first, second = treatment_matrix(config), treatment_matrix(config)
        self.assertEqual(first, second)
        self.assertEqual(len(TREATMENTS) * len(config["seeds"]), len(first))
        self.assertEqual({(t, s) for t in TREATMENTS for s in config["seeds"]}, {(row["treatment"], row["seed"]) for row in first})
        for seed in config["seeds"]:
            rows = {row["treatment"]: row for row in first if row["seed"] == seed}
            self.assertNotEqual(rows["FIXED_TOPOLOGY"]["genotype_sha256"], rows["MORPHOLOGY_ONLY"]["genotype_sha256"])
            self.assertNotEqual(rows["FIXED_TOPOLOGY"]["functional_signature"], rows["GRAPH_ONLY"]["functional_signature"])

    def test_controller_gene_has_no_hidden_task_or_energy_advantage(self) -> None:
        config = load_config()
        for seed in config["seeds"]:
            graph = build_treatment(config, "GRAPH_ONLY", seed)["genome"]
            joint = build_treatment(config, "JOINT_MORPHOLOGY_CONTROLLER", seed)["genome"]
            graph_result = assess_candidate(config, graph, "training_task")
            joint_result = assess_candidate(config, joint, "training_task")
            self.assertEqual(graph_result["value"], joint_result["value"])
            self.assertNotEqual(graph["controller"]["gain"], joint["controller"]["gain"])

    def test_all_treatments_return_scoped_training_and_holdout_evidence(self) -> None:
        config = load_config()
        statuses = set()
        for row in treatment_matrix(config):
            training = assess_candidate(config, row["genome"], "training_task")
            holdout = assess_candidate(config, row["genome"], "holdout_task")
            statuses.update((training["status"], holdout["status"]))
            self.assertTrue(training["numerical_pass"])
            self.assertTrue(holdout["numerical_pass"])
            self.assertLessEqual(training["error"], config["tolerances"]["maximum_reference_relative_error"])
            self.assertNotEqual(training["dataset_id"], holdout["dataset_id"])
        self.assertTrue(statuses <= {"physically_feasible", "physically_failed"})

    def test_process_envelope_is_measured_and_can_fail_without_erasing_physics(self) -> None:
        config = load_config()
        genome = root_genome(7)
        passed = assess_process(config, genome)
        self.assertEqual("manufacturing_compatible", passed["status"])
        changed = deepcopy(config)
        changed["process"]["minimum_diameter_m"] = 0.1
        failed = assess_process(changed, genome)
        self.assertEqual("manufacturing_incompatible", failed["status"])
        self.assertGreater(failed["process_violation_ratio"], 1.0)

    def test_task_material_and_claim_tampering_fail_validation(self) -> None:
        config = load_config()
        changed = deepcopy(config)
        changed["holdout_task"]["dataset_id"] = changed["training_task"]["dataset_id"]
        with self.assertRaisesRegex(FunctionalDiscoveryViolation, "distinct"):
            validate_trial_config(changed)
        changed = deepcopy(config)
        changed["material"]["model_scope"] = "validated_real_material"
        with self.assertRaisesRegex(FunctionalDiscoveryViolation, "scope"):
            validate_trial_config(changed)
        changed = deepcopy(config)
        changed["claim_boundary"]["prohibited_claims"].remove("physical_validation")
        with self.assertRaisesRegex(FunctionalDiscoveryViolation, "boundary"):
            validate_trial_config(changed)

    def test_candidate_task_ancestry_and_material_are_bound_to_registration(self) -> None:
        config = load_config()
        wrong_ancestry = root_genome(7)
        wrong_ancestry["terminals"][0]["ancestry"] = ["unregistered_source"]
        with self.assertRaisesRegex(FunctionalDiscoveryViolation, "ancestry"):
            assess_candidate(config, wrong_ancestry, "training_task")
        wrong_material = root_genome(7)
        wrong_material["parts"][0]["material_id"] = "undeclared_material"
        with self.assertRaisesRegex(FunctionalDiscoveryViolation, "material identity"):
            assess_candidate(config, wrong_material, "training_task")

    def test_unresolved_proxy_audit_preserves_unknown_labels(self) -> None:
        selection = {
            "selection_sha256": "1" * 64,
            "population": [
                {"candidate_id": "a", "proxy_score": None},
                {"candidate_id": "b", "proxy_score": 0.5},
            ],
            "selection": {"selected": [{"candidate_id": "a"}, {"candidate_id": "b"}]},
        }
        report = unresolved_proxy_audit(selection, {
            "a": {"status": "physically_feasible"},
            "b": {"status": "physically_failed"},
        })
        self.assertEqual("not_estimable_due_to_unresolved_proxy_labels", report["status"])
        self.assertEqual(1, report["proxy_unresolved_count"])
        self.assertEqual(1, report["proxy_boolean_count"])
        self.assertIsNone(report["false_negative_rate"])
        self.assertIsNone(report["false_positive_rate"])


if __name__ == "__main__":
    unittest.main()
