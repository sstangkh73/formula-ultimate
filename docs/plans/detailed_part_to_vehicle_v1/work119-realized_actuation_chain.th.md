# Work 119: ชุดส่งกำลังและ actuation ที่มีฮาร์ดแวร์จริง

ต้นฉบับภาษาอังกฤษ: `work119-realized_actuation_chain.md`

Status: Planned

หมายเลขเดิมใน Work 106: 118

พึ่งพา: Work 114, Work 115, Work 116

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

เปลี่ยนคำสั่งกำลัง/motion ให้เป็นเส้นทางฮาร์ดแวร์ละเอียดที่รองรับได้ พร้อม reactions และ losses จริง

แบบ interface, moving contact, thermal และ material; เลือก reference route ที่ทำไหวและเปิดเผย ไม่ใช่ whitelist เทคโนโลยีถาวร

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/subsystems/realized_actuation_chain.py`
- `config/development/realized_actuation_chain_v1.json`
- `scripts/development/run_realized_actuation_chain.py`
- `tests/test_realized_actuation_chain.py`

## 3. ขั้นลงมือทำ

1. ล็อก input/output ports และ rate/load envelope เลือกเฉพาะ conversion laws ที่รองรับ
2. สร้างสมาชิกถ่ายกำลังภายใน interfaces, supports และ containment geometry ที่จำเป็น
3. หา stiffness, losses, reaction loads และภาระความร้อนจากเส้นทางที่ทำจริง
4. ตรวจ response map ที่มีขอบเขต และเปิด extension interfaces สำหรับวิธีอื่น

## 4. การทดลอง

- IV: geometry ส่งกำลัง การจัด interface, speed/load และ temperature
- DV: งาน/torque/force ออก, loss, capacity, mass และ support reactions
- Controls: port task, วัสดุที่อนุญาต และ energy input เดียวกัน; การจัด reference ที่ปรับดี

## 5. Tests และการหักล้าง

ตัด power path, ล็อก output, กลับการทำงาน, สั่งเกินขีดจำกัด และเอา supports ออก ตรวจปลายทางพลังงานทุกกรณี

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อกสมมติฐาน conversion, load/speed/temperature envelope, loss/error tolerances และ hardware coverage

ทุก action ที่อ้างมี geometry/material รองรับและบัญชีที่ตรวจแล้ว torque อุดมคติที่ไร้ฮาร์ดแวร์อธิบายผ่านไม่ได้

## 7. สิ่งส่งมอบและงานรับต่อ

CAD ภายใน physical path graph, response/loss maps, support/thermal loads และ validation report

ส่งให้พลังงาน Work 120, controller hardware Work 122 และ transient integration Work 123

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

ฟิสิกส์แปลงพลังงานใหม่อาจเกิน package ต้องแยก law verification ก่อน admission ไม่บังคับเฟือง เพลา หรือ motor แบบใด

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_realized_actuation_chain tests.test_repository_contract -v
python scripts/development/run_realized_actuation_chain.py --config config/development/realized_actuation_chain_v1.json --output-root artifacts/work119/run_a
python scripts/development/run_realized_actuation_chain.py --config config/development/realized_actuation_chain_v1.json --output-root artifacts/work119/run_b --replay-reference artifacts/work119/run_a/result.json
```
