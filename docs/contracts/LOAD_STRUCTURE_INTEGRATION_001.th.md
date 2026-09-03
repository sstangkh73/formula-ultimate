# Load Structure Integration Candidate 001

ไฟล์ต้นฉบับภาษาอังกฤษ: `LOAD_STRUCTURE_INTEGRATION_001.md`

## ขอบเขต

สัญญานี้ประเมิน fixture การจัดวางระดับรถแบบ synthetic หนึ่งแบบ บังคับตัวตน exact ของ Work 083, Work 084 และ Work 086, STEP/FreeCAD solid แยกสิบเจ็ดชิ้น, mass properties จากรูปทรง, หลักฐาน interference ทุกคู่, service/routing clearance, บัญชี load/thermal, ความเข้ากันได้ของ motion interface, causal controls และ replay ไม่ได้ validate chassis, monocoque, crash structure, cooling package หรือ production assembly

## รูปทรงและเส้นทาง

นำเข้าชิ้นส่วน subsystem ที่ตรึงไว้สิบสองชิ้นโดยไม่แก้ สร้าง solid ใหม่ห้าชิ้นเป็น upper bridge, mount สองชิ้น และ coolant route สองเส้น วัดทุก unordered pair Overlap ที่ไม่ประกาศเกิน `1e-12 m3` หรือ clearance ต่ำกว่า `0.5 mm` เป็น blocker ที่มองเห็นได้และห้ามปิดบัง Routing/service clearance ต้องไม่น้อยกว่า `2 mm` และรูปทรง integration ใหม่ต้องสูงกว่าระนาบสัมผัสที่ตรึงไว้อย่างน้อย `5 mm`

มวล จุดศูนย์กลางมวล และ inertia เต็มคำนวณจาก volume/centre/inertia ของ B-rep exact ด้วยความหนาแน่น synthetic และ parallel-axis translation ค่าเหล่านี้ไม่ใช่การวัดทางกายภาพ

## บัญชี Controls และ Verdict

Load case หกกรณีจับคู่แรง/แรงบิดทุกค่ากับ structure reaction ที่ชัดเจน Force/moment residual ต้อง `<=1e-5` ความร้อนที่เกิดต้องเท่ากับ coolant บวก air rejection ภายใน `1e-4`; external primary inflow เป็นศูนย์ Controls บังคับต้อง reject mount ที่ขาด/อ่อน, service ถูกบล็อก, routing ชน, rejection ไม่พอ, โหลดไม่สมมาตร และโครงบาง; mirror กับ replay ต้องชัดเจน

Work 083 อนุญาต axle เคลื่อนแนวดิ่ง `+/-7 mm` ขณะที่ Work 084 ประกาศ rigid coaxial butt interface ด้วย alignment tolerance `1e-6 m` Evaluator ต้องเปิดเผย motion mismatch นี้ ห้ามเพิ่มข้อต่อเงียบ ๆ Blocker ใด ๆ ทำให้ `integration_status=partial`, `candidate_verdict=not_admitted` และ `design_use_allowed=false`
