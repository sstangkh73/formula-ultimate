"""Scoped evidence admission, independent outcome dimensions, and legacy boundaries."""

from __future__ import annotations

from .discovery_registration import (
    DiscoveryViolation, canonical, clone, digest, exact, integer, nonempty, number,
    require, sha, strings, guarded,
)


CONTEXT_KEYS = {"candidate_id", "genotype_sha256", "geometry_sha256", "material_sha256",
                "boundary_sha256", "controller_sha256", "environment_sha256", "task_sha256",
                "registration_sha256"}
STATES = {
    "representation": {"generated", "representation_invalid", "geometry_measured"},
    "boundary": {"not_evaluated", "boundary_resolved", "boundary_unresolved"},
    "physics": {"not_evaluated", "numerically_unresolved", "physically_failed", "physically_feasible"},
    "manufacturing": {"not_evaluated", "manufacturing_unresolved", "manufacturing_compatible", "manufacturing_incompatible"},
    "gate": {"not_evaluated", "numerically_unresolved", "failed", "passed"},
}
FAILURE_REASONS = {"solver_divergence", "timeout", "unsupported_physics", "unsupported_representation",
                   "mesh_failure", "error_gate", "lost_output"}


def validate_context(context: dict) -> None:
    exact(context, CONTEXT_KEYS, "context")
    nonempty(context["candidate_id"], "candidate id")
    for key in CONTEXT_KEYS - {"candidate_id"}:
        if key in {"geometry_sha256", "boundary_sha256"} and context[key] is None:
            continue
        sha(context[key], key)


@guarded
def validate_candidate(candidate: dict, registration: dict, registration_sha256: str) -> None:
    exact(candidate, {"id", "parents", "genotype", "context", "representation", "treatment",
                      "seed", "partition", "dataset_id", "mutation_trace"}, "candidate")
    validate_context(candidate["context"])
    c = candidate["context"]
    require(candidate["id"] == c["candidate_id"], "candidate identity mismatch")
    require(c["registration_sha256"] == registration_sha256, "candidate registration mismatch")
    require(c["genotype_sha256"] == digest(candidate["genotype"]), "genotype identity mismatch")
    require(isinstance(candidate["genotype"], dict) and bool(candidate["genotype"]), "executable genotype declaration required")
    require(len(canonical(candidate)) <= 1024 * 1024, "candidate declaration exceeds V1 byte bound")
    strings(candidate["parents"], "parents", empty=True)
    require(candidate["id"] not in candidate["parents"], "self ancestry")
    require(isinstance(candidate["mutation_trace"], list), "mutation trace required")
    require(not candidate["parents"] or bool(candidate["mutation_trace"]), "descendant needs mutation trace")
    for item in candidate["mutation_trace"]:
        exact(item, {"operator", "parameters"}, "mutation")
        nonempty(item["operator"], "operator")
        require(isinstance(item["parameters"], dict), "operator parameters required")
    nonempty(candidate["representation"], "representation")
    require(candidate["treatment"] in registration["treatments"], "unregistered treatment")
    integer(candidate["seed"], "candidate seed")
    require(candidate["seed"] in registration["seeds"], "unregistered seed")
    require(candidate["partition"] in registration["partitions"], "unknown partition")
    require(candidate["dataset_id"] in registration["partitions"][candidate["partition"]], "dataset/partition mismatch")
    for key in ("task_sha256", "environment_sha256"):
        require(c[key] == registration["profiles"][key], f"external {key} changed")


def initial_state(candidate: dict, promotion_scope: str) -> dict:
    return {"context": clone(candidate["context"]), "representation": "generated",
            "boundary": "not_evaluated", "physics": {}, "manufacturing": {}, "gate": {},
            "promotion": {promotion_scope: {"status": "not_ready", "use": promotion_scope,
                                            "scientific_survivor": False, "physical_validation": False}}, "history": []}


def gate_for(registration: dict, gate_id: str) -> dict:
    matches = [g for g in registration["gates"] if g["id"] == gate_id]
    require(len(matches) == 1, "unknown gate identity")
    return matches[0]


@guarded
def admit_artifact(artifact: dict, candidate: dict, context: dict, gate: dict, registration: dict) -> bool:
    exact(artifact, {"body", "sha256"}, "artifact")
    b = artifact["body"]
    require(artifact["sha256"] == digest(b), "artifact hash mismatch")
    exact(b, {"evidence_class", "evaluator_id", "implementation_sha256", "validation_sha256",
              "context_sha256", "gate_id", "dataset_id", "metric", "unit", "value", "converged",
              "error", "refinements", "evidence_type", "details"}, "artifact body")
    ev = next(e for e in registration["evaluators"] if e["id"] == gate["evaluator_id"])
    for key in ("implementation_sha256", "validation_sha256", "evidence_class"):
        require(b[key] == ev[key], f"artifact {key} mismatch")
    require(b["evidence_class"] == registration["evidence_class"], "evidence class leakage")
    require(b["context_sha256"] == digest(context), "artifact causal context mismatch")
    require(b["gate_id"] == gate["id"] and b["evaluator_id"] == gate["evaluator_id"], "artifact gate/evaluator mismatch")
    require(candidate["representation"] in ev["representations"], "representation outside evaluator coverage")
    require(b["dataset_id"] in registration["partitions"]["holdout"] if gate["kind"] == "holdout"
            else b["dataset_id"] == candidate["dataset_id"], "artifact dataset scope mismatch")
    require(b["metric"] == gate["metric"] and b["unit"] == gate["unit"], "metric or SI unit mismatch")
    require(b["evidence_type"] == gate["evidence_type"], "field/scalar evidence scope mismatch")
    number(b["value"], "measured value", -1e300)
    number(b["error"], "measured error")
    require(type(b["converged"]) is bool and b["converged"], "solver not converged")
    require(b["error"] <= gate["error_limit"], "numerical error gate failed")
    levels = b["refinements"]
    require(isinstance(levels, list) and len(levels) >= gate["minimum_refinements"], "insufficient refinement evidence")
    for level in levels:
        integer(level, "refinement level", 1)
    require(all(a < z for a, z in zip(levels, levels[1:])), "non-increasing refinement levels")
    require(isinstance(b["details"], dict) and bool(b["details"]), "evidence limitations/details required")
    if registration["evidence_class"] == "admitted_simulation":
        require(b["details"].get("synthetic_only") is not True, "synthetic fixture cannot be admitted science")
        if gate["evidence_type"] == "field":
            require(b["details"].get("no_field_solver_executed") is not True, "field solver evidence missing")
    return b["value"] <= gate["threshold"] if gate["comparison"] == "le" else b["value"] >= gate["threshold"]


@guarded
def apply_outcome(snapshot: dict, candidate: dict, result: dict, registration: dict) -> dict:
    """Return a new state; never mutate a caller-owned candidate or previous result."""
    exact(result, {"dimension", "scope", "status", "reason", "context", "artifact"}, "outcome")
    dim = result["dimension"]
    require(isinstance(dim, str) and dim in STATES, "unknown outcome dimension")
    require(result["status"] in STATES[dim], "unknown outcome state")
    nonempty(result["scope"], "outcome scope")
    nonempty(result["reason"], "outcome reason")
    context = result["context"]
    validate_context(context)
    expected = clone(snapshot["context"])
    # The first measured geometry/boundary seals that identity once. Later changes need a descendant.
    fill = "geometry_sha256" if dim == "representation" and result["status"] == "geometry_measured" else (
        "boundary_sha256" if dim == "boundary" and result["status"] == "boundary_resolved" else None)
    if fill is not None and expected[fill] is None:
        sha(context[fill], fill)
        expected[fill] = context[fill]
    require(context == expected, "outcome causal context changed")
    state = clone(snapshot)
    state["context"] = clone(context)
    if dim in {"representation", "boundary"}:
        require(result["scope"] == dim, "geometry/boundary scope mismatch")
        require(result["artifact"] is not None, "geometry/boundary diagnostic artifact required")
        artifact = result["artifact"]
        exact(artifact, {"body", "sha256"}, "diagnostic artifact")
        require(digest(artifact["body"]) == artifact["sha256"], "diagnostic artifact hash mismatch")
        body = artifact["body"]
        exact(body, {"context_sha256", "evidence_class", "details"}, "diagnostic body")
        require(body["context_sha256"] == digest(context) and body["evidence_class"] == registration["evidence_class"],
                "diagnostic context/class mismatch")
        require(isinstance(body["details"], dict) and bool(body["details"]), "diagnostic details required")
        if dim == "representation":
            require(state[dim] == "generated" and result["status"] != "generated", "representation already resolved")
            if result["status"] == "geometry_measured":
                sha(context["geometry_sha256"], "measured geometry")
        else:
            require(state["representation"] == "geometry_measured", "binding before geometry")
            require(state[dim] != "boundary_resolved", "boundary already sealed")
            if result["status"] == "boundary_resolved":
                sha(context["boundary_sha256"], "resolved boundary")
        state[dim] = result["status"]
    else:
        gate = gate_for(registration, result["scope"])
        expected_dim = gate["kind"] if gate["kind"] in {"physics", "manufacturing"} else "gate"
        require(dim == expected_dim, "outcome dimension differs from gate")
        passed = result["status"] in {"physically_feasible", "manufacturing_compatible", "passed"}
        failed = result["status"] in {"physically_failed", "manufacturing_incompatible", "failed"}
        if passed or failed:
            require(state["representation"] == "geometry_measured" and state["boundary"] == "boundary_resolved",
                    "evidence without measured geometry and resolved boundary")
            admitted_pass = admit_artifact(result["artifact"], candidate, context, gate, registration)
            require(admitted_pass == passed, "outcome disagrees with registered threshold")
        else:
            require(result["artifact"] is None, "unresolved evidence cannot be admitted as a gate result")
            if result["status"] != "not_evaluated":
                require(result["reason"] in FAILURE_REASONS, "unresolved reason required")
            else:
                require(result["reason"] in {"budget_exhausted", "cancelled", "unsupported_physics", "unsupported_representation"},
                        "not-evaluated reason required")
        state[dim][gate["id"]] = clone(result)
    # Promotion is a decision about the current evidence set, not an immortal property.
    state["promotion"] = {use: {"status": "not_ready", "use": use,
                                "scientific_survivor": False, "physical_validation": False} for use in state["promotion"]}
    state["history"].append(clone(result))
    return state


def exploration_permission(snapshot: dict, declaration: dict) -> dict:
    exact(declaration, {"missing_domains", "approximations", "interfaces_sha256", "scope"}, "exploratory assembly")
    strings(declaration["missing_domains"], "missing domains", empty=True)
    strings(declaration["approximations"], "approximations", empty=True)
    sha(declaration["interfaces_sha256"])
    nonempty(declaration["scope"], "assembly scope")
    require(snapshot["representation"] == "geometry_measured" and snapshot["boundary"] == "boundary_resolved",
            "exploratory assembly requires traceable geometry and resolved interfaces")
    return {"eligible": True, "scope": declaration["scope"], "promotion_allowed": False,
            "declaration_sha256": digest(declaration)}


@guarded
def promotion_decision(snapshot: dict, registration: dict, target: str, use: str) -> dict:
    require(target in {"candidate_survivor", "promotion_ready"}, "unknown promotion target")
    nonempty(use, "declared use")
    require(use == registration["promotion_scope"], "unregistered promotion use")
    require(registration["evidence_class"] != "exploratory_simulation", "exploratory evidence cannot promote")
    required = registration["survivor_gates" if target == "candidate_survivor" else "promotion_gates"]
    results = {**snapshot["physics"], **snapshot["manufacturing"], **snapshot["gate"]}
    missing = [g for g in required if g not in results or results[g]["status"] not in {
        "physically_feasible", "manufacturing_compatible", "passed"}]
    require(not missing, f"missing or failed promotion evidence: {missing}")
    for g in required:
        require(results[g]["context"] == snapshot["context"], "stale promotion context")
    scientific = registration["evidence_class"] == "admitted_simulation"
    return {"status": target, "use": use, "evidence_class": registration["evidence_class"],
            "scientific_survivor": scientific, "physical_validation": False,
            "context_sha256": digest(snapshot["context"]),
            "evidence_sha256": digest({g: results[g] for g in required})}


def legacy_annotation(work: str, raw: dict) -> dict:
    """Do not turn a legacy benchmark's success assertion into physical admission."""
    require(isinstance(raw, dict), "legacy result object required")
    if work == "095":
        require(raw.get("status") in {"accepted", "repaired", "rejected"}, "unknown Work 095 label")
        return {"physics": "not_evaluated", "manufacturing": "not_evaluated",
                "evidence_class": "software_fixture", "reason": "synthetic_preperformance_gate",
                "legacy_sha256": digest(raw), "legacy_status": raw["status"]}
    if work == "097":
        require(raw.get("status") in {"passed", "invalid"}, "unknown Work 097 label")
        divergence = raw.get("status") == "invalid" and raw.get("reason") == "solver_divergence"
        return {"physics": "numerically_unresolved" if divergence else "not_evaluated",
                "manufacturing": "not_evaluated", "evidence_class": "reduced_order_cross_method_benchmark",
                "reason": "solver_divergence" if divergence else "scalar_benchmark_not_field_admission",
                "legacy_sha256": digest(raw), "legacy_status": raw["status"]}
    raise DiscoveryViolation("unsupported legacy adapter")
