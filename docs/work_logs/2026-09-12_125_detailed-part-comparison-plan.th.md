# แผน Work 125: การเปรียบเทียบค้นพบชิ้นส่วนละเอียดที่ลงทะเบียน

แหล่งภาษาอังกฤษ: `2026-09-12_125_detailed-part-comparison-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

รัน paired comparison ที่ preregister แบบมีขอบเขตของ arm fixed-family, existing-grammar, open-material และ random-control ที่ optimize แล้ว ตรึงหลักฐาน connection/motion/thermal/material จาก Work 113–116 และ accounting จาก Work 124; แยกเงื่อนไข pilot/training จาก holdout ที่ไม่ถูกแตะ

คิด optimization/holdout budget เท่ากัน ประเมิน signed utility difference และ uncertainty ที่ fidelity สูงขึ้น audit geometry ที่ rejected/unresolved โดยไม่ขึ้นกับ proxy score และ ablate geometry ที่อ้างว่า active การทดลองจบด้วยผลลบได้; claim discovery-benefit ต้องผ่าน constraints, meaningful signed effect และ uncertainty เพิ่ม

## ตัวแปร control และไฟล์

- IV: representation arm, tuned parameter, active/ablated coupling, coarse/fine fidelity และ held-out condition
- DV: verified utility, paired effect/interval, mass/energy burden, constraint state, ranking reversal และต้นทุนรวม
- Controls: task, material/process boundary, paired seed และ budget เดียวกัน; arm ที่ optimize แล้ว, inactive appendage, same-topology response, omitted hardware, fine-fidelity reversal และ holdout leak
- Success: accounting/provenance เป็นธรรม, holdout แยก, ablation เป็นเชิงเหตุ, มี fidelity evidence และ exact replay ไม่บังคับผล discovery บวก

ไฟล์ที่วางแผน: `src/formula_ultimate/experiments/detailed_part_comparison.py`, `config/development/detailed_part_comparison_v1.json`, `scripts/development/run_detailed_part_comparison.py`, `tests/test_detailed_part_comparison.py`, contract `docs/contracts/DETAILED_PART_COMPARISON_V1*` สองภาษา, plan/result สองภาษาชุดนี้ และ `artifacts/work125/run_a|run_b` ที่ไม่ติดตามใน Git

## การตรวจสอบ

```powershell
python -m unittest tests.test_detailed_part_comparison tests.test_repository_contract -v
python scripts/development/run_detailed_part_comparison.py --config config/development/detailed_part_comparison_v1.json --output-root artifacts/work125/run_a
python scripts/development/run_detailed_part_comparison.py --config config/development/detailed_part_comparison_v1.json --output-root artifacts/work125/run_b --replay-reference artifacts/work125/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน regression ที่ได้รับผลของ Work 113–116/124 และตรวจ staged/cached diff แบบระบุไฟล์ จะ commit ทันทีเมื่อทุก gate ผ่านเท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

Response fixture ที่ลงทะเบียนเป็น synthetic และยืนยัน external novelty หรือ whole-vehicle benefit ไม่ได้ สิ่งที่ไม่ทำ: ปรับ threshold หลังผล, บังคับความแปลกตา, physical validation, push หรือแก้ประวัติ
