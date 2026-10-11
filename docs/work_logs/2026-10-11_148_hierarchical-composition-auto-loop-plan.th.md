# แผน Work 148: Auto-Loop สำหรับการประกอบชิ้นส่วน free-form แบบลำดับชั้น

ฉบับภาษาอังกฤษ: `2026-10-11_148_hierarchical-composition-auto-loop-plan.md`

วันที่: 2026-10-11

Status: Completed

## วัตถุประสงค์

เตรียม runner ของ Claude + Codex ใน `auto-loop/` (ยังไม่ได้อยู่ใน git) ให้ทำงานได้เองโดยไม่มีคนเฝ้า
ตามเป้าหมายที่เจ้าของโครงการกำหนด คือให้ระบบออกแบบชิ้นส่วนแบบ free-form ได้ทุกขนาด แล้วประกอบจากล่างขึ้นบน
ชิ้นเล็กประกอบเป็นชุดย่อย ชุดย่อยประกอบเป็นระบบ ระบบประกอบเป็นรถทั้งคัน
และต้องเป็นแบบนี้กับทุกหน้าที่ของรถ ไม่ใช่เฉพาะตัวแปลงพลังงาน
ห้ามกำหนดรายการชิ้นส่วนแบบดั้งเดิมไว้ล่วงหน้า (ลูกสูบ หัวฉีด น็อต)

งานนี้เตรียมลูปเท่านั้น คือเขียนเป้าหมาย สเปกการยอมรับ ตัวตรวจ และ runner
แต่ไม่เขียน generator และไม่รันลูป

## ขอบเขต

- แทนเป้าหมาย ซอร์ส และเทสต์ตัวอย่าง BAHTTEXT ของ template ด้วยเป้าหมาย
  และชุด acceptance test ที่ห้ามแก้ สำหรับการประกอบ free-form แบบลำดับชั้น
- ปรับ runner ให้เข้ากับ repository นี้และกับ `AGENTS.md`
  - รันจาก root ของ repository และไม่ `git init` repository ซ้อนเด็ดขาด
  - ไม่ยอมรันบน `main` และทำงานบน branch `loop/...` แยกต่างหาก
  - ไม่ stage แบบเหมารวม agent stage เฉพาะไฟล์ที่ระบุ และ commit หลัง validation ที่ประกาศไว้ผ่านเท่านั้น
  - แต่ละรอบเป็น work item ที่มีเลขกำกับ พร้อม plan/result สองภาษา
  - หยุดเมื่อไฟล์ที่ป้องกันไว้ถูกแก้ รวมถึงเทสต์ใดๆ ที่มีอยู่ตอนเริ่มลูป
- กำหนดตัวตรวจเป็น 3 ด่าน: ตรวจขอบเขตการเผยแพร่ข้อมูลวัสดุ, unittest ทั้งหมดของ repository
  และชุด acceptance
- เขียนเอกสารของลูปทั้งภาษาอังกฤษและภาษาไทย

## สเปกการยอมรับ (ลูปถือว่า "เสร็จ" เมื่อไหร่)

entry point
`scripts/hierarchy/generate_hierarchical_vehicle.py --seed S --out DIR` ที่รันด้วย
CadQuery runtime ที่ pin ไว้ `.tools/cadquery-mcp/Scripts/python.exe`
ต้องเขียน `DIR/manifest.json` และ STL mesh หนึ่งไฟล์ต่อชิ้นส่วน leaf หน่วยเป็นเมตร
acceptance test รันด้วย Python ของระบบ และตรวจผลลัพธ์อย่างอิสระ ไม่เชื่อสิ่งที่ generator อ้างเอง

1. Replay: seed เดียวกันต้องได้ manifest และ mesh เหมือนกันทุก byte โดย manifest
   บันทึก design-language version, seed, config hash และ git commit
2. ลำดับชั้น: ต้นไม้ชิ้นส่วนต้องไม่มีวงวนและมี root เดียว มีอย่างน้อย 4 ระดับ
   และมีชิ้นส่วน leaf อย่างน้อย 150 ชิ้น ขนาดลักษณะเฉพาะของชิ้น leaf
   ต้องต่างกันอย่างน้อย 100 เท่า
3. ทุกหน้าที่: ความสามารถแบบไม่ผูกเทคโนโลยีทั้งเก้าใน
   `functional_vehicle.REQUIRED_CAPABILITIES` ต้องมี assembly subtree รองรับ
   ที่ลึกอย่างน้อย 2 ระดับและมีชิ้น leaf อย่างน้อย 5 ชิ้น
4. เรขาคณิต: mesh ของ leaf ทุกชิ้นต้องปิด หันทิศทางสม่ำเสมอ และมีปริมาตรเป็นบวก
   มวลของ leaf เท่ากับปริมาตร mesh คูณความหนาแน่นที่ประกาศ มวลของ assembly
   เท่ากับผลรวมของลูก มวลรถและจุดศูนย์กลางมวลต้องตรงกับที่คำนวณใหม่จาก mesh
5. Free form: leaf ที่เต็ม bounding box แนวแกน (คือเป็นกล่อง) มีได้ไม่เกิน 25 %
   leaf ทุกชิ้นต้องบันทึกโปรแกรมที่ใช้สร้างมัน พร้อม hash ที่ตรงกัน
6. Interface: ใน assembly ทุกตัว ลูกต้องเชื่อมกันด้วย interface ที่ประกาศไว้
   ซึ่งชนิดเป็นหนึ่งในชนิดรอยต่อแบบไม่ผูกเทคโนโลยีจาก Work 140
   interface ทุกตัวต้องมีการสัมผัสของ mesh ที่วัดได้จริงภายใน tolerance ที่ประกาศ (ไม่เกิน 0.5 mm)
   และจุดที่สุ่มตรวจต้องไม่พบ leaf ทะลุเข้าไปในอีกชิ้นเกิน tolerance หรือ interference ที่ประกาศ
7. ไม่มี template ตายตัว: seed ต่างกัน 3 ค่าต้องได้โครงสร้างต้นไม้ที่ต่างกันทุกคู่
   และแต่ละความสามารถต้องมีโครงสร้าง subtree อย่างน้อย 2 แบบในสาม seed นั้น

## ไฟล์ที่วางแผนไว้

- `auto-loop/README.md`, `auto-loop/README.th.md`
- `auto-loop/GOAL.md`, `auto-loop/GOAL.th.md`
- `auto-loop/PROMPT.md`, `auto-loop/PROMPT.th.md`
- `auto-loop/progress.md`, `auto-loop/progress.th.md`
- `auto-loop/run-loop.ps1`, `auto-loop/verify.ps1`, `auto-loop/tools/codex.sh`,
  `auto-loop/.gitignore`
- `auto-loop/acceptance/__init__.py`,
  `auto-loop/acceptance/test_hierarchical_composition.py`
- ลบไฟล์ตัวอย่าง `auto-loop/src/bahttext.py` และ `auto-loop/tests/test_bahttext.py`
- แผนนี้ ฉบับภาษาไทย และบันทึกผล Work 148 ที่คู่กัน

## Validation

1. ตรวจชุด acceptance เองด้วย fixture ใน scratchpad: package สังเคราะห์ขนาดเล็กที่ถูกต้อง
   ต้องผ่านทุกข้อ และ package ที่ตั้งใจทำให้เสีย (mesh เปิด, มวลผิด, ขาดความสามารถ, ชิ้นทะลุกัน,
   ผลไม่ deterministic, template เดียว) ต้องตกในเทสต์ที่ตั้งใจไว้แต่ละข้อ
   fixture generator ถูกฉีดผ่าน environment variable ที่ `verify.ps1` ล้างทิ้ง
2. รัน `pwsh -NoProfile -File auto-loop/verify.ps1` บน repository จริง
   ผลที่คาดคือด่าน 1 และ 2 ผ่าน ส่วนด่าน 3 ตกเพราะยังไม่มี generator ซึ่งเป็นสถานะเริ่มต้นของลูป
3. ตรวจ syntax ของ `run-loop.ps1` ด้วย PowerShell parser และลอง preflight logic
   (กัน branch, hash ไฟล์ที่ป้องกัน) แบบ dry-run โดยไม่เรียก `claude`
4. รัน unittest ทั้งหมดและ publication-boundary validator
5. stage เฉพาะไฟล์ของ Work 148 รัน `git diff --cached --check` commit ครั้งเดียว และรายงาน hash

## เกณฑ์ความสำเร็จ

- ชุด acceptance ตกบน repository ปัจจุบันด้วยเหตุผลที่ระบุ และผ่านหรือตกถูกต้องกับ fixture ตรวจตัวเองทุกตัว
- runner `git init` ไม่ได้ รันบน `main` ไม่ได้ ไม่ stage แบบเหมารวม และหยุดเมื่อไฟล์ที่ป้องกันถูกแก้
- เป้าหมายระบุชัดว่าการผ่านคือด่าน representation ของเรขาคณิตและการประกอบ ไม่ใช่การยืนยันทางฟิสิกส์
- เทสต์เดิมทั้งหมดยังผ่าน

## ความเสี่ยง

- การตรวจ interference จาก mesh สุ่มดูเฉพาะ vertex และจุดศูนย์กลางของสามเหลี่ยม
  จึงอาจพลาดการซ้อนทับแบบตัดผ่านกันบางกรณี ข้อจำกัดนี้บันทึกไว้ในเป้าหมาย
- ตัวชี้วัดสัดส่วนกล่องเป็นแค่ตัวแทนของ free form ไม่ได้พิสูจน์ความใหม่
- ความหลากหลายจากสาม seed แสดงว่าการแยกส่วนไม่ใช่ template ตายตัวแบบเดียว
  แต่ไม่ได้แสดงว่าการแยกส่วนนั้นมีประโยชน์
- การให้ CadQuery สร้างชิ้นส่วนเกิน 150 ชิ้นต่อ seed สี่รอบอาจช้า ชุด acceptance ให้เวลา 20 นาทีต่อรอบ
- agent ที่ทำงานเองโดยไม่มีคนเฝ้ายังอาจเขียนโค้ดคุณภาพต่ำที่ผ่านได้
  การป้องกันคือ acceptance test ที่ห้ามแก้ และให้คนตรวจทุก work item ที่ commit

## สิ่งที่ไม่ทำ

- ไม่เขียน generator หรือ physics model ใดๆ
- ไม่รันลูป และไม่ใช้งบ API ของ Claude หรือ Codex กับมัน
- ยังไม่เชื่อมลำดับชั้นเข้ากับ race simulation ซึ่งเป็นเป้าหมายรอบหลัง
- ไม่แตะข้อมูลวัสดุใน `/private/` acceptance test อ่านค่าความหนาแน่นจาก artifact
  ที่ generator สร้างและอยู่ใน gitignore เท่านั้น
- ไม่ push ไม่เผยแพร่ และไม่เขียนประวัติ git ใหม่
