# Semantic Geometry Witness V3

Thai companion: `SEMANTIC_GEOMETRY_WITNESS_V3.th.md`

## Boundary

V3 independently imports the exact ten Work 092 STEP files with FreeCAD/OCCT and emits order-invariant semantic evidence. Passing proves inspection of this frozen corpus. It does not prove structural validity, global minimum thickness, assembly clearance, manufacturability, safety, or physical validity.

## Geometry evidence

Each record includes body/solid/shell counts, validity, volume, area, declared-density mass, centre of mass, full inertia, deterministic principal axes, degeneracy, axis-aligned and principal-oriented bounds, face signatures, curvature samples/spectra, material-span thickness samples, section evolution, declared datums, semantic regions, path evidence, within-candidate clearance/interference, and a static swept envelope.

Thickness values are exact B-rep line-intersection spans at frozen grid and per-solid-centre probes; they are sampled values, not a guaranteed wall minimum. Section area is thin-slab intersection volume divided by slab thickness. Its second moment is explicitly a bounding proxy. Curvature radii come from finite fixed-parameter `Face.curvatureAt` samples.

## Semantic correspondence

Support and load regions use extreme face-centroid rules along the declared longest path. Contact uses the largest-area boundary set, thermal uses all faces, and fluid uses curved faces or all faces when no curved face exists. Each region hashes the sorted face-signature set and area. Datum and region recovery never uses a face ordinal. Missing, ambiguous, altered, or stale semantics fail closed.

## Replay

Exact STEP, manifest, sampling, toolchain, and configuration identities are retained. A clean rerun must reproduce the report and comparison. Permuting candidate, face, datum, or region records may change the raw report hash but must preserve the normalized semantic comparison identity.
