# ผล Work 126: การปิดรายละเอียดยานพาหนะ

แหล่งภาษาอังกฤษ: `2026-09-12_126_detailed-vehicle-closure-result.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

Work 126 สร้าง G3 registry เชิงกำหนดที่มี component region ซึ่งมี owner ไม่ซ้ำ 12 รายการ ครอบคลุม external function และ hardware role ที่ลงทะเบียนทั้งหมด mass ที่คำนวณใหม่คือ `60.0 kg`, center คือ `[0.0, 0.0, 0.5] m`, diagonal inertia คือ `[0.9, 179.65, 179.65] kg m^2` และ occupied volume คือ `0.324 m^3`; declared residual ทั้งหมดอยู่ภายใน `1e-9` กราฟ energy, signal, heat และ load เชื่อมต่อ assembly แบบ static ไม่มี box interference และ swept-motion sample 5 จุดที่ลงทะเบียนไม่มี collision

Controls ปฏิเสธการเอา fastener/support/seal/signal hardware ออก, region ownership ซ้ำ, geometry นอก envelope, interference, open signal path และ stale envelope registry, exploded-view registry และ section-view registry ที่สร้างมี hash ตรึงไว้ Result SHA-256 คือ `ce5f08c8a572b1ef5adbf88db7e7200616c8c1c9c431ba6d032236d8917e3171`; exact replay ผ่าน หลักฐานจำเป็นยังไม่คลี่คลาย จึงมีสถานะ `detailed_exploratory` และ promotion เป็น false

ไฟล์ที่เปลี่ยน: implementation, configuration, runner, tests, สัญญาสองภาษา `DETAILED_VEHICLE_CLOSURE_V1` และ plan/result สองภาษานี้ หลักฐานที่ ignore อยู่ใต้ `artifacts/work126/run_a|run_b`

## รายงานบั๊ก

- อาการ: unit test แรกค้างระหว่างตรวจ connected path
- สาเหตุราก: pre-BFS loop เก่าวาง `queue.popleft()` ไว้เฉพาะแขนของ conditional expression ที่ไม่ถูกเลือก ทำให้ queue ไม่เดินหน้าสำหรับ adjacency แบบ list
- วิธีแก้: ลบลูปเก่าและคง explicit BFS ชุดเดียวที่ไม่ขึ้นกับทิศทาง โดย dequeue ทุกครั้งและ enqueue neighbor ที่ยังไม่เคยพบ
- ทดสอบซ้ำ: Work 126 ผ่านทั้ง 6 tests, evidence run สองรอบจบด้วย SHA-256 เดียวกัน และ affected regression ผ่านทั้ง 63 tests

## การตรวจสอบและข้อจำกัด

```powershell
python -m unittest tests.test_detailed_vehicle_closure -v
# รอบแรกค้าง; หลังแก้ exit 0; ผ่าน 6 tests
python -m py_compile src/formula_ultimate/assembly/detailed_vehicle_closure.py scripts/development/run_detailed_vehicle_closure.py tests/test_detailed_vehicle_closure.py
# exit 0
python scripts/development/run_detailed_vehicle_closure.py --config config/development/detailed_vehicle_closure_v1.json --output-root artifacts/work126/run_a
# exit 0; detailed_exploratory; result SHA-256 ตามข้างต้น
python scripts/development/run_detailed_vehicle_closure.py --config config/development/detailed_vehicle_closure_v1.json --output-root artifacts/work126/run_b --replay-reference artifacts/work126/run_a/result.json
# exit 0; exact replay
python -m unittest tests.test_ground_interaction_tasks tests.test_realized_actuation_chain tests.test_onboard_energy_realization tests.test_geometry_flow_heat_exchange tests.test_control_hardware_realization tests.test_coupled_vehicle_transient tests.test_multiscale_discovery_search tests.test_detailed_part_comparison tests.test_detailed_vehicle_closure tests.test_repository_contract -v
# exit 0; ผ่าน 63 tests
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; มีไฟล์ Work 126 ที่ประกาศไว้ 10 ไฟล์พอดี
git diff --cached --check
# exit 0
```

G3 registry ใช้ axis-aligned box bounds และ graph connectivity ไม่ใช่ native whole/individual CAD และยืนยัน detailed surfaces, tolerance-stack manufacturability, measured material survival, real collision behavior หรือ physical validation ไม่ได้ Work 127 ใช้ exact identity นี้สำหรับ fair optimized controls ได้ แต่ต้องรักษาขอบเขต non-promotion
