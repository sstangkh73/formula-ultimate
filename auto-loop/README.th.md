# Claude + Codex Auto Loop

ฉบับภาษาอังกฤษ: `README.md`

ลูปที่ทำงานเองโดยไม่มีคนเฝ้า แต่ละรอบ Claude ทำ work item ที่มีเลขกำกับหนึ่งชิ้น ส่งงานเขียนโค้ดที่ขอบเขตชัดให้ Codex
และทำต่อไปเรื่อยๆ จนกว่า `verify.ps1` จะผ่านบน tree ที่สะอาดและ commit แล้ว Work 148 ปรับให้ใช้กับ repository นี้

```
run-loop.ps1 ──► claude -p (อ่าน PROMPT.md) ที่ root ของ repository
     ▲               ├─ วางแผน / ดีบั๊ก / ตรวจงาน / commit   ← Claude
     │               └─ bash auto-loop/tools/codex.sh        ← Codex (ไม่ stage ไม่ commit)
     │
     ├─ ตัวกัน: ไฟล์ที่ป้องกันไม่ถูกแก้, branch เดิม, ไม่เขียนประวัติใหม่, main ไม่ขยับ
     └─ verify.ps1 ── Gate 1 ขอบเขตข้อมูลวัสดุ
                      Gate 2 เทสต์ทั้ง repository
                      Gate 3 acceptance (เป้าหมาย)  ── ผ่าน + tree สะอาด → หยุด
```

## ไฟล์

| ไฟล์ | หน้าที่ | ใครแก้ |
|---|---|---|
| `GOAL.md` | เป้าหมายและสัญญาการยอมรับ | คน |
| `acceptance/` | เป้าหมายในรูปเทสต์ที่รันได้ | คน |
| `verify.ps1` | ตัวตัดสิน: exit 0 = เสร็จ | คน |
| `PROMPT.md` | คำสั่งที่ Claude ได้รับทุกรอบ | คน |
| `run-loop.ps1`, `tools/codex.sh` | runner และสะพานไป Codex | คน |
| `progress.md` | ความจำระหว่างรอบ (commit ด้วย) | agent |
| `.loop/` | log แต่ละรอบ, log ของ Codex, ผล verify ล่าสุด, ประวัติ | runner (อยู่ใน gitignore) |

ไฟล์ที่คนแก้ทั้งหมดถูกป้องกันไว้ runner hash ไฟล์เหล่านี้รวมกับเทสต์ทุกไฟล์ที่อยู่ใน git
และหยุดทันทีถ้ามีไฟล์ใดเปลี่ยน

## ต่างจาก template เดิมอย่างไร

- รันจาก root ของ repository และไม่ `git init` เด็ดขาด
- ไม่ยอมรันบน `main` จะสร้างหรือสลับไป `loop/functional-composition-v2`
  (เปลี่ยนชื่อได้ด้วย `-Branch` ส่วนเป้าหมาย v1 รันบน `loop/hierarchical-composition`) และหยุดถ้า `main` ขยับ
- ไม่ stage และไม่ commit เอง แต่ละรอบทำตาม `AGENTS.md` คือมีบันทึก plan/result สองภาษา
  `git add <files>` แบบระบุไฟล์ และ commit หลัง Gate 1 และ 2 ผ่านเท่านั้น
- agent ที่รันแบบ headless ถูกห้าม stage แบบเหมารวม, amend, reset, rebase, สลับ branch, push และใช้ web tool
- agent เขียนไฟล์ `auto-loop/BLOCKED` เพื่อหยุดลูปแล้วถามคนได้

## ติดตั้ง (ครั้งเดียว)

```
npm install -g @anthropic-ai/claude-code @openai/codex
claude        # ล็อกอิน แล้วพิมพ์ /exit
codex login
```

ต้องมี CadQuery runtime ที่ pin ไว้อยู่ที่ `.tools/cadquery-mcp/`
(ดู `scripts/bootstrap_cadquery_mcp.ps1`)

## รัน

```
pwsh -File auto-loop/run-loop.ps1 -PreflightOnly          # ตรวจอย่างเดียว ไม่เริ่ม agent ไม่สลับ branch
pwsh -File auto-loop/run-loop.ps1 -MaxIterations 20 -MaxHours 8
```

- **หยุด:** สร้างไฟล์ `auto-loop/STOP` หรือกด Ctrl+C
- **ดูความคืบหน้า:** `auto-loop/progress.md`, `git log --oneline`, `auto-loop/.loop/iter-*.log`,
  `auto-loop/.loop/history.txt`
- **ตรวจงาน:** ทุกรอบเป็น commit ปกติบน branch ของลูป ให้ตรวจก่อน merge อะไรเข้า `main`
- **ย้อนกลับ:** branch ของลูปทิ้งได้ จะลบหรือ reset ก็ได้ `main` ไม่ถูกแตะ

## ค่าใช้จ่ายและความปลอดภัย

- ทุกรอบใช้งบทั้งฝั่ง Claude และ OpenAI จำกัดด้วย `-MaxIterations`, `-MaxHours`
  และ `-MaxTurnsPerIteration`
- Gate 2 รันเทสต์ทั้ง repository ซึ่งใช้เวลาประมาณ 6 นาที และ Gate 3 รัน generator 4 ครั้ง
  verify แต่ละครั้งจึงอาจใช้เวลานาน
- Codex รันด้วย `--sandbox workspace-write` ที่ root ของ repository
- การผ่าน Gate 3 คือผลด้าน representation ของเรขาคณิตและการประกอบ ไม่ใช่การยืนยันทางฟิสิกส์ (ดู `GOAL.md`)
