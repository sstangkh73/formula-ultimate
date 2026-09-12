# แผน Work 113: Contact ของจุดเชื่อมแบบละเอียด

ต้นฉบับภาษาอังกฤษ: `2026-09-12_113_detailed-connection-contact-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

พัฒนา fastening-scale connection experiment แบบมีขอบเขตโดยใช้ contracts ของ Work 111 vector field และ Work 112 physical interface ที่ตรงกัน เปรียบเทียบ threaded reference กับ segmented-ramp alternative ที่ topology ต่างกัน ภายใต้ terminal wrench, envelope, synthetic materials, สมมติฐานอุณหภูมิ, preload range และ friction uncertainty เดียวกัน

สร้าง mating CAD solids จริง รวม reference helix/root และ engagement ramps ของทางเลือก ประเมิน discrete contact patches ด้วย unilateral compression, Coulomb slip capacity, preload, off-axis moment, recovered transmitted wrench และ opening/slip ที่สังเกตได้ Fit reduced joint stiffness เฉพาะ load/preload domain ที่ลงทะเบียนและเปรียบเทียบกับ detailed discrete response

## ตัวแปร controls และไฟล์

- IV: joining geometry, contact refinement, engagement, preload, friction, clearance, axial/shear load และ off-axis moment
- DV: active contact fraction, opening, slip, tangent stiffness, displacement, transmitted force/moment, stress proxy, balance residual และ reduced-model error
- Controls: task/materials เดียวกัน; analytic helical geometry checks; joint ถูกถอด/ตัด, reverse load, เพิ่ม clearance และลด engagement; unilateral/contact-friction inequalities; ไม่มี fictitious supports
- Success: ตรึง CAD และ semantic interface identities, threaded reference verification ผ่าน, ทั้งสอง strategies ให้ causal bounded transfer evidence, ปริมาณสามระดับผ่าน registered change gates, negative casesล้มเหลวชัดเจน และ replay ตรงทุกบิต ทางเลือกที่ล้มเหลวยังคงเป็นผลลบที่ยอมรับได้

ไฟล์ที่วางแผน: `src/formula_ultimate/structural/detailed_connection_contact.py`, `config/development/detailed_connection_contact_v1.json`, `scripts/development/run_detailed_connection_contact.py`, `tests/test_detailed_connection_contact.py`, `docs/contracts/DETAILED_CONNECTION_CONTACT_V1*` สองภาษา, plan/result นี้สองภาษา และ `artifacts/work113/run_a|run_b` แบบ ignored

## Validation

```powershell
python -m unittest tests.test_detailed_connection_contact tests.test_repository_contract -v
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_detailed_connection_contact.py --config config\development\detailed_connection_contact_v1.json --output-root artifacts\work113\run_a
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_detailed_connection_contact.py --config config\development\detailed_connection_contact_v1.json --output-root artifacts\work113\run_b --replay-reference artifacts\work113\run_a\result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน affected regressions, `git diff --check`, stage เฉพาะไฟล์ที่ประกาศ, ตรวจ cached scope และ `git diff --cached --check`; commit ทันทีเมื่อทุก gate ที่ประกาศผ่านเท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

Discrete patch model ไม่ใช่ general nonlinear contact solver; stress quantities เป็น regularized patch averages และ thread-root geometry ยังเป็น CAD finite-resolution Friction ไม่แน่นอนและ loosening/fatigue ยัง unresolved สิ่งที่ไม่ทำ: universal thread standard, production fastener sizing, fatigue life, safety certification, manufacturing release, physical validation, push หรือ rewrite history
