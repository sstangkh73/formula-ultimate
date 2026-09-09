# Work 116: ที่มาวัสดุและความเสียหายตามขอบเขต

ต้นฉบับภาษาอังกฤษ: `work116-material_failure_scope.md`

Status: Planned

หมายเลขเดิมใน Work 106: 115

พึ่งพา: Work 111, Work 114, Work 115

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

แทนสมมติฐานความแข็งแรง/การผลิตที่ไม่มีหลักฐานด้วยขอบเขตใช้ที่ย้อนที่มาได้และ failure models ที่เลือกตรวจ

geometry/field histories จากงานก่อน; หลักฐาน material/process ของ candidate แยก synthetic fixtures จาก measured data ชัดเจน

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/structural/material_failure_scope.py`
- `config/development/material_failure_scope_v1.json`
- `scripts/development/run_material_failure_scope.py`
- `tests/test_material_failure_scope.py`

## 3. ขั้นลงมือทำ

1. บันทึกที่มาวัสดุ units, ช่วง temperature/rate/history, uncertainty และผลจาก process
2. พัฒนา eligibility หลักฐานและ domain checks ก่อนเลือก constitutive/failure laws
3. ตรวจ yielding/buckling models แรกที่ใช้ได้กับ reference พร้อมความไวต่อ imperfection
4. เตรียมส่วนขยาย fatigue, fracture และ wear แยก รับเฉพาะโดเมนที่มี tests/ข้อมูลรองรับ

## 4. การทดลอง

- IV: วัสดุ/process, temperature, loading history และ geometric imperfections
- DV: failure margins, uncertainty, sensitivity และ coverage ขอบเขตหลักฐาน
- Controls: geometry/load history เดียวกันและ reference materials อิสระ

## 5. Tests และการหักล้าง

ปฏิเสธคุณสมบัตินอกช่วง หน่วยหาย วัสดุผสมไร้เหตุ และการเปลี่ยนป้าย synthetic เป็น measured มี fixtures ที่ทราบว่าปลอดภัยใน elastic และล้มเหลว

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อกแหล่งข้อมูลที่รับได้ วิธีจัด uncertainty สมมติฐาน constitutive และ failure criteria ที่เลือก

กฎ failure ที่พัฒนาผ่าน references และ applicability checks; โดเมนขาดคงเป็น blocker ต่อคำอ้างที่ต้องใช้

## 7. สิ่งส่งมอบและงานรับต่อ

registry หลักฐาน material/process, law verification, uncertainty ranges และรายงานโดเมนขาดราย candidate

ส่งขอบเขต material/failure ที่รับได้ให้ทุก subsystem และ manufacturing Work 130

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

fatigue/fracture สากลเกินหนึ่งงาน ต้องแยกตามกฎ/โดเมนข้อมูล registry coverage เสร็จไม่ได้แปลว่าพิสูจน์รอดทางกายภาพครบ

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_material_failure_scope tests.test_repository_contract -v
python scripts/development/run_material_failure_scope.py --config config/development/material_failure_scope_v1.json --output-root artifacts/work116/run_a
python scripts/development/run_material_failure_scope.py --config config/development/material_failure_scope_v1.json --output-root artifacts/work116/run_b --replay-reference artifacts/work116/run_a/result.json
```
