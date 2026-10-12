# แผนงาน Work 163: การส่งกำลัง v2 (โซ่ลูกกลิ้งแบบสัมผัสกลิ้ง)

ต้นฉบับภาษาอังกฤษ: `2026-10-13_163_v2-power-transmission-plan.md`

Status: Completed

## วัตถุประสงค์

เพิ่มกลไกส่งกำลังในชั้นกลไก v2 เพื่อให้แพ็กเกจมีหลักฐาน `power_transmission`
จริง: โซ่ของชิ้นที่หมุนแบบ revolute เต็มรอบอย่างน้อย 2 ชิ้น ชิ้นที่ติดกันเชื่อมด้วย
interface ทุกชิ้นมี `bearing` กับชิ้นส่วนที่อยู่กับที่ กวาดได้โดยไม่ชน
และยึดกับแผ่นโครงสร้าง (deck)

## การออกแบบ

- โมดูล Python ล้วนใหม่ `src/formula_ultimate/hierarchy/power_transmission.py`
  มี `add_power_transmission(layer, seed, catalogue, config)` (ต่อจาก layer ของ
  `add_direction_control`) และ `power_transmission_problems(layer)`
- assembly ระดับรากหนึ่งชุด `m<k>-power_transmission` ติดแท็ก
  `[power_transmission]` ในส่วน -x ที่ว่างของ bay บน deck ตั้งแต่
  `bay_x0 + m` ถึงวงกลมกวาดของแขนบังคับเลี้ยวลบ `m` (m = 0.02 m)
- สถานี 2 หรือ 3 สถานีเรียงตามแนว y บนเส้นกึ่งกลางของแถบว่าง แต่ละสถานี:
  boss (แผ่นหลายเหลี่ยมปกติ N_b เหลี่ยมบนผิว deck, `bonded` กับ deck),
  post (หลายเหลี่ยมปกติ N_p เหลี่ยมบน boss, `bonded`), roller (จานหลายเหลี่ยม
  ปกติ N_r เหลี่ยม N_r เป็นเลขคู่ มีรูเจาะ 96 เหลี่ยม apothem `r_p + c`,
  c = 2.5e-5 m ลอยเหนือผิว boss เป็นระยะ `c`, `bearing` กับ post)
- การสัมผัสแบบกลิ้ง: จุดศูนย์กลาง roller ที่ติดกันห่างกัน `R_i + R_j + c`
  (รัศมีวงกลมล้อมรอบ) และแต่ละ roller มีจุดยอดชี้ไปยังเพื่อนบ้านแต่ละตัว
  ช่องว่างที่วัดจากจุดยอดจึงเป็น `c` และเพราะการกวาดเต็มรอบอยู่ภายในวงกลมล้อมรอบ
  จึงไม่มีการหมุนใดทำให้ roller หนึ่งเข้าไปในอีกตัว interface ชนิด `rolling`
  ระหว่าง roller ที่ติดกัน
- Motion `<assembly>.r<i>` = {roller i} แบบ revolute รอบ +z ช่วง 2 pi
- หลักฐาน: `power_transmission: {chain: [motion id ตามลำดับ]}`
- generator เรียกหลัง `add_direction_control` และนำ config ไปรวมใน hash

## ไฟล์ที่วางแผน

- `src/formula_ultimate/hierarchy/power_transmission.py` (ใหม่)
- `scripts/hierarchy/generate_functional_vehicle.py`
- `tests/test_hierarchy_power_transmission.py` (ใหม่)
- บันทึกแผน/ผล (EN + TH), `auto-loop/progress.md` (+ `.th.md`)

## การตรวจสอบ

- `python -m unittest tests.test_hierarchy_power_transmission tests.test_hierarchy_direction_control -v`
- สร้าง seed 11, 23, 37 ลงใน `artifacts/work163/`; รันคลาส acceptance
  โดยผ่อนการตรวจเก้าคีย์ในเครื่อง (สคริปต์ที่ gitignore) สำหรับ A0 interfaces,
  A2 motions, B3, B4, B5, B6; รัน Level-0 evaluator กับ seed 11
- `pwsh -NoProfile -File auto-loop/verify.ps1`: Gate 1 และ 2 ต้องผ่าน
  ห้ามมีการทดสอบ Gate 3 ที่เคยผ่านแล้วถดถอย

## เกณฑ์ความสำเร็จ

การทดสอบเฉพาะผ่าน การตรวจ B3 และ A2 ในเครื่องผ่านบน 11/23/37 Gate 1-2 ผ่าน
Tier A, B10 และ C1 ยังเขียว

## ความเสี่ยง

- แถบว่างอาจแคบได้ถึงประมาณ 0.12 m รัศมี roller จึงถูกจำกัดให้พอดี
  และการวางแผนจะ raise หากแม้ค่าต่ำสุดก็ไม่พอดี
- roller สัมผัสกันที่จุดยอดคู่เดียว (ตัวแทนของการสัมผัสแบบเส้น)
  ไม่มีแบบจำลองแรงบิดหรือการลื่น

## สิ่งที่ไม่ใช่เป้าหมาย

ไม่มีการเชื่อม roller กับล้อหรือ converter ไม่มีฟันเฟือง ไม่มีแรงบิด
ประสิทธิภาพ หรือการลื่น ไม่ใช่การยืนยันทางฟิสิกส์
