# ผล Work 009: Protocol การ Commit หลัง Validation

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-25_009_validated-commit-protocol-result.md`

สถานะ: Completed

## ผลลัพธ์

คำสั่ง project agent กำหนดแล้วว่า work item ทุกงานที่เสร็จและผ่าน validation
ต้องถูก commit ทันที การเสร็จงานต้องมี commit สำเร็จ explicit staging การตรวจ
staged diff, validation แบบ fail-fast และการรายงาน short hash ที่เกิดขึ้น

งานก่อนหน้าที่เสร็จแต่ยังไม่ commit ถูกแยก commit ตาม work item แล้ว:

- Work 006: `455a9d0` — constrained CAD evidence loop
- Work 007: `a4ef20f` — ทิศทางวิจัยหลัก
- Work 008: `774c66e` — physics profile ของสนามจริง 10 สนาม

## ไฟล์ที่เปลี่ยน

- `AGENTS.md`
- `AGENTS.th.md`
- `docs/physics/CIRCUIT_MODEL.md`
- `docs/physics/CIRCUIT_MODEL.th.md`
- `docs/research/REAL_CIRCUIT_SOURCE_REPORT.md`
- `docs/research/REAL_CIRCUIT_SOURCE_REPORT.th.md`
- `docs/work_logs/2026-08-25_008_real-circuit-physics-result.th.md`
- plan/result Work 009 ภาษาอังกฤษและไทยชุดนี้

## การตัดสินใจ

1. Work item ยังไม่เสร็จจนกว่า commit จะสำเร็จ
2. ต้อง stage ด้วยรายการไฟล์ explicit ห้าม blanket `git add -A` ใน mixed
   worktree
3. Validation gate ต้องเรียกแยกหรือใช้ fail-fast control flow เพื่อไม่ให้
   success ภายหลังกลบ failure ก่อนหน้า
4. ต้องเรียก `git diff --cached --check` ก่อน commit
5. การ amend commit, rewrite history, squash, push และ publish ยังเป็น action
   แยกที่ต้องได้รับคำสั่งชัดเจนจากผู้ใช้
6. รักษา history ของ Work 006–008 แทนการ rewrite

## หลักฐานการแก้ไข

ระหว่าง staged check ของ Work 008 คำสั่ง `git diff --cached --check` รายงาน
trailing whitespace ได้ถูกต้อง แต่ shell invocation ใช้ semicolon แบบ
unconditional จึงยังเรียก `git commit` ภายหลัง Work 009 ลบ spaces เหล่านั้น
บันทึกเหตุการณ์ตรงไปตรงมา และเพิ่มกฎส่งต่อ failure เพื่อป้องกันการเกิดซ้ำ

## การตรวจสอบ

### Test ของ repository

```powershell
python -m unittest discover -s tests -v
```

Exit status: `0`

```text
Ran 42 tests in 0.573s
OK
```

### Working-tree whitespace check

```powershell
git diff --check
```

Exit status: `0` Git แสดงเพียงคำเตือนการแปลง LF เป็น CRLF ไม่มี whitespace error
เหลืออยู่

### Staged validation และ commit

จะเรียก `git diff --cached --check`, ตรวจ staged scope, สร้าง commit และตรวจ
post-commit หลัง stage result record นี้ และรายงาน short hash ของ Work 009 ที่
สำเร็จใน final handoff

## ข้อจำกัด

- Protocol นี้ควบคุม local commit และไม่ได้อนุญาตให้ push ไป remote
- Git hook และ repository configuration ยังขวาง commit ได้ หากเกิดขึ้นต้องคง
  สถานะว่างานไม่เสร็จและรายงาน blocker

## งานต่อไป

ใช้ protocol นี้กับทุก numbered work item ต่อไป และรักษา commit boundary หนึ่ง
รายการที่ตรวจสอบได้ต่อ work item เว้นแต่ plan ระบุเหตุผลชัดเจนว่าต้องใช้โครงสร้าง
อื่น
