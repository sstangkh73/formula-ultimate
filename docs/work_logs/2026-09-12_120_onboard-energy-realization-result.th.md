# ผล Work 120: การทำระบบพลังงานบนรถให้เกิดจริงอย่างละเอียด

แหล่งภาษาอังกฤษ: `2026-09-12_120_onboard-energy-realization-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

Work 120 ทำ route stored-electric/DC synthetic หนึ่งเส้นทางให้มี active storage, enclosure, insulation, connector, mount และ converter มวลครบชุดจาก geometry/จำนวนคือ `58.1820224 kg`; nominal active energy คือ `28.8 MJ`, usable capacity `23.04 MJ` และ initial energy ที่ลงทะเบียน `18.432 MJ`

กรณี nominal `8000 W` ส่ง `4.8 MJ` ใน `600 s`, มี modeled loss `257950.13850415577 J`, ถึง `304.93957447302887 K` และปิดบัญชีด้วย residual `-7.8580342233181e-10 J` คง temperature จาก Work 115, material claim ที่ blocked จาก Work 116 และ actuation output ที่ใช้ได้จาก Work 119 `11465 W` Control empty, rate-limited, thermal-limited, disconnected, omitted-containment, hidden-replenishment และ boundary ผ่าน

Result SHA-256 คือ `607140da3cdbb4346fdcbccce030b0e767d54872cc21bccbe966be8f1def3979`; replay ตรงกันทุกบิต ไม่พบบัคในการนำไปใช้ ไฟล์ที่เปลี่ยน: implementation/config/runner/test, contract `ONBOARD_ENERGY_REALIZATION_V1` สองภาษา และ plan/result สองภาษาชุดนี้ หลักฐานที่ไม่ติดตามใน Git อยู่ใต้ `artifacts/work120/run_a|run_b`

## การตรวจสอบและข้อจำกัด

```powershell
python -m unittest tests.test_onboard_energy_realization -v
# exit 0; ผ่าน 6 tests
python -m py_compile src/formula_ultimate/subsystems/onboard_energy_realization.py scripts/development/run_onboard_energy_realization.py
# exit 0
python scripts/development/run_onboard_energy_realization.py --config config/development/onboard_energy_realization_v1.json --output-root artifacts/work120/run_a
# exit 0; ได้ result SHA-256 ข้างต้น
python scripts/development/run_onboard_energy_realization.py --config config/development/onboard_energy_realization_v1.json --output-root artifacts/work120/run_b --replay-reference artifacts/work120/run_a/result.json
# exit 0; replay ตรงกันทุกบิต
python -m unittest tests.test_coupled_thermal_solid tests.test_material_failure_scope tests.test_realized_actuation_chain tests.test_onboard_energy_realization tests.test_repository_contract -v
# exit 0; ผ่าน 29 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; ตรงกับ 10 ไฟล์ที่ประกาศสำหรับ Work 120
git diff --cached --check
# exit 0
```

Property ด้าน storage/conversion/thermal ทั้งหมดเป็น synthetic ส่วน chemistry safety, capacity/rate/life ที่วัดจริง, alternative route, aging/fault และ physical validation ยัง unresolved งานนี้ไม่ใช่ใบอนุญาตสร้างหรือจ่ายพลังงาน จะรายงาน commit hash ที่ตรวจแล้วในสรุปสุดท้าย
