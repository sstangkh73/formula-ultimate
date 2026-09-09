# ตัวสร้างเนื้อวัสดุรูปทรงอิสระ V1

ต้นฉบับภาษาอังกฤษ: `FREEFORM_MATERIAL_GENERATOR_V1.md`

Status: พัฒนาโดย Work 109 สำหรับ Cartesian field แบบมีขอบเขต

## ขอบเขตคำกล่าวอ้าง

Contract นี้อนุญาตให้ occupancy และ topology ของ material/void เปลี่ยนโดยไม่เลือกชื่อชิ้นส่วนหรือ target silhouette การผ่านยืนยัน geometry coverage แบบ deterministic ภายในขอบเขต grid, operator และงบที่ลงทะเบียน ไม่ยืนยัน functional benefit, smooth-CAD equivalence, physical feasibility, manufacturing หรือ physical validation

## Representation และ dependency

ข้อมูลต้นทางคือ Cartesian cell field finite หน่วยเมตร occupied cell แต่ละช่องมี material label แบบ scalar เพียงหนึ่งค่า; การไม่มี cell คือ void ล็อก domain, resolution, minimum feature, คำศัพท์วัสดุ, maximum occupied cells, maximum changed cells per edit และ maximum surface triangles Work 109 ตรึง commit Work 108 และ SHA-256 ของ spatial contract ภาษาอังกฤษ หลักฐาน dependency เก่าล้มเหลวแบบปิด

domain ที่ admitted คือ `[-0.12, 0.12] m` ในแต่ละแกน resolution หลักคือ `0.01 m`; หลักฐาน refinement ใช้ `0.02`, `0.01` และ `0.008 m` ระดับเหล่านี้วัด representation sensitivity ไม่ใช่ physical convergence

## Causal operators และการทำบัญชี

Operators ที่ลงทะเบียนคือ `boundary_displacement`, `cavity_route`, `branch`, `split`, `merge` และ `material_redistribution` แต่ละ slot มี seed และ parameters คงที่ mutation บันทึก geometry identities ก่อน/หลังและค่าใช้จ่าย changed-cell No-op edit, วัสดุไม่ถูกต้อง, geometry non-finite, path ยาวศูนย์ และเกินงบล้มเหลวแบบมองเห็นได้

Geometry identity hash พิกัด cell ที่เรียงแล้วพร้อม material labels โดยไม่รวมชื่อ case การเปลี่ยนชื่อโดย occupancy/material ไม่เปลี่ยนจึง promote เป็น novelty ไม่ได้ Source เก็บ asymmetric thin feature ที่ tag ไว้ และ chain admitted บังคับให้คง cell เดิมอย่างน้อย `0.8`

## Surface adapter และ topology

ทุก exterior cell face กลายเป็น OBJ triangles สองหน้าในทิศสอดคล้องกัน ใช้ shared vertices แบบ canonical ทุก edge ต้องมี triangles สองหน้าพอดี edge-only contact ที่ทำให้ boundary เป็น non-manifold ถูกปฏิเสธโดยไม่ heal signed triangle volume ต้องเท่ากับ occupied cell volume ภายใน relative error `1e-10`

Occupied และ enclosed-void components ใช้ six-neighbour flood fill Euler characteristic ของ boundary และจำนวน connected surfaces ให้ค่า genus รวม Controls admitted บังคับ through-hole ให้ genus เปลี่ยน `0 -> 1`, การเติมกลับเป็น `1 -> 0`, split เปลี่ยน occupied components `1 -> 2` และ merge กลับเป็น `2 -> 1`

## หลักฐานและการส่งต่อ

`result.json` เก็บ protocol/dependency identities ที่ลงทะเบียน, snapshots ทั้งหมด, operator ancestry, จำนวน cell/triangle, surface residuals, refinement trials, adapters ที่ไม่รองรับ, negative controls, resource counts และ scientific review การรันสะอาดรอบสองต้องสร้าง `result_sha256` เดิมแบบ exact

Work 110 แปลงได้เฉพาะ field/surface artifacts ที่ admitted และต้องรักษา material/void identityพร้อมวัด mesh approximation Smooth B-rep conversion, mixed-cell homogenization, fields ต่ำกว่าสเกล cell และคำกล่าวอ้างทางกายภาพทั้งหมดยังไม่รองรับใน V1
