# Work 126: candidate ดิจิทัลละเอียดครบทั้งคัน

ต้นฉบับภาษาอังกฤษ: `work126-detailed_vehicle_closure.md`

Status: Planned

หมายเลขเดิมใน Work 106: 125

พึ่งพา: Work 118, Work 119, Work 120, Work 121, Work 122, Work 123, Work 124, Work 125

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

ทำทุกหน้าที่ทางกายภาพและเส้นทางฮาร์ดแวร์ภายในที่จำเป็นให้เกิดจริงในชุด candidate ทั้งคันที่ตรวจได้

แบบ subsystem ที่ใช้ได้ หลักฐานย่อย Work 125 และสถาปัตยกรรมสำรวจ ไม่บังคับทุกชิ้นชนะเมื่อแยกเดี่ยว

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/assembly/detailed_vehicle_closure.py`
- `config/development/detailed_vehicle_closure_v1.json`
- `scripts/development/run_detailed_vehicle_closure.py`
- `tests/test_detailed_vehicle_closure.py`

## 3. ขั้นลงมือทำ

1. ไล่หน้าที่ภายนอกถึงบริเวณวัสดุ hardware ภายใน และ interfaces ทำรายการช่องว่าง unresolved ทั้งหมด
2. สร้าง/วางชิ้นส่วนและจุดเชื่อมละเอียด เปิดให้บริเวณหลายหน้าที่และเปลี่ยนสถาปัตยกรรม
3. ทำบัญชี mass/inertia, occupied volume, energy, signal, heat และ load paths ให้ครบ
4. ตรวจชุดประกอบและ swept motion แล้วรันหลักฐานย่อย/coupled ที่กระทบบน revision สุดท้าย

## 4. การทดลอง

- IV: ตำแหน่ง part, วิธีเชื่อม, architecture และ tolerance state
- DV: hardware coverage, overlap/clearance, mass ครบ, motion compatibility และช่องว่างโดเมนจำเป็น
- Controls: หน้าที่/task ภายนอกเดียวกันและการเป็นเจ้าของเนื้อวัสดุต้นทางเดียวกัน

## 5. Tests และการหักล้าง

เอา fastener/support/seal/signal path ที่จำเป็นออก ตรวจโพรงแฝง มวลซ้ำ interference และ subsystem envelopes เก่า

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก completeness checklist, geometry-detail level G3, functional coverage, tolerance และ collision/motion gates

geometry/hardware paths จำเป็นครบและตรวจ revision สุดท้ายได้ ถ้าฟิสิกส์สำคัญขาดให้เป็น detailed exploratory candidate ไม่ใช่ promotion-ready

## 7. สิ่งส่งมอบและงานรับต่อ

CAD ทั้งชุด/รายชิ้น ภาพแยก/หน้าตัด บัญชีบริเวณ ลำดับประกอบ closure matrix และ unresolved list

ส่ง candidate identities ที่แน่นอนให้ Works 127–130

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

ห้ามใช้ geometry Work 088 ที่ถูกบล็อกโดยไม่มีหลักฐานใหม่ G3 ละเอียดไม่ใช่ physical validation ชิ้นซื้อมีที่มาและไม่นับเป็นสิ่งค้นพบที่สร้างเอง

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_detailed_vehicle_closure tests.test_repository_contract -v
python scripts/development/run_detailed_vehicle_closure.py --config config/development/detailed_vehicle_closure_v1.json --output-root artifacts/work126/run_a
python scripts/development/run_detailed_vehicle_closure.py --config config/development/detailed_vehicle_closure_v1.json --output-root artifacts/work126/run_b --replay-reference artifacts/work126/run_a/result.json
```
