# ผลลัพธ์ Work 012: Typed Energy และ Powertrain Component Graph

ต้นฉบับภาษาอังกฤษ: `2026-08-26_012_typed-energy-graph-result.md`

สถานะ: Completed

## ผลลัพธ์

Work 012 เสร็จสมบูรณ์ repository มี typed component graph แบบ fail-closed
สำหรับ power interface ของ source, converter, transmission, tyre และ sink
Chain อ้างอิง compile แบบทำซ้ำได้เป็น:

```text
battery -> motor -> gearbox -> rear_tyre -> road
```

การกลับลำดับ input ทั้ง component และ connection ให้ compiled metadata เท่ากัน
ทุกประการ Carrier mismatch, direction mismatch, endpoint หาย, identity ซ้ำ,
required port ไม่ต่อ, fan-out โดยนัย, หลาย source เข้า input, self-loop,
role violation และ directed cycle ถูกปฏิเสธ

ผลนี้ validate เฉพาะกฎ topology/interface ไม่มีข้ออ้างด้าน energy conservation
หรือ physical validation

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/physics/energy_graph.py`: typed port, component,
  connection, factory, compiler deterministic และ error topology invalid
- `src/formula_ultimate/physics/__init__.py`: export API energy graph สาธารณะ
- `tests/test_energy_graph.py`: test 12 รายการสำหรับ valid, permutation, type,
  role, connectivity, topology, capacity และ invalid-input
- `scripts/validate_energy_graph.py`: หลักฐาน valid-chain replay และการปฏิเสธ
  mismatch
- `docs/physics/ENERGY_COMPONENT_GRAPH.md` และ `.th.md`: contract SI/type,
  กฎ fail-closed, ลำดับ deterministic, boundary และข้อจำกัด
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md` และ `.th.md`: สถานะ Work 012
- คู่ plan/result Work 012 ภาษาอังกฤษและไทยนี้

## การตัดสินใจ

1. Carrier vocabulary ปิดที่ chemical, electrical, mechanical rotational,
   mechanical translational และ thermal
2. ทุก port มี direction, carrier และ capacity หน่วยวัตต์ที่ finite/เป็นบวก
3. Source มีเฉพาะ output; sink มีเฉพาะ input; converter มีทั้งสอง; transmission
   คงเป็น rotational; tyre แปลง rotational input เป็น translational output
4. Port ทุกจุด required และ one-to-one Fan-out และหลาย source เข้า input ล้มเหลว
   แทนการบอกเป็นนัยว่าทำซ้ำหรือบวก power
5. Connection ต้อง carrier ตรงกันและมีทิศ output-to-input
6. Capacity connection ที่ compile คือ capacity ปลายที่น้อยกว่า
7. Lexical Kahn sorting ทำให้ลำดับ component ไม่ขึ้นกับลำดับ input tuple ส่วน
   compiled connection เรียง endpoint แบบ lexical

## การทบทวนการทดลอง

- Independent variables: role/ID ของ component, type/direction/capacity ของ
  port, endpoint และ input permutation
- Dependent variables: compile status/reason, ลำดับ component/connection และ
  capacity
- Controls: vocabulary/factory คงที่, lexical tie-break, required port แบบ
  one-to-one และไม่มีความสุ่ม/การซ่อม
- หลักฐานสนับสนุน: reference ห้า component compile เหมือนกันภายใต้ reverse input
  permutation พร้อม connection ceiling `480000`, `440000`, `410000` และ
  `390000 W`
- หลักฐานขัดแย้ง/หักล้าง: chemical-to-rotational โดยตรง, output fan-out,
  สอง source เข้า input เดียว, disconnection, self-loop และ cycle สอง converter
  ล้มเหลวทั้งหมด
- คำอธิบายทางเลือกที่ตัดออก: deterministic equality เป็น equality ของโครงสร้าง
  dataclass ไม่ใช่เพียงลำดับ print ที่ดูคล้ายกัน
- หลักฐานที่ยังขาด: instantaneous power, stored energy, loss, efficiency,
  depletion, regenerative flow และ conservation residual
- ความมั่นใจ: สูงสำหรับ topology/type compilation; ไม่มีต่อ conservation หรือ
  physical performance จนกว่าจะใช้กฎขั้นถัดไป

## ปัญหาที่พบ

ไม่พบปัญหาที่มีสาระซึ่งต้องสร้าง problem report แยก การ review ภายในพบว่า
generic component ต้องมี role-specific port check ด้วย จึงเพิ่ม check และ test
ตาม invalid-contract ที่วางแผนไว้ก่อน validation

## หลักฐาน Validation

ทุกคำสั่งรันจาก `C:\Formula Ultimate` พร้อม fail-fast exit handling

```powershell
python -m unittest tests.test_energy_graph -v
```

Exit status: `0` ผลสำคัญ: `Ran 12 tests`; `OK`

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0` ผลสำคัญ: `Ran 80 tests`; `OK`

```powershell
python scripts/validate_energy_graph.py
```

Exit status: `0` ผลสำคัญ:

```text
component_order: battery, motor, gearbox, rear_tyre, road
permutation_replay_equal: true
carrier_mismatch_rejected: true
claim_boundary: topology compiled; no energy conservation claim
```

```powershell
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit status: `0` ทุกคำสั่ง โดยรัน staged check หลัง stage แบบระบุขอบเขตและก่อน
commit อีกครั้ง

## ข้อจำกัดและงานต่อเนื่อง

- ไม่คำนวณ operating power หรือ energy
- ยังไม่ยอมรับ branch, merger, regenerative cycle หรือ dynamic control
- Capacity เป็นเพดาน interface ไม่ใช่ operating point ที่ทำนาย
- Work 013 จะเพิ่ม independent conservation audit ต่อ step ซึ่งทำให้ hidden หรือ
  double-counted energy invalid
