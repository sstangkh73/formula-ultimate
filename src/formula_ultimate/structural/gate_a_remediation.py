"""Evidence-domain decisions for the Work 051 Gate A remediation."""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Iterable, Mapping, Sequence

from .acceptance import StructuralEvidenceError


def relative_difference(first: float, second: float) -> float:
    if not math.isfinite(first) or not math.isfinite(second):
        raise StructuralEvidenceError("comparison response must be finite")
    scale = 0.5 * (abs(first) + abs(second))
    return abs(first - second) / scale if scale else 0.0


def support_topology(
    support_ids: Iterable[str], *, allowed_support_ids: Iterable[str]
) -> tuple[str, ...]:
    raw = tuple(support_ids)
    if not raw or any(not isinstance(item, str) or not item for item in raw):
        raise StructuralEvidenceError("support topology must contain non-empty identities")
    if len(set(raw)) != len(raw):
        raise StructuralEvidenceError("support topology contains duplicated identities")
    allowed = set(allowed_support_ids)
    if not set(raw) <= allowed:
        raise StructuralEvidenceError("support topology contains an undeclared identity")
    return tuple(sorted(raw))


def support_topology_signature(
    support_ids: Iterable[str], *, allowed_support_ids: Iterable[str]
) -> str:
    canonical = support_topology(support_ids, allowed_support_ids=allowed_support_ids)
    payload = json.dumps(canonical, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def classify_boundary_comparison(
    *,
    reference_supports: Iterable[str],
    candidate_supports: Iterable[str],
    allowed_support_ids: Iterable[str],
    reference_model_id: str,
    candidate_model_id: str,
    reference_compliance: float,
    candidate_compliance: float,
    maximum_equivalent_change_relative: float,
) -> dict[str, Any]:
    reference = support_topology(reference_supports, allowed_support_ids=allowed_support_ids)
    candidate = support_topology(candidate_supports, allowed_support_ids=allowed_support_ids)
    change = relative_difference(reference_compliance, candidate_compliance)
    if reference != candidate:
        return {
            "status": "topology_mutation",
            "admitted_as_representation_test": False,
            "reference_topology": reference,
            "candidate_topology": candidate,
            "compliance_change_relative": change,
        }
    if not reference_model_id or not candidate_model_id or reference_model_id != candidate_model_id:
        return {
            "status": "boundary_model_mutation",
            "admitted_as_representation_test": False,
            "reference_topology": reference,
            "candidate_topology": candidate,
            "compliance_change_relative": change,
        }
    return {
        "status": "supported" if change <= maximum_equivalent_change_relative else "rejected",
        "admitted_as_representation_test": True,
        "reference_topology": reference,
        "candidate_topology": candidate,
        "compliance_change_relative": change,
        "limit": maximum_equivalent_change_relative,
    }


def evaluate_c3d10_refinement(
    mesh_results: Sequence[Mapping[str, Any]],
    *,
    ordered_mesh_ids: Sequence[str],
    maximum_last_two_change_relative: float,
    maximum_secant_error_relative: float,
    maximum_eigenvalue_error_relative: float,
) -> dict[str, Any]:
    if len(ordered_mesh_ids) < 3 or len(set(ordered_mesh_ids)) != len(ordered_mesh_ids):
        raise StructuralEvidenceError("C3D10 refinement requires at least three unique mesh identities")
    by_id = {str(item["mesh_id"]): item for item in mesh_results}
    if any(mesh_id not in by_id for mesh_id in ordered_mesh_ids):
        raise StructuralEvidenceError("C3D10 refinement evidence is incomplete")
    selected = [by_id[mesh_id] for mesh_id in ordered_mesh_ids]
    if any(item.get("element_type") != "C3D10" or int(item.get("order", 0)) != 2 for item in selected):
        raise StructuralEvidenceError("non-C3D10 evidence entered the C3D10 refinement decision")
    sizes = [float(item["characteristic_size_m"]) for item in selected]
    if any(not math.isfinite(value) or value <= 0.0 for value in sizes) or any(
        later >= earlier for earlier, later in zip(sizes, sizes[1:])
    ):
        raise StructuralEvidenceError("C3D10 refinement sizes are not strictly decreasing")
    case_counts = {len(item["nonlinear_cases"]) for item in selected}
    if len(case_counts) != 1 or not case_counts or 0 in case_counts:
        raise StructuralEvidenceError("C3D10 load-case evidence is incomplete")
    load_count = next(iter(case_counts))
    changes: dict[str, float] = {}
    penultimate, final = selected[-2:]
    for index in range(load_count):
        first_case = penultimate["nonlinear_cases"][index]
        second_case = final["nonlinear_cases"][index]
        first_load, second_load = float(first_case["load_n"]), float(second_case["load_n"])
        if first_load != second_load:
            raise StructuralEvidenceError("C3D10 refinement load identities differ")
        changes[str(first_load)] = relative_difference(
            float(first_case["measured_amplification"]),
            float(second_case["measured_amplification"]),
        )
    secant_errors = [
        float(case["secant_error_relative"])
        for item in selected
        for case in item["nonlinear_cases"]
    ]
    eigen_errors = [float(item["analytical_eigenvalue_error_relative"]) for item in selected]
    supported = (
        max(changes.values()) <= maximum_last_two_change_relative
        and max(secant_errors) <= maximum_secant_error_relative
        and max(eigen_errors) <= maximum_eigenvalue_error_relative
    )
    return {
        "status": "supported" if supported else "rejected",
        "ordered_mesh_ids": tuple(ordered_mesh_ids),
        "last_two_amplification_change_relative": changes,
        "maximum_last_two_change_relative": max(changes.values()),
        "maximum_secant_error_relative": max(secant_errors),
        "maximum_eigenvalue_error_relative": max(eigen_errors),
        "limits": {
            "last_two_change_relative": maximum_last_two_change_relative,
            "secant_error_relative": maximum_secant_error_relative,
            "eigenvalue_error_relative": maximum_eigenvalue_error_relative,
        },
    }
