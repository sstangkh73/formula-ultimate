"""Structural solver contracts and verification evidence."""

from .acceptance import (
    MeshData,
    StructuralEvidenceError,
    TensionSpec,
    build_calculix_input,
    parse_calculix_dat,
    parse_msh2,
)

__all__ = [
    "MeshData",
    "StructuralEvidenceError",
    "TensionSpec",
    "build_calculix_input",
    "parse_calculix_dat",
    "parse_msh2",
]
