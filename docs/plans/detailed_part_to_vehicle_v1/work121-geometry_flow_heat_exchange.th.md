# Work 121: การไหลและแลกเปลี่ยนความร้อนจาก geometry

ต้นฉบับภาษาอังกฤษ: `work121-geometry_flow_heat_exchange.md`

Status: Planned

หมายเลขเดิมใน Work 106: 120

พึ่งพา: Work 110, Work 115, Work 116

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

ให้ทางไหลภายในและพื้นผิวส่งผลจริงต่อ pressure loss, heat transfer และ aerodynamic loads ภายนอก

geometry meshes Work 110, heat sources Work 115 และขอบเขตวัสดุ/ข้อมูล การไหลภายในกับภายนอกต้องตรวจแยกขอบเขต

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/physics/geometry_flow_heat_exchange.py`
- `config/development/geometry_flow_heat_exchange_v1.json`
- `scripts/development/run_geometry_flow_heat_exchange.py`
- `tests/test_geometry_flow_heat_exchange.py`

## 3. ขั้นลงมือทำ

1. แยก solid/fluid domains และขอบเขต inlet/outlet/wall/far-field ทางกายภาพ
2. ตรวจกรณี heat/pressure ทางไหลภายในก่อนใช้ geometry ระบายความร้อนทั่วไป
3. สร้าง external-flow adapter พร้อม reference อิสระที่ตรวจแล้วและ flow regime ที่ประกาศ
4. ส่ง wall heat/pressure/shear loads กลับชุด coupled และเทียบ geometry mutations

## 4. การทดลอง

- IV: ทางเดิน passage, surface shape, flow demand, speed และสมมติฐานขอบเขต
- DV: pressure drop, heat rejected, pumping power, aerodynamic forces/moments และ error
- Controls: source heat, ambient state, สภาวะทำงาน และ reference task เดียวกัน

## 5. Tests และการหักล้าง

อุด passage, ขีดจำกัด flow/source ศูนย์, เปลี่ยน surface/cavity, ความไวขนาดโดเมน และ conservation; refine wall/mesh/time เมื่อเกี่ยวข้อง

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก flow regime, สมมติฐาน constitutive/closure, boundary domain, refinement schedule และ errors ที่รับได้

flow scope ที่ admitted แต่ละอันผ่าน reference/convergence ของตน internal-flow สำเร็จไม่ได้ยืนยัน aerodynamics รถทั้งคัน

## 7. สิ่งส่งมอบและงานรับต่อ

fluid/solid meshes, fields, heat/pressure loads, power costs และรายงาน coverage ราย regime

ส่งให้ transient coupling Work 123 และการชั่งประโยชน์รถ Work 127

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

มีสอง solver scopes ขนาดใหญ่ แยกงานภายใน/ภายนอกเมื่อจำเป็น ไม่อ้าง turbulence, cavitation หรือ compressibility ทั่วไปจาก benchmark เดียว

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_geometry_flow_heat_exchange tests.test_repository_contract -v
python scripts/development/run_geometry_flow_heat_exchange.py --config config/development/geometry_flow_heat_exchange_v1.json --output-root artifacts/work121/run_a
python scripts/development/run_geometry_flow_heat_exchange.py --config config/development/geometry_flow_heat_exchange_v1.json --output-root artifacts/work121/run_b --replay-reference artifacts/work121/run_a/result.json
```
