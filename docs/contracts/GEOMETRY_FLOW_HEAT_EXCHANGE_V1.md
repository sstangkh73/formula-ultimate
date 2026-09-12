# Geometry Flow and Heat Exchange V1

Thai companion: `GEOMETRY_FLOW_HEAT_EXCHANGE_V1.th.md`

Status: Implemented by Work 121 as two bounded Level-0 reference scopes.

## Geometry and separate scopes

This contract pins the exact Work 110 finest hollow B-rep Gmsh artifact, Work 115 `10 W` heat source and Work 116 material limitation. Gmsh node bounds determine an external projected YZ area; an explicitly registered bounded circular adapter supplies internal passage length/diameter. Inlet, outlet and wall boundaries are separate from body-wall, far-field and symmetry boundaries.

Internal flow is limited to a synthetic laminar, constant-property, circular passage below Reynolds `2300`. Hagen-Poiseuille pressure drop and fully developed constant-wall-temperature Nusselt `3.66` are the analytic references. Segment counts `10`, `20`, `40` must converge monotonically to analytic heat-transfer capacity; source heat, outlet enthalpy and wall heat must close within `1e-10 W`.

External flow is a separate synthetic incompressible subsonic quadratic-drag adapter. Pressure and shear fractions must sum to total drag within `1e-12 N`. Far-field widths `0.5`, `1.0`, `2.0 m` use an explicit blockage correction; the finest domain error must be at most `0.001`.

## Controls and claim boundary

Blocked passage, zero flow/source/speed, passage-diameter mutation, projected-area mutation and domain sensitivity are mandatory. Geometry changes must causally change pressure or drag. Loads and heat are returned to the assembly, but internal success cannot establish external or whole-car aerodynamics.

Fluid properties, closures and drag coefficient are synthetic. Turbulence, cavitation, compressibility, arbitrary passages, conforming fluid meshes, conjugate 3D CFD, validated cooling, whole-car aerodynamics and physical validation remain unresolved.
