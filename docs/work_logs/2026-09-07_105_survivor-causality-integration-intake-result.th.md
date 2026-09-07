# ผล Work 105: Survivor Causality และ Whole-Vehicle Integration Intake V1

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-07_105_survivor-causality-integration-intake-result.md`

วันที่: 2026-09-07 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์

Work 105 ทำ implementation phase แรกแบบมีขอบเขตสู่ roadmap milestone Work 101 สำเร็จ โดยเพิ่ม fail-closed intake ที่ตรวจ exact Work 100 V2 deterministic identity รวม mechanical/thermal flow ระดับละเอียดสุดตาม original edge ตัด inactive appendage ออกจาก identifier-independent active-topology identity เปรียบเทียบทุก candidate กับ paired fixed control และรายงาน technology-neutral capability/evidence coverage

ผล intake เป็นเชิงลบอย่างถูกต้อง: `blocked_incomplete_capability_and_evidence_coverage` และ `work101_program_exit = false` Work 100 subsystem survivors ทั้งสิบยังถูกเก็บและ typed เป็น `load_structure` inputs ที่เป็นไปได้ แต่ไม่ได้สร้าง whole-vehicle candidate และไม่ได้ promote ตัวใด

## ผลด้าน causality

- `functional_mechanism_candidate_count = 0`
- Graph/joint candidates สี่รายการเป็น `declared_topology_only_inactive_appendage`: แต่ละรายการมี coupled active edges เดิมสามเส้นและเพิ่ม inactive edge หนึ่งเส้น Response difference จาก paired fixed control มีเพียงประมาณ `1e-14`
- Candidates สี่รายการเป็น shape-response variants ที่ active topology ไม่เปลี่ยน ได้แก่ morphology-only สองและ random-control สอง cases
- `RANDOM_CONTROL` seed `7` มี meaningful absolute utilization difference `+0.0586275358` เพราะ utilization ต้อง minimize ค่านี้จึงแย่ลง ไม่ใช่ improvement
- Shape differences อื่นที่ตรวจพบยังต่ำกว่า frozen meaningful threshold `0.05`
- Preferred hypothesis ว่า Work 100 survivor มี task-relevant active-topology mechanism ถูกหักล้างที่ intake fidelity นี้ โดย local feasibility และ geometry-response evidence ยังอยู่ครบ

Whole-vehicle coverage มีเพียง `load_structure` ยังขาด capabilities แปดรายการ: braking, controller, direction control, energy converter, energy storage, ground propulsion, heat rejection และ power transmission และขาด program-exit evidence classes เจ็ดรายการ: contact, coupled transient, energy, failure, independent higher fidelity, optimized baseline และ safety Work 100 holdout evidence ยังคงอยู่ แต่ formula reference ที่ใช้ runtime ร่วมกันไม่ได้ถูกเปลี่ยนป้ายเป็น independent higher fidelity

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/experiments/integration_intake.py`
- `config/experiments/work101_integration_intake_v1.json`
- `scripts/experiments/run_integration_intake.py`
- `tests/test_integration_intake.py`
- `docs/contracts/WHOLE_VEHICLE_INTEGRATION_INTAKE_V1.md` และไฟล์คู่ภาษาไทย
- plan/result นี้และไฟล์คู่ภาษาไทย

Generated reports ใต้ `artifacts/work105/` ยังคงถูก ignore โดย Git; `run_c` และ `run_d` เป็น final-source exact pair

## หลักฐาน validation ที่แน่นอน

1. `python -m unittest tests.test_integration_intake -v`
   - Exit `0`; `Ran 9 tests in 0.005s`; `OK`
2. Work 105 final-source run C และ independent exact replay D
   - ทั้งสอง exit `0`
   - ทั้งสองรายงาน ten candidates, zero mechanism candidates, blocked intake และ `work101_program_exit = false`
   - Exact result SHA-256: `559fb55a4513003af35e302ddff9120ece830b88d8f19f62188a052c3411229e`
3. Targeted Works 098-100, functional vehicle, release/promotion และ whole-mechanical audit regression
   - Exit `0`; `Ran 114 tests in 25.563s`; `OK`
4. `python -m compileall -q src scripts tests`
   - Exit `0`
5. `python -m unittest discover -s tests -q`
   - Exit `0`; `Ran 794 tests in 332.058s`; `OK (skipped=8)`

## การตัดสินใจ ข้อจำกัด และงานต่อไป

- Active หมายถึง relative mechanical และ thermal flow มากกว่า `1e-8`; ค่าเท่ากันเป็น inactive ไม่มีการเปลี่ยน threshold หลังเห็นผล
- Canonicalization เป็น exact unlabelled simple graph จนถึงแปด active nodes โดยตั้งใจไม่รวม source/sink coloring, direction และ parallel-edge multiplicity จึงเป็น intake descriptor ไม่ใช่ complete mechanism proof
- Input เป็น admitted Work 100 evidence เดิม Work 105 เพิ่ม analysis ไม่ได้เพิ่ม physical evidence ใหม่
- Negative intake เป็นผล fail-closed ที่ถูกต้องและไม่ทำให้ work item เป็น `Stopped`
- Phase ถัดไปควรสร้างหรือรับ typed subsystem survivors เพิ่มพร้อม causal active paths ก่อนพยายาม assembly ห้ามบังคับ conventional layout หรือ reuse blocked whole-mechanical candidate โดยไม่มี geometry/evidence ใหม่

Validated commit hash จะรายงานใน final handoff หลัง mandatory exact-scope commit สำเร็จ
