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

ต้องมี discretization 3 ระดับที่เพิ่มเป็นสองเท่าอย่างเคร่งครัด และผ่าน fine response, การเปลี่ยนแปลงสองระดับสุดท้าย, observed order หรือ exact discrete match, ความสอดคล้องสมดุล/พลังงาน constitutive แบบสเกลาร์ และ scalar solver convergence ค่าที่ไม่ finite และ divergence เป็น invalid โดยห้าม fallback Work 103 แก้คำอธิบายด่าน force/moment/energy เดิม: adapters ลดรูปเหล่านี้ไม่ได้กู้คืน field reactions อย่างอิสระ

`evaluator_version=generalized_geometry_equations_v2` แยกผลที่แก้แล้วจาก Work 097 เดิม ค่า `force_residual_relative`, `moment_residual_relative` และ `energy_residual_relative` เปลี่ยนเป็น `null` พร้อม `field_balance_status=not_computed_no_independent_field_reactions` และ `full_balance_validated=false` หมายถึงไม่มีหลักฐาน field ไม่ใช่ residual ศูนย์หรือผ่านด่านสมดุล ตัวตัดสินปฏิเสธค่าศูนย์แบบเก่า ฟิลด์ที่หาย scope/version ที่เปลี่ยน ค่า energy/reference error ปลอม และลำดับ refinement ผิด

หลักฐานสเกลาร์ใช้ q = K*u^p โดย K มาจากโมเดล/discrete compliance ก่อนแก้ u ไม่ใช่หา K จาก q/u ภายหลัง ค่า `generalized_equilibrium_residual_relative` คือ abs(K*u^p-q)/q ส่วน `constitutive_energy_residual_relative` เทียบพลังงานสะสม K*u^(p+1)/(p+1) กับงานของ quasistatic ramp ที่กำหนด q*u/(p+1) งานนี้สมมติให้ ramp มีรูป power law เดียวกัน ไม่ใช่ประวัติโหลดที่วัดอิสระ ทั้งสองเป็นการตรวจความสอดคล้องของกฎสเกลาร์เดียวกัน ไม่ใช่ independent validation ใช้ tolerance force/energy เดิมกับ scalar checks นี้ ส่วน tolerance moment เดิมใช้ยืนยันสมดุลโมเมนต์ไม่ได้ Newton รายงานประวัติ residual/iteration ที่ทำจริง และจะ converge เมื่อ residuals <= 1e-12 หากงบหมดแล้วยังไม่ converge ต้องคง invalid

โมเดลเชิงเส้นใช้ p = 1 ส่วน Hertz normal proxy ใช้ p = 3/2, E* = E/[2(1-nu^2)], K = (4/3)*E*sqrt(R*), a = (3*F*R*/(4*E*))^(1/3) และ p0 = 3*F/(2*pi*a^2) การยุบตัวและความดันสัมผัสใช้ E* กับ R* เดียวกัน R* คือ sampled bend-radius proxy ที่ประกาศ หรือใช้ sampled thickness เฉพาะเมื่อไม่มี radius โดยไม่ clamp ไปเท่าความหนาเงียบ ๆ สมมติวัสดุยืดหยุ่น isotropic เหมือนกันและบริเวณสัมผัสปกติเล็กไร้แรงเสียดทาน ชื่อ typed interface แบบ frictional ไม่ได้เพิ่มการแก้แรงสัมผัสแนว tangential ดู [CompuTiX Hertz theory](https://computix.gitlabpages.inria.fr/computix/db/d6e/group__Hertz.html)

อินทิเกรต F = K*delta^(3/2) ได้ U = (2/5)*K*delta^(5/2) หรือ (2/5)*F*delta เมื่อสมดุล ไม่ใช่ (1/2)*F*delta การอนุมานนี้สมมติโหลดยืดหยุ่น quasistatic ไม่มีการสูญเสีย พลังงานจากแรงมีหน่วย J ส่วนงานจากความดัน shell มีหน่วย J/m^2 เพราะความดันคูณการกระจัดเป็นพลังงานต่อพื้นที่ ไม่ใช่พลังงานรวมของ shell Newton เริ่มจากครึ่งหนึ่งของ indentation เชิงวิเคราะห์เพื่อ benchmark จำนวน iteration แบบจำกัดเท่านั้น ไม่ใช่ contact solver อิสระ

ตัวประเมินบันทึกการคัดกรองความเค้น bending, torsion, axial, hoop, contact และ thermal แบบ fully constrained รวมถึง Euler buckling, yield/plastic-strain proxy, fracture-domain ratio และ synthetic fatigue damage ตัวชี้วัดเหล่านี้เป็นการตรวจสอบขอบเขตจำกัดโดยใช้วัสดุสังเคราะห์ ไม่ใช่ค่ากำลังวัสดุที่รับรองแล้ว

ความเสียหายเปลี่ยน typed connection edge ที่ประกาศจาก `intact` เป็น `failed` ทำให้แรงและโมเมนต์ที่ส่งผ่านเป็นศูนย์ และระบุ functional paths ที่ได้รับผลกระทบ ตัวควบคุม severed-edge จะปฏิเสธแรงส่งผ่านที่ไม่เป็นศูนย์ เกณฑ์ความเสียหายและข้อห้ามการซ่อมหลังเห็นผลถูกตรึงใน configuration

## การทำซ้ำ

```powershell
python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work103/run_a/result.json
python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work103/run_b/result.json --replay-reference artifacts/work103/run_a/result.json
python -m unittest tests.test_generalized_geometry_benchmarks -v
```

## ขอบเขตการอ้างผล

เก็บ outputs Work 097 เดิมไว้โดยไม่แก้ การทำซ้ำให้ได้ identity เดิมต้องใช้ implementation ในอดีต Work 103 ไม่เปลี่ยน input configuration โหลด thresholds หรือ source identities ของ Work 096

การผ่านยืนยันเพียงพฤติกรรมที่ทำซ้ำได้ของ benchmark ลดรูป 7 กรณีที่ตรึงไว้และการบันทึกการแพร่ความเสียหายเท่านั้น ไม่ได้ยืนยัน topology ใหม่ในอนาคต, stress concentration เฉพาะจุดจาก STEP, shell instability, nonlinear material redistribution, crack growth, fretting, ข้อมูล fatigue จริง, ความสามารถในการผลิต, ความปลอดภัยของรถ หรือการรับเข้าสู่การออกแบบ การเลื่อนระดับผู้สมัครให้สูงกว่านี้ต้องมี mesh ที่สร้างจากเรขาคณิตจริงและหลักฐาน Gmsh/CalculiX หรือเทียบเท่าที่มี fidelity สูงกว่าอย่างอิสระ
