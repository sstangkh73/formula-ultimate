# แผนงาน 060: Protocol v2 Admitted Main Campaign

สถานะ: หยุดก่อน execution — admission preflight ใช้ path hash ของ protocol v1 จึง reject valid v2 admission ก่อน ledger initialization

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_060_v2-admitted-main-campaign-plan.md`

## วัตถุประสงค์

รันและวิเคราะห์ successor campaign `FU-BMC-002` ด้วย exact committed v2 implementation ที่ Work 059 admit แผนนี้แทน stopped Work 058 โดยไม่ reuse v1 campaign observation ใด ๆ

## แบบการทดลองและขอบเขต

Independent variable, paired seeds 12 ตัว `55001`–`55012`, treatments `GRID`/`RANDOM`/`EVOLUTION`, 80 opportunities ต่อ treatment/seed, รวม `2,880`, promotion cap สองตัว, frozen holdouts, Work 053 refinement, STEP/FreeCAD witness, outcomes, analysis seed `551337`, statistical methods, winner rule, prohibited claims และ failure policies ไม่เปลี่ยนจาก Work 058/v1

Work 060 จะ reuse committed Work 059 code โดยไม่แก้ เขียน fresh ignored ledgers/evidence ใต้ `artifacts/work060/` วิเคราะห์ preregistered outcome ทุกตัว เขียน result/research evidence สองภาษา validate และ commit หากหลัง admission ต้องแก้ code/config ให้หยุด `FU-BMC-002`

## เกณฑ์ admission และสำเร็จ

Admission ต้องมี clean committed Work 059 summary ที่ decision เป็น `burn_in_accepted_for_admitted_main_campaign`, protocol ID `bounded_whole_vehicle_main_campaign_v2`, campaign ID `FU-BMC-002`, implementation/upstream/tool identities exact และ replay exact

สำเร็จเมื่อมี terminal opportunities exactly `2,880`, 80 ต่อ treatment/seed, 960 ต่อ treatment, GRID opportunities ไม่ซ้ำ, terminal evidenceครบสำหรับ selected candidate ทุกตัว, exact replay, preregistered paired-seed analysisครบ และ final campaign status ที่อนุญาตหนึ่งค่า Preferred effect ที่ไม่เป็นบวกหรือไม่มี supported finisherยังเป็นผลที่ถูกต้อง

## Stop criteria และ evidence discipline

หยุดเมื่อ identity, fairness, partition, ledger, replay, mutation-after-burn-in หรือ infrastructure ผิด ห้าม retry/replace consumed opportunity ต้องรายงาน supporting/contradicting evidence, alternative explanations, missing evidence, confidence, compute cost, failure counts และ bounded claim level

## การตรวจสอบและสิ่งที่ไม่ทำ

รัน admission check, campaign, verify-only replay, full tests, compilation, bilingual documentation checks, explicit staging, `git diff --cached --check`, commit และ clean-tree replay ห้ามอ้าง physical validation, real safety, manufacturability, race/algorithm superiority, novelty, discovery หรือ certified material performance และไม่ push/publish
