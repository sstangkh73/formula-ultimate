# แผน Work 075: Motion Ratio ของ Linkage ที่คำนวณจาก Geometry

สถานะ: กำลังดำเนินการ (In progress)

แปลจากไฟล์ภาษาอังกฤษ: `2026-09-02_075_geometry-linkage-motion-ratio-plan.md`

## วัตถุประสงค์และขอบเขต

แทนขอบเขตการกระจัดช่วงล่างแบบหนึ่งต่อหนึ่งโดยปริยายของ Work 073 ด้วย geometry ของ rocker/link แบบ small-angle ที่ชัดเจน คำนวณ motion ratio ของแต่ละ contact จาก pivot, rotation axis, wheel pickup, spring pickup, wheel direction และ spring axis แบบ 3D ที่ประกาศ แล้วแปลง stiffness, damping และ travel ของสปริงเป็นพิกัดล้อก่อน Work 073 แก้โหลดแนวดิ่ง

นี่เป็นหลักฐาน linkage แบบ geometry-causal ระดับ Level 0 บนจุดสังเคราะห์ที่ประกาศ ไม่ใช่ detailed CAD joint validation

## การออกแบบการทดลอง

- ตัวแปรอิสระ: พิกัด pivot/pickup, rotation axis, ทิศ spring/wheel, stiffness/damping และ travel ของสปริง
- ตัวแปรตาม: projected lever arm, motion ratio, stiffness/damping/travel ในพิกัดล้อ การตอบสนอง load/body/energy ของ Work 073 และ terminal failure
- ตัวควบคุม: unit ratio, spring arm สองเท่า, spatial mirror, projected wheel arm เป็นศูนย์, spring arm collinear, axis scaling, permutation และ geometry identity ที่เปลี่ยน
- สมมติฐานหลัก: `r = d_spring/d_wheel` จาก geometry ทำให้ `k_wheel = k_spring r^2`, `c_wheel = c_spring r^2`, wheel travel limit `s_limit/r`; geometry ที่เปลี่ยนทำให้การตอบสนองรถเปลี่ยน ขณะที่ unit ratio รักษา Work 073
- การหักล้าง: ใช้ ratio ที่ประกาศแทนการคำนวณ, ขาด virtual-work scaling, ซ่อน sign ambiguity ด้วย clip, ยอมรับ geometry เสื่อมสภาพ, energy drift หรือ geometry เปลี่ยนแต่ response identity ไม่เปลี่ยน

## ไฟล์ที่วางแผน

- `config/vehicle/geometry_linkage_motion_ratio_v1.json`
- `src/formula_ultimate/simulation/linkage_motion_ratio.py`
- simulation exports, runner, tests และเอกสารวิจัย/ผลสองภาษา
- หลักฐานที่ ignore ใต้ `artifacts/work075/`

## การตรวจสอบและเกณฑ์สำเร็จ

กรณี lever analytical และ geometry mirror ต้องปิดภายใน `1e-12`; degeneracy และ geometry non-finite ต้อง fail closed Unit ratio ต้องรักษา Work 073 result hash Geometry non-unit ต้องเปลี่ยน stiffness/travel และ coupled response โดย equation/energy residual อยู่ในขอบเขต Replay, geometry mutation identity, focused/full tests, compilation, bilingual contract, scoped commit และ post-commit replay ต้องผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

แบบจำลอง rigid-rocker small-angle ไม่รวม arc ที่ระยะมาก, compliance/backlash/friction ของ joint, pushrod geometry, anti-dive/squat, collision, bearing stress, fastener load และ CAD assembly constraints จุดที่ประกาศยังไม่ได้ดึงจาก STEP/FreeCAD solids
