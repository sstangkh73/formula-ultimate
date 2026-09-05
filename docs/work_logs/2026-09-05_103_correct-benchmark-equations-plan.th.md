# แผน Work 103: แก้สมการและหลักฐานสมดุลของ benchmark

ต้นฉบับภาษาอังกฤษ: `2026-09-05_103_correct-benchmark-equations-plan.md`

Status: Completed

## เป้าหมายและขอบเขต

แก้ข้อผิดพลาดที่ระบุใน Work 102 ภายใน generalized geometry benchmark: residual ที่สร้างให้เป็นศูนย์เอง, ธง convergence ที่ให้ผ่านเสมอ, พลังงาน Hertz และความไม่สอดคล้องของ effective modulus/radius ระหว่าง indentation กับ contact stress เริ่มจาก revision `1b6e93c` ไม่เปลี่ยนโหลด/เกณฑ์เพื่อทำให้ผลใหม่ผ่าน

คำนวณ residual ของสมการ constitutive แบบสเกลาร์จาก stiffness/compliance ที่กำหนดก่อนคำตอบ แยกจาก force/moment/energy balance ของสนาม 3D ที่ยังไม่มี โดยใช้ null และสถานะชัดเจนสำหรับหลักฐานที่ไม่มี Hertz ใช้ E* = E/[2(1-nu^2)], effective radius เดียวกัน, F = K*delta^(3/2), U = (2/5)*K*delta^(5/2) สำหรับการเพิ่มโหลดแบบ quasistatic สมมติฐานวัสดุเท่ากันและ radius proxy ต้องเปิดเผย ไม่อ้างว่าแก้ contact จาก STEP จริงแล้ว

## ไฟล์ที่วางแผน

- `src/formula_ultimate/structural/generalized_geometry_benchmarks.py`
- `scripts/structural/run_generalized_geometry_benchmarks.py`
- `tests/test_generalized_geometry_benchmarks.py`
- `docs/contracts/GENERALIZED_GEOMETRY_BENCHMARKS_V1.md` และ `.th.md`
- แผนและผล Work 103 สองภาษา; outputs ใหม่ใน `artifacts/work103/` (ไม่ commit artifacts)

## การตรวจและเกณฑ์สำเร็จ

ทดสอบค่ามาตรฐาน Hertz ที่คำนวณแยก การอินทิเกรตแรงเป็นพลังงาน dU/ddelta = F การสเกลโหลด/วัสดุ การรบกวนคำตอบให้ residual ไม่เป็นศูนย์ การหมดงบ Newton/ค่าผิดโดเมน และการปฏิเสธหลักฐานปลอม/ไม่ครบ รัน `python -m unittest tests.test_generalized_geometry_benchmarks -v`, runner กับ output run_a แล้ว replay run_b, และ `python -m unittest discover -s tests -q` ตรวจคู่ภาษา staged scope และ `git diff --cached --check` แล้ว commit เฉพาะงาน

ตัวแปรต้นคือ implementation สมการ ความละเอียด/iteration และการรบกวน; ตัวแปรตามคือ response, residual, energy, contact pressure, convergence/failure และ replay identity; controls คือ config วัสดุ geometry และโหลดเดิม สำเร็จเมื่อ regression tests ผ่าน ค่าตรงสมการอิสระ และผลทำซ้ำได้ ล้มเหลวเมื่อคำตอบผิดยังผ่านหรือมี hidden repair หาก baseline เดิมตกจากสมการที่แก้ ต้องรายงานตรงและไม่ปรับโหลดกลบ

## ความเสี่ยงและสิ่งที่ไม่ทำ

ผล/identity อาจเปลี่ยนและเทียบ replay กับ Work 097 เดิมไม่ได้ จึงเพิ่ม evaluator version และเก็บหลักฐานเดิม ไม่เขียนประวัติใหม่ ไม่สร้าง general FEM หรือแก้รถทั้งคัน ไม่ยกระดับ physical validation จาก scalar checks งานต่อเรื่อง mesh/reactions อิสระยังแยกต่างหาก
