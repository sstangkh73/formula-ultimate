# แผน Work 083: Ground-Interaction Candidate 001

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-03_083_ground-interaction-candidate-001-plan.md`

## สถานะ

สถานะ: Completed

## วัตถุประสงค์

สร้าง candidate เชิงกลหลายชิ้นหนึ่งแบบที่ตรวจสอบและ replay ได้ ซึ่งถ่ายแรงปฏิกิริยาพื้นแนวตั้ง แนวยาว และแนวข้างไปยัง structural mount ส่งแรงบิดขับและแรงบิดเบรกไปยังจุดสัมผัส อนุญาตการเลื่อนแนวดิ่งและการหมุนของชิ้นสัมผัสตามที่ประกาศ และล้มเหลวอย่างสังเกตได้เมื่อเส้นทางวิกฤตขาด

นี่คือ candidate ที่สร้างขึ้นหนึ่งแบบ ไม่ใช่สถาปัตยกรรมรถที่ evaluator บังคับใช้ งานซอฟต์แวร์และ CAD อาจเสร็จสมบูรณ์ได้ แต่คำตัดสิน design admission ต้องยังเป็นลบ เพราะหลักฐานวัสดุ/กระบวนการที่มีอยู่เป็น synthetic

## ขอบเขตและการทดลองที่ตรึงไว้

- ตรึง candidate ห้าชิ้นก่อนประเมิน: structural mount, guide frame, translating carrier, axle และ annular contact roller
- ใช้ค่า SI ใน declaration และแปลงเป็นมิลลิเมตรเฉพาะที่ขอบเขต CadQuery
- คำนวณ mobility ของ assembly จากแถวข้อจำกัดข้อต่อที่ประกาศชัด: fixed mount, fixed guide, prismatic carrier, fixed axle และ revolute roller
- ประเมินระยะเคลื่อนที่แนวดิ่ง ระยะห่างรูปทรงจริงที่ปลายช่วงเคลื่อนที่ แรงกดตั้งฉากที่เป็นบวก การปิดสมดุลแรง/โมเมนต์ การปิดสมดุลพลังงานขับ/เบรก และเส้นทาง mount/แรงบิดที่ต่อเนื่อง
- รัน control สำหรับ mirror symmetry, rigid/no-travel, disconnected mount, blocked translation, seized rotation, broken torque path, undersized capacity และ contact loss
- ใช้หลักฐาน structural-mount coupling ที่ตรงตัวตนจาก Work 082 ซ้ำเป็น structural witness แบบจำกัดขอบเขต และไม่ขยายผลไปยังชิ้นส่วนอื่น
- สร้างแต่ละชิ้นและ assembly ทั้งหมดเป็น canonical STEP และบันทึก FreeCAD FCStd witness ที่มี solid นำเข้าแยกชิ้น
- รัน CAD/replay ใหม่สองครั้ง แล้วเปรียบเทียบตัวตน declaration, part, assembly, FreeCAD summary และ evaluation

ตัวแปรอิสระคือ topology, รูปทรงชิ้นส่วน, ชนิด/ตำแหน่งข้อต่อ, ระยะเคลื่อนที่, รัศมีสัมผัส, เวกเตอร์แรง, แรงบิด, ความเร็วเชิงมุม, ประสิทธิภาพ, สถานะการเชื่อมต่อ, capacity scale และ mirror state ตัวแปรตามคือจำนวนและตัวตนชิ้นส่วน, mobility, ระยะเคลื่อนที่, clearance, แรงตั้งฉาก, wrench และแรงบิดที่ส่ง, กำลัง/งาน, residual สมดุลและพลังงาน, สถานะ structural witness, สถานะ subsystem, การตอบสนองของ control และตัวตน replay ค่าอ้างอิงและ mirror ที่ตรึงไว้เป็น positive controls ส่วน fault ที่ฉีดทุกกรณีเป็น falsification controls

## ไฟล์ที่วางแผนแก้ไข

- `config/candidates/ground_interaction_candidate_001.json`
- `src/formula_ultimate/subsystems/__init__.py`
- `src/formula_ultimate/subsystems/ground_interaction.py`
- `scripts/candidates/build_ground_interaction_candidate_001.py`
- `scripts/candidates/inspect_ground_interaction_freecad.py`
- `tests/test_ground_interaction_candidate_001.py`
- `docs/contracts/GROUND_INTERACTION_CANDIDATE_001.md` และไฟล์คู่ภาษาไทย
- แผนนี้และไฟล์คู่ภาษาไทย
- result ที่ตรงกันและไฟล์คู่ภาษาไทยหลัง validation
- หลักฐานที่สร้างภายใต้ `artifacts/work083/` ซึ่งถูก ignore

## การตรวจสอบ

1. รัน candidate builder สองครั้งใน pinned CadQuery environment
2. นำเข้าแต่ละชิ้นและ assembly ที่ตรงตัวตนผ่าน FreeCAD โดยไม่ซ่อม บันทึก FCStd และวัด solid ที่แยกกัน
3. เปรียบเทียบตัวตน replay แบบ exact และรัน functional/failure controls ที่ประกาศทั้งหมด
4. รัน unit test เฉพาะจุดและ repository-contract test, compile แหล่ง Python ทั้งหมด แล้วรัน test suite เต็ม
5. stage เฉพาะไฟล์ Work 083 ตรวจขอบเขต staged รัน `git diff --cached --check`, commit และตรวจเฉพาะจุดหลัง commit ซ้ำ

## เกณฑ์สำเร็จ

- มี solid ชิ้นส่วนแยกที่ valid ห้าชิ้น และมี assembly STEP/FCStd witness หนึ่งชุด
- mobility ที่คำนวณได้เท่ากับสอง DOF พอดี: การเลื่อนแนวดิ่งหนึ่งและการหมุนชิ้นสัมผัสหนึ่ง
- ระยะเคลื่อนที่อ้างอิงและ geometric clearance ผ่านโดยไม่มี hidden repair หรือการปิดบัง interference
- มีเส้นทางแรงต่อเนื่องที่ไม่กำกวมไปถึง mount และเส้นทางแรงบิดที่ไม่กำกวมไปถึงจุดสัมผัส
- force และ moment residual แต่ละค่า `<=1e-5`; energy residual `<=1e-4`
- หลักฐานโครงสร้างผูกกับตัวตน exact และยังระบุชัดว่า synthetic-only
- fault ที่กำหนดทุกกรณีทำให้เกิดการเปลี่ยนแปลงที่ประกาศ และ disconnection/contact loss วิกฤตทำให้ `DNF`
- สองรันสร้าง hash ของ declaration, part STEP, assembly STEP, evaluation และ canonical FreeCAD summary ซ้ำได้
- คำตัดสิน candidate คือ `not_admitted_synthetic_evidence` เสมอ ไม่ใช่คำอ้างการตรวจสอบในโลกจริง

## ความเสี่ยง

- ตำแหน่ง assembly หรือ tolerance อาจทำให้เกิดการทับซ้อนที่ไม่ได้ตั้งใจตลอดช่วงเคลื่อนที่
- serialization ของ STEP หรือ FCStd อาจมี timestamp; ใช้เฉพาะหลักฐานที่ canonicalize อย่างชัดเจนสำหรับ exact replay
- สมการ quasi-static อย่างง่ายตรวจ bookkeeping ได้ แต่ยืนยันสมรรถนะ tyre/contact, fatigue, bearing หรือ dynamics ไม่ได้
- หลักฐาน Work 082 ที่ใช้ซ้ำครอบคลุมเฉพาะ bracket/load family ที่ตรงตัว และใช้คุณสมบัติวัสดุ synthetic

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่อ้างว่าเป็น suspension, wheel, tyre, steering, brake, bearing, ชิ้นส่วนการผลิต, safety case, fatigue life หรือ physical test ที่ผ่าน validation
- ไม่เพิ่มความชอบ topology จาก candidate เดียวนี้เข้าไปใน evaluator ทั่วไป
- ไม่มี hidden repair, force clipping, overlap suppression, การเปลี่ยนรูปทรงตามผลลัพธ์ หรือการ relabel หลักฐาน synthetic ให้เป็น design evidence
- ไม่ทำ energy converter ของ Work 084, integrated load structure ของ Work 085 หรือ whole vehicle ของ Work 086
