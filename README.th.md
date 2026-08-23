# Formula Ultimate

[English version](README.md)

> ฉบับภาษาไทยของ `README.md`

Formula Ultimate คือแพลตฟอร์มวิจัยสำหรับศึกษาการค้นพบทางวิศวกรรมแบบ
open-ended ภายใต้ข้อจำกัดด้านฟิสิกส์ ความปลอดภัย ทรัพยากร และการแข่งขันที่
ประกาศไว้อย่างชัดเจน

> ไม่มีการกำหนดสถาปัตยกรรมรถล่วงหน้า นอกเหนือจากข้อจำกัดที่ประกาศไว้

ระยะวิจัยแรกตั้งใจจำกัดขอบเขตให้แคบ: ค้นพบและเปรียบเทียบ topology ของ
powertrain แบบหนึ่งมิติ ก่อนเพิ่ม geometry รถแบบอิสระ aerodynamics โครงสร้าง
หรือการออกแบบ control ร่วมกัน

## สถานะปัจจุบัน

Repository มี research charter, แผนระบบฟิสิกส์, ขอบเขต design language,
กลยุทธ์ validation, work protocol, package skeleton และ deterministic Level-0
longitudinal reference kernel แล้ว Kernel นี้เป็นฐานทดสอบเชิง analytical
แต่ **ยังไม่ใช่ simulator รถแข่งที่ผ่าน validation**

## แผนผัง Repository

```text
config/                         ค่า simulation และ experiment ที่มี version
docs/
  DESIGN_LANGUAGE_BOUNDARY.md  สิ่งที่ระบบค้นหาสามารถและไม่สามารถค้นพบได้
  PHYSICS_SYSTEM_PLAN.md       domain, contract, solver และ roadmap ฟิสิกส์
  RESEARCH_CHARTER.md           คำถามวิจัย สมมติฐาน และขอบเขต
  VALIDATION_STRATEGY.md        หลักฐานที่ต้องมีก่อนนำไปใช้ทางวิทยาศาสตร์
  WORK_PROTOCOL.md              กฎแผนก่อนทำงานและรายงานผลหลังทำงาน
  work_logs/                    บันทึก plan/result ที่ตรวจย้อนหลังได้
src/formula_ultimate/
  components/                   component model และ typed port ทางฟิสิกส์
  topology/                     candidate graph, mutation และ graph validation
  physics/                      สมการ หน่วย และ numerical solver
  simulation/                   การรันการแข่งขันและ orchestration หลาย fidelity
  telemetry/                    output และหลักฐาน failure ที่ทำซ้ำได้
  experiments/                  baseline, sweep และ multi-seed study
tests/                          unit, invariant, integration และ regression test
```

## ขั้นตอนการพัฒนา

ทุกงานเริ่มด้วย Markdown plan ภาษาอังกฤษและภาษาไทยแยกไฟล์ และจบด้วย
result record ภาษาอังกฤษและภาษาไทยแยกไฟล์ ซึ่งต้องมีหลักฐานที่เทียบเท่าและ
ทำซ้ำได้ Markdown ภาษาอังกฤษทุกไฟล์ที่ดูแลต้องมีไฟล์ `.th.md` คู่กัน อ่าน
[`docs/WORK_PROTOCOL.th.md`](docs/WORK_PROTOCOL.th.md) ก่อนแก้ไขงาน

รันการตรวจ repository ปัจจุบันด้วย:

```powershell
python -m pip install -e .
python -m unittest discover -s tests -v
```

## ขอบเขตการวิจัย

แพลตฟอร์มนี้ไม่ได้อ้างว่าสามารถลบสมมติฐานของมนุษย์ทั้งหมด Design language,
component model, numerical solver และ objective คือขอบเขตการทดลองที่ต้อง
ประกาศชัดเจน ข้ออ้างด้านความใหม่ใช้ได้เฉพาะภายในขอบเขตเหล่านั้น
