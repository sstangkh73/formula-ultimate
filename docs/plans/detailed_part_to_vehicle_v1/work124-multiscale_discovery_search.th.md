# Work 124: การค้นพบหลายสเกลและบัญชีต้นทุนเป็นธรรม

ต้นฉบับภาษาอังกฤษ: `work124-multiscale_discovery_search.md`

Status: Planned

หมายเลขเดิมใน Work 106: 123

พึ่งพา: Work 109, Work 117, Work 123

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

ค้นหา geometry, topology, materials, interfaces และ controller ร่วมกัน พร้อมการตัดสินย้อนที่มาได้และโอกาสคำนวณเท่ากัน

generator Work 109 และ feedback Work 117; เริ่มโหมดย่อยก่อนโหมดรถ Work 123 ได้ ตรวจสมมติฐาน intake/accounting เดิมก่อน admission

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/search/multiscale_discovery_search.py`
- `config/development/multiscale_discovery_search_v1.json`
- `scripts/development/run_multiscale_discovery_search.py`
- `tests/test_multiscale_discovery_search.py`

## 3. ขั้นลงมือทำ

1. นิยาม archives แบบ feasible/near-feasible/unresolved ตามขอบเขต และ descriptors shape/function ที่มีเหตุจริง
2. จองทรัพยากรก่อนเรียก CAD/mesh/solver/tuning ทุกครั้ง คิดต้นทุน failures, retries และ audits
3. ตรวจ source/admission provenance ทั้งหมด แยก exact decisions จาก numerical replay
4. จัด representation audits ไม่ขึ้นกับคะแนน และ refinement/promotion ตามงบคำนวณ

## 4. การทดลอง

- IV: นโยบาย search/representation, fidelity allocation, archive strategy และ coupling mode
- DV: utility/diversity ที่ตรวจแล้ว time-to-evidence, false-negative audits และทรัพยากรรวม
- Controls: external task, โอกาส library, seed pairing, hardware และงบครบเท่ากัน

## 5. Tests และการหักล้าง

งบหมดก่อน execute, attempts ล้มเหลว, cache หมดอายุ, admission summary ถูกแก้, ส่วนยื่นไม่ทำงาน และรูปทรงมีประโยชน์ topology เดิม

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อกส่วนแบ่งงบทั้งหมด หน่วย accounting, escalation rules, signed effect ที่มีความหมาย และวิธีเทียบ uncertainty

ผ่าน accounting/provenance/replay; counters ไม่ทราบไม่ใช่ศูนย์ shape ต่อเนื่องที่ดีขึ้นมีสิทธิ์โดยไม่ต้องกราฟใหม่

## 7. สิ่งส่งมอบและงานรับต่อ

search ancestry, budget ledger ที่ลงทะเบียน, archives, audit samples และรายงาน signed benefit/uncertainty

ส่ง engine ทดลอง admitted ให้ Works 125 และ 127

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

ไม่บังคับ optimizer หรือ representation เดียว จำกัดการเรียก identity/solver ที่แพงและแสดงข้อเสนอ not-evaluated ไม่อ้างความใหม่จาก diversity อย่างเดียว

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_multiscale_discovery_search tests.test_repository_contract -v
python scripts/development/run_multiscale_discovery_search.py --config config/development/multiscale_discovery_search_v1.json --output-root artifacts/work124/run_a
python scripts/development/run_multiscale_discovery_search.py --config config/development/multiscale_discovery_search_v1.json --output-root artifacts/work124/run_b --replay-reference artifacts/work124/run_a/result.json
```
