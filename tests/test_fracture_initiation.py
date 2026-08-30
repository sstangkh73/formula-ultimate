from __future__ import annotations

from dataclasses import replace
import math
import unittest

from formula_ultimate.structural import CrackedCoupon, FractureMaterialRecord, StructuralEvidenceError, crack_representation, evaluate_fracture, validate_lefm_domain


def material() -> FractureMaterialRecord:
    return FractureMaterialRecord("m", 15e6, 250e6, 70e9, "synthetic only", False)


def coupon(a: float = 0.005) -> CrackedCoupon:
    return CrackedCoupon("c", 0.4, 0.2, 0.012, a, "ideal_infinite_plate_center_crack_Y1", "plane_strain_screened")


class FractureInitiationTests(unittest.TestCase):
    def test_closed_form_initiation_and_deterministic_event(self) -> None:
        domain = validate_lefm_domain(material(), coupon(), maximum_full_crack_width_ratio=0.1, maximum_plastic_zone_crack_ratio=0.1)
        result = evaluate_fracture(material(), coupon(), applied_force_n=domain["initiation_force_n"], maximum_full_crack_width_ratio=0.1, maximum_plastic_zone_crack_ratio=0.1)
        self.assertTrue(result.initiated)
        self.assertAlmostEqual(15e6, result.stress_intensity_pa_sqrt_m)
        self.assertEqual(result.event_id, evaluate_fracture(material(), coupon(), applied_force_n=domain["initiation_force_n"], maximum_full_crack_width_ratio=0.1, maximum_plastic_zone_crack_ratio=0.1).event_id)

    def test_representation_retains_exact_crack_tips(self) -> None:
        coarse = crack_representation(coupon(), segments_per_half_crack=8)
        fine = crack_representation(coupon(), segments_per_half_crack=32)
        self.assertEqual(coarse["left_tip_m"], fine["left_tip_m"])
        self.assertNotEqual(coarse["sha256"], fine["sha256"])

    def test_invalid_domains_and_provenance_fail_closed(self) -> None:
        with self.assertRaisesRegex(StructuralEvidenceError, "plane-strain"):
            validate_lefm_domain(material(), replace(coupon(), thickness_m=0.001), maximum_full_crack_width_ratio=0.1, maximum_plastic_zone_crack_ratio=0.1)
        with self.assertRaisesRegex(StructuralEvidenceError, "finite-width"):
            validate_lefm_domain(material(), replace(coupon(), crack_half_length_m=0.02), maximum_full_crack_width_ratio=0.1, maximum_plastic_zone_crack_ratio=0.1)
        with self.assertRaises(StructuralEvidenceError):
            replace(material(), provenance="")

    def test_yield_before_fracture_is_rejected(self) -> None:
        weak_toughness_domain = replace(material(), toughness_pa_sqrt_m=40e6)
        wide_thick = replace(coupon(), width_m=0.4, thickness_m=0.1, crack_half_length_m=0.005)
        with self.assertRaisesRegex(StructuralEvidenceError, "yield precedes"):
            validate_lefm_domain(weak_toughness_domain, wide_thick, maximum_full_crack_width_ratio=0.1, maximum_plastic_zone_crack_ratio=0.1)


if __name__ == "__main__":
    unittest.main()
