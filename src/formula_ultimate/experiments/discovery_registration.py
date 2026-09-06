"""Strict, content-addressed registration for the Work 098 software contract."""

from __future__ import annotations

import hashlib
import json
import math
import re
from functools import wraps
from typing import Any


SCHEMA = "discovery_contract_v1"
PROTOCOL_ID = "FU-WHOLE-VEHICLE-DISCOVERY-V1-2026-09-06"
CLASSES = {"software_fixture", "exploratory_simulation", "admitted_simulation"}
POOLS = {"exploration", "audit", "quality", "stepping_stone", "finalist"}
RESOURCES = {"proposals", "attempts", "geometry_executions", "cad_calls", "mesh_attempts", "elements", "dof",
             "solver_iterations", "cpu_s", "gpu_s", "wall_s", "peak_memory_bytes", "cache_hits"}
COUNTERS = RESOURCES - {"cpu_s", "gpu_s", "wall_s"}
PROFILE_KEYS = {"task_sha256", "energy_profile_sha256", "material_library_sha256",
                "representation_library_sha256", "operator_library_sha256", "environment_sha256"}


class DiscoveryViolation(ValueError):
    """Untrusted input or an illegal transition must not enter the ledger."""


def guarded(function):
    """Normalize malformed JSON shapes at public admission boundaries."""
    @wraps(function)
    def checked(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (KeyError, TypeError, AttributeError, StopIteration, OverflowError) as error:
            raise DiscoveryViolation(f"malformed contract input in {function.__name__}: {error}") from error
    return checked


def require(condition: bool, message: str) -> None:
    if not condition:
        raise DiscoveryViolation(message)


def exact(value: Any, keys: set[str], label: str) -> None:
    require(isinstance(value, dict) and set(value) == keys, f"{label}: schema mismatch")


def nonempty(value: Any, label: str) -> None:
    require(isinstance(value, str) and bool(value.strip()), f"{label}: nonempty string required")


def number(value: Any, label: str, minimum: float = 0) -> None:
    require(type(value) in (int, float) and math.isfinite(value) and value >= minimum,
            f"{label}: finite number >= {minimum} required")


def integer(value: Any, label: str, minimum: int = 0) -> None:
    require(type(value) is int and value >= minimum, f"{label}: integer >= {minimum} required")


def strings(value: Any, label: str, *, empty: bool = False) -> None:
    require(isinstance(value, list) and (empty or bool(value)), f"{label}: list required")
    for item in value:
        nonempty(item, label)
    require(len(value) == len(set(value)), f"{label}: duplicates")


def sha(value: Any, label: str = "identity") -> None:
    require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None,
            f"{label}: SHA-256 required")


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (ValueError, TypeError, OverflowError) as error:
        raise DiscoveryViolation("noncanonical or nonfinite data") from error


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def clone(value: Any) -> Any:
    return json.loads(canonical(value))


def strict_json(raw: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict:
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    try:
        value = json.loads(raw, object_pairs_hook=pairs)
        canonical(value)
        return value
    except (ValueError, TypeError) as error:
        raise DiscoveryViolation(f"invalid JSON: {error}") from error


def vector(value: Any, label: str) -> None:
    exact(value, RESOURCES, label)
    for key, item in value.items():
        (integer if key in COUNTERS else number)(item, f"{label}.{key}")


def zero_cost() -> dict:
    return {key: 0 for key in sorted(RESOURCES)}


def freeze(body: dict) -> dict:
    """A new freeze is a new registration, not permission to resume an old run."""
    envelope = {"body": clone(body), "registration_sha256": digest(body)}
    validate_registration(envelope)
    return envelope


@guarded
def validate_registration(envelope: dict, *, expected_sha256: str | None = None) -> dict:
    exact(envelope, {"body", "registration_sha256"}, "registration")
    sha(envelope["registration_sha256"])
    b = envelope["body"]
    require(digest(b) == envelope["registration_sha256"], "registration identity changed")
    if expected_sha256 is not None:
        require(expected_sha256 == envelope["registration_sha256"], "frozen registration mismatch")
    exact(b, {"schema", "protocol_id", "experiment_id", "evidence_class", "hypothesis",
              "alternatives", "independent_variables", "controls", "profiles", "treatments",
              "seeds", "partitions", "evaluators", "gates", "survivor_gates", "promotion_gates",
              "analysis", "budget", "audit", "execution", "criteria", "promotion_scope"}, "body")
    require(b["schema"] == SCHEMA and b["protocol_id"] == PROTOCOL_ID, "protocol version mismatch")
    require(b["evidence_class"] in CLASSES, "unknown evidence class")
    for key in ("experiment_id", "hypothesis", "promotion_scope"):
        nonempty(b[key], key)
    for key in ("alternatives", "independent_variables", "controls", "treatments"):
        strings(b[key], key)
    require(len(b["treatments"]) >= 2, "matched comparison needs at least two treatments")
    exact(b["profiles"], PROFILE_KEYS, "profiles")
    for key, value in b["profiles"].items():
        sha(value, key)
    require(isinstance(b["seeds"], list) and bool(b["seeds"]), "seeds required")
    for seed in b["seeds"]:
        integer(seed, "seed")
    require(len(b["seeds"]) == len(set(b["seeds"])), "duplicate seed")
    exact(b["partitions"], {"calibration", "training", "holdout"}, "partitions")
    seen = set()
    for key, values in b["partitions"].items():
        strings(values, key, empty=(key == "calibration"))
        require(not seen.intersection(values), "partition leakage")
        seen.update(values)
    evs = b["evaluators"]
    require(isinstance(evs, list) and bool(evs), "coverage registry required")
    evaluator_ids = set()
    for ev in evs:
        exact(ev, {"id", "implementation_sha256", "validation_sha256", "evidence_class",
                   "domains", "fidelities", "representations", "applicability", "independent_of"}, "evaluator")
        nonempty(ev["id"], "evaluator id")
        require(ev["id"] not in evaluator_ids, "duplicate evaluator")
        evaluator_ids.add(ev["id"])
        for key in ("implementation_sha256", "validation_sha256"):
            sha(ev[key], key)
        require(ev["evidence_class"] == b["evidence_class"], "fixture/evidence class mismatch")
        for key in ("domains", "fidelities", "representations"):
            strings(ev[key], key)
        nonempty(ev["applicability"], "applicability")
    evmap = {ev["id"]: ev for ev in evs}
    for ev in evs:
        other = ev["independent_of"]
        if other is not None:
            require(isinstance(other, str) and other in evmap and other != ev["id"], "independence reference")
            require(ev["implementation_sha256"] != evmap[other]["implementation_sha256"],
                    "independent evaluator must use different implementation")
    gates = b["gates"]
    require(isinstance(gates, list) and bool(gates), "gates required")
    gate_ids = set()
    for gate in gates:
        exact(gate, {"id", "kind", "domain", "fidelity", "evaluator_id", "metric", "unit",
                     "comparison", "threshold", "minimum_refinements", "error_limit", "evidence_type", "fidelity_rank"}, "gate")
        for key in ("id", "domain", "fidelity", "metric", "unit"):
            nonempty(gate[key], key)
        require(gate["id"] not in gate_ids, "duplicate gate")
        gate_ids.add(gate["id"])
        require(gate["kind"] in {"physics", "manufacturing", "holdout", "replay", "safety", "independent"}, "gate kind")
        require(gate["evaluator_id"] in evmap, "unknown evaluator")
        ev = evmap[gate["evaluator_id"]]
        require(gate["domain"] in ev["domains"] and gate["fidelity"] in ev["fidelities"], "gate outside coverage")
        if gate["kind"] == "independent":
            require(ev["independent_of"] is not None, "independent gate lacks independent evaluator")
        require(gate["comparison"] in {"le", "ge"}, "comparison required")
        number(gate["threshold"], "threshold", -1e300)
        number(gate["error_limit"], "error limit")
        integer(gate["minimum_refinements"], "refinements", 1)
        integer(gate["fidelity_rank"], "fidelity rank")
        require(gate["evidence_type"] in {"field", "scalar", "check"}, "evidence type")
        if gate["evidence_type"] == "field":
            require(gate["minimum_refinements"] >= 3, "field evidence needs three refinements")
    gate_map = {g["id"]: g for g in gates}
    for key in ("survivor_gates", "promotion_gates"):
        strings(b[key], key)
        require(set(b[key]) <= gate_ids, "unknown promotion gate")
        kinds = {gate_map[g]["kind"] for g in b[key]}
        require({"physics", "manufacturing", "holdout", "replay"} <= kinds, "incomplete survivor gates")
    require(set(b["survivor_gates"]) <= set(b["promotion_gates"]), "promotion drops survivor gates")
    require({"independent", "safety"} <= {gate_map[g]["kind"] for g in b["promotion_gates"]}, "incomplete promotion gates")
    for gate_id in b["promotion_gates"]:
        g = gate_map[gate_id]
        if g["kind"] == "independent":
            source = evmap[g["evaluator_id"]]["independent_of"]
            prior = [gate_map[x] for x in b["survivor_gates"] if gate_map[x]["kind"] == "physics"
                     and gate_map[x]["evaluator_id"] == source and gate_map[x]["domain"] == g["domain"]]
            require(bool(prior) and all(g["fidelity_rank"] > x["fidelity_rank"] for x in prior),
                    "independent promotion must exceed registered source fidelity")
    a = b["analysis"]
    exact(a, {"primary_metric", "unit", "direction", "minimum_effect", "secondary_metrics", "sample_size",
              "sample_size_rationale", "test", "alpha", "multiplicity", "uncertainty", "controller_policy"}, "analysis")
    for key in ("primary_metric", "unit", "sample_size_rationale", "test", "multiplicity", "uncertainty", "controller_policy"):
        nonempty(a[key], key)
    require(a["direction"] in {"minimize", "maximize"}, "metric direction")
    number(a["minimum_effect"], "minimum effect")
    require(a["minimum_effect"] > 0, "minimum meaningful effect must be positive")
    strings(a["secondary_metrics"], "secondary metrics", empty=True)
    integer(a["sample_size"], "sample size", 1)
    require(a["sample_size"] == len(b["seeds"]), "sample size must match paired seeds")
    number(a["alpha"], "alpha")
    require(0 < a["alpha"] < 1, "alpha outside (0,1)")
    budget = b["budget"]
    exact(budget, {"primary_resource", "pools", "retry_limit", "cache_policy", "overshoot_policy", "recovery_policy"}, "budget")
    require(budget["primary_resource"] in {"cpu_s", "wall_s"}, "unsupported primary resource")
    exact(budget["pools"], POOLS, "budget pools")
    for pool, limits in budget["pools"].items():
        vector(limits, pool)
        require(limits["attempts"] > 0 and limits[budget["primary_resource"]] > 0, "pool needs nonzero opportunity")
    integer(budget["retry_limit"], "retry limit")
    require(budget["cache_policy"] == "same_context_full_charge", "unsupported cache policy")
    require(budget["overshoot_policy"] == "record_and_stop", "unsupported overshoot policy")
    require(budget["recovery_policy"] == "started_charge_reservation_unstarted_charge_attempt", "unsupported recovery policy")
    exact(b["audit"], {"sample_per_stratum", "seed", "reporting"}, "audit")
    integer(b["audit"]["sample_per_stratum"], "audit sample", 1)
    integer(b["audit"]["seed"], "audit seed")
    require(b["audit"]["reporting"] == "within_stratum_unknown_bounds", "unsupported audit reporting")
    require(canonical(b["execution"]) == canonical({"workers": 1, "ordering": "registered_serial", "reallocation": "none",
                               "stopping": "budget_or_protocol_failure", "holdout_feedback": False}), "execution policy mismatch")
    exact(b["criteria"], {"success", "failure", "unresolved", "leakage", "reproduction"}, "criteria")
    for key, value in b["criteria"].items():
        nonempty(value, key)
    return clone(b)
