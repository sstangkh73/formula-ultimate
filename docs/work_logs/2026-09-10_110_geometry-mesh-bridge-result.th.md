# ผล Work 110: สะพานจาก geometry จริงสู่ mesh

ต้นฉบับภาษาอังกฤษ: `2026-09-10_110_geometry-mesh-bridge-result.md`

วันที่: 2026-09-10 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และไฟล์

Work 110 สร้าง Gmsh meshes ที่ solver อ่านได้แบบ deterministic หกชุด: สามระดับจาก labelled field Work 109 และ voxel approximations สามระดับของ hollow B-rep ที่ตรงกันจาก Work 108 Tetrahedra ทั้งหมดมี Jacobian บวก material/boundary sets ครบ centerline ของ cavity ยังเป็น void, controls ล้มเหลวแบบปิด และ replay exact

ไฟล์ที่เปลี่ยน: `src/formula_ultimate/structural/geometry_mesh_bridge.py`, `config/development/geometry_mesh_bridge_v1.json`, `scripts/development/run_geometry_mesh_bridge.py`, `tests/test_geometry_mesh_bridge.py`, `docs/contracts/GEOMETRY_MESH_BRIDGE_V1*` สองภาษา, plan/result นี้สองภาษา และ `artifacts/work110/run_a|run_b` ที่ ignore

## การตัดสินใจ ความล้มเหลว และการหักล้าง

- การแบ่ง cell เป็น tetra หกก้อนคงที่ให้ orientation บวก, material groups และ Gmsh 2.2 แบบ deterministic แต่ไม่ใช่ unstructured B-rep mesh ที่ conforming
- Semantic sets คือ `external_surface`, `load_surface`, `contact_surface` และ `material_interface` เมื่อ labels พบกัน
- runner แรก replay mutation chain ของ Work 109 ที่ทุก resolution ของ Work 110 อย่างผิดขอบเขต ที่ `0.02 m` edit หนึ่งกลายเป็น no-op และ run exit `1` การทดลองที่แก้แล้ว mesh source field เดียวกันของ Work 109 ทุกระดับ โดยไม่ขยาย validity ของ mutation เกิน `0.01 m` ที่ลงทะเบียน
- run ถัดมาเปิดเผย signature จริง `isInside(point, tolerance)` ของ CadQuery การตัด argument ตัวที่สี่ซึ่งไม่รองรับแก้ adapter โดยไม่เปลี่ยน geometry หรือ thresholds
- Controls ปฏิเสธ inverted elements, boundary sets หาย, หน่วยผิด, cavity ถูกเติม, reference เก่า และ geometry substitution

## หลักฐาน

Result SHA-256: `46a4d7a0a7f168c0bbb879b186751397cf4127347cd27bd495979153eb82c0fd` Artifact manifest: `e50a30b1338a350a8151ff5e95d7b9c65a007cf485f398c7aab49c6b0085bd2a` และ `run_b/replay.json` เป็น `exact: true`

| Route / resolution (`m`) | Nodes | Tets | Triangles | Volume error | Min Jacobian (`m3`) |
|---|---:|---:|---:|---:|---:|
| field / `0.02` | `289` | `984` | `434` | `1.801494463428658e-14` | `7.999999999999988e-6` |
| field / `0.01` | `1865` | `8100` | `2008` | `1.1596947681993097e-13` | `9.999999999999944e-7` |
| field / `0.008` | `3220` | `14880` | `2936` | `1.6428340630214454e-13` | `5.11999999999996e-7` |
| hollow B-rep / `0.02` | `62` | `78` | `120` | `0.07909779256191748` | `7.999999999999991e-6` |
| hollow B-rep / `0.01` | `334` | `732` | `728` | `0.26586471819763147` | `9.99999999999998e-7` |
| hollow B-rep / `0.008` | `503` | `1062` | `1092` | `0.05969078506606261` | `5.119999999999991e-7` |

Maximum edge ratio คือ `1.7320508075688812` ต่ำกว่า `1.8` B-rep errors ไม่ monotonic จึงขัดแย้งกับ convergence; ทุกค่าอยู่ใต้ approximation gate `0.35` ที่ลงทะเบียน

## การตรวจ

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_geometry_mesh_bridge tests.test_repository_contract -v
# exit 0; ผ่าน 10 tests
python -m compileall -q src scripts tests
# exit 0
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_geometry_mesh_bridge.py --config config\development\geometry_mesh_bridge_v1.json --output-root artifacts\work110\run_a
# exit 0; หก meshes; status passed
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_geometry_mesh_bridge.py --config config\development\geometry_mesh_bridge_v1.json --output-root artifacts\work110\run_b --replay-reference artifacts\work110\run_a\result.json
# exit 0; exact replay
git diff --check
# exit 0
```

ยังต้องรัน affected regression สุดท้ายและ staged checks ก่อน commit จะรายงาน hash ที่ตรวจแล้วใน final handoff

## ข้อจำกัดและงานต่อ

เส้นทาง B-rep ใช้ voxels ที่ sample centre และขอบเขต `35%` ที่เปิดเผยและค่อนข้างกว้าง เหมาะเป็น bridge แบบมีขอบเขต ไม่ใช่ curved meshing ความละเอียดสูง Error aliasing, thin-feature loss นอกกรณีที่เลือก และ solver-field convergence ที่ยังไม่มีคงเป็นข้อจำกัด Work 111 ต้อง solve และ verify vector fields บน meshes ชุดนี้โดยไม่ถือ mesh quality เป็น physics validation
