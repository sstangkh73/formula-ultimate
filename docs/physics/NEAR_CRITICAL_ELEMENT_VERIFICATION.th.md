# การตรวจ Near-Critical Mesh และ Element

ไฟล์ต้นฉบับภาษาอังกฤษ: `NEAR_CRITICAL_ELEMENT_VERIFICATION.md`

## ข้ออ้างและผลลัพธ์

Work 041 ทำ solver-backed precritical verification experiment สำหรับ imperfect cantilever column จาก Work 037-039 สำเร็จ Execution gate ผ่าน แต่ **สมมติฐาน convergence โดยรวมถูกปฏิเสธ** Mesh C3D4 สองระดับละเอียดสุดสอดคล้องกันภายในเกณฑ์ `5%` ทุกโหลด แต่ refined C3D4 กับ C3D10 ต่างกัน `9.213%` ที่โหลดสูงสุด หลักฐานนี้จึงยังไม่อนุญาตข้ออ้างด้าน post-buckling capacity หรือโครงสร้างรถทั้งคัน

นี่คือ numerical-element verification สำหรับ synthetic elastic fixture ไม่ใช่ material validation, component certification, fracture evidence, fatigue evidence หรือ safety factor

## Physics fixture

ชิ้นทดสอบควบคุมเป็นเสาหน้าตัดสี่เหลี่ยม fixed-free โดย `L=0.2 m`, `b=h=0.01 m`, `E=70 GPa`, `nu=0.3` และ synthetic density `2700 kg/m^3` ใส่ transverse eigenmode imperfection ขนาด `e0=0.1 mm` ทุก mesh รับ absolute compression load เดียวกันคือ `1857.580`, `2600.612` และ `3157.886 N`

Analytical check คือ

```text
I = b h^3 / 12
Pcr = pi^2 E I / (K L)^2, K = 2
amplification = 1 / (1 - P/Pcr)
```

Euler load เชิงวิเคราะห์คือ `3598.293 N` ความสัมพันธ์ eigenmode secant ใช้เฉพาะ precritical region และไม่ใช่ post-buckling constitutive model

## นิยาม Element และ Pilot ที่ Freeze

Implementation อ่าน Gmsh MSH2 linear/quadratic tetrahedra และ boundary triangles โดย Gmsh ระบุ type `4` เป็น tetrahedron สี่ node, type `11` เป็น second-order tetrahedron สิบ node, type `2` เป็น triangle สาม node และ type `9` เป็น second-order triangle หก node CalculiX ระบุ C3D10 เป็น quadratic tetrahedron สิบ nodeที่มีสี่ integration points Converter ใช้ Gmsh-to-CalculiX final edge-node swap ที่ตรวจแล้วและ consistent quadratic face load

ก่อนเห็น solver result ของ C3D10 มีการทำ mesh-only pilot แล้ว freeze C3D10 ที่ `1.4 mm`: C3D4 `0.65 mm` มี `65,835` nodes และ C3D10 `1.4 mm` มี `57,426` nodes ค่าต่างแบบใช้ C3D4 เป็นตัวหารใน pilot คือ `12.773%`; symmetric comparison ใน admitted runner คือ `13.644%` ทั้งคู่ต่ำกว่า compute-comparability limit `25%` ที่ประกาศไว้ Node count ที่เทียบได้ไม่ได้แปลว่า truncation error เท่ากัน

## การออกแบบการทดลอง

- ตัวแปรอิสระ: element family/order, characteristic mesh size และ absolute compression load
- ตัวแปรตาม: eigenvalue critical load, nonlinear amplification, stress, reaction, solver status, mesh size, wall time และ artifact hash
- ตัวแปรควบคุม: geometry, material parameter, support, eigenmode imperfection, load distribution, absolute load, Gmsh/CalculiX route และ parsing rule
- สมมติฐานที่ต้องการพิสูจน์: mesh C3D4 สองระดับละเอียดสุดและ refined C3D4/C3D10 ต่างกันไม่เกิน `5%` ทุกโหลด
- การพยายามหักล้าง: เก็บโหลดสูงสุด, reject ผล missing/non-finite, ไม่แทน absolute load ด้วย per-mesh load fraction และบันทึก changed mode/failed solve

## ผลการทดลอง

| Mesh | Nodes | Tetrahedra | Eigenvalue `Pcr` (N) | Amplification ที่ 1857.580 N | ที่ 2600.612 N | ที่ 3157.886 N |
|---|---:|---:|---:|---:|---:|---:|
| C3D4, 1.0 mm | 20,514 | 95,711 | 3715.160 | 1.9971 | 3.3269 | 6.6413 |
| C3D4, 0.8 mm | 36,927 | 182,285 | 3675.360 | 2.0201 | 3.4160 | 7.0795 |
| C3D4, 0.65 mm | 65,835 | 337,805 | 3649.524 | 2.0343 | 3.4744 | 7.3923 |
| C3D10, 1.4 mm | 57,426 | 35,460 | 3599.539 | 2.0641 | 3.5986 | 8.1062 |

Amplification change ของ C3D4 `0.8 -> 0.65 mm` คือ `0.702%`, `1.694%` และ `4.323%` ซึ่งผ่าน gate `5%` ทั้งหมด ความต่าง refined C3D4 เทียบ C3D10 คือ `1.455%`, `3.512%` และ `9.213%` โดยเคสโหลดสูงไม่ผ่าน gate `5%` Maximum secant error คือ `0.539%`, maximum analytical eigenvalue error คือ `3.248%` และ admitted reaction residual ทั้งหมดเป็นศูนย์ที่ความละเอียดของ parser

## การประเมินหลักฐาน

หลักฐานสนับสนุน:

- admitted mesh ทั้งหมด solve ได้ผล finite เก็บ hash และคง global transverse-bending mode family เดิม
- C3D4 refinement ผ่าน last-two-mesh gate ที่ประกาศแล้ว
- C3D10 ทำนาย analytical eigenvalue คลาดเคลื่อนเพียง `0.035%` และ nonlinear case ทั้งหมดยังใกล้ secant reference
- node budget ของ C3D4/C3D10 ผ่าน frozen comparability gate

หลักฐานขัดแย้ง:

- element-family amplification ต่าง `9.213%` ที่ `3157.886 N` จึงต้อง reject สมมติฐาน convergence โดยรวม
- disagreement เพิ่มเมื่อเข้าใกล้ critical load ซึ่งเป็นบริเวณที่ข้ออ้างเป้าหมายไวที่สุด

คำอธิบายทางเลือกประกอบด้วย interpolation error, imperfection transfer, surface-load discretization ที่ต่างกัน และข้อจำกัดของ node count ในฐานะ equal-accuracy measure หลักฐานที่ยังขาดคือ asymptotic C3D10 refinement series, solver หรือ element formulation ที่ตรวจแล้วชุดที่สอง, strain-energy parsing ที่ตรวจอิสระแล้ว, process peak memory ที่วัดจริง และ post-critical continuation

มีความมั่นใจสูงว่า solver path และ gate ที่ประกาศไว้ reject element-family agreement สำหรับ fixture นี้ แต่ความมั่นใจต่ำสำหรับ post-buckling inference เพราะยังไม่ได้ทดสอบบริเวณนั้นและ Gate A ยังเปิดอยู่ Work 042 ด้าน plasticity ทำต่อเป็น evidence stream อิสระได้ แต่ post-buckling promotion ยังถูก block จนกว่าจะมี remedial mesh/element study ใหม่

## การรันซ้ำ

```powershell
.\scripts\run_work041.ps1
py -3.14 -m unittest tests.test_element_verification tests.test_eigenvalue_buckling_acceptance tests.test_nonlinear_imperfect_column -v
```

Machine-readable evidence อยู่ที่ `artifacts/work041/experiment_summary.json` และตั้งใจ ignore จาก Git ต้องทำ clean-tree replay หลัง implementation commit เพื่อให้ summary บันทึก commit นั้นตรง ๆ และ `worktree_dirty_during_run=false`
