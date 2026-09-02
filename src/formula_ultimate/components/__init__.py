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
]
