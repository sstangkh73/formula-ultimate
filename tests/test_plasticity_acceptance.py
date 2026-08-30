from __future__ import annotations

from dataclasses import replace
import unittest

from formula_ultimate.structural import (
    BilinearPlasticitySpec,
    StructuralEvidenceError,
    build_plasticity_deck,
    structured_hex_mesh,
)


def spec() -> BilinearPlasticitySpec:
    return BilinearPlasticitySpec("p", "synthetic", 0.1, 0.01, 0.01, "m", 70e9, 0.3, 2700, 250e6, 1e9, "synthetic only")


class PlasticityReferenceTests(unittest.TestCase):
    def test_hardening_conversion_preserves_total_tangent(self) -> None:
        item = spec()
        h = item.hardening_modulus_pa
        self.assertAlmostEqual(item.tangent_modulus_pa, item.youngs_modulus_pa * h / (item.youngs_modulus_pa + h))
        peak = 270e6
        self.assertAlmostEqual(item.monotonic_strain(peak), item.yield_stress_pa / item.youngs_modulus_pa + 0.02)
        self.assertAlmostEqual(item.monotonic_plastic_strain(peak), 0.02 - (peak - item.yield_stress_pa) / item.youngs_modulus_pa)

    def test_invalid_or_unsourced_material_fails_closed(self) -> None:
        with self.assertRaises(StructuralEvidenceError):
            replace(spec(), provenance="")
        with self.assertRaises(StructuralEvidenceError):
            replace(spec(), tangent_modulus_pa=70e9)

    def test_structured_mesh_and_load_area_close(self) -> None:
        mesh = structured_hex_mesh(spec(), nx=2)
        self.assertEqual(8, len(mesh.elements))
        self.assertAlmostEqual(spec().area_m2, sum(mesh.tributary_area_m2.values()))
        self.assertFalse(set(mesh.fixed_x) & set(mesh.loaded))

    def test_deck_declares_plasticity_history_and_output(self) -> None:
        item = spec()
        deck = build_plasticity_deck(item, structured_hex_mesh(item, nx=2), load_factors=(0.8, 1.0, 1.08, 0.0), maximum_plastic_strain=0.03)
        self.assertIn("*PLASTIC", deck)
        self.assertIn("S, E, PEEQ, ENER, ELSE", deck)
        self.assertEqual(4, deck.count("*CLOAD, OP=NEW"))


if __name__ == "__main__":
    unittest.main()
