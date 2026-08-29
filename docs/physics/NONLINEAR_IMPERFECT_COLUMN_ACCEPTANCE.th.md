# เกณฑ์ยอมรับเสาไม่สมบูรณ์แบบเชิงไม่เชิงเส้น

ไฟล์ต้นฉบับภาษาอังกฤษ: `NONLINEAR_IMPERFECT_COLUMN_ACCEPTANCE.md`

## คำถามและขอบเขตข้ออ้าง

Work 038 ถามว่าแรงอัดตามแกนส่งผ่าน initial geometric imperfection ไปเป็น lateral displacement ที่เพิ่มขึ้นจริงหรือไม่ งานนี้ตรวจ precritical, linear-elastic, geometrically nonlinear CalculiX route เท่านั้น ไม่ได้วัด post-buckling capacity, collapse, allowable load, yield, fracture หรือ fatigue

Solver deck ใช้ `*STEP, NLGEOM` เอกสาร CalculiX ระบุว่า `NLGEOM` บน `*STEP` เปิด geometrically nonlinear static formulation และแนะนำให้ตรวจ confirmation message ใน solver output: <https://www.feacluster.com/CalculiX/ccx_2.18/doc/ccx/node332.html>

## ชิ้นทดสอบและค่าอ้างอิง

ชิ้นทดสอบคือ solid cantilever column จาก Work 037: `L=0.2 m`, `b=h=0.01 m`, `E=70 GPa`, `nu=0.3`, C3D4 mesh size `1.25 mm`, ยึดที่ `x=0` และอัดด้วย tributary-area-weighted end-face load Work 037 วัด matching-mesh eigenvalue เป็น `Pcr=3776.375 N`; Euler reference ที่แยกไว้คือ `3598.293271 N`

Initial cross-section translation คือ

```text
z0(x) = e0 [1 - cos(pi x / (2L))]
```

ดังนั้น fixed face ไม่เลื่อนและ free-end offset เท่ากับ `e0` พอดี สำหรับ mode-shaped imperfect elastic column ที่ต่ำกว่า `Pcr` ใช้ค่าเทียบ

```text
A(P) = 1 / (1 - P/Pcr)
e(P) = e0 A(P)
```

ทดสอบสอง amplitude คือ `e0=0.1 mm` และ `0.2 mm` ที่ `P/Pcr={0.25,0.50,0.70,0.85}`

## ตัวแปรและ gate

- ตัวแปรอิสระ: `e0` และ `P/Pcr`
- ตัวแปรตาม: incremental/total lateral tip displacement, amplification, axial shortening, maximum computed von Mises stress, reaction closure, solver status และ evidence hash
- ตัวแปรควบคุม: geometry, elastic property, mesh, support, load distribution, imperfection function, solver และ parser
- ผ่านเมื่อ: nonlinear case ทุกตัว converge, reaction error `<=1e-5`, response เพิ่มอย่างเคร่งครัด, secant-reference error `<=15%` และ cross-amplitude normalized spread `<=10%`
- ไม่ผ่านเมื่อ: evidence หาย/ผิดรูป, ไม่มี NLGEOM confirmation, response ไม่ monotonic หรือเกิน gate ใด ๆ

Perfect-column control ต้องมี lateral drift ต่ำกว่า `2e-6 m` ซึ่งเป็น 2% ของ imperfection ต่ำสุด Threshold นี้ calibrate หลัง initial pilot พบ mesh-asymmetry drift แล้วจึง pin ก่อน reported replay ดังนั้น Work 038 เป็น solver acceptance evidence ไม่ใช่ independently preregistered confirmatory study

## ผล

| `P/Pcr` | Secant `A` | `A`, `e0=0.1 mm` | error | `A`, `e0=0.2 mm` | error |
|---:|---:|---:|---:|---:|---:|
| 0.25 | 1.3333 | 1.3327 | 0.044% | 1.3326 | 0.055% |
| 0.50 | 2.0000 | 1.9982 | 0.089% | 1.9978 | 0.109% |
| 0.70 | 3.3333 | 3.3292 | 0.123% | 3.3273 | 0.180% |
| 0.85 | 6.6667 | 6.6457 | 0.314% | 6.5724 | 1.414% |

ที่ `0.85 Pcr` total tip offset คือ `0.664571 mm` และ `1.314475 mm` Largest cross-amplitude spread คือ `1.110%`; largest reaction error คือ `2.648e-7` Perfect NLGEOM control drift `0.000426 mm` ต่ำกว่า gate `0.002 mm` Imperfect geometrically linear control ได้เพียง `A=1.8485` และพลาด secant response `72.27%` จึงหักล้างคำอธิบายว่า initial geometry อย่างเดียวเพียงพอโดยไม่ต้องมี geometric stiffness

## การตีความและข้อจำกัด

หลักฐานสนับสนุนคือ nonlinear response ที่เพิ่มตาม load สอดคล้องระหว่าง amplitude และใกล้ secant หลักฐานแย้งคือความคลาดเคลื่อนที่เพิ่มขึ้นเมื่อ imperfection ใหญ่และ load สูงสุด ซึ่งสอดคล้องกับการเริ่มออกจาก ideal small-deflection secant approximation Mesh asymmetry, C3D4 bending stiffness และ pinned numerical eigenvalue เป็นคำอธิบายทางเลือก ยังไม่มี nonlinear amplification mesh-convergence study แยก

ความเชื่อมั่นสูงว่า route นี้ส่ง axial load เป็น precritical P-delta displacement สำหรับ fixture นี้ ปานกลางสำหรับ quantitative transfer ไป solid column อื่น และไม่มีข้ออ้างสำหรับ post-buckling หรือ material failure งานถัดไปต้องมี imperfection-shape variation, nonlinear mesh convergence, arc-length หรือ continuation method อื่นที่ validate แล้ว และ material nonlinearity ก่อนอ้าง collapse หรือ DNF coupling
