"""Typed, renaming-invariant physical-interface multigraphs for Work 112."""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
import math
from typing import Any, Mapping


PROTOCOL_VERSION = "physical_interface_graph_v1"


class PhysicalInterfaceViolation(ValueError):
    pass


def canonical_sha256(value: Any) -> str:
    try:
        data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode()
    except (TypeError, ValueError) as exc:
        raise PhysicalInterfaceViolation("evidence must be finite canonical JSON") from exc
    return hashlib.sha256(data).hexdigest()


def _unit_vector(value: Any, label: str) -> tuple[float, float, float]:
    if not isinstance(value, list) or len(value) != 3 or any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in value):
        raise PhysicalInterfaceViolation(f"{label} must be a finite 3-vector")
    vector = tuple(float(x) for x in value)
    norm = math.sqrt(sum(x*x for x in vector))
    if abs(norm - 1.0) > 1e-9:
        raise PhysicalInterfaceViolation(f"{label} must be unit length")
    return vector


def spatial_region_index(spatial: Mapping[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    result = {}
    for case in spatial["cases"]:
        for region in case["material_regions"]:
            result[(case["case_id"], region["region_id"])] = {"kind": "material", "source_step_sha256": case["source_step_sha256"], "family": case["family"], "material_id": region["material_id"], "body_indices": region["body_indices"]}
        for region in case["void_regions"]:
            result[(case["case_id"], region["region_id"])] = {"kind": "void", "source_step_sha256": case["source_step_sha256"], "family": case["family"], "operation": region["operation"], "occupied_feature_id": region["occupied_feature_id"]}
    return result


def validate_protocol(raw: Mapping[str, Any], spatial: Mapping[str, Any]) -> dict[str, Any]:
    if set(raw) != {"protocol_version", "units", "dependency", "limits", "domains", "laws", "graph", "transfer_fixtures", "experiment"} or raw.get("protocol_version") != PROTOCOL_VERSION or raw.get("units") != "SI_m_kg_s_K_N_W_rad":
        raise PhysicalInterfaceViolation("protocol schema, identity, or units mismatch")
    dependency = raw["dependency"]
    if set(dependency) != {"work108_commit", "contract_path", "contract_sha256", "spatial_config"} or len(dependency["work108_commit"]) != 40 or len(dependency["contract_sha256"]) != 64:
        raise PhysicalInterfaceViolation("Work 108 dependency identity is invalid")
    limits = raw["limits"]
    if set(limits) != {"maximum_terminals", "frame_origin_tolerance_m", "opposed_normal_dot_maximum", "exchange_residual_absolute"} or not 2 <= limits["maximum_terminals"] <= 8:
        raise PhysicalInterfaceViolation("identity or compatibility limits are invalid")
    if not 0 < limits["frame_origin_tolerance_m"] <= 1e-3 or not -1 <= limits["opposed_normal_dot_maximum"] < 0 or not 0 < limits["exchange_residual_absolute"] <= 1e-6:
        raise PhysicalInterfaceViolation("compatibility tolerance is invalid")
    if not raw["domains"] or not raw["laws"] or any(not values for values in raw["experiment"].values()):
        raise PhysicalInterfaceViolation("domain, law, or experiment registration is incomplete")
    report = validate_graph(raw["graph"], spatial_region_index(spatial), raw)
    return {"status": "passed", "terminal_count": report["terminal_count"], "edge_count": report["edge_count"], "protocol_sha256": canonical_sha256(raw)}


def validate_graph(graph: Mapping[str, Any], regions: Mapping[tuple[str, str], dict[str, Any]], protocol: Mapping[str, Any]) -> dict[str, Any]:
    if set(graph) != {"graph_id", "terminals", "edges"} or not isinstance(graph["terminals"], list) or not isinstance(graph["edges"], list):
        raise PhysicalInterfaceViolation("graph schema mismatch")
    terminals = graph["terminals"]
    if not 2 <= len(terminals) <= protocol["limits"]["maximum_terminals"]:
        raise PhysicalInterfaceViolation("terminal count exceeds canonical identity bound")
    by_id = {}
    for terminal in terminals:
        required = {"terminal_id", "owner_id", "region_binding", "role", "domain", "variable", "unit", "frame", "allowed_motion"}
        if set(terminal) != required or terminal["terminal_id"] in by_id:
            raise PhysicalInterfaceViolation("terminal schema or identity is invalid")
        domain = protocol["domains"].get(terminal["domain"])
        if domain is None or terminal["variable"] != domain["variable"] or terminal["unit"] != domain["unit"] or terminal["role"] not in {"source", "sink", "bidirectional"}:
            raise PhysicalInterfaceViolation("terminal domain variable, unit, or role is incompatible")
        binding = terminal["region_binding"]
        if set(binding) != {"case_id", "region_id", "surface_id"} or not binding["surface_id"] or (binding["case_id"], binding["region_id"]) not in regions:
            raise PhysicalInterfaceViolation("missing mating surface or spatial region")
        frame = terminal["frame"]
        if set(frame) != {"origin_m", "normal", "reference"} or len(frame["origin_m"]) != 3 or any(not math.isfinite(float(x)) for x in frame["origin_m"]):
            raise PhysicalInterfaceViolation("terminal frame is invalid")
        normal = _unit_vector(frame["normal"], "frame normal"); reference = _unit_vector(frame["reference"], "frame reference")
        if abs(sum(a*b for a,b in zip(normal, reference))) > 1e-9:
            raise PhysicalInterfaceViolation("frame normal and reference must be orthogonal")
        if terminal["allowed_motion"] not in {"rigid", "revolute", "prismatic", "free"}:
            raise PhysicalInterfaceViolation("allowed motion is unsupported")
        by_id[terminal["terminal_id"]] = terminal
    edge_ids = set(); adjacency = {name: set() for name in by_id}; maximum_exchange_residual = 0.0
    for edge in graph["edges"]:
        if set(edge) != {"edge_id", "terminals", "direction", "law_ref", "exchange"} or edge["edge_id"] in edge_ids or len(edge["terminals"]) != 2 or edge["terminals"][0] == edge["terminals"][1]:
            raise PhysicalInterfaceViolation("edge schema, identity, or endpoints are invalid")
        edge_ids.add(edge["edge_id"]); a_id,b_id=edge["terminals"]
        if a_id not in by_id or b_id not in by_id or edge["law_ref"] not in protocol["laws"] or edge["direction"] not in {"a_to_b", "b_to_a", "bidirectional"}:
            raise PhysicalInterfaceViolation("edge endpoint, direction, or law is invalid")
        a,b=by_id[a_id],by_id[b_id]
        if a["domain"] != b["domain"] or a["variable"] != b["variable"] or a["unit"] != b["unit"] or protocol["laws"][edge["law_ref"]]["domain"] != a["domain"]:
            raise PhysicalInterfaceViolation("incompatible units or physical domains")
        source,sink=(a,b) if edge["direction"]=="a_to_b" else ((b,a) if edge["direction"]=="b_to_a" else (a,b))
        if edge["direction"] != "bidirectional" and (source["role"] not in {"source","bidirectional"} or sink["role"] not in {"sink","bidirectional"}):
            raise PhysicalInterfaceViolation("edge direction conflicts with source/sink roles")
        if {a["allowed_motion"], b["allowed_motion"]} & {"rigid"} and a["allowed_motion"] != b["allowed_motion"] and "free" not in {a["allowed_motion"], b["allowed_motion"]}:
            raise PhysicalInterfaceViolation("rigid/moving conflict")
        distance=math.dist(a["frame"]["origin_m"],b["frame"]["origin_m"]); dot=sum(x*y for x,y in zip(a["frame"]["normal"],b["frame"]["normal"]))
        if distance > protocol["limits"]["frame_origin_tolerance_m"] or dot > protocol["limits"]["opposed_normal_dot_maximum"]:
            raise PhysicalInterfaceViolation("mating frames are incompatible")
        if not isinstance(edge["exchange"], list) or len(edge["exchange"]) != 2 or any(not math.isfinite(float(x)) for x in edge["exchange"]):
            raise PhysicalInterfaceViolation("exchange values are invalid")
        residual=abs(float(edge["exchange"][0])+float(edge["exchange"][1])); maximum_exchange_residual=max(maximum_exchange_residual,residual)
        if residual > protocol["limits"]["exchange_residual_absolute"]:
            raise PhysicalInterfaceViolation("exchange conservation residual exceeded")
        adjacency[a_id].add(b_id); adjacency[b_id].add(a_id)
    components=[]; unseen=set(by_id)
    while unseen:
        stack=[min(unseen)]; component=set()
        while stack:
            node=stack.pop()
            if node in component: continue
            component.add(node); unseen.discard(node); stack.extend(adjacency[node]-component)
        components.append(sorted(component))
    return {"status":"passed","terminal_count":len(terminals),"edge_count":len(graph["edges"]),"parallel_edge_count":len(graph["edges"])-len({tuple(sorted(edge["terminals"])) for edge in graph["edges"]}),"connected_component_count":len(components),"components":components,"maximum_exchange_residual":maximum_exchange_residual}


def canonical_identity(graph: Mapping[str, Any], regions: Mapping[tuple[str, str], dict[str, Any]], maximum_terminals: int) -> dict[str, Any]:
    terminals=graph["terminals"]
    if len(terminals) > maximum_terminals:
        return {"status":"unresolved","reason":"terminal count exceeds canonical identity bound"}
    by_id={t["terminal_id"]:t for t in terminals}; best=None
    for permutation in itertools.permutations([t["terminal_id"] for t in terminals]):
        position={name:index for index,name in enumerate(permutation)}; owner_codes={}; next_owner=0; node_rows=[]
        for name in permutation:
            t=by_id[name]
            if t["owner_id"] not in owner_codes: owner_codes[t["owner_id"]]=next_owner; next_owner+=1
            binding=t["region_binding"]; descriptor=regions[(binding["case_id"],binding["region_id"])]
            node_rows.append([owner_codes[t["owner_id"]],t["role"],t["domain"],t["variable"],t["unit"],t["frame"],t["allowed_motion"],binding["surface_id"],descriptor])
        edge_rows=[]
        for edge in graph["edges"]:
            a,b=edge["terminals"]; pa,pb=position[a],position[b]; exchange=edge["exchange"]
            if edge["direction"]=="b_to_a": pa,pb=pb,pa; exchange=[exchange[1],exchange[0]]
            elif edge["direction"]=="bidirectional" and pb<pa: pa,pb=pb,pa; exchange=[exchange[1],exchange[0]]
            edge_rows.append([pa,pb,edge["direction"]=="bidirectional",edge["law_ref"],exchange])
        candidate=json.dumps([node_rows,sorted(edge_rows)],sort_keys=True,separators=(",",":"),allow_nan=False)
        if best is None or candidate<best: best=candidate
    return {"status":"resolved","identity_sha256":hashlib.sha256(best.encode()).hexdigest()}


def transfer_bindings(graph: Mapping[str, Any], changes: Mapping[str, list[Mapping[str, Any]]]) -> dict[str, Any]:
    transferred=copy.deepcopy(graph); events=[]
    for terminal in transferred["terminals"]:
        binding=terminal["region_binding"]; key=binding["case_id"]+"/"+binding["region_id"]
        if key not in changes: continue
        candidates=[item for item in changes[key] if binding["surface_id"] in item.get("source_surface_ids",[])]
        if len(candidates)!=1:
            events.append({"terminal_id":terminal["terminal_id"],"event":"evidence_invalidated","reason":"ambiguous or missing split surface binding"}); continue
        target=candidates[0]; terminal["region_binding"]={"case_id":target["case_id"],"region_id":target["region_id"],"surface_id":target["surface_id"]}
        events.append({"terminal_id":terminal["terminal_id"],"event":"evidence_invalidated","reason":"spatial binding changed; dependent evidence must be recomputed"})
    return {"graph":transferred,"events":events,"event_sha256":canonical_sha256(events)}
