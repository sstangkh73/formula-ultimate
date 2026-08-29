# Research Experiment Protocol v1

ไฟล์ต้นฉบับภาษาอังกฤษ: `RESEARCH_EXPERIMENT_PROTOCOL.md`

Protocol ID: `formula_ultimate_research_experiment_protocol_v1`

สถานะ: Protocol ระยะ Phase 1 ที่ใช้งานอยู่

## วัตถุประสงค์และขอบเขตข้ออ้าง

Protocol นี้เปลี่ยน candidate 3D ที่ประกาศไว้เป็นหลักฐานที่ audit ได้ผ่าน:

```text
versioned declaration
  -> constrained CadQuery 3D B-rep
  -> hashed STEP exchange artifact
  -> FreeCAD import and independent measurement
  -> evidence admission
  -> Level 0 evaluation from FreeCAD-derived properties
  -> falsification review
```

การผ่านรองรับเพียง **geometry-to-Level-0 pipeline coherence** ไม่รองรับข้ออ้าง
เรื่อง physical validation, complete-vehicle feasibility, race performance,
ความปลอดภัย, การผลิต, optimality, novelty หรือ discovery โดย Level 0 ยังเป็น
selection gate เท่านั้น

Protocol ไม่บังคับ conventional vehicle layout หรือรูปทรงที่รู้จัก Candidate
แรกจงใจใช้ grammar `mounting_plate_v1` แบบมีขอบเขตที่มีอยู่ เพราะ repo ปัจจุบัน
ยังไม่มี complete-vehicle grammar, assembly-interface solver หรือระบบ
packaging/collision

## Artifact ของ Protocol

- คำประกาศ protocol:
  `config/experiments/research_experiment_protocol_v1.json`
- คำประกาศ candidate:
  `config/experiments/candidate_fu-c0001.json`
- สัญญารับหลักฐาน:
  `src/formula_ultimate/experiments/research_protocol.py`
- Launcher ที่ทำซ้ำได้: `scripts/run_candidate_001.ps1`
- หลักฐานจากการรัน: `artifacts/work031/FU-C0001/` (Git ignore)

คำประกาศ candidate เป็น input ที่แก้ไม่ได้ภายในการรัน หากเปลี่ยน declaration,
protocol, grammar, adapter หรือ tolerance ต้องเป็น run identity ใหม่ ห้ามเขียน
ผลย้อนหลังเพื่อซ่อนการเปลี่ยน

## Stage Gate ที่บังคับ

| Stage | Input ที่ต้องมี | เงื่อนไขผ่าน | ความล้มเหลวที่สังเกตได้ |
|---|---|---|---|
| `declaration_gate` | protocol และ candidate JSON | ID, version, class, ค่า SI, grammar, control และ tolerance ผ่านการรับ | identity ผิด/ไม่ประกาศ หรือค่า invalid |
| `cadquery_3d_generation` | candidate ที่รับแล้ว | valid CadQuery solid หนึ่งชิ้นโดยไม่มี hidden repair | generation error, invalid shape หรือ solid count ไม่เท่ากับหนึ่ง |
| `step_export_identity` | B-rep ที่สร้างแล้ว | STEP เริ่ม `ISO-10303-21;` และบันทึก size/SHA-256 | ไฟล์หาย/ผิด หรือ hash ไม่ตรง |
| `freecad_import_measurement` | exact STEP artifact | FreeCAD import hash เดียวกันเป็น valid solid หนึ่งชิ้น และรายงาน volume, bounds, centre of mass | import error, invalid shape, hash ผิด, report หาย หรือ solid count ผิด |
| `level0_evidence_admission` | analytical, CadQuery และ FreeCAD evidence | dimensions/volumes ผ่าน tolerance; volume จาก FreeCAD คูณ density ที่ประกาศเป็น mass | tolerance/contract ล้มเหลว และห้าม analytical substitution |
| `falsification_review` | หลักฐานครบทุก stage | บันทึก supporting, contradicting, alternative, missing-evidence และ confidence | review ไม่ครบหรือขยายข้ออ้างเกินหลักฐาน |

ห้าม stage ใดตัดค่าพารามิเตอร์, ซ่อม geometry, แทน FreeCAD evidence ที่หายด้วย
ค่า analytical หรือเปลี่ยน failure เป็น pass แบบเงียบ Runner จะเขียน
`experiment_failure.json` พร้อม stage ที่ล้มเหลวและ process evidence เมื่อผ่าน
ขอบเขตไม่ได้

## ข้อกำหนดการออกแบบการทดลอง

ทุก experiment ต้องประกาศล่วงหน้า:

- ID ของ protocol, experiment, candidate, grammar, component/material และ seed
- preferred hypothesis และขอบเขตข้ออ้าง
- ตัวแปรอิสระ, ตัวแปรตาม, ตัวแปรควบคุม และหน่วย SI
- evidence tolerance และเกณฑ์สำเร็จ/ล้มเหลวที่ชัดเจน
- compute route และตัวตน tool/source/config/repository
- baseline และ budget control ที่ตั้งใจใช้เมื่อจัดอันดับหลาย candidate

ทุกผลต้องรายงานหลักฐานสนับสนุน, หลักฐานขัดแย้ง, คำอธิบายทางเลือก,
หลักฐานที่ขาด และ confidence ความล้มเหลวของ candidate/solver ต้องคงอยู่เป็น
observation ใน dataset

## Candidate `FU-C0001`

`FU-C0001` เป็น bounded component geometry specimen ไม่ใช่รถทั้งคัน ใช้แผ่น
มุมโค้งขนาด `0.200 x 0.120 x 0.008 m`, mounting hole สี่รูที่ประกาศไว้,
central lightening radius `0.025 m` และสมมติฐาน aluminium constant-density
`2700 kg/m^3` บันทึก seed `31001` แม้ grammar ปัจจุบัน deterministic

Preferred hypothesis คือ input ที่ประกาศสามารถผ่านทุก evidence boundary โดย
ไม่มี hidden repair หรือ analytical substitution การรันที่มี candidate เดียว
ไม่ประมาณผลของ design variable และจัดอันดับ design ไม่ได้

Control ของการประเมิน specimen ระดับ Level 0 คือ base vehicle mass `300 kg`,
tractive force `1200 N`, duration `5 s` และ timestep `0.05 s` โดย Level 0 ใช้
เฉพาะ volume ที่ FreeCAD วัดเพื่อ derive component mass

## การรันแรกที่บันทึก

คำสั่ง:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_candidate_001.ps1
```

การรัน Work 031 ครั้งแรกผ่านทั้งหก stage:

| หลักฐาน | ค่าที่บันทึก |
|---|---:|
| STEP bytes | `55,774` |
| STEP SHA-256 | `13881EC14571A6AA8BC8EC3911E46D38C0364ED5691B002B6AB12BF0A0462383` |
| CadQuery volume | `0.0001739968154162849 m^3` |
| FreeCAD 1.1.3 volume | `0.00017399681541628494 m^3` |
| FreeCAD minus CadQuery volume | `5.421010862427522e-20 m^3` |
| FreeCAD solid count / validity | `1 / true` |
| component mass ที่ derive จาก FreeCAD | `0.4697914016239693 kg` |
| Level 0 final speed | `19.968729541866246 m/s` |
| Level 0 final distance | `49.9218238546656 m` |

ผล machine-readable ที่ตรงกันอยู่ที่
`artifacts/work031/FU-C0001/experiment_result.json` STEP hash ยืนยัน artifact
ของ run นี้ ส่วน semantic replay เปรียบเทียบ dimensions และ physical properties
ตาม tolerance เพราะ metadata ของ STEP exporter อาจทำให้ byte เปลี่ยน

## การตีความและกฎ Promotion

ผลรองรับว่า input นี้ผ่านเส้นทาง software/evidence ที่ประกาศบนเครื่องนี้ ไม่ได้
แสดงว่าการตัด material มีประโยชน์ทางโครงสร้างหรือชิ้นส่วนเหมาะกับรถแข่งขัน
CadQuery และ FreeCAD ยังใช้เทคโนโลยี geometry ตระกูล OCCT เหมือนกัน ผลที่ตรงกัน
จึงไม่ใช่ทฤษฎีที่เป็นอิสระ

ห้าม promote `FU-C0001` เป็น design discovery การ promote ในอนาคตอย่างน้อยต้อง
มี interface/load ที่ประกาศ, independent model ที่แรงกว่า, numerical
convergence, manufacturing/assembly/safety evidence และการเทียบ optimized
baseline อย่างยุติธรรมด้วย candidate-evaluation หรือ measured compute budget
เท่ากัน
