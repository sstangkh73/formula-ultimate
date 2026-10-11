from __future__ import annotations

import hashlib
import json
import math
import unittest
from dataclasses import replace

from formula_ultimate.hierarchy.part_tree import (
    AssemblyNode,
    Interface,
    PartNode,
    PartTree,
    PartTreeViolation,
    canonical_sha256,
    leaf_ids,
    levels,
    roll_up,
    subtree_height,
    subtree_leaves,
    to_manifest_interfaces,
    to_manifest_nodes,
    topology_signature,
    validate_part_tree,
)


def make_part(part_id: str, mass_kg: float, x_m: float) -> PartNode:
    return PartNode(
        id=part_id,
        mesh=f"meshes/{part_id}.obj",
        material_id="steel",
        density_kg_m3=7800.0,
        mass_kg=mass_kg,
        center_of_mass_m=(x_m, 1.0, -x_m),
        grammar_version="grammar-v1",
        program={"primitive": "box", "part": part_id},
    )


def make_valid_tree() -> PartTree:
    parts = tuple(make_part(f"p{i}", float(i), float(i - 1)) for i in range(1, 7))
    nodes = parts + (
        AssemblyNode("sa1", ("p1", "p2"), ("support",)),
        AssemblyNode("sa2", ("p3",), ("support",)),
        AssemblyNode("sb1", ("p4", "p5"), ("drive",)),
        AssemblyNode("sb2", ("p6",), ("drive",)),
        AssemblyNode("subsystem-a", ("sa1", "sa2"), ("front",)),
        AssemblyNode("subsystem-b", ("sb1", "sb2"), ("rear",)),
        AssemblyNode("root", ("subsystem-a", "subsystem-b"), ("vehicle",)),
    )
    interfaces = (
        Interface("i12", "p1", "p2", "threaded"),
        Interface("i34", "p3", "p4", "interference", 1e-5),
    )
    return PartTree("root", nodes, interfaces, 1e-4)


def make_tree(
    nodes: tuple[PartNode | AssemblyNode, ...],
    *,
    root: str = "root",
    interfaces: tuple[Interface, ...] = (),
    tolerance: float = 1e-4,
) -> PartTree:
    return PartTree(root, nodes, interfaces, tolerance)


class PartTreeTests(unittest.TestCase):
    def test_valid_four_level_tree_and_metrics(self) -> None:
        tree = make_valid_tree()

        validate_part_tree(tree)
        self.assertEqual(4, levels(tree))
        self.assertEqual(("p1", "p2", "p3", "p4", "p5", "p6"), leaf_ids(tree))
        self.assertEqual(3, subtree_height(tree, "root"))
        self.assertEqual(2, subtree_height(tree, "subsystem-a"))
        self.assertEqual(0, subtree_height(tree, "p1"))
        self.assertEqual(frozenset({"p1", "p2", "p3"}), subtree_leaves(tree, "subsystem-a"))
        self.assertEqual(frozenset({"p6"}), subtree_leaves(tree, "sb2"))

    def test_roll_up_uses_child_order_and_mass_weighted_com(self) -> None:
        rolled = roll_up(make_valid_tree())

        self.assertAlmostEqual(21.0, rolled["root"][0])
        self.assertAlmostEqual(70.0 / 21.0, rolled["root"][1][0])
        self.assertAlmostEqual(1.0, rolled["root"][1][1])
        self.assertAlmostEqual(-70.0 / 21.0, rolled["root"][1][2])
        self.assertEqual((6.0, (5.0, 1.0, -5.0)), rolled["p6"])
        self.assertAlmostEqual(6.0, rolled["subsystem-a"][0])
        self.assertAlmostEqual(4.0 / 3.0, rolled["subsystem-a"][1][0])

    def test_topology_signature_is_exact_and_child_order_independent(self) -> None:
        leaf_a = make_part("a", 1.0, 0.0)
        leaf_b = make_part("b", 1.0, 0.0)
        leaf_c = make_part("c", 1.0, 0.0)
        tree = make_tree(
            (
                leaf_a,
                leaf_b,
                leaf_c,
                AssemblyNode("branch", ("a", "b"), ("b",)),
                AssemblyNode("root", ("branch", "c"), ("z", "a")),
            )
        )
        reordered = replace(
            tree,
            nodes=(
                leaf_a,
                leaf_b,
                leaf_c,
                AssemblyNode("branch", ("b", "a"), ("b",)),
                AssemblyNode("root", ("c", "branch"), ("a", "z")),
            ),
        )
        different_shape = make_tree(
            (leaf_a, leaf_b, leaf_c, AssemblyNode("root", ("a", "b", "c"), ("a", "z")))
        )

        self.assertEqual("(a,z:(b:LL)L)", topology_signature(tree, "root"))
        self.assertEqual(topology_signature(tree, "root"), topology_signature(reordered, "root"))
        self.assertNotEqual(topology_signature(tree, "root"), topology_signature(different_shape, "root"))

    def test_manifests_have_exact_fields_and_declared_order(self) -> None:
        tree = make_valid_tree()
        nodes = to_manifest_nodes(tree)
        interfaces = to_manifest_interfaces(tree)

        self.assertEqual("root", nodes[0]["id"])
        self.assertEqual(
            {"id", "kind", "children", "functions", "mass_kg", "center_of_mass_m"},
            set(nodes[0]),
        )
        part = next(item for item in nodes if item["id"] == "p1")
        self.assertEqual(
            {
                "id",
                "kind",
                "mesh",
                "material_id",
                "density_kg_m3",
                "mass_kg",
                "center_of_mass_m",
                "generator",
            },
            set(part),
        )
        self.assertEqual(
            {"grammar_version", "program", "program_sha256"}, set(part["generator"])
        )
        self.assertEqual({"id", "a", "b", "kind"}, set(interfaces[0]))
        self.assertEqual(
            {"id", "a", "b", "kind", "interference_m"}, set(interfaces[1])
        )
        self.assertEqual(["root", "subsystem-a", "sa1", "p1", "p2", "sa2", "p3", "subsystem-b", "sb1", "p4", "p5", "sb2", "p6"], [item["id"] for item in nodes])
        self.assertEqual(["i12", "i34"], [item["id"] for item in interfaces])

    def test_program_sha256_matches_independent_hashlib_computation(self) -> None:
        program = {"z": ["ไทย", 2], "a": {"enabled": True}}
        part = replace(make_part("p", 1.0, 0.0), program=program)
        encoded = json.dumps(
            program,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
        expected = hashlib.sha256(encoded).hexdigest()

        self.assertEqual(expected, part.program_sha256)
        self.assertEqual(expected, canonical_sha256(program))
        self.assertIs(program, part.program)

    def test_deep_chain_is_iterative(self) -> None:
        child_id = "deep-part"
        nodes: list[PartNode | AssemblyNode] = [make_part(child_id, 1.0, 0.0)]
        for index in reversed(range(2999)):
            node_id = f"a{index}"
            nodes.append(AssemblyNode(node_id, (child_id,), ()))
            child_id = node_id
        tree = make_tree(tuple(nodes), root="a0")

        self.assertEqual(3000, levels(tree))
        self.assertEqual(3000, len(roll_up(tree)))
        signature = topology_signature(tree, "a0")
        self.assertEqual("(:" * 2999 + "L" + ")" * 2999, signature)

    def assert_invalid(self, tree: PartTree) -> None:
        with self.assertRaises(PartTreeViolation):
            validate_part_tree(tree)

    def test_invalid_ids_and_node_structure(self) -> None:
        base = make_valid_tree()
        self.assert_invalid(replace(base, root=""))
        self.assert_invalid(replace(base, root=1))
        self.assert_invalid(replace(base, root="missing"))
        self.assert_invalid(replace(base, root="p1"))
        self.assert_invalid(replace(base, nodes=base.nodes + (make_part("", 1.0, 0.0),)))
        self.assert_invalid(
            replace(base, nodes=base.nodes + (make_part("p1", 1.0, 0.0),))
        )
        self.assert_invalid(
            make_tree((AssemblyNode("root", ("missing",), ("vehicle",)),))
        )
        self.assert_invalid(make_tree((AssemblyNode("root", (), ("vehicle",)),)))

    def test_invalid_parent_and_graph_relationships(self) -> None:
        p = make_part("p", 1.0, 0.0)
        self.assert_invalid(make_tree((p, AssemblyNode("root", ("p", "p"), ("vehicle",)))))
        self.assert_invalid(
            make_tree(
                (
                    p,
                    AssemblyNode("root", ("a", "b"), ("vehicle",)),
                    AssemblyNode("a", ("p",), ("a",)),
                    AssemblyNode("b", ("p",), ("b",)),
                )
            )
        )
        self.assert_invalid(
            make_tree(
                (
                    p,
                    AssemblyNode("root", ("a",), ("vehicle",)),
                    AssemblyNode("a", ("root",), ("a",)),
                )
            )
        )
        with self.assertRaisesRegex(PartTreeViolation, "cycle"):
            validate_part_tree(
                make_tree(
                    (
                        p,
                        AssemblyNode("root", ("p",), ("vehicle",)),
                        AssemblyNode("a", ("b",), ("a",)),
                        AssemblyNode("b", ("a",), ("b",)),
                    )
                )
            )
        self.assert_invalid(
            make_tree(
                (
                    p,
                    make_part("unreachable", 1.0, 0.0),
                    AssemblyNode("root", ("p",), ("vehicle",)),
                )
            )
        )

    def test_invalid_part_properties(self) -> None:
        base = make_valid_tree()
        p1 = next(node for node in base.nodes if node.id == "p1")
        for change in (
            {"density_kg_m3": 0.0},
            {"density_kg_m3": math.nan},
            {"mass_kg": 0.0},
            {"mass_kg": math.inf},
            {"center_of_mass_m": (0.0, 0.0)},
            {"center_of_mass_m": (0.0, math.nan, 0.0)},
            {"mesh": ""},
            {"mesh": "/absolute/mesh.obj"},
            {"mesh": "meshes/../mesh.obj"},
            {"material_id": ""},
            {"grammar_version": ""},
            {"program": {}},
            {"program": []},
            {"program": {"value": math.nan}},
        ):
            with self.subTest(change=change):
                changed = replace(p1, **change)
                self.assert_invalid(
                    replace(base, nodes=tuple(changed if node.id == "p1" else node for node in base.nodes))
                )

    def test_invalid_assembly_functions_and_tolerance(self) -> None:
        base = make_valid_tree()
        for function_values in (("",), ("vehicle", "vehicle")):
            changed = AssemblyNode("root", base.node_map()["root"].children, function_values)
            tree = replace(base, nodes=tuple(changed if node.id == "root" else node for node in base.nodes))
            self.assert_invalid(tree)
        for tolerance in (0.0, -1e-6, 5e-4 + 1e-9, math.inf):
            self.assert_invalid(replace(base, contact_tolerance_m=tolerance))

    def test_invalid_interfaces(self) -> None:
        base = make_valid_tree()
        cases = (
            (
                Interface("i12", "p1", "p2", "threaded"),
                Interface("i12", "p3", "p4", "welded"),
            ),
            (Interface("non-string", [], "p1", "threaded"),),
            (Interface("bad", "sa1", "p1", "threaded"),),
            (Interface("same", "p1", "p1", "threaded"),),
            (Interface("kind", "p1", "p2", "unknown"),),
            (Interface("extra", "p1", "p2", "welded", 1e-5),),
            (Interface("nan", "p1", "p2", "interference", math.nan),),
            (Interface("zero", "p1", "p2", "interference", 0.0),),
            (Interface("large", "p1", "p2", "interference", 1e-4 + 1e-9),),
        )
        for interfaces in cases:
            with self.subTest(interfaces=interfaces):
                self.assert_invalid(replace(base, interfaces=interfaces))


if __name__ == "__main__":
    unittest.main()
