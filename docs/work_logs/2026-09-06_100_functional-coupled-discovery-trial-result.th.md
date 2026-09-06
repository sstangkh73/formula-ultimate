# ผล Work 100: การทดลองค้นพบเชิงหน้าที่และแบบควบคู่ V1

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-06_100_functional-coupled-discovery-trial-result.md`

วันที่: 2026-09-06 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์

Work 100 สร้างและรัน geometry-derived scalar axial/thermal subsystem evaluator แบบมีขอบเขตบน executable morphology จาก Work 099 Primary midpoint-subdivision solver ส่งออก nodal fields, segment flows, reactions, equilibrium/energy residuals, stresses, temperatures, utilization, geometry-derived mass และ vehicle-burden feedback ส่วน exact linear-radius resistance implementation แยกต่างหากใช้ตรวจสอบ numerical แบบ cross-method ระบบ freeze และตรวจ task terminal ancestry, material identity, environment, source hashes, budgets, partitions และ claim limits ก่อนรัน

Registration V2 SHA-256 คือ `2c3aaa21ffb6ed36da532493c82c6e1f0195b13990180dc5d055c75fb47bdd45` Admitted run A และ B ที่เริ่มแยกจากกันคืน exit `0` และให้ deterministic evidence SHA-256 เดียวกันคือ `652ba7d9db9d76ed841d5b2c24af421075cc2d266a9098bc065fe4a8ac45da61` Trusted ledger ทั้งสองเปิดซ้ำได้แบบ exact Candidates ทั้งสิบผ่าน refined training, computational process envelope, holdout ที่ไม่แตะต้อง และ decision replay จึงสร้าง `candidate_survivor` แบบมี scientific accounting สิบรายการภายใน scope ที่แคบ Graph/joint signature อย่างน้อยหนึ่งรายการต่างจาก fixed signature จึงผ่าน survivor condition ที่ preregister ไว้

ผลนี้ไม่ใช่หลักฐาน functional superiority Graph-only และ joint มี mean difference จาก fixed ประมาณ `-1.51e-14`; กิ่งที่เพิ่มแทบไม่มี source-to-sink flow Morphology-only มี paired difference คนละทิศและ mean `-0.0031219`; random-control mean difference คือ `+0.0159315` เมื่อ `n = 2` การวิเคราะห์จึงเป็น descriptive only ผลยืนยัน executable distinct architectures และ bounded simulated feasibility แต่ไม่ยืนยัน useful load path ใหม่ ความเป็นไปได้ของรถทั้งคัน race advantage ความใหม่ของเทคโนโลยี manufacturing proof สถานะ `promotion_ready` หรือ physical validation

## V1 ที่ freeze แล้วหยุด และการจัดการ V2

Registration V1 SHA-256 `aa5012d3b0a85b9f6c42b1ede5561681713cb9c9832577f6d2bf88e09d96a871` ถูก freeze ก่อน observation การรันหยุดหลัง proxy/refined evaluation เพราะ proxy label แปดรายการเป็น `numerically_unresolved` ภายใต้ refinement-change gate `0.005` ที่ freeze ไว้ และ reporter เดิมของ Work 098 ต้องการ Boolean proxy label จึงไม่มี V1 holdout, survivor หรือ contrast result โดยไม่ได้ทำต่อจาก ledger และไม่ได้ขยาย threshold

V2 คง scientific threshold, task, treatment, seed, selection rule และ claim boundary ทุกค่า ก่อน observation เพิ่มเพียง deterministic report สำหรับกรณี label ที่ประเมิน rate ไม่ได้ Audit ของ V2 รายงาน `proxy_boolean_count = 2`, `proxy_unresolved_count = 8`, refined-feasible สิบรายการ และ `false_negative_rate = null`, `false_positive_rate = null` โดยไม่เปลี่ยน unknown label เป็น pass/fail

## ไฟล์ที่เปลี่ยน

- เพิ่ม primary/reference solvers ใต้ `src/formula_ultimate/physics/`
- เพิ่ม trial implementation และ runner ใต้ `src/formula_ultimate/experiments/` และ `scripts/experiments/`
- เพิ่ม frozen trial configuration และ V1/V2 registrations ใต้ `config/experiments/`
- เพิ่ม `tests/test_functional_discovery.py` จำนวน 14 tests ครอบคลุม analytical, conservation, refinement, registration, binding, failure, treatment และ audit
- เพิ่ม bilingual contract และ bilingual plan/result ชุดนี้
- สร้าง ignored evidence ใต้ `artifacts/work100/`: `run_a` ที่หยุด, admitted `run_v2_a` และ replay `run_v2_b`

## หลักฐาน validation ที่แน่นอน

1. `python -m unittest tests.test_functional_discovery -q`: exit `0`; `Ran 14 tests`; `OK`
2. CadQuery targeted Works 098-100/topology/geometry regression: exit `0`; `Ran 131 tests in 27.745s`; `OK`
3. V2 run A: exit `0`; `candidate_count = 10`; `survivor_count = 10`; audit `not_estimable_due_to_unresolved_proxy_labels`; deterministic SHA ตามด้านบน
4. V2 run B พร้อม `--replay-reference artifacts/work100/run_v2_a/result.json`: exit `0`; counts และ deterministic SHA ตรงกันแบบ exact
5. `python -m compileall -q src scripts tests`: exit `0`
6. `python -m unittest discover -s tests -q`: exit `0`; `Ran 785 tests in 421.299s`; `OK (skipped=8)`
7. `git diff --check`: exit `0`; ไม่มี output

## การตัดสินใจ ข้อจำกัด และงานต่อไป

- Numerical failure คง unresolved และไม่ถูกเปลี่ยนเป็น physical failure แบบเงียบ
- Exact reference ใช้สมการ genotype และ NumPy ร่วมกัน Independent/safety promotion gates ยังไม่ได้ประเมิน จึงไม่มี candidate เป็น `promotion_ready`
- CAD ยืนยัน executable geometry identity แต่ scalar gene-derived network นี้ไม่ใช่ volumetric finite-element solve
- Process check เป็นเพียง declared envelope ไม่ใช่ manufacturing proof
- Timing เป็น diagnostic Peak native memory ไม่ได้วัดจริง จึงบันทึกศูนย์แทนการอ้าง measured bound
- `.gitattributes` แบบจำกัด path คงทุก source ที่ hash แบบ raw bytes เป็น LF ภายใต้ Windows `core.autocrlf=true` เพื่อป้องกัน identity drift เทียมหลัง checkout
- Work 101 ควรบังคับ task-relevant nonzero-flow topology changes, whole-vehicle coupling ที่แรงขึ้น, powered comparisons และ independent/safety evidence

Validated commit hash จะรายงานใน final handoff หลัง exact-scope commit สำเร็จ
