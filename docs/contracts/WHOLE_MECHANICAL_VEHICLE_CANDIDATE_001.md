# Whole Mechanical Vehicle Candidate 001 Admission Contract

Thai companion: `WHOLE_MECHANICAL_VEHICLE_CANDIDATE_001.th.md`

This contract distinguishes a successful admission audit from an admitted candidate. An intact evidence bundle may produce `audit_status=passed` and `candidate_verdict=not_ready`. That outcome is a valid, completed audit and is not a vehicle-readiness claim.

The audit identity-locks Work 083, 084, 086, and 087 evidence; verifies seventeen individual STEP files, the assembly STEP, and FCStd; emits the required assembly, interface, material, mass-property, interference, structural, energy, failure, replay, and Level-0 decision records; and evaluates all eleven preregistered cases.

Any source mutation, missing artifact, blocker suppression, synthetic-evidence relabelling, case omission, or attempt to run Level 0 while blocked is an audit error. Intact but adverse evidence returns `not_ready` and `level0_simulation.status=not_run_pre_admission_blocked` with exit code `0`, because the decision process succeeded even though the candidate did not qualify.

The audit never repairs geometry, supplies missing physical evidence, or converts Level-0/component evidence into physical validation.
