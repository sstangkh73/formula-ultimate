# การแก้ Gate A ด้าน Element และ Boundary

ไฟล์ต้นฉบับภาษาอังกฤษ: `GATE_A_ELEMENT_BOUNDARY_REMEDIATION.md`

## ขอบเขตการอ้างและผลตัดสิน

Work 051 จำกัด Gate A ให้เป็น numerical evaluation domain ที่ชัดเจน ไม่ได้ validate structural transferability โดยทั่วไป Domain ที่ admit ใช้เส้นทาง C3D10 precritical ที่ตรวจแล้ว และบังคับ exact support-topology signature พร้อม boundary-model identity ภายใน domain นี้ Work 046 เริ่มได้ในฐานะ bounded coupling-policy experiment

ผล reject ของ C3D4/C3D10 จาก Work 041 และ one-support transfer จาก Work 045 ยังคงเป็นหลักฐานขัดแย้ง ไม่มีการเฉลี่ย ลบ หรือเปลี่ยนชื่อให้เป็นผลผ่าน

## การแก้ด้าน element

มีการ replay geometry, synthetic elastic material, imperfection `0.1 mm`, absolute load, เส้นทาง Gmsh/CalculiX, surface traction และ parser เดิมจาก Work 041 Preregistered quadratic series คือ:

| Mesh | Nodes | Tetrahedra | Eigenvalue `Pcr` (N) | Analytical error |
|---|---:|---:|---:|---:|
| C3D10, `1.8 mm` | 29,770 | 17,661 | 3,599.795 | `0.0417%` |
| C3D10, `1.4 mm` | 57,426 | 35,460 | 3,599.539 | `0.0346%` |
| C3D10, `1.2 mm` | 89,833 | 57,137 | 3,599.457 | `0.0324%` |

Amplification change จาก `1.4 -> 1.2 mm` ที่โหลด `1857.580`, `2600.612` และ `3157.886 N` เท่ากับ `0.00267%`, `0.00640%` และ `0.01702%` Maximum secant-reference error ตลอด C3D10 series เท่ากับ `0.5391%` ทุกค่าอยู่ต่ำกว่า preregistered limit `5%`

ผลนี้รองรับ C3D10 convergence สำหรับ precritical fixture ที่ประกาศ แต่ไม่ได้ทำให้ C3D4 ใกล้ critical กลับมาผ่าน: retained cross-family hypothesis ของ Work 041 ยัง reject และ C3D4 ถูก exclude จาก near-critical promotion ในช่วงที่ cross-family difference เกิน `5%`

## การแก้ด้าน boundary

มีการรัน CAD, STEP, FreeCAD, fine mesh, load, material, solver และ parser เดิมจาก Work 045 สองครั้ง Reference support encoding คือ `support_upper, support_lower`; equivalent encoding เปลี่ยนเพียงลำดับ list ทั้งคู่ได้:

- topology signature `7f4444a78af66157f04441b38e4d4bc3225a892b29f90ebf9840279694fb6258`;
- STEP SHA-256 `6f20d310970723738abafb19fa212264f14a5147880144280c2dbe92502c4aee`;
- compliance change `0`;
- integrated reaction-resultant change `0`

การลบ `support_upper` ทำให้ canonical topology ต่างกัน จึงไม่ admit เป็น representation-only comparison Compliance change เท่ากับ `119.843%` ตาม symmetric metric ของ Work 051 Raw response เดียวกันให้ retained reference-denominator change `299.021%` ใน Work 045 ทั้งสองค่าอธิบาย response difference ขนาดใหญ่เดียวกันด้วย denominator ที่ประกาศต่างกัน และไม่มีค่าใดรองรับการ transfer ไป one-support topology

## Contract ที่ admit สำหรับ Work 046

Work 046 ใช้ได้เฉพาะ:

1. C3D10 precritical structural evidence ที่ผ่าน frozen mesh, mode, reaction และ secant gate
2. exact support-topology signature
3. exact boundary-model identity `bonded_cylindrical_surface_zero_displacement_v1`
4. typed yield/fracture/fatigue crossing event พร้อม limitation เดิม
5. failure coupling ในฐานะ deterministic state/energy policy ไม่ใช่ real fracture dynamics

การแทน element family, topology change, boundary-model change, contact model, preload, friction หรือ post-critical state ใด ๆ อยู่นอก domain และต้อง fail closed หรือเข้าสู่ study ที่ validate แยกต่างหาก

## การทบทวนเพื่อหักล้าง

หลักฐานสนับสนุนประกอบด้วย solver-backed C3D10 refinement, equivalent-encoding replay ที่เหมือนกัน, exact STEP identity และ negative control สำหรับ duplicate/undeclared support identity กับ non-C3D10 evidence

หลักฐานขัดแย้งยังคงเป็น high-load cross-family difference `9.213%` จาก Work 041 และ one-support response change จาก Work 045 คำอธิบายทางเลือกคือ C3D4 interpolation error ที่เพิ่มใกล้ critical load และ physical load-path change จากการลบ support หลักฐานที่ยังขาดคือ post-critical continuation, independent solver, joint contact/preload/friction, fastener flexibility, physical calibration และ real material record

ความมั่นใจสูงเฉพาะ narrow numerical identity contract และต่ำเมื่ออยู่นอก contract Level 0 และ solver fixture เหล่านี้ยังเป็น selection/verification gate ไม่ใช่ physical proof

## การทำซ้ำ

```powershell
.\scripts\run_work051.ps1
py -3.14 -m unittest tests.test_element_verification tests.test_loaded_interface tests.test_gate_a_remediation -q
py -3.14 -m unittest discover -s tests -q
```

Machine-readable evidence อยู่ใต้ `artifacts/work051/` และ Git จงใจ ignore ต้องทำ clean-tree replay หลัง commit
