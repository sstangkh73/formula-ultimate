# Work 117: โจทย์สองทางระหว่างสถาปัตยกรรมกับชิ้นส่วน

ต้นฉบับภาษาอังกฤษ: `work117-architecture_part_feedback.md`

Status: Planned

หมายเลขเดิมใน Work 106: 116

พึ่งพา: Work 112, Work 114, Work 115

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

สาธิตวงสำรวจปิดที่ feedback ชุดประกอบเปลี่ยนโจทย์ย่อยและสร้าง geometry ใหม่

terminals Work 112 และแบบชุดประกอบ coupled Work 114/115; โจทย์ภายนอกเปลี่ยนไม่ได้

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/experiments/architecture_part_feedback.py`
- `config/development/architecture_part_feedback_v1.json`
- `scripts/development/run_architecture_part_feedback.py`
- `tests/test_architecture_part_feedback.py`

## 3. ขั้นลงมือทำ

1. นิยามข้อเสนอโจทย์ภายในมี version พร้อม loads, heat, motion, envelopes และ unknowns
2. สร้าง candidate ย่อยจากเงื่อนไขที่หาได้จากชุดประกอบ ไม่เลือกโหลดเอื้อด้วยมือ
3. รวมแบบลดรูป/ยังไม่ครบที่ประกาศชัด แล้วส่งข้อกำหนดที่เปลี่ยนกลับ generator
4. รันวงสร้างใหม่มีขอบเขต และยกเลิกหลักฐานย่อยเก่าเมื่อโจทย์เปลี่ยน

## 4. การทดลอง

- IV: การเปลี่ยน architecture/part, decomposition และเปิด feedback เทียบโจทย์ย่อยคงที่
- DV: คุณภาพชุดประกอบ มวล/ความร้อนที่ย้ายไปส่วนอื่น feasibility margins และต้นทุนต่อ iteration
- Controls: โจทย์ภายนอก model coverage, candidates เริ่มต้น และโอกาสคำนวณเดียวกัน

## 5. Tests และการหักล้าง

เปลี่ยนโหลดชุดแล้วต้องประเมินย่อยใหม่ รวมบริเวณหลายหน้าที่โดยไม่คิดมวลซ้ำ บล็อก coefficients ที่แต่งเติมส่วนขาด

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อกเพดาน iteration/resource, task-change schema, uncertainty intervals และกฎตัดสิน/หยุด

ต้องมีวง feedback/สร้างใหม่ที่ย้อนที่มาได้อย่างน้อยหนึ่งวงพร้อมหลักฐานปรับตามเหตุ ทดสอบ improvement แต่ผลลบยังเป็นการทดลองที่ถูกต้องได้

## 7. สิ่งส่งมอบและงานรับต่อ

task ancestry, geometry ก่อน/หลัง, coupling ledger และผลเปรียบเทียบบวก/ลบ

ส่งวง co-design ให้การขยาย subsystem และ search Work 124

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

ห้ามกลับไปบังคับใช้เฉพาะชิ้นส่วนผ่านเดี่ยว แบบ unresolved สำรวจได้ แต่ใช้ยืนยัน feasibility ครบหรือเปลี่ยนกติกาแข่งไม่ได้

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_architecture_part_feedback tests.test_repository_contract -v
python scripts/development/run_architecture_part_feedback.py --config config/development/architecture_part_feedback_v1.json --output-root artifacts/work117/run_a
python scripts/development/run_architecture_part_feedback.py --config config/development/architecture_part_feedback_v1.json --output-root artifacts/work117/run_b --replay-reference artifacts/work117/run_a/result.json
```
