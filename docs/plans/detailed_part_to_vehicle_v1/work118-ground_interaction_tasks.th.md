# Work 118: ปฏิสัมพันธ์พื้น การหยุด และควบคุมทิศทาง

ต้นฉบับภาษาอังกฤษ: `work118-ground_interaction_tasks.md`

Status: Planned

หมายเลขเดิมใน Work 106: 117

พึ่งพา: Work 114, Work 116

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

ประเมินปฏิสัมพันธ์พื้นและหน้าที่เคลื่อนที่ที่ต้องมี โดยไม่กำหนดโครงสร้างล้อหรือการเลี้ยวตายตัว

แบบ moving/contact และขอบเขตวัสดุ ล็อกพื้นผิว/สิ่งแวดล้อมภายนอกในแต่ละ comparison

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/simulation/ground_interaction_tasks.py`
- `config/development/ground_interaction_tasks_v1.json`
- `scripts/development/run_ground_interaction_tasks.py`
- `tests/test_ground_interaction_tasks.py`

## 3. ขั้นลงมือทำ

1. นิยาม ground-contact ports, คุณสมบัติพื้น และ sign conventions แรง/โมเมนต์
2. พัฒนาเส้นทาง contact/friction ที่มีขอบเขตและผ่านการตรวจ พร้อม applicability ชัด
3. ประเมินแรงปฏิกิริยาขับเคลื่อน เปลี่ยนทิศ และหยุด พร้อมบันทึกกำลัง dissipated ทั้งหมด
4. ลองตำแหน่ง/geometry contact ต่างกัน และส่งโหลดกลับแบบชิ้นส่วน

## 4. การทดลอง

- IV: geometry/ตำแหน่ง contact, สภาพพื้น, slip state และคำสั่ง motion
- DV: traction, ระยะ/เวลาหยุด, การตอบสนองทิศทาง, loss และ contact stability
- Controls: เส้นทางภายนอก initial state, surface และโอกาสพลังงานเดียวกัน

## 5. Tests และการหักล้าง

ขีดจำกัด friction ศูนย์ ยกพ้นพื้น กลับทิศ saturation และ actuation ถูกตัด ห้ามมีแรงพื้นเมื่อไม่มีปฏิสัมพันธ์ที่อนุญาต

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อกข้อมูล/ช่วง surface, contact resolution, force/loss errors และเกณฑ์ numerical stability

ผ่านพฤติกรรม reference และ conservation/refinement checks; พฤติกรรมยางหรือแบบไม่ใช้ยางที่ไม่รองรับคง unresolved ไม่เติม coefficient ทั่วไป

## 7. สิ่งส่งมอบและงานรับต่อ

ประวัติ contact/motion, force/loss maps, stopping/direction tests และขอบเขต coverage

ส่งให้ whole-candidate transient Work 123 และชุดละเอียด Work 126

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

กฎ friction ง่ายไม่ได้ยืนยันยาง ดินอ่อน หรือ locomotion ทุกแบบ ต้องแยกโดเมนใหม่เป็น adapters ที่ตรวจแล้ว ไม่ตั้งกฎจำนวนล้อ

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_ground_interaction_tasks tests.test_repository_contract -v
python scripts/development/run_ground_interaction_tasks.py --config config/development/ground_interaction_tasks_v1.json --output-root artifacts/work118/run_a
python scripts/development/run_ground_interaction_tasks.py --config config/development/ground_interaction_tasks_v1.json --output-root artifacts/work118/run_b --replay-reference artifacts/work118/run_a/result.json
```
