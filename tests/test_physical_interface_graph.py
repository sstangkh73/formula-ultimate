from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from formula_ultimate.assembly.physical_interface_graph import (
    PhysicalInterfaceViolation,
    canonical_identity,
    spatial_region_index,
    transfer_bindings,
    validate_graph,
    validate_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/development/physical_interface_graph_v1.json"
SPATIAL = ROOT / "config/development/spatial_material_v1.json"


class PhysicalInterfaceGraphTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads(CONFIG.read_text(encoding="utf-8")); self.spatial = json.loads(SPATIAL.read_text(encoding="utf-8")); self.regions = spatial_region_index(self.spatial); self.graph = self.raw["graph"]

    def identity(self, graph):
        return canonical_identity(graph, self.regions, self.raw["limits"]["maximum_terminals"])["identity_sha256"]

    def test_protocol_and_multiedge_connectivity(self):
        self.assertEqual(validate_protocol(self.raw, self.spatial)["status"], "passed")
        report = validate_graph(self.graph, self.regions, self.raw)
        self.assertEqual(report["parallel_edge_count"], 1); self.assertEqual(report["connected_component_count"], 3); self.assertEqual(report["maximum_exchange_residual"], 0.0)

    def test_identifier_only_rename_preserves_identity(self):
        renamed = copy.deepcopy(self.graph); mapping = {t["terminal_id"]: f"renamed_{i}" for i,t in enumerate(renamed["terminals"])}
        for i,terminal in enumerate(renamed["terminals"]): terminal["terminal_id"] = mapping[terminal["terminal_id"]]; terminal["owner_id"] = f"group_{i}"
        for i,edge in enumerate(renamed["edges"]): edge["edge_id"] = f"edge_{i}"; edge["terminals"] = [mapping[x] for x in edge["terminals"]]
        self.assertEqual(self.identity(self.graph), self.identity(renamed))

    def test_direction_multiplicity_and_owner_partition_are_distinct(self):
        deleted=copy.deepcopy(self.graph); deleted["edges"].pop(1)
        regrouped=copy.deepcopy(self.graph); regrouped["terminals"][1]["owner_id"] = regrouped["terminals"][0]["owner_id"]
        reversed_graph=copy.deepcopy(self.graph); reversed_graph["terminals"][0]["role"]="sink"; reversed_graph["terminals"][1]["role"]="source"
        for edge in reversed_graph["edges"][:2]: edge["direction"]="b_to_a"
        baseline=self.identity(self.graph)
        self.assertNotEqual(baseline,self.identity(deleted)); self.assertNotEqual(baseline,self.identity(regrouped)); self.assertNotEqual(baseline,self.identity(reversed_graph))

    def test_incompatible_units_surfaces_motion_and_exchange_fail_closed(self):
        fixtures=[]
        unit=copy.deepcopy(self.graph); unit["terminals"][1]["unit"]="kN"; fixtures.append((unit,"unit"))
        surface=copy.deepcopy(self.graph); surface["terminals"][1]["region_binding"]["surface_id"]=""; fixtures.append((surface,"missing mating surface"))
        motion=copy.deepcopy(self.graph); motion["terminals"][3]["allowed_motion"]="revolute"; fixtures.append((motion,"rigid/moving"))
        exchange=copy.deepcopy(self.graph); exchange["edges"][0]["exchange"][1]=-119.0; fixtures.append((exchange,"conservation"))
        for graph, phrase in fixtures:
            with self.subTest(phrase=phrase), self.assertRaisesRegex(PhysicalInterfaceViolation,phrase): validate_graph(graph,self.regions,self.raw)

    def test_split_transfer_invalidates_and_ambiguity_is_not_silent(self):
        clear=transfer_bindings(self.graph,self.raw["transfer_fixtures"]["unambiguous_split"]); ambiguous=transfer_bindings(self.graph,self.raw["transfer_fixtures"]["ambiguous_split"])
        self.assertEqual(clear["events"][0]["reason"],"spatial binding changed; dependent evidence must be recomputed")
        self.assertEqual(clear["graph"]["terminals"][0]["region_binding"]["region_id"],"branch_left")
        self.assertIn("ambiguous",ambiguous["events"][0]["reason"]); self.assertEqual(ambiguous["graph"]["terminals"][0]["region_binding"]["region_id"],"branch_body")

    def test_oversize_identity_is_explicitly_unresolved(self):
        oversize=copy.deepcopy(self.graph)
        while len(oversize["terminals"]) <= self.raw["limits"]["maximum_terminals"]:
            clone=copy.deepcopy(oversize["terminals"][0]); clone["terminal_id"]=f"extra_{len(oversize['terminals'])}"; oversize["terminals"].append(clone)
        result=canonical_identity(oversize,self.regions,self.raw["limits"]["maximum_terminals"]); self.assertEqual(result["status"],"unresolved")


if __name__ == "__main__": unittest.main()
