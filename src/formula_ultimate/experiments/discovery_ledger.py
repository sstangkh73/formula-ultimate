"""Single-writer event ledger with replayed admission and resource settlement."""

from __future__ import annotations

from contextlib import contextmanager
import os
from pathlib import Path

from .discovery_audit import proxy_audit, ranked_selection, stratified_sample
from .discovery_evidence import (
    apply_outcome, exploration_permission, gate_for, initial_state, promotion_decision, validate_candidate,
)
from .discovery_registration import (
    DiscoveryViolation, POOLS, RESOURCES, canonical, clone, digest, exact, nonempty,
    require, sha, strict_json, validate_registration, vector, zero_cost, guarded,
)


ZERO = "0" * 64


def account_key(candidate: dict, pool: str) -> str:
    return digest([candidate["treatment"], candidate["seed"], pool])


def add_cost(previous: dict, cost: dict) -> dict:
    combined = {k: max(previous[k], cost[k]) if k == "peak_memory_bytes" else previous[k] + cost[k]
                for k in RESOURCES}
    vector(combined, "accumulated cost")
    return combined


def fits(cost: dict, limits: dict) -> bool:
    return all(cost[k] <= limits[k] for k in RESOURCES)


def fresh_state() -> dict:
    return {"candidates": {}, "states": {}, "attempts": {}, "accounts": {}, "selections": [],
            "permissions": [], "quarantines": [], "deferrals": [], "stopped": False, "accounting_complete": True}


def scientific_summary(state: dict) -> dict:
    reasons = []
    if state["stopped"]:
        reasons.append("campaign_stopped")
    if not state["accounting_complete"]:
        reasons.append("unknown_actual_cost")
    if any(a["disposition"] == "pending" for a in state["attempts"].values()):
        reasons.append("pending_cost")
    recorded = sum(d["scientific_survivor"] for s in state["states"].values() for d in s["promotion"].values())
    return {"scientific_survivors": 0 if reasons else recorded, "accounting_admissible": not reasons,
            "blocking_reasons": reasons, "physical_validation": False}


def selection(state: dict, registration: dict, pool: str, gate_id: str) -> dict:
    require(pool in {"audit", "quality", "stepping_stone"}, "selection pool")
    gate = gate_for(registration, gate_id)
    require(gate["kind"] == "physics", "selection needs a physical proxy gate")
    population = []
    contexts = {}
    # Separate treatment/seed strata: no family gains another treatment's opportunity.
    for cid, candidate in sorted(state["candidates"].items()):
        s = state["states"][cid]
        if candidate["partition"] != "training" or s["representation"] != "geometry_measured" or s["boundary"] != "boundary_resolved":
            continue
        if any(gate_for(registration, g)["kind"] == "holdout" for g in s["gate"]):
            continue
        result = s["physics"].get(gate_id)
        if pool == "stepping_stone" and (result is None or result["status"] not in {"physically_failed", "numerically_unresolved"}):
            continue
        value = result["artifact"]["body"]["value"] if result and result["artifact"] is not None else None
        population.append({"candidate_id": cid, "stratum": digest([candidate["treatment"], candidate["seed"],
                                                                    candidate["representation"]]), "proxy_score": value})
        contexts[cid] = digest(s["context"])
    if pool == "audit":
        chosen = stratified_sample(population, seed=registration["audit"]["seed"],
                                   per_stratum=registration["audit"]["sample_per_stratum"])
    else:
        # Quality opportunity is allocated independently for every treatment/seed.
        chosen_ids = []
        for treatment in registration["treatments"]:
            for seed in registration["seeds"]:
                sub = [r for r in population if state["candidates"][r["candidate_id"]]["treatment"] == treatment
                       and state["candidates"][r["candidate_id"]]["seed"] == seed]
                count = registration["budget"]["pools"][pool]["attempts"]
                ids = ranked_selection(sub, count=count, minimize=gate["comparison"] == "le")
                if pool == "stepping_stone":
                    # Give unscored unresolved hypotheses a deterministic bounded opportunity too.
                    ids += sorted(r["candidate_id"] for r in sub if r["proxy_score"] is None)[:max(0, count - len(ids))]
                chosen_ids += ids
        chosen = {"selected": [{"candidate_id": cid} for cid in chosen_ids]}
    payload = {"pool": pool, "gate_id": gate_id, "population": population, "contexts": contexts, "selection": chosen}
    return {**payload, "selection_sha256": digest(payload)}


@guarded
def reduce_event(state: dict, event: dict, registration: dict, registration_sha256: str) -> None:
    require(isinstance(event, dict), "event object required")
    kind = event.get("type")
    require(not state["stopped"] or kind == "quarantine", "campaign stopped by resource overshoot")
    if kind == "candidate":
        exact(event, {"type", "candidate"}, "candidate event")
        c = event["candidate"]
        validate_candidate(c, registration, registration_sha256)
        require(c["id"] not in state["candidates"], "candidate already exists; append a descendant")
        for parent in c["parents"]:
            require(parent in state["candidates"], "unknown parent")
            p = state["candidates"][parent]
            require((p["treatment"], p["seed"]) == (c["treatment"], c["seed"]), "cross-treatment ancestry leakage")
            require(p["partition"] != "holdout" and not any(gate_for(registration, g)["kind"] == "holdout"
                    for g in state["states"][parent]["gate"]), "holdout feedback prohibited")
        key = account_key(c, "exploration")
        cost = zero_cost()
        cost["proposals"] = 1
        used = add_cost(state["accounts"].get(key, zero_cost()), cost)
        require(fits(used, registration["budget"]["pools"]["exploration"]), "proposal budget exhausted")
        state["accounts"][key] = used
        state["candidates"][c["id"]] = clone(c)
        state["states"][c["id"]] = initial_state(c, registration["promotion_scope"])
    elif kind == "reserve":
        exact(event, {"type", "id", "candidate_id", "pool", "dimension", "scope", "cost", "retry_of", "cache_of",
                      "selection_sha256"}, "reservation")
        nonempty(event["id"], "attempt id")
        require(event["id"] not in state["attempts"], "duplicate attempt")
        require(not any(a["disposition"] == "pending" for a in state["attempts"].values()), "serial writer has pending attempt")
        require(event["candidate_id"] in state["candidates"], "unknown candidate")
        require(event["pool"] in POOLS, "unknown budget pool")
        require(event["dimension"] in {"representation", "boundary", "physics", "manufacturing", "gate"}, "reservation dimension")
        nonempty(event["scope"], "attempt scope")
        c = state["candidates"][event["candidate_id"]]
        s = state["states"][c["id"]]
        if event["dimension"] in {"representation", "boundary"}:
            require(event["scope"] == event["dimension"], "reserved diagnostic scope")
        else:
            g = gate_for(registration, event["scope"])
            require(event["dimension"] == (g["kind"] if g["kind"] in {"physics", "manufacturing"} else "gate"), "reserved gate dimension")
        vector(event["cost"], "reservation cost")
        require(event["cost"]["attempts"] == 1 and event["cost"]["proposals"] == 0, "reservation attempt/proposal accounting")
        if event["pool"] in {"audit", "quality", "stepping_stone"}:
            matches = [x for x in state["selections"] if x["selection_sha256"] == event["selection_sha256"]]
            require(len(matches) == 1, "missing selection before allocation")
            x = matches[0]
            require(x["pool"] == event["pool"] and c["id"] in {r["candidate_id"] for r in x["selection"]["selected"]}, "not selected for pool")
            require(x["contexts"][c["id"]] == digest(s["context"]), "selection context stale")
        else:
            require(event["selection_sha256"] is None, "unexpected selection")
        require(event["retry_of"] is None or event["cache_of"] is None, "retry and cache are distinct operations")
        prior = [a for a in state["attempts"].values() if a["reservation"]["candidate_id"] == c["id"]
                 and a["context"] == s["context"] and (a["reservation"]["dimension"], a["reservation"]["scope"])
                 == (event["dimension"], event["scope"])]
        if prior:
            require(event["retry_of"] is not None or event["cache_of"] is not None,
                    "repeat evaluation needs explicit retry/cache; changed design needs descendant")
            if event["retry_of"] is not None:
                require(event["retry_of"] == prior[-1]["reservation"]["id"], "retry must follow latest attempt")
        depth = 0
        for field in ("retry_of", "cache_of"):
            source_id = event[field]
            if source_id is None:
                continue
            require(source_id in state["attempts"], "unknown source attempt")
            a = state["attempts"][source_id]
            require(a["disposition"] != "pending", "source attempt still pending")
            require(a["reservation"]["candidate_id"] == c["id"] and a["context"] == s["context"], "retry/cache context mismatch")
            require((a["reservation"]["dimension"], a["reservation"]["scope"]) == (event["dimension"], event["scope"]), "retry/cache scope mismatch")
            if field == "retry_of":
                require(a.get("result") is None or a["result"]["status"] in {"numerically_unresolved", "manufacturing_unresolved", "not_evaluated", "boundary_unresolved"}, "retry source not unresolved")
                depth = a["retry_depth"] + 1
                require(depth <= registration["budget"]["retry_limit"], "retry limit exceeded")
            else:
                require(a.get("result") is not None and a["result"]["artifact"] is not None, "cache needs measured source result")
                require(event["dimension"] not in {"representation", "boundary"}, "cache only for scoped evaluation")
                require(event["cost"]["cache_hits"] == 1, "cache hit must be reserved")
                charge = {**a["charged"], "cache_hits": 1}
                require(fits(charge, event["cost"]), "cache cannot avoid full registered charge")
        if event["cache_of"] is None:
            require(event["cost"]["cache_hits"] == 0, "non-cache reservation has cache hit")
        key = account_key(c, event["pool"])
        require(fits(add_cost(state["accounts"].get(key, zero_cost()), event["cost"]),
                     registration["budget"]["pools"][event["pool"]]), "budget exhausted before invocation")
        state["attempts"][event["id"]] = {"reservation": clone(event), "context": clone(s["context"]),
                                          "started": False, "disposition": "pending", "retry_depth": depth}
    elif kind == "defer":
        exact(event, {"type", "candidate_id", "pool", "dimension", "scope", "cost", "reason"}, "deferral")
        require(event["candidate_id"] in state["candidates"], "unknown deferred candidate")
        require(event["pool"] in POOLS, "unknown deferral pool")
        require(event["reason"] == "budget_exhausted", "deferral needs actual exhausted budget")
        require(event["dimension"] in {"physics", "manufacturing", "gate"}, "deferred scope must be an evaluation")
        vector(event["cost"], "deferred requested cost")
        require(event["cost"]["attempts"] == 1 and event["cost"]["proposals"] == 0, "deferred attempt cost")
        cid = event["candidate_id"]
        c = state["candidates"][cid]
        key = account_key(c, event["pool"])
        require(not fits(add_cost(state["accounts"].get(key, zero_cost()), event["cost"]),
                         registration["budget"]["pools"][event["pool"]]), "budget is not exhausted")
        require(not any(a["disposition"] == "pending" for a in state["attempts"].values()), "deferral while operation pending")
        result = {"dimension": event["dimension"], "scope": event["scope"], "status": "not_evaluated",
                  "reason": "budget_exhausted", "context": state["states"][cid]["context"], "artifact": None}
        state["states"][cid] = apply_outcome(state["states"][cid], c, result, registration)
        state["deferrals"].append({**clone(event), "disposition": "budget_exhausted"})
    elif kind == "start":
        exact(event, {"type", "id"}, "start")
        require(event["id"] in state["attempts"], "unreserved start")
        a = state["attempts"][event["id"]]
        require(a["disposition"] == "pending" and not a["started"], "attempt already started/settled")
        a["started"] = True
    elif kind in {"settle", "recover"}:
        exact(event, {"type", "id", "observed_cost", "result", "diagnostics"} if kind == "settle" else {"type", "id"}, "settlement")
        require(event["id"] in state["attempts"], "unreserved settlement")
        a = state["attempts"][event["id"]]
        require(a["disposition"] == "pending", "duplicate settlement")
        reservation = a["reservation"]
        cid = reservation["candidate_id"]
        c = state["candidates"][cid]
        if kind == "recover":
            cost = clone(reservation["cost"]) if a["started"] else {**zero_cost(), "attempts": 1}
            a.update(observed_cost=None, result=None, diagnostics={"reason": "lost_output" if a["started"] else "cancelled_before_start"})
            state["accounting_complete"] = state["accounting_complete"] and not a["started"]
            dim = reservation["dimension"]
            if dim in {"physics", "manufacturing", "gate"}:
                status = ({"physics": "numerically_unresolved", "manufacturing": "manufacturing_unresolved", "gate": "numerically_unresolved"}[dim]
                          if a["started"] else "not_evaluated")
                result = {"dimension": dim, "scope": reservation["scope"], "status": status,
                          "reason": "lost_output" if a["started"] else "cancelled", "context": a["context"], "artifact": None}
                state["states"][cid] = apply_outcome(state["states"][cid], c, result, registration)
                a["result"] = result
            a["disposition"] = "cancelled"
        else:
            require(a["started"], "result before invocation")
            vector(event["observed_cost"], "observed cost")
            observed = event["observed_cost"]
            require(observed["attempts"] == 1 and observed["proposals"] == 0, "settlement opportunity accounting")
            require(isinstance(event["diagnostics"], dict), "diagnostics object required")
            result = event["result"]
            require((result.get("dimension"), result.get("scope")) == (reservation["dimension"], reservation["scope"]), "result differs from reservation")
            cost = clone(observed)
            if reservation["cache_of"] is not None:
                source = state["attempts"][reservation["cache_of"]]
                require(result == source["result"], "cache result changed")
                require(observed["cache_hits"] == 1, "missing measured cache hit")
                cost = {k: max(cost[k], source["charged"][k]) for k in RESOURCES}
                cost["cache_hits"] = 1
            else:
                require(observed["cache_hits"] == 0, "unexpected measured cache hit")
            state["states"][cid] = apply_outcome(state["states"][cid], c, result, registration)
            a.update(observed_cost=clone(observed), result=clone(result), diagnostics=clone(event["diagnostics"]), disposition="completed")
        key = account_key(c, reservation["pool"])
        used = add_cost(state["accounts"].get(key, zero_cost()), cost)
        state["accounts"][key] = used
        a["charged"] = cost
        a["overshoot"] = not fits(cost, reservation["cost"]) or not fits(used, registration["budget"]["pools"][reservation["pool"]])
        state["stopped"] = state["stopped"] or a["overshoot"]
    elif kind == "select":
        exact(event, {"type", "pool", "gate_id"}, "selection event")
        result = selection(state, registration, event["pool"], event["gate_id"])
        require(not any(x["selection_sha256"] == result["selection_sha256"] for x in state["selections"]), "duplicate selection event")
        state["selections"].append(result)
    elif kind == "explore":
        exact(event, {"type", "candidate_id", "declaration"}, "exploration event")
        require(event["candidate_id"] in state["states"], "unknown assembly")
        state["permissions"].append({"candidate_id": event["candidate_id"],
                                      **exploration_permission(state["states"][event["candidate_id"]], event["declaration"])})
    elif kind == "promote":
        exact(event, {"type", "candidate_id", "target", "use"}, "promotion event")
        require(event["candidate_id"] in state["states"], "unknown promotion candidate")
        require(not any(a["disposition"] == "pending" for a in state["attempts"].values()), "promotion with unsettled cost")
        if registration["evidence_class"] == "admitted_simulation":
            require(state["accounting_complete"], "unknown recovered cost blocks scientific admission")
        s = state["states"][event["candidate_id"]]
        require(event["use"] not in s["promotion"] or s["promotion"][event["use"]]["status"] != event["target"], "duplicate promotion decision")
        s["promotion"][event["use"]] = promotion_decision(s, registration, event["target"], event["use"])
    elif kind == "quarantine":
        exact(event, {"type", "source_sha256", "reason"}, "quarantine")
        sha(event["source_sha256"])
        nonempty(event["reason"], "protocol-invalid reason")
        state["quarantines"].append({**clone(event), "disposition": "protocol_invalid"})
    else:
        raise DiscoveryViolation("unknown event type")


class DiscoveryLedger:
    """One durable event at a time; explicit trusted heads detect rollback on reopen."""

    def __init__(self, path: Path, registration: dict, *, expected_head: str | None = None):
        self.path = Path(path)
        self.registration = clone(registration)
        validate_registration(self.registration)
        self.expected_head = expected_head
        if expected_head is not None:
            sha(expected_head, "trusted checkpoint")
        self.replay()

    def _read(self) -> tuple[list[dict], dict, str]:
        body = validate_registration(self.registration)
        state = fresh_state()
        rows = []
        previous = ZERO
        raw = self.path.read_bytes() if self.path.exists() else b""
        require(not raw or raw.endswith(b"\n"), "truncated ledger tail")
        try:
            lines = raw.decode("utf-8").splitlines()
        except UnicodeDecodeError as error:
            raise DiscoveryViolation("invalid ledger encoding") from error
        for sequence, line in enumerate(lines):
            row = strict_json(line)
            exact(row, {"sequence", "previous", "registration_sha256", "event", "sha256"}, "ledger row")
            require(type(row["sequence"]) is int and row["sequence"] == sequence, "ledger sequence mismatch")
            require(row["previous"] == previous, "ledger chain mismatch")
            require(row["registration_sha256"] == self.registration["registration_sha256"], "ledger registration changed")
            require(row["sha256"] == digest({k: v for k, v in row.items() if k != "sha256"}), "ledger hash mismatch")
            reduce_event(state, row["event"], body, self.registration["registration_sha256"])
            rows.append(row)
            previous = row["sha256"]
        if self.expected_head is not None:
            require(previous == self.expected_head, "trusted checkpoint mismatch or ledger rollback")
        return rows, state, previous

    def replay(self) -> dict:
        _, state, head = self._read()
        return {"head_sha256": head, "state_sha256": digest(state), "state": state}

    @contextmanager
    def _lock(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        lock = self.path.with_name(self.path.name + ".lock")
        try:
            descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as error:
            raise DiscoveryViolation("writer lock exists; inspect stale writer before recovery") from error
        try:
            os.write(descriptor, str(os.getpid()).encode("ascii"))
            yield
        finally:
            os.close(descriptor)
            lock.unlink()

    def append(self, event: dict) -> dict:
        with self._lock():
            rows, state, previous = self._read()
            clean = clone(event)
            reduce_event(state, clean, self.registration["body"], self.registration["registration_sha256"])
            row = {"sequence": len(rows), "previous": previous,
                   "registration_sha256": self.registration["registration_sha256"], "event": clean}
            row["sha256"] = digest(row)
            with self.path.open("ab") as stream:
                stream.write(canonical(row) + b"\n")
                stream.flush()
                os.fsync(stream.fileno())
            self.expected_head = row["sha256"]
        return self.replay()

    def audit_report(self, selection_sha256: str, reference_gate_id: str) -> dict:
        state = self.replay()["state"]
        gate = gate_for(self.registration["body"], reference_gate_id)
        require(gate["kind"] == "physics", "reference must be a physical gate")
        choices = [x for x in state["selections"] if x["selection_sha256"] == selection_sha256 and x["pool"] == "audit"]
        require(len(choices) == 1, "unknown audit selection")
        choice = choices[0]
        proxy = gate_for(self.registration["body"], choice["gate_id"])
        require(gate["fidelity_rank"] > proxy["fidelity_rank"] and gate["domain"] == proxy["domain"]
                and gate["metric"] == proxy["metric"] and gate["unit"] == proxy["unit"],
                "audit reference must have higher comparable fidelity")
        population = {r["candidate_id"]: r for r in choice["population"]}
        labels = []
        for row in choice["selection"]["selected"]:
            cid = row["candidate_id"]
            score = population[cid]["proxy_score"]
            require(score is not None, "proxy label unknown; audit rate not estimable")
            ref = state["states"][cid]["physics"].get(reference_gate_id)
            if ref is not None:
                require(digest(ref["context"]) == choice["contexts"][cid], "audit reference context changed")
            passed = None if ref is None or ref["status"] not in {"physically_failed", "physically_feasible"} else ref["status"] == "physically_feasible"
            labels.append({"candidate_id": cid, "proxy_pass": score <= proxy["threshold"] if proxy["comparison"] == "le" else score >= proxy["threshold"], "reference_pass": passed})
        return proxy_audit(choice["selection"], labels)
