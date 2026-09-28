# แผน Work 147: ขอบเขตสิทธิ์ข้อมูลวัสดุและการเผยแพร่

ฉบับภาษาอังกฤษ: `2026-09-28_147_material-licensing-publication-boundary-plan.md`

วันที่: 2026-09-28

Status: Completed

## วัตถุประสงค์

แทนร่างนโยบายข้อมูลวัสดุที่ยังไม่ commit ด้วยขอบเขตการเผยแพร่แบบอนุรักษนิยม
ซึ่งตัดสินจากสิทธิ์ของแต่ละแหล่ง ลดความเสี่ยงที่ Formula Ultimate จะเผยแพร่
ข้อมูลวัสดุ เอกสาร หรือ record ที่ derive จากบุคคลที่สามภายใต้ CC BY 4.0
โดยไม่มีอำนาจ และเพิ่มการตรวจแบบ fail-closed อัตโนมัติสำหรับ commit ในอนาคต

งานนี้ไม่รับประกันว่าสามารถกำจัดความเสี่ยงทางกฎหมายทั้งหมด โดยจะบันทึกหลักฐาน
ที่ตรวจแล้ว ตั้งต้นให้แหล่งที่สิทธิ์ไม่ชัดอยู่แบบ private และสงวนการตีความกฎหมาย
ขั้นสุดท้ายไว้ให้ผู้เชี่ยวชาญกฎหมายและ licence ของแหล่งที่ใช้บังคับ

## ขอบเขต

- ตรวจร่าง material policy, repository licence, README และ `.gitignore`
  ที่ยังไม่ commit โดยไม่เผยแพร่เนื้อหาจาก private source
- แยก project-authored synthetic fixture, ข้อมูล public-domain/open-licensed,
  ข้อมูลที่ได้รับ permission และแหล่งที่ถูกจำกัดหรือยังตรวจสิทธิ์ไม่ได้
- บันทึก source-rights register แบบสาธารณะสำหรับ ASM, MatWeb, MMPDS,
  CMH-17/SAE และ supplier datasheet จากเงื่อนไขทางการที่เข้าถึงได้ ณ 2026-09-28
- จำกัดการให้สิทธิ์ CC BY 4.0 เฉพาะสิทธิ์ที่เจ้าของโครงการควบคุม และทำเครื่องหมาย
  exclusion ของบุคคลที่สามให้ชัด
- เพิ่ม publication-boundary validator แบบ deterministic พร้อม tests โดย material
  record ที่ตั้งใจใช้เพื่อ design แบบสาธารณะต้องมีหลักฐานสิทธิ์เผยแพร่ที่เครื่องอ่านได้
  ส่วน source ที่ unknown หรือ restricted ต้อง fail closed
- รักษา synthetic verification fixture เดิมและขอบเขต
  `design_use_allowed=false` ที่ประกาศไว้ชัดเจน

## ไฟล์ที่วางแผนแก้

- `.gitignore`
- `LICENSE-DATA.md`
- `LICENSE-DATA.th.md`
- `README.md`
- `README.th.md`
- `docs/MATERIAL_DATA_POLICY.md`
- `docs/MATERIAL_DATA_POLICY.th.md`
- `docs/MATERIAL_SOURCE_RIGHTS_REGISTER.md`
- `docs/MATERIAL_SOURCE_RIGHTS_REGISTER.th.md`
- `scripts/validation/check_material_publication_boundary.py`
- `tests/test_material_publication_boundary.py`
- plan นี้และฉบับภาษาอังกฤษ
- result record ภาษาอังกฤษ/ไทยคู่กันของ Work 147

## การตรวจสอบ

1. รัน publication-boundary validator กับ repository
2. รัน focused unit tests สำหรับ synthetic/open record ที่อนุญาต และกรณี
   restricted, unknown, malformed และ `/private/` ที่ต้องถูกปฏิเสธ
3. รัน unittest suite ทั้งหมด
4. compile ไฟล์ Python ใหม่
5. ตรวจว่าคู่เอกสารอังกฤษ/ไทยและ policy link ครบ
6. stage เฉพาะไฟล์ Work 147 ที่ประกาศ ตรวจรายชื่อ staged file รัน
   `git diff --cached --check` ทำ commit เดียว ตรวจ commit hash และรัน
   publication-boundary validator ซ้ำหลัง commit

## เกณฑ์สำเร็จ

- ไม่มีข้อความนโยบายอ้างว่าข้อเท็จจริงค่าคุณสมบัติวัสดุทั้งหมดมีลิขสิทธิ์
  หรือแหล่งทุกชื่อมีเงื่อนไขเหมือนกัน
- ให้ CC BY 4.0 เฉพาะ material ที่เจ้าของโครงการมีอำนาจให้ licence และแยก
  third-party/separately licensed material ออกอย่างชัดเจน
- ถือ ASM และ MatWeb เป็น restricted ส่วน MMPDS, CMH-17/SAE และ supplier
  datasheet อยู่ private จนกว่าจะบันทึกหลักฐานสิทธิ์เผยแพร่เฉพาะแหล่ง
- material record แบบ sourced ที่ commit สาธารณะจะเป็น design-eligible ไม่ได้
  หากไม่มี publication-rights classification และหลักฐานที่ผ่านเกณฑ์
- synthetic fixture เดิมยัง replay ได้และห้ามใช้รองรับ physical-design claim ชัดเจน
- validation และ commit gate ที่ประกาศทั้งหมดผ่าน

## ความเสี่ยง

- Copyright, contract, database right และเขตอำนาจศาลเป็นคนละเรื่อง
  automation ใน repository ใช้แทนคำปรึกษากฎหมายไม่ได้
- เงื่อนไขของแหล่งอาจเปลี่ยน จึงต้องลงวันที่ register และตรวจซ้ำก่อนเผยแพร่
  sourced data ใหม่
- Content scanner พิสูจน์ที่มาหรือตรวจการติดป้ายเท็จโดยเจตนาไม่ได้
  จึงยังบังคับ human provenance review
- ประวัติ repository อาจมีข้อมูลที่ค้นไม่พบจากชื่อไฟล์หรือชื่อแหล่ง

## สิ่งที่ไม่ทำอย่างชัดเจน

- ไม่เผยแพร่ quote สรุป แจกแจง หรือแก้ไฟล์ใต้ `/private/`
- ไม่ตัดสิน ownership ของค่าจากบุคคลที่สามรายค่าโดยไม่มี exact source record
  และ controlling terms
- ไม่ขอ permission ไม่ซื้อ licence และไม่ให้คำปรึกษากฎหมาย
- ไม่เปลี่ยน physical model, material value, candidate geometry, search
  หรือ experiment result
- ไม่ push, publish, rewrite history หรือ amend commit เดิม
