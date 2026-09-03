# ผล Work 085: เส้นทางเมชทั่วไปสำหรับแรงบิด แบริ่ง และ Housing

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_085_generalized-meshed-torsion-bearing-housing-result.md`

## สถานะและผลลัพธ์

สถานะ: Stopped

การแก้ exact geometry ด้วย Gmsh/CalculiX ทั้งเก้ารอบ converge และ force, moment, energy residual ทุกค่าผ่าน แต่งานหยุดที่ mesh-convergence gate ราย metric ที่ preregister ไว้: maximum displacement ของ `converter_housing_mount` เปลี่ยน `0.13187908211258156` (`13.1879%`) ระหว่าง mesh `6 mm` กับ `4.5 mm` เกินขีดจำกัด `0.12` (`12%`) ที่ตรึงไว้ ไม่มีการผ่อน gate และไม่มี passing result ถูกสร้าง

Runner และ contract ยังเป็นโครงสร้าง remediation แบบ fail-closed ที่ใช้ต่อได้ แต่งานนี้ยังไม่ปิด blocker ของ Work 084 และไม่อนุญาต Gate B หรือ integration

## ไฟล์ที่เปลี่ยน

- `config/structural/generalized_meshed_torsion_bearing_housing_v1.json`
- `src/formula_ultimate/structural/generalized_coupling.py`
- `scripts/structural/run_generalized_structural_coupling.py`
- `tests/test_generalized_structural_coupling.py`
- `docs/contracts/GENERALIZED_MESHED_STRUCTURAL_COUPLING_V1.md` และไฟล์คู่ภาษาไทย
- result นี้และไฟล์คู่ภาษาไทย
- แผน Work 085 และไฟล์คู่ภาษาไทย ซึ่งเปลี่ยนเป็น `Stopped`

หลักฐาน solver ที่สร้างใต้ `artifacts/work085/` ถูก ignore และไม่ได้ commit

## หลักฐาน exact

- `output_shaft_combined` การเปลี่ยนสอง mesh สุดท้าย: displacement `3.9998%`, compliance `5.1700%`, p90 stress `1.6225%`; fine p90 stress `144476407.786 Pa`
- `support_block_bearing`: displacement `4.2929%`, compliance `2.5150%`, p90 stress `8.8751%`; fine p90 stress `1675373.113 Pa`
- `converter_housing_mount`: displacement `13.1879%` (ไม่ผ่าน), compliance `11.1479%`, p90 stress `8.3687%`; fine p90 stress `305585.035 Pa`
- residual สูงสุดจากเก้ารอบ: force `6.980456828420865e-7`, moment `1.4117028561584432e-6`, energy `4.489527613110193e-8`
- SHA-256 ของ solver evidence: `71244cf626bc593f953dc5c37329541eb55462340a6c28885601b4d733f2c247`

Root ที่หยุดก่อนหน้าสองชุดเปิดเผยปัญหา input serialization ของ CalculiX ค่า free-field ที่ยาว เช่น `-2.2621670056434022E-06` ถูกปฏิเสธทั้งที่ finite ตอนนี้ runner เขียน scientific notation ความยาวคงที่และลบเพียง arithmetic noise ต่ำกว่า `1e-12 N`; จากนั้น solve ทั้งเก้ารอบเสร็จ การแก้นี้เปลี่ยน serialization input ไม่ได้เปลี่ยนผลหรือ gate

## คำสั่ง validation

```powershell
python scripts\structural\run_generalized_structural_coupling.py `
  --config config\structural\generalized_meshed_torsion_bearing_housing_v1.json `
  --output-root artifacts\work085\run_g `
  --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" `
  --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"
# exit 1 หลัง solve ครบเก้ารอบ; fail-closed ที่ last-two mesh convergence

python -m unittest tests.test_generalized_structural_coupling tests.test_repository_contract -v
# exit 0; Ran 18 tests; OK

python -m compileall -q src scripts tests
# exit 0
```

## การทบทวนหลักฐานและงานถัดไป

หลักฐานสนับสนุน: upstream identity exact, solve converge เก้ารอบ, region ไม่ว่างและไม่ทับกัน, residual ปิด และสองกรณีผ่านทุก mesh metric หลักฐานที่ขัดแย้ง: displacement ของ housing หนึ่ง metric เกิน gate คำอธิบายทางเลือก: รู/fin ที่ซับซ้อนของ housing ต้องใช้ช่วง asymptotic ที่ละเอียดกว่า `8/6/4.5 mm`; แนวโน้มปัจจุบันพิสูจน์ไม่ได้หากไม่มีการทดลองใหม่ที่ตรึงไว้ หลักฐานที่ขาด: housing mesh ที่ละเอียดกว่าและ exact replay ของผลที่ผ่าน

งานหมายเลขถัดไปต้องตรึงลำดับ housing ที่ละเอียดขึ้นโดยไม่เปลี่ยน gate `12%` ใช้หลักฐาน shaft/support ที่ผ่านแล้วผ่าน exact identity และรัน/replay ก่อน integration
