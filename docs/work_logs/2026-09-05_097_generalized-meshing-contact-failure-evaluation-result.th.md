# ผล Work 097: การประเมิน Meshing, Contact และ Failure แบบทั่วไป

ต้นฉบับภาษาอังกฤษ: `2026-09-05_097_generalized-meshing-contact-failure-evaluation-result.md`

## สถานะและผลลัพธ์

สถานะ: Completed

Work 097 ผูกผู้สมัครที่ไม่ใช่รูปทรงพื้นฐานจาก Work 096 จำนวน 7 รายการเข้ากับ benchmark โครงสร้างลดรูปแบบ cross-method ที่ทำซ้ำได้ ทั้ง 7 รายการผ่านการเลือกแบบจำลอง, การผูก semantic region, refinement, reference response, force/moment/energy residual, contact law, failure domain แบบ intact และ connection state ที่ตรึงไว้ ครบเส้นทาง beam, shell, solid และ contact

ผลนี้ยืนยันความครอบคลุมของตัวประเมินสำหรับ benchmark adapter ที่ตรึงไว้ 7 กรณีเท่านั้น ไม่ได้ยืนยันความสามารถ finite-element จากเรขาคณิตแบบทั่วไปหรือความถูกต้องทางกายภาพของ topology ใด ๆ

## ไฟล์ที่เปลี่ยน

- `config/structural/generalized_geometry_benchmarks_v1.json`
- `src/formula_ultimate/structural/generalized_geometry_benchmarks.py`
- `src/formula_ultimate/structural/__init__.py`
- `scripts/structural/run_generalized_geometry_benchmarks.py`
- `tests/test_generalized_geometry_benchmarks.py`
- `docs/contracts/GENERALIZED_GEOMETRY_BENCHMARKS_V1.md` และคู่ภาษาไทย
- plan/result นี้และคู่ภาษาไทย
- หลักฐาน pilot/replay ที่เก็บไว้แต่ถูก ignore ภายใต้ `artifacts/work097/run_a` และ `run_b`

## การตัดสินใจและหลักฐาน

- ต้องใช้อัตลักษณ์ semantic config, FreeCAD report และ strict comparison จาก Work 096 ที่ตรงกันทุกค่า การแทนต้นทาง, semantic region ที่หาย และ hidden geometry repair จะ fail closed
- การเลือกแบบจำลองใช้จำนวน solid ที่วัดได้, หน้าตัดที่เป็นบวก, อัตราส่วน sampled thickness ต่อ path, คำประกาศ contact และชนิด load path ของ benchmark การรันจริงครอบคลุม `beam`, `shell`, `solid` และ `contact` พร้อมเหตุผลที่บันทึกด้วยเครื่อง
- Adapter 7 กรณีเปรียบเทียบเส้นทาง analytical/refined reference กับ discrete ที่แยกจากกันสำหรับ curved bending, tapered bending, shell membrane response, branched bending, rib springs, annular bearing compliance และ Hertz contact
- Discrete levels เพิ่มเป็นสองเท่าอย่างเคร่งครัด ทุกกรณีที่ไม่ exact มี observed order สูงกว่า `1.5`; เส้นทาง rib/contact ที่ exact ถูกระบุว่า exact โดยไม่สร้างค่า order เทียม Fine relative error สูงสุดคือ `0.0014270788520555852` ต่ำกว่า `0.005`; last-two change สูงสุดคือ `0.0042775693130952114` ต่ำกว่า `0.01`
- Force, moment และ energy relative residual เป็นศูนย์ใน baseline ที่ตรึงไว้และต่ำกว่าเกณฑ์ `1e-12` การฉีด non-finite response, residual เกิน และ non-convergence ถูกปฏิเสธ
- Pilot แรกปฏิเสธ baseline `contact_pair` ที่โหลด 100 N อย่างถูกต้องด้วย yield ratio `1.376816754162322` ก่อนปิดงานจึงลดโหลด baseline ที่ตรึงเป็น `25 N`; maximum failure ratio ใหม่คือ `0.8792554763052145` ทำให้ baseline เป็น intact โดยไม่มี post-observation repair ส่วน negative controls สำหรับ divergence และ severed edge ยังคงเป็น failure ตามที่ออกแบบ
- กฎ interface ครบทั้ง `bonded`, `sliding_friction`, `bearing_preload` และ `hertz_frictional` โดยเป็น typed benchmark states ไม่ใช่คำตอบ nonlinear contact สามมิติแบบทั่วไป
- Severed-edge controls ทั้ง 7 รายการมีแรง/โมเมนต์ส่งผ่านเป็นศูนย์และเก็บ affected path IDs ส่วน forced solver divergence ยังคงเป็น `invalid` พร้อม `fallback_used: false`

## หลักฐานอัตลักษณ์

- Config SHA-256: `dd74be7242b698354a124916167c4fc7efaa46bd4d505286741ce3cc31aabf8e`
- Work 096 FreeCAD report SHA-256: `96cf848f1dc1482be4b408eb146c36cca324f71b21c74a4b5b5de243412c6c08`
- Work 096 semantic comparison SHA-256: `731ba8b6c167f36703a278da959cf8f586714262995c811ede38b2892599cf7d`
- Work 097 result SHA-256 ของทั้งสองรอบ: `431292b4ffde83569808af6d13a6a6ce81d3fe98683f11e2439532c55843795e`
- จำนวนกรณี: `7`; model coverage: `beam`, `contact`, `shell`, `solid`; evidence class: `reduced_order_cross_method_benchmark`; design use: false

## คำสั่งตรวจสอบแบบตรงตัว

```powershell
python -m py_compile src/formula_ultimate/structural/generalized_geometry_benchmarks.py src/formula_ultimate/structural/__init__.py scripts/structural/run_generalized_geometry_benchmarks.py tests/test_generalized_geometry_benchmarks.py
# exit 0

python -m unittest tests.test_generalized_geometry_benchmarks tests.test_repository_contract -q
# exit 0; ผ่าน 15 tests ใน 2.191 s

python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work097/run_a/result.json
# exit 0; ผ่าน 7 กรณี; result SHA-256 431292b4ffde83569808af6d13a6a6ce81d3fe98683f11e2439532c55843795e

python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work097/run_b/result.json --replay-reference artifacts/work097/run_a/result.json
# exit 0; exact replay ตรงกัน

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -q
# exit 0; ผ่าน 689 tests ใน 347.187 s; skip ตามสภาพแวดล้อมที่คาดไว้ 7 รายการ
```

## ข้อจำกัดและงานต่อไป

Reference และ discrete solvers เป็น benchmark adapters ลดรูปที่ทำงานบน scalar/section summaries จาก Work 096 ไม่ได้สร้าง mesh จากผิว STEP หรือแก้ local stress concentration, local shell buckling, plastic redistribution, crack propagation, fretting, nonlinear contact history หรือความแปรปรวนวัสดุจริง Thermal stress เป็น fully constrained upper-bound screen และ fatigue เป็น synthetic power-law screen การผ่านไม่ได้รับรถเข้าสู่การออกแบบ ไม่ยืนยันความปลอดภัย และไม่ยืนยัน topology ใหม่ในอนาคต งานถัดไปต้องเพิ่ม mesh จากเรขาคณิตจริงและหลักฐาน solver ที่มี fidelity สูงกว่าอย่างอิสระก่อนเพิ่มระดับคำอ้างเชิงโครงสร้างของผู้สมัครเหล่านี้
