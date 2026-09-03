# Work 083 Result: Ground-Interaction Candidate 001

Thai companion: `2026-09-03_083_ground-interaction-candidate-001-result.th.md`

## Status and outcome

Status: Completed

The bounded Work 083 implementation is complete. CadQuery `2.8.0` generated a five-part ground-interaction mechanism, canonical per-part STEP files, and a five-solid assembly STEP. FreeCAD `1.1.3` / OCCT `7.8.1` imported the exact files without a healing call, retained five separate valid solids, and saved an inspectable FCStd document containing five named objects.

The calculated assembly mobility is exactly `2 DOF`: `0.014 m` total vertical carrier travel and contact-roller rotation about `+y`. Exact B-rep checks at `-0.007 m`, `0 m`, and `+0.007 m` found `0 m3` overlap and at least `0.008 m` clearance for every forbidden pair. The frozen force and torque graphs each have exactly one continuous path. Reference force, moment, and drive-energy residuals are all `0.0`, inside the respective `1e-5`, `1e-5`, and `1e-4` gates. All eight falsification controls produced their preregistered measurable consequence.

The software work item is complete, but the candidate is deliberately **not design-admitted**. Its verdict is `not_admitted_synthetic_evidence` and `design_use_allowed=false`. The structural witness uses synthetic material/process evidence and covers only Work 082's exact bracket and `500 N` tangential load family; it does not validate this candidate's `[320, 180, 1250] N` ground-force case or the other four parts.

## Files changed

- `config/candidates/ground_interaction_candidate_001.json`
- `src/formula_ultimate/subsystems/__init__.py`
- `src/formula_ultimate/subsystems/ground_interaction.py`
- `scripts/candidates/build_ground_interaction_candidate_001.py`
- `scripts/candidates/inspect_ground_interaction_freecad.py`
- `tests/test_ground_interaction_candidate_001.py`
- `docs/contracts/GROUND_INTERACTION_CANDIDATE_001.md` and Thai companion
- this result and its Thai companion
- the Work 083 plan and Thai companion, whose statuses changed to `Completed`

Generated CAD, FCStd, manifests, evaluations, and replay evidence under `artifacts/work083/` are ignored and were not committed.

## Decisions and measured evidence

- The mechanism is one inspectable candidate rather than a topology built into the general evaluator. Its five separate solids are `structural_mount`, `guide_frame`, `carrier`, `axle`, and `contact_roller`.
- The mount reuses exact Work 081/082 STEP hash `b06e3141f7a1fcad8017537d3680a787164d3190d4503417d3f6c1c98ed1ba89`; changed source bytes fail before generation.
- The assembly STEP hash is `57dc477bbec58da05a0908d1b9b8de04c57a482f710c2362980fed8c51ccb135`. The canonical geometry-manifest identity is `0ea7151e3610aa8652d0fd0352216bf3e667d84e34fc70e1720d00b26d517066`.
- The exact five-part synthetic mass total is `0.533616275507311 kg`; this is calculated from geometry and declared synthetic densities, not measured physical mass.
- Reference ground force magnitude is `1302.8046668629952 N`, positive normal force is `1250 N`, and reference capacity utilization is `0.6514023334314976`.
- Drive bookkeeping is `840 J` input, `772.8000000000001 J` delivered, and `67.19999999999993 J` loss. The separate braking case opposes rotation with `-30 Nm` and routes `600 J` to rejection; no recovery credit is invented.
- Disconnected mount and contact-loss controls cause `dnf`; undersized capacity produces utilization `2.6056093337259902` and `dnf`. Blocked translation, seized rotation, and broken torque path cause explicit degraded states with zero realized travel, power, or delivered torque as applicable.
- Runs `run_b` and `run_c` reproduced result identity `a061d0b2de7b01eb31233cd3ed1ab9945eb5dbc015ca478c26fb9b77fbfaded3`. Their result JSON file SHA-256 is identically `afc157a46b0837fb1c0d762f5e72225edc26929cfa1c8897bc7f99cabdc9eaa4`; replay identity is `acde7d11a1d32df69ace91dc9e6b7add31e46c9d7cfe4e8d4ac4d2dd3e2805b9`.
- The two canonical FreeCAD reports are byte-identical with report identity `de4b4c8f632b102f5dfeb8ba5a899b8a7773c4ccc852af046b49873f32e91afd`. Raw FCStd hashes differ (`cc8477...` versus `2f4a0e...`) because the FCStd ZIP container carries volatile metadata; therefore FCStd raw bytes are not claimed deterministic. Exact source STEP hashes plus the canonical FreeCAD report are the replay evidence.

## Evidence review

Supporting evidence: five independently inspectable solids, exact STEP identities, a five-object FCStd, calculated two-DOF mobility, three-position B-rep clearance, continuous force/torque paths, closed quasi-static ledgers, eight causal controls, and exact canonical replay.

Contradicting evidence: Work 082's structural case is only `500 N` tangential at the bracket hole, whereas this candidate declares a larger three-axis ground force. Raw FCStd byte identity also does not replay. These facts prevent structural/design admission and are retained rather than hidden.

Alternative explanations: the apparent mechanism feasibility may follow from generous clearances and simplified quasi-static bookkeeping; CadQuery and FreeCAD share OCCT technology; and zero residuals follow from algebraically paired reactions, not experimental measurement.

Missing evidence: design-eligible material/process records, structural analyses for the guide/carrier/axle/roller and the full candidate load vector, nonlinear contact, bearing/friction data, tyre or surface interaction, dynamic response, fatigue/buckling, thermal behaviour, manufacturing tolerances, physical tests, safety evidence, and integration with Works 084-086.

Confidence is high for exact software identities, separate CAD solids, declared mobility arithmetic, static clearance at the three frozen positions, bookkeeping, and fault propagation under this fixture. Confidence is low for any real-world capacity, durability, controllability, or production claim.

## Exact validation commands and results

```powershell
& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\candidates\build_ground_interaction_candidate_001.py `
  --config config\candidates\ground_interaction_candidate_001.json `
  --output-root artifacts\work083\run_b `
  --structural-result artifacts\work082\run_e\result.json `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe"
# exit 0; 5 parts; 5 assembly solids; 2 DOF; minimum clearance 0.008 m;
# maximum overlap 0.0 m3; all residuals 0.0;
# verdict=not_admitted_synthetic_evidence

& .\.tools\cadquery-mcp\Scripts\python.exe `
  scripts\candidates\build_ground_interaction_candidate_001.py `
  --config config\candidates\ground_interaction_candidate_001.json `
  --output-root artifacts\work083\run_c `
  --structural-result artifacts\work082\run_e\result.json `
  --freecad-python "C:\Program Files\FreeCAD 1.1\bin\python.exe" `
  --replay-reference artifacts\work083\run_b\result.json
# exit 0; replay_exact=true;
# result_sha256=a061d0b2de7b01eb31233cd3ed1ab9945eb5dbc015ca478c26fb9b77fbfaded3

python -m unittest `
  tests.test_ground_interaction_candidate_001 `
  tests.test_repository_contract -v
# exit 0; Ran 18 tests; OK

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -q
# exit 0; Ran 546 tests in 432.451s; OK (skipped=3)
```

An initial attempt to launch the inspection script by passing it directly to `FreeCADCmd.exe` returned exit `0` without executing the script or creating outputs. The runner now invokes FreeCAD's bundled `python.exe`, imports the same FreeCAD/Part APIs, and requires both the JSON report and FCStd files; missing outputs fail even when the subprocess exit code is zero.

## Limitations and follow-up

Work 083 does not satisfy the roadmap's real-part or design-evidence entry gate. A new work item must obtain design-eligible material/process/measurement evidence and run structural/contact cases that match this exact candidate and load vectors before admission can be reconsidered. Work 084 may consume the declared torque/contact interface only as a synthetic integration fixture, not as a validated hardware interface.
