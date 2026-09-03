# แผน Work 082: Geometry-to-Structural Physics Coupling V1

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-03_082_geometry-structural-coupling-v1-plan.md`

## วัตถุประสงค์และขอบเขต

สร้าง coupling แบบ fail-closed จาก exact STEP identity ของ Work 081 และ geometric region ที่ค้นได้ ไปยังการทดลองโครงสร้าง CalculiX แบบ mesh สามระดับ ชุดอ้างอิงที่มีขอบเขตจะใช้ canonical part หนึ่งชิ้นจาก Work 078/081, support/load signature ที่ immutable, แหล่งที่มาของโหลดหน่วย SI ที่ชัดเจน, exact material identity ของ Work 079, การ parse ผล solver, gate ของ convergence/residual, การจำแนก failure และการส่งต่อ connection state เชิงสาเหตุ

เนื่องจากหลักฐาน material/process ของ Work 079 ยังเป็น synthetic Work 082 จึงจำกัดเป็น `synthetic_verification` การเสร็จงานหมายถึงเส้นทาง software จาก geometry-to-mesh-to-solver-to-failure และ controls ถูกตรวจสอบ โดยต้องคืน `design_use_allowed=false` และห้ามยืนยัน capacity ของชิ้นส่วนจริง

## การออกแบบการทดลอง

- ตัวแปรอิสระ: exact STEP hash, mesh characteristic length, support/load region signature, ขนาด/ทิศแรง, synthetic material identity/properties, section geometry, connection criticality และ fault ของ solver/material/path ที่ฉีดโดยเจตนา
- ตัวแปรตาม: จำนวน node/element, displacement, stress, reactions, strain energy, force/moment/energy residual, การเปลี่ยนระดับ refinement สองระดับท้าย, failure class, transmitted wrench, connection state, subsystem state และ deterministic identities
- ตัวควบคุม: mesh สามระดับที่ freeze, key-order replay, แรงกลับทิศ, analytical control ที่หนากว่า, STEP hash เปลี่ยน, support/load surface หาย, mesh/path ขาด, reference ต่ำกว่า yield, overload ข้าม yield/ultimate domain, fracture/fatigue domain ที่ไม่รองรับ, connection critical เทียบ redundant และการฉีด solver non-convergence
- สมมติฐานที่ต้องการ: exact geometry/region identity ไปถึง solver artifacts ทุกชิ้น, reaction และ energy ปิดใน gate, response ที่ยอมรับ converge และ critical structural failure ลบ transmitted wrench พร้อมสร้าง deterministic `DNF`
- การหักล้าง: ใช้มิติที่พิมพ์แทน geometry, รับ STEP/report hash เก่า, ซ่อน non-convergence, clip stress/failure เงียบ, ส่ง load หลัง connection fail หรืออนุมัติ synthetic material สำหรับ design use

## ไฟล์ที่วางแผน

- `config/structural/geometry_structural_coupling_v1.json`
- `src/formula_ultimate/structural/geometry_coupling.py`
- `scripts/structural/run_geometry_structural_coupling.py`
- `tests/test_geometry_structural_coupling.py`
- `docs/contracts/GEOMETRY_STRUCTURAL_COUPLING_V1.md` และไฟล์ภาษาไทย
- matching Work 082 result records
- mesh, deck, solver output, parsed evidence และ replay record ที่ ignore ใต้ `artifacts/work082/`

## การตรวจสอบและเกณฑ์สำเร็จ

- exact Work 081 part/report/interface identity ต้องผูกเข้าสู่ record ทุก mesh level;
- mesh refinement สามระดับรันผ่าน local Gmsh/CalculiX toolchain ที่ pin โดยไม่แก้ geometry;
- integrated reaction force/moment relative residual `<=1e-5` และ strain-energy/work relative residual `<=1e-4`;
- การเปลี่ยน displacement/compliance และ stress แบบ non-singular สองระดับท้าย `<=5%`;
- negative controls ปฏิเสธ stale identity, region/path หาย, evidence ไม่รองรับ, invalid/numerical state และ residual/convergence ที่ล้ม;
- failure เปลี่ยน connection state และ transmitted wrench เชิงสาเหตุ; failure ที่ critical ตาม declaration ให้ deterministic `DNF`;
- exact replay, focused tests, repository contract, compilation และ full regression ผ่านก่อน scoped commit

## ความเสี่ยงและสิ่งที่ไม่อ้าง

pointwise peak stress ใกล้ idealized constraint อาจ singular และไม่ใช่ metric ที่ยอมรับ ให้ใช้ metric แบบ non-singular/integrated ที่ประกาศ เส้นทาง geometry ที่ใช้ OCCT ร่วมกันไม่ใช่ physical validation ค่าวัสดุ synthetic สนับสนุน real allowable, fatigue/fracture life, crashworthiness, safety หรือ production claim ไม่ได้ หาก solver ไม่ converge, residual ปิดไม่ได้, mesh response ไม่ refine หรือ structural event ไม่เปลี่ยน connection graph Work 082 จะหยุดแทนการใช้ผล fidelity ต่ำกว่า
