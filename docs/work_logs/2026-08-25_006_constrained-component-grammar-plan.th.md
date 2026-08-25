# แผน Work 006: Constrained 3D Component Grammar และวงจรหลักฐาน

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-25_006_constrained-component-grammar-plan.md`

## วัตถุประสงค์

สร้าง constrained 3D component grammar รุ่นแรกที่มี version และรันวงจรหลักฐาน
ที่ทำซ้ำได้ ตั้งแต่การสร้างด้วย CadQuery ผ่านไฟล์แลกเปลี่ยนกลาง STEP
การวัดอย่างอิสระด้วย FreeCAD จนถึง physics kernel ระดับ Level 0 ที่มีอยู่

## ขอบเขต

- กำหนด `mounting_plate_v1` ซึ่งเป็น grammar ขนาดเล็กโดยเจตนาสำหรับ
  structural mounting plate มุมโค้ง ประกอบด้วย:
  - body ของแผ่นหนึ่งชิ้นที่มีขอบเขตค่า;
  - mounting interface แบบ 4 รูคงที่หนึ่งชุด;
  - central lightening cut แบบมีหรือไม่มีก็ได้และมีขอบเขตค่า;
  - material density ที่ระบุชัดเจน;
  - input เป็นหน่วย SI และแปลงเป็น millimetre เฉพาะที่ขอบเขต CAD API เท่านั้น
- ปฏิเสธชุด parameter ที่ผิดกฎหรือไม่เป็น finite ก่อนรัน CadQuery
- สร้าง geometry แบบ single-solid ที่ deterministic ด้วย CadQuery และ artifact
  STEP
- import STEP แต่ละไฟล์กลับด้วย FreeCAD แบบ headless แล้วรายงานจำนวน solid,
  volume, bounding box และ centre of mass อย่างอิสระ
- แปลง volume ที่ FreeCAD วัดได้เป็นมวล component แล้วเพิ่มเข้า vehicle baseline
  คงที่ใน longitudinal model ระดับ Level 0
- รันการทดลอง lightening radius แบบควบคุม 3 candidate และ candidate ที่ผิดกฎ
  โดยเจตนา 1 ตัวเพื่อพยายามหักล้าง grammar gate
- เก็บ manifest, hash, replay input และผลลัพธ์ที่เครื่องอ่านได้ไว้ใต้ tree
  `artifacts/work006/` ซึ่ง Git ignore
- เพิ่ม unit test และ integration test สำหรับทุกกฎ grammar ที่ implement
  และสัญญา CAD-to-Level-0 ที่ทดสอบได้โดยไม่ต้องเปิด external CAD process
- ดูแล Markdown ใหม่หรือที่แก้ไขทุกไฟล์เป็นไฟล์ภาษาอังกฤษและไทยแยกกัน

## ไฟล์ที่วางแผน

- `src/formula_ultimate/components/grammar.py`
- `src/formula_ultimate/components/__init__.py`
- `src/formula_ultimate/experiments/cad_level0.py`
- `src/formula_ultimate/experiments/__init__.py`
- `scripts/cad/generate_mounting_plate.py`
- `scripts/cad/inspect_step_freecad.py`
- `scripts/run_work006.ps1`
- `tests/test_component_grammar.py`
- `tests/test_cad_level0.py`
- `docs/3d/CONSTRAINED_COMPONENT_GRAMMAR.md`
- `docs/3d/CONSTRAINED_COMPONENT_GRAMMAR.th.md`
- plan และ result record Work 006 ที่ตรงกัน แยกภาษาอังกฤษและไทย

รายการจริงอาจเปลี่ยนหากการตรวจ repository พบ interface ที่เล็กและปลอดภัยกว่า
การเบี่ยงเบนทุกอย่างจะบันทึกใน result

## นิยามการทดลอง

### สมมติฐานที่ต้องการทดสอบ

สำหรับแผ่น valid ที่เหมือนกันด้านอื่น การเพิ่ม central lightening radius จะลด
volume และ mass ที่วัดอย่างอิสระแบบ monotonic เมื่อใช้ tractive force และ
environment ระดับ Level 0 ชุดเดียวกัน มวลรถรวมที่ลดลงจะเพิ่ม final speed และ
distance แบบ monotonic

นี่คือสมมติฐานเรื่องความสอดคล้องของ pipeline ไม่ใช่ข้ออ้างด้าน structural
performance

### ตัวแปรอิสระ

- รัศมี central lightening cut หน่วย metre โดยกำหนดระดับ valid ล่วงหน้า 3 ระดับ

### ตัวแปรตาม

- volume จาก CadQuery และสูตรวิเคราะห์;
- volume, จำนวน solid, bounding box และ centre of mass จากการ import STEP ด้วย
  FreeCAD;
- component mass ที่คำนวณจาก density;
- final speed และ distance ระดับ Level 0;
- volume residual ข้ามเครื่องมือและ artifact hash

### ตัวแปรควบคุม

- grammar version และ implementation ของ generator;
- ขนาดภายนอกของแผ่น ความหนา รัศมีมุม เส้นผ่านศูนย์กลาง mounting hole และพิกัด
  mounting hole;
- material และ density;
- version ของ CadQuery และ FreeCAD;
- base vehicle mass, tractive force, environment, duration และ timestep;
- deterministic seed ซึ่งบันทึกไว้แม้กฎ version 1 ไม่มี stochastic rule

### การพยายามหักล้างและกรณีล้มเหลว

- ส่ง central cut ที่กำหนดล่วงหน้าซึ่งละเมิด minimum-web constraint และต้องถูก
  ปฏิเสธก่อน CAD execution
- ถือว่า input ไม่เป็น finite, single-solid topology ผิด, import STEP ล้มเหลว,
  จำนวน solid ผิดคาด, volume ไม่ตรงกันเกิน tolerance หรือผลควบคุมไม่ monotonic
  เป็น failure ที่สังเกตได้
- บันทึกหลักฐานสนับสนุน หลักฐานขัดแย้ง คำอธิบายทางเลือก หลักฐานที่ขาด
  และระดับความเชื่อมั่นในผล

## การตรวจสอบ

คำสั่งที่วางแผนรวมถึง:

```powershell
py -3.14 -m unittest discover -s tests -v
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work006.ps1
py -3.14 -m compileall -q src scripts tests
git diff --check
```

launcher จะเรียก Python environment ของ CadQuery ที่ pin ไว้ใน Work 005 และ
FreeCAD 1.1 headless executable ที่ตรวจแล้ว คำสั่ง exact, exit status, output
ที่เกี่ยวข้อง, version, hash และ path artifact จะบันทึกใน result

## เกณฑ์สำเร็จ

- Grammar ปฏิเสธ deliberate invalid candidate ก่อนรัน CadQuery
- Candidate valid ทุกตัวสร้าง valid solid แบบ deterministic หนึ่งชิ้นและไฟล์
  STEP
- FreeCAD import STEP ทุกไฟล์อย่างอิสระเป็น solid หนึ่งชิ้นพอดี
- Volume จากสูตรวิเคราะห์, CadQuery และ FreeCAD ตรงกันภายใน absolute และ
  relative tolerance ที่ประกาศ โดยไม่แก้ discrepancy แบบเงียบ
- มวลจาก FreeCAD เป็นค่าที่ส่งเข้า Level 0 และระบุหน่วย SI ชัดเจน
- Output แบบควบคุมเป็นไปตาม monotonic expectation ที่ประกาศล่วงหน้า มิฉะนั้น
  ต้องรายงานงานว่าล้มเหลว/หยุดพร้อมหลักฐานที่ขัดแย้ง
- Unit, integration, repository-contract, compile และ whitespace check ผ่าน
- Replay metadata เพียงพอสำหรับรันการทดลองซ้ำบน local toolchain ที่ตรวจแล้ว

## ความเสี่ยง

- CadQuery และ FreeCAD ใช้เทคโนโลยีตระกูล OCCT เดียวกัน การตรงกันจึงเป็น
  independent application/import check แต่ไม่ใช่ทฤษฎี geometry ที่อิสระเต็มที่
- STEP tolerance หรือ topology healing อาจทำให้ volume ต่างกันเล็กน้อย
- FreeCAD 1.1.3 แยก command-line path ที่มีช่องว่างผิด launcher ต้องใช้รูปแบบ
  temporary path สั้นที่ตรวจแล้ว
- Geometry ที่ผ่าน grammar ไม่ได้แปลว่าแข็งแรง ผลิตได้ ทน fatigue ปลอดภัยจาก
  collision หรือเหมาะกับรถ
- ผลของมวลในกรณี Level 0 แบบแรงคงที่อย่างง่ายอาจมีขนาดเล็ก ต้องเก็บ precision
  ที่เพียงพอและไม่กล่าวเกินจริง

## สิ่งที่ไม่ทำโดยชัดเจน

- ไม่ทำ FEA, CFD, thermal analysis, fatigue analysis, crash analysis, topology
  optimization, manufacturing certification หรือ real-world safety validation
- ไม่อ้างว่า `mounting_plate_v1` พร้อมใช้ในรถแข่งหรือ optimal
- ไม่แก้ geometry ใน Fusion และไม่ติดตั้ง FreeCAD community MCP
- ไม่เปรียบเทียบ free topology หรือสรุปเชิงวิทยาศาสตร์เรื่อง design discovery
- ไม่ clip parameter, repair topology หรือแทน CAD evidence ที่ล้มเหลวด้วยค่า
  analytical แบบเงียบ
