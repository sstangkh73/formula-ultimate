"""Execute the Work 112 physical-interface multigraph experiment."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/"src"
for item in (ROOT,SRC):
    if str(item) not in sys.path: sys.path.insert(0,str(item))

from formula_ultimate.assembly.physical_interface_graph import (  # noqa: E402
    PhysicalInterfaceViolation, canonical_identity, canonical_sha256, spatial_region_index,
    transfer_bindings, validate_graph, validate_protocol,
)


def read(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def write(path: Path,value: Any): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8",newline="\n")
def sha(path: Path): return hashlib.sha256(path.read_bytes()).hexdigest()


def rejected(action,phrase):
    try: action()
    except PhysicalInterfaceViolation as exc:
        if phrase not in str(exc): raise
        return {"status":"rejected","reason":str(exc)}
    raise PhysicalInterfaceViolation("negative control was accepted")


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--config",type=Path,required=True); parser.add_argument("--output-root",type=Path,required=True); parser.add_argument("--replay-reference",type=Path)
    args=parser.parse_args(); config_path=(ROOT/args.config).resolve() if not args.config.is_absolute() else args.config; output=(ROOT/args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root; output.mkdir(parents=True,exist_ok=True)
    raw=read(config_path); dependency=raw["dependency"]; spatial_path=ROOT/dependency["spatial_config"]; spatial=read(spatial_path)
    if sha(ROOT/dependency["contract_path"])!=dependency["contract_sha256"]: raise PhysicalInterfaceViolation("stale Work 108 contract")
    if subprocess.run(["git","cat-file","-e",dependency["work108_commit"]+"^{commit}"],cwd=ROOT,capture_output=True).returncode: raise PhysicalInterfaceViolation("missing Work 108 dependency commit")
    validation=validate_protocol(raw,spatial); regions=spatial_region_index(spatial); graph=raw["graph"]; report=validate_graph(graph,regions,raw); baseline=canonical_identity(graph,regions,raw["limits"]["maximum_terminals"])

    renamed=copy.deepcopy(graph); names={t["terminal_id"]:f"terminal_{i}" for i,t in enumerate(renamed["terminals"])}; owners={t["owner_id"]:f"owner_{i}" for i,t in enumerate(renamed["terminals"])}
    for terminal in renamed["terminals"]: terminal["terminal_id"]=names[terminal["terminal_id"]]; terminal["owner_id"]=owners[terminal["owner_id"]]
    for i,edge in enumerate(renamed["edges"]): edge["edge_id"]=f"interaction_{i}"; edge["terminals"]=[names[x] for x in edge["terminals"]]
    rename_identity=canonical_identity(renamed,regions,raw["limits"]["maximum_terminals"])
    if rename_identity!=baseline: raise PhysicalInterfaceViolation("identifier-only renaming changed meaning")

    deleted=copy.deepcopy(graph); deleted["edges"].pop(1)
    regrouped=copy.deepcopy(graph); regrouped["terminals"][1]["owner_id"]=regrouped["terminals"][0]["owner_id"]
    reversed_graph=copy.deepcopy(graph); reversed_graph["terminals"][0]["role"]="sink"; reversed_graph["terminals"][1]["role"]="source"
    for edge in reversed_graph["edges"][:2]: edge["direction"]="b_to_a"
    disconnected=copy.deepcopy(graph); disconnected["edges"]=[edge for edge in disconnected["edges"] if edge["edge_id"]!="heat_path"]
    distinctions={"parallel_edge_deleted":canonical_identity(deleted,regions,8),"owner_regrouped":canonical_identity(regrouped,regions,8),"source_sink_reversed":canonical_identity(reversed_graph,regions,8),"edge_disconnected":canonical_identity(disconnected,regions,8)}
    if any(item==baseline for item in distinctions.values()): raise PhysicalInterfaceViolation("registered physical distinction collapsed")
    disconnected_report=validate_graph(disconnected,regions,raw)
    if disconnected_report["connected_component_count"]<=report["connected_component_count"]: raise PhysicalInterfaceViolation("disconnected path was silently connected")

    unit=copy.deepcopy(graph); unit["terminals"][1]["unit"]="kN"
    surface=copy.deepcopy(graph); surface["terminals"][1]["region_binding"]["surface_id"]=""
    motion=copy.deepcopy(graph); motion["terminals"][3]["allowed_motion"]="revolute"
    exchange=copy.deepcopy(graph); exchange["edges"][0]["exchange"][1]=-119.0
    controls={
        "identifier_rename":{"status":"passed","baseline":baseline,"renamed":rename_identity},
        "distinctions":distinctions,
        "disconnected_path":{"status":"passed","before_components":report["connected_component_count"],"after_components":disconnected_report["connected_component_count"]},
        "incompatible_unit":rejected(lambda:validate_graph(unit,regions,raw),"unit"),
        "missing_mating_surface":rejected(lambda:validate_graph(surface,regions,raw),"missing mating surface"),
        "rigid_moving_conflict":rejected(lambda:validate_graph(motion,regions,raw),"rigid/moving"),
        "exchange_imbalance":rejected(lambda:validate_graph(exchange,regions,raw),"conservation"),
    }
    unambiguous=transfer_bindings(graph,raw["transfer_fixtures"]["unambiguous_split"]); ambiguous=transfer_bindings(graph,raw["transfer_fixtures"]["ambiguous_split"])
    if "ambiguous" not in ambiguous["events"][0]["reason"] or unambiguous["graph"]["terminals"][0]["region_binding"]["region_id"]==graph["terminals"][0]["region_binding"]["region_id"]: raise PhysicalInterfaceViolation("split transfer controls failed")
    oversize=copy.deepcopy(graph)
    while len(oversize["terminals"])<=raw["limits"]["maximum_terminals"]:
        clone=copy.deepcopy(oversize["terminals"][0]); clone["terminal_id"]=f"extra_{len(oversize['terminals'])}"; oversize["terminals"].append(clone)
    unresolved=canonical_identity(oversize,regions,raw["limits"]["maximum_terminals"])
    if unresolved["status"]!="unresolved": raise PhysicalInterfaceViolation("oversize identity did not remain unresolved")
    body={"status":"passed","claim_scope":"bounded semantic physical-interface descriptor; not mechanism proof, contact solve, or physical validation","validation":validation,"dependency":dependency,"graph_report":report,"canonical_identity":baseline,"controls":controls,"transfers":{"unambiguous":unambiguous,"ambiguous":ambiguous},"oversize_identity":unresolved,"review":{"supporting_evidence":["typed roles, directions, units, frames, laws and parallel edges survived canonicalization","identifier-only renaming was invariant while four physical mutations remained distinct","compatibility, conservation, disconnection and transfer ambiguity controls failed visibly"],"contradicting_evidence":["frame and surface bindings are declarations rather than CAD contact measurements"],"alternative_explanations":["the small colored corpus makes exact canonicalization inexpensive"],"missing_evidence":["general graph-scale identity","contact mechanics","measured exchanges","physical validation"],"confidence":"high inside the six-terminal declared corpus; low for general mechanism discovery"}}
    result={"body":body,"result_sha256":canonical_sha256(body)}; write(output/"result.json",result)
    if args.replay_reference:
        path=(ROOT/args.replay_reference).resolve() if not args.replay_reference.is_absolute() else args.replay_reference; prior=read(path); exact=prior.get("result_sha256")==result["result_sha256"]; write(output/"replay.json",{"reference_result_sha256":prior.get("result_sha256"),"current_result_sha256":result["result_sha256"],"exact":exact})
        if not exact: raise PhysicalInterfaceViolation("replay differs from reference")
    print(json.dumps({"status":"passed","result_sha256":result["result_sha256"],"terminal_count":report["terminal_count"],"edge_count":report["edge_count"]},sort_keys=True)); return 0


if __name__=="__main__": raise SystemExit(main())
