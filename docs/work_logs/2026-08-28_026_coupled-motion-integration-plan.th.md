# แผนงาน 026: การอินทิเกรตสถานะการเคลื่อนที่แบบ coupled

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-28_026_coupled-motion-integration-plan.md`

## วัตถุประสงค์

สร้าง motion step ระดับ Level 0 แบบ deterministic หนึ่งก้าว ซึ่งอัปเดตความเร็วตามยาวและด้านข้าง อัตรา yaw, yaw, ตำแหน่งระนาบ เวลา และระยะทางแข่ง จากผลรวมสัญญาณแรง/โมเมนต์ aerodynamic และ contact โดยความล้มเหลวของ corridor และเชิงตัวเลขต้องสังเกตได้

## ขอบเขต

- นิยาม motion configuration, candidate state, integration evidence และ corridor evidence แบบ typed
- รวม wrench จาก aerodynamic ของ Work 024 และ contact ของ Work 025 โดยไม่แก้แรงหรือโมเมนต์แบบซ่อน
- อินทิเกรตการเคลื่อนที่ rigid body บนระนาบในหน่วย SI ด้วยวิธี deterministic ที่ระบุชัด
- เพิ่มระยะทางแข่งจากความคืบหน้าตามแนวสัมผัส corridor ไม่ใช่ขนาดความเร็วรวม
- ปฏิเสธ spatial evidence ที่หายหรือไม่รองรับ และแสดง corridor departure, reverse progress, non-finite state และ residual ที่ไม่ผ่าน
- เพิ่มการทดสอบ analytical reference, timestep refinement, deterministic replay, adapter contract และ failure
- เพิ่ม validator แยก และเอกสารโมเดล/ผลลัพธ์สองภาษา
- หาก architecture ปัจจุบันส่งสัญญาณ corridor ที่จำเป็นไม่ได้ ให้เขียนรายงานปัญหาสองภาษาแยกและแก้ด้วย architecture รุ่นใหม่ โดยไม่แก้หลักฐานประวัติแบบเงียบ

## ไฟล์ที่วางแผน

- `src/formula_ultimate/simulation/motion_coupling.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_motion_coupling.py`
- `scripts/validate_motion_coupling.py`
- `docs/simulation/COUPLED_MOTION_INTEGRATION.md`
- `docs/simulation/COUPLED_MOTION_INTEGRATION.th.md`
- `docs/integration/COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.md`
- `docs/integration/COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.th.md`
- แผนนี้และไฟล์คู่ภาษาไทย
- บันทึกผลลัพธ์ที่เข้าคู่กัน
- ไฟล์ architecture/test/problem report แบบมี version เฉพาะเมื่อการตรวจ signal contract ยืนยันว่าจำเป็น

## นิยามการทดลอง

- ตัวแปรอิสระ: แรงและ yaw moment, timestep, ความเร็ว body/อัตรา yaw เริ่มต้น, curvature/grade/bank/width ของ segment และระยะเผื่อ corridor ของรถ
- ตัวแปรตาม: ความเร็ว อัตรา yaw, yaw, ตำแหน่ง ระยะทางแข่งที่เพิ่ม residual การอินทิเกรต และสถานะ corridor
- ตัวควบคุม: มวล yaw inertia, สถานะเริ่มต้น วิธีอินทิเกรต provenance ของ input และลำดับแบบ deterministic
- เมตริก: ค่าคลาดเคลื่อนจาก analytical state, ค่าคลาดเคลื่อน timestep หยาบเทียบละเอียด, force/moment residual, corridor clearance, replay equality และจำนวน output เมื่อ invalid
- เกณฑ์สำเร็จ: fixture เชิงวิเคราะห์ตรงตาม tolerance; refinement ลด error ใน fixture การเคลื่อนที่โค้ง; residual ที่ประกาศผ่านทั้งหมด; replay เท่ากัน exact; corridor departure และหลักฐาน spatial ที่หายทำให้ adapter invalid และมี output signal เป็นศูนย์
- เกณฑ์ล้มเหลว: ยอมรับ input non-finite หรือผิดมิติ; ระยะทางแข่งเพิ่มจากการเคลื่อนที่ด้านข้าง/ถอยหลัง; ซ่อน corridor failure; ผลเปลี่ยนตามลำดับ input; หรือ commit residual ที่ไม่ผ่าน
- การพยายามหักล้างสมมติฐาน: ใช้ fixture lateral-only, reverse-motion, off-corridor, width ไม่พอ, spatial evidence หาย และ wrench ที่จงใจให้ไม่สอดคล้อง

## การตรวจสอบ

1. unit test เฉพาะ Work 026
2. test suite ทั้ง repository
3. validator ของ Work 026 พร้อมหลักฐาน analytical และ refinement
4. compile Python bytecode
5. `git diff --check` และ `git diff --cached --check`
6. ตรวจ staged scope แบบระบุไฟล์ก่อน commit

## เกณฑ์สำเร็จ

- สร้าง candidate motion state หนึ่งชุดจากผลรวม wrench ที่ตรง exact
- สถานะตามยาว ด้านข้าง yaw ตำแหน่ง เวลา และ race progress ตามแนวสัมผัส corridor เชื่อมกันและ replay ได้
- analytical, refinement, residual และ corridor gate ผ่าน
- failure path ทุกแบบสังเกตได้และไม่ปล่อย candidate state
- บันทึกอังกฤษและไทยตรงกันด้านสมการ หน่วย คำสั่ง หลักฐาน ข้อจำกัด และสถานะ
- commit งานที่เสร็จเป็น validated commit แยกหนึ่งรายการ

## ความเสี่ยง

- architecture จาก Work 021 อาจไม่ได้ route `circuit.segment_inputs` เข้า motion module
- spatial sample เฉพาะตำแหน่งอาจไม่เพียงพอสร้าง centerline ที่สำรวจครบ
- การอินทิเกรตอันดับหนึ่งอาจปิด force balance ได้แต่สะสม trajectory error
- การใช้ขนาดความเร็วเป็นระยะทางแข่งจะให้รางวัลผิดกับการเคลื่อนที่ด้านข้างหรือถอยหลัง

## สิ่งที่ไม่ทำโดยชัดแจ้ง

- ไม่อ้าง calibrated validation, surveyed-circuit validation, CFD, tyre-rig หรือ physical validation
- ไม่ทำ full-race orchestrator, energy/thermal state commit, lap event arbitration หรือ Work 027-030
- ไม่ project รถกลับเข้า corridor แบบซ่อน และไม่ redistribute แรงแบบซ่อน
- ไม่ optimize ดีไซน์รถ
