# แผนงาน 032: รายงานวิจัย Design Search Agent v0

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_032_design-search-agent-v0-report-plan.md`

สถานะ: เสร็จสมบูรณ์

## วัตถุประสงค์

จัดทำแผนวิจัยที่พร้อมนำไป implement สำหรับ Design Search Agent ตัวแรกของ
Formula Ultimate โดยอิง Research Experiment Protocol ที่เสร็จแล้วและขอบเขต
หลักฐานปัจจุบัน `3D -> STEP -> FreeCAD -> Level 0`

## ขอบเขต

- กำหนดบทบาท agent, ขอบเขตอำนาจ, input, output, state และการทำงานร่วมกับ
  evaluator แบบ deterministic
- เลือกการทดลอง component ที่มีหน้าที่จริงชุดแรก พร้อม interface, load,
  keep-out region, material assumption และ failure criteria ที่ประกาศ
- กำหนด candidate representation, generation operator, พฤติกรรมเมื่อ reject,
  baseline, matched compute budget, seed, metric และ falsification test
- กำหนด roadmap การ implement และ promotion ตามลำดับ จาก parameter search ไป
  independent structural evidence โดยไม่อ้าง complete-vehicle discovery
- ระบุความเสี่ยงด้าน safety, research integrity, simulator exploitation และ
  evidence พร้อม control ที่ชัดเจน
- ดูแลรายงานภาษาอังกฤษและไทยแยกไฟล์

## ไฟล์ที่วางแผน

- `docs/reports/DESIGN_SEARCH_AGENT_V0_PLAN.md`
- `docs/reports/DESIGN_SEARCH_AGENT_V0_PLAN.th.md`
- แผน/ผล Work 032 ภาษาอังกฤษและไทยที่ตรงกัน

Work item นี้เป็นงานเอกสารเท่านั้น จะไม่ implement หรือรัน simulator, CAD
grammar, optimizer, candidate artifact หรือ external service

## คำถามของรายงาน

1. Agent ใดทำ design search และระบบใดยังคงเป็น evaluator ที่ไม่ใช่ agent?
2. งานออกแบบแรกที่เล็กที่สุดแต่มีความหมายทางวิทยาศาสตร์คืออะไร?
3. Agent เปลี่ยนตัวแปรใดได้ และ control ใดแก้ไม่ได้?
4. วัด candidate validity, performance และ failure อย่างไร?
5. กฎ baseline และ compute budget แบบใดทำให้เปรียบเทียบยุติธรรม?
6. ต้องมี evidence gate ใดก่อน promote เกิน Level 0?
7. ลำดับ implementation ใดทดสอบและ falsify ได้ทีละขั้น?

## การตรวจสอบ

คำสั่งที่วางแผน:

```powershell
py -3.14 -m unittest tests.test_repository_contract -v
py -3.14 -m unittest discover -s tests -q
git diff --check
git diff --cached --check
```

ผล work item จะบันทึก exit code และ output แบบกระชับที่แน่นอน

## เกณฑ์สำเร็จ

- รายงานแยก Codex orchestration, Design Search Agent ในอนาคต และ CAD/physics
  evaluator แบบ deterministic อย่างชัดเจน
- การทดลองแรกมีตัวแปรอิสระ/ตาม, control, metric, success criteria และ failure
  criteria ที่ชัดเจน
- fixed/random/search treatment ได้ budget และ seed ที่ประกาศเท่ากัน
- แผนพยายาม falsify preferred hypothesis และบันทึก alternative explanation
  กับ missing evidence
- Roadmap อยู่ภายในหลักฐาน implementation ปัจจุบันและไม่เรียก Level 0 ว่า
  physical validation
- bilingual, repository, whitespace และ staged-scope check ผ่านและ commit สำเร็จ

## ความเสี่ยง

- เป้าหมายกว้างแบบ “ออกแบบรถแข่ง” จะเกิน geometry และ physics contract ปัจจุบัน
- Component grammar อาจฝัง preferred solution ทำให้ search ดูฉลาดเกินจริง
- Fitness ที่ใช้ mass-only Level 0 จะให้รางวัลการตัด material ที่เป็นไปไม่ได้
  ทางโครงสร้าง
- Optimization effort ที่ไม่เท่ากันทำให้ searched treatment ดูเหนือ baseline
  ที่ tune ไม่พอ
- รายงานอาจถูกเข้าใจผิดว่า implement แล้ว ต้องระบุ status และ non-goal ชัดเจน

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่ implement Design Search Agent และไม่รัน autonomous search
- ไม่มี complete-vehicle generation, free-topology claim, ผล FEA/CFD,
  physical validation, safety claim, manufacturing claim หรือ discovery claim
- ไม่กำหนด conventional vehicle layout เพียงเพราะประวัติการแข่งใช้รูปแบบนั้น
- ไม่ push, publish, upload ภายนอก หรือ rewrite history
