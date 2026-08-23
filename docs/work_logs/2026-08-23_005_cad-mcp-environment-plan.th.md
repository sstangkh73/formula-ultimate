# แผนงาน 005: สร้างสภาพแวดล้อม CAD และ MCP

วันที่: 2026-08-23
สถานะ: เสร็จสมบูรณ์

> ฉบับภาษาไทยของ `2026-08-23_005_cad-mcp-environment-plan.md`

## วัตถุประสงค์

ตรวจโปรแกรม CAD ที่ดาวน์โหลด/ติดตั้ง สร้างสภาพแวดล้อม MCP local ที่ปลอดภัย
สำหรับงานวิจัย 3D แรกของ Formula Ultimate และเก็บหลักฐานที่ทำซ้ำได้ว่าตัวใด
เชื่อมต่อและทดสอบจริง

## ขอบเขต

- หาและบันทึก version กับ executable/runtime path ของ Autodesk Fusion,
  FreeCAD, CadQuery และ Blender ที่ติดตั้ง/ดาวน์โหลด
- แยก vendor-provided MCP ออกจาก community/project MCP
- Enable และตรวจ official Autodesk Fusion MCP เมื่อ Fusion version ที่ติดตั้งมี
- ติดตั้ง CadQuery และ project-contrib MCP ที่ review แล้วใน environment เฉพาะ
  โปรเจกต์แบบ isolated พร้อม pin source revision เมื่อทำได้
- ตรวจ FreeCAD command-line/Python automation ก่อนเลือกหรือติดตั้ง community
  MCP bridge
- ตรวจ Blender version และ requirement ของ official Blender Lab MCP เชื่อมต่อ
  เฉพาะผ่านเส้นทางที่ review แล้ว
- บันทึก MCP endpoint/configuration โดยไม่เปิดเผย credential หรือข้อมูลผู้ใช้ที่
  ไม่เกี่ยวข้อง
- รัน non-destructive smoke test ด้วย geometry/artifact ชั่วคราว

## สิ่งที่ไม่ทำ

- ไม่ upload design Formula Ultimate ขึ้น cloud
- ไม่ซื้อหรือเปลี่ยน CAD subscription
- ไม่ติดตั้ง community MCP ที่ยังไม่ review จาก moving branch
- ไม่ให้ generated CAD code เข้าถึง filesystem/network แบบไม่จำกัด
- ไม่ออกแบบหรือ optimize research component ตัวแรก
- ไม่เรียก connection proof ว่า engineering validation

## สิ่งส่งมอบที่วางแผนไว้

- `docs/3d/CAD_MCP_ENVIRONMENT.md`
- `docs/3d/CAD_MCP_ENVIRONMENT.th.md`
- Project-local environment/configuration ที่ ignore เมื่อจำเป็น
- Result record Work 005 ภาษาอังกฤษและภาษาไทยแยกไฟล์ พร้อมคำสั่ง exact,
  version, endpoint, tool inventory, test output และข้อจำกัด

## ลำดับการทำงาน

1. อ่านข้อกำหนด repository และ skill การตั้งค่า Windows/Codex ที่เกี่ยวข้อง
2. สำรวจ executable path, installed version, downloaded installer และ MCP config
  ปัจจุบันด้วย read-only check
3. Review ที่มาของ MCP package และ pin revision ก่อนติดตั้ง
4. สร้าง CadQuery MCP environment แล้วรัน import/server/tool smoke test
5. ตรวจ FreeCAD headless automation ด้วย disposable solid และ neutral export
6. Enable และ probe official Fusion MCP กับ document ว่าง/ชั่วคราว
7. ตรวจ Blender version และ official MCP compatibility ทำ disposable connection
  test เฉพาะเมื่อ install ได้ตรงไปตรงมาและผ่าน review
8. บันทึก confirmed, partial, blocked และ unverified แยกกัน
9. รัน repository test, compilation, bilingual coverage และ staged-diff gate
10. Commit/push เฉพาะเอกสาร/configuration/script ของ repository ห้าม commit
   installed environment, credential หรือ CAD cache

## แผน Validation

- บันทึก application/server version แบบ exact
- ตรวจ executable discovery จากคำสั่งใหม่
- MCP ที่เชื่อมแต่ละตัวต้องมี initialization และ discovered tool evidence
- CAD smoke test ทุกตัวใช้ temporary directory และตรวจ artifact type,
  dimension/property และการ cleanup/recover
- ยืนยันว่าไม่มี credential, token หรือ machine-specific secret config เข้า Git
- รัน repository test suite และ GitHub Actions ทั้งหมด

## เกณฑ์สำเร็จ

- อย่างน้อย CadQuery MCP ติดตั้งใน isolated environment และตอบ protocol/tool
  smoke test
- FreeCAD headless automation ต้องมี disposable artifact proof หรือ blocker exact
- ยืนยันสถานะ official Fusion MCP จากโปรแกรมที่ติดตั้ง ไม่ใช่สมมติจากเว็บ
- ยืนยัน Blender official MCP compatibility จาก version ที่ติดตั้ง
- เอกสาร environment แยกสิ่งที่เชื่อมจริงออกจากสิ่งที่แค่ดาวน์โหลด/ติดตั้ง
- ไม่มี sensitive หรือ machine-global configuration ถูก commit

## เกณฑ์ล้มเหลว

- ติดตั้ง community server โดยไม่มี pinned/reviewed source identity
- Generated code เข้าถึงไฟล์หรือ secret ที่ไม่เกี่ยวข้องโดยไม่จำกัด
- รายงาน GUI screenshot หรือโปรแกรมที่ติดตั้งว่าเป็น MCP connection
- Test artifact แก้ CAD project เดิมของผู้ใช้
- รายงานว่า tool validated โดยไม่มี command/tool result ที่ทำซ้ำได้

## ความเสี่ยงและการควบคุม

- Installer กำกวม: ตรวจ filename, signature/publisher และ target path ก่อน execute
- MCP execute code: ใช้ isolated environment, bounded temporary workspace,
  least privilege และ reviewed tool surface
- GUI state: ใช้ disposable document และไม่ save ทับงานเดิม
- Version drift: บันทึก version และ pin community revision
- External account: ไม่ upload, share, publish หรือเปลี่ยน billing/licensing
- Automation ไม่ครบ: บันทึก GUI step ที่ต้องให้ผู้ใช้ทำแทนการข้าม security หรือ
  ลดความเข้ม test เงียบ ๆ
