# รายงานเครื่องมือ Engineering CAD ที่รองรับ MCP

วันที่วิจัย: 2026-08-23

> ฉบับภาษาไทยของ `MCP_CAD_TOOLING_REPORT.md`

## ข้อสรุปสำหรับตัดสินใจ

Formula Ultimate ไม่ควรเลือกโปรแกรมเดียวให้ทำทั้ง open-ended geometric search
และ authoritative engineering review สถาปัตยกรรมที่แข็งแรงที่สุดในปัจจุบันคือ
pipeline สอง engine:

1. **CadQuery + CadQuery MCP** สำหรับสร้าง B-rep แบบ code-first, deterministic,
   headless และคัดกรอง candidate จำนวนมาก
2. **Autodesk Fusion + official Fusion MCP Server** สำหรับ detailed mechanical
   CAD แบบ interactive, human review, assembly, manufacturing handoff และงาน
   high-fidelity บางส่วน

**Onshape + official Onshape Labs FeatureScript MCP Server** เป็นทางเลือก
cloud-native ที่แข็งแรงที่สุด และอาจกลายเป็นระบบ parametric แบบ agent-native
ระยะยาวที่ดีที่สุด โดยเฉพาะการสร้าง reusable component generator แต่ปัจจุบัน
ยังเป็น early-access ของ Onshape Labs ขณะที่ Autodesk ระบุ Fusion MCP เป็น
General Availability

FreeCAD เป็นเส้นทาง independent CAD/CAE แบบ open-source ที่เหมาะที่สุด แต่ MCP
server ยังเป็น community project ไม่ใช่ official FreeCAD integration Blender
มีคุณค่ากับ morphology, lattice, procedural mesh และ visual inspection แต่ไม่ควร
เป็น source of truth ของ precision mechanical solid ส่วน OpenSCAD เหมาะกับ
deterministic demo ขนาดเล็ก แต่จำกัดเกินไปสำหรับ geometry engine สุดท้าย

## “การออกแบบชิ้นส่วนอย่างละเอียด” ต้องมีอะไร

การเชื่อม MCP เพียงอย่างเดียวไม่พอ เครื่องมือที่น่าเชื่อถือต้องรองรับส่วนใหญ่ของ:

- exact solid หรือ B-rep ไม่ใช่ triangle mesh เพียงอย่างเดียว
- parametric dimension และ design intent ที่เสถียร
- sketch, constraint, boolean, fillet, chamfer, loft และ sweep
- assembly หรือ component interface ที่ชัดเจน
- material assignment และ mass/volume/inertia ที่คำนวณอย่างอิสระ
- neutral export เช่น STEP และ BREP
- deterministic regeneration และ source/history ที่ตรวจได้
- batch/headless operation สำหรับ search
- เส้นทางอิสระไป FEA, CFD, thermal หรือ manufacturing validation
- bounded MCP tool, artifact isolation และ tool-call log ที่ทำซ้ำได้

## ตารางเปรียบเทียบ

| เครื่องมือ | ความลึก geometry/design | สถานะ MCP ณ วันที่วิจัย | ความเหมาะกับ headless/search | ข้อจำกัดหลัก | บทบาทใน Formula Ultimate |
|---|---|---|---|---|---|
| Autodesk Fusion | Professional parametric/direct/surface/mesh CAD, assembly, CAM/CAE | **Official Autodesk, GA**, local dynamic MCP | ต่ำ–ปานกลาง; live desktop session | Proprietary, session-based, ไม่เหมาะกับ 100k candidate โดยธรรมชาติ | Authoritative interactive CAD และ manufacturing review |
| Onshape | Professional cloud parametric CAD, FeatureScript, assembly/PDM | **Official Onshape Labs**, early access | ปานกลาง–สูงผ่าน FeatureScript/API | Cloud/IP boundary, Labs feature, license tier | Agent-authored reusable feature และ cloud collaboration |
| CadQuery | OCCT B-rep, Python parametric part, constrained assembly | MCP ใน `CadQuery/cadquery-contrib` ไม่ใช่ vendor service | **สูง** | GUI/drawing/CAE workflow ยังไม่ครบแบบ professional suite | Code-first geometry generator หลัก |
| FreeCAD | Full-precision OCCT B-rep/NURBS, parametric CAD, assembly, drawing, FEM/CAM | Community MCP; ยังไม่พบ official FreeCAD MCP | ปานกลาง–สูงผ่าน Python/headless | MCP แตกหลายโครงการและ maturity ต่างกัน | Open-source independent CAD/CAE evaluator |
| Blender | Mesh/curve/procedural Geometry Nodes, sculpt/render | Official Blender Lab MCP และมี community alternative | สูงสำหรับ procedural mesh/render | ไม่ใช่ precision mechanical B-rep/constraint system | Morphology exploration และ visualization |
| OpenSCAD | Deterministic constructive solid geometry script | Community MCP | สูง | เน้น mesh export, assembly/surface อ่อน, MCP ที่ตรวจไม่ export STEP native | Baseline ขนาดเล็กและ simple parametric fixture |
| SOLIDWORKS | Professional mechanical CAD, assembly, drawing | Community MCP bridge ไม่ได้รับรองโดย vendor | ต่ำ–ปานกลาง, Windows desktop | Licensed proprietary CAD และ community bridge | ใช้เมื่อมี licensed workflow เดิมเท่านั้น |

## ผลการตรวจโดยละเอียด

### 1. Autodesk Fusion — official local MCP ที่ดีที่สุดสำหรับ detailed interactive CAD

Autodesk ระบุ **Autodesk Fusion MCP Server เป็น General Availability** แล้ว
Server ทำงาน local ภายใน Fusion desktop session ที่เปิดอยู่ เปิด dynamic tool
ให้ MCP client ทำ real-time modeling และ command operation และไม่รับ remote
connection หรือ authentication ต้องเปิด Fusion ค้างและ enable ที่
`Preferences > General > API`; endpoint เริ่มต้นคือ
`http://127.0.0.1:27182/mcp`
([Autodesk MCP catalog](https://help.autodesk.com/view/ADSKMCP/ENU/),
[เอกสาร Fusion MCP](https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_FusionDesktopMcp_autodesk_fusion_mcp_server_html),
[คู่มือเชื่อมต่อ](https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_FusionDesktopMcp_connecting_to_the_fusion_mcp_server_html))

Fusion รองรับ constrained sketch, history-based parametric feature, direct
editing, surface, mesh, freeform T-spline, sheet metal, assembly, rendering และ
integrated manufacturing workflow
([รายการ feature ทางการของ Fusion](https://www.autodesk.com/products/fusion-360/features))

เหตุผลที่เหมาะกับ Formula Ultimate:

- เป็นตัวเลือก “เชื่อม agent กับ professional CAD ได้จริงตอนนี้” ที่แข็งแรงสุด
- Agent ทำงานใน live model ขณะที่มนุษย์ดูและ review การเปลี่ยนแปลงได้
- Native part/assembly history มีประโยชน์ต่อ engineering review มากกว่า final
  mesh เพียงอย่างเดียว
- ใช้เป็น promotion environment หลัง candidate ผ่าน cheap headless screening

เหตุผลที่ไม่ควรเป็น search engine เพียงตัวเดียว:

- MCP เป็น session-based และ tool surface ถูก discover แบบ dynamic
- ต้องเปิด Fusion บน desktop หนึ่งเครื่อง จึงไม่เหมาะกับ massive parallel evolution
- Native file และ advanced simulation/generative บางส่วนพึ่ง license และ cloud
- Local MCP endpoint ไม่มี authentication เพราะเป็น local-only แต่ยังต้องควบคุม
  permission ของ MCP client และแยก workstation

ด้าน license: Autodesk ระบุว่านักเรียนและอาจารย์ที่เข้าเกณฑ์ใช้ educational
access ได้ ส่วน personal-use จำกัดงาน non-commercial ที่เข้าเงื่อนไข Generative
Design ใช้ entitlement, extension หรือ token เฉพาะ จึงต้องตรวจสิทธิ์แยก
([เงื่อนไข Fusion ฟรี](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Do-I-qualify-for-free-use-of-Fusion-360.html),
[Generative Design overview](https://help.autodesk.com/view/fusion360/ENU/?contextId=GD-F360-GENERATIVE-DESIGN))

ข้อสรุป: **แนะนำเป็น engineering CAD ที่เชื่อม official MCP ตัวแรกและเป็น
human-review environment แต่ไม่ใช้เป็น high-volume evolutionary backend**

### 2. Onshape FeatureScript MCP — official agent-native parametric path ที่ดีที่สุด

Onshape เปิดตัว **FeatureScript MCP Server อย่างเป็นทางการผ่าน Onshape Labs**
โดยเชื่อม MCP client กับภาษา FeatureScript native ให้ agent generate, insert,
run, evaluate และ revise reusable parametric custom feature Onshape เรียกแนวทางนี้
ว่า text-to-code-to-CAD ไม่ใช่การสร้าง mesh ครั้งเดียว ปัจจุบันยังเป็น Labs
early-access
([ประกาศจาก Onshape](https://www.onshape.com/en/blog/featurescript-mcp-server-enables-text-code-cad))

FeatureScript คือภาษา parametric เดียวกับที่อยู่ใต้ Part Studio feature มี type
สำหรับคณิตศาสตร์ 3D, robust geometric reference, standard feature library และ
หลัก determinism ที่ระบุว่า model ต้อง regenerate เหมือนเดิมทุกครั้ง โดยไม่พึ่ง
เวลาและ randomness ภายนอก
([FeatureScript introduction](https://cad.onshape.com/FsDoc/index.html),
[language model และ determinism](https://cad.onshape.com/FsDoc/intro.html))

สิ่งนี้ตรงกับ Formula Ultimate มากเป็นพิเศษ:

- Agent สร้างโปรแกรม generate geometry ที่ใช้ซ้ำได้ ไม่ใช่ final artifact เท่านั้น
- FeatureScript parameter แสดง interface port, keep-out region, manufacturing
  limit และ component family ได้
- Onshape มี version history, branch, sharing, part, assembly และ neutral export
  รวม STEP/STEP AP242
  ([format export ของ Onshape](https://www.onshape.com/en/resource-center/tech-tips/how-to-import-and-export-with-onshape))

ขอบเขตสำคัญ:

- Official Labs MCP เน้น FeatureScript ห้ามสรุปเองว่าเปิดทุก assembly, drawing,
  simulation หรือ PDM operation
- เป็น cloud-native จึงต้อง review IP, account permission, network dependency
  และค่าใช้จ่าย bulk evaluation
- สถานะ Labs หมายความว่า service และ tool surface อาจเปลี่ยน
- ยังต้องมี engineering review โดย Onshape เองก็ระบุข้อจำกัดนี้

ด้านราคา/ความเป็นส่วนตัว: Onshape Free เก็บ document เป็น public และใช้แบบ
non-commercial ส่วน Student plan ฟรีมี professional modeling, assembly,
drawing, data management และ collaboration แต่ไม่รวม simulation feature ทุกแบบ
ของ educator/professional ปัจจุบัน private plan แสดงราคา Standard USD 1,500/
user/year และ Professional USD 2,500/user/year
([ราคา Onshape](https://www.onshape.com/en/pricing),
[แผนการศึกษา](https://www.onshape.com/en/education/plans))

ข้อสรุป: **แนะนำเป็น proof of concept ลำดับสอง และอาจเป็น component-grammar
system ระยะยาวที่ดีที่สุด หาก Labs เสถียรและผ่านนโยบาย IP**

### 3. CadQuery MCP — engine แรกที่ดีที่สุดสำหรับ automated search ที่ทำซ้ำได้

CadQuery คือ Python parametric CAD framework บน Open CASCADE/OCCT และใช้ B-rep
solid รองรับ constrained assembly และ STEP assembly export
([แนวคิด CadQuery](https://cadquery.readthedocs.io/en/stable/primer.html),
[assembly constraint](https://cadquery.readthedocs.io/en/latest/assy.html),
[STEP export](https://cadquery.readthedocs.io/en/latest/importexport.html))

Repository `CadQuery/cadquery-contrib` มี CadQuery MCP server ซึ่ง execute
CadQuery script, render หลายมุม, inspect bounding box, volume, surface area,
center of mass และ topology count, ดึง script parameter และ export STEP, STL,
SVG, DXF, AMF, 3MF, VRML และ BREP
([CadQuery MCP repository ต้นทาง](https://github.com/CadQuery/cadquery-contrib/tree/master/mcp-server))

เหตุผลที่ควรเป็นจุดเริ่ม Formula Ultimate:

- Geometry เป็น code ทำให้ candidate ทุกตัวมี genotype ที่ diff และ hash ได้
- รันโดยไม่ต้องมี interactive CAD session ขนาดใหญ่ และวางใน worker/container ได้
- B-rep และ STEP รักษาเส้นทาง engineering solid ไม่ยุบเป็น triangle ทันที
- MCP มี property inspection และ neutral export ที่ early trusted-evaluator ต้องใช้
- Python เชื่อมกับ simulator, telemetry, optimizer และ test เดิมโดยตรง

ข้อจำกัดและความเสี่ยง:

- MCP execute Python/CadQuery ที่ generate จึงต้องอยู่ใน sandbox, bounded
  workspace, resource limit และปิด secret/network เป็นค่าเริ่มต้น
- CadQuery เป็น code-first ไม่ใช่ professional drawing/CAM/CAE desktop ครบชุด
- OCCT operation อาจ fail กับ pathological fillet, feature เล็ก หรือ invalid
  topology ต้องบันทึก failure rate เป็น research telemetry ห้าม retry เงียบ
- Render preview ไม่ได้พิสูจน์ว่า solid valid หรือผลิตได้

ข้อสรุป: **แนะนำเป็น Phase A: MCP geometry generator และ batch screening engine ตัวแรก**

### 4. FreeCAD + community MCP — open-source independent evaluator ที่ดีที่สุด

FreeCAD รองรับ full-precision solid ด้วย Open CASCADE, B-rep/NURBS, parametric
object, constrained sketch, assembly, Python automation, STEP/IGES/STL export,
drawing, FEM, CAM และ engineering workbench อื่นอย่างเป็นทางการ
([ความสามารถ FreeCAD ทางการ](https://www.freecad.org/features.php?lang=eng_EN))
FreeCAD ใช้ LGPL2+ และใช้ application กับ design ที่สร้างได้ทั้ง commercial และ
non-commercial
([license FreeCAD](https://www.freecad.org/contributing.php?lang=eng))

มี community MCP หลายตัว ตัวอย่างสาย engineering จาก TESSA Labs เปิด
parametric creation, material/mass property, design sweep, STEP export, drawing,
defeaturing, meshing, boundary tagging และ handoff ไป Elmer/CalculiX/OpenFOAM
แต่เป็นโปรเจกต์อิสระขนาดเล็กภายใต้ MIT ไม่ใช่ official FreeCAD integration
([TESSA Labs FreeCAD MCP](https://github.com/tessalabs-space/freecad-mcp))

บทบาทใน Formula Ultimate:

- re-open/recompute/check STEP หรือ FCStd artifact อย่างอิสระ
- implementation ที่สองบน OCCT สำหรับจับ inconsistency ใน pipeline
- open-source meshing และ CAE preparation
- local workflow เมื่อรับ cloud CAD ไม่ได้

ปัญหาหลักคือไม่มี canonical FreeCAD MCP ตัวเดียว Server ต่าง ๆ มี tool set และ
bridge architecture ต่างกัน การเลือกต้อง source review, pin revision, รัน live
acceptance test กับ FreeCAD version exact และอาจควรสร้าง MCP surface ขนาดเล็ก
ที่โปรเจกต์เป็นเจ้าของเอง

ข้อสรุป: **แนะนำเป็น independent open-source evaluator และ project-owned bridge
ในอนาคต ไม่ใช้ generation server ที่ยังไม่ review เป็นตัวแรก**

### 5. Blender MCP — ดีมากสำหรับ exploration แต่ไม่ใช่ engineering authority

Blender มี official Blender Lab MCP server สำหรับ Blender 5.1+ แล้ว เปิด natural
language access สู่ Python API แต่ Blender เตือนชัดว่า generated code ถูก execute
โดยไม่มี guard และแนะนำ virtual machine หรือเครื่องที่ไม่มีข้อมูลสำคัญ
([หน้า official Blender Lab MCP](https://www.blender.org/lab/mcp-server/))

Procedural Geometry Nodes และ Python API เหมาะกับ:

- morphology แปลก รูปทรง organic/exotic
- lattice, field, duct, surface texture และ mesh experiment
- visual rendering และ human inspection
- geometry ที่ sketch/extrude CAD grammar แสดงออกยาก

Community fork หนึ่งมี structured Geometry Nodes patch แบบ revisioned พร้อม
dry-run และ actual-diff ซึ่งปลอดภัยเชิงแนวคิดกว่า arbitrary `bpy` execution แต่
ยังต้อง review source ของ third party
([structured Blender MCP Geometry Nodes](https://github.com/newo-ether/blender-mcp/blob/main/docs/geometry-nodes.md))

ข้ออนุมาน: workflow Blender ที่ตรวจเป็น mesh/Geometry-Nodes based จึงไม่ควรเป็น
authoritative source ของ exact B-rep feature, engineering sketch, tolerance หรือ
manufacturing drawing Geometry ที่สร้างต้องผ่าน manifold/solid check,
dimensional extraction, material assignment, mesh convergence และ independent
FEA/CFD ก่อนเข้า fitness

ข้อสรุป: **เพิ่มหลัง B-rep pipeline ทำงาน ใช้เป็น novelty branch และ visualizer
ไม่ใช้เป็น CAD truth เพียงตัวเดียว**

### 6. OpenSCAD MCP — deterministic baseline ที่ง่ายที่สุด

Community OpenSCAD MCP ตรวจ `.scad`, render หลายมุม, วิเคราะห์ dimension/
triangle count, จัดการ project file และ export STL, 3MF, AMF, OFF, DXF หรือ SVG
ได้ Server ที่ตรวจไม่ระบุ STEP/B-rep export
([OpenSCAD MCP repository](https://github.com/quellant/openscad-mcp),
[official OpenSCAD CLI](https://files.openscad.org/documentation/manual/Using_OpenSCAD_in_a_command_line_environment.html))

OpenSCAD เหมาะกับ MCP smoke test หนึ่งวัน เพราะ source เป็น text deterministic
และ parameter sweep ง่าย แต่ไม่เหมาะกับ advanced surface, robust feature history,
constrained assembly หรือ detailed manufacturing handoff

ข้อสรุป: **ใช้เป็น minimal baseline หรือ fixture generator ได้ แต่ CadQuery เหนือกว่า
สำหรับ engineering path หลัก**

### 7. SOLIDWORKS community MCP — ความสามารถสูงแต่ไม่ควรเริ่มก่อน

SOLIDWORKS เป็น mechanical CAD เชิงลึก และมี community MCP bridge ที่เปิด part,
assembly, configuration, drawing, inspection, verification และ automation plan
ผ่าน Windows COM หรือ optional in-process add-in โปรเจกต์ที่ตรวจระบุชัดว่าเป็น
อิสระ ไม่ได้รับรองโดย Dassault Systèmes/SOLIDWORKS และต้องมี Windows กับ licensed
installation
([ตัวอย่าง SOLIDWORKS MCP](https://github.com/danielproxd2/solidworks-mcp))

เส้นทางนี้เหมาะเมื่อ Formula Ultimate มี licensed SOLIDWORKS workflow เดิมหรือ
ต้องเข้ากับ supplier เฉพาะ มิฉะนั้นจะเพิ่ม license cost และ community bridge โดย
ไม่ช่วย high-volume open-ended search ให้ดีขึ้น

ข้อสรุป: **ไม่จัดเป็นลำดับแรกของ research prototype**

## สถาปัตยกรรมที่แนะนำสำหรับ Formula Ultimate

```text
Research requirement / component interface schema
  -> search agent
  -> CadQuery source generator ผ่าน restricted MCP tool surface
  -> isolated execution worker
  -> B-rep validity + bounding box + volume + center of mass
  -> STEP/BREP + source + parameters + hashes
  -> Level-0 property contract และ 1D race screening
  -> เฉพาะ candidate ที่ถูกเลือก
      -> Autodesk Fusion official MCP สำหรับ detailed review/edit
      -> FreeCAD/project-owned MCP สำหรับ independent re-open และ CAE preparation
      -> FEA / thermal / CFD authoritative solver
  -> ส่ง solver result และ failure กลับไป search

Optional novelty branch หลัง baseline validation:
  Blender Geometry Nodes / implicit-mesh generator
  -> manifold + dimensions + material + mesh-convergence gate
  -> independent simulation
```

Onshape สามารถแทนหรือเสริม Fusion เมื่อ reusable FeatureScript component family,
cloud collaboration, branching และ PDM มีค่ามากกว่า local desktop control

## เหตุผลที่ยังต้องมี MCP Layer ของโปรเจกต์เอง

แม้ CAD vendor มี MCP แล้ว Formula Ultimate ควรเปิด tool แคบของตัวเองแทนการให้
search agent ใช้ CAD command ทุกอย่าง:

- `create_candidate(source, parameters, interface_schema)`
- `validate_solid(candidate_id)`
- `inspect_mass_properties(candidate_id, material_id)`
- `export_neutral(candidate_id, format)`
- `promote_candidate(candidate_id, fidelity_level)`
- `run_authoritative_analysis(candidate_id, case_id)`

Wrapper ต้องบังคับ workspace root, immutable candidate ID, time/memory limit,
allowlisted import, ปิด implicit network, ควบคุม material library, artifact hash,
solver version และ append-only telemetry วิธีนี้เปลี่ยน MCP เป็น controlled
research interface แทน unrestricted remote control ของ desktop application

## ลำดับ Proof of Concept

### PoC A — CadQuery MCP geometry gate

1. ติดตั้ง CadQuery และ pin revision ของ `cadquery-contrib` ที่ review แล้ว
2. รัน MCP ใน isolated environment ที่ไม่มี secret หรือ unrestricted filesystem/
   network
3. กำหนด component interface schema หนึ่งแบบ: mounting plane สองจุด, bolt hole
   สี่รู, keep-out volume, load point, material และ maximum envelope
4. ให้ agent สร้าง mounting bracket แบบ parametric ที่แตกต่างกันสิบตัว
5. บังคับ valid single solid, interface geometry exact, STEP/BREP export,
   bounding box, volume, surface area และ center of mass
6. Rebuild candidate ทุกตัวสองครั้งแล้วเปรียบเทียบ source/artifact/property hash
7. บันทึก invalid-solid rate, regeneration rate, wall time และ diversity

### PoC B — promote ด้วย official Fusion MCP

1. Enable official Fusion MCP ในเครื่องและตรวจ runtime-discovered tool list
   ห้ามสมมติ tool ที่เอกสารไม่ได้ระบุ
2. Import STEP candidate ที่ดีที่สุดสามตัวเข้าสำเนา review project
3. ตรวจ dimension, interface, editable conversion path, material assignment,
   assembly fit และความสามารถสร้าง manufacturing drawing
4. บันทึก manual repair ทุกจุด Candidate ที่ต้องซ่อมแบบซ่อนถือว่า automatic
   promotion fail

### PoC C — Onshape FeatureScript grammar

1. ใช้ account การศึกษา/private ที่เหมาะสมและ review เงื่อนไข Onshape Labs
2. ให้ official MCP สร้าง reusable custom feature หนึ่งตัวสำหรับ bracket
   interface เดียวกัน แทนการสร้าง part ไม่เกี่ยวกันสิบตัว
3. สร้าง parameter family และตรวจ deterministic regeneration, version history,
   STEP export และ branch comparison
4. เปรียบเทียบ token/tool call และ failure rate กับ CadQuery

### PoC D — novelty geometry branch

หลัง A–C เชื่อถือได้ จึงเพิ่ม Blender/implicit geometry สำหรับ lattice หรือ duct
ห้าม promote mesh เพราะดูแปลก ต้องผ่าน interface, material, manifold,
minimum-feature, mesh-convergence และ solver gate เดียวกัน

## Metric สำหรับยอมรับระบบ

- valid-solid generation rate
- exact interface compliance rate
- deterministic rebuild/hash agreement
- STEP re-import success ใน CAD อิสระสองระบบ
- property disagreement ระหว่าง generator/evaluator
- wall time และ compute cost ต่อ valid candidate
- จำนวน hidden/manual repair
- FEA/CFD meshing success และ convergence rate
- topology/shape diversity หลังตัด duplicate ที่ต่างแค่ parameter
- promotion survival จาก cheap model ไป authoritative analysis

## ข้อกำหนดด้าน Security และ Research Integrity

- Pin MCP และ CAD version แบบ exact ห้าม install community server จาก moving
  branch ใน research environment
- Review source และ dependency ก่อนเชื่อมต่อ
- รัน MCP ที่ execute code ใน isolated worker ที่ไม่มี project secret
- ให้ candidate แต่ละตัวมี bounded directory ใหม่และห้าม path ออกนอกพื้นที่
- แยก read/inspect tool จาก mutate/execute/export tool
- ขอ explicit promotion approval ก่อน high-cost solver หรือ cloud upload
- เก็บ prompt, tool call, response, source, geometry, hash, CAD version, solver
  version, seed และ failure
- ถือ CAD rebuild failure และ solver disagreement เป็นข้อมูล ห้ามซ่อนเป็น error
  ที่น่ารำคาญ

## คำแนะนำสุดท้าย

หากติดตั้งได้โปรแกรมเดียวก่อน ให้เลือก **Autodesk Fusion กับ official GA MCP**
เพราะผู้ใช้อยู่บน Windows ต้องการชิ้นส่วนเครื่องกลจริงที่ละเอียด และอาจใช้สิทธิ์
การศึกษาได้

หากเป้าหมายคือ autonomous geometry experiment ตัวแรก ให้เริ่ม **CadQuery MCP**
เพราะเป็น code-first, B-rep, headless-friendly, testable และเชื่อมกับ Python
research stack เดิมง่าย

ดังนั้นลำดับที่ใช้ได้จริงคือ:

1. CadQuery MCP sandbox และ component-interface PoC
2. Autodesk Fusion official MCP เป็น human-visible promotion/review CAD
3. FreeCAD เป็น independent open-source re-import/CAE checker
4. ทดลอง Onshape Labs FeatureScript MCP สำหรับ reusable component grammar
5. เพิ่ม Blender novelty branch หลัง engineering gate เชื่อถือได้

โครงนี้ให้อิสระ agent ประดิษฐ์ geometry จริง โดยไม่ปล่อยให้ agent หรือ MCP server
ตัวเดียวกันสร้างทั้งรูปร่างและหลักฐานว่ารูปร่างนั้นใช้งานได้
