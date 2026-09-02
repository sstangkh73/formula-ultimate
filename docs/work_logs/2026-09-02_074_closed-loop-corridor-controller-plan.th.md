# แผน Work 074: ตัวควบคุม Corridor แบบ Closed Loop

สถานะ: เสร็จสมบูรณ์ (Completed)

แปลจากไฟล์ภาษาอังกฤษ: `2026-09-02_074_closed-loop-corridor-controller-plan.md`

## วัตถุประสงค์และขอบเขต

เพิ่ม feedback controller แบบ deterministic ที่แปลงสถานะ planar ปัจจุบันของ Work 073 และ centreline ของ `CircuitCorridor` ที่ประกาศไว้เป็นคำสั่งเลี้ยวแบบมีขอบเขต รัน controller ทีละ step ผ่าน plant แนวดิ่ง/ยาง/ระบบส่งกำลังของ Work 073 ที่ไม่เปลี่ยน เพื่อให้ tracking error ส่งผลต่อแรงยาง body mode พลังงาน และ terminal state จริง ไม่ใช่เพียงวาดเส้นทาง

Work 074 เป็นการทดลองควบคุมสังเคราะห์ระยะสั้นระดับ Level 0 ไม่ได้อ้าง autonomous racing, optimal control หรือการผ่านสนามจริง

## การออกแบบการทดลอง

- ตัวแปรอิสระ: เครื่องหมาย curvature, gain ของ feed-forward/heading/cross-track, steering limit, station spacing และ disturbance ด้านข้าง/heading เริ่มต้น
- ตัวแปรตาม: steer command, feed-forward/feedback terms, signed cross-track/heading error, progress, actual normal load, body mode, energy residual, จำนวน saturation และผลหยุด
- ตัวควบคุม: exact replay, straight corridor, left/right mirror, zero-feedback, gain ผิดเครื่องหมาย, steering saturation, corridor departure และ half-step refinement
- สมมติฐานหลัก: feedback เครื่องหมายถูกต้องลด cross-track error ของกรณี disturbed เทียบกับ feed-forward-only, mirror เมื่อกลับเครื่องหมาย curvature/disturbance และเชื่อมกับ Work 073 โดยไม่เปลี่ยน fixed-steer hash
- การหักล้าง: เครื่องหมายแก้ผิด, look-ahead แบบไม่เป็นเหตุ, clip steering แบบซ่อน, centreline identity ไม่ตรง, ข้าม target-load, พลังงานอธิบายไม่ได้, mirror/replay ไม่ผ่าน หรือ controller ไม่ดีกว่า zero-feedback

## ไฟล์ที่วางแผน

- `config/vehicle/closed_loop_corridor_controller_v1.json`
- `src/formula_ultimate/simulation/closed_loop_corridor_controller.py`
- exports ใน `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_closed_loop_corridor_controller.py`
- `tests/test_closed_loop_corridor_controller.py`
- เอกสารวิจัยและผล Work 074 สองภาษา
- แผน trilogy สำหรับ Work 075 และ Work 076 ที่ผู้ใช้สั่งพร้อม Work 074
- หลักฐานที่ ignore ใต้ `artifacts/work074/`

## การตรวจสอบและเกณฑ์สำเร็จ

Loader ต้องปฏิเสธ gain, limit, spacing, fixture ที่ไม่ปิด/identity ไม่ตรงเมื่อ protocol ห้าม และสถานะ non-finite กรณีอ้างอิงต้องรักษาโหลดยางเป็นบวกและระยะช่วงล่างอยู่ในขอบเขต ทุกคำสั่งต้องไม่เกิน steering limit feedback ที่ถูกต้องต้องลด final absolute cross-track error เทียบ zero-feedback control ที่ลงทะเบียนไว้ Straight/mirror controls, exact replay, การรักษา fixed-steer Work 073 hash, equation/energy residual, half-step refinement `<= 2%`, focused/full tests, bilingual contract, scoped commit และ post-commit replay ต้องผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

การฉายจุดลง centreline ที่ sample เป็น polyline แบบ deterministic เป็นค่าประมาณและเก็บ spacing error ให้เห็น Controller ไม่มี speed optimization, braking, obstacle avoidance, traffic response, state estimator, actuator latency, noise หรือ learning หลักฐาน corridor สังเคราะห์ไม่สามารถรับรองสนามจริง
