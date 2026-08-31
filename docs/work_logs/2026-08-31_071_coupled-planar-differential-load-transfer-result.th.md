# ผล Work 071: การเชื่อมแบบจำลองระนาบ ดิฟเฟอเรนเชียล และการถ่ายน้ำหนักราย Step

สถานะ: เสร็จสมบูรณ์

ต้นฉบับภาษาอังกฤษ: `2026-08-31_071_coupled-planar-differential-load-transfer-result.md`

## ผลลัพธ์

รถระนาบแบบสามจุดสัมผัสจาก Work 069 และดิฟเฟอเรนเชียลล้ออิสระจาก Work 070 ทำงานร่วมกันใน loop ระดับ Level 0 แบบ deterministic แล้ว แต่ละ step ที่รับได้เชื่อมการกระจายแรงกดปกติ wheel slip ตามยาว slip angle ด้านข้าง combined tyre-force projection โหลด powertrain การเคลื่อนโหมดดิฟเฟอเรนเชียล การเคลื่อนที่ตัวรถ yaw งาน ความร้อน และพลังงานรวม reference และตัวควบคุมผ่าน gate ที่ประกาศไว้ ส่วนมุมเลี้ยวมากโดยเจตนาจบด้วย `contact_lift` DNF ที่สังเกตได้

ผลนี้เป็นหลักฐานความเป็นไปได้ของการเชื่อม software เท่านั้น ไม่ใช่การยืนยันทางกายภาพหรือความพร้อมแข่งขัน

## ไฟล์ที่เปลี่ยน

- `config/vehicle/coupled_planar_differential_v1.json`
- `src/formula_ultimate/simulation/coupled_planar_differential.py`
- `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_coupled_planar_differential.py`
- `tests/test_coupled_planar_differential.py`
- `docs/research/COUPLED_PLANAR_DIFFERENTIAL_LOAD_TRANSFER_V1.md`
- `docs/research/COUPLED_PLANAR_DIFFERENTIAL_LOAD_TRANSFER_V1.th.md`
- ชุด plan/result สองภาษาของงานนี้

หลักฐาน deterministic ที่ ignore โดย Git ถูกสร้างใหม่ใน `artifacts/work071/`

## การตัดสินใจและหลักฐานการทำงาน

- คง geometry ที่ materialize จาก Work 069 v3 โดยไม่เปลี่ยน มี SHA-256 `cf78a1c499790aed6c8b117c8f583a427a9d91a9fb36605e2b7038b2907b1418`
- ใช้จุดสัมผัสหน้าสองจุดเป็น branch ที่ขับเคลื่อน/เลี้ยว และคงจุดรองรับหลังเป็น passive สำหรับแรงขับ
- แก้แรงกดปกติแบบ quasi-static ที่ขึ้นกับความเร่งภายใน fixed-point loop ของทุก step โหลดค่าลบยังมองเห็นและเป็น terminal โดยห้าม clipping
- ฉายแรงร้องขอตามยาวและด้านข้างพร้อมกันผ่าน friction ellipse และเก็บ saturation/แรงที่ให้ไม่ได้ไว้
- ใช้การ integrate ตัวรถและดิฟเฟอเรนเชียลที่สอดคล้องกับ midpoint เพื่อให้ Coriolis exchange และ modal damping ปิดในบัญชีพลังงาน
- จับคู่ความเร็วล้อ/carrier/converter ตอนเริ่มกับ `10 m/s` และหักพลังงานจลน์ของตัวรถกับชุดหมุนออกจาก storage ทำให้พลังงานรวมเริ่มต้นเท่ากับ `50,000,000 J` พอดีโดยไม่สร้างพลังงานแฝง
- การไม่ converge, ค่าที่ไม่ finite, contact lift, limit failure และ energy failure ยังคง explicit และ fail closed

## ผลการทดลอง

คำสั่ง reference: มุมเลี้ยว `+0.01 rad`, throttle `0.3`, ระยะเวลา `0.5 s`, `dt = 0.001 s`

- สถานะ/ผลลัพธ์: `passed/finished`, 500 steps
- ตำแหน่งสุดท้าย: `(5.370504659073167, 0.1338516705920943) m`
- heading/yaw rate สุดท้าย: `0.09777375911939074 rad`, `0.3638034159613838 rad/s`
- ความเร็ว branch สุดท้าย: ซ้าย `95.16937580718059 rad/s`, ขวา `83.57249258481846 rad/s`
- แรงกดปกติต่ำสุด: `282.9427858151486 N`
- combined contact utilization สูงสุด: `1.0000000000000002`
- จำนวน step ที่ saturation: `302`
- absolute residual ดุลแรงกดสูงสุด: `4.547473508864641e-13`
- body-energy residual สูงสุด: `1.4557244298885053e-11 J`
- global-energy residual สูงสุด: `0.25046080350875854 J`; แบบสัมพัทธ์ `5.009216070175171e-9`
- ความต่าง half-step แบบสัมพัทธ์สูงสุด: `0.002683761648435663` ต่ำกว่า `0.02`

มุมเลี้ยวศูนย์รักษาการวิ่งตรงแบบสมมาตรพอดี การเลี้ยวตรงข้ามและตัวควบคุม split-grip/spatial-mirror ให้ mismatch ของสถานะ mirror ที่เลือกเป็นศูนย์ ตัวควบคุมมุมเลี้ยวเกิน `+0.04 rad` ให้โหลดต่ำสุด `-0.14156334912604507 N` ที่ attempted step 443 และจบที่ `0.442 s` ด้วย `DNF: contact_lift`

ไฟล์หลักฐาน primary และ replay ตรงกันทุกไบต์ File SHA-256 คือ `3D9BF89250E57EC818B785797F3854F4A729BDBAEEBEB8313DD31EE5A2726359` ส่วน canonical evidence payload SHA-256 คือ `935eaec117ab5835e7af8b47cf50f63ec79cfa30e0d57cccad79b5ba1629a6ba`

## บันทึกการตรวจสอบ

environment probe แรก `python -m pytest tests/test_coupled_planar_differential.py -q` จบด้วย exit `1` เพราะ Python ระบบไม่มี `pytest` จากนั้นจึงใช้ runner `unittest` ที่ repo ประกาศไว้ นี่เป็นปัญหาเลือก runner ไม่ใช่ physics assertion ล้มเหลว

```text
python -m unittest tests.test_coupled_planar_differential -v
Exit: 0
Ran 10 tests in 13.528s — OK

python scripts/experiments/run_coupled_planar_differential.py --config config/vehicle/coupled_planar_differential_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work071/materialized_architecture_v3.json --output artifacts/work071/experiment_evidence.json
Exit: 0
status=passed; evidence_sha256=935eaec117ab5835e7af8b47cf50f63ec79cfa30e0d57cccad79b5ba1629a6ba

python scripts/experiments/run_coupled_planar_differential.py --config config/vehicle/coupled_planar_differential_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work071/replay/materialized_architecture_v3.json --output artifacts/work071/replay/experiment_evidence.json
Exit: 0
primary SHA-256 = replay SHA-256 = 3D9BF89250E57EC818B785797F3854F4A729BDBAEEBEB8313DD31EE5A2726359

python -m unittest discover -s tests -v
Exit: 0
Ran 431 tests in 48.203s — OK
```

ผล repository-contract, compilation, staged-diff, commit และ replay หลัง commit ขั้นสุดท้ายจะบันทึกใน final handoff หลังคำสั่งเหล่านั้นทำงาน

## ข้อจำกัดและงานถัดไป

การกระจายแรงกดปกติยังเป็น quasi-static แบบจำลองยังไม่มีระยะยุบ spring/damper, roll-centre geometry, unsprung mass, wheel hop, tyre relaxation, temperature/wear, camber, aligning moment, ข้อมูลยางที่วัดจริง, การเชื่อม aero map, road roughness, driver/path controller, ขอบสนาม หรือ lap timing residual ภายในที่สอดคล้องกันไม่ได้แสดงความแม่นยำต่อโลกจริง

งานถัดไปควรเพิ่มสถานะล้อ/ช่วงล่างแบบ transient พร้อม contract สำหรับ contact-loss/travel/energy แล้วตามด้วยการเชื่อม path และ circuit แบบ closed-loop การเทียบผลกับการทดลองจริงยังจำเป็นก่อนกล่าวอ้างการยืนยันทางกายภาพ
