from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.components.part_contract import (
    PartContract,
    PartContractViolation,
    canonical_part_bytes,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/components/geometry_causal_part_contract_v1.json"


def load_reference() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def reverse_mappings(value):
    if isinstance(value, dict):
        return {key: reverse_mappings(item) for key, item in reversed(tuple(value.items()))}
    if isinstance(value, list):
        return [reverse_mappings(item) for item in value]
    return value


class PartContractTests(unittest.TestCase):
    def test_reference_admits_and_key_order_replays_exactly(self) -> None:
        raw = load_reference()
        contract = PartContract.from_mapping(raw)
        reordered = PartContract.from_mapping(reverse_mappings(raw))
        self.assertEqual("reference_bracket_001", contract.part_id)
        self.assertEqual(contract.canonical_json, reordered.canonical_json)
        self.assertEqual(contract.declaration_sha256, reordered.declaration_sha256)
        self.assertEqual(64, len(contract.declaration_sha256))

    def test_unknown_top_level_field_fails_closed(self) -> None:
        raw = load_reference()
        raw["hidden_repair"] = True
        with self.assertRaisesRegex(PartContractViolation, "unknown=.*hidden_repair"):
            canonical_part_bytes(raw)

    def test_unknown_parameter_unit_fails_closed(self) -> None:
        raw = load_reference()
        parameters = raw["feature_history"][0]["parameters"]
        parameters["length_mm"] = parameters.pop("length_m")
        with self.assertRaisesRegex(PartContractViolation, "unknown or missing SI unit"):
            PartContract.from_mapping(raw)

    def test_missing_material_interface_or_load_path_fails_closed(self) -> None:
        cases = []
        raw = load_reference()
        del raw["material"]
        cases.append((raw, "material"))
        raw = load_reference()
        raw["interfaces"] = []
        cases.append((raw, "interfaces must not be empty"))
        raw = load_reference()
        raw["load_path"] = ["subsystem_load_region"]
        cases.append((raw, "at least two distinct"))
        for candidate, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(PartContractViolation, message):
                    PartContract.from_mapping(candidate)

    def test_nan_and_negative_thickness_fail_closed(self) -> None:
        raw = load_reference()
        raw["feature_history"][1]["parameters"]["thickness_m"] = math.nan
        with self.assertRaisesRegex(PartContractViolation, "must be finite"):
            PartContract.from_mapping(raw)
        raw = load_reference()
        raw["feature_history"][1]["parameters"]["thickness_m"] = -0.001
        with self.assertRaisesRegex(PartContractViolation, "thickness_m must be > 0"):
            PartContract.from_mapping(raw)

    def test_invalid_tolerances_fail_closed(self) -> None:
        raw = load_reference()
        raw["tolerances"]["general_tolerance_m"] = 0.0
        with self.assertRaisesRegex(PartContractViolation, "must be > 0"):
            PartContract.from_mapping(raw)
        raw = load_reference()
        raw["interfaces"][0]["tolerance_m"] = 0.004
        with self.assertRaisesRegex(PartContractViolation, "exceeds minimum feature size"):
            PartContract.from_mapping(raw)

    def test_invalid_frame_and_interface_type_fail_closed(self) -> None:
        raw = load_reference()
        raw["local_frame"]["z_axis"] = [0.0, 0.0, -1.0]
        with self.assertRaisesRegex(PartContractViolation, "right-handed"):
            PartContract.from_mapping(raw)
        raw = load_reference()
        raw["interfaces"][0]["interface_type"] = "magic_joint"
        with self.assertRaisesRegex(PartContractViolation, "unsupported interface_type"):
            PartContract.from_mapping(raw)

    def test_incomplete_or_unknown_parameter_provenance_fails_closed(self) -> None:
        raw = load_reference()
        del raw["parameter_provenance"]["features.base_sketch.parameters.length_m"]
        with self.assertRaisesRegex(PartContractViolation, "parameter provenance mismatch"):
            PartContract.from_mapping(raw)
        raw = deepcopy(load_reference())
        raw["parameter_provenance"]["undeclared.parameter_m"] = deepcopy(
            next(iter(raw["parameter_provenance"].values()))
        )
        with self.assertRaisesRegex(PartContractViolation, "parameter provenance mismatch"):
            PartContract.from_mapping(raw)


if __name__ == "__main__":
    unittest.main()
