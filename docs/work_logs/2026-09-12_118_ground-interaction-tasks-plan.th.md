# แผน Work 118: ปฏิสัมพันธ์พื้น การหยุด และการควบคุมทิศทาง

แหล่งภาษาอังกฤษ: `2026-09-12_118_ground-interaction-tasks-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

สร้าง ground-contact port ที่ไม่ผูกกับสถาปัตยกรรม และ reference ของ friction บนเส้นทาง rigid แบบมีขอบเขต โดยตรึงกับหลักฐาน motion/contact จาก Work 114 และหลักฐานขอบเขตการใช้ material จาก Work 116 ประเมินแรงปฏิกิริยาขับเคลื่อน การหยุด และการตอบสนองทิศทาง yaw โดยไม่สมมติว่าต้องใช้ล้อ ชุดบังคับเลี้ยว หรือจำนวน contact ตายตัว

ใช้ sign convention แบบ SI ที่ชัดเจน ระเบียนพื้นผิว rigid/dry แบบ synthetic ที่ลงทะเบียนแล้ว Coulomb force-circle saturation, กฎ lift-off/disconnection, บัญชีพลังงานการหยุด และ time-step refinement ส่งค่า contact load และ moment สูงสุดกลับหลักฐาน part model พร้อมคงโดเมน tire, soft-soil และ non-tire ที่ไม่รองรับเป็น unresolved

## ตัวแปร control และไฟล์

- IV: ตำแหน่ง contact, normal load, friction coefficient, คำสั่งแรง longitudinal/lateral, ความเร็วเริ่มต้น คำสั่ง yaw และ time step
- DV: แรง contact ที่รับเข้า yaw moment/response, เวลา/ระยะหยุด พลังงานสูญเสีย energy residual, สถานะ saturation และ local load ที่ส่งกลับ
- Controls: เส้นทาง/พื้นผิว/พลังงานเริ่มต้นเดียวกัน; friction ศูนย์ lift-off, reverse motion, saturation, actuation ถูกตัด และไม่มี physical interaction
- Success: แรง reference เป็นไปตาม force circle และเครื่องหมาย; analytic reference ของการหยุดและพลังงานลู่เข้า; การเปลี่ยนตำแหน่งเปลี่ยน yaw moment; interaction ที่ห้ามไม่สร้างแรงพื้น; exact replay ผ่าน

ไฟล์ที่วางแผน: `src/formula_ultimate/simulation/ground_interaction_tasks.py`, `config/development/ground_interaction_tasks_v1.json`, `scripts/development/run_ground_interaction_tasks.py`, `tests/test_ground_interaction_tasks.py`, contract `docs/contracts/GROUND_INTERACTION_TASKS_V1*` สองภาษา, plan/result สองภาษาชุดนี้ และหลักฐานที่ไม่ติดตามใน Git `artifacts/work118/run_a|run_b`

## การตรวจสอบ

```powershell
python -m unittest tests.test_ground_interaction_tasks tests.test_repository_contract -v
python scripts/development/run_ground_interaction_tasks.py --config config/development/ground_interaction_tasks_v1.json --output-root artifacts/work118/run_a
python scripts/development/run_ground_interaction_tasks.py --config config/development/ground_interaction_tasks_v1.json --output-root artifacts/work118/run_b --replay-reference artifacts/work118/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน regression ที่ได้รับผลของ Work 114/116 และตรวจ staged/cached diff แบบระบุไฟล์ จะ commit ทันทีเมื่อทุก gate ผ่านเท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

กฎ Coulomb แบบ dry rigid เป็น causal reference ที่มีขอบเขต ไม่ใช่โมเดล tire, compliant terrain หรือ arbitrary locomotion สิ่งที่ไม่ทำ: กำหนดชนิด/จำนวน contact, อ้าง validated traction, soft soil, hydroplaning, wear/thermal evolution, complete vehicle control, physical validation, push หรือแก้ประวัติ
