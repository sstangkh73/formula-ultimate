# Work 110: สะพานจาก geometry จริงสู่ mesh

ต้นฉบับภาษาอังกฤษ: `work110-geometry_mesh_bridge.md`

Status: Planned

หมายเลขเดิมใน Work 106: 109

พึ่งพา: Work 108, Work 109

ข้อกำหนดร่วมที่ต้องใช้: [ดัชนีและกติกา](README.th.md) หมายเลข ไฟล์ และ CLI ด้านล่างเป็นข้อเสนอ ยังไม่ใช่สิ่งที่พัฒนาแล้ว

## 1. ผลที่ต้องได้และข้อมูลเข้า

สร้าง volume/surface meshes พร้อมให้ solver ใช้จาก geometry candidate โดยรักษาโพรง วัสดุ และขอบเขตเชิงความหมาย

ใช้ solids Work 108 และ surfaces Work 109 เริ่ม meshing เส้นทาง B-rep ก่อน adapter representation ใหม่เสร็จได้

## 2. ไฟล์ที่เสนอ

- `src/formula_ultimate/structural/geometry_mesh_bridge.py`
- `config/development/geometry_mesh_bridge_v1.json`
- `scripts/development/run_geometry_mesh_bridge.py`
- `tests/test_geometry_mesh_bridge.py`

## 3. ขั้นลงมือทำ

1. benchmark mesh adapters บน corpus ที่ล็อก บันทึก versions และ failures ก่อนเลือก
2. ผูกบริเวณวัสดุและผิว load/contact กับ semantic mesh sets ที่คงตัวตน
3. สร้าง spatial refinement อย่างน้อย 3 ระดับ ตรวจ Jacobians โพรง และ interfaces
4. เทียบมวล mesh/CAD และ geometry ขอบเขต เก็บ manifests และ diagnostics ที่ทำซ้ำได้

## 4. การทดลอง

- IV: ตระกูล geometry, representation, mesh density และ curvature/feature refinement
- DV: element quality, geometric error, material coverage, mass discrepancy และ meshing cost
- Controls: source geometry/material hash และความหมายขอบเขตเดียวกันทุก refinement

## 5. Tests และการหักล้าง

ฉีด inverted elements, boundary sets หาย, โพรงถูกเติม, หน่วยผิด และ mesh references เก่า ห้ามแทน candidate ที่ mesh ไม่ได้ด้วย mesh กล่อง

## 6. ค่าที่ต้องล็อกและเกณฑ์รับ

ล็อก refinement schedule 3 ระดับ เกณฑ์ quality, coverage requirements และ geometry/mass tolerances

ทุก positive case ที่ admitted ต้องรักษาบริเวณและขอบเขตใน tolerance ที่ล็อก กรณีไม่รองรับยัง unresolved ไม่ใช่ล้มเหลวทางฟิสิกส์

## 7. สิ่งส่งมอบและงานรับต่อ

meshes จริง semantic maps, ตาราง quality/error, build metadata และรายงานทำซ้ำ

ส่งให้ vector mechanics Work 111 และ thermal/flow Work 115/121

## 8. ความเสี่ยงและสิ่งที่ไม่ทำ

feature บางอาจหายแม้ปริมาตรรวมดูถูก ต้องตรวจ geometry เฉพาะที่ด้วย ยังไม่อ้าง solver accuracy หรือ stress convergence

## 9. คำสั่งตรวจที่ต้องพัฒนา

ต้องสร้าง runner/CLI และล็อก config ก่อนใช้ คำสั่งนี้ยังไม่ได้รันในงานวางแผน สำหรับงานทดสอบของจริง runner วิเคราะห์ข้อมูลที่บันทึกไว้เท่านั้น ไม่ควบคุมอุปกรณ์

```powershell
python -m unittest tests.test_geometry_mesh_bridge tests.test_repository_contract -v
python scripts/development/run_geometry_mesh_bridge.py --config config/development/geometry_mesh_bridge_v1.json --output-root artifacts/work110/run_a
python scripts/development/run_geometry_mesh_bridge.py --config config/development/geometry_mesh_bridge_v1.json --output-root artifacts/work110/run_b --replay-reference artifacts/work110/run_a/result.json
```
