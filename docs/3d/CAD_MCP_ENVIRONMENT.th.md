# สภาพแวดล้อม CAD และ MCP

ไฟล์ต้นฉบับภาษาอังกฤษ: `CAD_MCP_ENVIRONMENT.md`

วันที่ตรวจสอบ: 2026-08-23

## วัตถุประสงค์

สภาพแวดล้อมนี้เป็นชั้นวิจัย 3D ที่ใช้งานได้จริงชั้นแรกของ Formula Ultimate
โดยเปิดทางให้นักออกแบบเอเจนต์ทำงานแบบเสริมกันดังนี้

- Autodesk Fusion สำหรับ CAD แบบ parametric ที่มี design history ผ่าน local
  MCP อย่างเป็นทางการของ Autodesk
- CadQuery สำหรับการสร้างชิ้นงาน parametric จากโค้ด การตรวจรูปทรง การ render
  และการส่งออก neutral format ผ่าน MCP ชุมชนที่ pin revision แล้ว
- FreeCAD เป็นผู้สร้าง/ผู้ประเมิน STEP อิสระบนเครื่องผ่าน `FreeCADCmd`
- Blender เป็นทางสำหรับ morphology, mesh และ visualization ในอนาคต
  เมื่อเวอร์ชันที่ติดตั้งตรงตามข้อกำหนดของ Blender Lab MCP อย่างเป็นทางการ

การเชื่อมต่อสำเร็จไม่เท่ากับการตรวจสอบความถูกต้องทางวิศวกรรม
รูปทรงจากทุกเส้นทางยังต้องผ่านการตรวจ topology, หน่วย, manufacturability,
physics และ safety แบบอิสระในงานถัดไป

## สถานะที่ตรวจสอบแล้ว

| ระบบ | เวอร์ชันที่ตรวจแล้ว | บทบาท | สถานะ ณ 2026-08-23 |
|---|---:|---|---|
| Autodesk Fusion | 2704.1.53 | Interactive parametric CAD | เปิด official local MCP และผ่าน protocol handshake |
| CadQuery | 2.8.0 | Code-native parametric CAD | ติดตั้งใน environment แยก; ผ่าน MCP list, inspect และ render |
| CadQuery MCP | 0.1.0 ที่ `06b5e50a87fcf6808859f33d84e224fce675f8d7` | STDIO MCP bridge | เชื่อมใน project config; จำกัด `mcp` เป็น 1.29.0 |
| FreeCAD | 1.1.3 revision 20260725 | ตัวประเมิน STEP แบบ headless อิสระ | ส่งออก solid 10 x 20 x 30 mm สำเร็จ; ไม่ได้ติดตั้ง community MCP |
| Blender | 5.0.1 | Mesh/morphology/visualization | ติดตั้งแล้ว แต่ยังไม่เชื่อม official Blender Lab MCP เพราะต้องใช้ Blender 5.1+ |

endpoint และขั้นตอนเปิด Fusion ตรงกับ [Autodesk MCP Server
help](https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_FusionDesktopMcp_connecting_to_the_fusion_mcp_server_html)
ส่วนการตัดสินใจเรื่อง Blender ยึด [ข้อกำหนด Blender Lab MCP
อย่างเป็นทางการ](https://www.blender.org/lab/mcp-server/) ซึ่งเตือนด้วยว่า Python
ที่โมเดลสร้างจะถูกเรียกโดยไม่มี guard ป้องกัน

## การตั้งค่า MCP ของโปรเจกต์

ไฟล์ `.codex/config.toml` ที่อยู่ใน repository กำหนดว่า

- `fusion`: Streamable HTTP ที่ `http://127.0.0.1:27182/mcp`
- `cadquery`: STDIO ผ่าน `scripts/cadquery_mcp.ps1`
- ทั้งสอง server เป็น optional และตั้ง tool approval เป็น `prompt`

Codex รองรับ project-local MCP configuration รวมถึง local STDIO และ
Streamable HTTP ตาม [เอกสาร Codex MCP
อย่างเป็นทางการ](https://developers.openai.com/codex/mcp/)
project config ที่เพิ่มใหม่จะถูกอ่านโดย task ใหม่/ที่เปิดใหม่หลังจาก trust
โปรเจกต์แล้ว นอกจากนี้ Work 005 ยังทดสอบ protocol โดยตรง
จึงไม่ได้สรุปจาก connection badge ใน UI เท่านั้น

`prompt` เป็นจุดให้มนุษย์ตรวจอนุมัติ ไม่ใช่ security sandbox
และไม่ได้ทำให้ Python ที่สร้างโดยอัตโนมัติปลอดภัย

## การติดตั้ง CadQuery

environment อยู่ที่ `.tools/cadquery-mcp` และถูก ignore จาก Git
สร้างหรือซ่อม environment ด้วยคำสั่ง

```powershell
py -3.14 -m pip install --user uv
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\bootstrap_cadquery_mcp.ps1
```

bootstrap ใช้ Python 3.12 และไฟล์
`tools/cadquery-mcp-requirements.txt` โดย pin CadQuery contrib ที่ commit
`06b5e50a87fcf6808859f33d84e224fce675f8d7` และจำกัด `mcp` ไว้ที่ major
version 1 เพราะ CadQuery MCP 0.1.0 เข้ากันไม่ได้กับ `mcp` 2.0.0
รายละเอียด package และเครื่องมืออยู่ใน [CadQuery contrib MCP
README](https://github.com/CadQuery/cadquery-contrib/blob/master/mcp-server/README.md)

ทดสอบโดยไม่แก้เอกสาร CAD เดิมด้วย

```powershell
$py = (Resolve-Path .tools\cadquery-mcp\Scripts\python.exe).Path
$server = (Resolve-Path .tools\cadquery-mcp\Scripts\cadquery-mcp.exe).Path
& $py scripts\cad\mcp_probe.py `
  --output artifacts\work005\cadquery_mcp_probe.json `
  stdio --command $server --inspect-box `
  --render-output artifacts\work005\cadquery_box.svg
```

probe สร้างกล่อง 10 x 20 x 30 mm แบบกำหนดตายตัว ผลวันที่ 2026-08-23 คือ
volume 6000 mm3, surface area 2200 mm2, 1 solid, 6 faces, 12 edges, 8 vertices
และตอบ SVG โดย `render_is_error=false`

## การทดสอบ Fusion

ต้องเปิด Fusion ค้างไว้และเปิด **Preferences > General > API > Fusion MCP
Server** จากนั้นทดสอบ endpoint โดยไม่เรียก mutation tool ด้วย

```powershell
$py = (Resolve-Path .tools\cadquery-mcp\Scripts\python.exe).Path
& $py scripts\cad\mcp_probe.py `
  --output artifacts\work005\fusion_mcp_probe.json `
  http --url http://127.0.0.1:27182/mcp
```

tool inventory ที่ตรวจพบคือ

- `fusion_mcp_read`
- `fusion_mcp_update`
- `fusion_mcp_execute`
- `fusion_mcp_electronics_read`

Work 005 ทำเพียง initialization และ tool discovery โดยเจตนา
ไม่ได้เรียก mutation/execute tool ของ Fusion และไม่ได้สร้าง cloud document

## การตรวจ FreeCAD แบบ Headless

ใช้คำสั่ง

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\freecad_smoke.ps1
```

launcher สร้าง artifact ที่ถูก ignore ใต้ `artifacts/work005/` ตรวจ header STEP
`ISO-10303-21;` และแสดง dimensions, volume, byte size กับ SHA-256
FreeCAD 1.1.3 บน Windows เครื่องนี้แยก CLI path ที่มีช่องว่างผิด
launcher จึงใช้ 8.3 alias ที่ filesystem ให้มาสำหรับ script และ output
ชั่วคราว

ปัจจุบัน FreeCAD เป็นตัวประเมิน headless อิสระ ไม่ใช่ authoring surface
ที่ต่อ MCP และไม่ได้ติดตั้ง FreeCAD community MCP ที่ยังไม่ผ่านการตรวจ

## ขอบเขตความปลอดภัย

เครื่องมือทั้ง 4 ของ CadQuery MCP รับ Python จากเอเจนต์แล้วประมวลผลผ่าน
CadQuery CQGI ส่วน export tool รับ filename จากผู้เรียกโดยตรง
bridge ปัจจุบันจึงมีความเสี่ยงด้าน arbitrary code และ arbitrary path
ภายใต้สิทธิ์ของบัญชีผู้ใช้ การควบคุมที่ Work 005 ทำไว้มีเพียง

- Python environment แยก
- pin source revision และ MCP major version
- launcher/config ระดับโปรเจกต์
- approval prompt
- geometry ทดสอบแบบใช้แล้วทิ้งและ artifact path ที่ Git ignore
- ไม่มี credential ใน config

สิ่งเหล่านี้ช่วยด้าน auditability แต่ยังไม่แยก process, filesystem หรือ
network ก่อนจะมี constrained structured design service ต้องตรวจทุก generated
script และ export path ก่อนอนุมัติ และห้ามเปิด server นี้ให้ prompt
ที่ไม่น่าเชื่อถือหรือ repository อื่น

Fusion update/execute tool ก็ต้องตรวจเพราะแก้ active document ได้
Blender Lab มีคำเตือนลักษณะเดียวกันสำหรับ generated Python
จึงยังไม่เชื่อม Blender ใน environment นี้

## งานถัดไปที่แนะนำ

Work 006 ควรกำหนดการทดลอง 3D แบบมีขอบเขตครั้งแรก
แทนการเปิดให้รัน Python อย่างอิสระทันที

1. กำหนด component/design grammar แบบ typed ขนาดเล็กพร้อมหน่วย
2. สร้าง reference part แบบ parameterized ผ่าน CadQuery
3. ส่งออก STEP แล้วให้ FreeCAD ตรวจแบบอิสระ
4. เปรียบเทียบ mass/volume กับ Level 0 physics kernel
5. เก็บ design genome, tool calls, geometry hashes และผล evaluator
6. จากนั้นจึงทดสอบ Fusion mutation บน design ใหม่แบบใช้แล้วทิ้ง
7. อัปเกรด Blender เป็น 5.1+ และตรวจ official Lab bridge ใน work item
   ที่มีแผนแยกก่อนเปิดใช้งาน
