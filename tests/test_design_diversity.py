from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from formula_ultimate.experiments.design_diversity import (
    DesignDiversityError, describe_candidate, load_sources, summarize_census,
    validate_config,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/experiments/design_diversity_v1.json"
BASE = ROOT / "config/vehicle/topology_neutral_vehicle_v1.json"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rename(raw: dict) -> dict:
    value = deepcopy(raw)
    component_map = {item["component_id"]: f"renamed_component_{i}" for i, item in enumerate(value["components"])}
    interface_map = {item["interface_id"]: f"renamed_interface_{i}" for i, item in enumerate(value["interfaces"])}
    for item in value["components"]: item["component_id"] = component_map[item["component_id"]]
    for item in value["interfaces"]:
        item["component_id"] = component_map[item["component_id"]]; item["interface_id"] = interface_map[item["interface_id"]]
    for item in value["connections"]:
        item["connection_id"] = "renamed_" + item["connection_id"]
        item["interface_a"] = interface_map[item["interface_a"]]; item["interface_b"] = interface_map[item["interface_b"]]
    for item in value["contacts"]:
        item["contact_id"] = "renamed_" + item["contact_id"]; item["interface_id"] = interface_map[item["interface_id"]]
    value["energy_edges"] = [[component_map[a], component_map[b]] for a, b in value["energy_edges"]]
    value["external_load_components"] = [component_map[item] for item in value["external_load_components"]]
    return value


def scale_translate_rotate(raw: dict) -> dict:
    value = deepcopy(raw)
    def transform(vector): return [3.0 * (-vector[1]) + 4.0, 3.0 * vector[0] - 2.0, 3.0 * vector[2] + 1.0]
    def local(vector): return [3.0 * (-vector[1]), 3.0 * vector[0], 3.0 * vector[2]]
    for item in value["components"]:
        item["translation_m"] = transform(item["translation_m"])
        primitive = item["primitive"]
        if primitive["type"] == "box": primitive["size_m"] = [3.0 * primitive["size_m"][1], 3.0 * primitive["size_m"][0], 3.0 * primitive["size_m"][2]]
        else:
            primitive["radius_m"] *= 3.0; primitive["height_m"] *= 3.0
    for item in value["interfaces"]: item["local_position_m"] = local(item["local_position_m"])
    return value


class DesignDiversityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read(CONFIG); cls.base = read(BASE); cls.reference = describe_candidate(cls.base)

    def test_config_and_source_identities(self):
        self.assertEqual(validate_config(self.config)["status"], "passed")
        self.assertEqual(set(load_sources(ROOT, self.config)), set(self.config["sources"]))

    def test_unknown_config_field_fails(self):
        config = deepcopy(self.config); config["unknown"] = 1
        with self.assertRaisesRegex(DesignDiversityError, "schema"):
            validate_config(config)

    def test_renaming_is_invariant(self):
        changed = describe_candidate(rename(self.base))
        self.assertEqual(self.reference["topology_signature"], changed["topology_signature"])
        self.assertEqual(self.reference["geometry_signature"], changed["geometry_signature"])

    def test_translation_axis_change_and_scale_are_invariant(self):
        changed = describe_candidate(scale_translate_rotate(self.base))
        self.assertEqual(self.reference["topology_signature"], changed["topology_signature"])
        self.assertEqual(self.reference["geometry_signature"], changed["geometry_signature"])

    def test_branch_addition_changes_topology(self):
        changed = deepcopy(self.base)
        changed["components"].append({"component_id":"branch","function_tags":["branch"],"material_id":"light","primitive":{"type":"box","size_m":[0.02,0.02,0.02]},"translation_m":[0.0,-0.1,0.15]})
        changed["interfaces"].append({"interface_id":"branch_i","component_id":"branch","local_position_m":[0,0,0]})
        changed["connections"].append({"connection_id":"branch_c","interface_a":"core_support","interface_b":"branch_i"})
        self.assertNotEqual(self.reference["topology_signature"], describe_candidate(changed)["topology_signature"])

    def test_connectivity_reroute_changes_topology(self):
        changed = deepcopy(self.base); changed["connections"][2]["interface_a"] = "source_out"
        self.assertNotEqual(self.reference["topology_signature"], describe_candidate(changed)["topology_signature"])

    def test_primitive_family_changes_geometry_not_topology(self):
        changed = deepcopy(self.base); changed["components"][0]["primitive"] = {"type":"cylinder_z","radius_m":0.1,"height_m":0.4}
        descriptor = describe_candidate(changed)
        self.assertEqual(self.reference["topology_signature"], descriptor["topology_signature"])
        self.assertNotEqual(self.reference["geometry_signature"], descriptor["geometry_signature"])

    def test_interface_topology_change_is_detected(self):
        changed = deepcopy(self.base); changed["connections"].pop()
        self.assertNotEqual(self.reference["topology_signature"], describe_candidate(changed)["topology_signature"])

    def test_non_finite_geometry_fails(self):
        changed = deepcopy(self.base); changed["components"][0]["translation_m"][0] = float("nan")
        with self.assertRaisesRegex(DesignDiversityError, "finite"):
            describe_candidate(changed)

    def test_census_count_fails_closed(self):
        with self.assertRaisesRegex(DesignDiversityError, "attempt count"):
            summarize_census([], 288)


if __name__ == "__main__":
    unittest.main()
