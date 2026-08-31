# Work 069 Result: Stable Support Topology and Planar Gate

English result for `2026-08-31_069_stable-support-topology-planar-gate-plan.md`.

Status: Completed

Thai companion: `2026-08-31_069_stable-support-topology-planar-gate-result.th.md`

## Outcome

The frozen v2 two-contact architecture was correctly rejected as statically unstable. A separate v3 architecture added one passive rear ground support, passed the functional architecture contract, formed a positive-area support polygon around the geometry-derived centre of mass, passed the declared static/quasi-static load cases, exposed the deliberate contact-lift case without clipping, and produced bounded sign-correct planar steering responses.

The same materialized geometry produced `11` deterministic STEP solids. Independent FreeCAD import reproduced aggregate mass, centre, and inertia within a maximum relative residual `5.000115436834047e-16` against tolerance `1e-6`.

## Files changed

- `config/vehicle/functional_vehicle_architecture_v3_planar.json`
- `config/vehicle/planar_support_gate_v1.json`
- `src/formula_ultimate/simulation/planar_support_gate.py`
- `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_planar_support_gate.py`
- `tests/test_planar_support_gate.py`
- `docs/research/STABLE_SUPPORT_TOPOLOGY_PLANAR_GATE_V1.md`
- `docs/research/STABLE_SUPPORT_TOPOLOGY_PLANAR_GATE_V1.th.md`
- matching bilingual Work 069 plan/result records

Generated evidence under ignored `artifacts/work069/` includes the materialized architecture, experiment JSON, component/assembly STEP, CadQuery manifest, FreeCAD report, and an independent replay tree.

## Decisions and evidence

- v2 support margin: `-0.4749520887695175 m`; status `unstable`.
- v3 support area: `0.32000000000000006 m^2`; margin `0.15751201265152398 m`; status `stable`.
- v3 mass: `276.89543100079806 kg`; contacts: `3`; components: `11`.
- Minimum load over admitted frozen quasi-static cases: `343.2099673452492 N`.
- Excess lateral control: minimum load `-254.24190827234736 N`; status `contact_lift`.
- Positive `0.02 rad` steer final heading: `0.1731027912670698 rad`; yaw rate: `0.5736686138311934 rad/s`.
- Zero steer remained exactly zero in lateral position, heading, lateral velocity, and yaw rate; equal negative steer produced exact opposite selected lateral states.
- Maximum planar contact utilization: `1.0000000000000002`, admitted within `1e-12` roundoff.
- Half-step maximum selected relative difference: `0.001216322032258299`, below `0.02`.
- Experiment evidence SHA-256: `d3a480c4637f5955668259d7e3b52b8bc474ce084a32359964558d4c624a81b5`.
- Materialized architecture SHA-256: `cf78a1c499790aed6c8b117c8f583a427a9d91a9fb36605e2b7038b2907b1418`.
- Assembly STEP SHA-256: `a260b74185fbd473ef33fb0e71387121af25c045609a4007347e3256b3affaf4`.
- Replay matched architecture bytes, evidence hash, assembly hash, all component STEP hashes, and FreeCAD mass exactly.

## Exact validation commands and status

```powershell
python -m unittest tests.test_planar_support_gate -v
# exit 0; Ran 8 tests; OK

python scripts/experiments/run_planar_support_gate.py --config config/vehicle/planar_support_gate_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work069/materialized_architecture_v3.json --output artifacts/work069/experiment_evidence.json
# exit 0; status passed

.\.tools\cadquery-mcp\Scripts\python.exe scripts/cad/generate_functional_vehicle_v2.py --config artifacts/work069/materialized_architecture_v3.json --output-root artifacts/work069/step --manifest artifacts/work069/cadquery_manifest.json
# exit 0; component_count 11; status passed

& 'C:\Program Files\FreeCAD 1.1\bin\python.exe' scripts/cad/inspect_functional_vehicle_v2_freecad.py artifacts/work069/cadquery_manifest.json artifacts/work069/materialized_architecture_v3.json artifacts/work069/freecad_report.json
# exit 0; component_count 11; maximum_residual 5.000115436834047e-16; status passed

# The experiment, CadQuery, and FreeCAD commands were repeated under artifacts/work069/replay.
# Comparison: evidence_exact=true, architecture_bytes_exact=true,
# assembly_exact=true, component_hashes_exact=true, freecad_mass_exact=true.

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests
# exit 0; Ran 412 tests in 36.327s; OK
```

## Limitations and follow-up

This remains synthetic Level-0 evidence. It has rigid quasi-static support, fixed cornering stiffness/friction, no suspension transient, no tyre measurement, no aerodynamic transient, and no real-world validation. The admitted `0.02 rad` specimen does not prove arbitrary steering commands are safe; the exploratory `0.04 rad` run caused contact lift.

Independent left/right driven speeds remain intentionally deferred. Work 070 must define a differential/carrier energy and inertia contract before branching the common Work 067 output shaft. Whole-race claims remain blocked until that drivetrain branch model, higher-fidelity chassis/contact evidence, circuit trajectory coupling, and physical validation are added.
