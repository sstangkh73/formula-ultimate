"""Controlled baselines, search studies, and reproducible analyses."""

from .cad_level0 import (
    CadLevel0Result,
    CadMeasurement,
    EvidenceViolation,
    Level0Controls,
    evaluate_cad_measurement,
)
from .research_protocol import (
    CandidateDeclaration,
    ResearchProtocol,
    admit_candidate_evidence,
)
from .whole_vehicle_baseline import (
    BASELINE_EVALUATOR_VERSION,
    BaselineCaseRecord,
    WholeVehicleBaselineError,
    WholeVehicleBaselineResult,
    convergence_metrics,
    evaluate_baseline,
    evaluate_reference_matrix,
    validate_baseline_inputs,
)

__all__ = [
    "CadLevel0Result",
    "CadMeasurement",
    "EvidenceViolation",
    "Level0Controls",
    "evaluate_cad_measurement",
    "CandidateDeclaration",
    "ResearchProtocol",
    "admit_candidate_evidence",
    "BASELINE_EVALUATOR_VERSION",
    "BaselineCaseRecord",
    "WholeVehicleBaselineError",
    "WholeVehicleBaselineResult",
    "convergence_metrics",
    "evaluate_baseline",
    "evaluate_reference_matrix",
    "validate_baseline_inputs",
]
