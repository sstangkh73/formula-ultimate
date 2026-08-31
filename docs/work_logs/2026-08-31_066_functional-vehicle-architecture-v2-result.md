# Work 066 Result: Functional Vehicle Architecture v2

Thai companion: `2026-08-31_066_functional-vehicle-architecture-v2-result.th.md`

Status: Completed

## Outcome

Implemented a technology-neutral functional-vehicle grammar and a ten-component reference candidate. Admission now requires compatible typed ports and explicit structural, power, thermal, control, and ground paths. A declared propulsion component with no storage-to-ground power path fails as `force-from-nowhere`.

The reference generated ten component STEP files and one ten-solid assembly. CadQuery generation, independent FreeCAD import, mass-property comparison, and separate-directory deterministic replay passed without hidden repair.

## Files changed

- `src/formula_ultimate/topology/functional_vehicle.py`
- `src/formula_ultimate/topology/__init__.py`
- `config/vehicle/functional_vehicle_architecture_v2.json`
- `scripts/cad/generate_functional_vehicle_v2.py`
- `scripts/cad/inspect_functional_vehicle_v2_freecad.py`
- `tests/test_functional_vehicle_architecture.py`
- `docs/research/FUNCTIONAL_VEHICLE_ARCHITECTURE_V2.md`
- `docs/research/FUNCTIONAL_VEHICLE_ARCHITECTURE_V2.th.md`
- this bilingual plan/result set

Ignored generated evidence is under `artifacts/work066/`. The principal viewable model is `artifacts/work066/step/assembly.step`.

## Decisions

- Capabilities are inferred from function tags and connected physical domains, not component names or a prescribed vehicle layout.
- The fixed reference is an evidence baseline, not a preferred discovered solution and not a replacement for the frozen Work 062 campaign.
- Each functional component remains a separate solid. Primitive geometry is intentionally sufficient only for architecture, packaging, and deterministic mass-property checks.
- Energy and torque conservation are local fail-closed admission checks; control connections carry no power.
- Geometry mismatch, invalid state, broken path, or replay mismatch is reported rather than repaired.

## Validation evidence

Reference grammar validation returned `status=passed`, `component_count=10`, `port_count=48`, `connection_count=23`, `ground_contact_count=2`, and mass `272.55249331647553 kg`. Its validation identity is `d29f5d51a9b23db2dce9c33f93539cb71afaa020709fc5bcb69b2b6ebaa27677`.

Command:

```powershell
py -3.14 -m unittest tests.test_functional_vehicle_architecture -q
```

Exit status `0`; output: `Ran 7 tests ... OK`. Negative controls covered missing power/structural/thermal/control paths, port incompatibility, invalid limits, undeclared power/torque creation, overlap, outside ports, invalid ground elevation, excessive connection length, and cylinder-axis inertia.

Command:

```powershell
.\.tools\cadquery-mcp\Scripts\python.exe scripts/cad/generate_functional_vehicle_v2.py --config config/vehicle/functional_vehicle_architecture_v2.json --output-root artifacts/work066/step --manifest artifacts/work066/cadquery_manifest.json
```

Exit status `0`; generated 10 valid components and a valid 10-solid assembly. Assembly SHA-256: `983902b813ab6ee3fd69c703521ee32206e224b98013f430d1aeee7249ac75da`.

Command:

```powershell
& 'C:\Program Files\FreeCAD 1.1\bin\python.exe' scripts/cad/inspect_functional_vehicle_v2_freecad.py artifacts/work066/cadquery_manifest.json config/vehicle/functional_vehicle_architecture_v2.json artifacts/work066/freecad_report.json
```

Exit status `0`; FreeCAD 1.1.3 independently confirmed 10 valid solids. Relative residuals were mass `2.0855952616365914e-16`, centre `1.2421529906547113e-17`, and inertia `7.979411838121619e-18`, each below `1e-6`.

The same generation and inspection were repeated under `artifacts/work066/replay/`. Exit status was `0`; the assembly hash and all 10 component hashes matched exactly.

Commands:

```powershell
py -3.14 -m unittest discover -s tests -q
py -3.14 -m compileall -q src scripts tests
git diff --check
```

Exit statuses were `0`; full output: `Ran 388 tests ... OK`; compilation and diff checks emitted no errors.

## Limitations and contradicting evidence

No contradictory result was observed inside the declared architecture/CAD checks. However, passing these checks does not show that the reference can accelerate, steer, brake, reject heat, survive loads, or complete a race. Component limits are synthetic declarations, not measured maps or certified allowables. The model omits transient dynamics, electrical state, torque-speed behavior, shaft compliance, tyre slip, suspension, detailed joints, thermal state, nonlinear material response, fatigue, fracture, buckling, crashworthiness, manufacturability, and safety validation. Level 0 and primitive CAD cannot close those claims.

## Follow-up

Work 067 should implement and analytically validate the coupled storage-converter-transmission dynamic path, including state, efficiency/loss heat, torque-speed limits, inertia, compliance, failure states, and deterministic replay. Subsequent work should connect that path to ground-force/slip, steering/braking, thermal, and structural solvers before any whole-car optimization claim.
