# การยอมรับ Solid-Shaft Torsion

ไฟล์ต้นฉบับภาษาอังกฤษ: `SHAFT_TORSION_ACCEPTANCE.md`

สถานะ: ผ่านสำหรับ Work 036

Work 036 verify local linear Saint-Venant torsion ผ่าน `3D cylinder -> Gmsh C3D4 -> CalculiX -> strict evidence gates` แต่ไม่ validate yield, fracture, fatigue, joint, gear, bearing หรือ drivetrain

Synthetic fixture ใช้ `L=0.1 m`, `R=0.01 m`, `T=10 N*m`, `E=70 GPa`, `nu=0.3` โดย reference คือ `G=26.9230769231 GPa`, `J=1.5707963267949e-8 m^4`, `theta=0.00236458772593673 rad` และ `U=0.0118229386296837 J`

Tangential traction ถูก integrate แบบ consistent บน triangle ของ loaded face แล้ว scale เป็น pure wrench: resultant force ศูนย์และ torque ตรง Twist ใช้ area-weighted least-squares face rotation ส่วน interior `(Sxy,Sxz)` เทียบเป็น signed volume-weighted vector field

| Mesh | Nodes | C3D4 | Twist error | Shear RMS error | Correlation |
|---|---:|---:|---:|---:|---:|
| 1.9 mm | 4,810 | 22,264 | 4.662% | 11.427% | 0.993825 |
| 1.7 mm | 6,382 | 30,539 | 3.802% | 10.270% | 0.994976 |
| 1.5 mm | 8,967 | 44,200 | 3.023% | 8.932% | 0.996165 |

Fine force/moment closure เท่ากับ `1.52e-13` และ `7.02e-9` แบบ relative Last-two twist/work change เท่ากับ `0.810%`; shear-error change `1.338` percentage points

Live metamorphic check ผ่าน: `-T` กลับ twist/stress โดย energy ยังบวกเท่าเดิม; `2T` ทำ twist/stress สองเท่าและ work สี่เท่า; doubled modulus ทำ twist ครึ่งหนึ่งโดย stress คงเดิม CalculiX คืน exit `0` ให้ shaft ที่จงใจไม่ยึด แต่ displacement เกิน `1e8 m`; evidence gate จึง reject เป็น rigid-body singular behavior

Sequence `4 mm`, `2.5 mm`, `2.0 mm` แรก fail analytical/stress gate เดิม Accepted sequence จึง refine mesh แทนการผ่อน tolerance รันซ้ำด้วย `scripts\run_work036.ps1` และเปิด `artifacts/work036/fine_1p5mm/shaft.frd` ใน FreeCAD FEM

ข้อจำกัด: faceted circular geometry ยังปรากฏใน volume error, ยังไม่ parse internal solver strain energy อย่างอิสระ และไม่มี second solver/physical shaft data Milestone ฟิสิกส์อิสระถัดไปคือ material yield/elastoplastic acceptance หรือ buckling ตาม roadmap
