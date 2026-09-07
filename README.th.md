# Formula Ultimate

[English version](README.md)

> ฉบับภาษาไทยของ `README.md`

Formula Ultimate คือแพลตฟอร์มวิจัยสำหรับการค้นพบทางวิศวกรรมแบบ open-ended
ด้วยระบบอัตโนมัติ ภารกิจระยะยาวคือให้เอเจนต์ออกแบบยานยนต์แข่งขัน 3D ได้ทั้งคัน
ตั้งแต่สถาปัตยกรรมระดับรถจนถึง geometry ภายในชิ้นส่วน โดยไม่กำหนดให้ใช้ layout,
dimension, powertrain, การจัดวางล้อ, รูปทรงตัวถัง หรือรูปทรงชิ้นส่วนที่กติกา
รถแข่งและแนวคิดของมนุษย์ในอดีตกำหนดไว้

> ไม่มีการกำหนดสถาปัตยกรรมรถแบบดั้งเดิมล่วงหน้า นอกเหนือจากข้อจำกัดด้านฟิสิกส์
> การแข่งขัน พลังงาน ทรัพยากร ความปลอดภัย และหลักฐานที่ประกาศไว้

เป้าหมายไม่ใช่เพียงสร้างรถหน้าตาแปลก งานวิจัยถามว่าเอเจนต์สามารถค้นพบ
สถาปัตยกรรมรถหรือเทคโนโลยีชิ้นส่วนที่แตกต่างด้านหน้าที่ ลดเวลาแข่งขันรวมใน
แต่ละ race environment ชนะ conventional baseline ที่ปรับแต่งอย่างยุติธรรม
และยังคงข้อได้เปรียบเมื่อประเมินด้วยฟิสิกส์ที่มี fidelity สูงขึ้นได้หรือไม่

## คำถามวิจัยหลัก

ภายใต้ race และ energy protocol ที่อ้างอิง Formula One และมี version ซึ่งกำหนด
ให้ primary propulsion energy ทั้งหมดต้องอยู่บนรถก่อนเริ่มแข่งและห้ามเติม
primary energy ระหว่างการแข่งขัน เอเจนต์อัตโนมัติสามารถค้นพบสถาปัตยกรรม
ยานยนต์แข่งขัน 3D และเทคโนโลยีชิ้นส่วนแบบครบถ้วน โดยไม่กำหนด conventional
vehicle layout ล่วงหน้า ซึ่งทำเวลาแข่งขันรวมดีกว่า conventional baseline
ที่ปรับแต่งแล้วและยังผ่าน multi-fidelity physics validation ได้หรือไม่

สำหรับ race environment `r` objective หลักคือ:

```text
d*_r = arg min_d T_race(d, r)
```

โดยมีเงื่อนไขอย่างน้อย:

```text
RaceCompleted(d, r) = true
initial primary energy <= declared race energy budget
external primary-energy addition during the race = 0
conservation residuals <= declared tolerances
complete 3D CAD is valid and physically accounted
structural, thermal, aerodynamic, tyre, material, and numerical gates pass
```

ดังนั้น “เร็วที่สุด” หมายถึงเวลาโดยรวมต่ำที่สุดในกลุ่ม candidate ที่แข่งจบตาม
race definition และผ่าน evidence gate ที่ต้องใช้ ไม่ใช่ความเร็วสูงสุดชั่วขณะ
การวิ่งก่อนพัง หรือ numerical exploit

## Race และ Energy Contract ที่อ้างอิง Formula One

Formula Ultimate นำข้อกำหนดสถาปัตยกรรมเก่าออก แต่ไม่ได้นำ race discipline
หรือ energy accounting ออก เอกสารอ้างอิงปัจจุบันคือกติกา FIA Formula One
ปี 2026 ที่เผยแพร่แล้ว:

- Sporting Regulation B5.1.4 ห้ามเพิ่มหรือนำเชื้อเพลิงออกหลังรถออกจาก Pit Lane
  เพื่อวิ่ง reconnaissance lap จนแสดง end-of-session signal
- Technical Regulation C6.4.4 ระบุว่าห้ามเพิ่มหรือนำเชื้อเพลิงออกจากรถระหว่าง
  Race

แหล่งข้อมูลทางการ: [2026 FIA Section B, Sporting Regulations, Issue
08](https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_b_sporting_-_iss_08_-_2026-08-05_7.pdf)
และ [2026 FIA Section C, Technical Regulations, Issue
20](https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_c_technical_-_iss_20_-_2026-08-05.pdf)
ซึ่งเผยแพร่วันที่ 5 สิงหาคม 2026 ทั้งคู่

ทุก experiment ต้อง pin regulatory profile กฎแกนกลางที่รับมาคือ:

```text
all declared primary propulsion energy is onboard before the race
no undeclared external primary-energy inflow is permitted during the race
```

เอเจนต์ออกแบบ internal energy recovery ได้อย่างอิสระเมื่อ experiment อนุญาต
แต่ทุก joule ที่ recover ต้องตรวจย้อนกลับไปยัง braking, exhaust, heat,
suspension หรือ physical flow อื่นที่ประกาศไว้ Conservation loss ต้องสังเกตได้
ห้ามนับพลังงานซ้ำหรือสร้างพลังงานด้วย control edge

โปรเจกต์ **ไม่** รับข้อจำกัด geometry หรือ architecture เฉพาะ ICE/ERS ของ FIA
ปัจจุบันทั้งหมดโดยอัตโนมัติ การเปรียบเทียบ battery, chemical fuel, flywheel,
compressed media, thermal store หรือระบบพลังงานที่เอเจนต์เสนอ ต้องมี profile
energy-equivalent ที่เป็น technology-neutral และมี version ทุก treatment
ต้องได้รับโอกาสด้าน initial primary energy ตามที่ประกาศเท่ากัน เว้นแต่ energy
budget เป็น independent variable ที่ประกาศล่วงหน้า

## ขอบเขตการออกแบบ 3D แบบเปิด

ในอนาคตเอเจนต์สามารถเปลี่ยนหรือสร้าง:

- topology และ packaging ทั้งคัน;
- dimension ตัวรถ external surface และ aerodynamic device;
- จำนวน ตำแหน่ง และการกำหนดหน้าที่ของ ground-contact endpoint ที่อนุญาต;
- energy store, converter, propulsion path, cooling path และ controller;
- structure, housing, duct, rotor, joint, coupling, fastener และ component
  อื่นที่ไม่มีใน conventional catalog;
- การกระจายวัสดุภายในและ component geometry ภายใต้ material และ manufacturing
  language ที่ประกาศ

น็อตหรือ fastener ที่ไม่เคยมีรูปแบบดังกล่าวมาก่อนสามารถเป็น candidate ได้
แต่มันไม่เป็น discovery เพียงเพราะรูปร่างใหม่ Interface, material, manufacturing
assumption, load, contact behavior, failure mode และผลต่อรถแข่งทั้งคันต้องผ่าน
evidence gate เช่นเดียวกับชิ้นส่วนที่รู้จักอยู่แล้ว

การออกแบบ 3D ทั้งคันเป็น causal input ของ simulation ไม่ใช่ render ตกแต่ง:

```text
functional requirements and typed interfaces
  -> agent-generated complete 3D CAD / B-rep / implicit geometry
  -> independent geometry validity and interface checks
  -> geometry-derived volume, mass, centre of mass, and inertia
  -> packaging, collision, clearance, and manufacturing gates
  -> structural, thermal, flow, electromagnetic, and aerodynamic evaluation
  -> uncertainty-aware component models
  -> vehicle and race simulation
  -> failures and evidence returned to the next design generation
```

Generated component ห้ามรายงานเองว่าเบา แข็งแรง เย็น มีประสิทธิภาพ ปลอดภัย
หรือผลิตได้ คุณสมบัติเหล่านี้ต้องมาจาก material, geometry, boundary condition
และ independent evaluator ที่ประกาศไว้

## สิ่งที่นับเป็น Discovery

ดีไซน์เป็นเพียง **technology-discovery candidate** เมื่อ:

1. functional architecture หรือ operating principle ต่างจาก baseline
   ที่ประกาศ ไม่ใช่เพียงหน้าตา;
2. ปรับปรุงเวลาแข่งขันรวมหรือ metric ที่ประกาศล่วงหน้า ภายใต้ constraint,
   evaluation budget, component opportunity และ random seed ที่เทียบเท่ากัน;
3. ข้อได้เปรียบไม่ได้เกิดจาก solver bug, hidden energy, invalid material,
   objective loophole หรือ compute ที่ไม่เท่ากัน;
4. candidate ยังคง valid เมื่อ promote ไป fidelity ถัดไป และผ่าน independent
   model เมื่อทำได้;
5. เก็บ source, geometry, configuration, regulatory profile, solver setting,
   artifact, hash และ replay metadata ไว้

“Generated,” “simulation-valid,” “promoted,” “physically validated” และ
“discovered” เป็นข้ออ้างคนละระดับและห้ามใช้แทนกัน

## สถานะ Implementation ปัจจุบัน

ภารกิจสูงสุดตั้งใจกว้างกว่า implementation ปัจจุบัน Repository มี governance
และ validation document, deterministic Level-0 longitudinal reference kernel
และวงจรหลักฐาน component ตัวแรก
`CadQuery -> STEP -> FreeCAD -> Level 0` แล้ว Grammar 3D ตัวแรกเป็นการทดลอง
mounting plate แบบ bounded ไม่ใช่รถทั้งคันและไม่ใช่ racing component ที่ผ่าน
physical validation

Phase 1 ยังตั้งใจจำกัดขอบเขตให้แคบ: ค้นพบและเปรียบเทียบ topology ของ
powertrain แบบหนึ่งมิติภายใต้ budget ที่เท่ากัน ก่อนเปิด geometry 3D ทั้งคัน,
aerodynamics, structure และ control co-design Fidelity ladder เป็นเส้นทาง
promotion ไม่ใช่สิทธิ์ให้อ้าง capability ของขั้นหลังล่วงหน้า

## แผนผัง Repository

```text
config/                         ค่า simulation และ experiment ที่มี version
docs/
  3d/                           CAD environment และ constrained 3D grammar
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

Formula Ultimate ไม่ได้อ้างว่าสามารถลบสมมติฐานของมนุษย์ทั้งหมด Race definition,
energy profile, physics model, material/manufacturing language, component และ
geometry grammar, numerical solver, fidelity gate และ objective คือขอบเขต
การทดลองที่ต้องประกาศ Open-ended search หมายถึงไม่มี conventional architecture
ที่กำหนดล่วงหน้า **ภายในขอบเขตที่ประกาศเหล่านั้น** ไม่ได้หมายถึงไม่มีข้อจำกัด

รูปลักษณ์ใหม่ไม่ใช่หลักฐานของเทคโนโลยีใหม่ และความสำเร็จระดับ Level 0 ไม่ใช่
physical validation ต้องพยายามหักล้างสมมติฐานที่ต้องการในทุก promotion stage

## สัญญาอนุญาต

- **โค้ด** ใช้สัญญาอนุญาต MIT ดู [`LICENSE`](LICENSE)
- **เอกสาร ข้อมูล และภาพประกอบ** ใช้ Creative Commons Attribution 4.0
  International (CC BY 4.0) ดู [`LICENSE-DATA.md`](LICENSE-DATA.md)
  ครอบคลุม `docs/`, `config/` และรายงานที่สร้างขึ้น

การให้เครดิต: Chisanupong Injun (2026)
[ORCID 0009-0000-2979-1916](https://orcid.org/0009-0000-2979-1916)

เอกสารกฎของ FIA ที่ลิงก์ไว้ใน `README.md` เผยแพร่โดย FIA
และไม่อยู่ภายใต้สัญญาอนุญาตข้างต้น

## การตรวจสอบข้ออ้างใน repository นี้

[`EVIDENCE.md`](EVIDENCE.md) แมปทุกข้ออ้างเกี่ยวกับโครงการนี้
ไปยังหลักฐานหรือคำสั่งที่ใช้ทำซ้ำผลนั้น และบันทึกสถานะ CI ตามความเป็นจริง
รวมถึงปัญหาที่ยังเปิดอยู่สองข้อ ซึ่งทำให้การรันบน Ubuntu CI ยังแดง
ทั้งที่ชุดทดสอบผ่านบนแพลตฟอร์มที่ใช้พัฒนา
