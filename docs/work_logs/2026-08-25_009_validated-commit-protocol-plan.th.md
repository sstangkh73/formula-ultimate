# แผน Work 009: Protocol การ Commit หลัง Validation

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-25_009_validated-commit-protocol-plan.md`

สถานะ: Completed

## วัตถุประสงค์

ทำให้คำสั่งของผู้ใช้ที่กำหนดให้ commit ทุก work item ที่ทำเสร็จและผ่าน validation
เป็น protocol บังคับของ repository และแก้ปัญหา whitespace ใน Markdown ของ Work
008 ที่พบจากการตรวจ staged diff ครั้งแรก

## ขอบเขต

- เพิ่มหัวข้อ post-validation commit แบบบังคับในคำสั่ง project agent ภาษาอังกฤษ
  และไทย
- บังคับ explicit staging, การตรวจ cached diff, cached whitespace check แบบ
  fail-fast, การสร้าง commit สำเร็จ และการรายงาน commit hash
- ห้ามตีความ validation ที่ล้มเหลวว่าสำเร็จเพียงเพราะคำสั่งถัดไปในการเรียก shell
  เดียวกันสำเร็จ
- รักษาการเปลี่ยนแปลงอื่นของผู้ใช้และห้าม blanket staging
- ลบ trailing spaces ในเอกสาร Work 008 ที่พบ โดยไม่ rewrite commit ก่อนหน้า
- สร้างหลักฐานผล Work 009 สองภาษาและ commit งานที่เสร็จแล้ว

## ไฟล์ที่วางแผน

- `AGENTS.md`
- `AGENTS.th.md`
- ไฟล์ Markdown Work 008 ที่มี trailing whitespace
- plan/result Work 009 ภาษาอังกฤษและไทยชุดนี้

## การตรวจสอบ

```powershell
python -m unittest discover -s tests -v
git diff --check
git diff --cached --check
git status --short
git log -4 --oneline
```

คำสั่งตรวจที่ต้อง gate ขั้นถัดไปจะเรียกแยกกันหรือใช้ control flow แบบ fail-fast
ห้ามต่อด้วย semicolon แบบ unconditional

## เกณฑ์สำเร็จ

- คำสั่งโครงการภาษาอังกฤษและไทยบังคับ commit หลัง validation เหมือนกัน
- Protocol บังคับขอบเขตชัดเจน การส่งต่อ failure และการรายงาน hash
- trailing whitespace ของ Work 008 ถูกลบ
- Test ของ repository และ whitespace check ผ่าน
- Work 009 ถูก commit และรายงาน commit hash

## ความเสี่ยง

- dirty worktree อาจมีการเปลี่ยนแปลงอื่นของผู้ใช้ ต้อง stage แบบ explicit เท่านั้น
- commit hook หรือปัญหา Git identity อาจขวาง commit หลัง validation ต้องรายงานว่า
  งานยังไม่สมบูรณ์แทนการข้ามแบบเงียบ ๆ

## สิ่งที่ไม่ทำโดยชัดเจน

- ไม่ rewrite history หรือ amend commit Work 006–008 ที่เสร็จแล้ว
- ไม่ push ไป remote repository
- ไม่เปลี่ยนพฤติกรรม physics, CAD หรือ experiment
