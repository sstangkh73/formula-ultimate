from __future__ import annotations

import unittest

from formula_ultimate.structural import (
    StructuralEvidenceError,
    classify_boundary_comparison,
    evaluate_c3d10_refinement,
    support_topology_signature,
)


def mesh(mesh_id: str, size: float, scale: float = 1.0, *, element: str = "C3D10") -> dict:
    return {
        "mesh_id": mesh_id,
        "element_type": element,
        "order": 2 if element == "C3D10" else 1,
        "characteristic_size_m": size,
        "analytical_eigenvalue_error_relative": 0.01,
        "nonlinear_cases": [
            {"load_n": 10.0, "measured_amplification": 2.0 * scale, "secant_error_relative": 0.01},
            {"load_n": 20.0, "measured_amplification": 4.0 * scale, "secant_error_relative": 0.02},
        ],
    }


class GateARemediationTests(unittest.TestCase):
    def test_support_signature_is_order_invariant_but_deletion_is_mutation(self) -> None:
        allowed = ("upper", "lower")
        self.assertEqual(
            support_topology_signature(("upper", "lower"), allowed_support_ids=allowed),
            support_topology_signature(("lower", "upper"), allowed_support_ids=allowed),
        )
        result = classify_boundary_comparison(
            reference_supports=("upper", "lower"), candidate_supports=("lower",),
            allowed_support_ids=allowed, reference_model_id="fixed-v1", candidate_model_id="fixed-v1",
            reference_compliance=2.0, candidate_compliance=8.0,
            maximum_equivalent_change_relative=1e-10,
        )
        self.assertEqual(result["status"], "topology_mutation")
        self.assertFalse(result["admitted_as_representation_test"])

    def test_duplicate_and_undeclared_supports_fail_closed(self) -> None:
        with self.assertRaises(StructuralEvidenceError):
            support_topology_signature(("upper", "upper"), allowed_support_ids=("upper", "lower"))
        with self.assertRaises(StructuralEvidenceError):
            support_topology_signature(("unknown",), allowed_support_ids=("upper", "lower"))

    def test_equivalent_encoding_is_admitted_and_model_mutation_is_not(self) -> None:
        values = dict(
            reference_supports=("upper", "lower"), candidate_supports=("lower", "upper"),
            allowed_support_ids=("upper", "lower"), reference_model_id="fixed-v1",
            reference_compliance=2.0, candidate_compliance=2.0,
            maximum_equivalent_change_relative=1e-10,
        )
        self.assertEqual(classify_boundary_comparison(**values, candidate_model_id="fixed-v1")["status"], "supported")
        self.assertEqual(classify_boundary_comparison(**values, candidate_model_id="spring-v1")["status"], "boundary_model_mutation")

    def test_c3d10_refinement_supports_and_rejects_invalid_family(self) -> None:
        results = [mesh("q18", 0.0018, 0.98), mesh("q14", 0.0014, 0.995), mesh("q12", 0.0012, 1.0)]
        decision = evaluate_c3d10_refinement(
            results, ordered_mesh_ids=("q18", "q14", "q12"),
            maximum_last_two_change_relative=0.05,
            maximum_secant_error_relative=0.05,
            maximum_eigenvalue_error_relative=0.05,
        )
        self.assertEqual(decision["status"], "supported")
        results[-1] = mesh("q12", 0.0012, element="C3D4")
        with self.assertRaises(StructuralEvidenceError):
            evaluate_c3d10_refinement(
                results, ordered_mesh_ids=("q18", "q14", "q12"),
                maximum_last_two_change_relative=0.05,
                maximum_secant_error_relative=0.05,
                maximum_eigenvalue_error_relative=0.05,
            )


if __name__ == "__main__":
    unittest.main()
