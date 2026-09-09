# Work 113: พิสูจน์การยึดและ contact แบบละเอียด

ต้นฉบับภาษาอังกฤษ: `work113-detailed_connection_contact.md`

Status: Planned

หมายเลขเดิมใน Work 106: 112

พึ่งพา: Work 111, Work 112

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

สร้างจุดเชื่อมที่เกิดจริงละเอียดถึงสเกลการยึด เทียบ reference เกลียวกับวิธีเชื่อมทางเลือกที่สร้างอิสระ

ข้อมูลเข้า: vector solid solver, physical interfaces และโจทย์จุดเชื่อมที่ล็อก ใช้ geometry ขบจริงสำหรับวิธีที่เลือก

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/structural/detailed_connection_contact.py`
- `config/development/detailed_connection_contact_v1.json`
- `scripts/development/run_detailed_connection_contact.py`
- `tests/test_detailed_connection_contact.py`

## 3. ขั้นลงมือทำ

1. ล็อก terminal loads, motion ที่ยอมได้, envelope, สมมติฐานอุณหภูมิ และข้อกำหนดการยึด
2. สร้าง geometry คู่ประกบ clearance และผิวรองรับ แก้ราก/แนวเกลียวเมื่อเลือกเกลียว
3. พัฒนา contact/preload เริ่มต้น การหา reactions และการสังเกต separation/slip
4. สร้างแบบลดรูป joint ในช่วง load/preload จำกัด และเทียบกับคำตอบละเอียด

## 4. การทดลอง

- IV: geometry การยึด ระยะขบ preload, friction และโหลดเยื้องแกน
- DV: stiffness, slip/opening, stress quantities, แรง/โมเมนต์ส่งผ่าน และ reduction error
- Controls: โจทย์เชื่อมและสมมติฐานวัสดุเดียวกัน reference เกลียวที่ตรวจแล้วโดยไม่บังคับคำตอบต้องมีเกลียว

## 5. Tests และการหักล้าง

เอาจุดเชื่อมออก/ตัด กลับโหลด เปลี่ยน clearance และลดระยะขบ ทดสอบ contact inequality/friction limits และ refinement เฉพาะที่ ไม่เติม support ช่วยสมมติ

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก contact law, friction uncertainty, ช่วง preload, local mesh levels และ reduction error ที่รับได้

ผ่าน reference verification และ causal load-transfer tests ในขอบเขต การคลายตัว/fatigue ที่ไม่รองรับคง unresolved ทางเลือกที่ล้มเหลวเป็นผลลบที่ยอมรับได้

## 7. สิ่งส่งมอบและงานรับต่อ

CAD joint ละเอียด หน้าตัด contact fields, preload state, convergence และ manifest ขอบเขตแบบลดรูป

ส่งให้ชุดเคลื่อนที่ Work 114 และ thermo-mechanical tests Work 115

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

nonlinear contact อาจต้องงานแยก แบ่งการตรวจ solver จาก discovery เมื่อจำเป็น ไม่บังคับมาตรฐานน็อตสากลหรือรับรอง fatigue-life/ความปลอดภัย

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_detailed_connection_contact tests.test_repository_contract -v
python scripts/development/run_detailed_connection_contact.py --config config/development/detailed_connection_contact_v1.json --output-root artifacts/work113/run_a
python scripts/development/run_detailed_connection_contact.py --config config/development/detailed_connection_contact_v1.json --output-root artifacts/work113/run_b --replay-reference artifacts/work113/run_a/result.json
```
