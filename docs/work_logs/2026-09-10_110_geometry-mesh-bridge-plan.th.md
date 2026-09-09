# แผน Work 110: สะพานจาก geometry จริงสู่ mesh

ต้นฉบับภาษาอังกฤษ: `2026-09-10_110_geometry-mesh-bridge-plan.md`

วันที่: 2026-09-10 (Asia/Bangkok)

Status: Completed

## วัตถุประสงค์และขอบเขต

พัฒนา tetrahedral volume meshes และ triangular surface/semantic sets ที่ solver อ่านได้จาก upstream representations ที่ admitted ทั้งสองแบบ: labelled cells ของ Work 109 และ hollow B-rep ที่ตรงกันจาก Work 108 รักษา cavities, material labels, source identities และ approximation/quality errors ที่สังเกตได้ตลอดสามระดับที่ลงทะเบียน

Field adapter แบ่ง occupied Cartesian cell ทุกช่องเป็น tetrahedra โดยไม่แทน geometry ส่วน B-rep adapter sample solid โค้งกลวงจริงที่ resolution ลงทะเบียน ทำเครื่องหมาย boundary cells ที่ยังเป็น approximation และ tetrahedralize เฉพาะ occupied cells ที่ admitted ทั้งสองแบบ emit Gmsh 2.2 ASCII และ manifests แบบ deterministic

## การทดลองและไฟล์ที่วางแผน

- ตัวแปรอิสระ: source representation/family และ resolution
- ตัวแปรตาม: nodes/elements, signed Jacobian, aspect proxy, volume/mass discrepancy, material coverage, boundary-set coverage, cavity/topology preservation และ deterministic cost
- ตัวควบคุม: upstream SHA-256/material semantics และความหมาย named boundary เดิมทุกระดับ
- ความล้มเหลว: inverted/zero elements, sets หาย, cavity ถูกเติม, หน่วยผิด, source identity เก่า, label หาย, mesh เกินงบ หรือ geometry ถูกแทน

ไฟล์ที่วางแผน:

- `src/formula_ultimate/structural/geometry_mesh_bridge.py`
- `config/development/geometry_mesh_bridge_v1.json`
- `scripts/development/run_geometry_mesh_bridge.py`
- `tests/test_geometry_mesh_bridge.py`
- `docs/contracts/GEOMETRY_MESH_BRIDGE_V1.md` และคู่ภาษาไทย
- plan/result นี้และคู่ภาษาไทย
- meshes/evidence ที่ ignore ใต้ `artifacts/work110/`

## การตรวจและเกณฑ์สำเร็จ

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_geometry_mesh_bridge tests.test_repository_contract -v
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_geometry_mesh_bridge.py --config config\development\geometry_mesh_bridge_v1.json --output-root artifacts\work110\run_a
& .\.tools\cadquery-mcp\Scripts\python.exe scripts\development\run_geometry_mesh_bridge.py --config config\development\geometry_mesh_bridge_v1.json --output-root artifacts\work110\run_b --replay-reference artifacts\work110\run_a\result.json
python -m compileall -q src scripts tests
```

ทั้งสามระดับของทั้งสองเส้นทางต้องมีเฉพาะ tetrahedra ปริมาตรบวก วัสดุครบ และ semantic surface sets ที่ต้องการ; volume ของ field mesh ต้อง exact, volume/mass errors ของ B-rep อยู่ในขอบเขต approximation ที่ล็อก, centerline ของ hollow ยังเป็น void, negative controls ปฏิเสธ และ replay exact จากนั้นรัน affected regressions, diff/staged checks และ commit จำกัด scopeหนึ่งก้อนทันที

## ความเสี่ยงและสิ่งที่ไม่ทำ

Voxel sampling อาจทำให้ feature บาง/โค้งหายและไม่ใช่ unstructured conforming B-rep mesher ต้องบันทึกอคตินี้และ conversion ที่ unresolved ห้ามแทน candidate ที่ล้มด้วยกล่อง สิ่งที่ไม่ทำ: solver accuracy, stress convergence, constitutive physics, universal meshing, manufacturing, รถทั้งคันหรือ physical validation, ติดตั้ง, push หรือเขียนประวัติใหม่
