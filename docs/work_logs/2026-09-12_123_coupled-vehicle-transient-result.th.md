# ผล Work 123: ระบบรัน Candidate ทั้งคันแบบ Coupled Transient

แหล่งภาษาอังกฤษ: `2026-09-12_123_coupled-vehicle-transient-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

Work 123 เชื่อมหลักฐาน Work 117–122 ที่ระบุแน่นอนผ่าน schema ของ state owner และ signed exchange Run ละเอียดสุด `0.005 s` จบที่ `33.97591865087971 m`, `9.964358996108553 m/s`, stored energy `18416105.011570092 J` และ `299.6451530112513 K` Maximum step residual คือ `4.157563182616286e-12 J`; global residual คือ `-9.645725640439196e-8 J` Refinement สามระดับและ control sign, double-count, event, depletion, validity และ decoupling ผ่าน

Result SHA-256 คือ `66abf81b6f49179cb881e70d594e856b5042c4ef0f6fcc0fa813ef2acad2a14c`; replay ตรงกันทุกบิต สถานะยังเป็น `passed_exploratory_only` พร้อม `promotion_allowed: false` เพราะ complete geometry และโดเมน material/ground/aero/structural ที่ validate แล้วยัง unresolved

## บันทึกบัค

- อาการ: การตรวจก่อน run พบว่า runner derive drag coefficient จาก `unbounded_reference_drag_n` ของ Work 121 แต่ config ของ harness แทนค่า `drag_force_n` ที่รวม far-field correction แล้ว
- สาเหตุหลัก: field ข้างกันสองรายการใน Work 121 มีหน่วยเหมือนกันแต่ความหมายด้าน boundary domain ต่างกัน
- วิธีแก้: derive `work121_drag_coefficient_n_per_m_s2` จากค่า admitted finest `drag_force_n / 30^2`
- Retest: unit tests, run A, exact replay run B และ affected regression 51 tests ผ่านทั้งหมด ไม่พบบัคอื่น

ไฟล์ที่เปลี่ยน: implementation/config/runner/test, contract `COUPLED_VEHICLE_TRANSIENT_V1` สองภาษา และ plan/result สองภาษาชุดนี้ History/result ที่ไม่ติดตามใน Git อยู่ใต้ `artifacts/work123/run_a|run_b`

## การตรวจสอบและข้อจำกัด

```powershell
python -m unittest tests.test_coupled_vehicle_transient -v
# exit 0; ผ่าน 6 tests
python -m py_compile src/formula_ultimate/simulation/coupled_vehicle_transient.py scripts/development/run_coupled_vehicle_transient.py
# exit 0
python scripts/development/run_coupled_vehicle_transient.py --config config/development/coupled_vehicle_transient_v1.json --output-root artifacts/work123/run_a
# exit 0; ได้ result SHA-256 ข้างต้น
python scripts/development/run_coupled_vehicle_transient.py --config config/development/coupled_vehicle_transient_v1.json --output-root artifacts/work123/run_b --replay-reference artifacts/work123/run_a/result.json
# exit 0; replay ตรงกันทุกบิต
python -m unittest tests.test_architecture_part_feedback tests.test_ground_interaction_tasks tests.test_realized_actuation_chain tests.test_onboard_energy_realization tests.test_geometry_flow_heat_exchange tests.test_control_hardware_realization tests.test_coupled_vehicle_transient tests.test_repository_contract -v
# exit 0; ผ่าน 51 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; ตรงกับ 10 ไฟล์ที่ประกาศสำหรับ Work 123
git diff --cached --check
# exit 0
```

Trajectory สั้นแบบลดรูปนี้ไม่ยืนยันรถที่สมบูรณ์ race completion, readiness หรือ physical validation จะรายงาน commit hash ที่ตรวจแล้วในสรุปสุดท้าย
