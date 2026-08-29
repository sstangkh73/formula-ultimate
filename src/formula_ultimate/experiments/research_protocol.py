"""Versioned admission contract for one geometry-to-Level-0 candidate run."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping

from formula_ultimate.components.grammar import MountingPlateSpec
from formula_ultimate.experiments.cad_level0 import (
    CadMeasurement,
    EvidenceViolation,
    Level0Controls,
    evaluate_cad_measurement,
)


REQUIRED_STAGE_SEQUENCE = (
    "declaration_gate",
    "cadquery_3d_generation",
    "step_export_identity",
    "freecad_import_measurement",
    "level0_evidence_admission",
    "falsification_review",
)
REQUIRED_IDENTITY_FIELDS = (
    "protocol_id",
    "experiment_id",
    "candidate_id",
    "grammar_version",
    "seed",
)
REQUIRED_REVIEW_FIELDS = (
    "supporting_evidence",
    "contradicting_evidence",
    "alternative_explanations",
    "missing_evidence",
    "confidence",
)


@dataclass(frozen=True, slots=True)
class ResearchProtocol:
    protocol_id: str
    protocol_version: int
    required_stage_sequence: tuple[str, ...]
    permitted_claim_level: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ResearchProtocol":
        try:
            protocol_version = value["protocol_version"]
            stages = tuple(value["required_stage_sequence"])
            if type(protocol_version) is not int or protocol_version < 1:
                raise EvidenceViolation("protocol_version must be a positive integer")
            if stages != REQUIRED_STAGE_SEQUENCE:
                raise EvidenceViolation("required protocol stage sequence differs from v1")
            if tuple(value["required_identity_fields"]) != REQUIRED_IDENTITY_FIELDS:
                raise EvidenceViolation("required protocol identity fields differ from v1")
            if tuple(value["required_review_fields"]) != REQUIRED_REVIEW_FIELDS:
                raise EvidenceViolation("required protocol review fields differ from v1")
            failure_policy = value["failure_policy"]
            forbidden_true = (
                "silent_parameter_clipping",
                "silent_geometry_repair",
                "analytical_substitution_for_missing_freecad_evidence",
            )
            if any(failure_policy[item] is not False for item in forbidden_true):
                raise EvidenceViolation("protocol permits a forbidden silent correction")
            if failure_policy["failed_stages_are_observable"] is not True:
                raise EvidenceViolation("protocol must make failed stages observable")
            result = cls(
                protocol_id=str(value["protocol_id"]),
                protocol_version=protocol_version,
                required_stage_sequence=stages,
                permitted_claim_level=str(value["permitted_claim_level"]),
            )
        except (KeyError, TypeError) as exc:
            raise EvidenceViolation(f"malformed research protocol: {exc}") from exc
        if not result.protocol_id.strip() or not result.permitted_claim_level.strip():
            raise EvidenceViolation("protocol identity and claim level must not be empty")
        return result


@dataclass(frozen=True, slots=True)
class CandidateDeclaration:
    protocol_id: str
    experiment_id: str
    candidate_id: str
    candidate_class: str
    grammar_version: str
    seed: int
    hypothesis: str
    independent_variables: tuple[str, ...]
    dependent_variables: tuple[str, ...]
    pre_registered_failure_criteria: tuple[str, ...]
    spec: MountingPlateSpec
    controls: Level0Controls
    volume_absolute_tolerance_m3: float
    volume_relative_tolerance: float
    bounds_absolute_tolerance_m: float

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CandidateDeclaration":
        try:
            candidate = value["candidate"]
            candidate_id = str(value["candidate_id"])
            if str(candidate["candidate_id"]) != candidate_id:
                raise EvidenceViolation("candidate ID differs inside the declaration")
            seed = value["seed"]
            if type(seed) is not int:
                raise EvidenceViolation("seed must be an integer")
            spec_payload = {
                **value["common_spec"],
                "lightening_radius_m": candidate["lightening_radius_m"],
                "material": value["material"],
                "grammar_version": value["grammar_version"],
            }
            tolerance = value["tolerances"]
            result = cls(
                protocol_id=str(value["protocol_id"]),
                experiment_id=str(value["experiment_id"]),
                candidate_id=candidate_id,
                candidate_class=str(value["candidate_class"]),
                grammar_version=str(value["grammar_version"]),
                seed=seed,
                hypothesis=str(value["hypothesis"]),
                independent_variables=tuple(value["independent_variables"]),
                dependent_variables=tuple(value["dependent_variables"]),
                pre_registered_failure_criteria=tuple(
                    value["pre_registered_failure_criteria"]
                ),
                spec=MountingPlateSpec.from_mapping(spec_payload),
                controls=Level0Controls(**value["level0_controls"]),
                volume_absolute_tolerance_m3=float(tolerance["volume_absolute_m3"]),
                volume_relative_tolerance=float(tolerance["volume_relative"]),
                bounds_absolute_tolerance_m=float(tolerance["bounds_absolute_m"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            if isinstance(exc, EvidenceViolation):
                raise
            raise EvidenceViolation(f"malformed candidate declaration: {exc}") from exc
        identity = (
            result.protocol_id,
            result.experiment_id,
            result.candidate_id,
            result.candidate_class,
            result.grammar_version,
            result.hypothesis,
        )
        if any(not item.strip() for item in identity):
            raise EvidenceViolation("candidate identity fields must not be empty")
        if result.candidate_class != "bounded_component_geometry_specimen":
            raise EvidenceViolation("candidate_class is outside the Phase-1 boundary")
        declared_lists = (
            result.independent_variables,
            result.dependent_variables,
            result.pre_registered_failure_criteria,
        )
        if any(
            not items or any(type(item) is not str or not item.strip() for item in items)
            for items in declared_lists
        ):
            raise EvidenceViolation("experiment variables and failure criteria must be non-empty strings")
        tolerances = (
            result.volume_absolute_tolerance_m3,
            result.volume_relative_tolerance,
            result.bounds_absolute_tolerance_m,
        )
        if not all(math.isfinite(item) and item >= 0.0 for item in tolerances):
            raise EvidenceViolation("evidence tolerances must be finite and >= 0")
        return result


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise EvidenceViolation(f"expected a JSON object: {path}")
    return value


def admit_candidate_evidence(
    *,
    protocol: ResearchProtocol,
    declaration: CandidateDeclaration,
    manifest: Mapping[str, Any],
    freecad_report: Mapping[str, Any],
    step_path: Path,
) -> dict[str, Any]:
    """Authenticate CAD evidence and evaluate both tools without substitution."""

    if declaration.protocol_id != protocol.protocol_id:
        raise EvidenceViolation("candidate declares a different protocol ID")
    if manifest.get("candidate_id") != declaration.candidate_id:
        raise EvidenceViolation("CadQuery manifest has a different candidate ID")
    if manifest.get("seed") != declaration.seed:
        raise EvidenceViolation("CadQuery manifest has a different seed")
    if manifest.get("spec", {}).get("grammar_version") != declaration.grammar_version:
        raise EvidenceViolation("CadQuery manifest has a different grammar version")
    if not step_path.is_file():
        raise EvidenceViolation("STEP artifact is missing")
    actual_step_hash = sha256_file(step_path)
    step = manifest.get("step", {})
    if step.get("header") != "ISO-10303-21;":
        raise EvidenceViolation("STEP artifact has an unexpected header")
    if step.get("sha256") != actual_step_hash:
        raise EvidenceViolation("STEP hash differs from the CadQuery manifest")
    if freecad_report.get("step_sha256") != actual_step_hash:
        raise EvidenceViolation("FreeCAD measured a different STEP artifact")

    kwargs = {
        "spec": declaration.spec,
        "controls": declaration.controls,
        "volume_absolute_tolerance_m3": declaration.volume_absolute_tolerance_m3,
        "volume_relative_tolerance": declaration.volume_relative_tolerance,
        "bounds_absolute_tolerance_m": declaration.bounds_absolute_tolerance_m,
    }
    cadquery_measurement = CadMeasurement.from_mapping(manifest["cadquery_measurement"])
    freecad_measurement = CadMeasurement.from_mapping(freecad_report)
    cadquery_gate = evaluate_cad_measurement(
        measurement=cadquery_measurement,
        **kwargs,
    )
    level0_result = evaluate_cad_measurement(
        measurement=freecad_measurement,
        **kwargs,
    )
    return {
        "status": "passed",
        "protocol_id": protocol.protocol_id,
        "protocol_version": protocol.protocol_version,
        "experiment_id": declaration.experiment_id,
        "candidate_id": declaration.candidate_id,
        "candidate_class": declaration.candidate_class,
        "claim_level": protocol.permitted_claim_level,
        "completed_stages": list(protocol.required_stage_sequence),
        "step": {
            "path": str(step_path),
            "bytes": step_path.stat().st_size,
            "sha256": actual_step_hash,
        },
        "cadquery_measurement": dict(manifest["cadquery_measurement"]),
        "freecad_measurement": dict(freecad_report),
        "cross_tool_residuals": {
            "freecad_minus_cadquery_volume_m3": (
                freecad_measurement.volume_m3 - cadquery_measurement.volume_m3
            ),
            "cadquery_analytical_relative": cadquery_gate.volume_relative_residual,
            "freecad_analytical_relative": level0_result.volume_relative_residual,
        },
        "level0_from_freecad": level0_result.to_dict(),
    }
