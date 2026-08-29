# การยอมรับ Solver ด้วยชิ้นทดสอบแรงดึง

ไฟล์ต้นฉบับภาษาอังกฤษ: `TENSION_SOLVER_ACCEPTANCE.md`

สถานะ: ผ่านสำหรับ Work 034

## ขอบเขตของข้ออ้าง

Work 034 ตรวจสอบ structural-analysis route ระดับ local หนึ่งเส้นทาง:

```text
declared 3D prism -> Gmsh C3D4 mesh -> CalculiX linear solve
-> strict result parser -> analytical and mesh-convergence gates
```

ผลนี้แสดงว่า applied axial load ไหลผ่าน meshed solid แล้วปรากฏเป็น
displacement, support reaction, axial stress และ external work แต่ยังไม่ validate
วัสดุจริง รถ candidate, nonlinear failure หรือ candidate route เต็มรูปแบบ
`3D -> STEP -> FreeCAD -> Level 0`

## ชิ้นทดสอบและสมการที่ประกาศ

Synthetic SI fixture เป็น rectangular prism ขนาด
`0.1 m x 0.01 m x 0.01 m` โดยใช้ `E = 70 GPa`, `nu = 0.3`, density
`2700 kg/m^3`, ยึด face ที่ `x = 0` ทุกแกน และใส่ resultant `1000 N` ที่ face
`x = 0.1 m` แรงถูกกระจายไป surface node ตาม triangle tributary area ไม่ใช่
แบ่งเท่ากันทุก node

Analytical reference คือ:

```text
A       = 1.0e-4 m^2
sigma   = F/A       = 1.0e7 Pa
epsilon = sigma/E   = 1.4285714285714287e-4
delta   = FL/(AE)   = 1.4285714285714287e-5 m
U       = F*delta/2 = 7.1428571428571435e-3 J
```

Material ที่กำหนดเป็น analytical fixture ไม่ใช่ aluminium certificate หรือ
ข้อมูล coupon ที่วัดจริง

## ผลลัพธ์

Mesh ที่ประกาศล่วงหน้าทั้งสามผ่านทั้งหมด Stress คือ mean `Sxx` ที่ weight ด้วย
volume ของ tetrahedron และ displacement คือ loaded-face displacement ที่ weight
ด้วย load โดยไม่ใช้ peak stress เพราะ fully fixed boundary ทำให้เกิด local end
effect

| Mesh | Size (m) | Nodes | C3D4 | Displacement (m) | Displacement error | Mean Sxx (Pa) | Force residual |
|---|---:|---:|---:|---:|---:|---:|---:|
| coarse | 0.0100 | 86 | 198 | 1.4162150e-5 | 0.86495% | 9,999,999.72 | 2.0e-4 N |
| medium | 0.0075 | 140 | 313 | 1.4182479165e-5 | 0.72265% | 9,999,999.89 | 0 N |
| fine | 0.0050 | 190 | 434 | 1.4198094754e-5 | 0.61334% | 9,999,999.88 | -3.0e-5 N |

ระหว่าง mesh สองระดับละเอียดสุด ค่า relative change ของ displacement/external
work เท่ากับ `0.11010%` และ mean axial stress เท่ากับ `1.70e-7%` ส่วน fine-mesh
force-closure residual เท่ากับ `3.0e-8` แบบ relative ทุก generated tetrahedral
volume ปิดกับค่าที่ประกาศ `1.0e-5 m^3` ภายใน gate

Replay evidence ถูกเขียนใต้ `artifacts/work034/` ที่ ignore โดย accepted summary
เก็บ command, exit code, wall time, repository identity, source/config/tool hash,
input/output hash ของแต่ละ mesh, solver output, metric และ structured
falsification review หากขั้นใด fail จะเขียน `experiment_failure.json` และคืน
nonzero exit code โดยไม่แทนผลด้วย analytical answer

## การรันซ้ำและดูผล

รัน installed Gmsh/CalculiX route ด้วย:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work034.ps1
```

Numerical record อยู่ที่ `artifacts/work034/experiment_summary.json` แต่ละ mesh
directory มี `tension.geo`, `tension.msh`, `tension.inp`, `tension.dat` และ
`tension.frd` เปิดผล `.frd` ใน FEM workbench ของ FreeCAD เพื่อดู solved
displacement/stress field หรือ import `.msh` เพื่อดู mesh ชิ้นงาน undeformed มี
ขนาดเพียง `100 mm x 10 mm x 10 mm`; หากมองไม่เห็นให้ใช้ Fit All การแสดง field
มีไว้ช่วยตรวจ แต่ JSON gate คือ machine-readable evidence ที่รับ

## Falsification review และข้อจำกัด

Supporting evidence คือ fresh output จาก connected mesh สามระดับ, load/reaction
ที่ปิด, analytical agreement และ last-two-mesh convergence ขณะเดียวกัน simple
uniform-tension prism คือ alternative explanation ที่สำคัญที่สุดสำหรับความตรง
กันสูง เพราะ fixture นี้ตั้งใจให้ง่ายและไม่ได้พิสูจน์ arbitrary geometry

หลักฐานที่ยังขาดและมีผลชี้ขาดคือ independent-solver agreement, measured coupon
data, bending, torsion, buckling, loaded interface, plasticity, yield, fracture,
fatigue และการตัด connection หลัง failure การทดลองนี้ตรวจ external work กับ
`F*delta/2` แต่ยังไม่ได้ parse solver-reported internal strain energy อย่างอิสระ
ดังนั้นผลนี้อนุญาตให้ไปชิ้นทดสอบถัดไป ไม่ได้อนุญาตให้อ้าง whole-vehicle safety
หรือ physical validation
