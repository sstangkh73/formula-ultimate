# แผน Work 135: Native Detailed Vehicle Realization

แหล่งภาษาอังกฤษ: `2026-09-13_135_native-detailed-vehicle-realization-plan.md`

วันที่: 2026-09-13 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์

ดำเนินแผนละเอียด Work 135 ที่อนุมัติ โดยสร้าง candidate หนึ่งรายการที่แน่นอนเป็น native OCCT B-rep part solids ซึ่งตรวจได้และเป็น assembly ที่เชื่อมต่อทางกายภาพ ใช้แทน box registry ของ Work 126 ในฐานะ geometry evidence แต่เก็บ registry เดิมเป็น architecture-neutral function checklist เท่านั้น

## ขอบเขตและไฟล์ที่วางแผน

- ตรึง consumed commits, contract/result hashes, geometry runtimes ที่ติดตั้ง, candidate identity, task/energy/safety boundary, complete required-occurrence inventory และ deterministic thresholds
- สร้าง `src/formula_ultimate/assembly/native_detailed_vehicle.py` สำหรับ strict declaration parsing, semantic identities, occurrence completeness, assembly/interface/tolerance/motion validation, ledgers, physics-boundary ownership และ falsification controls
- เพิ่ม `config/development/native_detailed_vehicle_v1.json` สำหรับ frozen candidate และ admitted gates
- เพิ่ม `scripts/cad/build_native_detailed_vehicle.py` สำหรับ deterministic native parts, STEP ราย definition และ separate-solid assembly STEP
- เพิ่ม `scripts/cad/inspect_native_detailed_vehicle_freecad.py` สำหรับ exact no-repair FreeCAD import, native-property cross-check และสร้าง FCStd witness
- เพิ่ม `scripts/development/run_native_detailed_vehicle.py` สำหรับ admitted orchestration, artifacts, negative controls ทั้งหมด และ clean replay comparison
- เพิ่ม `tests/test_native_detailed_vehicle.py` และสัญญาสองภาษา `docs/contracts/NATIVE_DETAILED_VEHICLE_V1.md` / `.th.md`
- สร้างผล Work 135 สองภาษาที่ตรงกัน แก้ maintained file อื่นเฉพาะเมื่อ repository contract บังคับและบันทึกทุกไฟล์เพิ่มในผล

จำกัด generated evidence ไว้ใน path ที่ ignore คือ `artifacts/work135/{pilot,run_a,run_b,negative_controls}`

## Validation

รัน CadQuery builder และ FreeCAD inspector ตามคำสั่งตรง, admitted `run_a`, clean `run_b`, Work 135 unit/negative-control suite, regressions ด้าน geometry/assembly/motion/energy/flow/control ที่ได้รับผล, compilation, repository contract และ Git whitespace/staged-scope gates แต่ละคำสั่งต้องรักษา exit status ของตนเอง

## เกณฑ์สำเร็จ

- required physical-occurrence coverage เท่ากับ `1.0`, unknown essential occurrence เป็นศูนย์ และไม่มี unsupported purchased proxy
- material occurrence ทุกตัวเป็น valid native solid ที่มี ownership เดียว พร้อม required voids, routes, interfaces, fasteners, seals, supports และ service relations ชัดเจน
- CadQuery/FreeCAD relative volume และ mass residual `<= 1e-8`, center residual `<= 1e-7 m`, componentwise inertia residual `<= 1e-7` และ counts/signatures รอด exact import โดยไม่มี hidden repair
- mating residual `<= 1e-6 m`, non-contact penetration `<= 1e-12 m^3`, motion มีอย่างน้อย 101 samples และ refinement convergence `<= 1e-5 m`, preview chord `<= 0.00025 m`
- falsification controls ทั้ง 18 รายการถูกปฏิเสธด้วยเหตุผลที่ประกาศ และ evidence hashes ของ `run_a` กับ clean `run_b` ตรงกันทุกค่า
- final admitted status เป็น `passed_native_detailed_geometry` ซึ่งหมายถึง geometry/assembly gate เท่านั้น

## ความเสี่ยงและสิ่งที่ไม่ทำ

ถ้าขาด exact geometry, occurrence ownership ไม่ครบ, assembly ยัง unresolved, semantic boundary หาย หรือ replay drift ต้องหยุด ห้ามซ่อนด้วย bounding boxes หรือ manual aggregate properties CadQuery และ FreeCAD ใช้ OCCT ร่วมกัน จึงเป็น cross-application witness ไม่ใช่ independent-kernel validation

Work นี้ไม่บังคับ conventional vehicle layout, ไม่พิสูจน์ performance benefit, ไม่ rerun downstream structural/thermal/flow/energy/control physics, ไม่ยืนยัน manufacturing readiness หรือ safety, ไม่อนุญาต fabrication, ไม่ทำ physical validation, push หรือ rewrite history การ revalidate physics ปลายทางอยู่ใน Work 136 แยกต่างหาก
