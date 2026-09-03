# Geometry-to-Structural Physics Coupling V1

ไฟล์ต้นฉบับภาษาอังกฤษ: `GEOMETRY_STRUCTURAL_COUPLING_V1.md`

## ขอบเขตและขอบเขตหลักฐาน

Work 082 ผูก exact identity ของ `bracket_001.step` และ cylindrical-interface signature จาก Work 081 เข้ากับ tetrahedral mesh ของ Gmsh, deck ของ CalculiX, field โครงสร้างที่ parse, residual gate, refinement evidence และการส่ง connection state ชุดอ้างอิงใช้ record อะลูมิเนียมคล้ายจริงแบบ synthetic จาก Work 079 จึงยังเป็น `synthetic_verification` และ `design_use_allowed=false`

การผ่าน V1 พิสูจน์เฉพาะว่า software path จาก geometry-to-solver ที่มีขอบเขตเป็น deterministic และ causal ภายใต้ fixture ที่ประกาศ ไม่ใช่ real-part capacity, physical validation, อายุ fracture/fatigue, crashworthiness, safety หรือ production approval

## ชุดอ้างอิงที่ freeze

- STEP SHA-256: `b06e3141f7a1fcad8017537d3680a787164d3190d4503417d3f6c1c98ed1ba89`
- Work 081 FreeCAD report: `34ad809df13ba746352107e952e67a6d187795c96e1cb1096a6efc9a7ba28132`
- loaded surface signature: `04e1d97edb2595c219cc0132fdfb43b74132d3ca9b7cf3656d445706550e332f`
- material record: `72a1b5527e4aede10c6de73523c54835f11458f80100c6383d2a304d4d912097` (`synthetic`)
- โหลด: แรง tangential `500 N` แบบ consistent บนผิว through-hole ที่วัด;
- support: ผิวปลายที่วัด `x=0.06 m`;
- mesh: first-order tetrahedra `6 mm`, `4 mm` และ `3 mm`

เส้นทาง Gmsh import exact STEP แทนการสร้างมิติที่พิมพ์ใหม่ boundary triangle ถูกเลือกด้วย geometry deck ของ CalculiX กระจาย resultant ที่ประกาศตามพื้นที่ triangle และบันทึก displacement, reaction, stress/strain, internal energy และ field output

## หลักฐานตัวเลขที่ยอมรับ

| Mesh | Nodes | Tetrahedra | Max displacement (m) | Compliance (m/N) | p90 von Mises (Pa) |
|---|---:|---:|---:|---:|---:|
| coarse 6 mm | 930 | 2,924 | `1.526042230277076e-5` | `2.831564572874119e-8` | `3.708533574964357e6` |
| medium 4 mm | 2,297 | 8,542 | `1.57548489513747e-5` | `2.8876628978500013e-8` | `3.8627178311174945e6` |
| fine 3 mm | 4,382 | 17,463 | `1.5955631992710995e-5` | `2.919834633813767e-8` | `3.926391799777586e6` |

การเปลี่ยน medium-to-fine ประมาณ `1.27%` displacement, `1.11%` compliance และ `1.65%` p90 stress ต่ำกว่า gate `5%` ที่ freeze ทั้งหมด fine force, moment และ energy relative residual คือ `4.4238208804794904e-8`, `2.249840148494702e-8` และ `3.1124177238745204e-8` ตามลำดับ metric p90 หลีกเลี่ยงการถือ point singularity ใกล้ constraint อุดมคติเป็น capacity metric ที่ยอมรับ

## การส่ง failure และ replay

reference ยังอยู่ในโดเมน elastic แบบ synthetic connection critical ที่ severed หรือเกิน ultimate-domain เปลี่ยน `bracket_structural_mount` เป็น `failed`, เขียน transmitted force เป็นศูนย์ และตั้ง subsystem state เป็น `dnf` การเกิน yield-domain เห็นได้เป็น degraded; fracture/fatigue evidence ที่ไม่รองรับไม่เคยได้รับ neutral capacity

ไฟล์ FRD ของ CalculiX มี runtime clock V1 เก็บ raw file แต่ canonicalize เฉพาะค่า `1UTIME` เดียวก่อน hash; ถ้าเวลาไม่มีหรือซ้ำจะ fail Mesh, deck, DAT, parsed metrics, adjudication, connection result และ canonical FRD hash replay ตรงกัน exact

## คำสั่งรัน

```powershell
python scripts\structural\run_geometry_structural_coupling.py `
  --config config\structural\geometry_structural_coupling_v1.json `
  --geometry-root artifacts\work081 `
  --output-root artifacts\work082\run_a `
  --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" `
  --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"
python -m unittest tests.test_geometry_structural_coupling -v
```

## ข้อจำกัด

support และ distributed cylindrical load เป็น bonded boundary แบบอุดมคติ โมเดลเป็น linear elastic C3D4 และไม่แทน contact, preload, friction, large deformation, plastic redistribution, crack growth, fatigue, local bearing damage หรือ manufacturing residual stress Work 083 ใช้ได้เฉพาะ software-coupling evidence; claim การออกแบบ ground-interaction จริงยังถูกบล็อกด้วย material/process ที่มีแหล่งอ้างอิงและหลักฐาน fidelity สูงกว่า
