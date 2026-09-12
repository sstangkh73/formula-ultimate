# ผล Work 118: ปฏิสัมพันธ์พื้น การหยุด และการควบคุมทิศทาง

แหล่งภาษาอังกฤษ: `2026-09-12_118_ground-interaction-tasks-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

Work 118 สร้าง ground-contact port ที่ไม่ผูกกับสถาปัตยกรรม และ reference ของ Coulomb บนพื้น rigid/dry แบบ synthetic ที่มีขอบเขต โดยตรึงหลักฐาน Work 114 และ Work 116 ที่ระบุแน่นอน คงโหลด Work 114 `19196.837823792008 N` และรักษา material claim `blocked_no_measured_process-qualified_material`

Fixture การหยุด `300 kg`, `20 m/s`, normal load `3000 N` ใช้ coefficient `0.8` และหยุดใน `2.5 s` เป็นระยะ `25.00000000000007 m` ตรงกับ analytic reference ของแรงคงที่ที่ time step `0.1`, `0.05` และ `0.025 s` Energy residual และ refinement gate สองระดับสุดท้ายผ่าน ตำแหน่ง contact เปลี่ยน yaw moment จาก `0` เป็น `960 N*m`; force-circle saturation และ control friction ศูนย์ lift-off, reverse motion, disconnection, ไม่มี interaction และพื้นผิวที่ไม่รองรับทำงานเชิงเหตุตามที่ลงทะเบียน

Ground resultant สูงสุดที่รับเข้าคือ `960 N` ที่ `contact_alpha` ค่านี้เป็น part-load handoff ไม่ใช่ claim ว่า material รอด Result SHA-256 คือ `e843d60deda1d892c38331e3f51b6f27479954660acbcfafdf6394956f9d0a85`; replay ตรงกันทุกบิต ไม่พบบัคในการนำไปใช้ระหว่าง run ที่รับเข้า

ไฟล์ที่เปลี่ยน: implementation/config/runner/test, contract `GROUND_INTERACTION_TASKS_V1` สองภาษา และ plan/result สองภาษาชุดนี้ history/result ที่ไม่ติดตามใน Git อยู่ใต้ `artifacts/work118/run_a|run_b`

## การตรวจสอบและข้อจำกัด

```powershell
python -m unittest tests.test_ground_interaction_tasks -v
# exit 0; ผ่าน 7 tests
python -m py_compile src/formula_ultimate/simulation/ground_interaction_tasks.py scripts/development/run_ground_interaction_tasks.py
# exit 0
python scripts/development/run_ground_interaction_tasks.py --config config/development/ground_interaction_tasks_v1.json --output-root artifacts/work118/run_a
# exit 0; ได้ result SHA-256 ข้างต้น
python scripts/development/run_ground_interaction_tasks.py --config config/development/ground_interaction_tasks_v1.json --output-root artifacts/work118/run_b --replay-reference artifacts/work118/run_a/result.json
# exit 0; replay ตรงกันทุกบิต
```

```powershell
python -m unittest tests.test_moving_contact_assembly tests.test_material_failure_scope tests.test_ground_interaction_tasks tests.test_repository_contract -v
# exit 0; ผ่าน 24 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; ตรงกับ 10 ไฟล์ที่ประกาศสำหรับ Work 118
git diff --cached --check
# exit 0
```

Coefficient, พื้นผิว normal load คงที่ และ rigid contact เป็น synthetic ส่วน tire, soft-soil, non-tire adapter, load transfer, compliant contact, control stability, wear/thermal evolution และ physical validation ยัง unresolved จะรายงาน commit hash ที่ตรวจแล้วในสรุปสุดท้าย
