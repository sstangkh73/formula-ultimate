# Work 114: ชุดประกอบเคลื่อนที่และยืดหยุ่นที่มี contact

ต้นฉบับภาษาอังกฤษ: `work114-moving_contact_assembly.md`

Status: Planned

หมายเลขเดิมใน Work 106: 113

พึ่งพา: Work 113

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

สาธิตการเคลื่อนที่ที่ไม่ขัดกันและการส่งแรงในชุดประกอบละเอียดขนาดเล็ก รวมประวัติ contact

แบบ joint ละเอียด/ลดรูป Work 113 และ frames Work 112; เก็บความขัดกัน moving/rigid จาก Work 088 เป็น regression

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/assembly/moving_contact_assembly.py`
- `config/development/moving_contact_assembly_v1.json`
- `scripts/development/run_moving_contact_assembly.py`
- `tests/test_moving_contact_assembly.py`

## 3. ขั้นลงมือทำ

1. นิยาม generalized coordinates, constraints, initial conditions และ motion envelopes
2. เชื่อมสมาชิก rigid/flexible กับ joint จริง ติดตามประวัติ contact เปิด ปิด และลื่น
3. ตรวจ swept-volume collision และ clearance ตลอดการเคลื่อน ไม่ตรวจเฉพาะท่าแรก
4. เทียบคำตอบละเอียดกับลดรูปเมื่อ refine time step และกลับทิศ

## 4. การทดลอง

- IV: ตำแหน่ง joint, compliance, motion input, preload และ time step
- DV: constraint drift, แรง/โมเมนต์ส่งผ่าน, clearance, energy และ phase response
- Controls: geometry, initial energy และ boundary histories ที่ป้อนเหมือนกัน

## 5. Tests และการหักล้าง

free rigid motion, constraints ขัดกัน, coupling ถูกตัด, impact/reversal และออกนอกช่วงแบบลดรูป; หา reactions คืนไม่แต่งค่า

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก time-step ladder, contact event rules, clearance tolerance และ constraint/energy residuals ที่ยอมได้

motion cases ที่ลงทะเบียนผ่าน consistency/refinement gates; collisions หรือ joint ขัดกันบล็อกชุดนั้น ไม่บล็อก representation ทั้งหมด

## 7. สิ่งส่งมอบและงานรับต่อ

motion replay, swept-clearance report, contact histories, energy ledger และขอบเขตใช้

ส่งความสามารถชุดประกอบพลวัตให้ Works 117, 118 และ 119

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

contact แข็งกับ flexible modes อาจใช้สเกลเวลาต่างกัน ต้องแสดง coupling error ไม่อ้าง suspension ครบ crash หรือรถพร้อม

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_moving_contact_assembly tests.test_repository_contract -v
python scripts/development/run_moving_contact_assembly.py --config config/development/moving_contact_assembly_v1.json --output-root artifacts/work114/run_a
python scripts/development/run_moving_contact_assembly.py --config config/development/moving_contact_assembly_v1.json --output-root artifacts/work114/run_b --replay-reference artifacts/work114/run_a/result.json
```
