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

__all__ = [
    "CadLevel0Result",
    "CadMeasurement",
    "EvidenceViolation",
    "Level0Controls",
    "evaluate_cad_measurement",
    "CandidateDeclaration",
    "ResearchProtocol",
    "admit_candidate_evidence",
]
