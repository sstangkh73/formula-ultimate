# ผลงาน 062: Protocol v3 Admitted Main Campaign

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_062_v3-admitted-main-campaign-result.md`

## ผลลัพธ์

รัน admitted campaign `FU-BMC-003` จาก clean commit `bfa33a29bc92890628df0429351cef3e6eed017e` สำเร็จครบ `2,880/2,880` terminal attempts โดยไม่มี pending reservation มี promotions 72, terminal holdouts 72, terminal refinements 72 และ terminal CAD records 72 Refinement และ STEP/FreeCAD witness ผ่าน 51 candidates คำตัดสินสุดท้ายคือ `completed_with_supported_finishers`; clean-tree verify-only replay เป็น exact

EVOLUTION สร้าง supported finishers ได้ 11/12 seeds เทียบกับ RANDOM 9/12 และ GRID 10/12 Primary EVOLUTION-minus-RANDOM rate difference เท่ากับ `+0.1667` แต่ exact McNemar `p = 0.5`; ดังนั้นงานนี้ไม่อ้าง algorithm superiority การตีความและข้อจำกัดฉบับเต็มอยู่ใน `docs/research/BOUNDED_MAIN_CAMPAIGN_V3_RESULT.th.md`

## ไฟล์ที่เปลี่ยน

- อัปเดตสถานะแผนงานภาษาอังกฤษและไทยของงานนี้เป็น `Completed`
- เพิ่ม `docs/research/BOUNDED_MAIN_CAMPAIGN_V3_RESULT.md` และ `.th.md`
- เพิ่มผลภาษาอังกฤษฉบับนี้และ `2026-08-31_062_v3-admitted-main-campaign-result.th.md`
- สร้าง ignored immutable evidence ใต้ `artifacts/work062/`; ไม่มี admitted code หรือ protocol file ถูกเปลี่ยน

## คำสั่งจริงและ validation

- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work062.ps1` → exit `0`; attempts `2,880`, promotions `72`, refinement passes `51`, CAD passes `51`, decision `completed_with_supported_finishers`
- `py -3.14 scripts/experiments/run_bounded_main_campaign.py --kind main --protocol config/experiments/bounded_whole_vehicle_main_campaign_v3.json --artifact-root artifacts/work062 --admission artifacts/work061/campaign_summary.json --verify-only` → exit `0`; replay `exact`, supported streams `30`
- `py -3.14 -m unittest discover -s tests -q` → exit `0`; `Ran 372 tests in 32.872s`, `OK`
- `py -3.14 -m compileall -q src scripts tests` → exit `0`

## Evidence identities

- Protocol fingerprint: `9ef748f2719923632a05ef5fcbba95b8f2fa1b4156d2dbbf6cb9b4fbd02d4c36`
- Training fingerprint: `503917192f3029c66e27cec2a2ef1f7521ebfba9c2872e3541945bf35a281176`
- Stage fingerprint: `9e2554f865788b98c21cff736063d46857eff888e022299256222fad186e1182`
- Analysis fingerprint: `f6a86288b3653b75d1d5c56f62b948344884911d946b91ef8ddbfc6e46dbef19`
- Training feasible/structural failure: `2,107/773`; GRID unique: `960`
- Holdout feasible: `72/72`; refinement passed/refined disagreement: `51/21`; CAD passed/not run: `51/21`

## การตัดสินใจ ข้อจำกัด และงานถัดไป

คง consumed failures ไว้, holdout information ไม่เข้าสู่ selection และรายงาน preregistered outcomes ครบ Primary exact test ไม่มีนัยสำคัญ, evaluator ยัง bounded และ 21 Level-0-feasible candidates ไม่ผ่าน refined agreement ไม่อ้าง physical validation, safety, manufacturability, arbitrary-topology หรือ algorithm superiority

งานถัดไปควร preregister independent replication และแยกยกระดับ structural fidelity ไปสู่ solid/contact/nonlinear behavior, calibrated material data, fatigue and failure propagation และ hardware correlation Result commit และ post-commit clean-tree replay จะรายงานใน final handoff
