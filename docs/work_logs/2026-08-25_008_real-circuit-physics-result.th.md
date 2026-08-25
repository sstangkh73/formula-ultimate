# ผล Work 008: Physics Profile ของสนามจริงสิบสนาม

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-25_008_real-circuit-physics-result.md`

สถานะ: Completed

## ผลลัพธ์

สร้างแค็ตตาล็อก Level 0 ของสนาม Formula One จริง 10 สนามแบบ deterministic
และตรวจสอบแหล่งข้อมูลย้อนกลับได้แล้ว การสร้างรถสามารถรับแรงกดดันเฉพาะสนามที่
ขัดกันก่อนออกแบบ และความกว้างรถสามารถถูกคัดกรองกับความกว้างต่ำสุดที่เผยแพร่และ
ใช้กับ layout นั้นได้ก่อนเข้า race simulation

รถอ้างอิงที่จงใจกว้าง `7.0 m` พร้อมระยะเผื่อข้างละ `0.25 m` ถูก Monaco ปฏิเสธ
หลักฐานความกว้างที่หายไปหรือใช้คนละ layout จะคืน `indeterminate` และไม่ผ่าน
แบบเงียบ ๆ

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/physics/circuit.py`
- `src/formula_ultimate/physics/__init__.py`
- `config/circuits/real_circuits_v1.json`
- `scripts/validate_circuits.py`
- `tests/test_circuit.py`
- `docs/physics/CIRCUIT_MODEL.md`
- `docs/physics/CIRCUIT_MODEL.th.md`
- `docs/research/REAL_CIRCUIT_SOURCE_REPORT.md`
- `docs/research/REAL_CIRCUIT_SOURCE_REPORT.th.md`
- plan/result Work 008 ภาษาอังกฤษและไทยชุดนี้

ไม่ได้เขียนทับหรือลบการเปลี่ยนแปลง Work 006 หรือ Work 007 ที่มีอยู่ก่อน

## พฤติกรรมที่สร้างแล้ว

- 10 profile: Monaco, Monza, Spa-Francorchamps, Singapore, Suzuka,
  Silverstone, Hungaroring, Mexico City, Bahrain และ Sao Paulo
- strict dataclass ตรวจ identifier, ค่า SI, ขอบเขตคะแนน, source metadata,
  การเชื่อม width กับ source, ID ซ้ำ และ residual ระยะเรซ
- แกนแรงกดดันแบบ ordinal หยาบ 8 แกนแยกจากข้อเท็จจริงสนามอย่างชัดเจน และ
  เวกเตอร์ทั้ง 10 สนามไม่ซ้ำกัน
- ผล static width คือ `screen_passed`, `rejected` หรือ `indeterminate`
- หลักฐานความกว้างที่ใช้ได้คือ Monaco `7 m`, Monza `10–12 m`, Suzuka
  `10–16 m` และ Sao Paulo `12–15 m`
- คำนวณความหนาแน่นอากาศแห้ง ISA เฉพาะเมื่อมีระดับความสูงเชิงตัวเลขพร้อมแหล่ง
  Mexico City ที่ `2,285 m` ให้ `0.9779651043911286 kg/m^3`
- เก็บ official race distance แยกจากผลคูณความยาวรอบที่ปัดเศษ และแสดงผลต่างเป็น
  `race_start_offset_m`
- validator ส่งออก JSON แบบ deterministic สำหรับ admission check และ metadata
  การทดลองภายหลัง

## การตัดสินใจและการแก้ข้อมูล

1. แยก field ข้อเท็จจริงที่เผยแพร่จากสมมติฐานคะแนนแรงกดดัน
2. การผ่าน width เป็นเพียง static screen ที่จำเป็น ไม่ใช่หลักฐานว่ารถเลี้ยวได้
   หรือ swept volume ไม่ชนกำแพง
3. Singapore ใช้ layout FIA ปี 2025 ยาว `4.94 km`, 19 โค้ง และ 62 รอบ ค่า
   `10–15 m` ในหน้าประวัติของผู้จัดเป็น layout ปี 2008 ที่เลิกใช้แล้ว จึงให้
   Singapore เป็น `indeterminate`
4. ผลค้นหาครั้งแรกดูเหมือนสนับสนุน Bahrain `14–15 m` แต่เมื่อตรวจหน้าเต็มพบว่า
   ค่าอยู่ใต้หัวข้อ **Inner Track** ไม่ใช่ Formula 1 Grand Prix Track จึงถอดออก
   จาก hard constraint และเก็บเพียงหลักฐานว่าใช้ไม่ได้ Bahrain ยังคงเป็น
   `indeterminate`
5. ผู้ดำเนินการสนามเทศบาล Sao Paulo ให้ช่วงความกว้างที่ใช้ได้ชุดที่สี่คือ
   `12–15 m`
6. altitude, width และ geometry ละเอียดที่ไม่ทราบต้องแสดงเป็นหลักฐานที่ขาด
   ไม่แทนด้วยค่าประมาณที่ดูสมเหตุผล

## หลักฐานการตรวจสอบ

### ชุดทดสอบทั้งหมด

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`

ผลสำคัญ:

```text
Ran 42 tests in 0.228s
OK
```

การทดสอบสนาม 10 รายการครอบคลุม deterministic loading, จำนวนแค็ตตาล็อกพอดี,
เวกเตอร์แรงกดดันต่างกันและอยู่ในขอบเขต, ความหนาแน่น ISA, การปฏิเสธรถใหญ่,
ข้อจำกัดของ static pass, missing evidence แบบ indeterminate, การเชื่อม source,
residual ระยะเรซที่สังเกตได้ และการปฏิเสธอินพุตผิด

### การทดลองหักล้างด้วย envelope ใหญ่เกิน

```powershell
python scripts/validate_circuits.py --vehicle-width-m 7.0 --clearance-per-side-m 0.25
```

Exit status: `0`

ผลสำคัญ:

```text
"circuit_count": 10
"width_evidence_count": 4
"status_counts": {
  "indeterminate": 6,
  "rejected": 1,
  "screen_passed": 3
}
Monaco: minimum_width_m=7.0, status=rejected
Mexico City: isa_air_density_kg_per_m3=0.9779651043911286
```

### การ compile

```powershell
python -m compileall -q src scripts tests
```

Exit status: `0`; ไม่มี output

### การตรวจ whitespace

```powershell
git diff --check
```

Exit status: `0`; มีเพียงคำเตือน line-ending เดิมของ Git

## หลักฐานสนับสนุนและขัดแย้ง

หลักฐานสนับสนุนคือรถอ้างอิงขนาดใหญ่ไม่มีสิทธิ์แข่งได้ทุกสนาม และทุกสนามมี
เวกเตอร์แรงกดดันก่อนออกแบบที่ไม่ซ้ำกัน

หลักฐานขัดแย้งและคำอธิบายทางเลือกคือ static screen ไม่จำลองการเลี้ยวหรือ swept
volume, 6 profile ยังไม่มี published minimum width ที่ใช้ได้, คะแนนแรงกดดันเป็น
สมมติฐาน ordinal ที่มนุษย์กำหนด และความต่างเวลาในอนาคตอาจมาจากคุณภาพ control,
ผิวสนาม อากาศ หรือ geometry ที่ขาด มากกว่าจะมาจาก topology รถ

ความมั่นใจสูงสำหรับข้อเท็จจริงขนาดเรซ ปานกลางสำหรับ static width screen 4 สนาม
และต่ำถึงปานกลางสำหรับสมมติฐานแรงกดดันจนกว่าจะเทียบ sensitivity และ telemetry

## ข้อจำกัด

- งานนี้ไม่มี centerline, boundary, wall, kerb, runoff, camber, banking,
  gradient ตามตำแหน่ง หรือ pit-lane model จากการสำรวจ 3D
- `screen_passed` ไม่ใช่ physical validation และไม่อนุมัติรถสำหรับแข่ง
- ความหนาแน่น ISA เป็นบรรยากาศแห้งอ้างอิง ไม่ใช่สภาพอากาศวันแข่ง
- profile เดียวไม่แทนสถานะเปียก/แห้ง การสะสมยาง ลม อุณหภูมิ หรือ grip ที่เปลี่ยน
  ตามเวลา
- หน้าแหล่งข้อมูลสาธารณะเปลี่ยนได้ ต้องเก็บ access date และ layout reference
  เพื่อ replay แบบ deterministic

## งานต่อไป

1. เพิ่ม 3D centerline และขอบ corridor ซ้าย/ขวาจากการสำรวจแบบมี version
2. เพิ่ม full-vehicle swept-volume check จาก width, length, wheelbase,
   steering lock, overhang, roll และ pitch
3. เพิ่ม gradient, banking, curvature, surface และการกระจาย weather พร้อม
   uncertainty ชัดเจน
4. ปรับและพยายามหักล้างเวกเตอร์แรงกดดัน ordinal กับ telemetry หรือ simulator
   อ้างอิงที่ละเอียดกว่า
5. ป้อน circuit admission และ pressure metadata เข้า grammar สร้างรถก่อนเริ่ม
   whole-car optimization
