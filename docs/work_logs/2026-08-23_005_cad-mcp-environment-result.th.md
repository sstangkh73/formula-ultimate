# ผลงาน 005: สร้างสภาพแวดล้อม CAD และ MCP

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-23_005_cad-mcp-environment-result.md`

วันที่: 2026-08-23
สถานะ: เสร็จสมบูรณ์

## สรุป

สร้างและทดสอบ toolchain 3D local ชุดแรกของ Formula Ultimate สำเร็จดังนี้

- เปิด local MCP ที่ผู้ผลิตให้มาใน Autodesk Fusion และทำ Streamable HTTP
  initialize/list-tools handshake จริงสำเร็จ
- ติดตั้ง CadQuery กับ CadQuery contrib MCP ใน Python 3.12 environment
  ที่ Git ignore, pin source revision, แก้ dependency incompatibility
  ของ upstream และเรียก inspect/render ผ่าน protocol สำเร็จ
- พิสูจน์การสร้าง solid และส่งออก STEP แบบ headless ด้วย FreeCAD 1.1.3
  พร้อมหลักฐาน dimensions, volume, header, file size และ hash
- ตรวจ Blender 5.0.1 และยังไม่ต่อ official Blender Lab MCP เพราะ server
  อย่างเป็นทางการกำหนด Blender 5.1 ขึ้นไป
- เพิ่ม launcher, project MCP config, เอกสารใช้งานสองภาษา
  และแก้ขอบเขต repository contract ให้ไม่สแกน local tool tree ที่ ignore

ไม่มีการแก้ CAD document เดิม ไม่ได้เรียก mutation/execute tool ของ Fusion
และไม่มีการ upload หรือ share design

## ไฟล์ที่เปลี่ยน

### การตั้งค่า MCP และ environment

- `.codex/config.toml`: project definition แบบ optional และ approval-gated
  สำหรับ Fusion HTTP MCP กับ CadQuery STDIO MCP
- `.gitignore`: ignore `.tools/` และโฟลเดอร์
  `cadquery-contrib-master/` ที่ผู้ใช้แตกไว้
- `tools/cadquery-mcp-requirements.txt`: pin CadQuery MCP source commit,
  MCP major version และ pytest version

### เครื่องมือที่ทำซ้ำได้

- `scripts/bootstrap_cadquery_mcp.ps1`: bootstrap Python 3.12/uv ที่รันซ้ำได้
- `scripts/cadquery_mcp.ps1`: STDIO launcher ที่อ้าง path จากโปรเจกต์
- `scripts/cad/mcp_probe.py`: ทดสอบ initialization/tool inventory ผ่าน
  STDIO/Streamable HTTP และเก็บผล CadQuery inspect/SVG render
- `scripts/cad/freecad_smoke.py`: สร้าง solid และ STEP ชั่วคราวด้วย FreeCAD
- `scripts/freecad_smoke.ps1`: แก้ compatibility ของ Windows path
  และแสดง header/size/SHA-256

### เอกสารและการทดสอบ

- `docs/3d/CAD_MCP_ENVIRONMENT.md` และ `.th.md`: stack, คำสั่ง, หลักฐาน,
  ข้อจำกัด และ security boundary ที่ตรวจแล้ว
- แผน/ผล Work 005 ภาษาอังกฤษและไทย
- `tests/test_repository_contract.py`: ข้าม dependency tree ที่ ignore คือ
  `.tools` กับ `cadquery-contrib-master` แต่ยังตรวจเอกสารที่ repo ดูแลทั้งหมด

## การตัดสินใจสำคัญ

1. **ใช้ official Fusion server แทน community bridge** เพราะ Fusion ที่ติดตั้ง
   มี localhost MCP ของตัวเองและรายงาน tool group 4 กลุ่ม
2. **ใช้ CadQuery สำหรับ generation/inspection ที่ทำซ้ำได้** โดย pin source ที่
   `06b5e50a87fcf6808859f33d84e224fce675f8d7` ไม่ดึง moving branch ตอนรัน
3. **จำกัด `mcp` เป็น `>=1,<2`** เพราะ package upstream ระบุเพียง lower bound
   แต่ใช้ API ที่ถูกตัดใน MCP 2.0.0 ส่วน 1.29.0 ผ่าน upstream test ทั้งไฟล์
4. **เก็บ FreeCAD เป็น evaluator อิสระ** ไม่ติดตั้ง community MCP
   โดยไม่มี security review แยก
5. **ไม่ติดตั้ง Blender MCP บน Blender 5.0.1** เพราะ official Blender Lab
   ต้องใช้ 5.1+ และเตือนว่า generated Python ไม่มี guard
6. **ถือ approval prompt เป็นจุดตรวจ ไม่ใช่ isolation** เพราะ CadQuery
   ยังรับ arbitrary Python และ export path จากผู้เรียก

## หลักฐานการตรวจสอบ

### 1. Environment ที่ติดตั้ง

คำสั่ง: ตรวจ version จาก executable, `uv --version` และ Python package
metadata

สภาพแวดล้อม: Windows, PowerShell, Python 3.14 หลัก และ Python 3.12.14
ใน environment แยก

Exit code: 0

ผล:

```text
Fusion 2704.1.53
FreeCAD 1.1.3 Revision: 20260725 (Git shallow)
Blender 5.0.1
uv 0.12.5
Python 3.12.14
CadQuery 2.8.0
cadquery-mcp 0.1.0
mcp 1.29.0
```

### 2. Socket ของ Fusion server

คำสั่ง:

```powershell
Test-NetConnection -ComputerName 127.0.0.1 -Port 27182
```

Exit code: 0

ผล: `TcpTestSucceeded : True`

### 3. Fusion MCP protocol

คำสั่ง:

```powershell
.tools\cadquery-mcp\Scripts\python.exe scripts\cad\mcp_probe.py `
  --output artifacts\work005\fusion_mcp_probe.json `
  http --url http://127.0.0.1:27182/mcp
```

Exit code: 0

ผล:

```text
server_name: MCP Server Adapter
server_version: 1.0.0
tools: fusion_mcp_electronics_read, fusion_mcp_execute,
       fusion_mcp_read, fusion_mcp_update
```

### 4. CadQuery bootstrap

คำสั่ง:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File scripts\bootstrap_cadquery_mcp.ps1
```

Exit code: 0

ผล:

```text
Python 3.12 is already installed
Checked 77 packages
CadQuery 2.8.0
cadquery-mcp 0.1.0
mcp 1.29.0
```

### 5. Upstream test ของ CadQuery และ failure ของ dependency

environment แรก: `mcp 2.0.0`

คำสั่งแรก: upstream `test_cadquery_mcp_server.py`

Exit code แรก: 1

ผลแรก: `27 failed` โดย root exception คือ
`AttributeError: 'Server' object has no attribute 'list_tools'`

คำสั่งแก้:

```powershell
py -3.14 -m uv pip install `
  --python .tools\cadquery-mcp\Scripts\python.exe "mcp<2"
```

คำสั่งสุดท้าย:

```powershell
.tools\cadquery-mcp\Scripts\python.exe -m pytest -q `
  -p no:cacheprovider `
  cadquery-contrib-master\cadquery-contrib-master\mcp-server\test_cadquery_mcp_server.py
```

Exit code สุดท้าย: 0

ผลสุดท้าย: `27 passed, 1 warning in 2.76s` คำเตือนมาจาก CadQuery CQGI
ที่ยังใช้ `ast.NameConstant` ซึ่ง deprecated

### 6. CadQuery MCP inspect และ render

คำสั่ง:

```powershell
.tools\cadquery-mcp\Scripts\python.exe scripts\cad\mcp_probe.py `
  --output artifacts\work005\cadquery_mcp_probe.json `
  stdio --command .tools\cadquery-mcp\Scripts\cadquery-mcp.exe `
  --inspect-box --render-output artifacts\work005\cadquery_box.svg
```

Exit code: 0

ผล:

```text
tools: export, get_parameters, inspect, render
inspect_is_error: false
bounds_mm: 10 x 20 x 30
volume_mm3: 6000
surface_area_mm2: 2200
topology: 1 solid, 6 faces, 12 edges, 8 vertices
render_is_error: false
render_mime_type: image/svg+xml
render_bytes: 2420
render_sha256: CB69BA4DD6A23EE8653C1EF37E2BEFC4E55797CC6EC22ACAD0B1163E663A74CA
```

artifact หลักฐานถูก Git ignore ไว้ใต้ `artifacts/work005/` โดยเจตนา

### 7. FreeCAD STEP smoke test

คำสั่ง:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\freecad_smoke.ps1
```

Exit code: 0

ผลจาก final recorded run:

```text
bounds_mm: [10.0, 20.0, 30.0]
volume_mm3: 6000.0
solid_count: 1
STEP header: ISO-10303-21;
bytes: 6854
SHA256: 4C4182EA8152C9327CB9AF4A8AB20FC8FC4470D979380DC0D833EA8D2A5F39D1
```

การลองครั้งแรกที่ส่ง output path ซึ่งมี `C:\Formula Ultimate`
ไม่เกิด artifact เพราะ FreeCAD 1.1.3 แบ่ง path ตรงช่องว่าง
launcher ที่ commit ใช้ short path จาก filesystem และรอบถัดไปผ่าน

### 8. Repository tests

คำสั่ง:

```powershell
py -3.14 -m unittest discover -s tests -v
```

Exit code: 0

ผล: `Ran 14 tests ... OK`

รอบแรกมี bilingual subtest ล้ม 24 รายการ เพราะ test เข้าไปสแกน Markdown
ที่ติดตั้ง/แตกไว้ใน `.tools/` กับ CadQuery tree ซึ่ง Git ignore
จึงแก้ขอบเขตให้ข้ามสองโฟลเดอร์นั้น โดยยังตรวจ Markdown ที่ repo ดูแลทั้งหมด

### 9. Static/configuration checks

คำสั่ง:

```powershell
py -3.14 -m py_compile scripts\cad\mcp_probe.py scripts\cad\freecad_smoke.py
py -3.14 -c "import tomllib, pathlib; tomllib.loads(pathlib.Path('.codex/config.toml').read_text())"
git diff --check
```

Exit code: 0, 0, 0

ผล: compile Python สำเร็จ, TOML parse พบ server `cadquery,fusion`
และไม่พบ whitespace error

## ข้อสรุปที่หลักฐานรองรับ

- official local server ของ Fusion เปิดและตอบ MCP handshake
- CadQuery MCP 0.1.0 list tools, inspect geometry แบบกำหนดตายตัว และ render
  SVG ได้ใน environment ที่ pin
- FreeCAD สร้าง reference solid และส่งออก STEP exchange file ที่มี header
  ถูกต้องแบบ headless ได้บนเครื่องนี้
- repository มี project MCP definitions สำหรับ Codex task ใหม่ที่ trust แล้ว

## ข้อสรุปที่หลักฐานยังไม่รองรับ

- ไม่ได้ทดสอบ Fusion mutation/execute tool และไม่ได้สร้าง geometry ใน Fusion
- project MCP config ที่เพิ่งเขียนไม่ได้ hot-load ใน task ที่กำลังรันอยู่
  ส่วน packaged `codex mcp list` เปิดจาก PowerShell ไม่ได้เพราะ WindowsApps
  ตอบ `Access is denied` จึงใช้ direct protocol test แทน
- FreeCAD ยังไม่ได้ต่อ MCP
- Blender MCP ยังไม่ได้ติดตั้งหรือต่อ
- กล่องอ้างอิงยังไม่ใช่ชิ้นส่วนรถแข่งที่ validate แล้ว
- ยังไม่มี topology discovery, optimizer, CFD, FEA, vehicle dynamics,
  manufacturing หรือ safety validation
- approval prompt ไม่ได้ sandbox การรัน CadQuery หรือ Fusion

## สิ่งที่ต่างจากแผน

- ตรวจ Blender แล้วแต่ไม่เชื่อม เพราะ 5.0.1 ไม่ผ่านข้อกำหนด official 5.1+
- ยังไม่เลือก FreeCAD MCP bridge หลังพิสูจน์ headless automation ตามแผน
  เพราะ community bridge ยังต้องมี security review แยก
- เพิ่ม bootstrap script กับ requirements file เพื่อทำ installation ที่ pin
  ให้สร้างซ้ำได้

## ข้อจำกัดและงานถัดไป

CadQuery bridge ปัจจุบันเปิด arbitrary Python และ arbitrary export path
Work 006 ควรสร้าง constrained 3D component grammar ตัวแรก และวงจรหลักฐาน
CadQuery -> STEP -> FreeCAD -> Level 0 mass/volume จากนั้นค่อยทดสอบ Fusion
mutation ใน design ใหม่แบบใช้แล้วทิ้ง ส่วนการอัปเกรด Blender และตรวจ Lab MCP
ควรอยู่ใน work item แยกที่มีแผนก่อนเริ่ม
