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
]
