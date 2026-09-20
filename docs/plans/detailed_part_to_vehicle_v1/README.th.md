# แผนละเอียดราย Work: การค้นพบชิ้นส่วนไปจนถึงรถทั้งคัน

ต้นฉบับภาษาอังกฤษ: `README.md`

วันที่: 2026-09-09 (Asia/Bangkok) จัดทำโดย Work 107 จริง ซึ่งเริ่มเมื่อ 2026-09-07

Status: Planned implementation specifications; ชุดแผนนี้ยังไม่ได้พัฒนาความสามารถของงานอนาคต

## 1. ข้อกำกับและหมายเลข

อ่าน [roadmap Work 106](../../reports/DETAILED_PART_TO_VEHICLE_DISCOVERY_ROADMAP_V1_2026-09-07.th.md) สำหรับจุดหมาย และ [protocol กำกับ Work 104](../../contracts/WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.th.md) สำหรับกติกาวิทยาศาสตร์ ฟิสิกส์ ทรัพยากร และการเลื่อนระดับหลักฐาน

Work 107 จริงคือการขยายเอกสารครั้งนี้ ดังนั้นหมายเลข packages ที่ Work 106 เคยเสนอเป็น 107–132 จึงเทียบเป็น Works 108–133 สำหรับการพัฒนาด้านล่าง นี่เป็นการเทียบลำดับเดินหน้าอย่างชัดเจน ไม่ใช่เขียน roadmap เก่าใหม่ ข้อเสนอเดิม “Work 107 ถัดไป = spatial material” จึงเป็น Work 108 หมายเลขอนาคตยังไม่จอง ถ้ามีงานแทรกใช้เลข ให้เลือกหมายเลขว่างถัดไปและเพิ่มบันทึกเทียบเมื่อเริ่มทำจริง

ไฟล์เหล่านี้เป็นข้อกำหนดวางแผน ไม่ใช่ work logs ที่เริ่มแล้ว ก่อนพัฒนา package ต้องสร้าง work-log plan สองภาษาลงวันที่และสถานะ `In progress` ไม่ทำให้งานอนาคตทั้งหมด in progress ตอนนี้ คำขอนี้อนุญาตให้วางแผน ไม่ใช่ทดสอบของจริงที่อธิบายช่วงท้าย

## 2. ดัชนีและตารางเทียบเลขเก่า–ใหม่

แผนแต่ละลิงก์มีหลักฐานก่อนเริ่ม ไฟล์ที่เสนอ ขั้นพัฒนา ตัวแปร/ตัวควบคุม negative tests ตัวเลขที่ต้องลงทะเบียน เกณฑ์รับ artifacts ความเสี่ยง และงานรับต่อ

| งานที่เสนอ | Package เดิม | แผนละเอียด | ความสามารถที่พึ่งพา |
|---|---|---|---|
| 108 | 107 | [ข้อมูลต้นทางร่วมของเนื้อวัสดุและช่องว่าง](work108-spatial_material.th.md) | CAD เดิม |
| 109 | 108 | [ตัวสร้างเนื้อวัสดุรูปทรงอิสระ](work109-freeform_material_generator.th.md) | 108 |
| 110 | 109 | [สะพานจาก geometry จริงสู่ mesh](work110-geometry_mesh_bridge.th.md) | 108, 109 |
| 111 | 110 | [สนามของแข็งแบบ vector จาก geometry ที่สร้าง](work111-vector_solid_fields.th.md) | 110 |
| 112 | 111 | [terminals ทางกายภาพและความหมายการประกอบ](work112-physical_interface_graph.th.md) | 108 |
| 113 | 112 | [พิสูจน์การยึดและ contact แบบละเอียด](work113-detailed_connection_contact.th.md) | 111, 112 |
| 114 | 113 | [ชุดประกอบเคลื่อนที่และยืดหยุ่นที่มี contact](work114-moving_contact_assembly.th.md) | 113 |
| 115 | 114 | [ความร้อนตามเวลาเชื่อมกับของแข็ง](work115-coupled_thermal_solid.th.md) | 111, 113 |
| 116 | 115 | [ที่มาวัสดุและความเสียหายตามขอบเขต](work116-material_failure_scope.th.md) | 111, 114, 115 |
| 117 | 116 | [โจทย์สองทางระหว่างสถาปัตยกรรมกับชิ้นส่วน](work117-architecture_part_feedback.th.md) | 112, 114, 115 |
| 118 | 117 | [ปฏิสัมพันธ์พื้น การหยุด และควบคุมทิศทาง](work118-ground_interaction_tasks.th.md) | 114, 116 |
| 119 | 118 | [ชุดส่งกำลังและ actuation ที่มีฮาร์ดแวร์จริง](work119-realized_actuation_chain.th.md) | 114, 115, 116 |
| 120 | 119 | [การทำระบบพลังงานบนรถให้เกิดจริงอย่างละเอียด](work120-onboard_energy_realization.th.md) | 115, 116, 119 |
| 121 | 120 | [การไหลและแลกเปลี่ยนความร้อนจาก geometry](work121-geometry_flow_heat_exchange.th.md) | 110, 115, 116 |
| 122 | 121 | [controller, sensor และฮาร์ดแวร์รองรับ](work122-control_hardware_realization.th.md) | 119, 120 |
| 123 | 122 | [ระบบรัน candidate ทั้งคันแบบ coupled transient](work123-coupled_vehicle_transient.th.md) | 117, 118, 119, 120, 121, 122 |
| 124 | 123 | [การค้นพบหลายสเกลและบัญชีต้นทุนเป็นธรรม](work124-multiscale_discovery_search.th.md) | 109, 117, 123 |
| 125 | 124 | [การเปรียบเทียบค้นพบชิ้นส่วนละเอียดที่ลงทะเบียน](work125-detailed_part_comparison.th.md) | 113, 114, 115, 116, 124 |
| 126 | 125 | [candidate ดิจิทัลละเอียดครบทั้งคัน](work126-detailed_vehicle_closure.th.md) | 118, 119, 120, 121, 122, 123, 124, 125 |
| 127 | 126 | [baseline รถที่ปรับดีและการแทนชิ้นเพื่อทดสอบเหตุ](work127-optimized_vehicle_controls.th.md) | 123, 126 |
| 128 | 127 | [การแข่ง held-out และความทนทาน](work128-heldout_race_robustness.th.md) | 127 |
| 129 | 128 | [ตรวจคำกล่าวอ้างอิสระด้วย fidelity สูงขึ้น](work129-independent_claim_validation.th.md) | 125, 126, 127, 128 |
| 130 | 129 | [ส่งต่อการผลิต tolerance และการประกอบ](work130-manufacturing_tolerance_handoff.th.md) | 126, 129 |
| 131 | 130 | [การวัดวัสดุและจุดเชื่อมเมื่อได้รับอนุญาต](work131-physical_connection_correlation.th.md) | 113, 116, 130 |
| 132 | 131 | [เทียบ subsystem จริงและความทนทานเมื่อได้รับอนุญาต](work132-physical_subsystem_correlation.th.md) | 131 |
| 133 | 132 | [โปรแกรมตรวจรถทั้งคันเมื่อได้รับอนุญาต](work133-physical_vehicle_validation.th.md) | 128, 129, 130, 131, 132 |
| 135 | — | [Native detailed vehicle realization](work135-native_detailed_vehicle_realization.th.md) | 108, 110, 112–123, 125, 126, 129, 130 |
| 138 | — | [Structural evaluator ที่รับ geometry ใดก็ได้](work138-geometry_general_evaluator.th.md) | 062, 078, 092, 110, 111, 135 |
| 139 | — | [Vehicle candidate ที่ใช้รูปทรงอิสระ](work139-freeform_vehicle_candidates.th.md) | 047, 091, 092, 138 |
| 140 | — | [ความละเอียดของชิ้นส่วนและระบบข้อต่อ](work140-part_resolution_joint_systems.th.md) | 092, 135, 138, 139 |

เลข 136 และ 137 ถูกใช้ไปกับงานที่ดำเนินการแล้ว โดย 136 ซ่อม test guard ของ CadQuery ที่เป็น optional พร้อมอัปเดตเอกสารสถานะ และ 137 เขียนการ์ด Work 138 ด้านล่าง ส่วนบันทึกของ Work 135 เรียกงานรันฟิสิกส์ต่อบน native solids ว่า "Work 136" งานนั้นจะใช้เลขถัดไปที่ยังว่างตอนลงมือ Work 138 เป็นส่วนขยายเชิงแก้ไข เพราะ evaluator ที่ bounded campaign ใช้อ่านตัวแปรสเกล 5 ตัวแทนที่จะอ่าน geometry รูปทรงนอก template จึงให้คะแนนไม่ได้ ส่วน Work 139 เปิด grammar รูปทรงอิสระให้ candidate ของรถ มีสเปกและดำเนินการแล้ว ส่วนเลข 140 ถูกใช้กับ gate ความละเอียดของชิ้นส่วนและระบบข้อต่อ ซึ่งวัดว่าชิ้นส่วนถูกโมเดลที่ระดับความละเอียดจริงหรือไม่ และข้อต่อที่ประกาศมีผิวต่อที่วัดได้หรือไม่ ส่วนการป้อนผล evaluator เข้าสู่เวลาแข่งจะใช้เลขถัดไปที่ยังว่าง

dependency ในตารางหมายถึงความสามารถขาเข้าที่ต้องใช้สำหรับขอบเขตครบ ไม่ใช่ต้องรอก่อนเริ่มเตรียมงานทุกอย่าง Work 110 เริ่ม B-rep ได้ก่อน representation ใหม่พร้อม Work 112 เดินต่อหลัง spatial geometry ขณะพัฒนา meshing ได้ search ย่อยของ Work 124 เริ่มหลัง Work 117 ได้ ส่วนโหมดรถต้องมี Work 123 เพิ่ม ห้ามอ้าง package ครบถ้าส่วนจำเป็นที่ประกาศยังขาด

Work 132 ต้องมีทุกโดเมนที่พัฒนาและเกี่ยวข้องกับ subsystem ที่เลือกเพิ่มด้วย Work 133 ต้องมีหลักฐาน physical subsystem ที่เกี่ยวข้อง qualified safety review และอำนาจอนุญาตแยก การอ้าง dependency เป็นตัวเลขอย่างเดียวไม่ถ่ายโอนหลักฐานออกนอกช่วง load/material/temperature/geometry เดิม

## 3. ข้อกำหนดดำเนินงานร่วม

ทุกแผนรายงานรับข้อกำหนดต่อไปนี้ร่วมกัน การไม่พิมพ์ซ้ำในแผนสั้นไม่ใช่การยกเว้น

1. อ่านข้อกำหนด repository ที่ใช้ ตรวจ checkout, source state และ upstream artifact identities ปัจจุบัน รักษา edits ที่ไม่เกี่ยวและหลักฐานประวัติ
2. ล็อกคำถามที่มีขอบเขต physical domain, SI conventions, โจทย์ภายนอก material/data eligibility, inputs และสิ่งที่ไม่ทำ แยก software fixtures, exploratory pilots และ admitted comparisons
3. พัฒนา geometry/model/adapter จริงพร้อม tests ทุก physical law หรือ component model ที่เพิ่ม การประกาศหรือป้าย coverage อย่างเดียวไม่ใช่ implementation
4. รัน CAD/mesh/solver dependencies จริงสำหรับความสามารถที่อ้าง Python ในคำสั่งแต่ละแผนหมายถึง runtime ที่ตรวจแล้วว่ามี dependencies เหล่านั้น ให้แทนด้วย executable ที่ resolve จริงใน execution log การ skip dependency test ที่จำเป็นบล็อกการจบความสามารถนั้น
5. ตรวจตามขอบเขตและรัน regressions upstream/downstream ที่กระทบ ใช้ full suite เมื่อความเสี่ยงการเปลี่ยนสมควร บันทึก environment exclusions และไม่นับว่าเป็นหลักฐานทางฟิสิกส์
6. สร้าง result logs สองภาษาพร้อมคำสั่งจริง exit outputs ข้อจำกัดและงานต่อ เปลี่ยน execution plan เป็น `Completed` เฉพาะเมื่อ gates ผ่าน commit ขอบเขตชัดทันที ตรวจและรายงาน hash ถ้า commit ไม่สำเร็จงานยังไม่ครบ ไม่ push หรือเขียนประวัติใหม่
7. เก็บผลทดลองเดิมทั้งหมด สมมติฐานวิทยาศาสตร์ล้มเหลวเป็นการทดลองที่จบได้เมื่อ execution/reporting gates ผ่าน แต่ไม่บรรลุหมุดหมายค้นพบผลบวก

ไฟล์ที่เสนอในแต่ละแผนเป็นจุดแบ่ง implementation เริ่มต้น ไม่ใช่คำสั่งให้สร้างโมดูลซ้ำ เมื่อดำเนินการให้ตรวจ APIs เดิมและใช้ซ้ำตามเหมาะสม บันทึกเหตุผลเปลี่ยน path ในแผนใหม่ สร้าง contract สองภาษาใน `docs/contracts/` และ work logs สองภาษาตามข้อกำหนดสำหรับทุก package ที่พัฒนา CLI ที่เสนอต้องพัฒนาและทดสอบก่อนใช้ ไม่ได้รันได้เพียงเพราะมีพิมพ์ในแผน

## 4. Numerical registration: ต้องมีตัวเลขก่อน admitted runs

แต่ละแผนระบุค่าตามโดเมนที่ต้องล็อก execution registration ต้องเติมค่าจริง หน่วย ที่มา และเหตุผลของทุกช่องที่เกี่ยวข้อง

| หมวด | เนื้อหาที่ต้องมี |
|---|---|
| Task และ inputs | ตัวตน geometry/material/controller/environment; ประวัติ load, motion, heat และ boundary; initial state |
| Representation | spatial domain, minimum feature, approximation tolerance, เพดาน topology/complexity และนโยบายขยาย |
| Numerics | เพดาน mesh/DOF/iteration/time; structural refinement อย่างน้อย 3 ระดับ; นิยาม convergence/error/residual |
| Materials และ physics | constitutive validity range, ที่มา measured เทียบ synthetic, property uncertainty, โดเมนที่ละไว้ |
| Experiment | IV, DV, controls, outcome estimand, sample/seed design, ทิศทาง effect, meaningful effect และวิธีสถิติ |
| Holdout | ตัวตน data/condition ที่ยังไม่ใช้ นโยบายเข้าถึงและตรวจ leakage; ข้อมูลที่เห็นแล้วไม่ใช่ holdout ใหม่ |
| Resources | จองก่อนเรียกงาน งบทุกส่วน failures/retries/tuning/audits; hardware/concurrency และ peaks ที่วัด |
| Decision | แยก geometry invalid, physics violated, numerical unresolved และ not evaluated; promotion rules ตามคำอ้าง |
| Safety สำหรับงานจริง | อนุญาตชัด qualified review, bounds ที่อนุมัติ stop/recovery และ measurement plan |

ห้ามปล่อยช่องที่มีผลต่อการตัดสินว่างใน admitted run ใช้ pilots/calibration ที่เปิดเผยกำหนดค่าแล้วล็อกก่อน admitted evaluation ที่แยกกัน แผนนี้จงใจไม่แต่ง tolerances สากล sample counts, safe loads หรือเวลาเสร็จ ถ้า task/evaluator/thresholds เปลี่ยนให้ registration ใหม่ ห้ามลด threshold หลังเห็น failure แล้วเรียกรันเดิมว่าผ่าน

## 5. ชุดหลักฐานและระดับการรับ

runner contract ที่เสนอสร้าง `result.json` ใต้ output directory ที่ประกาศพร้อม artifact manifest ต้องมี status/claim scope, configuration/input identities ที่เปลี่ยนไม่ได้, exact/toleranced replay metadata, execution/cost records, ทุกกรณี pass/fail/unresolved/not-evaluated, numerical uncertainty, negative controls, หลักฐานสนับสนุน หลักฐานขัดแย้ง คำอธิบายทางเลือก หลักฐานที่ขาด และความมั่นใจ

งาน geometry เก็บ source/export geometry จริง material/void regions และ mass-property discrepancies เพิ่ม งาน fields เก็บ meshes จริง region/boundary maps, reactions/fluxes ที่คำนวณคืน, field outputs และ convergence งาน assembly เก็บ physical path closure, parts ภายใน, motion/contact และบัญชี hardware/material ครบ งานจริงเก็บ raw measurements, calibration/approval references และ specimen/configuration identities; runner ใช้วิเคราะห์ offline เท่านั้น

แยก gates ต่อไปนี้

- **Software execution:** ทดสอบ implementation ที่ตั้งใจและพฤติกรรม negative controls
- **Numerical verification:** ตรวจสมการ/การผูก geometry และ discretization ตามขอบเขต
- **Candidate feasibility:** candidate ที่แน่นอนผ่าน physical/model gates จำเป็นใน fidelity ที่ประกาศ
- **Scientific benefit:** effect มีทิศทางและมีประโยชน์ตามโจทย์มากกว่า uncertainty ภายใต้ fair controls และ holdout
- **Physical validation:** การวัดอิสระรองรับเงื่อนไขใช้งานที่ทดสอบอย่างเฉพาะเจาะจง

ผ่านระดับหนึ่งไม่ได้ผ่านระดับถัดไปอัตโนมัติ ฟิสิกส์ไม่รองรับไม่ใช่เป็นไปไม่ได้ทางฟิสิกส์ รูปทรงไม่คุ้นไม่ใช่ข้อบกพร่อง และ graph topology เดิมต้องไม่ตัดผลมีประโยชน์จาก shape

## 6. หมุดหมายและการจัดลำดับ

- **Geometry-to-field:** Works 108–111 เนื้อวัสดุ/ช่องว่างที่สร้างจริงส่งผลต่อ vector fields ที่ตรวจแล้ว
- **Detailed assembly:** Works 112–117 จุดเชื่อมเกิดจริง พฤติกรรมเคลื่อนที่/ความร้อน และวง feedback architecture/part ที่ย้อนที่มาได้
- **Whole digital candidate:** โดเมนที่เกี่ยวข้อง Works 118–123 และ search/comparison/closure Works 124–126 มี hardware ภายในที่จำเป็นชัดเจน
- **Evidence-backed comparison:** Works 127–130 baseline ที่ปรับดี เงื่อนไขแข่งที่ยังไม่ใช้ independent checks และขอบเขต manufacturing/tolerance
- **Measured validation:** Works 131–133 ที่ได้รับอนุญาต ในขอบเขตทดสอบที่ค่อยใหญ่ขึ้น

ลำดับเป็น dependency map ไม่ใช่สัญญาปฏิทิน ทำ cost pilots ก่อนกำหนดขนาดการศึกษา ถ้า package ต้องใช้ solver domain, โปรแกรมเก็บข้อมูล หรือ safety approval ที่แยกกันหลายชุด ให้แบ่งเป็น execution works มีหมายเลขและขอบเขตชัดก่อนพัฒนา โดยเฉพาะ detailed contact, material failure, internal/external flow, energy conversion และทดสอบรถจริงอาจต้องหลายงาน

อย่าเลื่อน exploratory architecture feedback ไปจนพัฒนาเทคโนโลยีครบทุกชนิด และอย่าเลื่อนระดับรถที่ hardware หรือ physics จำเป็นยัง unresolved ไม่มีชื่อชิ้นส่วน จำนวนล้อ symmetry, fastener มาตรฐาน หรือ powertrain บังคับ เว้นแต่โจทย์ที่ล็อกอย่างชัดเจนกำหนด

## 7. เริ่มงานถัดไป

เริ่ม [Work 108](work108-spatial_material.th.md): ตรวจการนับเนื้อวัสดุ/ช่องว่างจริงและ mass properties จาก geometry แล้วเปิดเส้นทาง implicit generator และ meshing/solid-fields จริง ให้ search ปลายทางใช้ geometry ที่มีเหตุทางฟิสิกส์

การจบชุดเอกสารนี้บันทึกใน [ผล Work 107](../../work_logs/2026-09-07_107_detailed-work-package-plans-result.th.md) การจบงานนั้นไม่ได้หมายความว่า Works 108–133 เริ่มแล้วหรือผ่านแล้ว

## 8. ส่วนขยายแก้ไขหลัง Work 133

Work 134 ที่ดำเนินการจริงเพิ่มแผน Work 135 หลังผลการทำงานแสดงว่า Work 126 ปิดงานด้วย registry ที่ใช้กล่อง แทนที่จะส่งมอบ native whole/individual CAD ตามการ์ดเดิม Work 135 เป็นงานแก้ไขไปข้างหน้า: ไม่เขียนประวัติ Work 126 ใหม่และไม่สืบทอด geometry ของ Work 126 เป็น detailed candidate กล่องเหล่านั้นคงใช้เป็น function checklist เท่านั้น
