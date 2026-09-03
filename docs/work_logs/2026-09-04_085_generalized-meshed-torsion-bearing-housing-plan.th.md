# แผน Work 085: เส้นทางเมชทั่วไปสำหรับแรงบิด แบริ่ง และ Housing

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_085_generalized-meshed-torsion-bearing-housing-plan.md`

## สถานะ

สถานะ: Stopped

## วัตถุประสงค์

ปิด blocker ด้านโครงสร้างแบบเมชที่ Work 084 บันทึกไว้อย่างชัดเจน โดยไม่แก้ Work 082 หรือเขียน Work 084 ย้อนหลัง เพิ่มเส้นทาง Gmsh/CalculiX จากรูปทรง exact ที่รองรับ end face ตามแกนหลักใด ๆ, cylindrical bearing surface, โหลดแรง/แรงบิดร่วม และ support plane ใด ๆ แล้วนำไปใช้กับ STEP exact ของ `output_shaft`, `support_block` และ `converter_housing` จาก Work 084

งานแก้นี้ถูกแทรกก่อนขอบเขต integration เดิม ดังนั้นงาน integration ที่เดิมเป็น Work 085 จะเลื่อนไป Work 086 และ whole-mechanical candidate ที่เดิมเป็น Work 086 จะเลื่อนไป Work 087 แผน roadmap เดิมคงไว้โดยไม่แก้ย้อนหลังเพื่อเป็นหลักฐาน append-oriented

## ขอบเขตและการทดลองที่ตรึงไว้

- ผูกตัวตนทุกกรณีกับผล Work 084 `c87fa43572efc0a8bc6ef67e375589943d73ecc4ca3b3a3d7a51df4ddb3edb66`, canonical FreeCAD report และ STEP hash exact ของแต่ละชิ้น
- mesh ชิ้นส่วน exact สามชิ้นแยกกันด้วย characteristic length ที่ preregister สามระดับต่อชิ้น
- `output_shaft_combined`: ใส่แรงปฏิกิริยา radial ที่ interface Work 083 `415.3846153846154 N` ร่วมกับแรงบิด output `22.8 Nm` ที่ปลาย `y=0.019 m`; ยึดปลาย `y=0.086 m`
- `support_block_bearing`: ใส่แรงปฏิกิริยา support `384.6153846153847 N` บนรูแกน `y`; ยึด mounting plane `x=-0.100 m`
- `converter_housing_mount`: ใส่แรงบิดปฏิกิริยา converter `8 Nm` บนรูแกน `y`; ยึด mounting plane `x=-0.080 m`
- สร้างแรงและคู่แรงที่ node แบบสอดคล้องกับพื้นที่ผิว รายงาน reaction, displacement, compliance, p90 von Mises stress, external/internal work และ force/moment residual
- รัน mesh convergence แยกแต่ละกรณี ห้ามซ่อน non-convergence หรือสถานะ failed/invalid
- คงตัวตนวัสดุ Work 079 และ `design_use_allowed=false`; หลักฐานซอฟต์แวร์แบบเมชไม่ใช่ physical validation
- ฉีด severed-support control ทุกกรณี และบังคับให้แรงที่ส่งเป็นศูนย์พร้อม subsystem rejection/`DNF`
- รัน solver สอง root ใหม่แล้วเปรียบเทียบ canonical identity

ตัวแปรอิสระคือชิ้นส่วน exact, ชนิด load region, support plane, แรง, แรงบิด, mesh length และ connection state ตัวแปรตามคือจำนวน node/element, node/พื้นที่ผิวที่ map, displacement, compliance, p90 stress, force/moment/energy residual, convergence, elastic/yield state และ failure propagation Controls คือ exact replay, identity mutation, ผิวหาย, โหลดไม่ finite, mesh non-convergence และ severed support

## ไฟล์ที่วางแผนแก้ไข

- `config/structural/generalized_meshed_torsion_bearing_housing_v1.json`
- `src/formula_ultimate/structural/generalized_coupling.py`
- `scripts/structural/run_generalized_structural_coupling.py`
- `tests/test_generalized_structural_coupling.py`
- `docs/contracts/GENERALIZED_MESHED_STRUCTURAL_COUPLING_V1.md` และไฟล์คู่ภาษาไทย
- แผนนี้และไฟล์คู่ภาษาไทย
- result ที่ตรงกันและไฟล์คู่ภาษาไทยหลัง validation
- หลักฐานที่ ignore ภายใต้ `artifacts/work085/`

## การตรวจสอบ

1. รัน Gmsh/CalculiX จากรูปทรง exact ทั้งเก้ากรณีภายใต้ output root ใหม่
2. ตรวจ surface mapping, solver freshness/convergence, การปิด force/moment/energy และการเปลี่ยนแปลงสอง mesh สุดท้ายแยกตามกรณี
3. รัน root ใหม่รอบสองและเปรียบเทียบ result กับ canonical solver-artifact identity
4. รัน focused tests, repository-contract tests, Python compilation และ repository suite เต็ม
5. stage เฉพาะไฟล์ Work 085 รัน `git diff --cached --check`, commit และตรวจ focused post-commit ซ้ำ

## เกณฑ์สำเร็จ

- STEP exact และตัวตน upstream result/report ทุกค่าตรงก่อน mesh
- load/support region ทุกกรณี map ได้อย่างไม่กำกวมและไม่ทับกัน
- solver ทั้งเก้ากรณี converge โดยไม่มี hidden geometry repair หรือการแก้สถานะเงียบ ๆ
- force และ moment residual แต่ละค่า `<=1e-5`; energy residual `<=1e-4`
- ทุกกรณีมีการเปลี่ยนของ maximum displacement, compliance และ p90 stress ไม่เกิน `12%` ระหว่าง mesh สองระดับสุดท้าย
- กรณี elastic ต้องต่ำกว่าค่า yield synthetic หรือ fail อย่างสังเกตได้ ห้าม clip stress
- severed-support control ทุกกรณีตัดแรงส่งและทำให้ reject/`DNF`
- สองรันสร้าง config/result และ canonical mesh/deck/DAT/FRD identity ซ้ำได้
- verdict ยังเป็น `synthetic_meshed_verification_only` และ `design_use_allowed=false`

## ความเสี่ยง

- การ map node บนผิวโค้งอาจล้มเหลวจาก tolerance ของ mesh
- stress concentration เฉพาะที่หรือ tetrahedra หยาบอาจทำให้ p90 ไม่ converge
- รูปทรง housing อาจต้องใช้ระดับ mesh หยาบกว่าเพื่อจำกัด compute
- คู่แรงที่ node เชิงพีชคณิตอาจปิดสมดุลรวมได้ แต่ยังเป็นแบบจำลอง bearing/contact อย่างง่าย

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่อ้าง physical validation, fatigue, fracture, nonlinear contact, fastener, bearing life, lubrication, manufacturing หรือ safety
- ไม่แก้ตัวตน Work 082 หรือเปลี่ยนสถานะ Work 084 ย้อนหลัง
- ไม่ทำ design admission จากหลักฐานวัสดุ/กระบวนการ synthetic
- ไม่ทำ load-structure integration หรือ whole-vehicle candidate ใน work item นี้
