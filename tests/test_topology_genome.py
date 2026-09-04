from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from formula_ultimate.search.topology_genome import (
    DOMAINS,
    TopologyGenomeError,
    canonical_topology_signature,
    declaration_sha256,
    validate_topology_corpus,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/genomes/typed_morphology_topology_genome_v1.json"
SOLID_CONFIG = ROOT / "config/cad/freeform_brep_solid_grammar_v2.json"


def load_genomes() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def solid_candidates() -> dict[str, str]:
    raw = json.loads(SOLID_CONFIG.read_text(encoding="utf-8"))
    return {item["candidate_id"]: item["family"] for item in raw["candidates"]}


def reverse_mappings(value):
    if isinstance(value, dict): return {key: reverse_mappings(item) for key, item in reversed(tuple(value.items()))}
    if isinstance(value, list): return [reverse_mappings(item) for item in value]
    return value


def renamed(genome: dict) -> dict:
    ready = deepcopy(genome)
    part_map = {part["part_id"]: f"renamed_part_{index}" for index, part in enumerate(ready["parts"])}
    interface_map = {item["interface_id"]: f"renamed_interface_{index}" for index, item in enumerate(ready["interfaces"])}
    terminal_map = {item["terminal_id"]: f"renamed_terminal_{index}" for index, item in enumerate(ready["terminals"])}
    for part in ready["parts"]:
        old_part = part["part_id"]; part["part_id"] = part_map[old_part]
        if part["parent_part_id"] is not None: part["parent_part_id"] = part_map[part["parent_part_id"]]
        feature_map = {item["feature_id"]: f"renamed_feature_{index}" for index, item in enumerate(part["features"])}
        for feature in part["features"]:
            old_feature = feature["feature_id"]; feature["feature_id"] = feature_map[old_feature]; feature["inputs"] = [feature_map[item] for item in feature["inputs"]]
        part["final_feature_id"] = feature_map[part["final_feature_id"]]
    for interface in ready["interfaces"]:
        old = interface["interface_id"]; interface["interface_id"] = interface_map[old]
        interface["part_a"] = part_map[interface["part_a"]]; interface["part_b"] = part_map[interface["part_b"]]
    for terminal in ready["terminals"]:
        old = terminal["terminal_id"]; terminal["terminal_id"] = terminal_map[old]; terminal["part_id"] = part_map[terminal["part_id"]]
    for path in ready["paths"]:
        path["path_id"] = "renamed_" + path["path_id"]
        path["terminal_ids"] = [terminal_map[item] for item in path["terminal_ids"]]
        path["part_ids"] = [part_map[item] for item in path["part_ids"]]
        path["interface_ids"] = [interface_map[item] for item in path["interface_ids"]]
    return ready


class TopologyGenomeTests(unittest.TestCase):
    def test_corpus_has_six_nonisomorphic_graphs_and_five_part_counts(self) -> None:
        result = validate_topology_corpus(load_genomes(), solid_candidates())
        self.assertEqual("passed", result["status"])
        self.assertEqual(6, result["genome_count"])
        self.assertEqual([1, 3, 4, 5, 6], result["distinct_part_counts"])
        self.assertEqual(6, result["unique_topology_signature_count"])
        self.assertTrue(any(item["branch_part_count"] > 0 for item in result["descriptors"]))
        self.assertTrue(any(item["interface_cycle_rank"] > 0 for item in result["descriptors"]))

    def test_key_order_and_consistent_identifier_rename_preserve_identity(self) -> None:
        raw = load_genomes()
        self.assertEqual(declaration_sha256(raw), declaration_sha256(reverse_mappings(raw)))
        for genome in raw["genomes"]:
            with self.subTest(genome=genome["genome_id"]):
                self.assertEqual(canonical_topology_signature(genome), canonical_topology_signature(renamed(genome)))

    def test_reroute_and_feature_dependency_change_topology_signature(self) -> None:
        genome = load_genomes()["genomes"][3]
        rerouted = deepcopy(genome); rerouted["paths"][0]["domains"] = ["load", "motion"]
        rerouted["paths"][1]["domains"] = ["energy", "fluid", "thermal", "control"]
        self.assertNotEqual(canonical_topology_signature(genome), canonical_topology_signature(rerouted))
        changed = deepcopy(genome); changed["parts"][0]["features"][-1]["inputs"].append("section")
        self.assertNotEqual(canonical_topology_signature(genome), canonical_topology_signature(changed))

    def test_parent_cycle_and_forward_feature_reference_fail_closed(self) -> None:
        raw = load_genomes(); genome = raw["genomes"][1]
        genome["parts"][0]["parent_part_id"] = "converter"; genome["parts"][1]["parent_part_id"] = "input"
        with self.assertRaisesRegex(TopologyGenomeError, "containment cycle"):
            validate_topology_corpus(raw, solid_candidates())
        raw = load_genomes(); raw["genomes"][0]["parts"][0]["features"][0]["inputs"] = ["body"]
        with self.assertRaisesRegex(TopologyGenomeError, "earlier features"):
            validate_topology_corpus(raw, solid_candidates())

    def test_orphan_terminal_missing_domain_and_disconnected_route_fail_closed(self) -> None:
        raw = load_genomes(); raw["genomes"][2]["paths"].pop()
        with self.assertRaisesRegex(TopologyGenomeError, "not traceable"):
            validate_topology_corpus(raw, solid_candidates())
        raw = load_genomes(); raw["required_domains"] = list(DOMAINS[:-1])
        with self.assertRaisesRegex(TopologyGenomeError, "required domain set"):
            validate_topology_corpus(raw, solid_candidates())
        raw = load_genomes(); raw["genomes"][1]["paths"][0]["interface_ids"][0] = "converter_to_output"
        with self.assertRaisesRegex(TopologyGenomeError, "disconnected"):
            validate_topology_corpus(raw, solid_candidates())

    def test_duplicate_self_interface_bad_dof_and_unknown_field_fail_closed(self) -> None:
        raw = load_genomes(); raw["genomes"][1]["interfaces"][0]["part_b"] = "input"
        with self.assertRaisesRegex(TopologyGenomeError, "self"):
            validate_topology_corpus(raw, solid_candidates())
        raw = load_genomes(); raw["genomes"][1]["interfaces"][0]["allowed_dof"] = ["teleport"]
        with self.assertRaisesRegex(TopologyGenomeError, "DOF"):
            validate_topology_corpus(raw, solid_candidates())
        raw = load_genomes(); raw["genomes"][0]["legacy_scalar_parameters"] = [1, 2, 3, 4, 5]
        with self.assertRaisesRegex(TopologyGenomeError, "schema mismatch"):
            validate_topology_corpus(raw, solid_candidates())

    def test_solid_identity_and_symmetry_misuse_fail_closed(self) -> None:
        raw = load_genomes(); raw["genomes"][0]["parts"][0]["solid_family"] = "wrong_family"
        with self.assertRaisesRegex(TopologyGenomeError, "solid candidate and family"):
            validate_topology_corpus(raw, solid_candidates())
        raw = load_genomes(); raw["genomes"][0]["symmetry"] = {"mode": "none", "axis": "x", "order": 2}
        with self.assertRaisesRegex(TopologyGenomeError, "hidden prior"):
            validate_topology_corpus(raw, solid_candidates())


if __name__ == "__main__":
    unittest.main()
