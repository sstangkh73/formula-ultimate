# ผลลัพธ์ Work 023: Typed Circuit และ Environment Step Inputs

ต้นฉบับภาษาอังกฤษ: `2026-08-28_023_typed-step-inputs-result.md`

สถานะ: Completed

## ผลลัพธ์

Work 023 สร้าง spatial, weather, traffic และ strategy input แบบ SI-typed
deterministic พร้อม `input_bridge` adapter จริง Profile สิบสนาม resolve ซ้ำได้ตรง
แต่ catalog ไม่มี surveyed local corridor, event-time weather หรือ traffic
scenario จึงเป็น incomplete ทั้งสิบและเข้า physics ถัดไปในรูป neutral value เงียบ
ไม่ได้

Analytical complete fixture หนึ่งชุด resolve ready และ emit สี่ signal ที่ประกาศ
ตรง ใช้ validate input contract เท่านั้น

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/simulation/step_inputs.py` และ simulation export
- `tests/test_step_inputs.py` (focused test 9 รายการ)
- `scripts/validate_step_inputs.py`
- `docs/simulation/TYPED_STEP_INPUTS.md` และ `.th.md`
- queue, plan/result และ fingerprint problem report สองภาษา

## การตัดสินใจและ Evidence

- Missing spatial/weather record มี reason และห้าม numeric default
- Unknown traffic ต่างจาก isolated control ที่ประกาศรถศูนย์ชัดเจน
- Cross-circuit evidence, SI value non-finite/out-of-range และ race distance เกิน
  ขอบเขต fail-closed
- Fingerprint pin profile ทั้งชุด, source/date, local evidence และ strategy ไม่ใช่
  แค่ circuit ID
- Incomplete adapter: `invalid`, reason ลิสต์ spatial/weather/traffic, emit `0`
- Complete fixture: `ready`, typed signal สี่ตัว, fingerprint
  `beaf971760985ac4218b2f4d708a3f1b61fef1af3eae5b591328d74470050d7e`
- Real physics-ready profile: `0/10`; ไม่มีการสร้าง evidence ปลอม

## ปัญหาและการแก้

Fingerprint รุ่นแรก pin แค่ `circuit_id` รายงานปัญหาแยกบันทึกแล้ว ปัจจุบัน
canonical hash รวม nested profile ทั้งชุด และ regression พิสูจน์ว่าแก้ content
ภายใต้ ID เดิมทำให้ hash เปลี่ยน

## Validation

```powershell
python -m unittest tests.test_step_inputs -v
# exit 0; Ran 9 tests in 0.007s; OK
python -m unittest discover -s tests -v
# exit 0; Ran 186 tests in 1.305s; OK
python scripts/validate_step_inputs.py
# exit 0; incomplete profile deterministic สิบสนาม; complete fixture emit 4
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
```

## Review และข้อจำกัด

Supporting evidence ครอบคลุม deterministic replay, exact missing field, strict
typing, fingerprint sensitivity และ incomplete input write ศูนย์ Ready fixture
เป็น alternative explanation ของ adapter success เพราะเป็น analytical ไม่ใช่
real-circuit evidence หลักฐานที่ยังขาดคือ surveyed local geometry, event weather
และ traffic ความมั่นใจสูงสำหรับ input contract และไม่เปลี่ยนสำหรับ vehicle physics

Work 024 ถัดไปคือ couple aerodynamic force/cooling เข้ากับ chassis force/moment
และ normal load โดยรับเฉพาะ ready typed input ไม่มีการ push
