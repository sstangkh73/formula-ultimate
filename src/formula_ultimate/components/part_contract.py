"""Fail-closed geometry-causal physical-part declarations for Work 077.

The contract validates evidence-bearing declarations only.  It deliberately
does not infer missing fields, repair geometry, or claim physical validity.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
import re
from typing import Any, Mapping, Sequence


PART_CONTRACT_VERSION = "geometry_causal_part_v1"
INTERFACE_TYPES = frozenset(
    {
        "fixed_mount",
        "revolute",
        "prismatic",
        "spherical",
        "bearing_seat",
        "shaft_coupling",
        "spline_key",
        "bolted",
        "welded",
        "ground_contact",
        "thermal",
        "electrical_fluid",
    }
)
DATUM_TYPES = frozenset({"point", "axis", "plane"})
LOAD_REGION_ROLES = frozenset(
    {"application", "support", "contact", "thermal", "electrical", "fluid"}
)
DOFS = frozenset({"tx", "ty", "tz", "rx", "ry", "rz"})
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_ID = re.compile(r"^[a-z][a-z0-9_.-]*$")
_PARAMETER_SUFFIXES = ("_m", "_m2", "_m3", "_rad", "_ratio", "_count")


class PartContractViolation(ValueError):
    """Raised when a part declaration is incomplete, ambiguous, or invalid."""


def _exact_keys(
    value: Mapping[str, Any], expected: set[str], context: str
) -> None:
    unknown = set(value) - expected
    missing = expected - set(value)
    if unknown or missing:
        raise PartContractViolation(
            f"{context} keys mismatch; missing={sorted(missing)}, "
            f"unknown={sorted(unknown)}"
        )


def _mapping(value: Any, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise PartContractViolation(f"{context} must be an object")
    return value


def _sequence(value: Any, context: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise PartContractViolation(f"{context} must be an array")
    return value


def _identifier(value: Any, context: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise PartContractViolation(f"{context} must be a lower-case identifier")
    return value


def _text(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PartContractViolation(f"{context} must be non-empty text")
    return value


def _number(value: Any, context: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise PartContractViolation(f"{context} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise PartContractViolation(f"{context} must be finite")
    return result


def _positive(value: Any, context: str) -> float:
    result = _number(value, context)
    if result <= 0.0:
        raise PartContractViolation(f"{context} must be > 0")
    return result


def _sha256(value: Any, context: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise PartContractViolation(f"{context} must be a lower-case SHA-256")
    return value


def _vec3(value: Any, context: str) -> tuple[float, float, float]:
    items = _sequence(value, context)
    if len(items) != 3:
        raise PartContractViolation(f"{context} must contain three values")
    return tuple(_number(item, context) for item in items)  # type: ignore[return-value]


def _dot(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return math.fsum(x * y for x, y in zip(a, b, strict=True))


def _cross(
    a: tuple[float, float, float], b: tuple[float, float, float]
) -> tuple[float, float, float]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _validate_frame(value: Any, context: str) -> None:
    frame = _mapping(value, context)
    _exact_keys(frame, {"origin_m", "x_axis", "y_axis", "z_axis"}, context)
    _vec3(frame["origin_m"], f"{context}.origin_m")
    x = _vec3(frame["x_axis"], f"{context}.x_axis")
    y = _vec3(frame["y_axis"], f"{context}.y_axis")
    z = _vec3(frame["z_axis"], f"{context}.z_axis")
    tolerance = 1e-9
    if any(abs(_dot(axis, axis) - 1.0) > tolerance for axis in (x, y, z)):
        raise PartContractViolation(f"{context} axes must be unit length")
    if any(abs(value) > tolerance for value in (_dot(x, y), _dot(x, z), _dot(y, z))):
        raise PartContractViolation(f"{context} axes must be orthogonal")
    if max(abs(a - b) for a, b in zip(_cross(x, y), z, strict=True)) > tolerance:
        raise PartContractViolation(f"{context} must be right-handed")


def _unique(values: Sequence[str], context: str) -> None:
    if len(values) != len(set(values)):
        raise PartContractViolation(f"{context} contains duplicate identities")


def _validate_parameter(name: str, value: Any, context: str) -> None:
    if not name.endswith(_PARAMETER_SUFFIXES):
        raise PartContractViolation(f"{context}.{name} has an unknown or missing SI unit")
    number = _number(value, f"{context}.{name}")
    if name.endswith("_count"):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise PartContractViolation(f"{context}.{name} must be an integer >= 1")
    elif "thickness" in name and number <= 0.0:
        raise PartContractViolation(f"{context}.{name} must be > 0")


def canonical_part_bytes(value: Mapping[str, Any]) -> bytes:
    """Return deterministic UTF-8 JSON after complete contract validation."""

    validate_part_mapping(value)
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise PartContractViolation(f"declaration is not canonical JSON: {exc}") from exc


def part_declaration_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_part_bytes(value)).hexdigest()


@dataclass(frozen=True, slots=True)
class PartContract:
    part_id: str
    canonical_json: bytes
    declaration_sha256: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "PartContract":
        encoded = canonical_part_bytes(value)
        return cls(
            part_id=str(value["part_id"]),
            canonical_json=encoded,
            declaration_sha256=hashlib.sha256(encoded).hexdigest(),
        )


def validate_part_mapping(value: Mapping[str, Any]) -> None:
    top = _mapping(value, "part")
    _exact_keys(
        top,
        {
            "contract_version",
            "part_id",
            "function_tags",
            "feature_history",
            "material",
            "local_frame",
            "datums",
            "interfaces",
            "load_regions",
            "load_path",
            "manufacturing",
            "tolerances",
            "minimum_feature_size_m",
            "parameter_provenance",
            "claim_boundary",
        },
        "part",
    )
    if top["contract_version"] != PART_CONTRACT_VERSION:
        raise PartContractViolation("contract_version mismatch")
    _identifier(top["part_id"], "part_id")

    function_tags = tuple(
        _identifier(tag, "function_tags item")
        for tag in _sequence(top["function_tags"], "function_tags")
    )
    if not function_tags:
        raise PartContractViolation("function_tags must not be empty")
    _unique(function_tags, "function_tags")

    feature_ids: list[str] = []
    provenance_targets: set[str] = {
        "minimum_feature_size_m",
        "tolerances.general_tolerance_m",
        "tolerances.angular_tolerance_rad",
    }
    for index, raw_feature in enumerate(
        _sequence(top["feature_history"], "feature_history")
    ):
        feature = _mapping(raw_feature, f"feature_history[{index}]")
        _exact_keys(
            feature,
            {"feature_id", "operator", "parameters", "parent_feature_ids"},
            f"feature_history[{index}]",
        )
        feature_id = _identifier(feature["feature_id"], "feature_id")
        _identifier(feature["operator"], "feature operator")
        parents = tuple(
            _identifier(parent, "parent_feature_id")
            for parent in _sequence(feature["parent_feature_ids"], "parent_feature_ids")
        )
        if any(parent not in feature_ids for parent in parents):
            raise PartContractViolation("feature parent must precede its child")
        parameters = _mapping(feature["parameters"], "feature parameters")
        if not parameters:
            raise PartContractViolation("feature parameters must not be empty")
        for name, parameter in parameters.items():
            _identifier(name, "feature parameter name")
            _validate_parameter(name, parameter, f"feature {feature_id}")
            provenance_targets.add(f"features.{feature_id}.parameters.{name}")
        feature_ids.append(feature_id)
    if not feature_ids:
        raise PartContractViolation("feature_history must not be empty")
    _unique(feature_ids, "feature_history")

    material = _mapping(top["material"], "material")
    _exact_keys(material, {"material_id", "record_sha256", "evidence_status"}, "material")
    _identifier(material["material_id"], "material_id")
    _sha256(material["record_sha256"], "material.record_sha256")
    if material["evidence_status"] not in {"sourced", "synthetic", "unsupported"}:
        raise PartContractViolation("material.evidence_status is unsupported")

    _validate_frame(top["local_frame"], "local_frame")

    datum_ids: list[str] = []
    for index, raw_datum in enumerate(_sequence(top["datums"], "datums")):
        datum = _mapping(raw_datum, f"datums[{index}]")
        _exact_keys(datum, {"datum_id", "datum_type", "frame"}, f"datums[{index}]")
        datum_ids.append(_identifier(datum["datum_id"], "datum_id"))
        if datum["datum_type"] not in DATUM_TYPES:
            raise PartContractViolation("unsupported datum_type")
        _validate_frame(datum["frame"], f"datum {datum_ids[-1]} frame")
    if not datum_ids:
        raise PartContractViolation("datums must not be empty")
    _unique(datum_ids, "datums")

    interface_ids: list[str] = []
    for index, raw_interface in enumerate(_sequence(top["interfaces"], "interfaces")):
        interface = _mapping(raw_interface, f"interfaces[{index}]")
        _exact_keys(
            interface,
            {
                "interface_id",
                "interface_type",
                "datum_id",
                "geometry_signature_sha256",
                "mating_role",
                "tolerance_m",
                "allowed_dofs",
            },
            f"interfaces[{index}]",
        )
        interface_id = _identifier(interface["interface_id"], "interface_id")
        interface_ids.append(interface_id)
        if interface["interface_type"] not in INTERFACE_TYPES:
            raise PartContractViolation("unsupported interface_type")
        if interface["datum_id"] not in datum_ids:
            raise PartContractViolation("interface references an unknown datum")
        _sha256(interface["geometry_signature_sha256"], "interface geometry signature")
        _text(interface["mating_role"], "interface mating_role")
        tolerance = _positive(interface["tolerance_m"], "interface tolerance_m")
        provenance_targets.add(f"interfaces.{interface_id}.tolerance_m")
        dofs = tuple(_sequence(interface["allowed_dofs"], "allowed_dofs"))
        if any(dof not in DOFS for dof in dofs):
            raise PartContractViolation("allowed_dofs contains an unsupported DOF")
        _unique(dofs, "allowed_dofs")
        if interface["interface_type"] == "fixed_mount" and dofs:
            raise PartContractViolation("fixed_mount must not allow a DOF")
        if tolerance > _number(top["minimum_feature_size_m"], "minimum_feature_size_m"):
            raise PartContractViolation("interface tolerance exceeds minimum feature size")
    if not interface_ids:
        raise PartContractViolation("interfaces must not be empty")
    _unique(interface_ids, "interfaces")

    region_ids: list[str] = []
    for index, raw_region in enumerate(_sequence(top["load_regions"], "load_regions")):
        region = _mapping(raw_region, f"load_regions[{index}]")
        _exact_keys(
            region,
            {"region_id", "role", "geometry_signature_sha256"},
            f"load_regions[{index}]",
        )
        region_ids.append(_identifier(region["region_id"], "region_id"))
        if region["role"] not in LOAD_REGION_ROLES:
            raise PartContractViolation("unsupported load region role")
        _sha256(region["geometry_signature_sha256"], "load region geometry signature")
    _unique(region_ids, "load_regions")
    load_path = tuple(
        _identifier(region_id, "load_path item")
        for region_id in _sequence(top["load_path"], "load_path")
    )
    if len(load_path) < 2 or len(set(load_path)) < 2:
        raise PartContractViolation("load_path must connect at least two distinct regions")
    if any(region_id not in region_ids for region_id in load_path):
        raise PartContractViolation("load_path references an unknown load region")

    manufacturing = _mapping(top["manufacturing"], "manufacturing")
    _exact_keys(manufacturing, {"process", "evidence_id"}, "manufacturing")
    _identifier(manufacturing["process"], "manufacturing.process")
    _text(manufacturing["evidence_id"], "manufacturing.evidence_id")

    tolerances = _mapping(top["tolerances"], "tolerances")
    _exact_keys(
        tolerances,
        {"general_tolerance_m", "angular_tolerance_rad"},
        "tolerances",
    )
    general_tolerance = _positive(
        tolerances["general_tolerance_m"], "tolerances.general_tolerance_m"
    )
    _positive(tolerances["angular_tolerance_rad"], "tolerances.angular_tolerance_rad")
    minimum_feature = _positive(top["minimum_feature_size_m"], "minimum_feature_size_m")
    if general_tolerance >= minimum_feature:
        raise PartContractViolation("general tolerance must be below minimum feature size")

    provenance = _mapping(top["parameter_provenance"], "parameter_provenance")
    if set(provenance) != provenance_targets:
        raise PartContractViolation(
            "parameter provenance mismatch; "
            f"missing={sorted(provenance_targets - set(provenance))}, "
            f"unknown={sorted(set(provenance) - provenance_targets)}"
        )
    for target, raw_record in provenance.items():
        record = _mapping(raw_record, f"parameter_provenance[{target}]")
        _exact_keys(record, {"source", "source_sha256", "confidence"}, "provenance record")
        _text(record["source"], "provenance source")
        _sha256(record["source_sha256"], "provenance source_sha256")
        confidence = _number(record["confidence"], "provenance confidence")
        if not 0.0 <= confidence <= 1.0:
            raise PartContractViolation("provenance confidence must be in [0, 1]")

    claim = _mapping(top["claim_boundary"], "claim_boundary")
    _exact_keys(claim, {"admitted_claims", "prohibited_claims"}, "claim_boundary")
    admitted = tuple(
        _identifier(item, "admitted claim")
        for item in _sequence(claim["admitted_claims"], "admitted_claims")
    )
    prohibited = tuple(
        _identifier(item, "prohibited claim")
        for item in _sequence(claim["prohibited_claims"], "prohibited_claims")
    )
    if not admitted or "physical_validation" not in prohibited:
        raise PartContractViolation(
            "claim boundary must admit at least one claim and prohibit physical_validation"
        )
    _unique(admitted, "admitted_claims")
    _unique(prohibited, "prohibited_claims")
