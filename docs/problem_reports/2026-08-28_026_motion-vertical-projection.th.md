# รายงานปัญหา: การ project แนวดิ่งแบบซ่อนระหว่าง motion step

สถานะ: Resolved

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-28_026_motion-vertical-projection.md`

## บริบท

ร่าง implementation แรกของ Work 026 คำนวณพิกัด `z` ของ candidate ด้วยการกำหนดให้เท่ากับพิกัด `z` ของ centreline ที่ advance แล้ว

## ผลกระทบ

หากสถานะเริ่มต้นมี vertical offset จาก corridor reference หนึ่ง motion step จะลบ offset นั้นโดยไม่มีแรงแนวดิ่ง constraint impulse หรือ residual ที่ประกาศไว้ จึงเป็นการแก้ state แบบซ่อน

## สาเหตุราก

การ advance centreline และ vehicle state ใช้ค่าแนวดิ่งเดียวกัน ทั้งที่ Work 026 เป็นโมเดลตามยาว/ด้านข้าง/yaw บนระนาบและไม่ได้แก้ vertical dynamics

## การแก้ไข

รักษา vertical offset เริ่มต้นของรถและใช้ vertical kinematics แบบความเร็วคงที่ เพราะ Work 026 ไม่ได้แก้แรงแนวดิ่ง โดย `z` ของ candidate เป็น:

`z_candidate = z_start + v_z_start * duration`

ค่า `v_z` คงเดิมและมี residual `motion.kinematic-z` ตรวจการอัปเดตตำแหน่ง ส่วน centreline reference ยัง advance แยกเพื่อสร้าง corridor evidence โดย Work 026 ไม่ project รถลงบน centreline

## Regression gate

unit test เริ่มรถเหนือ reference centreline พร้อม vertical velocity ที่ประกาศ และยืนยันการอัปเดต `z` แบบ constant velocity ที่ตรง exact

## ข้อจำกัด

การเคลื่อนที่แนวดิ่งที่ถูกบังคับตาม grade, suspension heave, road contact impulse, การกระโดด และ rigid-body dynamics แบบ 3D เต็มอยู่นอก Work 026 ระบบเก็บ grade evidence แต่ไม่บังคับใส่ candidate state แบบซ่อน
