# แผน Work 108: ข้อมูลต้นทางร่วมของเนื้อวัสดุและช่องว่าง

ต้นฉบับภาษาอังกฤษ: `2026-09-10_108_spatial-material-plan.md`

วันที่: 2026-09-10 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์

พัฒนาแพ็กเกจแรกใน `docs/plans/detailed_part_to_vehicle_v1`: spatial contract แบบมีขอบเขตและ replay ได้ ซึ่งบริเวณ B-rep ที่มีเนื้อ ช่องว่างที่ประกาศ การเป็นเจ้าของวัสดุ rigid placement ปริมาตร มวล จุดศูนย์กลางมวล และความเฉื่อย ใช้อัตลักษณ์ geometry และวัสดุที่เปลี่ยนย้อนหลังไม่ได้ร่วมกัน

## ขอบเขตและข้อมูลเข้า

ขอบเขต admitted ใช้ free-form B-rep grammar ของ Work 092 ที่ตรวจแล้วและอัตลักษณ์ config ต้นทางที่ตรงกัน ครอบคลุม CAD แบบโค้ง มีโพรง และหลาย body, homogeneous analytic reference หนึ่งกรณี, การเป็นเจ้าของ solid ที่มีเนื้อแต่ละก้อนเพียงครั้งเดียว, หลักฐาน cavity ที่ชัดเมื่อ feature DAG ต้นทางมี subtraction และ rigid placement ในหน่วย SI CadQuery สร้างและวัดครั้งแรก ส่วน FreeCAD import STEP ชุดเดียวกันแล้ววัดอย่างอิสระโดยไม่ healing

การทดลองล็อก:

- ตัวแปรอิสระ: revision ต้นทางที่มี cavity, ความหนาแน่นราย region และ rigid placement
- ตัวแปรตาม: ความต่างของ occupied volume, mass, centre-of-mass และ inertia
- ตัวควบคุม: homogeneous reference ที่ทราบคำตอบและ revision geometry ต้นทางที่ไม่เปลี่ยน
- เกณฑ์ล้มเหลว: overlap ที่ไม่ประกาศ การนับเจ้าของซ้ำ พิกัด non-finite, hash เก่า, CAD ไม่ถูกต้อง, หน่วย/กรอบไม่สอดคล้อง, เอา cavity ออกแล้วมวลเดิมยังค้าง หรือเกิน tolerance ใด ๆ

## ไฟล์ที่วางแผนเปลี่ยน

- `src/formula_ultimate/components/spatial_material.py`
- `src/formula_ultimate/components/__init__.py` หากต้อง export API สาธารณะ
- `config/development/spatial_material_v1.json`
- `scripts/development/run_spatial_material.py`
- `scripts/cad/inspect_spatial_material_freecad.py`
- `tests/test_spatial_material.py`
- `docs/contracts/SPATIAL_MATERIAL_VOID_V1.md` และคู่ภาษาไทย
- แผนนี้และคู่ภาษาไทย
- result log ที่ตรงกันและคู่ภาษาไทย
- หลักฐานที่ generate และ ignore ใต้ `artifacts/work108/`

ไฟล์ที่เพิ่มจาก card ที่เสนอจำกัดเพียง FreeCAD inspector อิสระ และ contract/evidence logs สองภาษาที่โปรโตคอลบังคับ

## วิธีพัฒนา

1. ตรวจ declaration แบบ exact schema ที่ใช้พิกัด SI finite, density เป็นบวก, เจ้าของ region ไม่ซ้ำ, การประกาศเจ้าของไม่ทับกัน, อัตลักษณ์ SHA-256 ต้นทาง และ placement transform ที่มีขอบเขต
2. สร้าง solid Work 092 ที่เลือกใหม่จาก config ต้นทางที่ล็อกไว้ เก็บ source STEP, placed STEP และ canonical manifests
3. หา volume, centre และ unit-density inertia จาก solid B-rep ที่มีเนื้อจริง ใช้ density, rigid rotation, translation และ parallel-axis theorem เพื่อหาสมบัติมวลรวม
4. แสดงหลักฐาน cavity ด้วย ancestry ของ feature subtraction จริง และตรวจว่าปริมาตรเนื้อเท่ากับ outer volume ลบ declared cavity volume ในกรณี hollow ที่ admitted
5. ให้ FreeCAD import STEP ที่ตรงกันอย่างอิสระ วัดแต่ละ solid สร้าง mass properties แบบถ่วงวัสดุใหม่ และเทียบตาม tolerance ที่ล็อก
6. ทดลองเปลี่ยนวัสดุ cavity/source และ placement บังคับให้อัตลักษณ์หลักฐานที่พึ่งพาเปลี่ยน และปฏิเสธ replay กับหลักฐานเก่า
7. สร้าง `result.json`, artifact manifest, mutation report และผล exact replay แบบกำหนดซ้ำได้ เก็บผลลบและข้อจำกัดทั้งหมด

## การตรวจสอบ

ต้องบันทึก executable ของ CadQuery Python และ FreeCAD Python ที่แก้พาธจริงใน result log ประตูตรวจที่วางแผนคือ:

```powershell
$env:PYTHONPATH='src'
& .\.tools\cadquery-mcp\Scripts\python.exe -m unittest tests.test_spatial_material tests.test_repository_contract -v
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_spatial_material.py --config config\development\spatial_material_v1.json --output-root artifacts\work108\run_a --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe'
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_spatial_material.py --config config\development\spatial_material_v1.json --output-root artifacts\work108\run_b --freecad-python 'C:\Program Files\FreeCAD 1.1\bin\python.exe' --replay-reference artifacts\work108\run_a\result.json
python -m compileall -q src scripts tests
python -m unittest tests.test_spatial_material tests.test_repository_contract -v
```

รัน regression ที่ได้รับผลกระทบหรือ full suite หากความเสี่ยงของ implementation สมควร ก่อน commit ให้รัน `git diff --check`, stage เฉพาะไฟล์ Work 108, ตรวจ `git diff --cached --name-only` และรัน `git diff --cached --check`

## เกณฑ์สำเร็จ

- positive invariants และ negative controls ที่ตั้งใจผ่านทั้งหมดโดยไม่มีการ skip CAD-dependent tests
- geometry Work 092 อย่างน้อยแบบโค้ง มีโพรง และหลาย body เก็บอัตลักษณ์ source/export ที่เปลี่ยนย้อนหลังไม่ได้
- กรณี hollow แสดงการเอา cavity ออกจาก geometry จริง โดยเอา cavity ออกแล้วมวลเดิมต้องไม่ค้าง
- CadQuery และ FreeCAD เห็นตรงกันอย่างอิสระใน volume, mass, centre และ inertia ภายใน tolerance ที่ลงทะเบียน
- rigid placement เปลี่ยน centre/inertia ในกรอบโลกอย่างสอดคล้อง พร้อมรักษา volume และ centroidal invariants
- clean replay ตรงกัน exact และปฏิเสธหลักฐาน source/material/placement เก่า
- contract สองภาษา, tests, implementation, configuration และ result evidence ถูก commit เป็น Work 108 เดียวแบบจำกัด scope

## ความเสี่ยงและสิ่งที่ไม่ทำอย่างชัดเจน

ความเสี่ยงรวมถึงลำดับ body ของ OCCT, convention ของ inertia tensor ไม่ตรงกัน, การนับซ้ำที่ junction เชื่อมมน, metadata CAD ที่ผันแปร และการสับสน declared cavity กับ complement ของ occupied solid วิธีลดความเสี่ยงคือ geometric identities, การเป็นเจ้าของราย solid, canonical ordering, ตรวจ symmetric tensor, วัด CAD อิสระ และเทียบแบบ fail closed

สิ่งที่ไม่ทำ: stress โครงสร้าง, พฤติกรรม thermal/flow, manufacturing feasibility, arbitrary material fields, feasibility รถทั้งคัน, physical validation, ติดตั้ง dependency, ทดสอบทางกายภาพ, push หรือเขียนประวัติ Git ใหม่ หรือบังคับ layout รถ/รูปทรงชิ้นส่วนแบบดั้งเดิมใด ๆ
