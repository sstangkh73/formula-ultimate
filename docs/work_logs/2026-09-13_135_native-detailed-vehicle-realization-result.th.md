# ผล Work 135: การสร้างรถละเอียดแบบเนทีฟ

แหล่งภาษาอังกฤษ: `2026-09-13_135_native-detailed-vehicle-realization-result.md`

วันที่: 2026-09-13 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และหลักฐาน

Work 135 สร้าง candidate ใหม่ `tri_contact_native_135_r1` เป็น definition แบบ native OCCT B-rep 48 รายการและ occurrence ที่มี ownership เฉพาะ 83 ชิ้น แบ่งเป็น material solid 77 ชิ้นและ void solid ที่ structural mass เป็นศูนย์ 6 ชิ้น สถาปัตยกรรมเป็นแบบ open-body สามจุดสัมผัสที่เลือกจาก contact task ของ Work 118 ส่วน Work 126 ใช้เฉพาะ function checklist ไม่ได้สืบทอด geometry implementation ที่ดูแลสร้างโครงสร้างจริง วัตถุสัมผัสพื้นสามชิ้นพร้อม carrier/bushing/axle, ชุดขับและส่งกำลังใน ground unit, energy containment และ internals, controller/sensor/connector, ฮาร์ดแวร์หล่อเย็นและ flow void, harness/tube แบบ route, panel/ช่องเปิดภายนอก, fastener/nut/washer/gasket และ service void

CadQuery คำนวณมวลจาก geometry ได้ `1023.6476530495439 kg` และ FreeCAD คำนวณใหม่จาก occurrence STEP ชุดเดียวกันได้ `1023.6476530421635 kg` residual สูงสุดข้ามแอปคือ volume `3.338611945214137e-9` relative, mass `3.3386118825076423e-9` relative, center `1.8893996922564327e-9 m` absolute และ inertia `4.176665888559849e-9` relative ไฟล์ definition STEP 48 ไฟล์และ occurrence STEP 83 ไฟล์นำเข้าเป็นหนึ่ง valid solid ต่อไฟล์ทั้งหมด จำนวน material/void assembly เป็น `77/6`, semantic selector ผ่าน `754/754`, non-contact penetration เป็น `0.0 m^3` และ motion ใช้ 101 sample โดย collision เป็นศูนย์และ refinement change `0.0 m`

required occurrence coverage และ physics-boundary coverage เท่ากับ `1.0` พอดี unknown essential occurrence เป็นศูนย์ falsification-control บังคับถูกปฏิเสธครบ 18 กลุ่ม การเลือกอิสระด้วย SHA-256 ตรวจ `pack_washer_1` โดยไม่เลือกตาม proxy score และไม่สร้างคำกล่าวอ้าง serviceability เฉพาะชิ้นขึ้นเอง `run_a` กับ clean `run_b` ตรงกันทุกประการที่ result SHA-256 `a9a3f55571bf5b5441c3ef3e8b2674623305d8c1fb02814dcf87cd4a1b9b7d3c`; canonical FCStd SHA-256 คือ `3353e4266e4d119e19fb76477862749fb77fc2fe5e0a72bea432bf165b782ee6`

สถานะ admitted คือ `passed_native_detailed_geometry` และ promotion ยังเป็น false นี่เป็น gate ด้าน native geometry/assembly ไม่ใช่คำกล่าวว่า candidate ที่ยังไม่ optimize และหนัก `1023.65 kg` แข่งขันได้หรือผ่าน physical validation

## ไฟล์ที่เปลี่ยน

- `src/formula_ultimate/assembly/native_detailed_vehicle.py`
- `config/development/native_detailed_vehicle_v1.json`
- `scripts/cad/build_native_detailed_vehicle.py`
- `scripts/cad/inspect_native_detailed_vehicle_freecad.py`
- `scripts/development/run_native_detailed_vehicle.py`
- `tests/test_native_detailed_vehicle.py`
- contract สองภาษา `docs/contracts/NATIVE_DETAILED_VEHICLE_V1.md` / `.th.md`
- plan/result Work 135 สองภาษาชุดนี้

หลักฐานที่สร้างยังถูก ignore ภายใต้ `artifacts/work135/{pilot,run_a,run_b}` admitted run มี STEP ต่อ definition 48 ไฟล์, STEP ต่อ instance 83 ไฟล์, STEP assembly material/void, preview STL ที่ไม่ใช่หลักฐาน, exact-import FCStd, รายงาน identity/semantic/interface/material-void/physics/property/collision/motion/tolerance/view, independent audit, control และ replay

## การตัดสินใจและสิ่งที่พบใน pilot

- รักษาสถาปัตยกรรมที่เลือกให้เปิดกว้างโดยไม่ใส่รูปแบบรถ conventional และใช้เอกลักษณ์ใหม่ `tri_contact_native_135_r1` เพื่อไม่สืบทอด box geometry จาก Work 126
- สร้าง geometry ที่ตรวจจาก Work 83/84/87/108/113 ใหม่ เพราะไม่มีรายการใดตรง placement และ interface ของ candidate นี้
- ใช้ valid one-solid OCCT topology ร่วมกับ exact FreeCAD re-import เป็น closed-solid witness เพราะ binding `Shape.Closed()` ของ CadQuery 2.8.0 ไม่น่าเชื่อถือ
- จับคู่ curved STEP face ด้วยสมบัติทางกายภาพที่เสถียร parameter-seam bounds และจำนวน seam edge เป็นข้อมูลวินิจฉัยเพราะ STEP อาจ reparameterize แต่ selector group ทั้งหมดยังต้อง survival แบบหนึ่งต่อหนึ่ง
- รักษาหลักฐาน packaging failure ใน pilot: overlap แบบ non-contact ระหว่างหลาย subsystem ถูกแก้ด้วย placement/feature จนรายงาน Boolean เป็น `0.0 m^3` โดยไม่ยกเว้น penetration แบบเงียบ
- ไม่ลดมวล `1023.65 kg` ที่คำนวณจาก geometry เพื่อให้ผลดูดี เก็บผลที่ขัดแย้งนี้ไว้ให้ Work 136 ทดสอบต่อ

## รายงานบัก

1. **CadQuery closed flag ให้ false-negative** อาการ: definition ที่เป็น valid one-solid รวมถึง plain box และ `active_stack` ถูกปฏิเสธเพราะ `Shape.Closed()` คืน `False` สาเหตุ: binding ของ CadQuery 2.8.0 ไม่เปิดเผย OCCT closed flag อย่างน่าเชื่อถือสำหรับ `TopoDS_Solid` เหล่านี้ การแก้: บังคับ `shape.isValid()` และมี `Solid` หนึ่งชิ้น แล้วตรวจ validity/count ซ้ำอิสระหลัง exact STEP import ด้วย FreeCAD การทดสอบซ้ำ: `test_cadquery_closed_flag_regression_uses_valid_single_solid` ผ่านและ STEP definition/occurrence ทั้ง 131 ไฟล์นำเข้าเป็น valid one-solid
2. **fan definition แยกเป็นสาม solid** อาการ: fan หกใบชุดแรก fuse เป็น solid ที่ไม่ต่อกันสามชิ้น สาเหตุ: ตำแหน่งรัศมี hub/blade เริ่มต้นซ้อนกันไม่พอให้เป็น finished form เดียว การแก้: เปลี่ยน hub radius เป็น `0.05 m`, blade-center radius เป็น `0.06 m` และ blade dimensions เป็น `[0.018, 0.12, 0.025] m` การทดสอบซ้ำ: `test_fan_definition_regression_is_one_fused_solid` และ admitted build ทั้งสองผ่าน
3. **semantic import gate อาจรายงานผ่านผิด** อาการ: รายงาน FreeCAD ช่วงแรกระบุ `passed` ทั้งที่ raw semantic survival มีเพียง `0.9458333333333333`; signed zero และการเปลี่ยน curved-face STEP seam ยังทำให้ signature หายแบบเท็จ สาเหตุ: status เดิมตรวจเฉพาะ invalid/null solid ขณะที่ raw exact hash รวมรายละเอียด parameterization ที่ไม่ใช่กายภาพ การแก้: canonicalize signed zero, quantize numeric field ที่ประกาศ, จับคู่ selector record แบบหนึ่งต่อหนึ่งด้วย positional tolerance `1e-7 m`, รักษา planar bounds/edge count แบบเข้ม, ถือ curved seam bounds/count เป็น diagnostic และรวม residual/count/hash/semantic threshold ทุกตัวเข้า inspector status การทดสอบซ้ำ: รายงานสุดท้ายผ่าน `754/754`, survival `1.0` และ negative control ที่ลด survival ถูกปฏิเสธ
4. **test environment ของ CadQuery import ไม่ได้** อาการ: คำสั่ง unit Work 135 รอบแรก exit 1 ด้วย `ModuleNotFoundError: No module named 'formula_ultimate'` สาเหตุ: CadQuery virtual environment ที่ตรึงไม่ได้ install local package และ test import ก่อนลงทะเบียน `src` การแก้: prepend repository root และ `src` แบบกำหนดซ้ำได้ใน test bootstrap การทดสอบซ้ำ: คำสั่งเดิม exit 0 และผ่าน 9 tests
5. **FCStd replay drift และ backup มี timestamp** อาการ: clean `run_b` ครั้งแรก exit 1; FCStd ที่เท่ากันมี document timestamp, UUID และ transient object ID ต่างกัน (`1df6ab...` เทียบ `eadd3d...`) และการ save ซ้ำอาจสร้าง `.FCBak` ที่มีเวลา สาเหตุ: metadata เอกสาร FreeCAD ไม่กำหนดซ้ำแม้ `Shape.bin` เหมือนกัน การแก้: save ไป FCStd ชั่วคราว, canonicalize เฉพาะ ZIP timestamp กับ metadata/object ID ที่ไม่ใช่ geometry, คง native shape bytes เดิม, replace witness แบบ atomic และไม่รับ backup/temp เป็นหลักฐาน การทดสอบซ้ำ: admitted run ทั้งสองให้ FCStd SHA-256 `3353e426...`, result SHA-256 `a9a3f555...` และ replay `exact: true`

## การตรวจสอบ

```powershell
& 'C:\Formula Ultimate\.tools\cadquery-mcp\Scripts\python.exe' -m unittest tests.test_native_detailed_vehicle -v
# รอบแรกก่อนแก้บัก 4 exit 1; รอบสุดท้าย exit 0; ผ่าน 9 tests
& 'C:\Formula Ultimate\.tools\cadquery-mcp\Scripts\python.exe' scripts/cad/build_native_detailed_vehicle.py --config config/development/native_detailed_vehicle_v1.json --output-root artifacts/work135/run_a/cad --manifest artifacts/work135/run_a/cadquery_manifest.json
# exit 0; 48 definitions, 83 instances, 77 material solids, 6 void solids, non-contact penetration 0.0 m^3
& 'C:\Program Files\FreeCAD 1.1\bin\python.exe' scripts/cad/inspect_native_detailed_vehicle_freecad.py artifacts/work135/run_a/cadquery_manifest.json config/development/native_detailed_vehicle_v1.json artifacts/work135/run_a/freecad_report.json artifacts/work135/run_a/native_vehicle_tri_contact_native_135_r1.FCStd
# exit 0; exact no-repair import; 48 definitions และ 83 instances valid; semantic survival 1.0
& 'C:\Formula Ultimate\.tools\cadquery-mcp\Scripts\python.exe' scripts/development/run_native_detailed_vehicle.py --config config/development/native_detailed_vehicle_v1.json --output-root artifacts/work135/run_a
# exit 0; passed_native_detailed_geometry; controls ถูกปฏิเสธ 18/18; result SHA-256 a9a3f55571bf5b5441c3ef3e8b2674623305d8c1fb02814dcf87cd4a1b9b7d3c
& 'C:\Formula Ultimate\.tools\cadquery-mcp\Scripts\python.exe' scripts/development/run_native_detailed_vehicle.py --config config/development/native_detailed_vehicle_v1.json --output-root artifacts/work135/run_b --replay-reference artifacts/work135/run_a/result.json
# รอบแรกก่อนแก้ FCStd exit 1; รอบสุดท้าย exit 0; exact replay
python -m compileall -q src scripts tests
# exit 0
python -m unittest tests.test_spatial_material tests.test_geometry_mesh_bridge tests.test_physical_interface_graph tests.test_detailed_connection_contact tests.test_moving_contact_assembly tests.test_realized_actuation_chain tests.test_onboard_energy_realization tests.test_geometry_flow_heat_exchange tests.test_control_hardware_realization tests.test_repository_contract -v
# exit 0; ผ่าน 61 tests
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; มี maintained files ของ Work 135 ที่ประกาศไว้ตรงกัน 12 ไฟล์
git diff --cached --check
# exit 0
```

## ข้อจำกัดและงานถัดไป

CadQuery กับ FreeCAD ใช้ OCCT เหมือนกัน จึงเป็น cross-application witness ไม่ใช่ independent-kernel validation วัสดุ geometry บางรายการใช้ synthetic geometry-only density และยังไม่มี supplier-certified purchased geometry, process qualification หรือ physical correlation assembly gate ไม่ได้ยืนยัน component-specific serviceability ของทุกชิ้น motion ที่ลงทะเบียนพิสูจน์เฉพาะการหมุนยางหน้าที่ axisymmetric ส่วน non-axisymmetric steering ยังไม่ได้ model

ต้องท้าทายมวลที่สูงมากของแบบที่ยังไม่ optimize และข้อสรุปเดิมด้าน structural, thermal, internal/external flow, ground, actuation, energy และ controller ทั้งหมดบน solid Work 135 ชุดนี้ Work 136 เป็นข้อบังคับก่อนคำกล่าวอ้างด้าน performance, feasibility, promotion, manufacturing, safety หรือ physical validation ทุกชนิด
