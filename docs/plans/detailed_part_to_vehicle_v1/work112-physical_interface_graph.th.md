# Work 112: terminals ทางกายภาพและความหมายการประกอบ

ต้นฉบับภาษาอังกฤษ: `work112-physical_interface_graph.md`

Status: Planned

หมายเลขเดิมใน Work 106: 111

พึ่งพา: Work 108

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

แทนรอยต่อแรง motion, thermal และโดเมนที่ประกาศจริง โดยไม่ทำทางขนานหายหรือบังคับบทบาทชิ้นส่วนแบบเดิม

ใช้บริเวณจาก Work 108 และข้อจำกัด simple-graph ไม่แยกชนิดจาก Work 105

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/assembly/physical_interface_graph.py`
- `config/development/physical_interface_graph_v1.json`
- `scripts/development/run_physical_interface_graph.py`
- `tests/test_physical_interface_graph.py`

## 3. ขั้นลงมือทำ

1. นิยาม terminal frames, spatial regions, units, domain variables และ sign conventions
2. แทน multiedges มีชนิด การเคลื่อนที่ที่ยอมได้ และ constitutive-law references
3. พัฒนา identity ที่ไม่เปลี่ยนตามชื่อ โดยไม่ทิ้งบทบาท ทิศทาง หรือจำนวนทางซ้ำ
4. ถ่าย interface ผ่าน geometry split/merge และแจ้งหลักฐานที่ต้องหมดอายุ

## 4. การทดลอง

- IV: บทบาท terminal, orientation, multiplicity, การจัดกลุ่ม part และ split/merge
- DV: connectivity, interface compatibility, การแลกเปลี่ยนที่อนุรักษ์ และ identity stability
- Controls: geometry และปฏิสัมพันธ์เทียบเท่าเมื่อเปลี่ยนเฉพาะ identifier

## 5. Tests และการหักล้าง

เปลี่ยนชื่อต้องรักษาความหมาย แต่สลับ source/sink หรือลบทางขนานไม่จำเป็นต้องเหมือนเดิม ปฏิเสธหน่วยขัดกัน ผิวคู่ประกบหาย และ rigid/moving conflicts

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก interface laws ที่รองรับ frame tolerances, identity limits และกฎ compatibility

ผ่าน fixtures ทั้งที่ต้องเหมือนและต้องต่าง ทางขาดต้องยังขาด identity เป็นตัวบรรยาย ไม่ใช่หลักฐานกลไกเพียงอย่างเดียว

## 7. สิ่งส่งมอบและงานรับต่อ

interface schema, semantic graph corpus, region bindings และรายงาน compatibility/identity

ส่งให้จุดเชื่อม Work 113 และการสร้างโจทย์สองทาง Work 117

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

canonicalization อาจแพงเมื่อกราฟโต จำกัด runtime และเก็บ identity unresolved โดยไม่ห้าม geometry ไม่อ้างค้นพบกลไกทั่วไป

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_physical_interface_graph tests.test_repository_contract -v
python scripts/development/run_physical_interface_graph.py --config config/development/physical_interface_graph_v1.json --output-root artifacts/work112/run_a
python scripts/development/run_physical_interface_graph.py --config config/development/physical_interface_graph_v1.json --output-root artifacts/work112/run_b --replay-reference artifacts/work112/run_a/result.json
```
