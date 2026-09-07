# Whole-Vehicle Integration Intake V1

ไฟล์ต้นฉบับภาษาอังกฤษ: `WHOLE_VEHICLE_INTEGRATION_INTAKE_V1.md`

Status: Implemented เป็น Work 105 ซึ่งเป็น bounded phase แรกสู่ roadmap milestone Work 101

## วัตถุประสงค์และขอบเขตคำกล่าวอ้าง

Intake นี้ป้องกันไม่ให้ subsystem ที่ feasible เฉพาะที่หรือ graph-diverse ถูกเลื่อนเป็น whole-vehicle claim แบบเงียบ ระบบใช้ deterministic portion ที่ตรง identity จาก Work 100 registration V2 รักษา scoped survivor ทุกตัว แยก active functional topology ออกจาก inactive appendage และรายงาน vehicle capabilities/evidence classes ที่ขาด

ผลลัพธ์เป็น analysis-only typed subsystem intake ไม่ใช่ physics solve ใหม่ complete vehicle การตัดสิน `promotion_ready`, whole-vehicle admission, race comparison, technology-discovery result หรือ physical validation Work 101 ยังคงเป็น program milestone ที่ต้องมี integration และ stronger evidence ในอนาคต

## วิธี active path

สำหรับทุก original edge และ field ระบบรวม maximum absolute flow บน Work 100 subdivision ระดับละเอียดสุด:

```text
mechanical_activity = max(abs(edge force)) / 5000 N
thermal_activity    = max(abs(edge heat flow)) / 30 W
```

Edge active ในหนึ่ง domain เฉพาะเมื่อ relative activity มากกว่า `1e-8` และ coupled active edge ต้อง active ทั้งสอง domain ระบบนำ subdivision node labels ออกโดยกู้ first/last endpoints ของ original edge Inactive edge ยังคงอยู่ใน report แต่ไม่รวมใน active topology

ระบบ canonicalize active simple graph เหนือ node permutations ทุกแบบจนถึง frozen bound แปด active nodes จึงได้ identifier-independent exact unlabelled simple-graph identity ภายในขอบเขตนี้ Graph ที่ใหญ่เกินจะ fail แทนการ fallback ไปใช้ชื่อ Identity นี้ตั้งใจไม่ encode source/sink coloring, geometry, parallel-edge multiplicity หรือ direction จึงเป็น intake descriptor ไม่ใช่ universal mechanism proof

Candidate ทุกตัวจับคู่กับ fixed control seed เดียวกัน Candidate เป็น `functional_mechanism_candidate` เฉพาะเมื่อ:

1. เป็น Work 100 `candidate_survivor` อยู่แล้ว
2. coupled active-topology identity ต่างจาก paired fixed control
3. absolute coupled-utilization difference อย่างน้อย frozen meaningful threshold `0.05`

Difference ต้องมากกว่าผลรวม numerical error ของ candidate และ fixed ด้วยจึงเรียก detectable Declared graph difference ที่ edge เพิ่ม inactive จะเป็น `declared_topology_only_inactive_appendage` Geometry response ที่ตรวจพบแต่ active topology เดิมคงเป็น shape-response variant Meaningful difference ไม่ได้แปลว่า improvement อัตโนมัติ เพราะ objective ที่ลงทะเบียนคือ minimize utilization

## Technology-neutral integration coverage

Required capabilities มาจาก functional vehicle contract เดิมโดยตรง ไม่ได้มาจากชื่อ component หรือ layout แบบดั้งเดิม:

- energy storage และ conversion
- power transmission และ ground propulsion
- direction control และ braking
- load structure และ heat rejection
- controller

Work 100 ให้ credible local evidence เฉพาะ `load_structure` Thermal conduction path ไม่ได้พิสูจน์ heat-rejection capability และ Work 100 ให้ scoped `candidate_survivor` กับ holdout evidence แต่ยังไม่มี independent higher fidelity, safety, coupled transient, energy, contact, failure หรือ optimized-baseline evidence

## ผล Work 105

Input identities ตรงกับ Work 100 registration `2c3aaa21ffb6ed36da532493c82c6e1f0195b13990180dc5d055c75fb47bdd45` และ deterministic evidence `652ba7d9db9d76ed841d5b2c24af421075cc2d266a9098bc065fe4a8ac45da61` Final-source run C/D ให้ exact result SHA-256 `559fb55a4513003af35e302ddff9120ece830b88d8f19f62188a052c3411229e`

- Scoped survivors ทั้งสิบยัง eligible เป็น typed load-structure subsystem inputs
- Functional-mechanism candidates: `0`
- Declared-topology inactive appendages: `4` คือ `GRAPH_ONLY` สองและ `JOINT_MORPHOLOGY_CONTROLLER` สอง candidates
- Shape-response variants: `4` คือ `MORPHOLOGY_ONLY` สองและ `RANDOM_CONTROL` สอง candidates
- `RANDOM_CONTROL` seed `7` เกิน absolute meaningful threshold `0.05` ด้วยค่า `+0.0586275`; utilization ต้อง minimize จึงเป็น meaningful worsening ไม่ใช่ improvement และ active topology ยังเหมือนเดิม
- ขาด vehicle capabilities `8` และ program-exit evidence classes `7`
- สถานะสุดท้าย `blocked_incomplete_capability_and_evidence_coverage`; `work101_program_exit = false`; ไม่ได้สร้าง whole-vehicle candidate

Preferred hypothesis ว่า Work 100 มี active-topology functional-mechanism candidate ถูกหักล้างที่ intake fidelity นี้ แต่ไม่ได้ลบ local feasibility หรือ geometry-response evidence

## การทำซ้ำ

```powershell
$env:PYTHONPATH = Join-Path $PWD 'src'
python -m unittest tests.test_integration_intake -v
python scripts/experiments/run_integration_intake.py --output artifacts/work105/run_c/result.json
python scripts/experiments/run_integration_intake.py --output artifacts/work105/run_d/result.json --replay-reference artifacts/work105/run_c/result.json
```

Generated evidence ใต้ `artifacts/work105/` ถูก ignore โดย Git Integration phase ต่อไปต้องเพิ่ม survivor types และ evidence ที่ขาด ห้าม reclassify negative intake นี้หรือกำหนด conventional vehicle layout เพื่อให้ coverage ง่ายขึ้น
