"""Deterministic opportunity selection and transparent, within-stratum proxy audits."""

from __future__ import annotations

import math
from .discovery_registration import clone, digest, exact, integer, nonempty, number, require, sha


def stratified_sample(population: list[dict], *, seed: int, per_stratum: int) -> dict:
    integer(seed, "audit seed")
    integer(per_stratum, "stratum sample", 1)
    groups: dict[str, list[str]] = {}
    seen = set()
    for row in population:
        exact(row, {"candidate_id", "stratum", "proxy_score"}, "audit population row")
        for key in ("candidate_id", "stratum"):
            nonempty(row[key], key)
        require(row["candidate_id"] not in seen, "duplicate audit candidate")
        seen.add(row["candidate_id"])
        if row["proxy_score"] is not None:
            number(row["proxy_score"], "proxy score", -1e300)
        groups.setdefault(row["stratum"], []).append(row["candidate_id"])
    selected = []
    for stratum, ids in sorted(groups.items()):
        ids = sorted(ids, key=lambda cid: (digest([seed, stratum, cid]), cid))
        n = min(per_stratum, len(ids))
        selected.extend({"candidate_id": cid, "stratum": stratum, "population_size": len(ids),
                         "sample_size": n, "inclusion_probability": n / len(ids)} for cid in ids[:n])
    return {"method": "hash_rank_without_proxy_score", "seed": seed, "selected": selected,
            "population_sha256": digest(sorted([{k: r[k] for k in ("candidate_id", "stratum")}
                                                  for r in population], key=lambda r: r["candidate_id"]))}


def proxy_audit(sample: dict, labels: list[dict]) -> dict:
    """No pooled biased rate. Unknown references get identification bounds, not labels."""
    rows = sample["selected"]
    exact(sample, {"method", "seed", "selected", "population_sha256"}, "audit sample")
    require(sample["method"] == "hash_rank_without_proxy_score", "unknown audit design")
    integer(sample["seed"], "audit seed")
    sha(sample["population_sha256"])
    for row in rows:
        exact(row, {"candidate_id", "stratum", "population_size", "sample_size", "inclusion_probability"}, "sample row")
        integer(row["population_size"], "stratum population", 1)
        integer(row["sample_size"], "stratum sample", 1)
        require(row["sample_size"] <= row["population_size"], "sample exceeds population")
        require(row["inclusion_probability"] == row["sample_size"] / row["population_size"], "sampling probability mismatch")
        members = [r for r in rows if r["stratum"] == row["stratum"]]
        require(len(members) == row["sample_size"] and all(r["population_size"] == row["population_size"] for r in members),
                "incomplete/inconsistent stratum sample")
    require(len({r["candidate_id"] for r in rows}) == len(rows), "duplicate sampled candidate")
    by_id = {}
    for label in labels:
        exact(label, {"candidate_id", "proxy_pass", "reference_pass"}, "audit label")
        require(type(label["proxy_pass"]) is bool, "proxy label must be Boolean")
        require(label["reference_pass"] is None or type(label["reference_pass"]) is bool, "reference label must be Boolean or unknown")
        require(label["candidate_id"] not in by_id, "duplicate reference label")
        by_id[label["candidate_id"]] = label
    require(set(by_id) == {r["candidate_id"] for r in rows}, "missing or unselected audit labels")
    groups = {}
    for row in rows:
        group = groups.setdefault(row["stratum"], {"labels": [], "probabilities": []})
        group["labels"].append(by_id[row["candidate_id"]])
        number(row["inclusion_probability"], "inclusion probability")
        require(0 < row["inclusion_probability"] <= 1, "invalid inclusion probability")
        group["probabilities"].append(row["inclusion_probability"])
    result = {}
    for name, group in sorted(groups.items()):
        ls = group["labels"]
        known = [l for l in ls if l["reference_pass"] is not None]
        positives = sum(l["reference_pass"] for l in known)
        negatives = len(known) - positives
        fn = sum(l["reference_pass"] and not l["proxy_pass"] for l in known)
        fp = sum(not l["reference_pass"] and l["proxy_pass"] for l in known)
        unknown_fail = sum(l["reference_pass"] is None and not l["proxy_pass"] for l in ls)
        unknown_pass = sum(l["reference_pass"] is None and l["proxy_pass"] for l in ls)
        def bounds(errors: int, denom: int, adverse: int, favorable: int) -> list[float]:
            lower = errors / (denom + favorable) if denom + favorable else 0.0
            upper = (errors + adverse) / (denom + adverse) if denom + adverse else 1.0
            return [lower, upper]
        result[name] = {
            "sampled": len(ls), "reference_positive": positives, "reference_negative": negatives,
            "reference_unknown": len(ls) - len(known), "false_negatives": fn, "false_positives": fp,
            "known_reference_fnr": fn / positives if positives else None,
            "known_reference_fpr": fp / negatives if negatives else None,
            "status": "not_estimable" if not known else "within_stratum_descriptive",
            "fnr_unknown_bounds": bounds(fn, positives, unknown_fail, unknown_pass),
            "fpr_unknown_bounds": bounds(fp, negatives, unknown_pass, unknown_fail),
            "inclusion_probabilities": group["probabilities"],
        }
    return {"strata": result, "pooled_rate": None,
            "uncertainty": "sample identification bounds for unknown labels; not population confidence intervals"}


def ranked_selection(population: list[dict], *, count: int, minimize: bool = True) -> list[str]:
    integer(count, "selection count")
    require(type(minimize) is bool, "direction must be Boolean")
    ids = [r["candidate_id"] for r in population]
    require(len(ids) == len(set(ids)), "duplicate selection candidate")
    scored = []
    for row in population:
        if row["proxy_score"] is not None:
            number(row["proxy_score"], "selection score", -1e300)
            scored.append(row)
    return [r["candidate_id"] for r in sorted(scored, key=lambda r: (
        r["proxy_score"] if minimize else -r["proxy_score"], r["candidate_id"]))[:count]]


def compare_execution(reference: dict, observed: dict, tolerances: dict) -> dict:
    """Pinned identities and field-specific tolerances; timing is reported separately."""
    for record in (reference, observed):
        exact(record, {"identity", "values", "wall_s"}, "execution record")
        number(record["wall_s"], "wall time")
        require(isinstance(record["identity"], dict) and bool(record["identity"]), "execution identity required")
        require(isinstance(record["values"], dict) and bool(record["values"]), "execution values required")
    require(reference["identity"] == observed["identity"], "execution identity mismatch")
    exact(reference["identity"], {"registration_sha256", "evaluator_sha256", "context_sha256", "tolerances_sha256"}, "execution identities")
    for value in reference["identity"].values():
        sha(value)
    require(reference["identity"]["tolerances_sha256"] == digest(tolerances), "execution tolerances changed")
    require(set(reference["values"]) == set(observed["values"]) == set(tolerances), "execution coverage mismatch")
    errors = {}
    for key, value in reference["values"].items():
        actual = observed["values"][key]
        number(value, key, -1e300)
        number(actual, key, -1e300)
        exact(tolerances[key], {"absolute", "relative"}, "execution tolerance")
        for tol in tolerances[key].values():
            number(tol, "execution tolerance")
        error = abs(value - actual)
        require(math.isfinite(error), "execution difference overflow")
        limit = tolerances[key]["absolute"] + tolerances[key]["relative"] * abs(value)
        errors[key] = {"absolute_error": error, "limit": limit, "passed": error <= limit}
    return {"passed": all(r["passed"] for r in errors.values()), "fields": errors,
            "reference_wall_s": reference["wall_s"], "observed_wall_s": observed["wall_s"],
            "bitwise_claim": False, "identity": clone(reference["identity"])}
