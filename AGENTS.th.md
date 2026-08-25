# ข้อกำหนดโปรเจกต์สำหรับ Agent ของ Formula Ultimate

> ฉบับภาษาไทยของ `AGENTS.md`

## Work-Log Protocol แบบบังคับ

ก่อนเปลี่ยน code, configuration, เอกสารวิจัย หรือ experiment ที่เฉพาะกับงาน:

1. สร้าง `docs/work_logs/YYYY-MM-DD_NNN_<slug>-plan.md` และไฟล์ภาษาไทยแยก
   `docs/work_logs/YYYY-MM-DD_NNN_<slug>-plan.th.md`
2. ระบุวัตถุประสงค์ ขอบเขต ไฟล์ที่วางแผน validation เกณฑ์สำเร็จ ความเสี่ยง
   และ non-goal ให้ชัดเจน
3. ตั้งสถานะเป็น `In progress` ก่อนเริ่มงาน

หลังทำงานและก่อน final commit:

1. สร้างไฟล์คู่
   `docs/work_logs/YYYY-MM-DD_NNN_<slug>-result.md` และ
   `docs/work_logs/YYYY-MM-DD_NNN_<slug>-result.th.md`
2. บันทึกไฟล์ที่เปลี่ยน การตัดสินใจ คำสั่งทดสอบ exact exit status output ที่
   เกี่ยวข้อง ข้อจำกัด และงานติดตาม
3. เปลี่ยนสถานะ plan เป็น `Completed` หลัง validation ผ่านเท่านั้น หรือเป็น
   `Stopped` พร้อมเหตุผลหากไม่สามารถทำงานให้เสร็จได้

Plan และ result record เป็นหลักฐานแบบ append-oriented ห้ามแก้บันทึกเก่าเพื่อ
ทำให้ผลที่เกิดภายหลังดูเหมือนถูกวางแผนไว้ ให้สร้าง work item หมายเลขใหม่

## Validated-Commit Protocol แบบบังคับ

ทุก work item ที่ถึงสถานะ `Completed` ต้องถูก commit ทันทีหลัง validation ที่
ประกาศไว้ผ่าน งานยังไม่เสร็จจนกว่า commit จะสำเร็จ

1. Stage เฉพาะไฟล์ที่ระบุชัดว่าเป็นของ work item ห้ามใช้ blanket staging เช่น
   `git add -A` ใน mixed worktree
2. ตรวจขอบเขตที่ stage และเรียก `git diff --cached --check` ก่อน commit
3. เรียก validation gate แบบ fail-fast หรือแยกคำสั่ง failure ต้องหยุด commit
   ทันที และห้ามให้คำสั่งที่สำเร็จภายหลังกลบ exit status ของคำสั่งที่ล้มเหลว
4. สร้าง descriptive commit หนึ่งรายการต่อ work item ที่เสร็จ เว้นแต่ plan
   ระบุเหตุผลชัดเจนว่าต้องมีหลาย commit
5. ตรวจ commit ใหม่และรายงาน short hash ใน result หรือ final handoff
6. รักษาการเปลี่ยนแปลงอื่นของผู้ใช้ ห้าม amend, rewrite, squash, push หรือ
   publish history เว้นแต่ผู้ใช้สั่ง action นั้นแยกต่างหากอย่างชัดเจน

หาก validation, commit hook หรือ Git configuration ขวาง commit ให้คง plan เป็น
`In progress` หรือเปลี่ยนเป็น `Stopped` ตามความเหมาะสม พร้อมรายงาน blocker ที่
แน่นอน ห้ามอ้างว่า work item เสร็จแล้ว

## Bilingual Markdown Protocol แบบบังคับ

- Markdown ภาษาอังกฤษ `name.md` ทุกไฟล์ที่ดูแลต้องมีไฟล์ภาษาไทยแยกชื่อ
  `name.th.md` อยู่ใน directory เดียวกัน
- สร้างหรือแก้ทั้งสองไฟล์ใน work item และ commit เดียวกัน
- ไฟล์ภาษาไทยต้องระบุชื่อ source ภาษาอังกฤษ
- รักษา code identifier สมการ คำสั่ง path หน่วย หลักฐานเชิงตัวเลข สถานะ และ
  ข้อจำกัดให้ตรงกันระหว่างสองภาษา
- ห้ามนำคำแปลภาษาไทยฉบับเต็มไปปนต่อท้ายไฟล์ภาษาอังกฤษ
- หากไฟล์คู่ตกหล่นหรือล้าสมัย งานเอกสารนั้นยังไม่เสร็จ

## กฎวิศวกรรม

- ทำงานจากสมมติฐานฟิสิกส์และหน่วย SI ที่ประกาศชัดเจน
- แยก feasibility validation ออกจาก simulation และ scientific validation
- ให้ conservation residual, numerical failure และ invalid state เป็น output
  ที่สังเกตได้ ห้ามแก้เงียบ ๆ
- ห้ามเรียก design ว่าผ่าน physical validation จาก Level-0 simulation เพียงอย่างเดียว
- เปรียบเทียบ fixed-topology baseline กับ free-topology experiment ด้วย compute
  budget, component library, constraint และ random seed ที่เทียบเท่ากัน
- เก็บ metadata สำหรับ deterministic replay ของทุก experiment
- เพิ่ม test ให้ทุก physical law หรือ component model ที่ implement

## ระเบียบการ Review

งาน experiment ต้องระบุ independent variable, dependent variable, control,
metric, success criteria และ failure criteria อย่างชัดเจน ต้องพยายามหักล้าง
สมมติฐานที่ต้องการ พร้อมบันทึกหลักฐานสนับสนุน หลักฐานขัดแย้ง คำอธิบายทางเลือก
หลักฐานที่ยังขาด และระดับความมั่นใจ
