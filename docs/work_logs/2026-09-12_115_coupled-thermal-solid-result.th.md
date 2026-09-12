# ผล Work 115: การตอบสนอง Coupled Thermal-Solid

ต้นฉบับภาษาอังกฤษ: `2026-09-12_115_coupled-thermal-solid-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

Work 115 พัฒนา transient coupling สองทางบน detailed joint regions สองส่วน ตรวจ Work 113 result identity, STEP hashes, volumes และ contact area ที่ derive จาก helix ใหม่ก่อน solve Heat เปลี่ยน temperatures, expansion, modulus และ preload; preload ที่เปลี่ยนส่ง contact conductance ที่เปลี่ยนกลับ Decoupled control ให้ความต่างที่สังเกตได้ จึงใช้แทน coupled run ไม่ได้

Result SHA-256 คือ `764f1c22774b3c3321cea384053ba079f8671b587fe1059d12b8910d51bcc5fa`; replay ตรงทุกบิต ที่ `0.005 s` male/female temperatures คือ `299.6262800251348/296.18422109463023 K`, preload `4027.010508986209 N` และ contact conductance `2.422791168670161 W/K` Coupled/decoupled return change คือ `0.008846767995635219` Reduced temperature-rise error คือ `0.026501053417395667`

ที่ `0.02/0.01/0.005 s` energy residuals คือ `4.405364961712621e-15`, `8.057554623519536e-14`, `1.0544454198679887e-13` Last-two changes ทุกค่าต่ำกว่า `1.45e-6` Insulated male จบที่ `314.1379777108881 K` เทียบ analytic `314.1379777108996 K`, absolute error `1.1482370609883219e-11 K` Zero-source equilibrium, free/constrained expansion, removed heat path, doubled area และ property-range rejection ผ่าน

ไฟล์ที่เปลี่ยน: implementation/config/runner/test ตามข้อเสนอ, contract `COUPLED_THERMAL_SOLID_V1` สองภาษา และ plan/result นี้สองภาษา Histories แบบ ignored อยู่ที่ `artifacts/work115/run_a|run_b`

## Validation และข้อจำกัด

```powershell
python -m unittest tests.test_coupled_thermal_solid -v
# exit 0; ผ่าน 6 tests
python -m py_compile src/formula_ultimate/physics/coupled_thermal_solid.py scripts/development/run_coupled_thermal_solid.py
# exit 0
python scripts/development/run_coupled_thermal_solid.py --config config/development/coupled_thermal_solid_v1.json --output-root artifacts/work115/run_a
# exit 0; result SHA-256 ตามข้างต้น
python scripts/development/run_coupled_thermal_solid.py --config config/development/coupled_thermal_solid_v1.json --output-root artifacts/work115/run_b --replay-reference artifacts/work115/run_a/result.json
# exit 0; exact replay
```

```powershell
python -m unittest tests.test_vector_solid_fields tests.test_detailed_connection_contact tests.test_coupled_thermal_solid tests.test_repository_contract -v
# exit 0; ผ่าน 23 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; ตรงกับไฟล์ Work 115 ที่ประกาศไว้ 10 ไฟล์
git diff --cached --check
# exit 0
```

Thermal properties และ conductances เป็น synthetic, regions เป็น lumped และไม่อ้าง spatial thermal stress, validated convection/radiation/fluid flow, fatigue, cooling adequacy หรือ physical validation รายงาน verified commit hash ใน final handoff
