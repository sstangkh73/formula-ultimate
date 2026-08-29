# แผนงาน 031: Research Experiment Protocol และ Candidate 001

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_031_research-experiment-protocol-candidate-001-plan.md`

สถานะ: เสร็จสมบูรณ์

## วัตถุประสงค์

สร้าง Research Experiment Protocol แบบมีเวอร์ชันสำหรับการทดลอง Formula
Ultimate ที่ใช้หลักฐานจาก geometry และรัน candidate แรกผ่านเส้นทางหลักฐาน
แบบปิด `3D -> STEP -> FreeCAD -> Level 0`

## ขอบเขต

- กำหนดตัวตน protocol, ตัวตน candidate, ข้อกำหนด input/evidence ที่แก้ย้อนหลัง
  ไม่ได้, stage gate, ระดับข้ออ้าง, replay metadata และข้อกำหนดการทบทวนแบบ
  falsification
- ประกาศ candidate แรกแบบมีขอบเขต `FU-C0001` ล่วงหน้า โดยใช้ grammar
  `mounting_plate_v1` ที่มีอยู่เป็นชิ้นทดสอบ geometry-evidence
- สร้าง candidate เป็น CadQuery B-rep, ส่งออก STEP ที่มี hash, import และวัด
  ไฟล์เดียวกันใน FreeCAD และยอมรับเฉพาะค่าที่ FreeCAD วัดเป็น input ของการ
  ประเมิน point-mass ระดับ Level 0 ที่มีอยู่
- บันทึกหลักฐานสำเร็จหรือล้มเหลวแบบมีโครงสร้าง โดยไม่ซ่อม geometry แบบซ่อน,
  ไม่ตัดค่าพารามิเตอร์ และไม่แทนค่าด้วยผล analytical
- เพิ่ม automated test ที่เจาะจงกับสัญญาหลักฐานของ protocol และดูแลเอกสาร
  คู่ภาษาอังกฤษ/ไทย

## ไฟล์ที่วางแผน

- `docs/research/RESEARCH_EXPERIMENT_PROTOCOL.md`
- `docs/research/RESEARCH_EXPERIMENT_PROTOCOL.th.md`
- `config/experiments/research_experiment_protocol_v1.json`
- `config/experiments/candidate_fu-c0001.json`
- `src/formula_ultimate/experiments/research_protocol.py`
- `src/formula_ultimate/experiments/__init__.py`
- `scripts/cad/run_research_candidate.py`
- `scripts/run_candidate_001.ps1`
- `tests/test_research_protocol.py`
- แผน/ผล Work 031 ภาษาอังกฤษและไทยที่ตรงกัน

หลักฐาน CAD และผลที่สร้างจะยังถูก Git ignore ภายใต้
`artifacts/work031/FU-C0001/`

## นิยามการทดลอง

### สมมติฐานที่ต้องการทดสอบ

Input `FU-C0001` ที่ประกาศไว้สามารถผ่านทุกขอบเขตหลักฐานโดยไม่มีการซ่อมแบบ
ซ่อน: valid solid หนึ่งชิ้นจาก CadQuery ส่งออกเป็น STEP ได้, FreeCAD import
STEP ที่มี hash ตรงกันเป็น valid solid หนึ่งชิ้นได้, dimensions และ volume
ที่รายงานแยกกันผ่าน tolerance ที่ประกาศ และ Level 0 รับ mass ที่ derive จาก
FreeCAD ได้

นี่คือสมมติฐานเรื่อง pipeline coherence ไม่ใช่สมมติฐานเรื่อง performance,
โครงสร้าง, ความปลอดภัย, การผลิต, ความใหม่ หรือ complete vehicle

### ตัวแปรอิสระ

- คำประกาศ geometry และ ID ของ candidate
- เวอร์ชัน protocol และ grammar

การรันแรกมี candidate ที่ประกาศล่วงหน้าเพียงหนึ่งตัว จึงไม่ได้ประมาณผลของ
design variable หรือจัดอันดับทางเลือก

### ตัวแปรตาม

- CAD validity และจำนวน solid
- STEP header, จำนวน byte และตัวตน SHA-256
- volume, bounds และ centre of mass จาก CadQuery และ FreeCAD
- residual ระหว่างเครื่องมือและเทียบ analytical
- component mass ที่ derive จาก density
- final speed และ final distance ระดับ Level 0
- สถานะ stage, failure code, เวอร์ชันเครื่องมือ, source hash และ wall time

### ตัวแปรควบคุม

- grammar `mounting_plate_v1` และ material density ที่ประกาศ
- geometry parameter, base mass, force, duration และ timestep ระดับ Level 0
- เส้นทาง adapter CAD/STEP/FreeCAD และ evidence tolerance
- deterministic seed และตัวตน repository/source

### เกณฑ์ falsification และความล้มเหลว

- ปฏิเสธ ID, version หรือหน่วยที่ไม่ประกาศ, ค่าที่ไม่ finite, topology ที่
  invalid, STEP header ที่หาย/ผิด, hash ไม่ตรง, FreeCAD import ล้มเหลว,
  จำนวน solid ไม่เท่ากับหนึ่ง, geometry จาก FreeCAD ที่ invalid, ค่าเกิน
  tolerance, หลักฐานขาด หรือสัญญา Level 0 ล้มเหลว
- เก็บ stage และข้อความที่ล้มเหลว ห้ามแทน FreeCAD evidence ที่หายหรือถูก
  ปฏิเสธด้วยค่า analytical
- บันทึกหลักฐานสนับสนุน, หลักฐานขัดแย้ง, คำอธิบายทางเลือก, หลักฐานที่ขาด
  และระดับความมั่นใจแม้ pipeline ผ่าน

## การตรวจสอบ

คำสั่งที่วางแผนให้หยุดทันทีเมื่อผิดพลาด:

```powershell
py -3.14 -m unittest tests.test_research_protocol -v
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_candidate_001.ps1
py -3.14 -m unittest discover -s tests -v
py -3.14 -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

จะบันทึกคำสั่งจริง, exit status, output สำคัญ, artifact hash, ข้อจำกัด และ
commit hash ในผล Work 031

## เกณฑ์สำเร็จ

- คำประกาศ protocol และ candidate มีเวอร์ชันและอ่านได้ด้วยเครื่อง
- `FU-C0001` สร้าง valid solid หนึ่งชิ้นและ STEP หนึ่งไฟล์โดยไม่ซ่อมแบบซ่อน
- FreeCAD วัด STEP hash เดียวกันเป็น valid solid หนึ่งชิ้น
- หลักฐาน analytical, CadQuery และ FreeCAD ตรงกันภายใน tolerance ที่ประกาศ
- เฉพาะ volume จาก FreeCAD และ density ที่ประกาศใช้กำหนด mass ที่ส่งเข้า
  Level 0
- ผลมีตัวตน source/config/tool/repository เพียงพอสำหรับ deterministic
  semantic replay
- focused/full validation ผ่าน, stage เฉพาะไฟล์ของ work item และ commit สำเร็จ

## ความเสี่ยง

- CadQuery และ FreeCAD ใช้เทคโนโลยี geometry ตระกูล OCCT เหมือนกัน จึงจำกัด
  ความเป็นอิสระของผลที่ตรงกัน
- STEP byte hash อาจเปลี่ยนข้ามการ export เพราะ metadata อาจมีข้อมูลตามเวลา
  replay จึงต้องเทียบ geometry และสมบัติทางกายภาพตาม tolerance พร้อมยืนยัน
  exact artifact ของแต่ละ run
- component แบบมีขอบเขตหนึ่งชิ้นพิสูจน์ complete-vehicle feasibility หรือ
  เปรียบเทียบ performance ของ candidate ไม่ได้
- Level 0 ลด geometry นี้เหลือ added point mass จาก constant density และยัง
  ไม่มีพฤติกรรมโครงสร้าง, thermal, aerodynamic, การผลิต, assembly และ safety

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่อ้าง complete vehicle, race readiness, optimality, discovery หรือ
  physical validation
- ไม่สร้าง free topology, ไม่กำหนด conventional vehicle layout และไม่เทียบ
  optimized baseline
- ไม่มี FEA, CFD, fatigue, crash, thermal, electromagnetic, manufacturing
  หรือ empirical validation
- ไม่แก้ Fusion, ไม่ upload ภายนอก, ไม่เผยแพร่, ไม่ push และไม่ rewrite history
