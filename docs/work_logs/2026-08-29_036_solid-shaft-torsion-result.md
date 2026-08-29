# Work 036 Result: Solid-Shaft Torsion

Status: Completed

Thai companion: `2026-08-29_036_solid-shaft-torsion-result.th.md`

Implemented the versioned torsion fixture, consistent pure-torque surface load, least-squares twist gauge, reaction torque, signed shear-vector field gates, three-mesh convergence, `-T`, `2T`, doubled-modulus, and unrestrained negative-control cases. Added configuration, structural contracts, runner, launcher, tests, and bilingual physics evidence.

Accepted fine result: 8,967 nodes, 44,200 C3D4, twist `0.002293104622232224 rad` (3.023% error), shear RMS error 8.932%, correlation 0.996165, force closure `1.52e-13`, moment closure `7.02e-9`. All metamorphic residuals were below `1.1e-8`; the unrestrained run was rejected for unbounded rigid-body displacement.

Failed attempts were retained conceptually in the report: excessive coordinate serialization first caused CalculiX input rejection; coarse mesh sequences then failed unchanged twist/stress gates; CalculiX exit `0` on the singular negative control required displacement-based rejection.

Validation returned exit `0`: focused `16 tests`, live Work 036, Work 035/034 regressions, full `284 tests in 46.474s`, compileall, `git diff --check`, explicit staging, and `git diff --cached --check`. The commit hash is reported in the final handoff.

Limitations remain those in `SHAFT_TORSION_ACCEPTANCE.md`; no nonlinear failure capability is claimed.
