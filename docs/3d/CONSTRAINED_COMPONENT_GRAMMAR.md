# Constrained Component Grammar Version 1

Thai companion: `CONSTRAINED_COMPONENT_GRAMMAR.th.md`

## Claim Boundary

`mounting_plate_v1` is the first narrow geometry and interface language used to
exercise the project's CAD evidence path. Passing the grammar means only that a
candidate is expressible inside declared dimensional and topology constraints.
It does not establish strength, stiffness, fatigue life, manufacturability,
safety, usefulness, or optimality.

## Production

```text
mounting_plate_v1
  := rounded_prismatic_plate
   + symmetric_four_hole_mounting_interface
   + optional_central_circular_lightening_cut
   + constant_density_material_assumption
```

The production always yields one intended prismatic solid. The four mounting
holes are interface ports, not free topology. Version 1 has no stochastic
production, but every experiment still records a seed so replay metadata does
not need a later schema break.

## Units and Coordinates

All grammar values are SI:

- length, width, thickness, radii, spacing, bounds, and centre of mass: metres;
- volume: cubic metres;
- density: kilograms per cubic metre;
- mass: kilograms.

The plate is centred on `X=0, Y=0`, begins at `Z=0`, and extends through positive
`Z`. CadQuery accepts millimetres, so the generator multiplies metres by `1000`
only inside the CAD adapter. CadQuery and FreeCAD measurements are divided by
the corresponding metric conversion before entering the evidence contract.

## Declared Parameters and Constraints

| Parameter | Version 1 range | Additional rule |
|---|---:|---|
| `length_m` | `[0.12, 0.30]` | finite |
| `width_m` | `[0.08, 0.20]` | finite |
| `thickness_m` | `[0.004, 0.015]` | finite |
| `corner_radius_m` | `[0.002, 0.030]` | at most one quarter of the smaller outer dimension |
| `mounting_hole_diameter_m` | `[0.005, 0.012]` | four equal holes |
| `mounting_spacing_x_m` | `[0.012, 0.260]` | symmetric about the origin |
| `mounting_spacing_y_m` | `[0.012, 0.160]` | symmetric about the origin |
| `lightening_radius_m` | `[0.0, 0.080]` | `0` omits the central cut |
| `density_kg_per_m3` | greater than `0` | finite, constant-density assumption |

Interface and web constraints are evaluated before CadQuery executes:

- mounting-hole edge ligament is at least `0.006 m` in both axes;
- mounting holes also retain that ligament to the rounded-corner arc, not only
  to the axis-aligned outer bounds;
- mounting-hole centre pitch leaves at least `0.006 m` between hole edges;
- a central cut leaves at least `0.006 m` to the nearest outer edge;
- a central cut leaves at least `0.006 m` to every mounting-hole edge;
- unknown schema keys, missing keys, wrong grammar versions, and non-finite
  values are rejected rather than clipped.

For this prismatic family, the analytical volume reference is:

```text
A_outer = length*width - (4 - pi)*corner_radius^2
A_cut = 4*pi*(mounting_hole_diameter/2)^2 + pi*lightening_radius^2
volume = (A_outer - A_cut)*thickness
mass = FreeCAD_STEP_volume*density
```

The analytical mass is recorded for comparison, but the Level 0 input uses the
FreeCAD STEP-import volume, not the generator's self-reported value.

## Evidence Loop

```text
versioned JSON candidate
  -> pure-Python grammar validation
  -> CadQuery B-rep generation and single-solid gate
  -> STEP file plus SHA-256 manifest
  -> FreeCAD headless import of that exact hash
  -> independent validity, solid-count, volume, bounds, and centre measurement
  -> analytical/CadQuery/FreeCAD residual gates
  -> FreeCAD volume * declared density
  -> total Level 0 point mass
  -> constant-traction final speed and distance
```

No failed CAD value is replaced with the analytical value. Current volume
tolerances are `1e-10 m^3` absolute and `1e-6` relative; bounding-box tolerance
is `1e-7 m`. The experiment configuration is
`config/work006_mounting_plate.json`.

## Controlled Work 006 Experiment

The predeclared independent variable is central cut radius: `0`, `0.025`, and
`0.040 m`. Outer dimensions, mounting interface, density, seed, base vehicle
mass, force, duration, timestep, and software route remain fixed. The preferred
hypothesis is decreasing volume/mass and increasing Level 0 final speed/distance
as the cut radius increases.

The deliberate `0.055 m` invalid radius must fail the outer-ligament rule before
CadQuery runs. This negative case is part of the experiment, not a discarded
generation failure.

Run the complete local loop with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work006.ps1
```

Generated STEP, manifests, independent measurements, and the combined summary
are stored under the Git-ignored `artifacts/work006/` directory.

## Interpretation Limits

CadQuery and FreeCAD are separate applications in this loop but both rely on
OCCT-family solid geometry, so agreement is not fully independent geometric
theory. Level 0 then treats the imported volume only as constant-density added
point mass. Work 006 has no loads, boundary conditions, material allowables,
mesh, FEA, fatigue, joints, tolerances, manufacturing process, collision model,
or empirical calibration. Those omissions prohibit any physical-validation
claim.
