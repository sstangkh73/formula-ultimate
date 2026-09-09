# Work 131: การวัดวัสดุและจุดเชื่อมเมื่อได้รับอนุญาต

ต้นฉบับภาษาอังกฤษ: `work131-physical_connection_correlation.md`

Status: Planned

หมายเลขเดิมใน Work 106: 130

พึ่งพา: Work 113, Work 116, Work 130

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

เทียบการวัดวัสดุ/จุดเชื่อมที่ปลอดภัยและได้รับอนุญาตกับคำทำนาย model ที่ล็อก พร้อมวัด discrepancy

ต้องมีอำนาจอนุญาตชัด สถานที่เหมาะสม qualified safety review, specimens ที่ตรวจ และเครื่องมือสอบเทียบก่อนทดสอบ

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/experiments/physical_connection_correlation.py`
- `config/development/physical_connection_correlation_v1.json`
- `scripts/development/run_physical_connection_correlation.py`
- `tests/test_physical_connection_correlation.py`

## 3. ขั้นลงมือทำ

1. เตรียม protocol ทดสอบขอบเขตจำกัด hazard review, stop conditions และ measurement uncertainty budget
2. ล็อกคำทำนายและ specimen/fixture identities แยก specimens/conditions สำหรับ calibration กับ validation
3. ให้ผู้ได้รับอนุญาตดำเนินการทดสอบที่อนุมัติ เก็บ raw observations โดยไม่แก้
4. วิเคราะห์ offline เทียบคำทำนาย และลงทะเบียนการปรับ model ก่อน validation ใหม่

## 4. การทดลอง

- IV: geometry specimen/joint, material batch และเงื่อนไขทดสอบจำกัดที่อนุมัติ
- DV: load/displacement/temperature ที่วัดหรือปริมาณอื่นที่อนุมัติ repeatability และ model discrepancy
- Controls: reference specimen, measurement chain สอบเทียบ, fixture compliance และบันทึกสิ่งแวดล้อม

## 5. Tests และการหักล้าง

analysis offline ปฏิเสธ calibration หาย specimen IDs สลับ sensor saturation และ raw data ถูกแก้ ทดสอบ stop logic โดยไม่จ่ายพลังงานให้อุปกรณ์อันตราย

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก safe bounds ที่ผู้มีความสามารถอนุมัติ sample design, measurement uncertainty และเกณฑ์ discrepancy ก่อนเก็บข้อมูล

ห้ามทดสอบจริงถ้าสิทธิ์เริ่มไม่ครบ การวัดใช้ได้รองรับเฉพาะขอบเขตที่ทดสอบ discrepancy ที่อธิบายไม่ได้บล็อก extrapolation

## 7. สิ่งส่งมอบและงานรับต่อ

approval references, specimen/measurement manifests, raw data, uncertainty และ correlation report; runner วิเคราะห์ offline เท่านั้น

ส่งขอบเขต material/joint ที่วัดจริงให้ subsystem Work 132

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

หยุดเมื่อไม่ปลอดภัยหรือขาดอนุญาต ไม่ควบคุมอุปกรณ์อัตโนมัติ ไม่ทดสอบทำลายไร้การกำกับ และไม่รับรองรถทั้งคัน

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_physical_connection_correlation tests.test_repository_contract -v
python scripts/development/run_physical_connection_correlation.py --config config/development/physical_connection_correlation_v1.json --output-root artifacts/work131/run_a
python scripts/development/run_physical_connection_correlation.py --config config/development/physical_connection_correlation_v1.json --output-root artifacts/work131/run_b --replay-reference artifacts/work131/run_a/result.json
```
