# Work 127: baseline รถที่ปรับดีและการแทนชิ้นเพื่อทดสอบเหตุ

ต้นฉบับภาษาอังกฤษ: `work127-optimized_vehicle_controls.md`

Status: Planned

หมายเลขเดิมใน Work 106: 126

พึ่งพา: Work 123, Work 126

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

ตรวจว่าประโยชน์ทั้งระบบของ candidate ยังอยู่เมื่อเทียบ baseline ที่ปรับดี ปรับ controller และรวมภาระที่ย้ายไปส่วนอื่น

ชุด candidate แน่นอน Work 126 และ harness Work 123; accounting/registration จาก Work 124

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/experiments/optimized_vehicle_controls.py`
- `config/development/optimized_vehicle_controls_v1.json`
- `scripts/development/run_optimized_vehicle_controls.py`
- `tests/test_optimized_vehicle_controls.py`

## 3. ขั้นลงมือทำ

1. นิยาม fixed-topology และ random/reference arms เป็นธรรม โดยไม่บังคับ open arm ให้ใช้ layout เดียวกัน
2. ปรับทุก arm ตาม task, โอกาส library และงบคำนวณครบที่เท่ากัน
3. แทนกลไกที่เสนอโดยใช้ controller ร่วม แล้วทดลอง retune ด้วยงบเท่ากัน
4. นับการเปลี่ยน cooling, containment, supports, energy และสมมติฐานผลิต

## 4. การทดลอง

- IV: vehicle/search arm, การแทน subsystem และวิธีจัด controller
- DV: completion/time, energy/mass รวม, failure margins และต้นทุน search/tuning รวม
- Controls: race, energy, environment, safety scope ภายนอก materials และนโยบาย random seed เดียวกัน

## 5. Tests และการหักล้าง

baseline ไม่ปรับ controller effort ฟรี มวล cooling ถูกละ และ source energy ไม่เท่าต้องทำให้คำอ้างความเป็นธรรมใช้ไม่ได้

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก baseline families, โอกาส optimization, paired comparison, meaningful system effect และวิธี uncertainty

ทุก arm ได้โอกาสที่ลงทะเบียนและคิดต้นทุนครบ คำอ้างประโยชน์ระบบต้องดีขึ้นเกิน uncertainty โดยไม่โยกภาระไปซ่อน

## 7. สิ่งส่งมอบและงานรับต่อ

artifacts baseline ที่ปรับดี substitution matrix, controller ledgers และ analysis ผลระบบมีเครื่องหมาย

ล็อก finalists และวิธีเปรียบเทียบให้ held-out race Work 128

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

baseline แบบเดิมเป็นตัวควบคุม ไม่ใช่คำตอบบังคับ ถ้าความเป็นธรรมใช้ไม่ได้ต้อง registration ใหม่ ไม่อ้างความใหม่ภายนอก

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_optimized_vehicle_controls tests.test_repository_contract -v
python scripts/development/run_optimized_vehicle_controls.py --config config/development/optimized_vehicle_controls_v1.json --output-root artifacts/work127/run_a
python scripts/development/run_optimized_vehicle_controls.py --config config/development/optimized_vehicle_controls_v1.json --output-root artifacts/work127/run_b --replay-reference artifacts/work127/run_a/result.json
```
