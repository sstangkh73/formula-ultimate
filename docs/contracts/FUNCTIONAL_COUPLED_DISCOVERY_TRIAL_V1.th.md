# การทดลองค้นพบเชิงหน้าที่และแบบควบคู่ V1

ไฟล์ต้นฉบับภาษาอังกฤษ: `FUNCTIONAL_COUPLED_DISCOVERY_TRIAL_V1.md`

สถานะ: Implemented และรันภายใต้ Work 100 registration V2

## ขอบเขตคำกล่าวอ้าง

การทดลองนี้ประเมินเฉพาะ subsystem แบบมีขอบเขตจาก source ถึง sink ซึ่งแทนด้วย scalar axial-force network และ steady-state thermal-resistance network เท่านั้น `candidate_survivor` หมายถึง morphology ผ่าน refined numerical physics, computational process envelope, งาน holdout ที่ไม่เคยใช้ปรับระบบ และ exact ledger replay ตาม registration ไม่ได้ยืนยันพฤติกรรมโครงสร้างสามมิติเต็มรูป ความเป็นไปได้ของรถทั้งคัน สมรรถนะการแข่งขัน ความใหม่ของเทคโนโลยี ความเป็นไปได้ในการผลิต สถานะ `promotion_ready` หรือ physical validation

สมบัติวัสดุเป็น declared linear isotropic study model ไม่ใช่ค่าที่ผ่าน certification ส่วน process gate ตรวจเพียง minimum diameter, part count และ coordinate span ไม่ใช่การสาธิตการผลิต controller gene แบบ passive ถูกบันทึกไว้แต่ไม่มี causal path ใน solver นี้ จึงไม่ได้รับ performance credit

## Geometry, field และสมการ

ทุก edge ของ genome เป็นสมาชิกเส้นตรงยาว `L` มีรัศมีปลาย `r_a` และ `r_b` เปลี่ยนเชิงเส้น พื้นที่หน้าตัดวงกลมคือ `A(x) = pi r(x)^2` fixed interface ที่มีทั้ง domain `load` และ `thermal` จะรวม network node เข้าด้วยกัน source และ sink อย่างละหนึ่ง terminal ถูกผูกด้วย ancestry ที่ลงทะเบียน และ material identifier ของทุก part ต้องตรงกับ study model ที่ลงทะเบียน

Primary evaluator แบ่งทุก edge เป็น midpoint segment จำนวน `n` สำหรับ segment ยาว `Delta x` และพื้นที่ `A_i` ความต้านทานเชิงกลและความร้อนคือ:

```text
R_mechanical,i = Delta x / (E A_i)
R_thermal,i    = Delta x / (k A_i)
```

Conductance matrix ที่ประกอบแล้วกำหนด source potential เป็นศูนย์และใส่แรง `F` หรืออัตราความร้อน `Q` ที่ sink ระบบเก็บ nodal displacement/temperature, segment force/heat flow, source reaction, free-node residual, global equilibrium residual และ energy residual ที่ refinement ทั้งสามระดับ Maximum axial stress ใช้พื้นที่ปลายที่น้อยที่สุดของ original edge เพื่อความ conservative ส่วน coupled utilization คือ:

```text
U = max(displacement / displacement_limit,
        maximum_axial_stress / yield_strength,
        temperature_rise / temperature_limit)
```

`U <= 1` เป็น `physically_feasible` เฉพาะภายใน model นี้ Numerical admission ยังบังคับให้ last-two-refinement relative change, conservation residual และ primary/reference disagreement ไม่เกินค่าที่ลงทะเบียน

Reference implementation แยกต่างหาก integrate รัศมีวงกลมที่เปลี่ยนเชิงเส้นแบบ exact:

```text
R_exact = L / (coefficient pi r_a r_b)
```

Reference ประกอบ edge resistance แยกเอง แต่ยังใช้สมการที่ประกาศ geometry genotype และ NumPy linear-algebra runtime เดียวกัน จึงเป็น cross-method corroboration ไม่ใช่ independent software stack หรือ experiment

Geometry-derived volume ใช้สมการ conical frustum `V = L pi (r_a^2 + r_a r_b + r_b^2) / 3`; mass และสัดส่วนต่อ reference vehicle `800 kg` เป็น feedback เท่านั้น CAD execution ยืนยัน geometry identity และ measurement แยกต่างหาก แต่ network สร้างจาก gene ชุดเดียวกับที่สร้าง CAD ไม่ใช่ volumetric finite-element mesh

## การทดลองที่ลงทะเบียน

- Treatments: `FIXED_TOPOLOGY`, `RANDOM_CONTROL`, `GRAPH_ONLY`, `MORPHOLOGY_ONLY`, `JOINT_MORPHOLOGY_CONTROLLER`
- Paired seeds: `7`, `19`; `n = 2` เป็น descriptive และใช้อนุมาน superiority ไม่ได้
- Training task: `5000 N`, `30 W`, displacement limit `0.0002 m`, temperature-rise limit `160 K`
- Holdout task: `6000 N`, `35 W`, ใช้ limit เดิมที่ลงทะเบียน และไม่มี holdout feedback
- Proxy refinements: `[1, 2, 4]`; refined/holdout refinements: `[4, 8, 16]`
- Limits: refinement change `0.005`, exact-reference error `0.005`, conservation residual `1e-10`, coupled utilization `1.0`
- Study material: density `2700 kg/m^3`, `E = 70 GPa`, yield strength `250 MPa`, conductivity `170 W/(m K)`
- Process envelope: diameter อย่างน้อย `0.004 m`, ไม่เกิน `8` parts, coordinate span ไม่เกิน `0.5 m`
- Runtime: Python `3.12.14`, CadQuery `2.8.0`, NumPy `2.5.2`, serial worker หนึ่งตัว

Registration V1 SHA-256 `aa5012d3b0a85b9f6c42b1ede5561681713cb9c9832577f6d2bf88e09d96a871` หยุดโดยยังไม่มี holdout หรือ survivor outcome เพราะ proxy label แปดรายการ unresolved และ audit reporter เดิมต้องการ Boolean proxy label โดยไม่ได้ทำต่อจาก partial ledger Registration V2 SHA-256 `2c3aaa21ffb6ed36da532493c82c6e1f0195b13990180dc5d055c75fb47bdd45` คง scientific threshold, task, treatment, seed และ selection rule ทุกค่า พร้อมกำหนด not-estimable audit result สำหรับ unresolved proxy label แบบล่วงหน้าอย่างชัดเจน

## ผล admitted

V2 run A และ B ที่เริ่มแยกจากศูนย์ให้ deterministic evidence SHA-256 เดียวกันคือ `652ba7d9db9d76ed841d5b2c24af421075cc2d266a9098bc065fe4a8ac45da61` Candidates ทั้งสิบผ่าน refined training task, process envelope, holdout task และ replay gate จึงมี scoped `candidate_survivor` สิบรายการ พร้อม accounting ที่ admissible Refined error ทุกค่าต่ำกว่า `0.000536` และ holdout utilization ต่ำกว่า `0.696`

Audit สุ่มครบ treatment/seed/representation strata ทั้งสิบ มี proxy label แบบ Boolean เพียงสองรายการ ขณะที่แปดรายการคง `numerically_unresolved` ดังนั้น false-negative และ false-positive rate เป็น `null` ไม่ใช่ศูนย์ Refined reference ทั้งสิบ feasible นี่เป็นข้อจำกัดด้าน proxy resolution ไม่ใช่หลักฐานว่า proxy แม่นหรือไม่แม่น

Graph-only และ joint treatments สร้าง signature ต่างจาก fixed topology จึงผ่าน survivor-success condition ที่ลงทะเบียน แต่ primary response ต่างจาก fixed control เพียง floating-point round-off (`mean difference ประมาณ -1.51e-14`) เพราะกิ่งที่เพิ่มแทบไม่มี source-to-sink flow Morphology-only มี paired difference คนละทิศและ mean `-0.00312`; random-control mean difference `+0.01593` ดังนั้นการทดลองนี้แสดง executable distinct architectures และ scoped feasible survivors แต่ไม่แสดง functional superiority, useful load-path effect ใหม่, race advantage หรือ technology discovery

## การทำซ้ำ

```powershell
$env:PYTHONPATH = Join-Path $PWD 'src'
python -m unittest tests.test_functional_discovery -v
& '.tools/cadquery-mcp/Scripts/python.exe' scripts/experiments/run_functional_discovery.py --output-dir artifacts/work100/run_v2_a
& '.tools/cadquery-mcp/Scripts/python.exe' scripts/experiments/run_functional_discovery.py --output-dir artifacts/work100/run_v2_b --replay-reference artifacts/work100/run_v2_a/result.json
```

Generated evidence ใต้ `artifacts/work100/` ถูก ignore โดย Git ตามตั้งใจ ส่วน registration, source, tests, contract และ work logs ที่ commit แล้วเก็บ specification ที่ทำซ้ำได้และ identity ที่รายงานอย่างแน่นอน
