"""Deterministic bounded topology proposals for Work 094."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import random
from typing import Any, Mapping

from .topology_genome import (
    DOMAINS,
    TopologyGenomeError,
    canonical_bytes,
    canonical_topology_signature,
    declaration_sha256,
    validate_topology_corpus,
)


PROTOCOL_VERSION = "reproducible_topology_mutation_v1"
OPERATORS = (
    "grow_branch", "prune_branch", "split_part", "add_crosslink", "reroute_path",
    "replace_solid_family", "insert_feature", "mutate_material_process",
)
TOPOLOGY_OPERATORS = {"grow_branch", "prune_branch", "split_part", "add_crosslink", "reroute_path"}


class TopologyMutationError(ValueError):
    """Raised when a proposal protocol or mutation is invalid."""


def protocol_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def validate_mutation_protocol(value: Mapping[str, Any], genome_declaration_sha256: str) -> dict[str, Any]:
    if set(value) != {"protocol_version", "source_genome_declaration_sha256", "proposal_phase", "maximum_retries_per_slot", "operator_schedule", "operator_probabilities", "initializer_strata", "interface_policy", "material_process_compatibility", "crossover"}:
        raise TopologyMutationError("mutation protocol schema mismatch")
    if value["protocol_version"] != PROTOCOL_VERSION or value["source_genome_declaration_sha256"] != genome_declaration_sha256:
        raise TopologyMutationError("protocol or source genome identity mismatch")
    if value["proposal_phase"] != "pre_evaluation_only": raise TopologyMutationError("mutation must be pre-evaluation only")
    retries = value["maximum_retries_per_slot"]
    if isinstance(retries, bool) or not isinstance(retries, int) or not 0 <= retries <= 8: raise TopologyMutationError("retry budget is outside bounds")
    schedule = value["operator_schedule"]
    if not isinstance(schedule, list) or tuple(schedule) != OPERATORS: raise TopologyMutationError("operator schedule mismatch")
    probabilities = value["operator_probabilities"]
    if set(probabilities) != set(OPERATORS) or any(not isinstance(item, (int, float)) or isinstance(item, bool) or item <= 0 for item in probabilities.values()) or abs(sum(probabilities.values()) - 1.0) > 1e-12:
        raise TopologyMutationError("operator probability table is invalid")
    strata = value["initializer_strata"]
    if not isinstance(strata, list) or len(strata) != 6: raise TopologyMutationError("six balanced initializer strata are required")
    names = set(); parents = set()
    for item in strata:
        if set(item) != {"stratum", "parent_genome_id", "seed"} or item["stratum"] in names or item["parent_genome_id"] in parents or isinstance(item["seed"], bool) or not isinstance(item["seed"], int):
            raise TopologyMutationError("initializer stratum is invalid or duplicated")
        names.add(item["stratum"]); parents.add(item["parent_genome_id"])
    policy = value["interface_policy"]
    if not isinstance(policy, dict) or not policy: raise TopologyMutationError("interface policy is missing")
    for interface_type, item in policy.items():
        if set(item) != {"domains", "allowed_dof"} or not set(item["domains"]).issubset(DOMAINS): raise TopologyMutationError(f"invalid interface policy {interface_type}")
    compatibility = value["material_process_compatibility"]
    if not isinstance(compatibility, dict) or any(not processes for processes in compatibility.values()): raise TopologyMutationError("material/process compatibility is missing")
    crossover = value["crossover"]
    if set(crossover) != {"enabled", "disabled_reason"} or crossover["enabled"] is not False or not crossover["disabled_reason"]:
        raise TopologyMutationError("V1 crossover must remain explicitly disabled")
    return {"status": "passed", "stratum_count": len(strata), "slots_per_stratum": len(schedule), "total_slots": len(strata) * len(schedule), "protocol_sha256": protocol_sha256(value)}


def _checkpoint(rng: random.Random) -> str:
    return hashlib.sha256(repr(rng.getstate()).encode("utf-8")).hexdigest()


def _unique(genome: Mapping[str, Any], prefix: str) -> str:
    used = {part["part_id"] for part in genome["parts"]}
    used |= {item["interface_id"] for item in genome["interfaces"]}
    used |= {item["terminal_id"] for item in genome["terminals"]}
    used |= {item["path_id"] for item in genome["paths"]}
    index = 0
    while f"{prefix}_{index}" in used: index += 1
    return f"{prefix}_{index}"


def _source_terminal(genome: Mapping[str, Any]) -> Mapping[str, Any]:
    candidates = [item for item in genome["terminals"] if item["role"] in {"source", "bidirectional"} and set(item["domains"]) == set(DOMAINS)]
    if not candidates: raise TopologyMutationError("no all-domain source terminal is available")
    return sorted(candidates, key=lambda item: item["terminal_id"])[0]


def _grow_branch(genome: dict[str, Any], rng: random.Random, tag: str) -> list[str]:
    source = _source_terminal(genome); template = deepcopy(rng.choice(genome["parts"])); part_id = _unique(genome, f"{tag}_branch")
    template["part_id"] = part_id; template["parent_part_id"] = source["part_id"]
    interface_id = _unique(genome, f"{tag}_interface"); terminal_id = _unique(genome, f"{tag}_sink"); path_id = _unique(genome, f"{tag}_path")
    genome["parts"].append(template)
    genome["interfaces"].append({"interface_id": interface_id, "part_a": source["part_id"], "part_b": part_id, "interface_type": "fixed", "domains": list(DOMAINS), "allowed_dof": []})
    genome["terminals"].append({"terminal_id": terminal_id, "part_id": part_id, "role": "sink", "domains": list(DOMAINS), "required": True})
    genome["paths"].append({"path_id": path_id, "domains": list(DOMAINS), "terminal_ids": [source["terminal_id"], terminal_id], "part_ids": [source["part_id"], part_id], "interface_ids": [interface_id]})
    return [f"added part {part_id}", f"added interface {interface_id}", f"added terminal/path {terminal_id}/{path_id}"]


def _prune_branch(genome: dict[str, Any], rng: random.Random, tag: str) -> list[str]:
    degree = {part["part_id"]: 0 for part in genome["parts"]}
    for interface in genome["interfaces"]: degree[interface["part_a"]] += 1; degree[interface["part_b"]] += 1
    sources = {item["part_id"] for item in genome["terminals"] if item["role"] == "source"}
    leaves = [part_id for part_id, count in degree.items() if count == 1 and part_id not in sources]
    rng.shuffle(leaves)
    for part_id in leaves:
        remove_paths = [path for path in genome["paths"] if part_id in path["part_ids"]]
        remove_terminals = {item["terminal_id"] for item in genome["terminals"] if item["part_id"] == part_id}
        remaining_domains = {domain for path in genome["paths"] if path not in remove_paths for domain in path["domains"]}
        if set(DOMAINS).issubset(remaining_domains):
            children = [item for item in genome["parts"] if item["parent_part_id"] == part_id]
            if children: continue
            removed_interfaces = {item["interface_id"] for item in genome["interfaces"] if part_id in {item["part_a"], item["part_b"]}}
            genome["parts"] = [item for item in genome["parts"] if item["part_id"] != part_id]
            genome["interfaces"] = [item for item in genome["interfaces"] if item["interface_id"] not in removed_interfaces]
            genome["terminals"] = [item for item in genome["terminals"] if item["terminal_id"] not in remove_terminals]
            genome["paths"] = [item for item in genome["paths"] if item not in remove_paths]
            return [f"pruned redundant leaf {part_id}"]
    raise TopologyMutationError("no redundant terminal leaf is eligible for pruning")


def _split_part(genome: dict[str, Any], rng: random.Random, tag: str) -> list[str]:
    source = _source_terminal(genome); original_id = source["part_id"]; original = next(item for item in genome["parts"] if item["part_id"] == original_id)
    new_id = _unique(genome, f"{tag}_split"); new_part = deepcopy(original); new_part["part_id"] = new_id; new_part["parent_part_id"] = original["parent_part_id"]; original["parent_part_id"] = new_id
    genome["parts"].append(new_part); interface_id = _unique(genome, f"{tag}_split_interface")
    genome["interfaces"].append({"interface_id": interface_id, "part_a": new_id, "part_b": original_id, "interface_type": "fixed", "domains": list(DOMAINS), "allowed_dof": []})
    for terminal in genome["terminals"]:
        if terminal["part_id"] == original_id and terminal["role"] in {"source", "bidirectional"}: terminal["part_id"] = new_id
    for path in genome["paths"]:
        if path["part_ids"][0] == original_id:
            path["part_ids"].insert(0, new_id); path["interface_ids"].insert(0, interface_id)
    return [f"split source part {original_id} into {new_id} -> {original_id}"]


def _add_crosslink(genome: dict[str, Any], rng: random.Random, tag: str) -> list[str]:
    part_ids = [item["part_id"] for item in genome["parts"]]; connected = {frozenset((item["part_a"], item["part_b"])) for item in genome["interfaces"]}
    pairs = [(a, b) for index, a in enumerate(part_ids) for b in part_ids[index + 1:] if frozenset((a, b)) not in connected]
    if not pairs: raise TopologyMutationError("no non-duplicate crosslink pair is available")
    a, b = rng.choice(pairs); interface_id = _unique(genome, f"{tag}_crosslink")
    genome["interfaces"].append({"interface_id": interface_id, "part_a": a, "part_b": b, "interface_type": "fixed", "domains": list(DOMAINS), "allowed_dof": []})
    return [f"added crosslink {interface_id} between {a} and {b}"]


def _reroute_path(genome: dict[str, Any], rng: random.Random, tag: str) -> list[str]:
    candidates = [item for item in genome["paths"] if len(item["part_ids"]) >= 3]
    if not candidates: raise TopologyMutationError("no multi-interface path is available for rerouting")
    path = rng.choice(candidates); a, b = path["part_ids"][0], path["part_ids"][-1]
    for interface in genome["interfaces"]:
        if {a, b} == {interface["part_a"], interface["part_b"]} and set(path["domains"]).issubset(interface["domains"]):
            alternate = deepcopy(path); alternate["path_id"] = _unique(genome, f"{tag}_alternate")
            alternate["part_ids"] = [a, b]; alternate["interface_ids"] = [interface["interface_id"]]
            genome["paths"].append(alternate)
            return [f"retained {path['path_id']} and added alternate {alternate['path_id']} over existing {interface['interface_id']}"]
    interface_id = _unique(genome, f"{tag}_route")
    genome["interfaces"].append({"interface_id": interface_id, "part_a": a, "part_b": b, "interface_type": "fixed", "domains": list(path["domains"]), "allowed_dof": []})
    alternate = deepcopy(path); alternate["path_id"] = _unique(genome, f"{tag}_alternate")
    alternate["part_ids"] = [a, b]; alternate["interface_ids"] = [interface_id]
    genome["paths"].append(alternate)
    return [f"retained {path['path_id']} and added alternate {alternate['path_id']} over new {interface_id}"]


def _replace_solid(genome: dict[str, Any], rng: random.Random, solid_candidates: Mapping[str, str], tag: str) -> list[str]:
    part = rng.choice(genome["parts"]); choices = [(candidate, family) for candidate, family in solid_candidates.items() if family != part["solid_family"]]
    candidate, family = rng.choice(choices); old = part["source_solid_candidate_id"]; part["source_solid_candidate_id"] = candidate; part["solid_family"] = family
    return [f"replaced {old} with {candidate} on {part['part_id']}"]


def _insert_feature(genome: dict[str, Any], rng: random.Random, tag: str) -> list[str]:
    part = rng.choice(genome["parts"]); old_final = part["final_feature_id"]; feature_id = f"{tag}_feature"
    part["features"].append({"feature_id": feature_id, "operator": "transform", "inputs": [old_final]}); part["final_feature_id"] = feature_id
    return [f"inserted transform feature {feature_id} after {old_final}"]


def _mutate_material(genome: dict[str, Any], rng: random.Random, compatibility: Mapping[str, list[str]], tag: str) -> list[str]:
    part = rng.choice(genome["parts"]); choices = [(material, process) for material, processes in compatibility.items() for process in processes if (material, process) != (part["material_id"], part["process_id"])]
    material, process = rng.choice(choices); old = (part["material_id"], part["process_id"]); part["material_id"] = material; part["process_id"] = process
    return [f"changed material/process on {part['part_id']} from {old[0]}/{old[1]} to {material}/{process}"]


MUTATORS = {"grow_branch": _grow_branch, "prune_branch": _prune_branch, "split_part": _split_part, "add_crosslink": _add_crosslink, "reroute_path": _reroute_path}


def validate_policy(genome: Mapping[str, Any], protocol: Mapping[str, Any]) -> None:
    for part in genome["parts"]:
        processes = protocol["material_process_compatibility"].get(part["material_id"], [])
        if part["process_id"] not in processes: raise TopologyMutationError("material/process combination is incompatible")
    for interface in genome["interfaces"]:
        policy = protocol["interface_policy"].get(interface["interface_type"])
        if policy is None or not set(interface["domains"]).issubset(policy["domains"]) or not set(interface["allowed_dof"]).issubset(policy["allowed_dof"]):
            raise TopologyMutationError("interface domain or DOF is impossible under policy")


def propose(
    corpus: Mapping[str, Any], protocol: Mapping[str, Any], solid_candidates: Mapping[str, str],
    *, parent_genome_id: str, operator: str, seed: int, slot_index: int,
    observation_available: bool = False,
) -> dict[str, Any]:
    if observation_available: raise TopologyMutationError("mutation after result observation is prohibited")
    if operator not in OPERATORS: raise TopologyMutationError("unsupported mutation operator")
    parent_index = next((index for index, item in enumerate(corpus["genomes"]) if item["genome_id"] == parent_genome_id), None)
    if parent_index is None: raise TopologyMutationError("parent genome is missing")
    parent = corpus["genomes"][parent_index]; parent_signature = canonical_topology_signature(parent); parent_identity = declaration_sha256(parent)
    rng = random.Random((seed << 16) ^ slot_index); start_checkpoint = _checkpoint(rng); failures = []
    for retry in range(protocol["maximum_retries_per_slot"] + 1):
        child = deepcopy(parent); child["genome_id"] = f"proposal_{seed}_{slot_index}_{retry}"; tag = f"m{slot_index}r{retry}"
        try:
            if operator in MUTATORS: trace = MUTATORS[operator](child, rng, tag)
            elif operator == "replace_solid_family": trace = _replace_solid(child, rng, solid_candidates, tag)
            elif operator == "insert_feature": trace = _insert_feature(child, rng, tag)
            else: trace = _mutate_material(child, rng, protocol["material_process_compatibility"], tag)
            validate_policy(child, protocol)
            trial = deepcopy(corpus); trial["genomes"][parent_index] = child
            validation = validate_topology_corpus(trial, solid_candidates)
            child_signature = canonical_topology_signature(child); declared_topology_change = operator in TOPOLOGY_OPERATORS
            if declared_topology_change and child_signature == parent_signature: raise TopologyMutationError("topology operator produced no signature change")
            body = {"status": "accepted", "parent_genome_id": parent_genome_id, "parent_genotype_sha256": parent_identity, "parent_topology_signature": parent_signature, "seed": seed, "slot_index": slot_index, "operator": operator, "operator_probability": protocol["operator_probabilities"][operator], "retry_index": retry, "maximum_retries": protocol["maximum_retries_per_slot"], "rng_checkpoint_before": start_checkpoint, "rng_checkpoint_after": _checkpoint(rng), "trace": trace, "declared_topology_change": declared_topology_change, "child_genotype_sha256": declaration_sha256(child), "child_topology_signature": child_signature, "validation_declaration_sha256": validation["declaration_sha256"], "prior_failures": failures, "child": child}
            return {**body, "lineage_sha256": hashlib.sha256(canonical_bytes(body)).hexdigest()}
        except (TopologyMutationError, TopologyGenomeError, StopIteration, IndexError) as error:
            failures.append({"retry_index": retry, "failure_code": type(error).__name__, "message": str(error), "rng_checkpoint": _checkpoint(rng)})
    body = {"status": "rejected", "parent_genome_id": parent_genome_id, "parent_genotype_sha256": parent_identity, "parent_topology_signature": parent_signature, "seed": seed, "slot_index": slot_index, "operator": operator, "operator_probability": protocol["operator_probabilities"][operator], "maximum_retries": protocol["maximum_retries_per_slot"], "rng_checkpoint_before": start_checkpoint, "rng_checkpoint_after": _checkpoint(rng), "failures": failures}
    return {**body, "lineage_sha256": hashlib.sha256(canonical_bytes(body)).hexdigest()}
