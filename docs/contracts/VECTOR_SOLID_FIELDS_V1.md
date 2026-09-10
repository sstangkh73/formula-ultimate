# Vector Solid Fields V1

Thai companion: `VECTOR_SOLID_FIELDS_V1.th.md`

Status: Implemented by Work 111 for bounded Level-0 evidence.

## Scope, units and dependency

This contract solves small-strain, isotropic, linear elasticity on Work 110 four-node tetrahedral meshes. Coordinates and displacement are in `m`, force in `N`, stress and Young's modulus in `Pa`, density in `kg/m3`, acceleration in `m/s2`, and strain energy in `J`. The exact Work 110 commit and `GEOMETRY_MESH_BRIDGE_V1.md` SHA-256 are frozen before a run.

The material record is a synthetic fixture, not certified production data. The output is Level-0 numerical field evidence only. It does not establish nonlinear response, contact, plasticity, fatigue, strength, vehicle feasibility, manufacturing feasibility or physical validation.

## Formulation and boundary conventions

Every mesh node has three translational displacement DOFs. A constant-strain tetrahedron uses the symmetric engineering-strain vector `[exx, eyy, ezz, gxy, gyz, gxz]` and the three-dimensional isotropic elasticity matrix. Element stiffness is `Ke = V B^T D B`. Consistent body force is `density * V * acceleration / 4` per node.

The declared resultant is distributed uniformly by triangle area over `load_surface`. All three translations on every `contact_surface` node are fixed. Reactions are recovered from `K u - f` on constrained DOFs; they are not assigned from the input resultant. A graph path must connect at least one loaded node to one supported node. Missing supports, singular/non-finite solves, severed paths, non-positive Young's modulus and invalid tetrahedra fail closed.

## Registered quantities and gates

Outputs include the full displacement vector field, six-component element stress field, von Mises stress, loaded-face mean displacement, maximum displacement, compliance, strain energy, recovered resultant reaction and deterministic SHA-256 identities. Sharp-corner maxima are excluded from acceptance; the registered stress quantity is the element-volume-weighted p90 von Mises stress.

For every admitted solve, relative force and moment residuals must not exceed `1e-8`, the strain-energy/work residual must not exceed `1e-10`, and the minimum-to-maximum free-DOF stiffness diagonal proxy must be at least `1e-6`. The proxy is observable screening evidence, not a spectral condition number.

The structured cuboid reference uses `0.04`, `0.02` and `0.01 m`; its finest loaded-face axial displacement must agree within `8%` of `F L / (E A)`. Affine patch, rigid translation and rigid rotation strain errors must be at most `1e-12`. The unfamiliar Work 109 field is routed through Work 110 at `0.02`, `0.01` and `0.008 m`; the last-two relative change of maximum displacement, compliance and p90 von Mises stress must each be at most `0.8`. This bound is a selection gate, not proof of asymptotic convergence.

## Falsification and handoff

Controls must reject unsupported rigid modes, a disconnected load path and corrupt stiffness. Doubling Young's modulus must halve compliance, while registered load-direction and geometry mutations must change the displacement-field identity. A prohibited uniform reaction assignment is hashed independently and must differ from the recovered reaction field.

Exact replay requires the same result SHA-256. Work 113 and Work 115 may consume these fields only with the declared mesh, material, load, support, resolution and limitation metadata. Any higher-fidelity or physical claim requires independent validation beyond this contract.
