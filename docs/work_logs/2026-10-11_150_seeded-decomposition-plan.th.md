# แผน Work 150: การแตกโครงสร้างแบบนามธรรมที่ขับด้วย seed

ฉบับภาษาอังกฤษ: `2026-10-11_150_seeded-decomposition-plan.md`

วันที่: 2026-10-11

Status: Completed

## วัตถุประสงค์

Milestone 2 ของ `auto-loop/GOAL.md`: กระบวนการแตกโครงสร้างที่ขับด้วย seed ซึ่งสร้างลำดับชั้นแบบนามธรรม
(ไม่มีเรขาคณิต) ครอบคลุมเก้าความสามารถใน `REQUIRED_CAPABILITIES` โดยไม่ใช้แคตตาล็อกชิ้นส่วนแบบดั้งเดิม
งานถัดไปจะสร้างเรขาคณิตของชิ้นส่วนใบและ interface จากโครงสร้างนี้

## ขอบเขต

- โมดูลใหม่ `src/formula_ultimate/hierarchy/decomposition.py`:
  - `DecompositionConfig` (frozen) ที่ประกาศข้อจำกัด: ช่วงงบจำนวนใบรวม, จำนวนชั้นขั้นต่ำ,
    ความสูงและจำนวนใบขั้นต่ำต่อความสามารถ, ช่วงจำนวนกิ่ง, ความลึกสูงสุด, ความน่าจะเป็นในการรวมความสามารถ,
    ความยาวลักษณะของ root (m), ช่วงสัดส่วนขนาดของลูก, อัตราส่วนขนาดใบขั้นต่ำ, จำนวนครั้งค้นหาสูงสุด
  - `decompose(seed, config)` ที่ใช้เฉพาะ `random.Random` ซึ่ง seed จาก `(seed, attempt)`:
    จัดกลุ่มความสามารถ (เดี่ยวหรือคู่), แบ่งงบใบต่อกลุ่ม, แบ่งงบแบบ recursive เป็นลูก 2..k
    (มี anchor child หนึ่งตัวต่อ assembly), กำหนดความยาวลักษณะจากสัดส่วนที่ประกาศ
    และประกาศ attachment แบบนามธรรม (anchor leaf ของลูกที่ไม่ใช่ anchor ต่อกับ anchor leaf ของ anchor child)
    พร้อมชนิดรอยต่อที่ seed เลือก attempt ที่ไม่ผ่านข้อจำกัดที่ประกาศจะถูกปฏิเสธและลองครั้งถัดไป
    และบันทึกหมายเลข attempt ที่ยอมรับ
  - `config_sha256(config)` ผ่าน `canonical_sha256`
  - ตัวตรวจต้นไม้นามธรรมและตัววัด (levels, leaves, subtree height, topology signature ตามนิยามของ acceptance)
- เทสต์ใหม่ `tests/test_hierarchy_decomposition.py`

## ไฟล์ที่วางแผน

- `src/formula_ultimate/hierarchy/decomposition.py` (ใหม่)
- `tests/test_hierarchy_decomposition.py` (ใหม่)
- คู่แผนและผลลัพธ์นี้ (อังกฤษและไทย)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## การตรวจสอบ

1. `python -m unittest tests.test_hierarchy_decomposition -v`
2. `pwsh -NoProfile -File auto-loop/verify.ps1` (Gate 1 และ 2 ต้องผ่าน;
   Gate 3 ยังล้มเพราะยังไม่มี generator)

## เกณฑ์ความสำเร็จ

- สำหรับ seed 11, 23, 37 และ seed อื่นอีกชุดหนึ่ง: >= 4 ชั้น, >= 150 ใบ,
  ทุกความสามารถมี assembly ที่ระบุชื่อด้วยความสูง >= 2 และ >= 5 ใบ, อัตราส่วนความยาวลักษณะของใบ >= 100,
  ทุก assembly ที่มีลูก >= 2 ตัวเชื่อมกันด้วย attachment
- seed 11, 23, 37 ให้ signature ของทั้งต้นไม้ต่างกันเป็นคู่ และทุกความสามารถมีชุด signature ต่างกัน >= 2 แบบ
- seed เดิมให้ต้นไม้เหมือนเดิม; root ไม่มีความสามารถ จึงไม่สามารถผ่านเกณฑ์ความสามารถได้ด้วยตัวเอง
- ไม่มีโค้ดที่แยกกรณีตาม seed เฉพาะ Gate 1 และ 2 ผ่าน

## ความเสี่ยง

- ความยาวลักษณะเป็นเป้าหมายการวางแผน ไม่ใช่เรขาคณิตที่วัดได้ อัตราส่วนขนาดของ acceptance
  วัดจาก mesh ภายหลังและอาจต่างไป
- การค้นหาแบบปฏิเสธอาจวนนาน จำกัดด้วย `max_attempts` พร้อม error ที่ชัดเจน

## สิ่งที่ไม่ทำ

- ไม่มีเรขาคณิต, CadQuery, STL, มวล, วัสดุ หรือ generator CLI
- ไม่อ้างว่าการแตกโครงสร้างมีประโยชน์ทางกายภาพ
