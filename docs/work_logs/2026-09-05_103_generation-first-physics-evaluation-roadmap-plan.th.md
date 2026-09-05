# แผน Work 103: Roadmap แบบสร้างก่อน แล้วใช้ฟิสิกส์ประเมิน

ต้นฉบับภาษาอังกฤษ: `2026-09-05_103_generation-first-physics-evaluation-roadmap-plan.md`

สถานะ: Completed

## วัตถุประสงค์

บันทึกสถาปัตยกรรม generation/evaluation ปัจจุบันของ Formula Ultimate และแทนสมมติฐานเดิมที่ representation กับ gate ครอบก่อนเวลา ด้วยแผน generation-first อย่างละเอียด: candidate แสดง morphology ที่ไม่คุ้นเคยได้ก่อน แล้วให้ฟิสิกส์วัด อธิบาย และจัดอันดับสิ่งที่ถูกสร้าง โดยยังคงข้อห้าม hard anti-exploit, ทรัพยากรจำกัด, หลักฐาน และด่าน promotion โดยไม่กำหนดรูปทรงชิ้นส่วนตามแบบเดิม

## ขอบเขตและไฟล์ที่วางแผน

- `docs/reports/GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.md` และคู่ภาษาไทย
- plan/result นี้และคู่ภาษาไทย

งานนี้เป็นแผนสถาปัตยกรรมและการทดลองแบบ append-oriented จะไม่แก้ roadmap และผลเก่าให้ดูเหมือนว่าทิศทางใหม่นี้ถูก implement มาตั้งแต่ต้น

## เนื้อหาที่วางแผน

1. บันทึกสภาพก่อนหน้าจาก Work 090 และ Works 091–097: primitive scalar search, free-form corpus ที่ตรึง, mutation เฉพาะ typed graph, synthetic manufacturing fixture ก่อน performance, semantic selector ที่ตรึง และ reduced-order structural adapter 7 แบบที่ตรึง
2. แยก constraint เป็น representation invariants, external task/resource constraints, measurable physics outcomes, manufacturability outcomes, numerical/evidence states และข้อกำหนดเฉพาะตอน promotion
3. กำหนดวงจรชีวิต candidate ใหม่ตั้งแต่ open-ended genotype และ executable geometry generation ไปสู่การวัด, ผูก boundary condition, ทดลอง solver, บันทึกผลต่อเนื่อง, quality-diversity archive และ fidelity promotion
4. ระบุความสามารถ genome/operator ใหม่สำหรับ control point, field, topology, interface, material distribution และ mechanism/controller co-evolution แทนการเลือกจาก frozen solid library
5. กำหนดให้ candidate ที่ physical fail, manufacturing incompatible และ numerically unresolved ยังเป็นหลักฐานที่สังเกตได้ ไม่ถูกรวมความหมายหรือทิ้งแบบเงียบ
6. แตกเป็น implementation works อย่างละเอียด พร้อม independent/dependent variables, controls, metrics, success/failure criteria, migration risks และ non-goals ชัดเจน

## การตรวจสอบและเกณฑ์สำเร็จ

- ข้อความทุกข้อเกี่ยวกับระบบปัจจุบันต้องชี้ไปยัง source, retained artifact หรือรายงานที่เสร็จแล้ว และคง claim boundary เดิม
- Flow ใหม่ต้องไม่ยอมรับ NaN/ทรัพยากรอนันต์, hidden energy, hidden repair, provenance ที่หาย, solver exploitation หรือข้ออ้างฟิสิกส์ที่ไม่มีหลักฐาน
- Geometry novelty ห้ามชดเชย physical failure แต่ physical/manufacturing failure สามารถเก็บเป็นผลค้นหาและ stepping-stone archive entry ที่วัดแล้วได้
- ต้องแยก `numerically_unresolved`, `physically_failed`, `manufacturing_incompatible` และ `representation_invalid`
- Roadmap ต้องระบุการเปลี่ยน executable ที่จำเป็นก่อน Work 100 โดยไม่อ้างว่า Work 097 ปัจจุบันประเมิน geometry อิสระได้แล้ว
- คู่ภาษาอังกฤษ/ไทย, local links, คำศัพท์, identifiers, ตัวเลข และข้อจำกัดต้องตรงกัน
- Repository-contract tests และ Markdown diff checks ต้องผ่านก่อน scoped commit

## ความเสี่ยงและสิ่งที่ไม่ทำ

การย้าย gate ไปภายหลังอาจใช้ compute มากหรือเปิดทาง simulator exploit หากไม่คง budget, escalation rule, conservation audit และ invalid-state accounting ให้ชัด Geometry แบบ solid/implicit ทั่วไปอาจ mesh ยาก แต่การแก้ไม่ได้ไม่ใช่หลักฐานว่าพังทางฟิสิกส์ Manufacturing ไม่ได้ถูกตัดออกจาก final promotion เพียงแต่ไม่ทำลาย candidate ในการสำรวจระยะแรก

Work 103 ไม่เปลี่ยน CAD generator, physics solver, search algorithm, configuration, experiment, การเผยแพร่ภายนอก หรือ roadmap เดิม เอกสารนี้ไม่ยืนยันรถและไม่รับประกันว่า open-ended search จะค้นพบกลไกที่มีประโยชน์
