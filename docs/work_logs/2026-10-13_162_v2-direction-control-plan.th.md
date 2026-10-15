# แผนงาน Work 162: การควบคุมทิศทาง v2 (เสาบังคับเลี้ยวและแขน)

ต้นฉบับภาษาอังกฤษ: `2026-10-13_162_v2-direction-control-plan.md`

Status: Completed

## วัตถุประสงค์

เพิ่มกลไกควบคุมทิศทางในชั้นกลไก v2 เพื่อให้แพ็กเกจมีหลักฐาน
`direction_control` จริง: การเคลื่อนที่แบบ revolute รอบแกนแนวตั้ง
(ห่างจากแกน ground-propulsion ทุกแกน ซึ่งอยู่ตามแนว y อย่างน้อย 30 deg)
ช่วงการหมุน >= 0.2 rad มี interface ชนิด `bearing` กับชิ้นส่วนที่อยู่กับที่
กวาดได้โดยไม่ชน และยึดกับแผ่นโครงสร้าง (deck)

## การออกแบบ

- โมดูล Python ล้วนใหม่ `src/formula_ultimate/hierarchy/direction_control.py`
  มี `add_direction_control(layer, seed, catalogue, config)` (ต่อจาก layer ของ
  `add_ground_contacts`) และ `direction_control_problems(layer)`
- assembly ระดับราก หนึ่งชุด `m<k>-direction_control` ติดแท็ก
  `[direction_control]` ในช่องว่าง (bay) ของ deck (`bay_x0..core_x1`) บนผิวบน
  ของ deck ประกอบด้วย prism `func-leaf-mechanism-v2` สามชิ้นที่อัดขึ้นตาม +z:
  - boss: แผ่นรูปหลายเหลี่ยมปกติ N_b เหลี่ยมบนผิว deck (`bonded` กับ deck)
  - post: prism รูปหลายเหลี่ยมปกติ N_p เหลี่ยมบนผิวบนของ boss (`bonded` กับ boss)
  - arm: แผ่นคานนูน (hub polygon รวมกับ tip polygon แล้วหา convex hull)
    มีรูเจาะ 96 เหลี่ยม apothem `r_p + c` (c = 2.5e-5 m มีจุดยอดรูตรงทิศจุดยอด
    ของ post ทุกจุด) ลอยเหนือผิว boss เป็นระยะ `c`; `bearing` กับ post
- Motion `<assembly>.steer` = {arm} แบบ revolute รอบ +z ผ่านแกน post
  ช่วงการหมุนสุ่มใน [0.3, 0.8] rad
- post อยู่ปลาย +x ของ bay กึ่งกลางในแนว y เพื่อให้วงกลมกวาดเต็มรอบของ arm
  อยู่ภายใน bay และภายในรูปรอยของ deck (ห่างจาก cluster และล้อ)
  และเหลือส่วน -x ของ bay ไว้ให้โมดูลถัดไป
- หลักฐาน: `direction_control: {motion: <steer id>}`
- generator เรียกหลัง `add_ground_contacts` และนำ config ไปรวมใน hash

## ไฟล์ที่วางแผน

- `src/formula_ultimate/hierarchy/direction_control.py` (ใหม่)
- `scripts/hierarchy/generate_functional_vehicle.py`
- `tests/test_hierarchy_direction_control.py` (ใหม่)
- บันทึกแผน/ผล (EN + TH), `auto-loop/progress.md` (+ `.th.md`)

## การตรวจสอบ

- `python -m unittest tests.test_hierarchy_direction_control tests.test_hierarchy_ground_contacts tests.test_hierarchy_mechanisms -v`
- สร้าง seed 11 (และ 23, 37) ลงใน `artifacts/work162/`; รันคลาส acceptance
  โดยผ่อนการตรวจเก้าคีย์ในเครื่อง (สคริปต์ที่ gitignore) สำหรับ A0 interfaces,
  A2 motions, B4, B5, B6; รัน Level-0 evaluator กับ seed 11
- `pwsh -NoProfile -File auto-loop/verify.ps1`: Gate 1 และ 2 ต้องผ่าน
  ห้ามมีการทดสอบ Gate 3 ที่เคยผ่านแล้วถดถอย

## เกณฑ์ความสำเร็จ

การทดสอบเฉพาะผ่าน การตรวจ B5 และ A2 ในเครื่องผ่านบน 11/23/37 Gate 1-2 ผ่าน
Tier A, B10 และ C1 ยังเขียว

## ความเสี่ยง

- พื้นที่ bay ใช้ร่วมกับโมดูลถัดไป งานนี้จองเฉพาะปลาย +x
- arm ลอยเหนือ boss เป็นระยะ `c` (ระยะเผื่อแรงตามแกน) ไม่มีการจำลองการยึดตามแกน

## สิ่งที่ไม่ใช่เป้าหมาย

ไม่มีข้อต่อจากแขนบังคับเลี้ยวไปยังล้อ ไม่มีเรขาคณิตการเลี้ยว ไม่มีพลศาสตร์ยานยนต์
ไม่ใช่การยืนยันทางฟิสิกส์
