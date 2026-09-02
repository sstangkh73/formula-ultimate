# ผล Work 073: การเชื่อมโยงมวลสปริง ผิวถนน และแนวดิ่งของยาง

Status: Completed

แปลจากไฟล์ภาษาอังกฤษ: `2026-09-01_073_sprung-body-road-tyre-vertical-result.md`

## ผลลัพธ์

สร้างและพยายามหักล้างระบบแนวดิ่ง 6 DOF ที่ระบุตัวตนด้วย geometry สำหรับ sprung heave/pitch/roll และสถานะ unsprung 3 จุด พร้อม suspension/tyre compliance การเคลื่อนที่ถนนแบบ deterministic การป้อน actual load กลับ Work 071 บัญชีพลังงานแนวดิ่ง contact loss และ travel failure ทุก gate ที่ประกาศผ่านแล้ว นี่เป็นหลักฐานความเป็นไปได้ของซอฟต์แวร์ Level 0 ไม่ใช่ physical validation หรือความพร้อมแข่ง

## ไฟล์ที่เปลี่ยน

- `config/vehicle/sprung_body_road_tyre_vertical_v1.json`
- `src/formula_ultimate/simulation/sprung_body_vertical_coupling.py`
- `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_sprung_body_vertical_coupling.py`
- `tests/test_sprung_body_vertical_coupling.py`
- `docs/research/SPRUNG_BODY_ROAD_TYRE_VERTICAL_V1.md`
- `docs/research/SPRUNG_BODY_ROAD_TYRE_VERTICAL_V1.th.md`
- ชุด plan/result สองภาษาของ Work 073 นี้

หลักฐาน deterministic ที่ ignore ถูกสร้างใต้ `artifacts/work073/`

## การตัดสินใจและหลักฐาน

- คำนวณมวลสปริง `245.95200000000003 kg`, roll inertia `4.218672483307425 kg m2` และ pitch inertia `46.253188363933454 kg m2` จากชิ้นส่วนสถาปัตยกรรมที่ไม่สัมผัสพื้น
- ใช้ implicit-midpoint solve ขนาด `6 x 6` และคำนวณ actual tyre load ภายใน fixed point ของ acceleration/load เดิม
- รักษาพลังงานรวมเริ่มต้นที่ `50,000,000 J` พอดี พร้อมแยก suspension heat, tyre heat, inertial work และ road work
- รักษา Work 072 result SHA-256 `2e70e32766915af2237b92cee20aa9ee415f65bfc5ab14e56fd02d1bf41628ad`
- กรณีอ้างอิงจบ `500` steps ช่วงโหลดคือ `298.98159710209535` ถึง `1763.2457662772727 N`; heave/pitch/roll สูงสุด `0.0033467120741574362 m`, `0.019441673288686227 rad`, `0.03707142724764741 rad`; ระยะช่วงล่างสูงสุด `0.01138991675295634 m`
- generalized-equation, vertical-energy และ combined relative energy residual สูงสุดคือ `5.115907697472721e-12`, `1.9463597400459776e-15 J`, `5.043254643678665e-9`
- bump จ่าย road work `0.7534111876506473 J` steering/bump mirror residual สูงสุด `1.11022302462516e-16` / `1.33226762955019e-15` ความต่างจาก time step ครึ่งหนึ่งสูงสุด `0.0037196002671815395`
- road drop ให้ `contact_loss` แบบไม่ commit ที่ step `23`; large ramp ก็เจอ contact loss ก่อนที่ step `192` ซึ่งหักล้างความคาดหมายแบบ travel-first ส่วน initial-state control แยกต่างหากให้ `suspension_travel` ที่ step `2` ด้วย `0.0506249708792031 m` ค่าถูกเก็บโดยไม่ clip หรือ relabel
- Reference result SHA-256: `802330a0566c746d00beb3f5a6cddb725cfee4a9e9f85e08a8bd509b4a6ce973`
- Canonical evidence SHA-256: `84c0911f35ef12036fd5dde2dc05183bf727a1bf3f25927c6a2febafd15ea2e3`
- Primary/replay evidence file SHA-256: `EF22581D6DE1172BFA7181A31E5EFD77B9FFF0FB4959C5521527D1C73CF5BA07`

## บันทึกการตรวจสอบ

```text
python -m unittest tests.test_sprung_body_vertical_coupling -v
Exit: 0
Ran 12 tests in 55.051s — OK

python scripts/experiments/run_sprung_body_vertical_coupling.py --config config/vehicle/sprung_body_road_tyre_vertical_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work073/materialized_architecture_v3.json --output artifacts/work073/experiment_evidence.json
Exit: 0
status=passed; evidence_sha256=84c0911f35ef12036fd5dde2dc05183bf727a1bf3f25927c6a2febafd15ea2e3

python scripts/experiments/run_sprung_body_vertical_coupling.py --config config/vehicle/sprung_body_road_tyre_vertical_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work073/replay/materialized_architecture_v3.json --output artifacts/work073/replay/experiment_evidence.json
Exit: 0
primary SHA-256 = replay SHA-256 = EF22581D6DE1172BFA7181A31E5EFD77B9FFF0FB4959C5521527D1C73CF5BA07

python -m unittest discover -s tests -v
Exit: 0
Ran 454 tests in 126.422s — OK

python -m compileall -q src scripts/experiments/run_sprung_body_vertical_coupling.py tests/test_sprung_body_vertical_coupling.py
Exit: 0

python -m unittest tests.test_repository_contract -v
Exit: 0
Ran 6 tests in 1.635s — OK
```

ผล repository-contract, staged-diff, commit และ post-commit ขั้นสุดท้ายจะรายงานใน handoff

## ข้อจำกัดและงานถัดไป

แบบจำลองยังเป็น linear, small-angle และ synthetic ไม่รวม motion ratio ของ linkage จาก CAD, contact ยางไม่เชิงเส้น, bump stop, chassis flex, anti-dive/squat, road spectrum จากการวัด, พารามิเตอร์ที่ระบุจากข้อมูล, aerodynamic load, gyroscopic effect ของล้อ และการระบุ event ภายใน sub-step implementation ที่ใช้ร่วมกันอาจซ่อนข้อผิดพลาด common-mode ระหว่างสมการกับ ledger แม้มี mirror/refinement controls

งานถัดไปควรเพิ่ม closed-loop path/circuit controller หลังตัดสินใจอย่างชัดเจนว่า CAD linkage kinematics และ nonlinear contact ต้องมาก่อนหรือไม่ ตอนนี้ยังไม่มี path following หรือข้อกล่าวอ้างว่าจบรอบสนาม
