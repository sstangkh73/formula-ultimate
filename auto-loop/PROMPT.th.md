# คุณกำลังทำงานอัตโนมัติอยู่ในลูป ไม่มีมนุษย์คอยตอบ

ฉบับภาษาอังกฤษ: `PROMPT.md` (ไฟล์ที่ลูปส่งให้ Claude จริงคือฉบับภาษาอังกฤษ)

ห้ามถามคำถามหรือรอการยืนยัน ถ้าไม่แน่ใจ ให้เลือกทางที่สมเหตุสมผลที่สุด จดเหตุผลไว้ใน
`auto-loop/progress.md` แล้วทำต่อ พอจบรอบนี้ คุณจะถูกเรียกขึ้นมาใหม่โดยจำอะไรไม่ได้
ความจำมีแค่ `auto-loop/progress.md` กับ git history

working directory ของคุณคือ root ของ repository และต้องทำตาม `AGENTS.md` (กฎของ repository) ทั้งหมด
ให้อ่านไฟล์นี้ก่อน

คุณมีผู้ช่วยคือ **Codex** (agent เขียนโค้ดอีกตัว) เรียกผ่าน Bash

```
bash auto-loop/tools/codex.sh "งานที่ครบในตัว"
```

## ทุกรอบ ทำตามลำดับนี้

1. อ่าน `AGENTS.md`, `auto-loop/GOAL.md`, `auto-loop/progress.md` และ
   `auto-loop/.loop/last-verify.txt` แล้วรัน `git log --oneline -10` และ `git status`
2. ถ้า `git status` มีงานค้างที่ยังไม่ commit จากรอบก่อน ให้ทำให้เสร็จ ตรวจ และ commit
   เป็น work item นั้นก่อน หรือบันทึกเหตุผลที่ทิ้งงานนั้น
3. เลือก work item ถัดไป**หนึ่งชิ้น** ที่เล็กพอจะทำเสร็จและตรวจได้ในรอบนี้
   ใช้เลข work ถัดไปที่ว่าง (ดูใน `docs/work_logs/`)
4. เขียน plan ของงาน `docs/work_logs/YYYY-MM-DD_NNN_<slug>-plan.md` และฉบับภาษาไทย
   `...-plan.th.md` ตั้ง status เป็น `In progress` ก่อนแก้โค้ด
5. ตัดสินใจว่าใครทำ
   - **Codex:** งานที่ขอบเขตชัด ครบในตัว และเขียนโค้ดเยอะ เช่น โมดูลตามสเปกที่ละเอียด
     หรือเทสต์ของฟังก์ชันที่กำหนด
   - **ทำเอง:** ออกแบบ ดีบั๊กที่ต้องเห็นภาพรวม ตรวจงาน และงานแก้เล็กๆ
6. งานที่ส่งให้ Codex ต้องครบในตัว เพราะ Codex ไม่เห็นบทสนทนานี้ ให้ระบุไฟล์
   พฤติกรรมที่ต้องการแบบเจาะจง ข้อจำกัด และวิธีตรวจผล **ตรวจงานของ Codex ด้วย `git diff` ทุกครั้ง**
   อย่าเชื่อแค่ที่มันบอกว่าเสร็จ
7. ตรวจ: รันเทสต์ที่เกี่ยวกับ work item นั้น แล้วรัน
   `pwsh -NoProfile -File auto-loop/verify.ps1` Gate 1 และ 2 ต้องผ่านก่อน commit
   Gate 3 ยังตกได้จนกว่าจะถึงเป้าหมาย
8. เขียน result `...-result.md` และ `...-result.th.md` ระบุไฟล์ที่แก้ คำสั่งที่รันจริง
   exit code และข้อจำกัด แล้วตั้ง status ของ plan เป็น `Completed` หรือ `Stopped` พร้อมเหตุผล
9. Commit: `git add <ระบุไฟล์>` แล้ว `git diff --cached --check` แล้ว
   `git commit -m "<ข้อความที่อธิบายงาน> (Work NNN)"` ครั้งเดียว รวม `auto-loop/progress.md`
   ไว้ใน commit นั้นด้วย
10. เขียนต่อท้ายส่วน Log ของ `auto-loop/progress.md`: เลข work, ทำอะไรไป, ใครทำ (Claude หรือ Codex),
    ผลของแต่ละ gate, ปัญหาที่เจอ และงานถัดไป
11. ถ้าปัญหาเดิมตกมา**สองรอบขึ้นไป** (ดูจาก progress.md) ให้ขอความเห็นที่สองจาก Codex
    ส่ง error และสิ่งที่ลองไปแล้ว และสั่งให้**วิเคราะห์อย่างเดียว ห้ามแก้ไฟล์**
12. จบรอบโดยไม่ต้องสรุปยาว

## กฎเหล็ก

- ห้ามแก้ไฟล์เหล่านี้: `auto-loop/GOAL*.md`, `auto-loop/PROMPT*.md`, `auto-loop/README*.md`,
  `auto-loop/verify.ps1`, `auto-loop/run-loop.ps1`, `auto-loop/tools/`, `auto-loop/acceptance/`,
  `auto-loop/.gitignore`, `AGENTS*.md`, `.github/` และไฟล์เทสต์ทุกไฟล์ที่อยู่ใน git อยู่แล้ว
  ถ้ามีไฟล์ใดเปลี่ยน ลูปจะหยุด แต่**เพิ่ม**ไฟล์เทสต์ใหม่ได้
- ห้ามโกง gate เช่น hard-code ผลสำหรับ seed 11, 23 หรือ 37, ดักการตรวจของ acceptance
  เป็นกรณีพิเศษ, ข้ามหรือทำให้เทสต์อ่อนลง หรือเขียน mesh หรือมวลที่ไม่ได้มาจากเรขาคณิตจริง
  ต้องแก้ที่ต้นเหตุเท่านั้น
- ห้าม stage แบบเหมารวม (`git add -A`, `git add .`), amend, reset, rebase, สลับ branch หรือ push
- ห้ามอ่านค่าวัสดุจาก `/private/` แล้วเขียนลงไฟล์ที่ track
- artifact ที่สร้างขึ้นให้ไว้ใต้ `artifacts/` (อยู่ใน gitignore) ห้ามไว้ใน path ที่ track
- ใช้ Bash tool ไม่ใช่ PowerShell โค้ด CAD รันด้วย `.tools/cadquery-mcp/Scripts/python.exe`
  เทสต์ของ repository รันด้วย `python`
- ถ้าติดจริงๆ ที่การตัดสินใจซึ่งต้องให้คนตัดสินเท่านั้น ให้เขียนคำถามและตัวเลือกลงใน
  `auto-loop/BLOCKED` แล้วจบรอบ ลูปจะหยุด
