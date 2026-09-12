# สัญญารถละเอียดแบบเนทีฟ V1

แหล่งภาษาอังกฤษ: `NATIVE_DETAILED_VEHICLE_V1.md`

รหัสโปรโตคอล: `native_detailed_vehicle_v1`

## วัตถุประสงค์และขอบเขตคำกล่าวอ้าง

สัญญานี้ยอมรับ candidate ที่แน่นอนหนึ่งตัวก็ต่อเมื่อ occurrence ทางกายภาพที่จำเป็นถูกทำเป็น solid แบบ native OCCT B-rep ที่กำหนดซ้ำได้ เชื่อมเป็น assembly เดียวอย่างชัดเจน และ FreeCAD นำเข้าจากไบต์ STEP ชุดเดียวกันโดยไม่มีการซ่อมแฝง สถานะผ่านมีเพียง `passed_native_detailed_geometry`

สถานะนี้ยืนยันเฉพาะ geometry, assembly, ownership, interface และการมีอยู่ของ boundary ไม่ได้ยืนยันประโยชน์ด้านสมรรถนะ ความถูกต้องทางฟิสิกส์ ความพร้อมผลิต ความปลอดภัย การตรวจสอบกับของจริง หรือการเลื่อนระดับ ต้องรันฟิสิกส์ปลายน้ำใหม่ทั้งหมดบน solid ชุดนี้ใน Work 136

## เอกลักษณ์และอินพุตที่ตรึง

declaration ต้องมี:

- candidate ID ที่ต่างจาก `final_126_r1`, revision, งานภายนอก, ขอบเขตพลังงานหลัก, ขอบเขตความปลอดภัยแบบดิจิทัลเท่านั้น และ claim scope `native_geometry_and_assembly_only`;
- commit, contract, result log, artifact file และ inner-result SHA-256 ที่แน่นอนของ Works 108, 110, 112–123, 125, 126, 129 และ 130;
- การตรวจ SHA-256 ต่อไฟล์ของ geometry ต้นทางจาก Works 83, 84, 87, 108 และ 113 พร้อม disposition `reuse_exact` หรือ `regenerate_for_candidate` ที่ชัดเจน;
- เอกลักษณ์ที่แน่นอนของ CadQuery Python, CadQuery, FreeCAD Python, FreeCAD, OCCT, Gmsh และ CalculiX;
- หน่วย SI, threshold ที่กำหนดซ้ำได้, ตัวแปรทดลอง, control, metric, เกณฑ์สำเร็จ/ล้มเหลว และช่องทบทวน falsification

ไฟล์ที่หาย hash ไบต์ที่เปลี่ยน commit ที่หาย หรือเอกลักษณ์ runtime ที่เปลี่ยนต้องล้มแบบ fail-closed

## ชิ้นส่วนเนทีฟและ occurrence

definition แต่ละรายการระบุเอกลักษณ์ที่คงที่ตาม revision, ownership ของ material หรือ void ที่มวลเป็นศูนย์, material/process ID, provenance ที่มีสิทธิ์, representation `native_occt_brep`, นโยบายหนึ่ง closed solid, finished-form flag, construction-feature inventory และ semantic face selector ห้ามใช้ตัวระบุถาวรแบบดิบ `FaceN` หรือ `EdgeN`

primitive ที่มี envelope เท่าเดิมไม่มีสิทธิ์ เว้นแต่ primitive นั้นเป็นรูปสำเร็จที่ตั้งใจจริงและมี seat, hole, passage และ end feature ที่จำเป็นครบ geometry ที่ซื้อต้องมี supplier, source URI และ source hash พร้อม `proxy: false`; proxy ที่ไม่มีหลักฐานต้องกันไม่ให้ผ่าน

occurrence ที่เกี่ยวข้องทุกชิ้นต้องมี instance ID, region ID, placement, occurrence class และ mass ownership เฉพาะตัว class ที่บังคับครอบคลุมโครงสร้าง วัตถุสัมผัสพื้นและส่วนรองรับ ระบบขับและส่งกำลัง พลังงานบนรถ control/sensor ระบบหล่อเย็น/การไหล geometry เปียกภายนอก/ช่องเปิด fastener/seal harness และเส้นทาง service/load/thermal coverage ต้องเท่ากับ `1.0` พอดีและ unknown essential occurrence ต้องเป็นศูนย์

## gate ของ assembly, tolerance, route และ motion

instance ที่ไม่ใช่ root ทุกชิ้นต้องเดินถึง root เดียวผ่าน joint ชัดเจนหรือ approved non-contact relation ที่มีเหตุผล relation แบบสัมผัสต้องระบุ semantic mating face, anchor ที่ตรงกัน, unit axis, สถานะ tolerance แบบ nominal และ worst-case, interface ownership รวมถึงฮาร์ดแวร์ยึดหรือซีลเมื่อเกี่ยวข้อง

ขีดจำกัดการยอมรับคือ:

- mating residual `<= 1e-6 m`;
- non-contact penetration `<= 1e-12 m^3` โดย Boolean failure ต้องมองเห็นและทำให้ล้ม;
- assembly ต้องไม่มีวงจร ไม่มี floating component และไม่มี material/void region ซ้ำ;
- fastener engagement เป็นบวกและ seal compression อยู่ในช่วงที่ประกาศ;
- endpoint ของ route ต่างกัน actual bend radius ไม่น้อยกว่า required radius และ minimum clearance ไม่ติดลบ;
- motion อย่างน้อย 101 sample และ refinement change `<= 1e-5 m` พร้อม analytic swept envelope และเปิดเผย between-sample risk ของ motion ที่ลงทะเบียน

## หลักฐาน STEP และ FreeCAD

CadQuery ส่งออก STEP ที่ทำเวลาเป็น canonical สำหรับทุก definition และ occurrence รวมถึง assembly material กับ void แยกกัน และคำนวณ volume, mass, center และ full inertia จาก native geometry กับ density ที่ประกาศ STL preview ไม่ใช่หลักฐานและใช้ chord tolerance `<= 0.00025 m`

FreeCAD อ่าน occurrence/assembly STEP ตาม hash เดิมโดยไม่ซ่อม บังคับหนึ่ง valid solid ต่อ occurrence และคำนวณ native property ใหม่ ขีดจำกัดข้ามแอปคือ relative volume และ mass `<= 1e-8`, absolute center `<= 1e-7 m` และ inertia `<= 1e-7` เทียบกับ component scale ที่ลงทะเบียน

semantic face จับคู่ด้วย surface type, area และ centroid ภายใต้ numeric tolerance ที่ประกาศ ส่วน planar orientation, bounds และ edge count ต้องตรงด้วย periodic curved face อาจย้าย parameter seam ตอนถ่ายผ่าน STEP จึงถือ curved-face axis-aligned bounds และจำนวน seam edge เป็นข้อมูลวินิจฉัย ไม่ใช่เอกลักษณ์ทางกายภาพ แต่ selector group ที่ประกาศทั้งหมดยังต้องจับคู่แบบหนึ่งต่อหนึ่งและ survival ต้องเท่ากับ `1.0`

FCStd witness ทำ canonical เฉพาะเวลาใน archive, ข้อความเวลาสร้าง/แก้เอกสาร, document UUID และหมายเลข object ชั่วคราว โดยไม่เปลี่ยนหรือ heal native geometry ใน `Shape.bin`

## การมีอยู่ของ physics boundary

declaration ทำแผนที่ semantic face หรือ region สำหรับ structural, thermal, internal-flow, external-aerodynamic, ground-motion, energy และ controller/sensor domain สิ่งนี้พิสูจน์เพียงว่ามี boundary ที่มีเจ้าของบน geometry ชุดแน่นอน domain ไม่ครบ instance ไม่รู้จัก หรือ selector หายต้องล้ม

## หลักฐานบังคับและ replay

ผล admitted ประกอบด้วย STEP ต่อ definition/instance, STEP assembly material/void แยก, FCStd, รายงาน CadQuery/FreeCAD, แผนที่ semantic/interface/material-void/physics, รายงาน mass-inertia, collision-clearance, motion และ tolerance, manifest exploded/section ที่มาจาก native geometry, independent component audit, negative-control 18 รายการ และ `result.json`

ห้ามนำผล `pilot` มา admitted ส่วน `run_a` และ clean `run_b` ต้องมี declaration, artifact และ result hash ตรงกันทุกประการ replay drift ต้องล้ม

## falsification control

runner ต้องปฏิเสธครบ 18 กลุ่มตามแผน Work 135: primitive substitution; occurrence หาย; floating component; ownership ซ้ำ; solid ไม่ถูกต้อง; STEP ถูกแก้; repair แฝง; semantic หาย; axis/engagement ล้ม; worst-case ล้ม; swept collision; assembly เป็นวงจร/ติดค้าง; route ล้ม; void มี structural density; ช่องเปิด external-flow หาย; purchased proxy ไม่มีหลักฐาน; เอกลักษณ์ต้นทางเปลี่ยน; และหลักฐานแบบ render เท่านั้น

ต้องเลือก material component อย่างน้อยหนึ่งชิ้นแบบกำหนดซ้ำได้จากดัชนีที่มาจาก SHA-256 โดยไม่เลือกตาม proxy score แล้วตรวจ feature, section, interface, ownership และ access หากไม่มี service relation เฉพาะชิ้นต้องคงเป็นข้อจำกัดชัดเจน ไม่สร้างผลผ่านขึ้นเอง

## สถานะและสิ่งที่ไม่ทำ

หลักฐานที่ล้มต้องมองเห็นเป็น `invalid_native_geometry`, `incomplete_part_realization`, `assembly_unresolved`, `physics_mapping_unresolved` หรือ validation exception ที่ระบุสาเหตุ ห้าม repair แฝงหรือใช้ aggregate ที่กรอกเองทับ geometry

สัญญานี้ไม่บังคับจำนวนล้อ ความสมมาตร รูปทรงตัวถัง หรือ powertrain แบบ conventional; ไม่อนุญาตการผลิต; ไม่สืบทอดข้อสรุปฟิสิกส์ Work 123–130 จาก box geometry; และไม่เรียกหลักฐาน Level-0/ข้ามแอปว่า physical validation
