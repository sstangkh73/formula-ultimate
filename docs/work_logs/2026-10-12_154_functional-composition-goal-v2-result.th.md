# ผล Work 154: เป้าหมาย v2 ของ Auto-Loop การประกอบตามหน้าที่

ฉบับภาษาอังกฤษ: `2026-10-12_154_functional-composition-goal-v2-result.md`

วันที่: 2026-10-12

แผน: `2026-10-12_154_functional-composition-goal-v2-plan.th.md`

Status: Completed

## ผลลัพธ์

เตรียมเป้าหมาย v2 เสร็จแล้ว และกำหนดขนาดงานให้พอดีกับการรันแบบไม่มีคนเฝ้า 8 ชั่วโมง
ชุด acceptance v2 (28 เทสต์ในชั้น A, B และ C) ทำให้ผ่านได้จริง เพราะ package สังเคราะห์ผ่านครบทุกข้อ
และแยกแยะได้ เพราะข้อบกพร่องที่ตั้งใจใส่ทั้ง 8 แบบตกในเทสต์ที่ตั้งใจไว้ทุกแบบ
บน repository จริง verify ให้สถานะเริ่มต้นของลูปตรงตามที่ตั้งใจ
ยังไม่ได้รันลูป และยังไม่ได้ merge branch ของเป้าหมาย v1 เข้า `main`
เพราะ permission policy ของ session ปฏิเสธการ merge นั้น

## ไฟล์ที่แก้

- `auto-loop/acceptance/test_functional_composition.py` (ใหม่) นำการตรวจของ v1 มาใช้กับ package v2
  ผ่านการ subclass (`TierA0*`) แล้วเพิ่มภาษาเรขาคณิต (`TierA1`), motion พร้อม bearing และ sweep ตรวจการชน (`TierA2`),
  inertia (`TierA3`), การตรวจหลักฐานของหน้าที่ 9 ข้อ บวกรูทะลุของเกลียวและเสถียรภาพบนพื้น
  (`TierB1`–`TierB10`) และตัวประเมิน Level-0 พร้อมการทดสอบหักล้างด้วยความไวต่อมวล (`TierC1`)
- `auto-loop/GOAL.md`, `GOAL.th.md`: สัญญาเป้าหมาย v2, กรอบเวลา, ชั้นของงาน และข้อจำกัด
- `auto-loop/verify.ps1`: ล้าง fixture hook ทั้งสามตัว และ Gate 3 รันทั้งสองชุด
- `auto-loop/run-loop.ps1`: ค่าเริ่มต้นใหม่คือ branch `loop/functional-composition-v2`,
  150 turn ต่อรอบ, 20 รอบ และ 8 ชั่วโมง
- `auto-loop/README.md`, `README.th.md`: ชื่อ branch
- `auto-loop/progress.md`, `progress.th.md`: สถานะเริ่มต้นของ v2 และบทเรียนจาก v1

## หลักฐานการประมาณขนาดงาน

- การรัน v1: 5 รอบ ตั้งแต่ราว 22:30 ถึง 00:37 เวลาของไฟล์ `iter-*.log` คือ 22:56, 23:11, 23:30,
  00:00 และ 00:27
- ตอนนี้ verify หนึ่งครั้งใช้ราว 10.3 นาที (Gate 2 `533.585s`, Gate 3 `82.014s`)
  และรันอย่างน้อยรอบละ 2 ครั้ง จึงประมาณว่ารอบละราว 30 นาที หรือราว 16 รอบใน 8 ชั่วโมง
  เทียบกับงานที่ประมาณไว้ 15–20 ชิ้น

## Validation

1. รันชุด v2 กับ fixture สังเคราะห์ที่ถูกต้อง (`fixture_v2.py`) และ evaluator จำลอง
   ทั้งสองอยู่ใน scratchpad และไม่ได้ commit
   `python -m unittest discover -s auto-loop/acceptance -p "test_functional*.py"`
   ได้ `Ran 28 tests`, `OK` รอบแรกเจอปัญหา 2 ข้อ แก้แล้วทั้งคู่
   - cross member ของ fixture ไม่เชื่อมกัน เป็นบั๊กของ fixture
   - การตรวจ "ล้อมรอบแกน" ของเทสต์สุ่มดูแค่ vertex จึงปฏิเสธน็อตสี่เหลี่ยมที่ถูกต้อง
     ตอนนี้เปลี่ยนเป็นยิง ray 8 ทิศจากแกนออกไป ซึ่งตรงกับเจตนามากกว่าด้วย
2. ตารางข้อบกพร่อง แต่ละแบบตกในเทสต์ที่ตั้งใจไว้พอดี

   | แบบ | เทสต์ที่ตก |
   |---|---|
   | no_void | `test_vessel_holds_declared_volume` |
   | piston_blocked | `test_motions_sweep_without_collision` |
   | no_fins | `test_surfaces_are_extended` |
   | threaded_no_hole | `test_threaded_joints_pass_through_a_hole` |
   | unstable | `test_rotating_ground_contacts_carry_the_vehicle_stably` |
   | wrong_inertia | `test_vehicle_inertia_matches_meshes` |
   | no_bearing | `test_every_motion_has_a_bearing_or_guide` |
   | evaluator ไม่สนใจมวล | `test_level0_race_uses_the_generated_vehicle` |

3. ตรวจฟังก์ชันวัดค่าเทียบกับคำตอบเชิงวิเคราะห์
   - กล่อง 2 x 1 x 0.5 m ความหนาแน่น 3: มวล `3.0`, จุดศูนย์กลางมวล `[1, 0.5, 0.25]`,
     แนวทแยงของ inertia `[0.3125, 1.0625, 1.25]` ตรงกับค่าเชิงวิเคราะห์ทุกตัว และพจน์นอกแนวทแยงเป็น `0.0`
   - วงแหวนสี่เหลี่ยม: genus `1` ปิดสนิท ปริมาตร `3.0` (คาดไว้ 3)
   - กล่องกลวง: ช่องว่าง `1.0` (คาดไว้ 1)
   - frustum ถูกจัดเป็นไม่ใช่ปริซึม ส่วนกล่องและจาน 64 เหลี่ยมถูกจัดเป็นปริซึม
4. รัน `pwsh -NoProfile -File auto-loop/verify.ps1` โดยตั้ง hook ทั้งสามตัวเป็นคำสั่งปลอม
   ได้ exit 3 Gate 1 ผ่าน Gate 2: `Ran 1094 tests in 533.585s`, `OK (skipped=11)`
   Gate 3: `Ran 41 tests`, `FAILED (failures=28)` เทสต์ v1 ทั้ง 13 ผ่าน และ v2 ทั้ง 28 ตกด้วย
   `missing: ...generate_functional_vehicle.py` ซึ่งพิสูจน์ว่า hook ถูกล้างแล้ว
5. PowerShell parser รายงาน 0 error ใน `run-loop.ps1` และ `verify.ps1`
6. gate ก่อน commit: `python -m unittest tests.test_repository_contract`,
   `git diff --cached --check` และ stage แบบระบุไฟล์

## ข้อจำกัด

- หลักฐานของหน้าที่ในสัญญาเป็นอคติของภาษาการออกแบบ ไปทางกลไกที่คุ้นตา
  (ที่เก็บพลังงานแบบมีช่องว่างภายใน, จุดสัมผัสพื้นที่หมุนได้)
- ตรวจเกลียวแค่ว่าเป็นรูทะลุ drag area ถูกจำกัดขอบเขตไว้เท่านั้น ไม่ได้คำนวณออกมาจริง
  และการตรวจ mesh เป็นแบบสุ่มจุด
- การประมาณ 8 ชั่วโมงอิงการรันแค่ 5 รอบครั้งเดียว
- `main` ยังชี้ที่ `56412d6` Work 149–154 อยู่บน `loop/hierarchical-composition`
  จนกว่าเจ้าของโครงการจะ fast-forward `main`

## งานต่อไป

- fast-forward `main` ไปที่ `loop/hierarchical-composition` แล้วเริ่มลูป v2 จาก `main`
- หลังรันเสร็จ ตรวจทั้งเรื่องการโกงและความลึกของงาน แบบที่ทำหลัง v1
