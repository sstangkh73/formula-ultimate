from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from formula_ultimate.search.freeform_material_generator import (
    FreeformMaterialViolation,
    apply_edit,
    extract_surface,
    field_descriptor,
    generate_source,
    grid_spec,
    validate_protocol,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "development" / "freeform_material_generator_v1.json"


class FreeformMaterialProtocolTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads(CONFIG.read_text(encoding="utf-8"))

    def test_registered_protocol_has_all_operators_and_three_levels(self):
        result = validate_protocol(self.raw)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(len(result["operator_coverage"]), 6)
        self.assertEqual(result["dimensions"], [24, 24, 24])

    def test_nonfinite_resolution_missing_operator_and_bad_dependency_fail(self):
        invalid = copy.deepcopy(self.raw)
        invalid["representation"]["resolution_m"] = float("inf")
        with self.assertRaisesRegex(FreeformMaterialViolation, "finite"):
            validate_protocol(invalid)
        invalid = copy.deepcopy(self.raw)
        invalid["operator_chain"] = invalid["operator_chain"][:-1]
        with self.assertRaisesRegex(FreeformMaterialViolation, "coverage"):
            validate_protocol(invalid)
        invalid = copy.deepcopy(self.raw)
        invalid["dependency"]["work108_commit"] = "stale"
        with self.assertRaisesRegex(FreeformMaterialViolation, "dependency identity"):
            validate_protocol(invalid)


class FreeformMaterialFieldTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.spec = grid_spec(self.raw["representation"])

    def test_single_voxel_surface_is_closed_and_has_exact_volume(self):
        field = {(4, 5, 6): "material_alpha"}
        descriptor = field_descriptor(field, self.spec)
        surface = extract_surface(field, self.spec, 100)
        self.assertEqual(surface["triangle_count"], 12)
        self.assertEqual(surface["boundary_components"], 1)
        self.assertEqual(surface["genus_sum"], 0)
        self.assertAlmostEqual(surface["enclosed_volume_m3"], descriptor["occupied_volume_m3"], places=15)

    def test_source_and_every_registered_edit_are_causal_and_budgeted(self):
        field, _ = generate_source(self.raw)
        identities = [field_descriptor(field, self.spec)["geometry_sha256"]]
        for edit in self.raw["operator_chain"]:
            field, trace = apply_edit(field, self.spec, edit, set(self.raw["materials"]), 4000)
            self.assertGreater(trace["changed_cells"], 0)
            identities.append(field_descriptor(field, self.spec)["geometry_sha256"])
        self.assertEqual(len(identities), len(set(identities)))

    def test_noop_label_mixing_and_surface_budget_fail_closed(self):
        field, _ = generate_source(self.raw)
        no_op = copy.deepcopy(self.raw["operator_chain"][-1])
        no_op["parameters"]["from_material"] = "missing"
        with self.assertRaisesRegex(FreeformMaterialViolation, "schema or material"):
            apply_edit(field, self.spec, no_op, set(self.raw["materials"]), 4000)
        with self.assertRaisesRegex(FreeformMaterialViolation, "label mixing"):
            field_descriptor({(1, 1, 1): ["material_alpha", "material_beta"]}, self.spec)  # type: ignore[dict-item]
        with self.assertRaisesRegex(FreeformMaterialViolation, "triangle budget"):
            extract_surface(field, self.spec, 12)

    def test_refinement_levels_divide_domain_and_change_representation(self):
        identities = []
        for resolution in self.raw["refinement_resolutions_m"]:
            spec = grid_spec(self.raw["representation"], resolution)
            field, _ = generate_source(self.raw, resolution)
            identities.append(field_descriptor(field, spec)["geometry_sha256"])
        self.assertEqual(len(identities), len(set(identities)))


if __name__ == "__main__":
    unittest.main()
