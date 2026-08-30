# แผนงาน 057: Campaign Physical Adapter และ Burn-In

สถานะ: หยุด (Stopped) — burn-in พบ downstream serialization replay mismatch หลัง training ครบ 240 opportunities และ protocol v1 ห้ามซ่อมแล้วทำต่อหลังเห็น burn-in

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_057_campaign-physical-adapter-burn-in-plan.md`

## วัตถุประสงค์

เชื่อม deterministic runner ที่ commit ใน Work 056 เข้ากับ frozen whole-vehicle evaluation chain ของ Work 047–053 พิสูจน์ recovery ข้าม process boundary และรันเฉพาะ excluded burn-in seed `55999` งานนี้ต้องสร้าง immutable go/stop adjudication ก่อนแตะ admitted seed ใด ๆ

## ขอบเขตและไฟล์ที่วางแผน

- เพิ่ม reusable campaign evaluation, holdout, Work 053 refinement, STEP/FreeCAD witness, adjudication และ analysis code ใต้ `src/formula_ultimate/experiments/`
- เพิ่ม generic campaign command ใต้ `scripts/experiments/` และ fail-fast wrapper `scripts/run_work057.ps1`
- เพิ่ม focused tests สำหรับ physical-adapter identity, solver failure accounting, partition isolation, process-boundary resume, promotion/refinement/witness eligibility และ burn-in stop/go logic
- สร้าง ignored Work 057 ledgers/evidence ใต้ `artifacts/work057/`
- เพิ่มเอกสารวิจัยและ result records สองภาษา ตรวจสอบและ commit Work 057 ก่อนเริ่ม Work 058

## แบบการทดลอง burn-in ที่ freeze

- Independent variable: proposal treatment (`GRID`, `RANDOM`, `EVOLUTION`)
- Burn-in seed: `55999` ซึ่งแยกออกจาก pilot และ main inference
- Opportunities: `80` ต่อ treatment รวม `240` ทุก reserved attempt ใช้หนึ่ง opportunity รวม invalid, failed หรือ interrupted evaluation
- Candidate variables/ranges, GRID mapping, RANDOM distribution, EVOLUTION initialization/mutation/parent rule, training partition, holdout partition, material, loads, thresholds และ promotion cap ต้องตรงกับ `bounded_whole_vehicle_main_campaign_v1` และ pinned upstream identitiesทุกตัว
- Dependent outputs: terminal training status/failure code, mass, energy, Level-0 objective, holdout status, Work 053 stress/deformation/convergence/cross-model result, STEP/FreeCAD validity/hash identity, supported-finisher presence, elapsed cost และ conservation/numerical failuresทั้งหมด
- Controls: equal treatment opportunity, exact replay, GRID proposals ไม่ซ้ำ, proposal/training ห้ามเข้าถึง holdout, analytical cantilever benchmark, project-vs-CalculiX cross-model comparison, invalid/mutated evidence rejection และ process-boundary pending-reservation resume probe ที่แยกจาก campaign evidence

## Pipeline และขอบเขตหลักฐาน

```text
reserve opportunity
  -> training grammar/geometry/Level 0
  -> training-only promotion (max 2 per treatment/seed)
  -> frozen holdout Level 0
  -> Work 053 project frame + CalculiX B31 refinement
  -> candidate-specific 3D -> STEP -> FreeCAD witness
  -> eligibility and burn-in infrastructure adjudication
```

Level 0 ยังเป็น selection gate Work 053 ยังเป็น bounded linear-elastic beam-network evidence ส่วน STEP/FreeCAD witness พิสูจน์เฉพาะการส่ง exact candidate geometry ไม่มีส่วนใดเป็น physical-safety หรือ manufacturability validation

## เกณฑ์ burn-in สำเร็จ

คืน `burn_in_accepted_for_admitted_main_campaign` เมื่อทุกข้อต่อไปนี้ผ่านเท่านั้น:

1. frozen protocol และ upstream/tool SHA-256 identities ทุกตัวตรงกัน
2. มี exactly `240` opportunities และ terminal training results แบ่ง `80/80/80` โดยไม่มี duplicate, skip, retry หรือ GRID repeat
3. ledger replay และ separate-process pending-reservation recovery เป็น exact
4. training selection ไม่อ่าน holdout/refined data และบันทึก promotion shortfall โดยไม่ยืม
5. promoted candidate ทุกตัวมี terminal holdout, refinement และ STEP/FreeCAD witness เมื่อ refinement ผ่าน พร้อมรักษา candidate identity ตลอดทาง
6. solver/process failures เป็น terminal counted outcomes ห้าม silent repair หรือ neutral substitution
7. หลังเห็น burn-in ไม่ต้องแก้ protocol code/config/threshold

Burn-in ไม่จำเป็นต้องสนับสนุน preferred hypothesis หรือสร้าง supported finisher เพราะทดสอบ infrastructure/protocol execution ไม่ใช่ treatment efficacy

## เกณฑ์ล้มเหลวและ falsification

หยุดก่อน Work 058 หาก protocol/upstream/tool mismatch, ledger/replay ไม่ตรง, budget ไม่เท่ากัน, GRID opportunity ซ้ำ, partition leakage, terminal result หาย, candidate เปลี่ยน, refined evaluator ใช้ไม่ได้, hidden CAD repair หรือจำเป็นต้องแก้ implementation/config หลัง burn-in ต้องบันทึกว่าความล้มเหลวขัดแย้งกับ runner reliability, adapter coherence หรือเป็นเพียง candidate feasibility

## การตรวจสอบ

รัน focused tests, full tests, compilation, preparation replay, isolated process-resume probe และ burn-in จากนั้นรัน burn-in แบบ verify-only ตรวจ counts/hashes เขียน result records สองภาษา stage เฉพาะไฟล์ Work 057 รัน `git diff --cached --check`, commit และ replay verification จาก clean commit

## ความเสี่ยงและสิ่งที่ไม่ทำ

จำนวน CalculiX subprocess และ STEP/FreeCAD generation อาจใช้เวลานาน Hash chain ตรวจการแก้ไขได้แต่ไม่มี external signature Work 057 ไม่ใช้ main seeds, ไม่ estimate treatment effects, ไม่เปลี่ยน frozen protocol, ไม่อ้าง physical validation, ไม่ push และไม่ publish
