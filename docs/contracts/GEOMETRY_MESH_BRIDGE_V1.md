# Geometry Mesh Bridge V1

Thai companion: `GEOMETRY_MESH_BRIDGE_V1.th.md`

Status: Implemented by Work 110 for two bounded routes.

## Boundary and sources

This contract creates Gmsh 2.2 tetrahedral volume and triangular semantic-surface meshes from the exact Work 109 labelled field and the exact Work 108 hollow B-rep. It proves deterministic mesh construction, identity/label transfer and bounded geometry approximation. It does not prove solver accuracy, field convergence, strength, thermal/flow behaviour, manufacturing or physical validity.

Both upstream commit and contract SHA-256 identities are frozen. The Work 109 route uses its validated implicit source field. The Work 108 route regenerates the complete Work 092 STEP corpus in original order and requires the hollow source SHA-256 `12bcac345f9395ffc766d84a8385a488c75533d162c233e6989215f8829e636d7`.

## Mesh construction and semantics

Each admitted occupied Cartesian cell is split into six tetrahedra around a fixed body diagonal. Shared grid corners become shared nodes. Negative orientation is reordered before admission; every final signed Jacobian must exceed `1e-12 m3` and edge ratio must not exceed `1.8`. No box or repaired geometry fallback exists.

Tetrahedra retain scalar material physical groups. Exterior faces create `external_surface`, negative-X faces create `load_surface`, negative-Z faces create `contact_surface`, and unlike-label neighbours create one persistent `material_interface`. Every route declares required sets; missing names or stale node references fail closed.

The B-rep route samples the actual occupied solid at cell centres. This is a disclosed voxel approximation, not a conforming curved mesh. Mesh/reference volume and constant-density mass errors must be at most `0.35`. The exact hollow centreline must remain void at every level; an outer-solid fill is an explicit negative control.

## Refinement, evidence and handoff

Both routes run `0.02`, `0.01` and `0.008 m`. Element quality, nodes, elements, deterministic visits, volume/mass errors, set coverage and identities are retained. Non-monotonic error is evidence of aliasing, not convergence. Inverted elements, missing sets, wrong units, filled cavities, stale sources, label loss, budget overflow and substitution fail visibly.

Work 111 may consume the exact Gmsh artifacts and semantic sets for vector solid fields, but must independently verify equations, boundary conditions and three-level numerical behaviour. Work 110 supplies mesh geometry only.
