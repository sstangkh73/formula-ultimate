# Work 047 Result: Topology-Neutral Whole-Vehicle CAD and Assembly Grammar

Status: Completed

Thai companion: `2026-08-30_047_topology-neutral-vehicle-assembly-result.th.md`

## Outcome

Implemented and validated the v1 topology-neutral multi-solid assembly grammar. The four-solid, one-contact fixture passed explicit interface, connection, energy/load path, envelope, keep-out, ground, deterministic STEP, FreeCAD validity, and mass-property gates.

## Files changed

- `config/vehicle/topology_neutral_vehicle_v1.json`
- `src/formula_ultimate/topology/vehicle_assembly.py` and exports
- `scripts/cad/generate_vehicle_assembly.py`
- `scripts/cad/inspect_vehicle_assembly_freecad.py`
- `scripts/topology/run_vehicle_assembly_acceptance.py`
- `scripts/run_work047.ps1`
- `tests/test_vehicle_assembly.py`
- `docs/physics/TOPOLOGY_NEUTRAL_VEHICLE_ASSEMBLY.md` and `.th.md`
- matching Work 047 bilingual plan/result records

Ignored CAD/STEP evidence is under `artifacts/work047/`.

## Decisions and evidence

- Used primitive function tags and variable declarations rather than a conventional-car schema.
- Used per-component STEP hashes and signatures because STEP labels are not trusted as identity.
- Four valid solids and one explicit contact produced mass `30.657168026350796 kg`.
- Maximum mass/centre/inertia relative error was `1.7042240975184457e-15`; interface residual was `1.3877787807814457e-17 m`.
- Two independent exports had identical assembly SHA-256 `f60bb686dfaca51c06bed8b1b086418c5f9ce2208d861b5b2ff18d8f845f18b9`.
- Eight negative controls failed closed.
- The first exploratory cylinder used `both=True`, doubled declared height, and produced a `4.43%` mass discrepancy. FreeCAD exposed it; the run was not admitted and the generator was corrected without changing the declaration or thresholds.
- A combined temp-probe command containing recursive deletion was rejected by host safety policy; the probe was rerun in an explicit artifact directory without that deletion.

## Exact validation

```powershell
py -3.14 -m unittest tests.test_vehicle_assembly tests.test_repository_contract -v
# exit 0; Ran 9 tests; OK

.\scripts\run_work047.ps1
# exit 0; status=passed; solid_count=4; mass_kg=30.657168026350796
# max_mass_property_error=1.7042240975184457e-15
# replay=exact; negative_controls=8

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 322 tests in 35.715s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0
```

Repository-contract checks, staged `git diff --cached --check`, explicit commit, and clean-tree Work 047 replay are verified after this record exists and reported in the final handoff.

## Limitations and follow-up

Grammar v1 is primitive and translation-only. It has no arbitrary orientation, free-form solids, physical joints, contact mechanics, FEA load cases, aero/thermal evidence, manufacturing constraints, or physical validation. Work 048 may consume the exact mass/inertia/interface identity but must not infer strength or race fitness from geometric admission.
