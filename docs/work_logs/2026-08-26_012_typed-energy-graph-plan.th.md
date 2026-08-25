# แผน Work 012: Typed Energy และ Powertrain Component Graph

ต้นฉบับภาษาอังกฤษ: `2026-08-26_012_typed-energy-graph-plan.md`

สถานะ: Completed

## วัตถุประสงค์

Implement component graph แบบ typed ที่ทำซ้ำได้สำหรับการไหลพลังงานของรถ เพื่อ
ให้ agent ประกอบ source, converter, transmission, tyre และ sink ได้เฉพาะผ่าน
power port ที่มีชนิดและทิศทางเข้ากัน ก่อนเริ่ม simulation พลังงาน

## ขอบเขต

- กำหนด contract แบบเข้มงวดสำหรับ component, port, connection, graph และ
  compiled graph
- ใช้ energy carrier ชัดเจน: chemical, electrical, mechanical rotational,
  mechanical translational และ thermal
- ใช้ port input/output ที่มีทิศทางและ power capacity หน่วยวัตต์
- มี constructor สำหรับ role source, converter, transmission, tyre และ sink
- Compile graph ด้วย lexical topological ordering ที่ทำซ้ำได้
- ปฏิเสธ carrier mismatch, direction mismatch, port หาย, component/port/
  connection identity ซ้ำ, required port ไม่ต่อ, output fan-out โดยนัย, หลาย
  source เข้า input เดียว, self-loop และ cycle
- เก็บ graph เดิมและคืน compiled order ชัดเจน โดยไม่ซ่อม topology แบบเงียบ
- เพิ่ม test valid-chain เชิงวิเคราะห์, permutation/replay และ invalid-graph ที่
  หักล้าง พร้อม validator และเอกสารสองภาษา
- Validate และ commit Work 012 แยกก่อนเริ่ม Work 013

## ไฟล์ที่วางแผน

- `src/formula_ultimate/physics/energy_graph.py`
- `src/formula_ultimate/physics/__init__.py`
- `scripts/validate_energy_graph.py`
- `tests/test_energy_graph.py`
- `docs/physics/ENERGY_COMPONENT_GRAPH.md`
- `docs/physics/ENERGY_COMPONENT_GRAPH.th.md`
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md`
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.th.md`
- คู่ plan/result Work 012 ภาษาอังกฤษและไทยนี้
- รายงานปัญหาแยกสองภาษาเฉพาะเมื่อพบปัญหาที่มีสาระ

## ขอบเขตโมเดล

ทุก port ส่ง power capacity แบบมีทิศทางและไม่ติดลบในหน่วยวัตต์ ทิศ connection
กำหนด flow บวกจาก output ไป input Connection เข้ากันทางชนิดเมื่อ port ทั้งคู่
ประกาศ carrier เดียวกัน

Work 012 ตรวจ topology และความหมาย interface เท่านั้น ยังไม่กำหนด power ขณะใด
ขณะหนึ่ง ไม่ integrate joule, ไม่ใช้ efficiency, ไม่ติดตาม stored energy และไม่
พิสูจน์ conservation การทำงานเหล่านั้นอยู่ใน Work 013 และงานหลังจากนั้น

Compiler baseline กำหนดให้แต่ละ port มี connection หนึ่งเส้นพอดี Output fan-out
ถูกปฏิเสธ เพราะการทำซ้ำ power output ไปหลาย branch ทำให้การคิดพลังงานกำกวม
splitter ในอนาคตต้องประกาศ allocation และ conservation อย่างชัดเจน

## นิยามการทดลอง

### สมมติฐานที่ต้องการทดสอบ

Graph แบบ typed และ fail-closed ปฏิเสธ powertrain topology ที่กำกวมทางฟิสิกส์
ก่อน simulation ขณะที่ compile chain source-to-tyre ที่ถูกต้องเหมือนกัน ไม่ว่า
ลำดับ input component/connection จะเป็นอย่างไร

### Independent variables

- role และ identifier ของ component
- carrier, direction และ capacity ของ port
- endpoint ของ connection และลำดับ input

### Dependent variables

- compile สำเร็จ/ล้มเหลวและเหตุผลชัดเจน
- ลำดับ component ที่ทำซ้ำได้
- ลำดับ connection ที่ทำซ้ำได้
- connection capacity ที่ derive

### Controls

- vocabulary ของ carrier และ role factory คงที่
- lexical tie-breaking ใน topological sort
- port ทุกจุด required และ one-to-one ใน baseline Work 012
- ไม่มีความสุ่มเชิงตัวเลขหรือการซ่อม topology แบบเงียบ

### เกณฑ์หักล้างและความล้มเหลว

- chemical output ต่อ mechanical input โดยตรงต้องล้มเหลว
- output-to-output, input-to-input, endpoint หาย, input มี source ซ้ำ,
  fan-out โดยนัย, self-loop และ cycle ต้องล้มเหลว
- required port ที่ไม่ต่อ ต้องล้มเหลว
- permutation ของ graph ที่ถูกต้องเดียวกันต้อง compile เป็น metadata เหมือนกัน
- capacity invalid/non-finite/ติดลบ และ carrier/direction/role ที่ไม่รองรับต้อง
  ล้มเหลว

## Validation

```powershell
python -m unittest tests.test_energy_graph -v
python -m unittest discover -s tests -v
python scripts/validate_energy_graph.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

คำสั่งจะใช้ fail-fast exit handling

## เกณฑ์สำเร็จ

- Graph source → converter → transmission → tyre → sink compile ได้
- Compiled order ทำซ้ำได้ข้าม permutation ของ input
- topology หักล้างทุกแบบที่ประกาศถูกปฏิเสธพร้อม error ที่สังเกตได้
- tests ทั้งหมด, validator, compilation, contract Markdown สองภาษา,
  whitespace, staging แบบระบุ, commit และ post-commit verification ผ่าน

## ความเสี่ยง

- Graph generic อาจดูมีความหมายทางฟิสิกส์ทั้งที่ยังไม่มีกฎ conservation จริง
  เอกสารและสถานะต้องทำให้ขอบเขตนี้ชัดเจน
- Port one-to-one จำกัด branching และ regenerative loop ซึ่งต้องใช้ component
  ชัดเจนและ temporal semantics ในอนาคต
- ความเข้ากันของ capacity อย่างเดียวไม่ได้กำหนด operating power

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่มี energy integration, efficiency loss, storage depletion, conservation
  audit, thermal flow, regenerative loop หรือ controller
- ไม่อ้างว่า graph ที่ compile แล้วผ่าน physical validation หรือผลิตได้
- ไม่เริ่ม Work 013 audit ก่อน commit Work 012
- ไม่ push remote
