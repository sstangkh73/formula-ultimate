# Work 113: Detailed fastening and contact proof

Thai companion: `work113-detailed_connection_contact.th.md`

Status: Planned

Original Work 106 package: 112

Dependencies: Work 111, Work 112

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Build a physically realized connection at fastening scale; compare a threaded reference with a freely generated joining alternative.

Inputs: vector solid solver, physical interfaces and a frozen connection task; actual engaged geometry for the selected strategy.

## 2. Proposed files

- `src/formula_ultimate/structural/detailed_connection_contact.py`
- `config/development/detailed_connection_contact_v1.json`
- `scripts/development/run_detailed_connection_contact.py`
- `tests/test_detailed_connection_contact.py`

## 3. Implementation sequence

1. Freeze terminal loads, allowed motion, envelope, temperature assumptions and joining requirements.
2. Create mating geometry, clearances and seating; resolve thread roots/helix when threaded.
3. Implement contact/preload initialization, reaction recovery and separation/slip observations.
4. Derive a reduced joint model over a bounded load/preload range and compare detailed response.

## 4. Experiment

- IV: Joining geometry, engagement, preload, friction and off-axis load.
- DV: Stiffness, slip/opening, stress quantities, transmitted force/moment and reduction error.
- Controls: Same connection task and material assumptions; verified threaded reference without mandating threaded answers.

## 5. Tests and falsification

Remove/sever the joint, reverse load, vary clearance and reduce engagement. Test contact inequality/friction limits and local refinement; no fictitious stabilizing support.

## 6. Registration and acceptance

Freeze contact law, friction uncertainty, preload range, local mesh levels and accepted reduction error.

Both the reference verification and causal load-transfer tests pass within scope; unsupported loosening/fatigue remains unresolved. A failed alternative is a valid negative result.

## 7. Deliverables and handoff

Detailed joint CAD, sections, contact fields, preload state, convergence and reduced-model applicability manifest.

Feeds moving assemblies Work 114 and thermo-mechanical tests Work 115.

## 8. Risks and non-goals

Nonlinear contact can require a dedicated sub-work. Split solver verification from discovery if needed. No universal nut standard, fatigue-life or safety certification.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_detailed_connection_contact tests.test_repository_contract -v
python scripts/development/run_detailed_connection_contact.py --config config/development/detailed_connection_contact_v1.json --output-root artifacts/work113/run_a
python scripts/development/run_detailed_connection_contact.py --config config/development/detailed_connection_contact_v1.json --output-root artifacts/work113/run_b --replay-reference artifacts/work113/run_a/result.json
```
