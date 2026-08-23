# Work Protocol ที่ตรวจย้อนหลังได้

> ฉบับภาษาไทยของ `WORK_PROTOCOL.md`

## กฎ

ทุก work item แยกมี Markdown record ที่ใช้วันที่ sequence number และ slug
เดียวกันในแต่ละภาษา:

```text
docs/work_logs/YYYY-MM-DD_NNN_<slug>-plan.md
docs/work_logs/YYYY-MM-DD_NNN_<slug>-plan.th.md
docs/work_logs/YYYY-MM-DD_NNN_<slug>-result.md
docs/work_logs/YYYY-MM-DD_NNN_<slug>-result.th.md
```

## กฎ Markdown สองภาษา

Markdown ภาษาอังกฤษทุกไฟล์ที่ดูแลต้องมีไฟล์ภาษาไทยแยกใน directory เดียวกัน:

```text
document.md -> document.th.md
```

สร้างและแก้ทั้งสองไฟล์ใน work item เดียวกัน ไฟล์ภาษาไทยต้องระบุชื่อ source
ภาษาอังกฤษ และรักษา technical identifier สมการ คำสั่ง path หน่วย หลักฐาน
เชิงตัวเลข สถานะ ข้ออ้าง และข้อจำกัดให้ตรงกัน ไฟล์ต้องแยกจากกัน ห้ามต่อ
คำแปลฉบับเต็มไว้ในเอกสารภาษาอังกฤษ

## ก่อนทำงาน: Plan Record

สร้าง plan ทั้งสองภาษาก่อนเปลี่ยนแปลงเฉพาะงาน โดยต้องมี:

- วัตถุประสงค์
- ขอบเขตและ non-goal
- deliverable/ไฟล์ที่วางแผน
- ลำดับการทำงาน
- แผน validation
- success criteria และ failure criteria
- ความเสี่ยงและการควบคุม
- สถานะ (`In progress`)

อนุญาตให้สำรวจ repository เท่าที่จำเป็นเพื่อเขียน plan ให้แม่นยำ แต่ห้ามทำ
implementation หรือ mutation เฉพาะงานก่อนมี plan

## ระหว่างทำงาน

- รักษาขอบเขตให้ตรงกับ plan
- หากพบวัตถุประสงค์ใหม่ที่มีสาระสำคัญ ให้สร้าง plan หมายเลขใหม่แทนการขยาย
  งานปัจจุบันโดยไม่บอก
- เก็บ failure และแนวทางที่ทดลองแล้วปฏิเสธไว้สำหรับ result report
- ห้ามลดความเข้มของ test เพียงเพื่อให้ได้ผลผ่าน

## หลังทำงาน: Result Record

ก่อน final commit ให้สร้าง result record ภาษาอังกฤษและภาษาไทยคู่กัน โดยมี:

- สถานะ (`Completed`, `Partial` หรือ `Stopped`)
- สรุปงานที่เสร็จ
- ไฟล์ที่เปลี่ยน แบ่งกลุ่มตามวัตถุประสงค์
- การตัดสินใจสำคัญและเหตุผล
- คำสั่ง validation exact และ exit code
- test output แบบย่อหรือ artifact reference
- ข้ออ้างที่หลักฐานรองรับและข้ออ้างที่ยังไม่รองรับ
- สิ่งที่เบี่ยงเบนจาก plan
- ข้อจำกัดที่ทราบและงานถัดไปที่แนะนำ

จากนั้นแก้สถานะ plan ให้ตรงกับผลลัพธ์

## รูปแบบหลักฐาน Test

```text
Command: python -m unittest discover -s tests -v
Environment: Python X.Y.Z, operating system
Exit code: 0
Result: N tests passed
Evidence: concise terminal output or versioned artifact path
```

ห้ามเขียนเพียง “tests passed” โดยไม่มีคำสั่งและผล ห้ามคัดลอกผลการรันครั้งก่อน
มาเป็นหลักฐานให้ code ที่เปลี่ยนแล้ว

## ขอบเขต Commit

ตามปกติ plan ทั้งสองภาษา implementation test และ result record ทั้งสองภาษา
อยู่ใน commit เดียวที่ review ได้ Commit hash ไม่สามารถฝังใน commit เดียวกันนั้น
ได้ จึงให้ Git history เป็น authoritative link สำหรับ experiment artifact
result record ทั้งสองภาษายังต้องบันทึก simulator/configuration commit ที่ใช้
สร้าง artifact
