# ผลงาน 053: ตัวประเมินทั้งคันแบบละเอียดด้วย section force

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-30_053_section-force-refined-evaluator-result.md`

## ผลลัพธ์

ตัวประเมินที่แก้ observable แล้วพร้อมใช้ภายในขอบเขต linear-elastic beam-network ที่ประกาศไว้ analytical benchmark ละเอียดสุดมี error สูงสุด `3.4276%`; candidate states 54 ชุดสร้าง isolated-section CalculiX processes 162 ครั้ง; negative controls ทั้ง 7 ชุดทำงานตามคาด; deterministic project replay ตรงกันทุกบิต candidate 7 จาก 9 แบบที่ proxy promote ผ่าน holdout ทั้งสอง อีกสองแบบยังถูก reject ด้วย project/CalculiX stress-difference gate `8%` เดิม

คำตัดสิน: `independent_refined_evaluator_available` คำตัดสิน candidate set: `partially_supported` (`7/9`)

## ไฟล์ที่เปลี่ยน

- `config/structural/section_force_vehicle_frame_refinement_v2.json`
- `src/formula_ultimate/structural/vehicle_frame_refinement.py` และ structural package exports
- `src/formula_ultimate/experiments/whole_vehicle_search.py` และ experiment package exports สำหรับ public deterministic geometry mutation adapter
- `scripts/structural/run_vehicle_frame_refinement.py` และ `scripts/run_work053.ps1`
- `tests/test_vehicle_frame_refinement.py`
- `docs/physics/WHOLE_VEHICLE_SECTION_FORCE_REFINED_EVALUATOR.md` และ `.th.md`
- แผน/ผล Work 053 สองภาษา
- แก้ trailing blank line ในผล Work 052 ภาษาอังกฤษที่หยุดแล้ว

raw evidence ที่ถูก ignore อยู่ใต้ `artifacts/work053/`

## การตัดสินใจและหลักฐาน

- แปลง CalculiX `SECTION FORCES` output เป็น surface stress ของหน้าตัดสี่เหลี่ยมจาก `N`, `V1`, `V2`, `T`, `M1`, `M2`; เก็บ integration-point material stress เป็นหลักฐานแต่ไม่นำไปเทียบ analytical root surface stress
- refinement ที่ preregister ยังคงเป็น `4/8/16`; ไม่ผ่อน threshold analytical/refinement `5%` หรือ cross-model `8%`
- fine analytical error คือ CalculiX displacement `0.08648%`, CalculiX stress `3.4276%`, project displacement ประมาณศูนย์ และ project stress `0.00375%`
- candidate reaction residual สูงสุด `2.2293e-11` relative
- สำหรับ candidate 7 แบบที่รับ last-two change สูงสุด `2.0489%`, fine cross-model difference สูงสุด `5.0207%`, yield margin ต่ำสุด `379.45` และ displacement สูงสุด `6.1326e-6 m`
- `candidate-9b03158dc541df18` ไม่ผ่านด้วย fine stress difference `16.69%/17.66%`; `candidate-372db49a7cbceba5` ไม่ผ่านด้วย `32.24%/33.51%` yield margin ที่สูงไม่สามารถลบหลักฐานจาก solver ที่ขัดแย้งกัน
- config SHA-256 คือ `a21cd3ad14f2b1c4e2e1b378101c2b1322fd17d41ba79ce2af20d85cfff26ed4`; deterministic project replay fingerprint คือ `e5b28abfa37224b8bc855d28f43626744401b79c03d084f1b6fb1953fe37020d`; CalculiX executable SHA-256 คือ `2ff89a72b6aac9c361cb716e44220dfcd01d2bb3e66abd6b6455b01b7250f350`

## ความล้มเหลวที่พบและไม่ถูกยอมรับ

การรัน Work 053 ครั้งแรกทำ physics stages ครบแต่ exit `1` ตอนรายงานผล เพราะ field สรุปที่เปลี่ยนชื่อเป็น `structural_states` ยังถูกพิมพ์ด้วยชื่อ `holdout_solves` แก้เฉพาะ key แล้วรันการทดลองทั้งหมดใหม่ ครั้งถัดมาพบ defect ของ decision schema ซึ่งผูก evaluator availability กับการที่ candidate ทั้ง 9 ต้องผ่าน ทั้งที่แผนกำหนดให้ candidate ทุกแบบต้องผ่านหรือ fail อย่างชัดเจน จึงแยก evaluator decision ออกจาก candidate-set decision โดยไม่เปลี่ยน threshold หรือ candidate metric แล้วรันการทดลองทั้งหมดใหม่อีกครั้ง

commit หลักฐาน Work 052 ก่อนหน้า `37359db` ถูกสร้างหลัง `git diff --cached --check` รายงาน blank line ที่ EOF หนึ่งจุด เพราะลำดับ shell ไม่ได้ fail fast Work 053 คงประวัตินี้ไว้ แก้ไฟล์ และใช้ validation แบบ fail-fast แยกคำสั่งสำหรับ commit นี้

## การตรวจสอบที่ใช้จริง

```powershell
py -3.14 -m unittest tests.test_vehicle_frame_refinement -q
# exit 0; Ran 5 tests; OK

powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work053.ps1
# exit 0; status=passed
# decision=independent_refined_evaluator_available
# candidate_set_decision=partially_supported; passed_candidates=7/9
# structural_states=54; candidate_calculix_processes=162
# fine_benchmark_max_error=0.03427617134482464
# negative_controls=7; replay=exact

py -3.14 -m unittest tests.test_vehicle_frame_refinement tests.test_whole_vehicle_search tests.test_repository_contract -q
# exit 0; Ran 15 tests; OK

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 339 tests in 32.391s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0
```

repository-contract checks, staged `git diff --cached --check`, explicit scoped commit และ clean-tree Work 053 replay จะตรวจหลัง result นี้มีอยู่และรายงานใน final handoff

## ข้อจำกัดและงานถัดไป

งานนี้ปิดเฉพาะ evaluator availability ยังไม่ validate solid/contact stress concentration, nonlinear material response, joint จริง, local buckling, fatigue life, vibration, crash, certified material allowable, manufacturing variation หรือ hardware งาน readiness ถัดไปต้องรับเฉพาะ candidate 7 แบบที่ผ่าน คง treatment fairness และ Work 050 evidence identity ทั้งหมด และห้าม rewrite ผล reject สองแบบ
