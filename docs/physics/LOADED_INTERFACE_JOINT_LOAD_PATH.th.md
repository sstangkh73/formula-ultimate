# Loaded Interface และ Joint Load Path

ไฟล์ต้นฉบับภาษาอังกฤษ: `LOADED_INTERFACE_JOINT_LOAD_PATH.md`

## ผลลัพธ์และขอบเขตข้ออ้าง

Work 045 ทำ solver-backed load-path experiment ผ่าน loaded cylindrical interface หนึ่งตัวและ bonded support interfaces สองตัวเสร็จ CAD/STEP/FreeCAD/mesh/result identity, force closure, moment closure, internal/external energy และ last-two-mesh compliance gate ผ่าน แต่ **สมมติฐานรวมถูกปฏิเสธ** เพราะเปลี่ยนจาก rigid support holes สองรูเป็นหนึ่งรูทำให้ compliance เปลี่ยน `299.021%` สูงกว่า transferability gate `10%` มาก

ผลนี้พิสูจน์ load path เฉพาะ exact bonded-interface fixture นี้ ไม่ validate bolt, pin/contact, bearing failure, weld, adhesive, friction, preload, tolerance, nonlinear failure, arbitrary joint หรือ vehicle chassis

## Geometry และ Identity Chain

`loaded_interface_plate_v1` เป็น plate ขนาด `0.12 x 0.08 x 0.008 m` มี through holes radius `5 mm` สามรู:

- `load_port`: `(x,y)=(0.09,0) m` รับ distributed load `(+1000,0,0) N` บน cylindrical surface ทั้งหมด
- `support_upper`: `(0.03,+0.02) m`
- `support_lower`: `(0.03,-0.02) m`

CadQuery 2.8.0 สร้าง valid solid หนึ่งชิ้น FreeCAD 1.1.3 import STEP อย่างอิสระและ identify cylindrical face ทุกตัวด้วย ID, center, radius, axis และพื้นที่ `0.0002513274122872 m^2` จากนั้น Gmsh map geometric signature แต่ละตัวเป็น boundary triangles/nodes ที่ไม่เป็นศูนย์ บน fine mesh แต่ละ interface map เป็น `90` triangles และ `56` nodes

ช่วงแรก OCCT ใส่ wall-clock time ใน STEP `FILE_NAME` header ทำให้ raw hash เปลี่ยนแม้ geometry เหมือนกัน Exporter จึง canonicalize เฉพาะ header timestamp นั้น Independent probe สองรอบให้ STEP SHA-256 เดียวกัน `6f20d310970723738abafb19fa212264f14a5147880144280c2dbe92502c4aee` และ hash เดียวกันอยู่ครบใน CadQuery manifest, FreeCAD import และ mesh run ทั้งหมด

## ผล Solver

| Mesh | Nodes | C3D4 | Compliance (m/N) | Max von Mises (Pa) | Force residual | Moment residual | Energy residual |
|---|---:|---:|---:|---:|---:|---:|---:|
| 6 mm | 1,110 | 3,228 | `2.13581e-9` | `5.29453e6` | `1.35e-8` | `3.49e-9` | `4.61e-8` |
| 4 mm | 2,115 | 7,059 | `2.14778e-9` | `5.78391e6` | `3.28e-8` | `9.19e-10` | `3.28e-9` |
| 3 mm | 4,178 | 15,293 | `2.16273e-9` | `5.59884e6` | `4.14e-9` | `1.08e-9` | `2.28e-8` |

Last-two compliance change คือ `0.6959%` และ integrated reaction-resultant change คือ `2.70e-8` ผ่าน gate `5%` ทั้งคู่ Symmetry แบ่ง axial reaction เท่ากันระหว่าง support สองตัว Fine baseline external/internal energy คือ `0.0010813635116 J` และ `0.0010813634869 J`

เมื่อ active เฉพาะ `support_lower`, compliance เพิ่มจาก `2.16273e-9` เป็น `8.62973e-9 m/N` และ maximum von Mises เพิ่มจาก `5.60` เป็น `27.61 MPa` Sensitivity solve ยังปิด force, moment และ energy ดังนั้นนี่คือ boundary-condition effect จริงภายใน model ไม่ใช่ failed solve จึง reject transferability

Negative control หกแบบ fail closed: missing support, duplicated support selection, zero-area interface, duplicated load ID, broken outer ligament และ disconnected solid

## Falsification review

หลักฐานสนับสนุนมี canonical STEP หนึ่งไฟล์, independently matched interfaces, connected mesh สามระดับ, complete field coverage, consistent surface loading, equilibrium/energy closure, converged compliance, symmetric load share และ negative-control rejection ครบ หลักฐานขัดแย้งคือ support-policy sensitivity `299.021%` ซึ่ง reject preferred transferability hypothesis

Rigid bonded hole constraint เป็นคำอธิบายทางเลือกที่เป็นไปได้และอาจครอบงำ compliance เมื่อเทียบกับ real pin/contact behavior หลักฐานที่ขาดคือ contact pressure, clearance, friction, preload, support compliance, plastic bearing, bolt/weld/adhesive mechanics, manufacturing tolerance และ yield/fracture/fatigue coupling มีความมั่นใจสูงสำหรับ declared solver load path นี้และต่ำสำหรับการ transfer ไป joint อื่น

## การรันซ้ำ

```powershell
.\scripts\run_work045.ps1
py -3.14 -m unittest tests.test_loaded_interface -v
```

Machine-readable evidence อยู่ที่ ignored `artifacts/work045/experiment_summary.json`
