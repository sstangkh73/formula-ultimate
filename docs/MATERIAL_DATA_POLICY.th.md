# นโยบายสิทธิ์ข้อมูลวัสดุและการเผยแพร่

ฉบับภาษาอังกฤษ: `MATERIAL_DATA_POLICY.md`

วันที่นโยบาย: 2026-09-28

Status: นโยบาย repository ที่ใช้งานอยู่; ไม่ใช่คำปรึกษากฎหมาย

## ข้อตัดสินใจ

Formula Ultimate จะเผยแพร่ material record เฉพาะเมื่อโครงการบันทึกอำนาจ
ในการเผยแพร่ record นั้นซ้ำจากแหล่งที่เจาะจงแล้ว การที่ตัวเลขเป็น “ค่าจริง”
ไม่ใช่เกณฑ์ทางกฎหมาย Copyright ของข้อความหรือการรวบรวม เงื่อนไขสัญญาการเข้าถึง
database right การรักษาความลับ และกฎหมายของเขตอำนาจที่เกี่ยวข้องอาจสร้างหน้าที่
ที่แตกต่างกัน

ข้อมูลวัสดุที่สิทธิ์ไม่แน่นอน ถูกจำกัด ซื้อมา ต้องใช้บัญชี เป็นความลับ
หรือกำลังรอ permission ต้องอยู่ใต้ขอบเขต `/private/` ที่ git ignore
ความไม่แน่นอนต้อง fail closed: การไม่พบข้อห้ามไม่ใช่หลักฐานว่าได้รับอนุญาต

การทบทวนแหล่งแบบลงวันที่อยู่ใน
[`MATERIAL_SOURCE_RIGHTS_REGISTER.th.md`](MATERIAL_SOURCE_RIGHTS_REGISTER.th.md)

## ชั้นสิทธิ์เผยแพร่

| ชั้น | การปฏิบัติใน public repository |
|---|---|
| `project_synthetic` | อนุญาตเฉพาะเมื่อสร้างเพื่อโครงการนี้ ติดป้าย synthetic และห้ามใช้รองรับ design หรือ physical-validation claim |
| `public_domain` | อนุญาตเฉพาะเมื่อมีหลักฐานระบุฐาน public domain และเขตอำนาจ |
| `open_licensed` | อนุญาตเฉพาะภายในเงื่อนไข licence ที่ตรง โดยรักษา source, licence, attribution, modification และ notice requirement |
| `permission_granted` | อนุญาตเฉพาะภายใน permission ที่เป็นลายลักษณ์อักษรและครอบคลุมการเผยแพร่ผ่าน repository กับ record ที่ตั้งใจใช้ |
| `restricted_private` | ห้าม commit และเป็นค่าเริ่มต้นของแหล่งที่ unknown, unverified, ซื้อมา, ต้องใช้บัญชี หรือยังไม่ได้ตรวจเงื่อนไขเฉพาะแหล่ง |

Identifier, citation หรือ public URL เพียงอย่างเดียวไม่ได้สร้างสิทธิ์คัดลอกหรือเผยแพร่
เนื้อหาต้นทางซ้ำ

## Material record แบบ public

Public record ที่มี `evidence_status: "sourced"` ต้องมี object
`publication_rights` ซึ่งประกอบด้วย:

- `status`: `public_domain`, `open_licensed` หรือ `permission_granted`;
- `redistribution_allowed: true`;
- `evidence_uri`: official licence, permission หรือ legal source ที่ใช้บังคับ;
- `evidence_sha256`: SHA-256 ของหลักฐานสิทธิ์ฉบับตรงที่ตรวจ;
- `verified_on`: วันที่ ISO `YYYY-MM-DD`;
- `license_id` และ attribution/notice ที่บังคับเมื่อใช้ open licence หรือ
  permission reference ที่ไม่เป็นความลับและ scope เมื่อใช้ written permission

Record ต้องรักษา material source identity, condition, unit, uncertainty และ
property-to-source mapping ที่ engineering contract บังคับด้วย สิทธิ์เผยแพร่
ไม่ได้ทำให้ property เหมาะทางเทคนิค และหลักฐานทางเทคนิคไม่ได้สร้างสิทธิ์เผยแพร่

## สิ่งที่ต้องอยู่ private

- Source PDF, handbook extract, screenshot, table, graph, database export,
  scraped record, account-gated content และ purchased electronic content
- ค่าหรือชุดรวบรวมที่ได้ภายใต้เงื่อนไขห้ามเผยแพร่สาธารณะ หรือยังไม่ได้ตรวจ
  สถานะการเผยแพร่ซ้ำ
- จดหมาย permission ที่มีข้อมูลลับหรือข้อมูลส่วนบุคคล
- ตาราง derive, fitted model หรือ report เมื่อ controlling terms จำกัด derivative
  หรือ output ทำซ้ำหรือทำให้กู้คืน restricted source content ได้
- Record ทุกตัวที่จัดชั้น `restricted_private`

Private record ใช้ได้เฉพาะภายใน controlling terms การไม่ใส่ไฟล์ใน Git
ไม่ได้ให้สิทธิ์ใช้งานไฟล์นั้นโดยตัวมันเอง

## สิ่งที่อยู่ public ได้

- Project-authored synthetic verification fixture ที่มี
  `design_use_allowed=false`
- Analytic reference case ที่โครงการเขียนเพื่อตรวจสมการ เมื่อไม่ได้คัดลอก
  การนำเสนอที่มีลิขสิทธิ์หรือ restricted dataset
- Source identifier, official link, bibliographic citation, rights class และ
  cryptographic hash ที่ไม่เปิด restricted content
- Code, schema, validator และ solver logic ที่โครงการสร้างและไม่ฝัง
  restricted source value
- Record แบบ public-domain, open-licensed หรือ permission-granted ที่หลักฐานสิทธิ์
  แบบ machine-readable ผ่านนโยบายนี้
- Public outcome ที่ย้อนกลับไม่ได้ เฉพาะหลังตรวจว่าเงื่อนไขเฉพาะแหล่งอนุญาต
  การไม่มี input value ในป้าย pass/fail ไม่ได้ทำให้ปลอดภัยโดยอัตโนมัติ

Fixture ตัวเลขแบบ aluminium-like และแบบอื่นที่มีอยู่ถูกประกาศเป็น
project-authored synthetic verification input ค่าที่ดูคุ้นเคยไม่ใช่ sourced design
allowable และใช้รองรับ material selection, structural safety, fatigue life,
manufacturing หรือ physical-validation claim ไม่ได้

## ขอบเขต private และการควบคุมการเผยแพร่

1. Restricted record และ source document ต้องอยู่ใต้ `/private/`; ห้ามใช้
   `git add -f` กับ path นี้
2. Code ที่อ่าน private record ต้อง fail closed เมื่อ record หรือ rights evidence
   หาย และห้ามแทนด้วย synthetic หรือ built-in value แบบเงียบ
3. Public result ที่ขึ้นกับ private data ต้องเปิดเผย dependency และห้ามเปิด
   restricted value หรือ derivative ที่ย้อนกลับได้
4. Public reference ไปยัง private record ใช้ stable non-secret ID และ hash
   Hash ที่บันทึกพิสูจน์ได้เพียง identity สำหรับผู้ที่ครอบครอง source bytes เดียวกัน
   อย่างชอบด้วยสิทธิ์ บุคคลทั่วไปตรวจเนื้อหา private ที่มองไม่เห็นไม่ได้
5. รัน `python scripts/validation/check_material_publication_boundary.py`
   ก่อน stage การเปลี่ยน material policy หรือ material record และ full test suite
   ต้องรัน boundary check นี้ด้วย
6. ยังคงบังคับ human review เพราะ validator พิสูจน์ที่มา ตีความ licence ทุกฉบับ
   หรือตรวจ record ที่ติดป้ายเท็จไม่ได้
7. ตรวจ controlling terms ซ้ำก่อนรับ source family ใหม่ทุกครั้ง และอัปเดต
   rights register ที่ลงวันที่ใน bilingual work item แยก

## ความสัมพันธ์กับ CC BY 4.0

[`LICENSE-DATA.th.md`](../LICENSE-DATA.th.md) ให้ licence เฉพาะ original material
ที่เจ้าของโครงการมีอำนาจให้ CC BY 4.0 ไม่ relicense third-party content,
restricted private data หรือ separately licensed material เมื่อไฟล์มี material
ภายใต้ licence แยก ให้ file-specific notice และ source terms ควบคุม material นั้น

## ผลต่อวิศวกรรมและการทำซ้ำ

- Private sourced record รองรับได้เฉพาะ claim ที่ technical evidence และ
  controlling terms อนุญาต และไม่ได้กลายเป็น public เพราะบันทึก hash
- Public replay ของผลที่ใช้ private data ทำไม่ได้ เว้นแต่มี dataset อิสระที่แจกจ่ายได้
  ให้รายงานเป็นข้อจำกัดด้าน reproducibility ไม่ใช่ public verification
- Source ชั้น `restricted_private` ห้ามใช้ train, fine-tune, evaluate, index, embed
  หรือป้อน AI/ML workflow เว้นแต่ controlling terms ที่ตรงอนุญาตชัดเจน
- หาก rights evidence กำกวม ให้หยุดเผยแพร่และขอ permission จากเจ้าของแหล่ง
  หรือรับการตรวจจากผู้เชี่ยวชาญกฎหมาย
