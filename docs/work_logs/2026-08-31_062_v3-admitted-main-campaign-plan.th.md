# แผนงาน 062: Protocol v3 Admitted Main Campaign

สถานะ: กำลังดำเนินการ แต่ execution ยังล็อกจนกว่า Work 061 commit และ clean-tree active-path admission replay ผ่าน

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_062_v3-admitted-main-campaign-plan.md`

## วัตถุประสงค์และแบบการทดลอง

รัน successor `FU-BMC-003` ด้วย exact committed Work 061 code/admission โดย independent variable, paired seeds `55001`–`55012`, three treatments, 80 opportunities ต่อ treatment/seed, รวม `2,880`, promotion/refinement/CAD gates, hypotheses, paired-seed analyses, winner rule, failures และ prohibited claims ไม่เปลี่ยน

## Admission และ execution

ก่อน ledger initialization ต้องตรวจ Work 061 decision, v3 protocol file SHA/fingerprint, upstream/tool/implementation identities, committed ancestor, clean worktree และ active protocol path แล้วจึงรัน fresh append-only ledgers ใต้ `artifacts/work062/` หาก code/config เปลี่ยนหลัง admission ให้หยุด `FU-BMC-003`; consumed failures ห้าม retry

## เกณฑ์สำเร็จ ล้มเหลว และ validation

สำเร็จเมื่อมี terminal attempts `2,880`, treatment/seed ละ `80`, treatment ละ `960`, GRID unique, downstream terminal evidenceครบ, exact replay, preregistered statisticsทุกตัว, explicit hypothesis support/contradiction, final status, bilingual evidence, tests, compilation, explicit commit และ clean-tree replay การไม่มี supported finisherเป็นผลที่ถูกต้อง Identity/fairness/leakage/replay violations หยุดเป็น protocol failure ส่วน durable infrastructure unavailable หยุดเป็น infrastructure failure

## สิ่งที่ไม่ทำ

ไม่อ้าง physical validation, safety, manufacturability, race superiority, algorithm superiority, novelty, discovery, arbitrary topology หรือ certified material และไม่ push/publish
