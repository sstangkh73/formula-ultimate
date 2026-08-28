# แผน Work 023: Typed Circuit และ Environment Step Inputs

ต้นฉบับภาษาอังกฤษ: `2026-08-28_023_typed-step-inputs-plan.md`

สถานะ: Completed

## วัตถุประสงค์

สร้าง deterministic typed circuit, spatial, weather, traffic และ strategy input
สำหรับ real-circuit profile สิบสนาม และเชื่อมกับ input adapter boundary จาก Work
022 โดย missing evidence ต้องแสดงชัดและห้ามกลายเป็น neutral condition เงียบ

## ขอบเขต

- กำหนด immutable SI record สำหรับ local circuit geometry, atmosphere/weather,
  traffic และ strategy command พร้อม source/provenance identity
- กำหนด input scenario และ resolution result ที่มี missing-evidence field ตรงจริง
  พร้อม deterministic fingerprint
- Resolve catalog profile ทั้งสิบที่ race distance ที่ขอ
- ถือว่า surveyed spatial evidence และ weather observation ที่ไม่มีเป็น
  incomplete ไม่ใช่ zero curvature, sea-level air, zero wind, dry track หรือ
  clear traffic
- อนุญาต isolated-traffic control ที่ประกาศชัด และแยกจาก unknown traffic
- สร้าง `input_bridge` adapter ให้ ready scenario emit สี่ signal ที่ประกาศ ส่วน
  incomplete scenario คืน atomic invalidity พร้อม write ศูนย์
- เพิ่ม falsification test, validator, เอกสาร model/result สองภาษา, queue update,
  problem report หากจำเป็น และ verified commit หนึ่งชุด

## ไฟล์ที่วางแผน

- `src/formula_ultimate/simulation/step_inputs.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_step_inputs.py`
- `scripts/validate_step_inputs.py`
- `docs/simulation/TYPED_STEP_INPUTS.md` และ `.th.md`
- `docs/integration/COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.md` และ `.th.md`
- คู่ plan/result สองภาษานี้และ problem report ที่จำเป็น

## นิยามการทดลอง

- สมมติฐานหลัก: typed resolver หนึ่งตัวแสดง deterministic ได้ว่า scenario ของ
  สิบสนามใด ready หรือ evidence-incomplete โดยไม่สร้าง neutral environment ปลอม
- Independent variables: circuit profile, race distance, spatial/weather/
  traffic evidence, strategy command, evidence identity และ registration order
- Dependent variables: readiness, missing field, fingerprint, adapter status,
  emitted signal type และ rollback/publication behavior
- Controls: versioned ten-circuit catalog เดิม, SI unit, circuit-ID match ตรง,
  explicit evidence status และ atomic transaction contract จาก Work 022
- Success criteria: profile สิบสนาม resolve deterministic; gap ปัจจุบันถูกลิสต์
  ตรง; complete fixture emit typed input สี่ signal; missing/mismatch/non-finite
  ทุกตัว fail-closed โดยไม่มี partial write
- Failure criteria: missing field กลายเป็น zero/default, fingerprint เปลี่ยนเมื่อ
  replay, evidence ข้าม circuit ID หรือ incomplete input ไปถึง physics-stage output
- Falsification: ลบ evidence แต่ละกลุ่ม, ใช้ unknown traffic, circuit ID ไม่ตรง,
  inject SI value non-finite/out-of-range, replay/reorder profile และ execute ready
  เทียบกับ incomplete input adapter

## ความเสี่ยง

- Profile สิบสนามเป็น circuit-level fact ไม่ใช่ surveyed local racing line จึงให้
  curvature/bank/width ณ distance ใดๆ ไม่ได้
- Weather/traffic เป็น event-time variable ห้ามอนุมานจากประเทศหรือ design pressure
- Complete analytical fixture validate input contract ไม่ใช่ real race

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่ refresh ข้อมูลสนามผ่านเว็บ, ไม่สร้าง real-circuit corridor/weather ปลอม,
  ไม่ couple aero/contact/motion/energy, ไม่มี whole-race simulation, optimizer,
  physical-validation claim, README change หรือ remote push

## Validation

```powershell
python -m unittest tests.test_step_inputs -v
python -m unittest discover -s tests -v
python scripts/validate_step_inputs.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```
