# แผน Work 010: 3D Circuit Corridor และ Swept Envelope แบบมี Version

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-25_010_3d-circuit-corridor-plan.md`

สถานะ: Completed

## วัตถุประสงค์

สร้างคิวถาวรสองภาษาสำหรับ Work 010–019 และ implement งานข้อแรก: physics
boundary ของ circuit corridor แบบมี version ซึ่งแทน centerline curvature,
grade, banking, clearance ซ้าย/ขวา, คุณภาพหลักฐาน และ kinematic swept envelope
ของรถทั้งคันก่อนเข้า race simulation

## ขอบเขต

- สร้างคิวงานฟิสิกส์ 10 ข้อภาษาอังกฤษและไทย ครอบคลุม Work 010–019 พร้อมลำดับ
  การทำให้เสร็จ
- กำหนด contract หน่วย SI แบบ strict สำหรับ corridor segment, vehicle envelope,
  source evidence, integrated 3D station และ assessment
- integrate piecewise-constant curvature, grade และ banking เป็นสถานีอ้างอิง 3D
  แบบ deterministic
- คัดกรอง static width, steering curvature และ swept radial envelope ด้านใน/
  ด้านนอกสำหรับ segment ตรงและรัศมีคงที่
- แยกผล `admitted`, `rejected`, `indeterminate` และผล verification แบบ
  synthetic geometry ที่ไม่ใช่ survey ต้องไม่อนุมัติการแข่งจริง
- เชื่อม corridor layer กับแค็ตตาล็อกสนามจริง 10 สนามโดยไม่สร้าง surveyed
  geometry ที่ไม่มีหลักฐาน
- เมื่อยืนยันปัญหาช่องว่างหลักฐาน geometry สนามจริงสาธารณะ ให้สร้าง problem
  report แยกสองภาษาและแก้ด้วย evidence-class gate, import contract และ
  analytical fixture แทนการเดาข้อมูล
- เพิ่ม unit test, analytical reference, invalid input, evidence gate และ
  deterministic replay
- สร้าง result evidence ฉบับเต็มสองภาษา ตรวจสอบ และ commit Work 010 ก่อนเริ่ม
  Work 011

## ไฟล์ที่วางแผน

- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.md`
- `docs/physics/PHYSICS_IMPLEMENTATION_QUEUE.th.md`
- `src/formula_ultimate/physics/corridor.py`
- `src/formula_ultimate/physics/__init__.py`
- `config/circuits/corridor_schema_v1.json`
- `scripts/validate_corridor.py`
- `tests/test_corridor.py`
- `docs/physics/CIRCUIT_CORRIDOR_MODEL.md`
- `docs/physics/CIRCUIT_CORRIDOR_MODEL.th.md`
- problem report แยกสองภาษาหากพบปัญหา geometry evidence
- plan/result Work 010 ภาษาอังกฤษและไทยชุดนี้

Path ของ schema fixture อาจเปลี่ยนหาก interface ที่เล็กกว่าเพียงพอ ต้องบันทึก
การเบี่ยงเบนใน result

## ขอบเขตโมเดล

Corridor ระดับ Level 0/ต้น Level 1 เป็นตัวแทน analytical แบบแบ่งช่วง สามารถ
ปฏิเสธรถจาก static clearance ไม่พอ, steering authority ไม่พอ หรือ swept
clearance บนรัศมีคงที่ แต่ไม่แทน laser scan, wall/kerb mesh ละเอียด, pose
ช่วงล่าง transient, tyre slip หรือ collision engine

เฉพาะ geometry ที่มี evidence class ซึ่งอนุญาต admission เท่านั้นจึงคืน
`admitted` ได้ Input แบบ approximate, digitized หรือ synthetic ต้องคงสถานะ
non-authoritative ให้เห็น แม้ผ่าน mathematical screen

## นิยามการทดลอง

### สมมติฐานที่ต้องการทดสอบ

รถที่ผ่าน static width ยังอาจถูกปฏิเสธจาก steering หรือ swept overhang ใน
corridor โค้ง ดังนั้นการเพิ่ม curvature และ longitudinal envelope ทั้งคันจะสร้าง
ข้อจำกัดต่อดีไซน์เอเจนต์ก่อน dynamics optimization อย่างมีนัยสำคัญ

### ตัวแปรอิสระ

- curvature และความกว้างซ้าย/ขวาของ corridor
- ความกว้างรถ wheelbase, front/rear overhang และ maximum steering angle
- geometry evidence class

### ตัวแปรตาม

- required steering angle
- swept radius/margin ด้านในและด้านนอก
- segment แรกที่ fail และเหตุผล
- admission status
- พิกัดสถานี 3D และ closure residual แบบ deterministic

### ตัวควบคุม

- หน่วย SI และ sign convention
- station spacing สำหรับ integration คงที่
- จุดอ้างอิงรถที่กึ่งกลางเพลาหลัง
- สมมติฐาน segment แบบ piecewise constant
- evidence gate และ tolerance เดียวกันสำหรับ candidate ทุกตัว

### การพยายามหักล้างและเกณฑ์ล้มเหลว

- สร้างรถที่ผ่าน static width แต่ overhang ล้ำขอบโค้งด้านนอกและต้องถูกปฏิเสธ
- สร้างรถที่ required steer เกิน limit ที่ประกาศและต้องถูกปฏิเสธ
- Corridor synthetic ที่ผ่านคณิตศาสตร์ต้องไม่ถูกเรียกว่า admitted
- ปฏิเสธข้อมูล non-finite, negative, impossible, discontinuous หรือไม่รองรับ
- geometry สนามจริงสาธารณะที่ไม่มีหลักฐานระดับ survey ต้องเป็น indeterminate
  ไม่ใช่ zero curvature หรือความกว้างที่เดา

## การตรวจสอบ

```powershell
python -m unittest discover -s tests -v
python scripts/validate_corridor.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

ทุก gate จะเรียกแยกหรือใช้ control flow แบบ fail-fast ชัดเจน

## เกณฑ์สำเร็จ

- มีคิว Work 010–019 สองภาษาและรักษาลำดับการทำทีละข้อ
- Contract ของ corridor และรถ strict, deterministic และใช้ SI
- กรณี analytical ทางตรง โค้งซ้าย และโค้งขวาผ่าน reference test
- Candidate แบบ static-fit-but-swept-fail และ steering-fail ถูกปฏิเสธ
- Real geometry ที่ไม่มีหลักฐานยังเป็น indeterminate
- Problem report แยกบันทึกและแก้ evidence gap ที่พบ
- Full test, compilation, bilingual Markdown contract, working/staged
  whitespace check, commit และ post-commit verification ผ่าน

## ความเสี่ยง

- แหล่งทางการสาธารณะอาจมีเพียง diagram แต่ไม่มีพิกัด 3D จากการสำรวจหรือ
  uncertainty ชัดเจน
- Rigid-body envelope แบบ curvature คงที่ไม่รวม tyre slip, roll, pitch,
  suspension travel และการเสียรูปของกำแพง
- Piecewise integration อาจสะสม closure error ต้องแสดงให้สังเกตได้
- การใช้ approximate geometry เป็น authoritative จะสร้างความมั่นใจทางฟิสิกส์
  ปลอมและ incentive ที่ไม่ปลอดภัยแก่เอเจนต์

## สิ่งที่ไม่ทำโดยชัดเจน

- ไม่อ้างว่าสนามจริงทั้ง 10 มี geometry 3D จากการสำรวจแล้ว
- ไม่ดึง dimension จาก marketing map ที่ไม่มี scale
- ไม่สร้าง full collision mesh, tyre model, racing-line optimizer หรือ lap-time
  model
- ไม่เริ่ม implement tyre ของ Work 011 ก่อน Work 010 ผ่านและ commit
- ไม่ push ไป remote repository
