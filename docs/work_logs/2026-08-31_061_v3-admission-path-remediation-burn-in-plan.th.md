# แผนงาน 061: Protocol v3 Admission-Path Remediation และ Burn-In

สถานะ: เสร็จสมบูรณ์ (Completed)

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-31_061_v3-admission-path-remediation-burn-in-plan.md`

## วัตถุประสงค์

สร้าง successor protocol/campaign v3 หลัง Work 060 fail closed ก่อน main-ledger initialization แทน hard-coded v1 admission hash path ด้วย exact active protocol path เพิ่ม regression test ที่เรียก successor admission validation แล้วรัน/commit fresh excluded-seed burn-in ก่อน successor main opportunity ใด ๆ

## ขอบเขต remediation ที่ freeze

- IDs ใหม่: `bounded_whole_vehicle_main_campaign_v3` และ `FU-BMC-003`
- Frozen source commit: `3d140bf8ffb2ad7f1476ca81905fb84648741481`
- เก็บ Work 060 failure SHA-256 `8b02e9292e173b797afe12134031547c3060a70a8da1270a1e06fe1b8a17e1e2` และ v2 admission fingerprints โดยไม่ reuse observations
- เปลี่ยนเฉพาะ admission protocol-file identity routing: validation ต้อง hash `--protocol` path exact ที่ command เลือก
- Scientific rules, seeds, budgets, search, physics, partitions, thresholds, outcomes, statistics และ claims ต้อง byte-equivalent หลังถอด identity/remediation fields

## ไฟล์และ tests ที่วางแผน

- เพิ่ม full v3 protocol declaration และขยาย exact successor validation
- ย้าย admission validation เป็น testable campaign-physics function ที่รับ active protocol path
- อัปเดต generic command ให้เรียก function นั้น เพิ่ม Work 061/062 wrappers
- ทดสอบ valid v3 admissionกับ v3 path, reject เมื่อใช้ path อื่น, scientific equivalence ข้าม v1/v2/v3 และ JSON representation regression เดิม
- รัน fresh v3 process-resume/burn-in ledgers ใต้ `artifacts/work061/` เขียนรายงาน validate และ commit

## เกณฑ์สำเร็จและหยุด

สำเร็จเมื่อ focused/full tests ผ่าน, exact v3 protocol validation, process probe `1/1/0`, fresh burn-in `240/240/0`, equal `80/80/80`, GRID unique, downstream evidence terminalครบ, exact replay, accepted decision, commit และ clean-tree replay ที่ admission validator ผ่านกับ exact v3 path โดยไม่สร้าง main ledger

หยุดหากต้องแก้ code/config หลัง v3 burn-in, admission-path regression fail หรือ fairness, identity, partition, solver, CAD, ledger, replay gate ใด fail Work 061 ไม่ใช้ main seed

## Evidence discipline และสิ่งที่ไม่ทำ

ต้องรายงาน fail-closed controls ก่อนหน้าทั้งสอง ไม่ซ่อน งานนี้ยังเป็น bounded digital evidence ไม่ใช่ physical validation หรือ safety proof และไม่เปลี่ยน scientific settings, push หรือ publish
