# ผลงาน 031: Research Experiment Protocol และ Candidate 001

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_031_research-experiment-protocol-candidate-001-result.md`

สถานะ: เสร็จสมบูรณ์

## ผลลัพธ์

สร้างสัญญาแบบมีเวอร์ชัน
`formula_ultimate_research_experiment_protocol_v1` และรัน `FU-C0001` ผ่าน
เส้นทาง local ครบ:

```text
candidate declaration
  -> CadQuery constrained 3D B-rep
  -> hashed STEP
  -> FreeCAD 1.1.3 import and measurement
  -> analytical/CadQuery/FreeCAD evidence admission
  -> FreeCAD-derived mass
  -> Level 0 point-mass evaluation
  -> falsification review
```

ทั้งหก stage ที่บังคับผ่าน ผลนี้รองรับเพียง geometry-to-Level-0 pipeline
coherence `FU-C0001` เป็น bounded component geometry specimen ไม่ใช่ complete
vehicle หรือ race design ที่ผ่าน physical validation

## ไฟล์ที่เปลี่ยน

### คำประกาศ Protocol และ Candidate

- `config/experiments/research_experiment_protocol_v1.json`
- `config/experiments/candidate_fu-c0001.json`

ไฟล์เหล่านี้ประกาศ identity, ลำดับ stage, ขอบเขตข้ออ้าง, นโยบายห้าม silent
correction, hypothesis, variables, controls, tolerances และ failure criteria

### สัญญาหลักฐานและเส้นทางที่รันได้

- `src/formula_ultimate/experiments/research_protocol.py`
- `src/formula_ultimate/experiments/__init__.py`
- `scripts/cad/run_research_candidate.py`
- `scripts/run_candidate_001.ps1`
- `scripts/cad/generate_mounting_plate.py`

Generator รับได้ทั้ง multi-candidate config ของ Work 006 เดิมหรือ candidate
เดี่ยว Runner ใหม่เก็บ boundary ที่ล้มเหลวเป็น `experiment_failure.json`,
ยืนยัน STEP ทั้งขอบเขต CadQuery และ FreeCAD และบันทึก
config/source/repository/tool/process evidence

### Test และเอกสาร

- `tests/test_research_protocol.py`
- `docs/research/RESEARCH_EXPERIMENT_PROTOCOL.md`
- `docs/research/RESEARCH_EXPERIMENT_PROTOCOL.th.md`
- แผน/ผล Work 031 ภาษาอังกฤษและไทย

หลักฐานที่สร้างยังถูก ignore ภายใต้ `artifacts/work031/FU-C0001/`

## การตัดสินใจสำคัญ

1. **เริ่มจาก geometry-evidence specimen ไม่อ้างว่าเป็นรถทั้งคัน** เพราะ repo
   ยังไม่มี complete-vehicle grammar, assembly-interface solver หรือระบบ
   packaging/collision
2. **รักษา protocol ให้เป็นกลางต่อเทคโนโลยีและ layout** แผ่นที่มีขอบเขตเป็น
   test surface แรก ไม่ใช่ข้อกำหนด architecture ของรถในอนาคต
3. **ใช้ค่าจาก STEP ที่ FreeCAD import จริงเพื่อหา mass สำหรับ Level 0** ค่า
   analytical และ CadQuery เป็น gate เท่านั้น ห้ามแทน FreeCAD evidence ที่หาย
4. **ให้ boundary ที่ล้มเหลวเป็นข้อมูล** Runner บันทึก stage, exception,
   process command, output, exit code และ wall time แทนการซ่อมหรือ retry
   geometry แบบเงียบ
5. **แยก artifact authentication จาก semantic replay** แต่ละ run บันทึก exact
   STEP hash ส่วน geometry/property ข้าม run เทียบตาม tolerance เพราะ STEP
   exporter metadata เปลี่ยน byte ได้

## การทดลอง Candidate 001

### Design ที่ประกาศล่วงหน้า

- Candidate: `FU-C0001`
- Class: `bounded_component_geometry_specimen`
- Grammar: `mounting_plate_v1`
- Seed: `31001`
- Envelope: `0.200 x 0.120 x 0.008 m`
- Central lightening radius: `0.025 m`
- สมมติฐาน density: `2700 kg/m^3`
- Level 0 controls: base mass `300 kg`, force `1200 N`, duration `5 s`,
  timestep `0.05 s`

Preferred hypothesis คือ candidate ที่ประกาศผ่าน evidence boundary ทั้งหมดได้
โดยไม่มี hidden repair หรือ analytical substitution เพราะการรันมี candidate
เดียว จึงไม่ประมาณผลของตัวแปรอิสระและจัดอันดับ design ไม่ได้

### หลักฐานสุดท้ายที่บันทึก

| หลักฐาน | ค่า |
|---|---:|
| Status | `passed` |
| CadQuery solid count / validity | `1 / true` |
| FreeCAD solid count / validity | `1 / true` |
| STEP bytes | `55,774` |
| STEP SHA-256 | `13881EC14571A6AA8BC8EC3911E46D38C0364ED5691B002B6AB12BF0A0462383` |
| CadQuery volume | `0.0001739968154162849 m^3` |
| FreeCAD volume | `0.00017399681541628494 m^3` |
| FreeCAD minus CadQuery volume | `5.421010862427522e-20 m^3` |
| FreeCAD analytical relative residual | `3.1155805061476737e-16` |
| component mass ที่ derive จาก FreeCAD | `0.4697914016239693 kg` |
| Level 0 mass รวม | `300.469791401624 kg` |
| Level 0 final speed | `19.968729541866246 m/s` |
| Level 0 final distance | `49.9218238546656 m` |

FreeCAD version คือ `1.1.3` การรันสุดท้ายบันทึก CadQuery generation wall time
`7.05679349997081 s` และ FreeCAD import wall time `0.643542799982242 s`
หลักฐาน machine-readable อยู่ที่
`artifacts/work031/FU-C0001/experiment_result.json`

Replay identity จากการรันสุดท้าย:

- protocol config SHA-256:
  `BBF71CE921E4BFB1B876DC690D2FC5D216F72A3EE13879A3D59BC3D2E8A418E2`
- candidate config SHA-256:
  `1CC3AD2E9083F1502D997367F22CA05B8D83DADE4A23ED2C77291653B2642267`
- repository commit ที่มีอยู่ตอนรัน:
  `557f20570158b96bdcd60f5d3a5da69726e0cb05`
- worktree dirty ระหว่างรัน: `true` เพราะ Work 031 ยังไม่ commit

ผลยังบันทึก SHA-256 ของ source ที่ execute ทุกไฟล์ ทำให้ dirty-worktree run
ยังระบุตัวตนได้

## Falsification Review

- หลักฐานสนับสนุน: CadQuery สร้าง valid solid หนึ่งชิ้น; FreeCAD import exact
  STEP hash เป็น valid solid หนึ่งชิ้น; การวัด analytical/CadQuery/FreeCAD ผ่าน
  tolerance; Level 0 ใช้ mass ที่ derive จาก FreeCAD
- หลักฐานขัดแย้ง: ไม่มีภายใน metric เรื่อง pipeline coherence ที่ประกาศ
- คำอธิบายทางเลือก: CadQuery และ FreeCAD ใช้ geometry ตระกูล OCCT เหมือนกัน;
  Level 0 เป็นสมการ added-point-mass และไม่บอก structural utility
- หลักฐานที่ขาด: complete-vehicle geometry/assembly, loads, FEA, fatigue, CFD,
  thermal, manufacturing, safety, empirical evidence, candidate หลายตัว และ
  fair optimized baseline
- Confidence: สูงสำหรับการรัน pipeline local นี้; ไม่มีสำหรับ physical
  suitability หรือ race performance

## คำสั่งตรวจสอบและผลที่แน่นอน

### Focused protocol tests

คำสั่ง:

```powershell
py -3.14 -m unittest tests.test_research_protocol -v
```

Exit code: `0`

ผล: `Ran 6 tests ... OK` ครอบคลุม protocol/declaration admission, การปฏิเสธ
silent repair, internal ID mismatch, preregistration ที่หาย, tolerance ที่ไม่
finite, exact STEP/FreeCAD mass admission และ hash mismatch

### Pipeline Candidate 001

คำสั่ง:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_candidate_001.ps1
```

Exit code: `0`

ผล: candidate `FU-C0001`, status `passed`, claim level
`geometry-to-level0 pipeline coherence only`, STEP SHA-256
`13881EC14571A6AA8BC8EC3911E46D38C0364ED5691B002B6AB12BF0A0462383`

### Full repository regression

คำสั่ง:

```powershell
py -3.14 -m unittest discover -s tests -q
```

Exit code: `0`

ผล: final rerun `Ran 268 tests in 36.036s ... OK`

### Work 006 backward-compatibility regression

คำสั่ง:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work006.ps1
```

Exit code: `0`

ผล: valid candidate ทั้งสามผ่าน, deliberate invalid candidate ถูกปฏิเสธก่อน
CadQuery และ monotonic check ทั้งสี่ยังเป็น `true`

### Static และ repository checks

คำสั่ง:

```powershell
py -3.14 -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Exit code: `0`, `0` และ `0` ในลำดับ final validation/staging

ผล: Python compile ผ่าน, ไม่พบ whitespace error และ staged scope มีเฉพาะไฟล์
Work 031 ที่ระบุ

## ข้ออ้างที่หลักฐานรองรับ

- Repo มี research experiment protocol แบบมีเวอร์ชันที่ machine-readable และ
  evidence runner เฉพาะ candidate แล้ว
- `FU-C0001` ผ่านเส้นทาง local `3D -> STEP -> FreeCAD -> Level 0` จริง
- replay และ audit ผลได้จาก config, hash, version, process evidence, source
  identity และ structured review

## ข้ออ้างที่หลักฐานไม่รองรับอย่างชัดเจน

- `FU-C0001` ไม่ใช่ complete vehicle, optimized design, discovery หรือ
  component ที่ผ่าน physical validation
- Level 0 ไม่พิสูจน์ structural, aerodynamic, thermal, manufacturing,
  assembly, collision, safety หรือ real race performance
- ความตรงกันของ CadQuery/FreeCAD ไม่ใช่ geometric theory ที่อิสระเต็มที่ เพราะ
  ทั้งคู่ใช้เทคโนโลยีตระกูล OCCT
- ไม่มี fair multi-candidate หรือ optimized-baseline comparison

## สิ่งที่ต่างจากแผน

วัตถุประสงค์หลักไม่เปลี่ยน Focused protocol suite มีหก test จากเดิมที่ไม่ได้
กำหนดจำนวน และ generalized generator เดิมให้น้อยที่สุดเพื่อรับคำประกาศ
candidate เดี่ยว พร้อมรักษาและรันเส้นทาง Work 006 เดิมครบ

## งานต่อไป

1. กำหนด component interface/load semantics และ solver-ready promotion
   contract ก่อนถามคำถามด้านโครงสร้าง
2. เพิ่ม candidate ที่สองเฉพาะเมื่อประกาศ baseline role, equal compute budget,
   comparison metric และ falsification target ชัดเจน
3. สร้าง complete-vehicle geometry/assembly/packaging contract ก่อนเรียก
   specimen `FU-Cxxxx` ในอนาคตว่า vehicle candidate
4. Promote เฉพาะ candidate ที่ evidence ครบไป independent higher fidelity
   และห้ามสรุป discovery จาก Level 0 เพียงอย่างเดียว
