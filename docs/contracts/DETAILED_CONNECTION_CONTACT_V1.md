# Detailed Connection Contact V1

Thai companion: `DETAILED_CONNECTION_CONTACT_V1.th.md`

Status: Implemented by Work 113 for bounded Level-0 joint evidence.

## Scope and fixed task

This contract pins the Work 111 vector-field and Work 112 physical-interface commits/contracts. A threaded helix reference and a topology-distinct six-ramp alternative share a `0.03 m` diameter by `0.04 m` envelope, `293.15 K`, synthetic isotropic material, `800 N` axial tension, `500 N` shear, `1 N m` off-axis moment, preload `2000-6000 N`, friction `0.2-0.35` and clearance `0-5e-5 m`. The engaged state permits no relative motion.

Both strategies produce separate valid male/female STEP solids. The reference contains a rounded swept helix around an explicit root cylinder; it is not a standardized V-thread. The alternative contains six segmented radial engagement ramps. Root, contact, engagement and sleeve radii and length must remain ordered and inside the common envelope. Male/female interference must not exceed `1e-12 m3`.

## Contact formulation and gates

The detailed model discretizes the declared engagement surface into `12`, `24` and `48` patches. It solves nonnegative normal reactions that balance remaining compression and off-axis moment. Patch contact is unilateral. Tangential transfer is limited by Coulomb capacity `mu * sum(normal reaction)`; exceedance is reported as slip with explicit post-slip compliance. Removed/severed joints, all-open contact, invalid engagement and out-of-range inputs fail closed. No hidden stabilizing support exists.

Acceptance uses patch-average maximum pressure rather than a singular point stress. The last-two relative changes of normal stiffness, shear displacement and maximum patch pressure must each be at most `0.15`; force and moment residuals must be at most `1e-9`. The reduced stiffness is admitted only for the registered full-engagement stick cases and displacement error must not exceed `0.05`.

Clearance, engagement, preload/friction and load reversal must change the response causally. A failed alternative is retained as negative evidence. Exact replay requires the same result SHA-256. This is deterministic initialization and reduced-model evidence, not a general nonlinear contact solve, thread strength, loosening/fatigue prediction, manufacturing release, safety certification or physical validation.
