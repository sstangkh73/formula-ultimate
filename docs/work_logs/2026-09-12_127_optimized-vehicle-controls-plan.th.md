# แผน Work 127: Optimized Vehicle Controls

แหล่งภาษาอังกฤษ: `2026-09-12_127_optimized-vehicle-controls-plan.md`

วันที่: 2026-09-12 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

ทดสอบว่าคะแนนระบบแบบจำกัดของ candidate จาก Work 126 ยังคงอยู่หรือไม่เมื่อเทียบกับ baseline แบบ fixed-topology, reference และ random-control ที่ optimize แล้ว หลัง common-controller substitution, matched-budget retuning และการคิด transferred burden ครบ ตรึง transient evidence จาก Work 123, reserve-before-execute accounting จาก Work 124 และ exploratory assembly exact ของ Work 126

ทุกแขนได้ external task, component-library opportunity, source energy, safety boundary, paired seeds และ search/tuning budget แยกส่วนเท่ากัน negative result ที่ทำครบถือว่ายอมรับได้ การอ้าง system benefit ต้องมีผลที่ลงทะเบียนเหนือ uncertainty โดยไม่มี hidden burden ด้าน mass, energy, cooling, containment, support หรือ manufacturing

## ตัวแปร controls และไฟล์

- IV: vehicle/search arm, mechanism substitution, controller treatment และ tuned parameter
- DV: paired system score, completion/time proxy, energy, installed mass, failure state, uncertainty และ search/tuning cost ที่ถูกคิด
- Controls: untuned baseline, free controller effort, omitted cooling mass และ unequal source energy ต้องทำให้ fairness เป็น invalid
- สำเร็จเมื่อ: ทุกแขน optimize ด้วยต้นทุนเท่ากัน, ประเมิน common controller แล้ว retune เท่ากัน, burden ledger ครบ, exact replay และ promotion decision อยู่ในขอบเขตหลักฐาน

ไฟล์ที่วางแผน: `src/formula_ultimate/experiments/optimized_vehicle_controls.py`, `config/development/optimized_vehicle_controls_v1.json`, `scripts/development/run_optimized_vehicle_controls.py`, `tests/test_optimized_vehicle_controls.py`, สัญญาสองภาษา `docs/contracts/OPTIMIZED_VEHICLE_CONTROLS_V1*`, plan/result สองภาษานี้ และ `artifacts/work127/run_a|run_b` ที่ ignore

## การตรวจสอบ

```powershell
python -m unittest tests.test_optimized_vehicle_controls tests.test_repository_contract -v
python scripts/development/run_optimized_vehicle_controls.py --config config/development/optimized_vehicle_controls_v1.json --output-root artifacts/work127/run_a
python scripts/development/run_optimized_vehicle_controls.py --config config/development/optimized_vehicle_controls_v1.json --output-root artifacts/work127/run_b --replay-reference artifacts/work127/run_a/result.json
python -m compileall -q src scripts tests
```

จากนั้นรัน regression ที่ได้รับผลของ Work 123/124/126 และตรวจ staged/cached diff โดยตรง; commit ทันทีเมื่อทุก gate ผ่านเท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

response model ที่ลงทะเบียนเป็นข้อมูลสังเคราะห์และยืนยัน race performance หรือ physical superiority ไม่ได้ fixed topology เป็นเพียง fair control และไม่บังคับ layout ของ open arm สิ่งที่ไม่ทำ: external novelty, เปลี่ยน threshold หลังเห็นผล, physical validation, promotion จาก exploratory assembly, push หรือ rewrite history
