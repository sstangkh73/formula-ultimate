# Work 130: ส่งต่อการผลิต tolerance และการประกอบ

ต้นฉบับภาษาอังกฤษ: `work130-manufacturing_tolerance_handoff.md`

Status: Planned

หมายเลขเดิมใน Work 106: 129

พึ่งพา: Work 126, Work 129

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

ประเมินว่า candidate ละเอียดที่เลือกผลิต ประกอบ และตรวจได้ด้วยเส้นทางที่ประเมินชัดเจนหรือไม่

รายละเอียดสุดท้าย Work 126, margins สำคัญ Work 129 และข้อมูล material/process ที่ใช้ได้

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/assembly/manufacturing_tolerance_handoff.py`
- `config/development/manufacturing_tolerance_handoff_v1.json`
- `scripts/development/run_manufacturing_tolerance_handoff.py`
- `tests/test_manufacturing_tolerance_handoff.py`

## 3. ขั้นลงมือทำ

1. ผูกแต่ละ region/feature กับ process routes, สมมติฐานวัตถุดิบ และการเข้าตรวจ
2. ตรวจ tool access, โพรงปิดติดค้าง, ลำดับเชื่อม, การเข้าถึงจุดยึด และการเปลี่ยนเมื่อโจทย์ต้องการ
3. ส่งผ่าน tolerances ไปสู่ fit, preload, clearance และ margins ฟิสิกส์สำคัญ
4. ทำเอกสารส่งตรวจ/ประกอบ และส่ง redesign ที่จำเป็นกลับ revision candidate ใหม่

## 4. การทดลอง

- IV: process route, tolerance allocation, ลำดับประกอบ และ material variability
- DV: features ที่เข้าถึง/ผลิตได้ fit yield, margin sensitivity และช่องว่าง process unresolved
- Controls: ข้อกำหนดหน้าที่ candidate และระดับหลักฐานเดียวกันข้ามตัวเลือก process

## 5. Tests และการหักล้าง

จุดยึดเข้าไม่ถึง core ภายในติดค้าง ลำดับประกอบเป็นไปไม่ได้ และ clearance/preload สุดช่วง fit เฉพาะ nominal ไม่ผ่าน tolerance readiness

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก routes ที่ประเมิน หลักฐาน process capability, tolerances, uncertainty propagation และ inspection criteria

อ้าง readiness เฉพาะ routes ที่ผ่านพร้อมหลักฐาน access/tolerance ครบ เส้นทางไม่รองรับยัง unknown ไม่ใช่เป็นไปไม่ได้ทุกวิธี

## 7. สิ่งส่งมอบและงานรับต่อ

dossier ผลิต/ประกอบ tolerance map, inspection plan และรายการ redesign/blockers

กำหนด hardware และเงื่อนไขที่ทดสอบได้ให้ Work 131 หลังได้รับอนุญาตแยก

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

process capability ต้องมีหลักฐาน ไม่ใช้เกณฑ์ feature ต่ำสุดอย่างเดียว งานนี้ไม่อนุญาตซื้อ ผลิต หรือรับรองความปลอดภัย

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_manufacturing_tolerance_handoff tests.test_repository_contract -v
python scripts/development/run_manufacturing_tolerance_handoff.py --config config/development/manufacturing_tolerance_handoff_v1.json --output-root artifacts/work130/run_a
python scripts/development/run_manufacturing_tolerance_handoff.py --config config/development/manufacturing_tolerance_handoff_v1.json --output-root artifacts/work130/run_b --replay-reference artifacts/work130/run_a/result.json
```
