# ผลงาน 004: วิจัย Engineering CAD ที่รองรับ MCP

วันที่: 2026-08-23
สถานะ: เสร็จสมบูรณ์

> ฉบับภาษาไทยของ `2026-08-23_004_mcp-cad-tooling-research-result.md`

## สรุป

จัดทำการประเมินซอฟต์แวร์สำหรับออกแบบชิ้นส่วนเครื่องกลอย่างละเอียดผ่าน MCP แบบ
สองภาษาและมี source link ครบ งานวิจัยแยก official vendor MCP ออกจาก Labs/
community bridge และแนะนำ multi-tool geometry pipeline สำหรับ Formula Ultimate
แทนการให้ CAD package เดียวเป็นทั้ง generator, evaluator และหลักฐานความถูกต้อง

## สิ่งส่งมอบ

- `docs/research/MCP_CAD_TOOLING_REPORT.md`
- `docs/research/MCP_CAD_TOOLING_REPORT.th.md`
- Plan/result Work 004 ภาษาอังกฤษและภาษาไทยแยกไฟล์

## เครื่องมือที่ประเมิน

- Autodesk Fusion
- Onshape / FeatureScript
- CadQuery
- FreeCAD
- Blender
- OpenSCAD
- SOLIDWORKS

## ผลค้นพบหลัก

1. Autodesk Fusion MCP เป็น official Autodesk General Availability local
   desktop integration แล้ว และเปิด dynamic tool สู่ live Fusion session
2. Onshape มี official Labs FeatureScript MCP สำหรับ agent-generated reusable
   parametric text-to-code-to-CAD feature
3. MCP ในโครงการ CadQuery contrib เป็นเส้นทางแรกที่แข็งแรงสุดสำหรับ deterministic,
   code-first, headless B-rep generation และ inspection
4. FreeCAD มี CAD/CAE/Python capability ทางการที่แข็งแรง แต่ MCP ที่ตรวจเป็น
   community project แยกกันและมี tool surface กระจัดกระจาย
5. Official Blender Lab MCP มีค่ากับ procedural morphology แต่หน้าโครงการเตือน
   ว่า generated code รันโดยไม่มี guard และ Blender mesh ไม่ถือเป็นหลักฐาน
   engineering
6. OpenSCAD เป็น deterministic baseline ที่มีประโยชน์ ส่วน SOLIDWORKS MCP ยัง
   เป็น licensed community-bridge path ไม่ใช่ตัวเลือกวิจัยแรก

## คำแนะนำ

ใช้ pipeline แบ่งชั้น:

```text
CadQuery MCP generation และ property gate
  -> Level-0 / 1D screening
  -> Autodesk Fusion official MCP promotion และ human review
  -> FreeCAD/project-owned bridge และ authoritative FEA/CFD/thermal validation
```

ทดลอง Onshape FeatureScript MCP เป็น reusable component-grammar path แล้วจึง
เพิ่ม Blender เป็น novelty branch ที่มี gate แยก หลัง B-rep pipeline เชื่อถือได้

## หลักฐานตรวจ Source

- บันทึกวันที่วิจัย: `2026-08-23`
- Unique primary/official source URL ในรายงานอังกฤษ: `24`
- Unique primary/official source URL ในรายงานไทย: `24`
- URL-set difference ระหว่างสองรายงาน: ไม่มี
- Claim ด้าน CAD capability อ้าง vendor/project documentation ทางการ
- Claim ด้าน community MCP link ไป primary project repository
- แยก official, Labs, community และ unverified/custom ชัดเจน

## หลักฐาน Repository Validation

คำสั่ง:

```powershell
python -m unittest discover -s tests -v
```

Environment: Windows, Python 3.14.3

Exit code: `0`

ผล:

```text
Ran 14 tests
OK
```

จำนวนเอกสารที่ดูแลหลังรวม result ทั้งสองไฟล์:

```text
English Markdown files: 18
Thai companion files:   18
Missing companions:      0
```

คำสั่งเพิ่มเติม:

```powershell
python -m compileall -q src tests
git diff --cached --check
```

Exit code ของแต่ละคำสั่ง: `0`

## ข้ออ้างที่มีหลักฐานรองรับ

- สถานะ official MCP ของ Fusion, Onshape Labs และ Blender Lab ณ วันที่วิจัย
- Geometry/API/export capability ที่เอกสารของเครื่องมือระบุ
- Tool surface ที่ primary community MCP repository อธิบาย
- คำแนะนำ toolchain ที่มีเหตุผลตามข้อกำหนด generation, validation,
  reproducibility และ security ของ Formula Ultimate

## หลักฐานที่ยังขาดและข้อจำกัด

- งานนี้ไม่ได้ติดตั้งหรือ live-test CAD/MCP ใด
- ยังไม่ได้บันทึก dynamic runtime tool inventory จาก Fusion ในเครื่องผู้ใช้
- ยังไม่ได้ทดสอบ Onshape Labs availability, account permission และ exact tool
  behavior ด้วย account ผู้ใช้
- Community MCP source และ dependency ยังไม่ผ่าน security audit
- ราคาและ feature availability อาจเปลี่ยนตาม region, plan และ release ในอนาคต
- คำแนะนำจึงอยู่ระดับ architecture ด้วยความมั่นใจปานกลาง การเลือก production
  ต้องผ่าน proof of concept ที่เสนอ

## สิ่งที่เบี่ยงเบนจากแผน

- ไม่มี ไม่มีการติดตั้ง เปลี่ยน account หรือซื้อบริการภายนอก

## งานถัดไปที่แนะนำ

เริ่ม work item สองภาษาชุดใหม่สำหรับติดตั้ง/PoC restricted CadQuery MCP geometry
gate ก่อนติดตั้งต้อง pin และ review revision ของ server exact พร้อมกำหนด sandbox,
candidate workspace และ component-interface schema
