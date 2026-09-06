"""Deterministic bounded multi-disposition quality-diversity archive for Work 099."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from .executable_morphology import MorphologyViolation, digest


DISPOSITIONS = ("feasible", "failed", "unresolved")
EVIDENCE_SCOPE = "morphology_software_fixture_only"


def niche_key(descriptors: Mapping[str, Any]) -> str:
    expected = {"part_count", "interface_cycle_rank", "branch_node_count", "terminal_domain_count"}
    if set(descriptors) != expected or any(isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in descriptors.values()):
        raise MorphologyViolation("archive descriptors are invalid")
    return digest({key: descriptors[key] for key in sorted(expected)})


def validate_record(record: Mapping[str, Any]) -> None:
    expected = {"candidate_id", "context_sha256", "functional_signature", "descriptors", "disposition", "quality", "margin", "cost", "novelty", "parents", "evidence_scope"}
    if set(record) != expected:
        raise MorphologyViolation("archive record schema mismatch")
    if not isinstance(record["candidate_id"], str) or not record["candidate_id"]:
        raise MorphologyViolation("archive candidate identity is missing")
    for key in ("context_sha256", "functional_signature"):
        if not isinstance(record[key], str) or len(record[key]) != 64:
            raise MorphologyViolation(f"archive {key} must be SHA-256")
    niche_key(record["descriptors"])
    if record["disposition"] not in DISPOSITIONS:
        raise MorphologyViolation("archive disposition is invalid")
    for key in ("quality", "margin"):
        value = record[key]
        if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float))):
            raise MorphologyViolation(f"archive {key} must be numeric or null")
    if record["disposition"] == "feasible" and record["quality"] is None:
        raise MorphologyViolation("feasible archive record needs quality")
    if record["disposition"] == "failed" and record["margin"] is None:
        raise MorphologyViolation("failed archive record needs a measured margin")
    if isinstance(record["cost"], bool) or not isinstance(record["cost"], (int, float)) or record["cost"] < 0:
        raise MorphologyViolation("archive cost must be non-negative")
    if isinstance(record["novelty"], bool) or not isinstance(record["novelty"], (int, float)) or record["novelty"] < 0:
        raise MorphologyViolation("archive novelty must be non-negative")
    if not isinstance(record["parents"], list) or any(not isinstance(item, str) or not item for item in record["parents"]):
        raise MorphologyViolation("archive ancestry is invalid")
    if record["evidence_scope"] != EVIDENCE_SCOPE:
        raise MorphologyViolation("archive evidence scope cannot imply physical feasibility")


def _rank(record: Mapping[str, Any]) -> tuple[Any, ...]:
    if record["disposition"] == "feasible":
        return (-float(record["quality"]), -float(record["novelty"]), float(record["cost"]), record["candidate_id"])
    if record["disposition"] == "failed":
        return (-float(record["margin"]), -float(record["novelty"]), float(record["cost"]), record["candidate_id"])
    return (float(record["cost"]), -float(record["novelty"]), record["candidate_id"])


class MorphologyArchive:
    """Bound every niche/disposition; the immutable ledger retains evicted attempts."""

    def __init__(self, capacities: Mapping[str, int], reproduction_caps: Mapping[str, int]):
        if set(capacities) != set(DISPOSITIONS) or set(reproduction_caps) != set(DISPOSITIONS):
            raise MorphologyViolation("archive disposition policy mismatch")
        for disposition in DISPOSITIONS:
            capacity, cap = capacities[disposition], reproduction_caps[disposition]
            if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 1:
                raise MorphologyViolation("archive capacity must be positive")
            if isinstance(cap, bool) or not isinstance(cap, int) or not 0 <= cap <= capacity:
                raise MorphologyViolation("reproduction cap is outside capacity")
        self.capacities = dict(capacities)
        self.reproduction_caps = dict(reproduction_caps)
        self._niches: dict[str, dict[str, list[dict[str, Any]]]] = {}

    def update(self, record: Mapping[str, Any]) -> dict[str, Any]:
        validate_record(record)
        key = niche_key(record["descriptors"])
        slots = self._niches.setdefault(key, {disposition: [] for disposition in DISPOSITIONS})
        disposition = record["disposition"]
        before = {item["candidate_id"] for item in slots[disposition]}
        if record["candidate_id"] in before:
            raise MorphologyViolation("archive candidate cannot be overwritten")
        candidates = slots[disposition] + [deepcopy(dict(record))]
        candidates.sort(key=_rank)
        slots[disposition] = candidates[: self.capacities[disposition]]
        retained = record["candidate_id"] in {item["candidate_id"] for item in slots[disposition]}
        evicted = sorted((before | {record["candidate_id"]}) - {item["candidate_id"] for item in slots[disposition]})
        return {"candidate_id": record["candidate_id"], "niche": key, "disposition": disposition, "retained": retained, "evicted": evicted, "archive_state_sha256": digest(self.snapshot())}

    def select_reproducers(self) -> dict[str, list[str]]:
        selected = {disposition: [] for disposition in DISPOSITIONS}
        for key in sorted(self._niches):
            for disposition in DISPOSITIONS:
                selected[disposition].extend(item["candidate_id"] for item in self._niches[key][disposition][: self.reproduction_caps[disposition]])
        return selected

    def snapshot(self) -> dict[str, Any]:
        niches = []
        for key in sorted(self._niches):
            niches.append({"niche": key, **{disposition: deepcopy(self._niches[key][disposition]) for disposition in DISPOSITIONS}})
        result = {"schema": "bounded_morphology_archive_v1", "evidence_scope": EVIDENCE_SCOPE, "capacities": dict(self.capacities), "reproduction_caps": dict(self.reproduction_caps), "niches": niches}
        result["archive_sha256"] = digest(result)
        return result
