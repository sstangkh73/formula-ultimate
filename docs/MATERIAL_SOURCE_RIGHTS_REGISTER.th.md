# ทะเบียนสิทธิ์ของแหล่งข้อมูลวัสดุ

ฉบับภาษาอังกฤษ: `MATERIAL_SOURCE_RIGHTS_REGISTER.md`

ตรวจเมื่อ: 2026-09-28

Status: บันทึก admission ของ repository แบบอนุรักษนิยม; ไม่ใช่คำปรึกษากฎหมายหรือ permission จากเจ้าของแหล่ง

## วัตถุประสงค์

ทะเบียนนี้บันทึกเงื่อนไขสาธารณะทางการที่พบสำหรับ source family ซึ่งมีชื่อใน
นโยบายข้อมูลวัสดุของ Formula Ultimate โดยตัดสินเฉพาะว่า source เข้า public
repository ได้หรือไม่ ไม่ได้ตัดสินว่าข้อเท็จจริงรายตัวมีลิขสิทธิ์หรือไม่
มีข้อยกเว้นใช้ได้หรือไม่ หรือการใช้แบบ private ชอบด้วยกฎหมายหรือไม่

`restricted_private` เป็นค่าเริ่มต้นเมื่อไม่มีหรือกำกวมเรื่องอำนาจเผยแพร่ซ้ำที่ตรง
เงื่อนไขแหล่งอาจเปลี่ยน จึงต้องตรวจ controlling terms ซ้ำก่อนรับ record ใหม่

## ทะเบียน

| Source family | หลักฐานทางการที่ตรวจ | ชั้นใน public repository | ข้อตัดสินใจของ repository |
|---|---|---|---|
| เว็บไซต์และ digital resource ของ ASM International | [Website Terms of Use](https://www.asminternational.org/about-asm/legal-policies/terms-of-use-website/); [Digital Resources License Agreement](https://www.asminternational.org/about-asm/legal-policies/asm-digital-resources-license-agreement/); [ขั้นตอนขอ permission](https://www.asminternational.org/about-asm/contact/permission/) | `restricted_private` | ห้าม commit ASM content, export, extract, transformed record หรือ derived material เว้นแต่ได้และบันทึก written permission ที่ตรงและครอบคลุมการใช้ใน repository นี้ |
| ฐานข้อมูล MatWeb | [MatWeb License Agreement](https://www.matweb.com/reference/terms.aspx) | `restricted_private` | ห้าม commit MatWeb record หรือใช้ใน AI/ML workflow เงื่อนไขสาธารณะห้าม redistribution/public database release และกำหนดข้อจำกัด AI/ML โดยเฉพาะ |
| Handbook MMPDS | [หน้าซื้อทางการ](https://www.mmpds.org/purchase-handbook/); [เว็บไซต์โปรแกรมทางการ](https://www.mmpds.org/) | `restricted_private` ระหว่างรอ exact licence | หน้าสาธารณะยืนยันการแจกจ่าย/ซื้อ handbook แต่ไม่พอพิสูจน์อำนาจเผยแพร่ผ่าน repository ให้เก็บ record ที่ derive จาก MMPDS เป็น private จน exact edition และ controlling licence อนุญาต public redistribution |
| Handbook CMH-17 ที่ SAE International แจกจ่าย | [หน้าซื้อ CMH-17](https://www.cmh17.org/RESOURCES/Purchase-Handbook); [SAE product record](https://saemobilus.sae.org/books/composite-materials-handbook-volume-3-revision-h-r-640) | `restricted_private` ระหว่างรอ exact licence | การซื้อได้และ citation ของผลิตภัณฑ์ไม่ใช่ permission เผยแพร่ ให้เก็บข้อมูล handbook เป็น private จนตรวจ exact volume/edition และ controlling SAE terms หรือ written permission |
| Datasheet ของ supplier หรือผู้ผลิต | ต้องมี exact document และเว็บไซต์ผู้ออก | `restricted_private` โดยค่าเริ่มต้น | ตรวจทีละเอกสาร PDF ที่ดูได้สาธารณะหรือ factual value เพียงอย่างเดียวไม่ใช่หลักฐานว่า repository แจกจ่ายข้อความ ตาราง ภาพ การรวบรวม หรือเนื้อหาที่สัญญาจำกัดได้ |
| Government/open data หรือแหล่ง open-licensed | ต้องมี exact official legal source หรือ licence | ไม่รับแบบเหมารวม | เปลี่ยนเป็น `public_domain` หรือ `open_licensed` ได้หลัง record-level review ระบุเขตอำนาจ licence/version หน้าที่ attribution/notice และขอบเขต redistribution |
| Written permission โดยตรง | ต้องมี exact non-secret permission reference และ scope | ไม่รับแบบเหมารวม | เปลี่ยนเป็น `permission_granted` ได้เมื่อ permission ครอบคลุม exact content, public Git redistribution, transformation/derived record ถ้าเกี่ยวข้อง, ระยะเวลา เขตแดน และ intended use |

## ความแตกต่างทางกฎหมายที่นโยบายใช้

- U.S. Copyright Office ระบุว่าข้อเท็จจริงไม่ได้รับความคุ้มครองด้วย copyright
  แต่การเลือกหรือจัดเรียง factual database ที่มี originality อาจได้รับความคุ้มครอง
  ดู [Copyright FAQ](https://www.copyright.gov/help/faq/faq-protect.html) และ
  [Automated Databases](https://www.copyright.gov/register/tx-databases.html)
- Copyright Act ของไทยรับรองการคุ้มครอง compilation หรือ composition ของข้อมูล
  ที่เข้าเงื่อนไข ดู [WIPO Lex record และตัวกฎหมาย](https://www.wipo.int/wipolex/en/legislation/details/3801)
- Contract, confidentiality, database right และ access term อาจมีผลแม้ factual
  value รายตัวไม่มีลิขสิทธิ์
- Creative Commons แนะนำให้ licensor มีสิทธิ์ที่จำเป็นสำหรับ permission ที่ให้
  และทำเครื่องหมาย material ที่ไม่อยู่ใต้ licence ดู
  [CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode)

## ขั้นตอนรับ public source ใหม่

1. ระบุ exact document, database edition, URL, supplier และ access route ที่ใช้
   ห้ามพึ่งชื่อ source family เพียงอย่างเดียว
2. เก็บ controlling terms แบบ private, hash หลักฐานฉบับตรง และบันทึก official
   public evidence URI เมื่อมี
3. ตรวจว่าอนุญาต public redistribution, transformation, derived record และ
   computational/AI use ที่ตั้งใจอย่างชัดเจนหรือไม่
4. บันทึกข้อกำหนด attribution, notice, share-alike, non-commercial,
   no-derivatives, jurisdiction, duration และ revocation ตามที่เกี่ยวข้อง
5. ถ้าสิทธิ์ที่จำเป็นข้อใดไม่แน่นอน ให้จัดชั้น `restricted_private` และหยุด public admission
6. ถ้ารับได้ ให้เพิ่ม block `publication_rights` แบบ machine-readable ตาม
   `MATERIAL_DATA_POLICY.md` รัน validator และรับ human review

## ข้อจำกัดของ audit ปัจจุบัน

- การทบทวนนี้ตรวจเงื่อนไขสาธารณะทางการ ไม่ได้ตรวจเนื้อหาหรือ purchase contract
  ของไฟล์ใต้ `/private/`
- Work 147 ไม่ได้ขอหรือได้รับ permission ใด
- ไม่มี public material record ปัจจุบันที่รับมาจาก ASM, MatWeb, MMPDS,
  CMH-17/SAE หรือ supplier datasheet ที่ไม่ระบุฉบับ
- ทะเบียนนี้เป็นการควบคุม repository และใช้แทนคำแนะนำจากทนายที่รู้ exact source
  contract และเขตอำนาจที่เกี่ยวข้องไม่ได้
