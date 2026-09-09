# Work 108: ข้อมูลต้นทางร่วมของเนื้อวัสดุและช่องว่าง

ต้นฉบับภาษาอังกฤษ: `work108-spatial_material.md`

Status: Planned

หมายเลขเดิมใน Work 106: 107

พึ่งพา: หลักฐาน CAD เดิม

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

สร้าง geometry จริงที่การนับเนื้อวัสดุ โพรง มวล จุดศูนย์ถ่วง และความเฉื่อยสอดคล้องกันหลัง export และย้ายตำแหน่ง

ข้อมูลเข้า: B-rep corpus จาก Work 092, CAD inspection adapters และ spatial contract ที่เสนอใน Work 106; ตรวจ CAD runtime ที่ติดตั้งจริง

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/components/spatial_material.py`
- `config/development/spatial_material_v1.json`
- `scripts/development/run_spatial_material.py`
- `tests/test_spatial_material.py`

## 3. ขั้นลงมือทำ

1. นิยามกรอบ SI บริเวณวัสดุ/ช่องว่าง การนับเนื้อ และการอ้าง revision ที่เปลี่ยนย้อนหลังไม่ได้
2. ต่อ CAD โค้ง แตกแขนง มีโพรง และหลาย body เดิม ปฏิเสธเนื้อซ้อนที่ไม่ประกาศ
3. คำนวณ mass properties จากเนื้อ geometry และเทียบการวัด CAD อิสระ
4. เปลี่ยนโพรง/วัสดุและตำแหน่ง ทำให้หลักฐานที่พึ่งพาหมดอายุ และ replay exports

## 4. การทดลอง

- IV: geometry โพรง วัสดุรายบริเวณ และตำแหน่ง rigid
- DV: ความต่าง volume, mass, center-of-mass และ inertia
- Controls: geometry revision เดียวกันและ reference วัสดุเนื้อเดียวที่ทราบคำตอบ

## 5. Tests และการหักล้าง

ตรวจโพรงหาย การนับเนื้อซ้ำ วัสดุซ้อน พิกัด non-finite, hashes เก่า และ frame/unit invariance เอาโพรงออกแล้วมวลต้องไม่คงเป็นค่าเก่า

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อกสเกล feature และ tolerance ความยาว/ปริมาตร/มวล/inertia หลัง CAD pilot ที่เปิดเผย ก่อนกรณี admitted

positive invariants และ negative rejections ที่ตั้งใจต้องผ่านทั้งหมด ต้องรัน CAD-dependent tests จริง การ skip บล็อกการจบ adapter

## 7. สิ่งส่งมอบและงานรับต่อ

solids ที่ export, region manifest, ตารางเทียบ mass properties, mutation report และ replay identities

ส่ง spatial contract ที่เชื่อถือได้ให้ Works 109, 110 และ 112

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

junction เชื่อมมนอาจทำให้นับเนื้อซ้ำ ต้องกำหนดเจ้าของเนื้อชัด ไม่ fuse ลับ ไม่อ้าง feasibility โครงสร้างหรือรถทั้งคัน

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_spatial_material tests.test_repository_contract -v
python scripts/development/run_spatial_material.py --config config/development/spatial_material_v1.json --output-root artifacts/work108/run_a
python scripts/development/run_spatial_material.py --config config/development/spatial_material_v1.json --output-root artifacts/work108/run_b --replay-reference artifacts/work108/run_a/result.json
```
