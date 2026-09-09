# Work 109: ตัวสร้างเนื้อวัสดุรูปทรงอิสระ

ต้นฉบับภาษาอังกฤษ: `work109-freeform_material_generator.md`

Status: Planned

หมายเลขเดิมใน Work 106: 108

พึ่งพา: Work 108

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

เปิดให้เปลี่ยนขอบเขตต่อเนื่องและ topology โดยไม่ใช้ template ชื่อชิ้นส่วน พิสูจน์ coverage เรขาคณิต ไม่ใช่สมรรถนะเหนือกว่า

ข้อมูลเข้า: region contract และการนับวัสดุ Work 108; ใช้ B-rep เดิมเป็นเส้นทางเทียบ

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/search/freeform_material_generator.py`
- `config/development/freeform_material_generator_v1.json`
- `scripts/development/run_freeform_material_generator.py`
- `tests/test_freeform_material_generator.py`

## 3. ขั้นลงมือทำ

1. นิยาม implicit/adaptive-volume representation พร้อมความละเอียดและ material labels
2. พัฒนาเลื่อนขอบเขต เดินโพรง แตกแขนง split/merge และกระจายวัสดุใหม่
3. สร้าง surface/export adapters และวัด approximation error เทียบสนามต้นทาง
4. รัน mutation chains ตาม seed และทดลองขยาย representation เก็บ conversions ที่ไม่รองรับ

## 4. การทดลอง

- IV: representation, edit operator, spatial resolution และ complexity cap
- DV: geometry error, topology ที่เข้าถึงได้, features ที่รักษาไว้ และ execution cost
- Controls: spatial domain, materials, random seeds และโอกาสคำนวณเท่ากัน; reference grammar คงที่

## 5. Tests และการหักล้าง

สร้างและปิดรู แยกและต่อบริเวณ รักษา feature บางไม่สมมาตร ตรวจ self-intersection, โพรงหาย, label ปน และความใหม่ปลอมจากการเปลี่ยนชื่อ

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก minimum feature, field resolution, conversion tolerance, mutation bounds และงบต่อ attempt

กรณี valid ที่ลงทะเบียนต้องรักษา occupancy/material identity ใน error bounds; invalid/unsupported conversions แสดงชัด ไม่ใช้เงาร่างเป้าหมายตายตัวเป็นเกณฑ์

## 7. สิ่งส่งมอบและงานรับต่อ

corpus ที่สร้าง mutation ancestry, source fields, surfaces ที่ตรวจได้ และ conversion-coverage matrix

ส่ง geometry ไม่คุ้นเคยให้ Work 110 และการค้นหา Work 124

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

อคติ kernel/grid อาจดูเหมือนข้อจำกัดฟิสิกส์ ต้องบันทึกและปรับ adapters ไม่แต่งคุณสมบัติวัสดุผสมหรือรับประกันรูปทรงใดก็ได้

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_freeform_material_generator tests.test_repository_contract -v
python scripts/development/run_freeform_material_generator.py --config config/development/freeform_material_generator_v1.json --output-root artifacts/work109/run_a
python scripts/development/run_freeform_material_generator.py --config config/development/freeform_material_generator_v1.json --output-root artifacts/work109/run_b --replay-reference artifacts/work109/run_a/result.json
```
