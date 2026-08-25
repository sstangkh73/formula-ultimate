# Level-0 Real-Circuit Physics Model

Status: Implemented screening baseline

Catalogue: `config/circuits/real_circuits_v1.json`

Thai companion: `CIRCUIT_MODEL.th.md`

## Purpose

The circuit model gives an agent real-world constraints before it designs a
vehicle. It prevents the design loop from treating a circuit as only a name or
a target lap time. Each circuit supplies race scale, an environmental input
where evidence exists, an auditable static-width gate, and a distinct vector of
design pressures.

This is a Level-0 feasibility screen. It is not a surveyed circuit model and it
cannot physically validate a car.

## Information flow

```text
official source facts
        |
        v
CircuitProfile ------> pre-design pressure vector
        |
        +------------> static width screen: passed / rejected / indeterminate
        |
        +------------> race distance, start-offset residual, ISA air density
                              |
                              v
                   later vehicle generation and simulation
```

## Three separated evidence layers

1. **Published facts:** lap length, lap count, official race distance, corner
   count, reference altitude, and published width where an applicable official
   source was found. Every width value links to one declared source ID.
2. **Derived screening inputs:** eight ordinal design-pressure scores and short
   strength/weakness statements. These encode research hypotheses from the
   official circuit descriptions; they are not measured forces or lap-time
   weights.
3. **Observable outputs:** ISA density, official-distance residual, and the
   width result. Missing evidence remains visible as `indeterminate`.

The eight pressure axes are `straight_speed`, `low_speed_agility`,
`high_speed_cornering`, `braking`, `traction`, `elevation`,
`thermal_cooling`, and `confinement`. Version 1 uses only
`0.00, 0.25, 0.50, 0.75, 1.00`. This coarse ordinal scale avoids false
precision. All ten vectors are distinct.

## Static vehicle-width screen

For a vehicle width \(w_v\), required clearance per side \(c\), and an optional
evidence allowance \(u\), the necessary static corridor is

\[
w_{required} = w_v + 2c + u.
\]

It is compared with the applicable published minimum track width
\(w_{published,min}\):

- `rejected` when \(w_{required} > w_{published,min}\);
- `screen_passed` when \(w_{required} \le w_{published,min}\); or
- `indeterminate` when there is no applicable width evidence.

`screen_passed` means only that the static rectangle is not wider than the
published minimum. It does not establish that the vehicle can negotiate a
corner. Wheelbase, steering lock, tyre envelope, body overhang, wall position,
kerbs, banking, pitch/roll, and the complete swept path need surveyed 3D
corridor geometry in a later work item.

Example command:

```powershell
python scripts/validate_circuits.py --vehicle-width-m 7.0 --clearance-per-side-m 0.25
```

With the current evidence this rejects the vehicle at Monaco, passes only the
static screen at Monza, Suzuka, and Sao Paulo, and reports the other six
circuits as indeterminate. An agent cannot treat an indeterminate circuit as
admitted.

## Atmospheric screening

Where a sourced reference altitude exists, the model calculates dry-air
density in the International Standard Atmosphere troposphere:

\[
T = T_0-Lh,
\qquad
p = p_0\left(\frac{T}{T_0}\right)^{g_0/(RL)},
\qquad
\rho = \frac{p}{RT}.
\]

Constants use SI units: \(T_0=288.15\ K\), \(p_0=101325\ Pa\),
\(L=0.0065\ K/m\), \(g_0=9.80665\ m/s^2\), and
\(R=287.05287\ J/(kg\,K)\). At Mexico City's sourced `2,285 m`, the model
returns approximately `0.978 kg/m^3`; at sea level it returns approximately
`1.225 kg/m^3`.

This is a reference atmosphere, not event weather. It must not silently replace
measured pressure, temperature, humidity, wind, or track-temperature data when
those become available.

## Race-distance residual

The catalogue preserves both the official race distance and
`lap_length_m * race_laps`. Their difference is exposed as
`race_start_offset_m`. It is not corrected away because published lap lengths
are rounded and the race start can be offset from the finish line. For example,
Monza exposes `-309 m`.

## Current evidence boundary

- Ten real circuits are present: Monaco, Monza, Spa-Francorchamps, Singapore,
  Suzuka, Silverstone, Hungaroring, Mexico City, Bahrain, and Sao Paulo.
- Applicable official width evidence is currently available for four profiles:
  Monaco, Monza, Suzuka, and Sao Paulo.
- Singapore's organizer published `10-15 m` for the superseded 2008 layout. It
  is retained only as evidence explaining why the current width is unresolved;
  it is not reused as a current hard limit.
- Bahrain's operator publishes `14-15 m` for the Inner Track, not the Grand
  Prix Track. The value is retained only as non-applicable evidence and Bahrain
  remains indeterminate.
- Only Mexico City currently has a sourced numerical altitude in this version.
- Grip, surface roughness, camber, banking, gradient by station, wall geometry,
  kerbs, weather distributions, pit geometry, and a 3D centerline/corridor are
  not implemented.
- The strength/weakness and pressure fields are hypotheses for controlled
  comparison. They require later sensitivity analysis and falsification against
  telemetry or higher-fidelity simulation.

## Next validation level

The next circuit work should ingest a versioned 3D centerline and left/right
boundaries, record coordinate reference system and survey uncertainty, then run
the complete vehicle envelope through a swept-volume collision test. That is
the point where vehicle length, wheelbase, steering geometry, overhang, and body
shape can become track-specific hard constraints rather than prose warnings.
