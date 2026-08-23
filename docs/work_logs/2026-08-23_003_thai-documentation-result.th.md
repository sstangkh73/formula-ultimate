# ผลงาน 003: เอกสารภาษาไทยแบบแยกไฟล์

วันที่: 2026-08-23
สถานะ: เสร็จสมบูรณ์

> ฉบับภาษาไทยของ `2026-08-23_003_thai-documentation-result.md`

## สรุป

สร้างไฟล์ภาษาไทยแยกต่างหากให้ Markdown ภาษาอังกฤษทุกไฟล์ที่ดูแลใน Formula
Ultimate และกำหนด bilingual Markdown coverage เป็น repository contract แบบ
บังคับและตรวจอัตโนมัติ ทุก work item ต้องมี plan ภาษาอังกฤษและภาษาไทยก่อนเริ่ม
และปิดงานด้วย result record ภาษาอังกฤษและภาษาไทยที่แยกไฟล์

งานนี้ไม่เปลี่ยนพฤติกรรมฟิสิกส์ใน Python

## การเปลี่ยนแปลง

### ไฟล์ภาษาไทยคู่กัน

เพิ่มไฟล์ภาษาไทยคู่กันสำหรับ:

- ภาพรวมโปรเจกต์ ข้อกำหนด agent และคำแนะนำการร่วมพัฒนาระดับ root
- คำแนะนำ configuration
- research charter, design-language boundary, physics-system plan, validation
  strategy และ work protocol
- Plan และ result ของ Work 001 project bootstrap
- Plan และ result ของ Work 002 reference kernel
- Plan และ result ของ Work 003 งานเอกสาร

เมื่อรวม result นี้ ชุดเอกสารที่ดูแลมี Markdown ภาษาอังกฤษ 15 ไฟล์ และไฟล์
ภาษาไทยแยกคู่กัน 15 ไฟล์

### การบังคับใช้ Workflow

- แก้ `AGENTS.md` ให้บังคับ plan/result `.md` และ `.th.md` แยกไฟล์ พร้อมแก้
  companion ใน work item เดียวกัน
- แก้ `CONTRIBUTING.md` และ `docs/WORK_PROTOCOL.md` เพิ่มกฎสองภาษา
- แก้ `README.md` เพิ่มทางเข้าภาษาไทยและ bilingual workflow
- เพิ่ม repository-contract test ซึ่งตรวจ Markdown ภาษาอังกฤษทุกไฟล์ที่ดูแล
  แบบ recursive ว่ามีไฟล์ภาษาไทยที่ไม่ว่างและระบุชื่อ source ภาษาอังกฤษ

## การตัดสินใจเรื่องชื่อ

Repository ใช้มาตรฐานเดียว:

```text
document.md -> document.th.md
```

วิธีนี้แยกแต่ละภาษา คาดเดาชื่อได้ และค้นพบง่าย โดยไม่ปนคำแปลฉบับเต็มเข้าใน
technical source document

## หลักฐาน Validation

### Test suite ทั้งหมด

คำสั่ง:

```powershell
python -m unittest discover -s tests -v
```

Environment: Windows, Python 3.14.3

Exit code: `0`

ผล:

```text
8 longitudinal physics tests ... ok
6 repository contract tests ... ok

Ran 14 tests
OK
```

Contract ใหม่ตรวจว่า:

- Markdown ภาษาอังกฤษทุกไฟล์ที่ดูแลมี `.th.md` อยู่ข้างกัน
- ไฟล์ภาษาไทยทุกไฟล์ไม่ว่าง
- ไฟล์ภาษาไทยทุกไฟล์ระบุ source ภาษาอังกฤษ
- Completed plan ยังคงมี result record คู่กัน

### Coverage Inventory

จำนวน maintained document สุดท้าย:

```text
English Markdown files: 15
Thai companion files:   15
Missing companions:      0
```

### Compilation และ Staged Diff

คำสั่ง:

```powershell
python -m compileall -q src tests
git diff --cached --check
```

Exit code ของแต่ละคำสั่ง: `0`

รันทุกคำสั่งซ้ำหลัง stage result ทั้งสองไฟล์ จากนั้น GitHub Actions รัน test
suite ทั้งหมดอย่างอิสระบน Python 3.11 หลัง push

## ข้ออ้างที่มีหลักฐานรองรับ

- Markdown ภาษาอังกฤษทุกไฟล์ที่ดูแลอยู่ปัจจุบันมีไฟล์ภาษาไทยแยก
- หากไฟล์ภาษาไทยตกหล่นในอนาคต automated repository test จะ fail
- Work plan และ result มีไฟล์แยกในทั้งสองภาษาแล้ว
- ตั้งใจรักษา technical path, command, equation, unit, value, claim และ
  limitation ระหว่างการแปล

## ข้ออ้างที่ยังตรวจอัตโนมัติไม่สมบูรณ์

- File coverage test พิสูจน์ semantic equivalence ที่สมบูรณ์ไม่ได้
- คุณภาพ natural-language translation ยังต้อง review เมื่อ source ภาษาใดภาษา
  หนึ่งเปลี่ยนอย่างมีสาระสำคัญ
- Test ปัจจุบันตรวจ Thai companion ที่ล้าสมัยไม่ได้ หากทั้งสองไฟล์ยังมีอยู่แต่
  แก้เฉพาะเนื้อหาภาษาอังกฤษ

## สิ่งที่เบี่ยงเบนจากแผน

- ไม่มี งานยังอยู่ในขอบเขต documentation และ contract เท่านั้น

## งานถัดไปที่แนะนำ

กลับเข้าสู่ physics roadmap ด้วย plan/result สองภาษาชุดใหม่ งานฟิสิกส์ถัดไป
ควร implement energy/work conservation audit ที่ Work 002 แนะนำ ก่อนเพิ่ม
motor, battery หรือ topology evolution
