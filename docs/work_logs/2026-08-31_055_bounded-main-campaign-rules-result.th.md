# ผลงาน 055: กติกา bounded main campaign

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_055_bounded-main-campaign-rules-result.md`

## ผลลัพธ์

กติกาของ bounded main campaign แรกถูก preregister และตรวจด้วยเครื่องแล้ว คำตัดสินคือ `rules_frozen_campaign_not_run` Work 055 ประเมิน candidate `0` ครั้ง

declaration ที่ตรึงใช้ paired seeds ใหม่ 12 ค่า, attempted evaluations 80 ครั้งต่อ treatment/seed, `960` attempts ต่อ treatment และ `2,880` attempts รวม GRID ใช้ opportunities ไม่ซ้ำ `960` จาก capacity `4^5=1,024` โดยไม่ wrap Candidate สูงสุดสองแบบต่อ treatment/seed เข้า stage ถัดไปได้ รวม promotions สูงสุด 72

preferred primary hypothesis เปรียบเทียบ refined-supported-finisher probability ระดับ seed ของ `EVOLUTION` กับ `RANDOM` โดย paired seed—not attempt แต่ละครั้ง—คือ inferential unit ห้าม holdout leakage, silent repair, neutral failure substitution, retry, ยืม budget ข้าม seed, เปลี่ยน refined threshold และให้สิทธิ์ winner โดยไม่มีหลักฐาน `3D -> STEP -> FreeCAD`

## ไฟล์ที่เปลี่ยน

- `config/experiments/bounded_whole_vehicle_main_campaign_v1.json`
- `src/formula_ultimate/experiments/main_campaign_protocol.py` และ experiment package exports
- `scripts/experiments/validate_main_campaign_protocol.py` และ `scripts/run_work055.ps1`
- `tests/test_main_campaign_protocol.py`
- `docs/research/BOUNDED_WHOLE_VEHICLE_MAIN_CAMPAIGN_PROTOCOL.md` และ `.th.md`
- แผน/ผล Work 055 สองภาษา

ignored validation evidence อยู่ใต้ `artifacts/work055/`

## การตัดสินใจและหลักฐาน

- Main seeds คือ `55001..55012`; pilot seeds `101/202/303` และ burn-in seed `55999` ถูก exclude
- failure/DNF ทุกกรณีใช้หนึ่ง opportunity และยังมองเห็นได้
- GRID เป็น fixed discrete calibration treatment และต้องรายงานความต่างของ distribution จาก RANDOM/EVOLUTION
- primary endpoints คือ supported-finisher presence ระดับ seed และ best frozen-holdout time ระดับ seed
- candidate eligibility ต้องผ่าน frozen holdout, Work 053 refined evidence, provenance/exploit checks และ final STEP/FreeCAD witness
- การอ้าง algorithm superiority ต้องมีทั้ง positive primary supported-finisher-rate effect และ independent replication ภายใต้ protocol ใหม่
- protocol config SHA-256 คือ `f42b9f59a0006ffb87e6607099de3446b03b559a38fe1b719bdd775a1d1a31ab`; canonical protocol fingerprint คือ `a332852d75da1c4c22caba78105062eb1a6859db3ec484dc14ec0f3aec844ceb`

## ความล้มเหลวที่พบและไม่ถูกยอมรับ

focused test ครั้งแรกล้มเพราะ validator ใช้กฎ artifact SHA-256 64 ตัวอักษรกับ Git commit identity 40 ตัวอักษร จึงเพิ่ม commit-ID validator แยกโดยไม่เปลี่ยนกติกา campaign การรันถัดมามี negative-fixture expectation ล้มหนึ่งจุด เพราะการเปลี่ยน attempt budget ถูก exact-budget rule ก่อนถึง GRID capacity จึงเปลี่ยน fixture ให้ทำลาย declared GRID capacity โดยตรงโดยไม่เปลี่ยน protocol หรือ threshold

## การตรวจสอบที่ใช้จริง

```powershell
py -3.14 -m unittest tests.test_main_campaign_protocol -q
# initial exit 1; Git commit identity ถูกตรวจผิดเป็น SHA-256
# intermediate exit 1; GRID negative fixture หนึ่งตัวถึง exact-budget guard ก่อน
# final exit 0; Ran 7 tests; OK

powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work055.ps1
# exit 0; status=passed
# decision=rules_frozen_campaign_not_run; candidate_evaluations=0
# paired_seeds=12; total_attempts=2880
# grid_unique=960; maximum_promotions=72; replay=exact

py -3.14 -m unittest tests.test_main_campaign_protocol tests.test_refined_readiness tests.test_whole_vehicle_search tests.test_repository_contract -q
# exit 0; Ran 21 tests; OK

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 350 tests in 31.939s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0
```

repository-contract checks, staged `git diff --cached --check`, explicit scoped commit และ clean-tree Work 055 replay จะตรวจหลัง result นี้มีอยู่และรายงานใน final handoff

## ข้ออ้างที่รองรับและยังไม่รองรับ

รองรับ: declaration สอดคล้องภายใน, pin bounded upstream evidence, balance treatment opportunity, ไม่ทำ GRID ซ้ำ, นิยาม seed-level outcome ที่หักล้างได้ และ validate แบบ deterministic โดยยังไม่รัน campaign

ยังไม่รองรับ: campaign outcome, candidate merit, treatment effect, algorithm superiority, discovery, physical validation, safety, manufacturability หรือ race performance

## ข้อจำกัดและงานถัดไป

12 seeds ไม่รับประกัน power สำหรับ effect ขนาดเล็ก grammar ห้าตัวแปรและ physics domain ปัจจุบันจำกัดการ transfer Work 056 ควร implement two-stage campaign runner และ append-only ledgers ตาม protocol นี้ Work 057 ใช้เฉพาะ excluded seed `55999` สำหรับ burn-in และการเปลี่ยนกติกาหลัง burn-in ต้องใช้ protocol ID ใหม่
