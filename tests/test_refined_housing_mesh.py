from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from tests.artifact_requirements import requires_artifacts
import unittest

from formula_ultimate.structural.generalized_coupling import canonical_sha256
from formula_ultimate.structural.refined_mesh import RefinedMeshViolation, derive_config, prior_failure_change, validate_refinement


ROOT=Path(__file__).resolve().parents[1]
REFINEMENT=ROOT/"config/structural/refined_housing_mesh_convergence_v1.json"
BASE=ROOT/"config/structural/generalized_meshed_torsion_bearing_housing_v1.json"
PRIOR=ROOT/"artifacts/work085/run_g/solver_evidence.json"
PRIOR_RELATIVE="artifacts/work085/run_g/solver_evidence.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class RefinedHousingMeshTests(unittest.TestCase):
    def test_reference_refinement_is_valid(self) -> None:
        self.assertEqual(validate_refinement(load(REFINEMENT))["status"],"passed")

    def test_gate_cannot_be_relaxed(self) -> None:
        raw=load(REFINEMENT); raw["unchanged_gate"]=0.14
        with self.assertRaisesRegex(RefinedMeshViolation,"gate changed"):
            validate_refinement(raw)

    def test_mesh_sequence_must_refine(self) -> None:
        raw=load(REFINEMENT); raw["replacement_mesh_levels_m"]=[0.003,0.004,0.002]
        with self.assertRaisesRegex(RefinedMeshViolation,"strictly refine"):
            validate_refinement(raw)

    @requires_artifacts(PRIOR_RELATIVE)
    def test_prior_failure_is_reproduced(self) -> None:
        raw=load(REFINEMENT); observed=prior_failure_change(load(PRIOR),raw["failed_case_id"],raw["failed_metric"])
        self.assertAlmostEqual(observed,raw["observed_last_two_relative_change"],places=15)
        self.assertGreater(observed,raw["unchanged_gate"])

    @requires_artifacts(PRIOR_RELATIVE)
    def test_derived_config_changes_only_target_meshes(self) -> None:
        raw=load(REFINEMENT); base=load(BASE); derived=derive_config(raw,base,load(PRIOR)); expected=deepcopy(base); expected["cases"][2]["mesh_levels_m"]=raw["replacement_mesh_levels_m"]
        self.assertEqual(derived,expected)
        self.assertEqual(derived["tolerances"]["last_two_mesh_relative_change"],0.12)

    @requires_artifacts(PRIOR_RELATIVE)
    def test_wrong_base_identity_fails_closed(self) -> None:
        raw=load(REFINEMENT); raw["base_config_sha256"]="0"*64
        with self.assertRaisesRegex(RefinedMeshViolation,"base config identity"):
            derive_config(raw,load(BASE),load(PRIOR))

    @requires_artifacts(PRIOR_RELATIVE)
    def test_prior_value_mutation_fails_closed(self) -> None:
        raw=load(REFINEMENT); prior=load(PRIOR); prior["case_results"][2]["mesh_results"][2]["maximum_displacement_m"]*=0.5
        with self.assertRaisesRegex(RefinedMeshViolation,"prior failure value"):
            derive_config(raw,load(BASE),prior)

    def test_evidence_cannot_be_relabelled(self) -> None:
        raw=load(REFINEMENT); raw["evidence_policy"]["design_use_allowed"]=True
        with self.assertRaisesRegex(RefinedMeshViolation,"policy changed"):
            validate_refinement(raw)

    def test_canonical_identity_is_stable(self) -> None:
        self.assertEqual(canonical_sha256({"x":1,"y":2}),canonical_sha256({"y":2,"x":1}))


if __name__=="__main__": unittest.main()
