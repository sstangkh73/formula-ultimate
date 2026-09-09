# Work 125: การเปรียบเทียบค้นพบชิ้นส่วนละเอียดที่ลงทะเบียน

ต้นฉบับภาษาอังกฤษ: `work125-detailed_part_comparison.md`

Status: Planned

หมายเลขเดิมใน Work 106: 124

พึ่งพา: Work 113, Work 114, Work 115, Work 116, Work 124

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

ทดสอบว่าชิ้นส่วนละเอียดที่สร้างอิสระให้ประโยชน์ตามโจทย์เกิน numerical uncertainty และ controls ที่ปรับดีอย่างเป็นธรรมหรือไม่

แบบจุดเชื่อม/fields ละเอียดที่ตรวจแล้วและ engine Work 124; ใช้ admitted conditions ใหม่แยกจาก pilots

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/experiments/detailed_part_comparison.py`
- `config/development/detailed_part_comparison_v1.json`
- `scripts/development/run_detailed_part_comparison.py`
- `tests/test_detailed_part_comparison.py`

## 3. ขั้นลงมือทำ

1. เลือก functional task ขอบเขตชัด ล็อก training/holdout และ meaningful effect ก่อนเทียบ
2. ปรับ arms แบบ fixed-family, grammar เดิม, open-material และ random-control ด้วยงบเท่ากัน
3. รันการศึกษาแบบจับคู่และ audit geometry ที่ปฏิเสธ/unresolved โดยไม่ขึ้นกับ proxy score
4. ablate geometry/coupling ที่เสนอว่าทำงาน แล้วประเมิน finalists ด้วย fidelity สูงขึ้น

## 4. การทดลอง

- IV: representation/search arm, การแทรก geometry/coupling และสภาพทำงาน held-out
- DV: task utility ที่ตรวจแล้ว ภาระ material/energy, failure margins และต้นทุนรวม
- Controls: task, หลักฐาน material/process, งบ และ seed pairing เดียวกัน; controls ปรับดี ไม่ใช้ default ที่ไม่ปรับ

## 5. Tests และการหักล้าง

ส่วนยื่นไม่ทำงาน การตอบสนองเปลี่ยนแต่กราฟเดิม hardware ถูกละ ลำดับกลับเมื่อ mesh ละเอียด และตรวจ holdout รั่ว

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก sample size จาก pilot แยก estimand ผลลัพธ์ วิธี uncertainty, effect threshold และกฎหยุด

การทดลองจบได้แม้ผลลบ ส่วนคำอ้างค้นพบมีประโยชน์ต้องผ่าน constraints, signed effect และ uncertainty เพิ่ม

## 7. สิ่งส่งมอบและงานรับต่อ

registration, ผลทุก arm, ablation evidence, holdout report และหลักฐานสนับสนุน/ขัดแย้ง/ทางเลือก/ที่ขาด

ส่งชิ้นส่วนมีประโยชน์ตามขอบเขตและผลลบให้รถละเอียด Work 126

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

ห้ามปรับ thresholds หลังผลหรือบังคับความแปลกตา ความใหม่เทียบ prior art และประโยชน์รถทั้งคันเป็นการศึกษาแยก

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_detailed_part_comparison tests.test_repository_contract -v
python scripts/development/run_detailed_part_comparison.py --config config/development/detailed_part_comparison_v1.json --output-root artifacts/work125/run_a
python scripts/development/run_detailed_part_comparison.py --config config/development/detailed_part_comparison_v1.json --output-root artifacts/work125/run_b --replay-reference artifacts/work125/run_a/result.json
```
