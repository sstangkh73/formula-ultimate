"""Structural solver contracts and verification evidence."""

from .acceptance import (
    BendingSpec,
    MeshData,
    StructuralEvidenceError,
    TensionSpec,
    build_bending_calculix_input,
    build_calculix_input,
    parse_calculix_dat,
    parse_msh2,
)

__all__ = [
    "BendingSpec",
    "MeshData",
    "StructuralEvidenceError",
    "TensionSpec",
    "build_bending_calculix_input",
    "build_calculix_input",
    "parse_calculix_dat",
    "parse_msh2",
]
