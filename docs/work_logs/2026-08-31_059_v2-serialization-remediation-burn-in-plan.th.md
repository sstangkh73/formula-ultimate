# แผนงาน 059: Protocol v2 Serialization Remediation และ Fresh Burn-In

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_059_v2-serialization-remediation-burn-in-plan.md`

## วัตถุประสงค์

แทน stopped protocol `bounded_whole_vehicle_main_campaign_v1` ด้วย protocol/campaign identity ใหม่ แก้เฉพาะ promotion JSON representation boundary ที่ Work 057 พบ เพิ่ม write/read regression control freeze corrected implementation แล้วรัน fresh excluded-seed burn-in จาก v2 ledgers ว่าง

## Failure evidence ที่เก็บไว้

Work 057 หยุดหลัง training records `240/240` และก่อน holdout เพราะ stored JSON `candidate_ids` lists ถูกเปรียบเทียบกับ in-memory tuples Hashes ของ v1 ledgers ถูกบันทึกในผล Work 057 Ledgers เหล่านั้น immutable และห้าม import เข้า v2

## ขอบเขตและไฟล์ที่วางแผน

- เพิ่ม `config/experiments/bounded_whole_vehicle_main_campaign_v2.json` ด้วย protocol ID `bounded_whole_vehicle_main_campaign_v2`, campaign ID `FU-BMC-002`, frozen source commit `b43c69fd9b52acf4888c9bb3abec8b4c179c8424` และ explicit remediation link ไป stopped v1 evidence
- ขยาย strict protocol validation สำหรับ exact v2 identity โดยยัง validate v1 ได้
- Canonicalize promotion selections ด้วย JSON-compatible round trip ก่อน append/replay comparison โดยไม่เปลี่ยน candidate generation, evaluation, partitions, budgets, physics, thresholds หรือ analysis
- เพิ่ม append/reload regression test เพื่อพิสูจน์ว่า tuple/list representation หยุด equal evidence ไม่ได้และ altered values ยังถูก reject
- เพิ่ม Work 059/060 wrappers, fresh ignored artifacts, เอกสาร/ผลสองภาษา validation และ dedicated commit

## Variables, controls และ metrics

Scientific independent/dependent variables และ controls ตรงกับ v1 ทุกอย่าง Remediation variable มีเพียง serialization representation (`tuple` ก่อน JSON เทียบกับ `list` หลัง JSON) Controls เปรียบเทียบ semantically equal round-tripped selection evidenceและ mutated candidate ID Metrics คือ exact stage replay, `240` terminal burn-in opportunities, stream counts `80/80/80`, promotion shortfall, terminal downstream counts, tool/implementation hashes และไม่ reuse v1/main ledger

## เกณฑ์สำเร็จ

1. v2 validate โดย scientific rules เท่ากับ v1 ทุกข้อ ยกเว้น identities, frozen commit และ remediation provenance
2. Regression test ผ่านหลัง append/reload และ reject altered selection content
3. Fresh v2 process-resume probeคืน reservation/result/pending exactly `1/1/0`
4. Fresh burn-in คืน `burn_in_accepted_for_admitted_main_campaign` พร้อม terminal training attempts `240`, exact replay, downstream evidence terminalครบ และไม่แก้ implementation/config หลัง observation
5. Commit Work 059 แล้ว clean-tree verify-only replay อัปเดต admission evidenceให้ชี้ commit นั้นก่อน Work 060

## เกณฑ์ล้มเหลว

หยุด successor main execution เมื่อพบ serialization mismatch ใหม่, identity drift, ledger reuse, budget inequality, GRID repeat, leakage, downstream terminal หาย, solver/CAD tool unavailable หรือต้องแก้หลัง burn-in ห้ามซ่อมแล้วทำต่อใต้ v2 หลัง observation

## การตรวจสอบ

รัน focused regression/protocol/runner tests, full tests, compilation, fresh process-resume probe, fresh burn-in, verify-only replay, explicit staged checks, commit และ clean-tree verify-only replay ตรวจ exact artifact counts, fingerprints, implementation/tool identities และ decision

## สิ่งที่ไม่ทำ

ไม่เปลี่ยน scientific rule, threshold, material, load, topology grammar, hypothesis, seed, budget หรือ claim boundary Work 059 ไม่ใช้ main seed และไม่อ้าง physical validation, safety, superiority, push หรือ publication
