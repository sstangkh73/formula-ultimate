"""Typed physical components and versioned component catalogs."""

from .grammar import (
    GRAMMAR_VERSION,
    GrammarViolation,
    Material,
    MountingPlateSpec,
)
from .part_contract import (
    INTERFACE_TYPES,
    PART_CONTRACT_VERSION,
    PartContract,
    PartContractViolation,
    canonical_part_bytes,
    part_declaration_sha256,
    validate_part_mapping,
)
from .brep_grammar import (
    BREP_GRAMMAR_VERSION,
    OPERATORS as BREP_OPERATORS,
    BrepGrammarViolation,
    brep_declaration_sha256,
    validate_brep_grammar,
)
from .engineering_contracts import (
    GEOMETRY_WITNESS_VERSION,
    MANUFACTURING_CONTRACT_VERSION,
    MATERIAL_CONTRACT_VERSION,
    EngineeringContractViolation,
    evaluate_manufacturing_witness,
    record_sha256,
    validate_engineering_assignment,
    validate_manufacturing_process,
    validate_material_record,
)

__all__ = [
    "GRAMMAR_VERSION",
    "GrammarViolation",
    "Material",
    "MountingPlateSpec",
    "INTERFACE_TYPES",
    "PART_CONTRACT_VERSION",
    "PartContract",
    "PartContractViolation",
    "canonical_part_bytes",
    "part_declaration_sha256",
    "validate_part_mapping",
    "BREP_GRAMMAR_VERSION",
    "BREP_OPERATORS",
    "BrepGrammarViolation",
    "brep_declaration_sha256",
    "validate_brep_grammar",
    "GEOMETRY_WITNESS_VERSION",
    "MANUFACTURING_CONTRACT_VERSION",
    "MATERIAL_CONTRACT_VERSION",
    "EngineeringContractViolation",
    "evaluate_manufacturing_witness",
    "record_sha256",
    "validate_engineering_assignment",
    "validate_manufacturing_process",
    "validate_material_record",
]
