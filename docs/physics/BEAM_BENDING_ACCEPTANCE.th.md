# การยอมรับ Beam Bending

ไฟล์ต้นฉบับภาษาอังกฤษ: `BEAM_BENDING_ACCEPTANCE.md`

สถานะ: ผ่านสำหรับ Work 035

## ขอบเขตของข้ออ้าง

Work 035 ตรวจสอบ local linear-elastic cantilever route หนึ่งเส้นทาง:

```text
declared 3D beam -> Gmsh C3D4 mesh -> CalculiX static solve
-> full stress/reaction parsing -> analytical/equilibrium/convergence gates
```

ผลนี้แสดงการส่ง transverse load ผ่าน 3D solid ไปเป็น deflection, axial bending
stress, support force และ support moment แต่ไม่ validate yield, plastic reserve,
buckling, fracture, fatigue, joint หรือรถทั้งคัน

## Fixture และ analytical domain

Synthetic fixture ใช้ `L = 0.12 m`, `b = 0.012 m`, `h = 0.012 m`,
`E = 70 GPa`, `nu = 0.3`, density `2700 kg/m^3` และ end resultant `5 N` ในทิศ
negative `z` โดยยึด face `x = 0` และกระจายแรงบน finite face `x = L` ตาม
triangle tributary area Slenderness เท่ากับ `L/h = 10` ซึ่งเป็นค่าต่ำสุดที่
fixture contract นี้รับ

เมื่อ `I = b*h^3/12` reference คือ:

```text
I                  = 1.728e-9 m^4
tip displacement   = P*L^3/(3*E*I) = 2.38095238095238e-5 m
root moment        = P*L             = 0.6 N*m
root outer stress  = P*L*(h/2)/I     = 2.08333333333333e6 Pa
external work      = P*delta/2       = 5.95238095238095e-5 J
Sxx(x,z)           = P*(L-x)*(z-h/2)/I
```

Stress comparison ใช้ tetrahedron-centroid `Sxx` ระหว่าง `x = 0.024 m` ถึง
`x = 0.096 m` โดย exclude clamp/load-introduction region ก่อน evaluate Error
เป็น volume-weighted signed normalized RMS และ signed correlation ป้องกันผล
absolute-value ซ่อนทิศ bending ที่กลับด้าน

## ผลที่รับ

| Mesh | Size (m) | Nodes | C3D4 | Tip (m) | Tip error | Stress RMS error | Signed correlation |
|---|---:|---:|---:|---:|---:|---:|---:|
| coarse | 0.0014 | 6,944 | 31,022 | 2.2812166e-5 | 4.1889% | 14.2772% | 0.989799 |
| medium | 0.0012 | 10,343 | 48,003 | 2.3062422e-5 | 3.1378% | 12.1645% | 0.992602 |
| fine | 0.0010 | 16,767 | 81,764 | 2.3281446e-5 | 2.2179% | 10.1221% | 0.994880 |

Fine-mesh force closure เท่ากับ `4.59e-12` แบบ relative และ moment closure
เท่ากับ `2.46e-8` ระหว่าง mesh สองระดับละเอียดสุด displacement/external-work
change เท่ากับ `0.9497%` และ stress-error change เท่ากับ `2.0425` percentage
points ทุกค่าต่ำกว่า gate ที่ประกาศ

## Failed attempt ที่เก็บเป็นหลักฐาน

รอบแรก fail ก่อน solve เพราะ CalculiX อนุญาต node-set ไม่เกิน 16 entries ต่อ
บรรทัด แต่ fixed face มี 18 nodes ตอนนี้ adapter wrap node set แบบ deterministic
และมี regression test บังคับ limit สำหรับทั้ง tension/bending deck

Beam เดิมลึก `6 mm` กับ coarse mesh `3 mm` fail displacement/stress gate เพราะ
first-order tetrahedron stiff เกินจริงใน bending Fixture ลึก `12 mm` กับ mesh
`2 mm` ผ่าน global deflection แต่ fail declared stress RMS gate ที่ `19.77%`
mesh `1.5 mm` ได้ `15.14%` ซึ่งยังเกิน gate `15%` ที่ไม่เปลี่ยน Accepted sequence
จึงเริ่มที่ `1.4 mm`; ไม่ได้ผ่อน tolerance เพื่อรับ failed mesh

## การรันซ้ำและดูผล

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work035.ps1
```

Machine-readable evidence อยู่ที่ `artifacts/work035/experiment_summary.json`
แต่ละ mesh directory มี `beam.geo`, `beam.msh`, `beam.inp`, `beam.dat` และ
`beam.frd` เปิด fine `.frd` ใน FEM workbench ของ FreeCAD แล้วใช้ Fit All เพื่อดู
displacement/stress field การแสดงภาพมีไว้ตรวจประกอบ ส่วน JSON gate และ hashed
artifact คือ admitted evidence

## ข้อจำกัดและ gate ถัดไป

Euler-Bernoulli comparison จำกัดเฉพาะ regular slender beam และ exclude end
region C3D4 centroid stress converge ช้ากว่า global displacement มีการตรวจ
external work แต่ยังไม่ parse solver-reported internal energy อย่างอิสระ และยัง
ไม่มี physical material/second-solver data

ผลนี้อนุญาตให้เริ่ม torsion specimen ใน work item แยก แต่ยังไม่อนุญาต structural
fitness สำหรับ arbitrary vehicle geometry หรือข้ออ้าง nonlinear failure
