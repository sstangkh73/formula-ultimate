# งานปฏิสัมพันธ์พื้น V1

แหล่งภาษาอังกฤษ: `GROUND_INTERACTION_TASKS_V1.md`

Status: Work 118 นำไปใช้เป็นหลักฐาน reference แบบมีขอบเขตที่ Level-0

## ขอบเขต port และ applicability

Contract นี้ตรึงหลักฐาน moving/contact จาก Work 114 และหลักฐานขอบเขต material จาก Work 116 ปฏิสัมพันธ์พื้นแสดงด้วย contact port ที่มีชื่อ ตำแหน่ง normal load ที่กำหนด และคำขอแรง longitudinal/lateral โดยไม่บังคับเทคโนโลยี contact กลไกบังคับทิศ หรือจำนวน contact แรง longitudinal บวกชี้ตามเส้นทาง แรง lateral บวกชี้ตามทิศขวางที่ลงทะเบียน และ yaw moment บวกคือ `x*F_lateral - y*F_longitudinal`

Adapter ที่นำไปใช้เพียงรายการเดียวคือพื้นผิว synthetic `rigid_dry_coulomb` ที่เปิดเผย coefficient `0.8`, ช่วง coefficient `0-1`, ช่วง normal load `0-6000 N` ต่อ port และช่วงความเร็ว `-30` ถึง `30 m/s` แรงสัมผัสลัพธ์ต้องไม่เกิน `mu*N` normal load ที่เป็นศูนย์หรือติดลบคือ lift-off; การตัดการเชื่อมต่อหรือไม่มี physical interaction ที่อนุญาตให้แรงพื้นเป็นศูนย์ พฤติกรรม tire, soft-soil และ non-tire ที่ไม่รองรับต้องคง unresolved แทนการรับ coefficient นี้ไปใช้

## การหยุด ทิศทาง และ gate

Reference การหยุดใช้ rigid body `300 kg` ที่ `20 m/s`, normal load รวมที่กำหนด `3000 N` และ time step `0.1`, `0.05` และ `0.025 s` โดยบันทึก contact work และ dissipated power แล้วเทียบเวลา ระยะ และการสูญเสีย kinetic energy กับ analytic reference ของแรงคงที่ Energy residual ต้องไม่เกิน `1e-12` แบบสัมพัทธ์ และการเปลี่ยนของ refinement สองระดับสุดท้ายต้องไม่เกิน `1e-10`

Force-circle saturation, friction ศูนย์ lift-off, reverse motion, actuation ถูกตัด, ไม่มี interaction และตำแหน่ง contact ที่เปลี่ยนเป็น causal control บังคับ ค่า resultant สูงสุดต่อ port และ yaw moment ถูกส่งกลับเป็น local part-model load โดย claim ด้าน material จาก Work 116 ยังคง blocked Contract นี้ไม่ยืนยัน tire, soft soil, arbitrary locomotion, load transfer, compliant contact, control stability, wear/thermal evolution, พฤติกรรมยานพาหนะเต็มระบบ หรือสมรรถนะจริง
