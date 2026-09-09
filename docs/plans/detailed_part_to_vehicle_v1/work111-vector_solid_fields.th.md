# Work 111: สนามของแข็งแบบ vector จาก geometry ที่สร้าง

ต้นฉบับภาษาอังกฤษ: `work111-vector_solid_fields.md`

Status: Planned

หมายเลขเดิมใน Work 106: 110

พึ่งพา: Work 110

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

เพิ่มความสามารถ vector solid mechanics ที่ระบุขอบเขตบน mesh candidate จริง แทนการใช้หลักฐาน scalar-member สำหรับคำอ้างนี้

ข้อมูลเข้า: meshes และ semantic supports Work 110; วัสดุ elastic สำหรับ fixture ที่ประกาศ ไม่ใช่ข้อมูลผลิตรับรอง

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/structural/vector_solid_fields.py`
- `config/development/vector_solid_fields_v1.json`
- `scripts/development/run_vector_solid_fields.py`
- `tests/test_vector_solid_fields.py`

## 3. ขั้นลงมือทำ

1. นิยาม displacement, traction, body-force และ support conventions ในกรอบ SI
2. พัฒนา/ต่อ linear elastic vector solve และหา reactions คืนจากระบบที่ประกอบ
3. คำนวณ quantities of interest ที่ประกาศ strain energy, สมดุลแรง/โมเมนต์ และ conditioning
4. รัน reference และรูปทรงไม่คุ้นเคยหลาย refinement levels เทียบ formulations อิสระ

## 4. การทดลอง

- IV: geometry ขอบเขต ทิศแรง material stiffness และ refinement
- DV: displacement, compliance, stress quantities, reaction residuals และ discretization error
- Controls: นิยามแรง/support ทางกายภาพและ geometry เดียวกันเมื่อเทียบ solvers

## 5. Tests และการหักล้าง

rigid translation/rotation, patch test, แรงนอกแกน, rigid modes ที่ไร้ support, ตัดทางแรง และ stiffness เสีย ตรวจว่า reactions ไม่ได้กำหนดให้เท่า input

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อกสมมติฐานวัสดุ schedule 3 ระดับ residual/error tolerances และ stress quantities ที่ไม่เอกฐาน

ผ่าน reference และ convergence gates; geometry mutations ทำให้ vector fields เปลี่ยนซ้ำได้ กรณีไม่ converge หรือ singular เป็น survivor ไม่ได้

## 7. สิ่งส่งมอบและงานรับต่อ

displacement/stress fields, recovered reactions, ตาราง energy, convergence และการเทียบ independent reference

เปิดทางจุดเชื่อมละเอียด Work 113, thermal coupling Work 115 และ failure scope Work 116

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

point stress มุมคมอาจไม่ converge ต้องระบุวิธีจัด geometry/quantity ที่มีเหตุผลให้เห็น ไม่อ้าง nonlinear contact, fatigue หรือ physical validation

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_vector_solid_fields tests.test_repository_contract -v
python scripts/development/run_vector_solid_fields.py --config config/development/vector_solid_fields_v1.json --output-root artifacts/work111/run_a
python scripts/development/run_vector_solid_fields.py --config config/development/vector_solid_fields_v1.json --output-root artifacts/work111/run_b --replay-reference artifacts/work111/run_a/result.json
```
