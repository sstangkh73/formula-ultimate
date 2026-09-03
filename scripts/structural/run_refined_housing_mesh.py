"""Run and replay the identity-locked Work 086 housing refinement."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.structural.generalized_coupling import canonical_sha256  # noqa: E402
from formula_ultimate.structural.refined_mesh import derive_config, validate_refinement  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+"\n", encoding="utf-8")


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--config",type=Path,required=True); parser.add_argument("--output-root",type=Path,required=True); parser.add_argument("--gmsh",type=Path,required=True); parser.add_argument("--ccx",type=Path,required=True); parser.add_argument("--replay-reference",type=Path)
    args=parser.parse_args(); args.output_root=args.output_root.resolve()
    if args.output_root.exists() and any(args.output_root.iterdir()): raise SystemExit("output-root must be absent or empty")
    args.output_root.mkdir(parents=True,exist_ok=True)
    refinement=json.loads(args.config.read_text(encoding="utf-8")); refinement_validation=validate_refinement(refinement)
    base_path=ROOT/refinement["base_config_path"]; prior_path=ROOT/refinement["failed_evidence_path"]
    if sha(prior_path) != refinement["failed_evidence_file_sha256"]: raise RuntimeError("prior failed evidence file identity mismatch")
    base=json.loads(base_path.read_text(encoding="utf-8")); prior=json.loads(prior_path.read_text(encoding="utf-8")); derived=derive_config(refinement,base,prior)
    derived_path=args.output_root/"derived_solver_config.json"; write_json(derived_path,derived)
    solver_root=args.output_root/"solver"
    process=subprocess.run([sys.executable,str(ROOT/"scripts/structural/run_generalized_structural_coupling.py"),"--config",str(derived_path),"--output-root",str(solver_root),"--gmsh",str(args.gmsh),"--ccx",str(args.ccx)],cwd=ROOT,text=True,capture_output=True,check=False)
    (args.output_root/"solver_stdout.txt").write_text(process.stdout,encoding="utf-8"); (args.output_root/"solver_stderr.txt").write_text(process.stderr,encoding="utf-8")
    if process.returncode != 0: raise RuntimeError(f"refined generalized solve failed: {process.stderr[-1500:]}")
    solver_result=json.loads((solver_root/"result.json").read_text(encoding="utf-8"))
    if solver_result.get("status") != "passed" or solver_result.get("verdict") != "synthetic_meshed_verification_only" or solver_result.get("design_use_allowed") is not False: raise RuntimeError("refined solver verdict changed")
    body={"status":"passed","verdict":"synthetic_meshed_verification_only","design_use_allowed":False,"refinement_sha256":refinement_validation["refinement_sha256"],"prior_failed_evidence_file_sha256":sha(prior_path),"base_config_sha256":refinement["base_config_sha256"],"derived_config_sha256":solver_result["config_sha256"],"solver_result_sha256":solver_result["result_sha256"],"cases":solver_result["adjudication"]["cases"]}
    result={**body,"result_sha256":canonical_sha256(body)}; write_json(args.output_root/"result.json",result)
    replay_exact=None
    if args.replay_reference:
        reference=json.loads(args.replay_reference.read_text(encoding="utf-8")); replay_exact=reference==result
        replay_body={"status":"passed" if replay_exact else "failed","exact":replay_exact,"reference_result_sha256":reference.get("result_sha256"),"replay_result_sha256":result["result_sha256"]}; write_json(args.output_root/"replay.json",{**replay_body,"replay_sha256":canonical_sha256(replay_body)})
        if not replay_exact: raise RuntimeError("refinement replay mismatch")
    print(json.dumps({"status":"passed","result_sha256":result["result_sha256"],"derived_config_sha256":result["derived_config_sha256"],"replay_exact":replay_exact,"cases":result["cases"]},sort_keys=True)); return 0


if __name__=="__main__": raise SystemExit(main())
