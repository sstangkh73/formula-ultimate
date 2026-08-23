# แผนงาน 004: วิจัยเครื่องมือ Engineering CAD ที่รองรับ MCP

วันที่: 2026-08-23
สถานะ: เสร็จสมบูรณ์

> ฉบับภาษาไทยของ `2026-08-23_004_mcp-cad-tooling-research-plan.md`

## วัตถุประสงค์

วิจัยซอฟต์แวร์ที่สามารถออกแบบชิ้นส่วนเครื่องกลอย่างละเอียดและควบคุมผ่าน
Model Context Protocol (MCP) แล้วแนะนำ toolchain ที่ใช้ได้จริงสำหรับ pipeline
ชิ้นส่วน 3D ที่ agent ออกแบบใน Formula Ultimate

## ขอบเขต

- ประเมิน engineering CAD, programmatic CAD, mesh/generative modeling และ
  validation tool ที่เกี่ยวข้องเฉพาะเมื่อสนับสนุน pipeline อย่างมีสาระสำคัญ
- แยก native/official MCP support ออกจาก community MCP server และความเป็นไปได้
  ของ custom MCP
- ตรวจ capability ปัจจุบันจากเอกสารทางการของผลิตภัณฑ์และ primary repository
  ของโปรเจกต์ MCP
- เปรียบเทียบ parametric solid/B-rep, constraint, assembly, STEP/STL export,
  scripting/API, headless use, Windows, license, determinism, MCP maturity และ
  ความเหมาะสมทางวิศวกรรม
- แนะนำ stack ระยะใกล้สำหรับ Formula Ultimate โดยไม่เลือกเครื่องมือเพียงเพราะ
  มี MCP demo

## สิ่งที่ไม่ทำ

- ไม่ติดตั้งหรือเชื่อมต่อ CAD/MCP ใน work item นี้
- ไม่ซื้อ license หรือเปลี่ยน external account
- ไม่ถือว่า mesh generation เพียงอย่างเดียวคือ mechanical engineering ที่ผ่าน
  validation
- ไม่อ้างว่า unofficial MCP server ได้รับการสนับสนุนจากผู้ผลิต CAD
- ไม่ออกแบบ component แรกของ Formula Ultimate

## สิ่งส่งมอบที่วางแผนไว้

- `docs/research/MCP_CAD_TOOLING_REPORT.md`
- `docs/research/MCP_CAD_TOOLING_REPORT.th.md`
- Result record Work 004 ภาษาอังกฤษและภาษาไทยแยกไฟล์ พร้อมหลักฐานแหล่งข้อมูล
  และ validation

## เกณฑ์การประเมิน

1. ความลึกของ mechanical design และ geometric representation
2. Parametric constraint, assembly, material และเส้นทาง manufacturability
3. คุณภาพ automation/API และ deterministic artifact generation
4. Export format และ interoperability กับ CFD/FEA/property extraction
5. ที่มา feature coverage การดูแล และ security boundary ของ MCP
6. Headless/batch operation, reproducibility และ compute scaling
7. Cost, license restriction, ความเหมาะกับ OS และ vendor lock-in
8. ความเหมาะสมสำหรับ agent exploration เทียบ authoritative validation

## วิธีวิจัย

1. ค้นเอกสารทางการ CAD สำหรับ geometry และ automation capability ปัจจุบัน
2. ค้น primary MCP repository และเอกสารผู้ผลิตสำหรับ integration ที่มีจริง
3. ตรวจ install/architecture/tool surface ของ candidate ที่แข็งแรงที่สุด
4. จัดประเภท MCP เป็น official, vendor-adjacent, community, custom-only หรือ
   unverified
5. เปรียบเทียบ candidate กับสถาปัตยกรรม 1D-to-3D trusted evaluator ของ
   Formula Ultimate
6. จัดทำคำแนะนำแบบ tier, implementation path, ความเสี่ยง และ proof-of-concept
   plan ขนาดเล็ก

## แผน Validation

- อ้างอิง claim เรื่อง MCP/support ที่เปลี่ยนตามเวลาใกล้ข้อความที่รองรับ
- ใช้ official documentation สำหรับ CAD capability และ primary repository
  สำหรับ community MCP implementation
- บันทึกวันที่วิจัยและแยก inference ออกจาก fact ที่ยืนยัน
- ตรวจว่า URL เปิดได้และรองรับ claim โดยตรง
- รัน Markdown companion, Python, compilation และ staged-diff test ของ repository

## เกณฑ์สำเร็จ

- รายงานระบุ tool path ที่น่าเชื่อถืออย่างน้อยสามแบบพร้อม trade-off
- ไม่ปน official กับ unofficial MCP support
- คำแนะนำครอบคลุม detailed solid design, exploratory geometry, neutral
  interchange และ independent validation
- รายงานให้ลำดับ proof-of-concept สำหรับ Formula Ultimate ที่นำไปทำต่อได้
- รายงานอังกฤษและไทยรักษาผลทางเทคนิคและ citation ให้เทียบเท่ากัน

## ความเสี่ยงและการควบคุม

- MCP ecosystem เปลี่ยนเร็ว: ระบุวันที่เข้าถึง ที่มา และ maintenance caveat
- Demo bias: ให้ความสำคัญกับ geometry kernel, API, export และ validation มากกว่า
  screenshot หรือความนิยม
- Supply-chain risk ของ repository: แนะนำ pin revision, local sandbox,
  least privilege และ source review สำหรับ community MCP server
- Vendor lock-in: ให้ความสำคัญกับ neutral artifact เช่น STEP, B-rep, STL/3MF,
  solver input และ content-addressed metadata
