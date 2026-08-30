# Gate A Element and Boundary Remediation

Thai companion: `GATE_A_ELEMENT_BOUNDARY_REMEDIATION.th.md`

## Claim and decision

Work 051 narrows Gate A to an explicit numerical evaluation domain. It does not globally validate structural transferability. The admitted domain uses the verified C3D10 precritical route and requires an exact support-topology signature plus boundary-model identity. Inside that domain, Work 046 may begin as a bounded coupling-policy experiment.

The rejected Work 041 C3D4/C3D10 comparison and the rejected Work 045 one-support transfer remain contradictory evidence. They were not averaged, deleted, or relabeled as passing results.

## Element remediation

The Work 041 geometry, synthetic elastic material, `0.1 mm` imperfection, absolute loads, Gmsh/CalculiX route, surface traction, and parsers were replayed. The preregistered quadratic series was:

| Mesh | Nodes | Tetrahedra | Eigenvalue `Pcr` (N) | Analytical error |
|---|---:|---:|---:|---:|
| C3D10, `1.8 mm` | 29,770 | 17,661 | 3,599.795 | `0.0417%` |
| C3D10, `1.4 mm` | 57,426 | 35,460 | 3,599.539 | `0.0346%` |
| C3D10, `1.2 mm` | 89,833 | 57,137 | 3,599.457 | `0.0324%` |

The `1.4 -> 1.2 mm` amplification changes at `1857.580`, `2600.612`, and `3157.886 N` were `0.00267%`, `0.00640%`, and `0.01702%`. The maximum secant-reference error across the C3D10 series was `0.5391%`. These are below the preregistered `5%` limits.

This supports C3D10 convergence for the declared precritical fixture. It does not rehabilitate C3D4 near the critical load: the retained Work 041 cross-family hypothesis remains rejected, and C3D4 is excluded from near-critical promotion where its cross-family difference exceeds `5%`.

## Boundary remediation

The exact Work 045 CAD, STEP, FreeCAD, fine mesh, load, material, solver, and parser route was run twice. The reference support encoding was `support_upper, support_lower`; the equivalent encoding reversed only that list order. Both produced:

- topology signature `7f4444a78af66157f04441b38e4d4bc3225a892b29f90ebf9840279694fb6258`;
- STEP SHA-256 `6f20d310970723738abafb19fa212264f14a5147880144280c2dbe92502c4aee`;
- compliance change `0`;
- integrated reaction-resultant change `0`.

Deleting `support_upper` produced a different canonical topology and was therefore not admitted as a representation-only comparison. Its compliance change is `119.843%` under the symmetric Work 051 metric. The same raw responses produced Work 045's retained `299.021%` reference-denominator change. Both values describe the same large response difference with different declared denominators; neither supports transfer to a one-support topology.

## Admitted contract for Work 046

Work 046 may consume only:

1. C3D10 precritical structural evidence that passes the frozen mesh, mode, reaction, and secant gates;
2. an exact support-topology signature;
3. the exact boundary-model identity `bonded_cylindrical_surface_zero_displacement_v1`;
4. typed yield/fracture/fatigue crossing events with their existing limitations;
5. failure coupling as a deterministic state/energy policy, not as real fracture dynamics.

Any element-family substitution, topology change, boundary-model change, contact model, preload, friction, or post-critical state is out of domain and must fail closed or enter a separately validated study.

## Falsification review

Supporting evidence includes solver-backed C3D10 refinement, identical equivalent-encoding replays, exact STEP identity, and negative controls for duplicate/undeclared support identities and non-C3D10 evidence.

Contradicting evidence remains the Work 041 `9.213%` high-load cross-family difference and the Work 045 one-support response change. Alternative explanations are growing C3D4 interpolation error near critical load and the physical load-path change caused by support deletion. Missing evidence includes post-critical continuation, an independent solver, joint contact/preload/friction, fastener flexibility, physical calibration, and real material records.

Confidence is high for the narrow numerical identity contract and low outside it. Level 0 and these solver fixtures remain selection/verification gates, not physical proof.

## Reproduction

```powershell
.\scripts\run_work051.ps1
py -3.14 -m unittest tests.test_element_verification tests.test_loaded_interface tests.test_gate_a_remediation -q
py -3.14 -m unittest discover -s tests -q
```

Machine-readable evidence is under `artifacts/work051/` and is intentionally ignored by Git. A clean-tree replay is required after commit.
