# การอินทิเกรตการเคลื่อนที่แบบ coupled

ไฟล์ต้นฉบับภาษาอังกฤษ: `COUPLED_MOTION_INTEGRATION.md`

## จุดประสงค์และขอบเขต

Work 026 อัปเดต `SharedVehicleState` แบบ topology-neutral หนึ่งก้าวจาก aerodynamic wrench ของ Work 024 และ contact wrench รวมของ Work 025 โมดูลนี้เป็นโมเดลคัดเลือกระดับ Level 0 บนระนาบแบบ deterministic ไม่ใช่ physical validation

โมดูลแก้การเคลื่อนที่แนวราบในพิกัด global และ yaw แต่ไม่แก้ heave, pitch, roll, suspension constraint impulse, การเลือก racing line จากสนามสำรวจ, barrier contact หรือ tyre relaxation

## Input และสัญญา coordinate frame

- `aero.force_moment`: แรงและโมเมนต์ใน vehicle body frame รอบ centre of mass
- `contact.force_moment`: แรงราย contact และค่ารวมใน body frame ที่ประกาศ
- `circuit.segment_inputs`: `SpatialStepEvidence` สถานะ available ซึ่งมี curvature, grade, bank, width และ uncertainty เฉพาะตำแหน่ง
- `state.current`: ตำแหน่ง/ความเร็ว global แบบ local-ENU พร้อม yaw และ yaw rate
- `MotionCorridorReference`: ตำแหน่งและ heading ของ centreline ใน local-ENU ณ race distance ของสถานะเริ่มต้นแบบ exact
- `MotionConfiguration`: มวล yaw inertia, duration และความกว้างรถในหน่วย SI

architecture `coupled-level0-reference-v2` route สัญญาณ corridor เข้า `vehicle_motion_solver` ส่วน version 1 คงเดิมเป็นหลักฐานประวัติ

## สมการ

horizontal wrench ใน body frame ที่ประกาศเป็น:

`F_x = F_x,aero + F_x,contact`

`F_y = F_y,aero + F_y,contact`

`M_z = M_z,aero + M_z,contact`

เมื่อถือว่า wrench คงที่ตลอด `dt` จะใช้ orientation ที่ midpoint:

`psi_mid = psi_0 + 0.5*r_0*dt + 0.125*(M_z/I_z)*dt^2`

จากนั้นหมุนแรง body ไป global local-ENU ที่ `psi_mid`, อัปเดตความเร็วหนึ่งครั้ง และใช้ความเร็วแบบ trapezoidal อัปเดตตำแหน่ง:

`v_1 = v_0 + R(psi_mid) * [F_x/m, F_y/m] * dt`

`p_1 = p_0 + 0.5*(v_0 + v_1)*dt`

`r_1 = r_0 + (M_z/I_z)*dt`

`psi_1 = psi_0 + r_0*dt + 0.5*(M_z/I_z)*dt^2`

แกนแนวดิ่งไม่ถูก project ลงถนน Work 026 รักษา `v_z` และใช้ `z_1 = z_0 + v_z*dt`; `motion.kinematic-z` แสดงความสอดคล้อง ส่วน grade ถูกเก็บเป็น evidence สำหรับงาน constrained 3D motion ภายหลัง

## Race progress และ corridor gate

ระบบ project horizontal displacement ไปตามแนวสัมผัส corridor เฉพาะตำแหน่ง เมื่อ curvature ไม่เป็นศูนย์จะใช้ fixed-point iteration จำนวนหกรอบแบบ deterministic เพื่อประเมินแนวสัมผัสที่ midpoint ความคืบหน้าบวกได้รับ race-distance credit ส่วนค่าลบถูกบันทึกเป็น `reverse_progress_m` และได้ credit ศูนย์ ดังนั้นการเคลื่อนที่ด้านข้างล้วนเพิ่ม race distance ไม่ได้

centreline advance ตาม progress ที่ได้รับ credit จากนั้นวัด lateral offset ของ candidate เทียบกับแนวสัมผัสปลายทาง ความกว้างซ้ายและขวาที่ใช้จริงหัก horizontal evidence uncertainty และครึ่งความกว้างรถ หาก clearance ติดลบจะเป็น `departed`; adapter คืน `invalid` พร้อม output signal ศูนย์ และไม่ project state กลับเข้า corridor

นี่เป็น body-width screen เฉพาะตำแหน่ง ยังไม่ sweep ความยาวรถ มุมรถ corner ของตัวถัง overhang, barrier หรือ kerb ส่วน Work 010 ยังคงเป็น static swept-envelope feasibility screen แยก

## Residual ที่สังเกตได้

ระบบเก็บ residual เก้ารายการ:

- input aggregation สามรายการสำหรับ `F_x`, `F_y` และ `M_z` ของ contact
- horizontal force balance สองรายการ
- yaw-moment balance หนึ่งรายการ
- position-kinematic check สามรายการสำหรับ `x`, `y` และ `z`

ค่ารวม contact ไม่สอดคล้อง, balance ไม่ผ่าน, spatial record หาย, corridor reference ไม่ตรง, สถานะเริ่มอยู่นอก corridor หรือ candidate ออกจาก corridor จะทำให้ adapter invalid และไม่เขียน motion candidate

## หลักฐานเชิงวิเคราะห์

validator แยกแสดงว่า:

- constant straight force: `v_x = 12 m/s`, `x = 11 m` และ race distance `= 11 m` หลัง `1 s` จาก `v_x = 10 m/s` เมื่อ `F_x = 2000 N`, `m = 1000 kg`
- residual ทั้งเก้ารายการผ่าน
- rotating constant body force: ลด `dt` จาก `1.0 s` เป็น `0.05 s` แล้ว error ของตำแหน่งหลังหนึ่งวินาทีลดจาก `0.08383245221108916 m` เป็น `0.00019773501705859235 m`
- lateral-only credited progress เท่ากับ `0 m`
- reverse raw progress เท่ากับ `-2 m`, credited progress เท่ากับ `0 m` และ uncredited reverse evidence เท่ากับ `2 m`
- corridor departure และ spatial evidence ที่หายคืน `invalid` พร้อม output ศูนย์
- input เดิม replay ได้ผล exact

## ข้อจำกัดและขอบเขตการเลื่อนระดับ

corridor fixture เป็นข้อมูลเชิงวิเคราะห์เฉพาะตำแหน่ง งานนี้ไม่ได้เลื่อน profile ใดในสิบสนามเป็น surveyed 3D admission ค่า bank และ grade ยังไม่สร้าง constraint force และ force input คงที่ภายในหนึ่ง step Level 0 ใช้ปฏิเสธหรือจัดอันดับ candidate ได้ แต่ยืนยัน performance หรือ safety ในโลกจริงไม่ได้
