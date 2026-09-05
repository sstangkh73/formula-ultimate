# เกณฑ์มาตรฐานเรขาคณิตทั่วไป V1

ต้นฉบับภาษาอังกฤษ: `GENERALIZED_GEOMETRY_BENCHMARKS_V1.md`

## วัตถุประสงค์

สัญญานี้ยอมรับพยานเรขาคณิตที่ไม่ใช่รูปทรงพื้นฐานจำนวน 7 รายการซึ่งตรึงไว้จาก Work 096 เข้าสู่การประเมินโครงสร้างแบบ benchmark ลดรูป เพื่อไม่ให้เรขาคณิตที่ไม่คุ้นเคยถูกปฏิเสธเพียงเพราะมีตัวประเมินเฉพาะรูปทรงพื้นฐานเท่านั้น ทั้งนี้ไม่ได้อ้างว่าเป็นตัวแก้ finite element ทั่วไป

## อัตลักษณ์แหล่งข้อมูล

`config/structural/generalized_geometry_benchmarks_v1.json` ผูกค่า SHA-256 ที่แน่นอนของ semantic configuration, รายงาน FreeCAD และ strict comparison จาก Work 096 ตัวรันจะปฏิเสธเมื่ออัตลักษณ์เปลี่ยน ผู้สมัครหาย region `support_region`/`load_region`/`contact_region` หาย หรือพบ `hidden_geometry_repair: true`

ผู้สมัครต้นทาง 7 รายการที่ตรึงไว้คือ:

1. `curved_branch_001`
2. `tapered_open_shell_001`
3. `tapered_hollow_duct_001`
4. `organic_load_bridge_001`
5. `ribbed_gusset_bridge_001`
6. `bored_chamfered_hub_001`
7. `revolved_intersection_member_001`

V1 ไม่ยอมรับการแทนที่ด้วยรูปทรงพื้นฐาน

## เส้นทางการประเมิน

แต่ละกรณีเลือกและให้เหตุผลสำหรับแบบจำลองหนึ่งชนิดจาก `beam`, `shell`, `solid` หรือ `contact` โดยใช้จำนวน solid, สมบัติหน้าตัดที่สุ่มวัด, อัตราส่วนความหนาต่อความยาวเส้นทาง, semantic regions และ path witness จาก Work 096 แบบจำลองที่คาดไว้กับที่เลือกต้องตรงกัน

เส้นทาง reference และ discrete ที่แยกจากกันประกอบด้วย curved bending เทียบ midpoint integration, tapered bending เทียบ refined section integration, membrane response เทียบ polygonized circumference, parallel-branch bending เทียบ discrete integration, rib network เทียบ assembled springs, annular compliance เทียบ radial integration และ Hertz contact เทียบ bounded Newton refinement

ทุกกรณีประกาศกฎ contact/interface ที่มีชนิดชัดเจนหนึ่งชนิดจาก `bonded`, `sliding_friction`, `bearing_preload` หรือ `hertz_frictional` V1 บันทึกกฎที่ทำงานและสถานะความถูกต้อง แต่ไม่ได้แก้ประวัติ nonlinear contact สามมิติแบบทั่วไป

## ด่านหลักฐาน

ต้องมี discretization 3 ระดับที่เพิ่มเป็นสองเท่าอย่างเคร่งครัด และต้องผ่านด่าน fine response, การเปลี่ยนแปลงสองระดับสุดท้าย, observed order หรือ exact discrete match, force residual, moment residual, energy residual และ solver convergence ค่าที่ไม่ finite และ divergence เป็นผลลัพธ์ invalid โดยห้ามใช้ fallback response

ตัวประเมินบันทึกการคัดกรองความเค้น bending, torsion, axial, hoop, contact และ thermal แบบ fully constrained รวมถึง Euler buckling, yield/plastic-strain proxy, fracture-domain ratio และ synthetic fatigue damage ตัวชี้วัดเหล่านี้เป็นการตรวจสอบขอบเขตจำกัดโดยใช้วัสดุสังเคราะห์ ไม่ใช่ค่ากำลังวัสดุที่รับรองแล้ว

ความเสียหายเปลี่ยน typed connection edge ที่ประกาศจาก `intact` เป็น `failed` ทำให้แรงและโมเมนต์ที่ส่งผ่านเป็นศูนย์ และระบุ functional paths ที่ได้รับผลกระทบ ตัวควบคุม severed-edge จะปฏิเสธแรงส่งผ่านที่ไม่เป็นศูนย์ เกณฑ์ความเสียหายและข้อห้ามการซ่อมหลังเห็นผลถูกตรึงใน configuration

## การทำซ้ำ

```powershell
python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work097/run_a/result.json
python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work097/run_b/result.json --replay-reference artifacts/work097/run_a/result.json
python -m unittest tests.test_generalized_geometry_benchmarks -v
```

## ขอบเขตการอ้างผล

การผ่านยืนยันเพียงพฤติกรรมที่ทำซ้ำได้ของ benchmark ลดรูป 7 กรณีที่ตรึงไว้และการบันทึกการแพร่ความเสียหายเท่านั้น ไม่ได้ยืนยัน topology ใหม่ในอนาคต, stress concentration เฉพาะจุดจาก STEP, shell instability, nonlinear material redistribution, crack growth, fretting, ข้อมูล fatigue จริง, ความสามารถในการผลิต, ความปลอดภัยของรถ หรือการรับเข้าสู่การออกแบบ การเลื่อนระดับผู้สมัครให้สูงกว่านี้ต้องมี mesh ที่สร้างจากเรขาคณิตจริงและหลักฐาน Gmsh/CalculiX หรือเทียบเท่าที่มี fidelity สูงกว่าอย่างอิสระ
