# ผล Work 007: ทิศทางวิจัยหลักใน README

สถานะ: Completed

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-25_007_main-research-direction-result.md`

## ผลลัพธ์

README ภาษาอังกฤษและไทยแสดงทิศทาง Formula Ultimate ที่ผู้ใช้ยืนยันเป็น framing
หลักที่จุดเข้า repository แล้ว:

- ในอนาคตเอเจนต์อัตโนมัติออกแบบรถแข่ง 3D ได้ทั้งคัน ตั้งแต่สถาปัตยกรรมระดับรถ
  จนถึง geometry ภายในชิ้นส่วนที่ไม่เคยมีมาก่อน;
- ไม่กำหนด conventional vehicle layout, dimension, powertrain, การจัดวางล้อ,
  รูปทรงตัวถัง และรูปทรงชิ้นส่วนที่รู้จัก เพียงเพราะแนวปฏิบัติรถแข่งในอดีตใช้มัน;
- ฟิสิกส์ race/energy contract ที่อ้างอิง Formula One และมี version, ทรัพยากร
  finite, ความปลอดภัย และหลักฐานยังเป็น hard boundary ที่ประกาศ;
- primary propulsion energy ทั้งหมดอยู่บนรถก่อนแข่งและห้ามเติม primary energy
  ระหว่างแข่ง;
- การทดลองข้ามสถาปัตยกรรมที่ยุติธรรมต้องมี equivalent energy profile แบบ
  technology-neutral แทนการให้สถาปัตยกรรม ICE/ERS ของ FIA ปัจจุบันได้เปรียบ
  แบบเงียบ;
- geometry 3D ทั้งคันเป็น causal physics input ที่ independent evaluator
  ใช้สร้างหลักฐานทางฟิสิกส์;
- objective คือเวลาแข่งขันรวมต่ำสุดในกลุ่ม candidate ที่แข่งจบและผ่าน fidelity
  gate ที่ต้องใช้;
- ข้ออ้าง novelty และ discovery ต้องมี baseline ที่ยุติธรรม การพยายามหักล้าง
  replay evidence และการอยู่รอดที่ fidelity สูงขึ้น

README ยังคงระบุว่า Phase 1 ตั้งใจแคบ และ Level 0 กับวงจร component Work 006
ที่มีอยู่ยังไม่ validate รถแข่งทางฟิสิกส์

## ไฟล์ที่เปลี่ยน

- `README.md`
  - เพิ่ม long-term mission และ primary research question;
  - นิยาม total-race-time objective และ hard constraint;
  - บันทึก race/energy contract ที่อ้างอิง Formula One พร้อมแหล่ง FIA 2026
    ทางการ;
  - นิยาม technology-neutral energy equivalence สำหรับงานวิจัย powertrain
    แบบเปิด;
  - นิยาม open 3D design domain, independent evidence loop, discovery standard,
    current implementation status และ claim boundary;
  - เพิ่ม `docs/3d/` ใน repository map
- `README.th.md`
  - สะท้อนโครงสร้าง identifier, equation, rule reference, date, link, claim
    และ limitation ของภาษาอังกฤษเป็นภาษาไทย;
  - ยังคงระบุ `README.md` เป็น English source
- plan และ result record Work 007 ที่ตรงกัน แยกภาษาอังกฤษและไทย
- `C:\Users\sstan\.codex\memories\extensions\ad_hoc\notes\2026-08-25T23-00-50-formula-ultimate-main-direction.md`
  - บันทึกทิศทางที่ผู้ใช้ยืนยันสำหรับ session ต่อไป โดยไม่แก้ managed memory
    registry โดยตรง

ไม่แก้ simulator, CAD, physics, optimization หรือ experiment configuration
การเปลี่ยน Work 006 ที่ยังไม่ commit ถูกเก็บไว้และไม่รวมเข้า Work 007

## การตัดสินใจ

1. **นิยาม openness เป็นอิสระด้านสถาปัตยกรรมภายในข้อจำกัด explicit** README
   ไม่เขียนว่า “ไม่มีข้อจำกัด” แต่เขียนว่าไม่มี conventional architecture
   ที่กำหนดล่วงหน้า นอกเหนือจาก physics, race, energy, resource, safety และ
   evidence constraint ที่ประกาศ
2. **รับหลักการ race-energy ของ F1 ไม่ใช่รูปทรง power-unit ปัจจุบันทุกข้อ**
   README อ้าง FIA 2026 Sporting Regulation B5.1.4 และ Technical Regulation
   C6.4.4 สำหรับ boundary ห้ามเติมเชื้อเพลิงระหว่างแข่ง ทุก experiment ต้อง pin
   regulatory profile
3. **บังคับการเปรียบเทียบ energy-equivalent** Store และ carrier ทางเลือกได้รับ
   initial primary-energy opportunity ที่ประกาศเท่ากัน เว้นแต่ energy budget
   เป็น independent variable ที่ประกาศล่วงหน้า Recovery ยอมรับได้เฉพาะผ่าน
   physical flow ที่ conserve และตรวจย้อนกลับได้
4. **ทำให้ geometry 3D เป็น causal** Geometry กำหนด mass, volume, centre of
   mass, inertia, packaging, collision, structural, thermal, flow,
   electromagnetic และ aerodynamic evidence การ render หรือ generator claim
   ไม่เพียงพอ
5. **ใช้ total race time หลัง feasibility gate** Peak speed, การวิ่งไม่จบ
   และ numerical exploit ชนะ objective ไม่ได้
6. **แยก generated, simulation-valid, promoted, physically validated และ
   discovered** Novel fastener ทำได้ แต่ความใหม่ยังไม่เป็น research discovery
   จนกว่าจะผ่านการเปรียบเทียบยุติธรรมและหลักฐานที่แข็งแรงขึ้น
7. **รักษาความตรงของ current capability** ทิศทางสูงสุดเด่นชัดแล้ว ขณะเดียวกัน
   ยังระบุขอบเขต Phase 1 และ Level-0/Work-006 ปัจจุบันอย่างชัดเจน

## หลักฐานกติกาทางการ

- [2026 FIA Formula One Sporting Regulations, Section B, Issue
  08](https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_b_sporting_-_iss_08_-_2026-08-05_7.pdf)
  เผยแพร่ 5 สิงหาคม 2026: B5.1.4 ห้ามเพิ่มหรือนำเชื้อเพลิงออกตั้งแต่ boundary
  reconnaissance lap จน end-of-session signal
- [2026 FIA Formula One Technical Regulations, Section C, Issue
  20](https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_c_technical_-_iss_20_-_2026-08-05.pdf)
  เผยแพร่ 5 สิงหาคม 2026: C6.4.4 ห้ามเพิ่มหรือนำเชื้อเพลิงออกระหว่าง Race

แหล่งเหล่านี้ถูกระบุ version ไม่ได้ถือว่าเป็นกฎถาวร Formula Ultimate ต้องเลือก
อัปเดตหรือคง pinned profile อย่างชัดเจนเมื่อกติกา FIA เปลี่ยน

## การตรวจสอบ

คำสั่ง:

```powershell
py -3.14 -m unittest discover -s tests -v
py -3.14 -m compileall -q src scripts tests
git diff --check
rg -n "Primary Research Question|คำถามวิจัยหลัก|B5\.1\.4|C6\.4\.4|external primary-energy|3D|Level 0|Level-0|physical validation|technology-discovery" README.md README.th.md
```

Exit status: `0` ทุกคำสั่งตรวจสอบ

Output ที่เกี่ยวข้อง:

```text
Ran 32 tests in 0.670s
OK
```

`compileall` และ `git diff --check` ไม่มี error Git แสดงเพียง Windows line-ending
warning สำหรับไฟล์ที่แก้ Focused README search พบ research question, equivalent
energy constraint, FIA article, ข้อกำหนดหลักฐาน 3D, discovery standard และ
Level-0 non-claim ในทั้งสองภาษา

Artifact hash หลัง validation:

| Artifact | SHA-256 |
|---|---|
| `README.md` | `80D9D0977704179F1945C5D19F7CA443D46B0FFA90614F2EF11CB11CF91055B1` |
| `README.th.md` | `443B01CEBB6B585A1A038901A9340210532B9852F81785739AAD108CE46B3D7E` |
| ad-hoc memory note | `A874933F95701D062E35FAD920244C5B0E4DB342895055A86F42F6103C81C9BD` |

## ข้อจำกัด

- README เป็นทิศทางและ research contract ไม่ใช่ implementation claim
- ยังไม่กำหนดตัวเลข race-energy budget แบบ technology-neutral ต้องทำเป็น
  experiment/configuration work item แยก
- Research charter และ design-language boundary ปัจจุบันยังอธิบาย staged plan
  ที่แคบกว่า ทั้งสองไม่ขัดแย้ง แต่ consistency work item ภายหลังควรกระจาย
  top-level framing ใหม่โดยไม่ปิดบัง Phase-1 control
- ไม่รับ current FIA architecture-specific power, state-of-charge หรือ per-lap
  recovery limit ทุกข้อโดยอัตโนมัติ
- ไม่เพิ่ม physical, empirical, FEA, CFD, manufacturability หรือ safety
  validation

## งานต่อไป

1. นิยามและให้เหตุผลกับ energy profile
   `FORMULA_ULTIMATE_EQUIVALENT_2026` ที่มี version ในหน่วย SI รวม initial
   primary-energy accounting, recovery ที่อนุญาต, external inflow ที่ห้าม,
   uncertainty และ cross-carrier equivalence
2. กระจาย main framing นี้เข้า research charter และ design-language boundary
   เป็น bilingual consistency work item แยก
3. กำหนด complete-vehicle 3D representation และ closure rule เพื่อให้ mass,
   volume, interface และ energy path ทุกส่วนถูก account ทางฟิสิกส์
4. รักษา fixed-topology baseline ของ Phase 1 และระเบียบ equal-budget comparison
   ปัจจุบันขณะขยาย fidelity ภายหลัง
