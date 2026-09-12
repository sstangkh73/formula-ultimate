# ผล Work 122: Controller, Sensor และฮาร์ดแวร์รองรับ

แหล่งภาษาอังกฤษ: `2026-09-12_122_control-hardware-realization-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

Work 122 ทำ signal path แบบ sampled sensor-controller-actuator synthetic พร้อม hardware ที่นับ `1.19 kg` Work 119 จำกัด authority ที่ `200 N*m` ต่ำกว่าหลักฐาน `200.6375 N*m` และ Work 120 จำกัด charged supply ที่ `100000 J` ต่ำกว่า initial energy `18.432 MJ`

โหมด common และ adapted ใช้ tuning อย่างละสี่ evaluation เท่ากัน Best gain ของ adapted คือ `140` และให้ RMSE `0.44575617787699745` Control dropout, disconnection, supply หมด, saturation และ delay เพิ่มสังเกตได้; parameter ที่ noncausal คง trace SHA เดิมและไม่นับว่ามีประโยชน์ Result SHA-256 คือ `3dad312ce2cc6f044be5df73fbe6323d4cbc4ffb09d6b5dd07cde7dc4a630810`; replay ตรงกันทุกบิต ไม่พบบัคในการนำไปใช้

ไฟล์ที่เปลี่ยน: implementation/config/runner/test, contract `CONTROL_HARDWARE_REALIZATION_V1` สองภาษา และ plan/result สองภาษาชุดนี้ หลักฐานที่ไม่ติดตามใน Git อยู่ใต้ `artifacts/work122/run_a|run_b`

## การตรวจสอบและข้อจำกัด

```powershell
python -m unittest tests.test_control_hardware_realization -v
# exit 0; ผ่าน 7 tests
python -m py_compile src/formula_ultimate/subsystems/control_hardware_realization.py scripts/development/run_control_hardware_realization.py
# exit 0
python scripts/development/run_control_hardware_realization.py --config config/development/control_hardware_realization_v1.json --output-root artifacts/work122/run_a
# exit 0; ได้ result SHA-256 ข้างต้น
python scripts/development/run_control_hardware_realization.py --config config/development/control_hardware_realization_v1.json --output-root artifacts/work122/run_b --replay-reference artifacts/work122/run_a/result.json
# exit 0; replay ตรงกันทุกบิต
python -m unittest tests.test_realized_actuation_chain tests.test_onboard_energy_realization tests.test_control_hardware_realization tests.test_repository_contract -v
# exit 0; ผ่าน 25 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; ตรงกับ 10 ไฟล์ที่ประกาศสำหรับ Work 122
git diff --cached --check
# exit 0
```

Plant, noise, delay และ hardware เป็น synthetic งานนี้ไม่ยืนยัน stability จริง electronics, EMI/fault safety, certification หรือ physical validation จะรายงาน commit hash ที่ตรวจแล้วในสรุปสุดท้าย
