# ผล Work 147: ขอบเขตสิทธิ์ข้อมูลวัสดุและการเผยแพร่

ฉบับภาษาอังกฤษ: `2026-09-28_147_material-licensing-publication-boundary-result.md`

วันที่: 2026-09-28

Status: Completed

## ผลลัพธ์

Formula Ultimate ใช้ขอบเขตการเผยแพร่ข้อมูลวัสดุแบบอนุรักษนิยมที่ตัดสินจาก
สิทธิ์ของแต่ละแหล่งแล้ว repository ให้ CC BY 4.0 เฉพาะเนื้อหาต้นฉบับที่โครงการ
สร้างและเจ้าของโครงการมีอำนาจให้ licence เท่านั้น โดยไม่ให้สิทธิ์เหนือ material
ของบุคคลที่สาม ฐานข้อมูลจำกัดสิทธิ์ มาตรฐาน handbook, paper, supplier document
หรือ private record

ผลนี้เป็นการลดความเสี่ยงและเพิ่ม engineering control ที่ตรวจสอบย้อนหลังได้
ไม่ใช่การรับประกัน legal clearance โดย licence, contract, permission เฉพาะแหล่ง
และกฎหมายที่ใช้บังคับยังเป็นข้อกำหนดหลัก

## ไฟล์ที่เปลี่ยน

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
- `docs/work_logs/2026-09-28_147_material-licensing-publication-boundary-plan.md`
- `docs/work_logs/2026-09-28_147_material-licensing-publication-boundary-plan.th.md`
- result นี้และฉบับภาษาอังกฤษ

## การตัดสินใจ

- การอนุญาตเผยแพร่ตัดสินจากสิทธิ์ของ source ที่มีหลักฐาน ไม่ใช่เพียงเพราะเรียก
  ค่าหนึ่งว่าเป็นข้อเท็จจริงหรือดูได้บนเว็บไซต์สาธารณะ
- แยก rights class เป็น `project_synthetic`, `public_domain`,
  `open_licensed`, `permission_granted` และ `restricted_private`
- จัด ASM และ MatWeb เป็น `restricted_private` ตามเงื่อนไขทางการที่ตรวจเมื่อ
  2026-09-28
- ตั้งต้นให้ MMPDS, CMH-17/SAE และ supplier datasheet ใช้แบบ private จนกว่า
  จะมีหลักฐานสิทธิ์เผยแพร่ของ edition หรือ document ที่ตรงกัน
- Sourced public material record ต้องมี `publication_rights` ที่เครื่องอ่านได้
  ระบุ status ที่ยอมรับ สิทธิ์ redistribution, evidence URI, evidence SHA-256
  และวันที่ตรวจ รวมทั้งหลักฐานเฉพาะ class ที่ระบบบังคับ
- Synthetic verification fixture เดิมยังเปิดเผยได้เฉพาะเพราะโครงการสร้างเอง
  และยังมี `claim_boundary.design_use_allowed=false`
- `/private/`, ไฟล์ใต้ `/papers/` และ format เอกสารแหล่งข้อมูลวัสดุทั่วไป
  จะ fail publication-boundary check หากเข้าสู่ candidate Git file set
- ยังบังคับ human provenance review เพราะระบบอัตโนมัติพิสูจน์ ownership,
  ตีความ contract ทุกแบบ หรือตรวจ label เท็จโดยเจตนาไม่ได้

## หลักฐานการตรวจสอบ

รันทุกคำสั่งจาก `C:\Formula Ultimate`

1. `python scripts/validation/check_material_publication_boundary.py`
   - Exit status: `0`
   - Output สำคัญ: `material publication boundary: PASS`
2. `python -m unittest tests.test_material_publication_boundary -v`
   - Exit status: `0`
   - Output สำคัญ: `Ran 7 tests`; `OK`
3. `python -m unittest discover -s tests -v`
   - Exit status: `0`
   - Output สำคัญ: `Ran 1042 tests in 400.308s`; `OK (skipped=11)`
   - Successful run นี้รันนอก filesystem sandbox หลังจาก sandbox run แสดง
     temporary-directory permission failure
4. `python -m py_compile scripts/validation/check_material_publication_boundary.py tests/test_material_publication_boundary.py`
   - Exit status: `0`
5. การตรวจ English/Thai companion และ cross-link
   - Exit status: `0`
   - Output สำคัญ: คู่ policy, register, licence, plan และ result ของ Work 147
     อยู่ครบ และมี source-filename reference
6. `git diff --check`
   - Exit status: `0`

การรัน full suite ครั้งแรกใน filesystem sandbox รัน 1,042 tests แต่จบด้วย
`PermissionError` 115 errors และ 11 skips ใน 358.688 วินาที Minimal
temporary-directory probe ทำให้เกิด write denial เดียวกัน จึงเป็นความล้มเหลว
ของ execution environment ไม่ใช่ product-test assertion จากนั้น full suite
เดียวกันผ่านเมื่อรันนอก sandbox ตามหลักฐานด้านบน

การตรวจ final staged scope, `git diff --cached --check`, commit identity และผล
publication-boundary หลัง commit จะบันทึกใน final handoff เพราะหลักฐานเหล่านั้น
เกิดได้หลังเขียน result file นี้เท่านั้น

## ข้อจำกัด

- Policy หรือ scanner ใน repository ไม่สามารถรับประกันว่า publication ในอนาคต
  จะไม่มีความเสี่ยงทางกฎหมาย
- Rights register เป็น engineering decision record ตามวันที่ ไม่ใช่คำปรึกษา
  กฎหมาย เงื่อนไขอาจเปลี่ยนและต้องตรวจซ้ำสำหรับ source หรือ edition ใหม่ทุกครั้ง
- Hash ที่ถูกต้องพิสูจน์ได้ว่าได้ตรวจ evidence ชุดใด แต่ไม่สร้างสิทธิ์หรือพิสูจน์
  ว่าผู้ตรวจตีความ controlling terms ถูกต้อง
- Validator ตรวจ candidate Git file set ปัจจุบันและ structured JSON material
  record แต่พิสูจน์ provenance ของข้อความทั่วไปหรือตรวจ source ที่ถูกระบุชื่อผิด
  โดยเจตนาไม่ได้
- งานนี้ไม่ได้ rewrite หรือ audit historical commits อย่างละเอียดทั้งหมด

## งานติดตาม

- ก่อนรับ sourced material record ให้เก็บ exact licence หรือ written permission
  แบบ private แล้วเพิ่มใน public repository เฉพาะ notice และ evidence metadata
  ที่ได้รับอนุญาต
- ตรวจ source terms และเขตอำนาจศาลอีกครั้งเมื่อ source, edition, licence
  หรือ intended use เปลี่ยน
- ขอ qualified legal review ก่อน public release หากโครงการจะรวมค่าที่ derive จาก
  commercial database, standard, handbook หรือ supplier document
