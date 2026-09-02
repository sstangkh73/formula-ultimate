# Mechanical Assembly and Joint Kernel V1

Thai companion: `MECHANICAL_ASSEMBLY_JOINT_KERNEL_V1.th.md`

## Purpose and evidence boundary

Work 080 converts explicitly placed, geometry-identified components into a deterministic mechanical-assembly constraint system. It validates datum/interface frames, calculates constraint rank and realized rigid-body degrees of freedom (DOFs), checks joint limits and declared clearances, and rejects conservative continuous motion-envelope collisions. The admitted fixture references exact canonical STEP SHA-256 identities produced by Work 078.

Passing V1 is evidence for a consistent declaration, calculated rigid-body DOFs, and clearance of the declared conservative proxy envelopes. It is not physical validation, exact B-rep collision certification, multibody dynamics, bearing life, joint strength, wear, friction, fatigue, or safety approval.

## Joint mathematics

Each non-ground component contributes six generalized coordinates. Every joint adds independent linearized constraint rows in its declared world-frame axis:

| Joint | Constraint rows | Realized relative DOFs |
|---|---:|---:|
| fixed | 6 | 0 |
| revolute | 5 | 1 rotation about the joint axis |
| prismatic | 5 | 1 translation along the joint axis |
| spherical | 3 | 3 rotations about the joint centre |

The kernel performs deterministic Gaussian elimination with a declared absolute rank tolerance. `realized_dof_count = 6 * component_count - calculated_rank`; the expected rank and DOFs are assertions checked after calculation, never inputs substituted for it. Redundant constraint rows reject the assembly as overconstrained. A component without a joint rejects as underconstrained.

## Frames, mates, and interfaces

Every component and interface frame contains an SI origin plus right-handed orthonormal axes. Unknown, non-finite, non-unit, non-orthogonal, and left-handed frames fail closed. Interface origins and joint axes must already agree within the most restrictive declared mate/interface tolerance. The kernel never snaps, aligns, heals, or repairs a declaration.

The V1 interface compatibility sets are bounded: fixed connections admit fixed mounts, bolted/welded interfaces, and shaft couplings; revolute connections admit revolute, bearing-seat, and shaft-coupling interfaces; prismatic and spherical connections require their corresponding interface classes. Missing, duplicate, reserved, self-connected, and incompatible references fail closed.

## Clearance and continuous collision controls

Joint minimum, home, and maximum values are ordered and finite; fixed-joint values must all be zero. Axial and radial clearances must not exceed their declared maxima. Preload and translational/rotational stiffness are observable declaration values, but V1 does not solve contact stress or deformation from them.

Collision proxies are component-local spheres. A prismatic sphere becomes an exact line-segment sweep of that sphere over its full declared travel. A revolute or spherical proxy becomes a conservative sphere about the joint centre large enough to contain all rotations; fixed proxies remain stationary. Pairwise finite-segment distance supplies the minimum gap and detects collisions over the continuous proxy envelopes, not at selected motion samples. This can produce conservative false positives and cannot certify exact B-rep clearance.

## Admitted reference and controls

`config/assembly/mechanical_assembly_joint_kernel_v1.json` contains four ground-connected components exercising fixed, revolute, prismatic, and spherical joints. The calculated system has 19 independent rows and 5 realized DOFs. Controls falsify acceptance through axis/origin mismatch, redundant constraints, incorrect declared or expected DOFs, excessive clearance, invalid limits, continuous-travel collision, missing/duplicate/incompatible interfaces, non-finite frames, and left-handed frames. Mapping-key permutation must preserve declaration and result identities; a geometry hash mutation must change them.

Run the admitted witness with:

```powershell
python scripts\assembly\run_joint_kernel_acceptance.py `
  --output artifacts\work080\acceptance.json
python -m unittest tests.test_joint_kernel -v
```

## V1 limitations and next dependency

The admitted fixture uses one ground connection per component. The rank formulation supports component-to-component constraints, but V1's swept-envelope placement has not validated moving-parent kinematic chains; those assemblies must not inherit the reference fixture's collision claim. Collision spheres are declared proxies rather than independently measured B-rep bounds. Work 081 must independently re-import the exact STEP bytes, measure geometry and mass properties, and recover declared interfaces by geometric signatures rather than persistent face numbers.
