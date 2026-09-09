# Work 115: ความร้อนตามเวลาเชื่อมกับของแข็ง

ต้นฉบับภาษาอังกฤษ: `work115-coupled_thermal_solid.md`

Status: Planned

หมายเลขเดิมใน Work 106: 114

พึ่งพา: Work 111, Work 113

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

ให้ความร้อน อุณหภูมิ การเสียรูป และ preload joint ส่งผลต่อกันจริงบน geometry ละเอียดเดียวกัน

fields Work 111, joints Work 113, บริเวณวัสดุร่วม และคุณสมบัติ/แหล่งความร้อนที่ประกาศ

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/physics/coupled_thermal_solid.py`
- `config/development/coupled_thermal_solid_v1.json`
- `scripts/development/run_coupled_thermal_solid.py`
- `tests/test_coupled_thermal_solid.py`

## 3. ขั้นลงมือทำ

1. สร้างบริเวณ thermal mesh, heat sources และ boundary/contact conductances จาก geometry/กฎที่ประกาศ
2. แก้ heat balance ตามเวลาด้วยพื้นที่ interface และความจุความร้อนวัสดุจริง
3. ส่งอุณหภูมิไปสู่การขยายตัว/วัสดุ แล้วส่งการเปลี่ยนที่ขึ้นกับ geometry/contact กลับ
4. เทียบแบบ coupled, decoupled และลดรูป ทำให้แบบลดรูปหมดอายุเมื่อออกนอกช่วง

## 4. การทดลอง

- IV: heat input, cooling boundary, contact state, คุณสมบัติขึ้นกับอุณหภูมิ และ coupling step
- DV: temperature, heat residual, expansion, preload shift และ coupling/reduction error
- Controls: geometry, thermal state เริ่มต้นและ energy input เดียวกัน; control decoupled ระบุแยก

## 5. Tests และการหักล้าง

พลังงานเพิ่มในระบบฉนวน สมดุลเมื่อไม่มี source การขยายอิสระเทียบถูกยึด ตัด heat path และเปลี่ยนพื้นที่ interface

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก spatial/time refinement, heat/contact laws, property range และ thermal/mechanical error tolerances

ผ่าน heat balance และการทดสอบ coupling ทั้งสองทาง แค่แก้ heat/load แยกกันไม่ถือว่าผ่าน

## 7. สิ่งส่งมอบและงานรับต่อ

ประวัติ temperature/deformation, interface heat transfers, preload response, convergence และขอบเขตแบบลดรูป

ส่งให้ขีดจำกัดวัสดุ Work 116, co-design Work 117 และ cooling Work 121

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

contact conductance ที่ยังไม่วัดต้องคง uncertainty ไม่อ้าง convection, radiation หรือของไหลที่ตรวจแล้วถ้ายังไม่พัฒนาและทดสอบแยก

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_coupled_thermal_solid tests.test_repository_contract -v
python scripts/development/run_coupled_thermal_solid.py --config config/development/coupled_thermal_solid_v1.json --output-root artifacts/work115/run_a
python scripts/development/run_coupled_thermal_solid.py --config config/development/coupled_thermal_solid_v1.json --output-root artifacts/work115/run_b --replay-reference artifacts/work115/run_a/result.json
```
