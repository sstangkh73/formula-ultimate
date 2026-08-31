# Stable Support Topology and Planar Gate v1

Thai companion: `STABLE_SUPPORT_TOPOLOGY_PLANAR_GATE_V1.th.md`

## Result and claim boundary

Work 069 falsified the frozen Work 066/068 two-contact fixture before extending its dynamics. Both v2 contacts lie on the line `x = 0.45 m`, but the geometry-derived centre-of-mass projection is at `x = -0.0249520887695175 m`. Its support hull is degenerate, has area `0 m^2`, and has signed margin `-0.4749520887695175 m`; it cannot close static pitch equilibrium.

A separate v3 reference adds one bounded passive rear support at `(-0.55, 0, 0) m`. This preserves the two powered contacts and all functional energy, control, thermal, braking, and structural paths while forming a technology-neutral three-contact polygon. It does not prescribe a four-wheel layout and is not an optimized vehicle.

The result admits geometry-derived static/quasi-static support and Level-0 planar steering only. It is not physical validation, a suspension model, a measured tyre model, or evidence that the whole vehicle can complete a race.

## Geometry-derived support

The materialized v3 architecture has `11` components, `24` connections, and `3` ground contacts. Its aggregate properties are:

```text
mass = 276.89543100079806 kg
centre of mass = (-0.0331871483063111, 9.21878252910516e-19, 0.276183105667901) m
support polygon area = 0.32000000000000006 m^2
signed centre-of-mass margin = 0.15751201265152398 m
```

The three normal loads are solved directly from component and port world positions:

```text
sum(N_i) = m g
sum((x_i - x_COM) N_i) = -m a_x h
sum((y_i - y_COM) N_i) = -m a_y h.
```

No negative load is clipped. Therefore a negative solution remains explicit contact-lift evidence.

## Frozen quasi-static load cases

| Case | Acceleration `(a_x, a_y)` | Loads `(left, right, rear)` N | Minimum N | Result |
| --- | ---: | ---: | ---: | --- |
| static | `(0, 0) m/s^2` | `(701.681093, 701.681093, 1312.054393)` | `701.681093` | passed |
| acceleration | `(6, 0) m/s^2` | `(472.259572, 472.259572, 1770.897433)` | `472.259572` | passed |
| braking | `(-6, 0) m/s^2` | `(931.102613, 931.102613, 853.211353)` | `853.211353` | passed |
| lateral left | `(0, 3) m/s^2` | `(343.209967, 1060.152218, 1312.054393)` | `343.209967` | passed |
| lateral right | `(0, -3) m/s^2` | `(1060.152218, 343.209967, 1312.054393)` | `343.209967` | passed |
| contact-lift control | `(0, 8) m/s^2` | `(-254.241908, 1657.604094, 1312.054393)` | `-254.241908` | contact_lift |

The largest absolute quasi-static equilibrium residual was `2.2737367544323206e-13 N m`, below the frozen relative tolerance `1e-9`. All admitted cases retained positive loads and stayed below declared normal-force capacities. The `8 m/s^2` falsification case lost contact as intended.

## Planar steering response

The planar specimen starts at `10 m/s`, applies `300 N` requested longitudinal force at each powered contact, uses steering angle magnitude `0.02 rad`, runs for `0.5 s`, and uses step `0.002 s`. The protocol steering ceiling is reconciled with the architecture direction actuator limit `0.6 rad`.

| Control | Final `y` m | Heading rad | Yaw rate rad/s | Result |
| --- | ---: | ---: | ---: | --- |
| zero steer | `0` | `0` | `0` | passed |
| `+0.02 rad` | `0.239430705274132` | `0.173102791267070` | `0.573668613831193` | passed |
| `-0.02 rad` | `-0.239430705274132` | `-0.173102791267070` | `-0.573668613831193` | passed |

Positive and negative responses are exactly antisymmetric for the selected lateral states. The positive run executed all `250` steps, retained minimum dynamic normal load `116.77062376095432 N`, and had maximum combined tyre utilization `1.0000000000000002`; the excess over one is floating-point roundoff within `1e-12`, not force beyond the boundary. Maximum force/moment balance residual was `2.277775479342381e-8` in the solver's reported units.

Halving the step to `0.001 s` changed selected terminal metrics by at most `0.001216322032258299`, below the frozen `0.02` relative ceiling. Exact execution replay reproduced result hash `8bfd4a8ea64cac71821930ea7e4769eeb0c7094639d16fc6edde4de6e5974936`.

## STEP and independent FreeCAD evidence

The materialized architecture hash is `cf78a1c499790aed6c8b117c8f583a427a9d91a9fb36605e2b7038b2907b1418`. CadQuery generated one valid STEP solid for each of the `11` components and an `11`-solid assembly with SHA-256 `a260b74185fbd473ef33fb0e71387121af25c045609a4007347e3256b3affaf4`.

FreeCAD `1.1.0` independently imported every component and the assembly. Its maximum relative mass/centre/inertia residual was `5.000115436834047e-16`, below the declared `1e-6` threshold. No hidden geometry repair was used. A clean replay reproduced the materialized JSON bytes, experiment evidence hash, assembly hash, every component STEP hash, and FreeCAD mass exactly.

The canonical experiment evidence SHA-256 is `d3a480c4637f5955668259d7e3b52b8bc474ce084a32359964558d4c624a81b5`.

## Falsification, contradictory evidence, and confidence

- The preferred hypothesis was contradicted for v2: it is statically inadmissible despite having valid individual solids and functional connections.
- The excessive lateral case disproved any claim that the v3 fixture remains supported under arbitrary acceleration.
- A previous exploratory `0.04 rad` steer command caused contact lift at `0.368 s`; the frozen admitted specimen uses `0.02 rad`. This is a physical/numerical boundary, not silently repaired output.
- Mutated base identity, excessive numerical tolerance, and steering limits inconsistent with the direction actuator fail closed.
- Eight focused tests and all `412` repository tests passed.

Confidence is high for deterministic contract enforcement, geometry identity, static equilibrium, declared load cases, Level-0 steering sign, STEP import, and replay. Confidence remains low for real transient handling because compliance, damping, tyre measurement, road input, aerodynamic transient load, and physical testing are absent.

## Missing evidence and next work

The three-contact reference uses a rigid quasi-static support solution. It omits suspension travel, pitch/roll/heave inertia, wheel-hop, road roughness, tyre relaxation length, camber, thermal/wear evolution, contact patch pressure, actuator dynamics, and validated coefficients. Its front contacts still share the one output shaft speed from Work 067.

Work 070 should add an explicit differential/carrier energy contract before introducing independent driven-contact angular speeds. Each branch must own declared inertia, torque, speed, slip power, heat, limits, and failure state so that splitting the shaft cannot duplicate inertia or create energy. Only after that should the reference be coupled to a circuit trajectory and whole-race gate.
