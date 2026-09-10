# กราฟ Physical Interface V1

ต้นฉบับภาษาอังกฤษ: `PHYSICAL_INTERFACE_GRAPH_V1.md`

Status: พัฒนาโดย Work 112 สำหรับ semantic corpus แบบมีขอบเขต

## ขอบเขตและ dependency

Contract นี้ผูก typed physical terminals กับ material/void regions ที่ตรงกันของ Work 108 พร้อมรักษา owner grouping, frames, surface names, roles, domains, variables, หน่วย SI, allowed motion, direction, constitutive-law references และ parallel-edge multiplicity ตรึง Work 108 commit `9e5249d343389a702d229a2cc090c71a12f13a4b` และ SHA-256 ของ spatial contract ภาษาอังกฤษ

Corpus ครอบคลุม mechanical force (`N`), heat flow (`W`) และ angular velocity (`rad_s`) Binding เป็น semantic evidence ที่ประกาศ ไม่ใช่ CAD contact ที่วัดจริง Descriptor นี้ไม่ใช่หลักฐานเพียงอย่างเดียวของ mechanism, contact response, solver field, vehicle feasibility หรือ physical validity

## Compatibility และ conservation

แต่ละ terminal มี origin/normal/reference frame แบบ orthonormal หน่วยเมตรและ named mating surface ที่ไม่ว่าง Terminal ที่เชื่อมกันต้องมี domain, variable และ unit เดียวกัน; origins ต่างกันได้ไม่เกิน `1e-6 m` และ normal dot product ต้องไม่เกิน `-0.999` Directed edges ต้องตรงกับ source/sink roles Rigid/moving conflicts ล้มเหลวเว้นแต่ free terminal อนุญาตความสัมพันธ์ชัดเจน Exchange pair ของแต่ละ edge ต้องรวมกันภายใน `1e-12` ในหน่วยที่ลงทะเบียน

Graph รักษา typed multiedges และประเมิน connectivity โดยไม่เชื่อม disconnected components กรณี regions/surfaces หาย, units/domains ไม่เข้ากัน, role-direction conflicts, frames ผิด, laws/motion ไม่รองรับ และ conservation ล้มเหลวถูกปฏิเสธแบบสังเกตได้

## Identity และ geometry revision

Exact canonical identity ไล่ terminal permutations ไม่เกินแปด terminals ลบชื่อ terminal, edge และ owner แต่รักษา owner partition รวมถึงทุก physical attribute และ edge Graph เกินขอบเขตรายงาน `unresolved`; ไม่ fallback เป็น identity จาก identifier Identifier-only rename ต้องรักษา identity ส่วน source/sink reversal, การลบ parallel edge และ owner regrouping ต้องแยกออก

Split/merge transfer ต้องมี target เพียงหนึ่งรายการที่อ้าง original surface Target เดียวแก้ binding และ invalidate dependent evidence เพื่อคำนวณใหม่ หากไม่พบหรือพบหลายรายการให้รักษา binding เดิมและส่ง ambiguity invalidation event Exact replay ต้องได้ result SHA-256 เดิม
