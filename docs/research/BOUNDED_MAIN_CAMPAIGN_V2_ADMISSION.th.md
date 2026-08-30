# การ Admit Bounded Main Campaign v2

ไฟล์ต้นฉบับภาษาอังกฤษ: `BOUNDED_MAIN_CAMPAIGN_V2_ADMISSION.md`

สถานะ: Burn-in ผ่าน แต่ admitted main execution ยังมีเงื่อนไขว่าต้อง commit และ clean-tree replay ก่อน

## เหตุผลที่มี v2

Protocol v1 หยุดระหว่าง excluded-seed burn-in หลัง training opportunities ครบ 240 ค่า promotion ไม่เปลี่ยน แต่ in-memory tuple ถูกเปรียบเทียบตรงกับ JSON list representation Strict replay จึง reject representation mismatch ก่อน holdout และ main-seed evaluation ทั้งหมด v1 ledgers และ failure hashes ยังคง immutable

Protocol `bounded_whole_vehicle_main_campaign_v2`, campaign `FU-BMC-002` เปลี่ยนเฉพาะ identity และ remediation provenance Regression check พิสูจน์ว่า scientific-rule subtree ทั้งหมดเท่ากับ v1 Implementation canonicalize promotion evidence ผ่าน strict JSON round trip ก่อน append/replay comparison โดย candidate generation, opportunity budgets, material, loads, thresholds, partitions, physics, hypotheses, outcomes และ analysis ไม่เปลี่ยน และไม่มี v1 observation เข้า v2

## ผล fresh v2 burn-in

Isolated process-resume probe หยุด process แรกหลัง reserve `candidate-52a6df50771f058c` แล้ว process ที่สอง complete exact candidate นั้น Counts reservation/result/pending คือ `1/1/0`

Seed `55999` ให้ผล:

| หลักฐาน | ผล |
|---|---:|
| Training reservations/results/pending | `240 / 240 / 0` |
| Attempts GRID/RANDOM/EVOLUTION | `80 / 80 / 80` |
| Unique GRID opportunities | `80` |
| Feasible / structural-failure training outcomes | `189 / 51` |
| Promotion streams/candidates/shortfall | `3 / 6 / 0` |
| Terminal holdout/refinement/CAD records | `6 / 6 / 6` |
| Refinement passed | `6 / 6` |
| STEP/FreeCAD witness passed | `6 / 6` |
| Treatment/seed streams ที่มี supported finisher | `3 / 3` |
| External solver/CAD processes | `123` |

Training combined fingerprint คือ `52de5c3a44423b126e6e05b50c594a0a70c4956d084bc4bc2a02b3c4fa9b3054` Downstream stage fingerprint คือ `cd019afbe7b85b10e6fc5bc744314b16b281e4dd1701b0eab0c94681f7978e97` และ verify-only replay คืน exact

## ขอบเขต admission

Burn-in decision คือ `burn_in_accepted_for_admitted_main_campaign` ซึ่งอนุญาตให้ exact committed implementation ขอ main execution ได้หลัง clean-tree verification ตรงกับ protocol, upstream, CalculiX, CadQuery Python, FreeCAD Python และ implementation hashes หาก code/config เปลี่ยนภายหลัง admission จะ invalid และต้องหยุด `FU-BMC-002`

ผลนี้พิสูจน์ bounded pipeline execution ไม่ใช่ physical validation Level 0 เป็น selection gate, refinement เป็น linear-elastic beam network และ STEP/FreeCAD พิสูจน์ exact primitive geometry transfer ส่วน solid/contact/nonlinear behavior, physical materials, tolerances, manufacturing, hardware safety และ independent replication ยังขาด
