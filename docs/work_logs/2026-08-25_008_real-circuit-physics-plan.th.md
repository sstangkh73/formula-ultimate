# แผน Work 008: Physics Profile ของสนามจริงสิบสนาม

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-25_008_real-circuit-physics-plan.md`

## วัตถุประสงค์

สร้าง circuit-physics boundary ที่มี version รุ่นแรกจากสนามแข่งจริงสิบสนาม
ซึ่งมีจุดแข็งและจุดอ่อนต่างกันอย่างมีนัยสำคัญ หลักฐานสนามต้องพร้อมก่อนเอเจนต์
ออกแบบรถ เพื่อให้ dimension, packaging, energy, cooling, downforce, braking,
traction และ control ของรถตอบสนองต่อ race environment ทางฟิสิกส์ ไม่ใช่สนาม
abstract ที่เหมือนกันทั้งหมด

## ขอบเขต

- เลือกสนาม Formula One จริงสิบสนามที่รวมกันสร้างแรงกดดันการออกแบบต่างกันมาก
  เช่น street geometry แคบ, high-speed efficiency, altitude, elevation change,
  thermal load, heavy braking, low-speed traction, fast lateral loading และ
  โครงสร้างรอบแบบสั้น/ยาว
- บันทึก identity และ race fact ของสนามที่มีแหล่งอ้างอิงในหน่วย SI อย่างน้อย
  layout length, lap count, race distance, direction, altitude หรือ elevation
  เมื่อหา evidence ได้ และ track-width/corridor constraint ที่ประกาศเมื่อมี
  แหล่ง authoritative รองรับ
- ห้ามสร้าง dimension สนามที่หาไม่ได้ ทุก field ต้องมี provenance, evidence
  quality และ uncertainty หรือคงสถานะ unavailable อย่างชัดเจน
- กำหนด circuit profile ระดับ Level 0/Level 1 ที่มีผลต่อ physics ได้ก่อนมี
  surveyed 3D centreline เต็มรูปแบบ
- implement conservative vehicle-envelope clearance gate เพื่อไม่ให้ candidate
  ที่กว้างเกิน drivable corridor ที่ประกาศเข้าสู่ race simulation
- encode track-character load share หรือ index เฉพาะเมื่อวิธีสร้าง explicit,
  มี version, bounded และแยกจาก measured fact
- บันทึก track-specific design pressure และ failure risk โดยไม่กำหนดคำตอบรถ
- เพิ่ม test สำหรับ schema, unit, derived race distance, evidence requirement,
  envelope rejection, deterministic loading และข้อมูล invalid/non-finite
- ดูแล Markdown ทุกไฟล์เป็นคู่ภาษาอังกฤษและไทยแยกกัน

## ไฟล์ที่วางแผน

- `src/formula_ultimate/physics/circuit.py`
- `src/formula_ultimate/physics/__init__.py`
- `config/circuits/real_circuits_v1.json`
- `scripts/validate_circuits.py`
- `tests/test_circuit.py`
- `docs/physics/CIRCUIT_MODEL.md`
- `docs/physics/CIRCUIT_MODEL.th.md`
- `docs/research/REAL_CIRCUIT_SOURCE_REPORT.md`
- `docs/research/REAL_CIRCUIT_SOURCE_REPORT.th.md`
- plan/result record Work 008 ที่ตรงกัน แยกภาษาอังกฤษและไทย

รายการจริงอาจลดลงหาก interface ที่เล็กกว่าพอใช้งาน การเบี่ยงเบนจะบันทึกใน result

## ขอบเขตโมเดล

### Fact ที่วัดหรือเผยแพร่

- ชื่อ circuit/layout และประเทศ;
- official layout length และจำนวนรอบ race;
- derived และ/หรือ official race distance;
- direction และ altitude/elevation fact เมื่อมีแหล่งรองรับ;
- width/corridor evidence เมื่อมีแหล่งรองรับ;
- source URL, publisher, publication/access context และ evidence quality

### Screening input ที่ derive

- reference air density จาก altitude และ atmospheric assumption ที่ประกาศ;
- conservative maximum vehicle width จาก narrowest supported corridor,
  required lateral clearance และ uncertainty margin;
- normalized design-pressure index สำหรับ straight, low-speed corner,
  high-speed corner, braking, traction, elevation, thermal environment และ
  street-circuit confinement

Derived index เป็น research control ไม่ใช่ข้ออ้างแทน telemetry หรือ surveyed
3D track

### Fidelity ในอนาคต

- full 3D centreline, curvature, grade, banking, kerb, wall, runoff, surface
  friction map, roughness, drainage, wind field, weather distribution และ
  time-varying grip เป็นงานภายหลัง เว้นแต่มี authoritative data และตรวจได้
  ใน work item นี้

## นิยามการทดลอง

### สมมติฐานที่ต้องการทดสอบ

ชุด circuit profile ที่มี version และต่างกันทางฟิสิกส์จะปฏิเสธ vehicle envelope
ที่ใหญ่เกินระดับโลกหรือไม่เหมาะกับ environment ได้อย่างน้อยบางส่วน และสร้าง
design-pressure vector ที่ต่างกันตามที่ประกาศ ทำให้เอเจนต์มีข้อมูล race
environment ที่มีความหมายก่อน generation ดีไซน์

### ตัวแปรอิสระ

- real circuit profile ที่เลือก;
- ความกว้าง candidate vehicle ใน envelope-gate reference test

### ตัวแปรตาม

- การรับ/ปฏิเสธ envelope และเหตุผล;
- reference air density;
- circuit design-pressure vector;
- derived race distance residual เทียบ official value เมื่อมีทั้งสองค่า

### ตัวแปรควบคุม

- circuit-schema version;
- atmospheric equation และ constant;
- lateral-clearance และ uncertainty policy;
- ช่วง normalized index และวิธีสร้าง;
- candidate envelope สำหรับ cross-circuit comparison;
- validation tolerance และ software version

### การพยายามหักล้างและเกณฑ์ล้มเหลว

- พยายามรับรถที่จงใจกว้างเกินเข้าสนาม supported ที่แคบที่สุดและต้องถูกปฏิเสธ
  แบบสังเกตได้
- ปฏิเสธ hard geometric constraint ที่ไม่มี provenance
- ปฏิเสธข้อมูล non-finite, negative, out-of-range, duplicate หรือขัดแย้งภายใน
- รายงาน field width, altitude หรือ geometry ที่ขาดแทนการกรอกขึ้นเอง
- ถือว่าชุด profile ที่ไม่มี cross-circuit variation มีความหมายเป็น research
  input ที่ล้มเหลว ไม่ใช่ catalog ที่สำเร็จ

## การตรวจสอบ

คำสั่งที่วางแผนรวมถึง:

```powershell
py -3.14 -m unittest discover -s tests -v
py -3.14 scripts\validate_circuits.py
py -3.14 -m compileall -q src scripts tests
git diff --check
```

Source review จะใช้ข้อมูลปัจจุบันจาก FIA, Formula 1, circuit operator หรือ
government/organizer ทางการเมื่อทำได้ Secondary material ใช้ได้เฉพาะเป็น context
ที่ระบุ confidence ต่ำกว่า และห้ามใช้เป็น hard clearance constraint โดยไม่ทำ
เครื่องหมาย

## เกณฑ์สำเร็จ

- สนามจริงสิบสนามพอดี load แบบ deterministic จาก dataset ที่มี version หนึ่งชุด
- ชุดสนามมี physical/design-pressure profile ต่างกันอย่างมีนัยสำคัญ
- hard real-world field ทุกค่าที่ physics ใช้มี source และ quality metadata
- อย่างน้อยหนึ่งสนามจริงมี conservative corridor gate ที่ปกป้องได้ และ width
  ที่ไม่ทราบยังสังเกตได้แทนการเดา
- รถ reference ที่กว้างเกินถูกปฏิเสธก่อน race simulation
- หน่วย SI และ atmospheric assumption explicit
- Test, validation script, compilation, bilingual repository contract และ
  whitespace check ผ่าน
- Documentation ระบุสิ่งที่ profile พิสูจน์ได้และไม่ได้

## ความเสี่ยง

- หน้า circuit ทางการสาธารณะมักไม่มี minimum width, banking หรือ elevation
  ละเอียด รูป map ไม่เป็น dimensional survey โดยอัตโนมัติ
- Circuit length ที่เผยแพร่อาจเปลี่ยนตาม layout revision ทุก profile ต้องระบุ
  layout และ version
- นิยาม “จำนวนโค้ง” ต่างกันและไม่พอ reconstruct curvature
- Altitude ค่าเดียวจำลองสนามที่ elevation change มากไม่ได้
- คำอธิบายสนามเชิงคุณภาพอาจ bias เอเจนต์หากนำเสนอเป็น measured physics ต้อง
  แยก derived index ให้เห็นชัด
- Conservative width gate จาก evidence ไม่ครบอาจเข้มหรือหลวมเกินไป ต้องเก็บ
  uncertainty margin และ limitation

## สิ่งที่ไม่ทำโดยชัดเจน

- ไม่อ้าง laser-scan, FIA Grade-1 homologation geometry หรือ clearance accuracy
  ระดับ centimetre
- ไม่สร้าง complete 3D track mesh, racing line, CFD wind field, tyre surface map
  หรือ lap-time optimizer
- ไม่ออกแบบหรือ optimize รถใน work item นี้
- ไม่ hard-code คำตอบรถที่ชอบสำหรับแต่ละสนาม
- ไม่ดึง dimension แบบเงียบจาก marketing map ที่ไม่มี scale
- ไม่อ้าง physical validation จาก circuit profile ระดับ Level 0 เพียงอย่างเดียว
