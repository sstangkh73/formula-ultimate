# ผลงาน 035: การยอมรับ Beam Bending

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-08-29_035_beam-bending-acceptance-result.md`

สถานะ: เสร็จสมบูรณ์

## ผลลัพธ์

Implement linear beam-bending specimen และรันผ่าน real Gmsh/CalculiX mesh สาม
ระดับ Accepted evidence ปิด transverse force/support moment, ตรงกับ
Euler-Bernoulli tip displacement/external work, ทำ signed interior `Sxx` field
ภายใน declared RMS gate และผ่าน last-two-mesh convergence

## ไฟล์ที่เปลี่ยน

- `config/structural/beam_bending_acceptance_v1.json`
- `src/formula_ultimate/structural/acceptance.py`
- `src/formula_ultimate/structural/__init__.py`
- `scripts/structural/run_beam_bending_acceptance.py`
- `scripts/run_work035.ps1`
- `tests/test_beam_bending_acceptance.py`
- `tests/test_structural_acceptance.py`
- `docs/physics/BEAM_BENDING_ACCEPTANCE.md`
- `docs/physics/BEAM_BENDING_ACCEPTANCE.th.md`
- แผน/ผล Work 035 ภาษาอังกฤษและไทย

สร้าง ignored replay evidence ใต้ `artifacts/work035/`

## การตัดสินใจและ failure ที่พบ

- ตอนนี้ CalculiX node set wrap ที่ 16 entries ต่อบรรทัด Initial coarse run พบ
  format limit นี้เมื่อ fixed nodes มี 18 ตัวและ exit `201`; ระบบ reject ก่อน
  physical evaluation และเพิ่ม regression test
- Parser เก็บ complete six-component stress tensor โดย axial-stress view ของ
  Work 034 derive จาก admitted tensor evidence เดียวกัน
- Total reaction force ใช้ explicit total row ของ CalculiX เพื่อไม่ต้องรวมค่า
  per-node ที่ถูกปัดใน text output ส่วน reaction moment คำนวณจาก nodal reaction
  รอบ fixed-face centroid
- ประเมิน `Sxx` ที่ tetrahedron centroid ด้วย volume-weighted signed RMS error
  และ signed correlation ใน interior domain ที่ประกาศล่วงหน้า
- Fixture เดิมลึก `6 mm` และ coarse mesh fail bending accuracy การทดลอง `2.0 mm`
  และ `1.5 mm` ภายหลังยัง fail gate stress RMS `15%` เดิมที่ `19.77%` และ
  `15.14%` Accepted sequence เริ่ม `1.4 mm`; ไม่ได้ผ่อน tolerance

## หลักฐานที่รับ

Reference: tip `2.38095238095238e-5 m`, root moment `0.6 N*m`, root outer
stress `2.08333333333333e6 Pa`, external work `5.95238095238095e-5 J`

| Mesh | Nodes | C3D4 | Tip error | Stress RMS | Correlation | Force closure | Moment closure |
|---|---:|---:|---:|---:|---:|---:|---:|
| coarse_1p4mm | 6,944 | 31,022 | 4.1889% | 14.2772% | 0.989799 | 3.54e-12 | 2.66e-8 |
| medium_1p2mm | 10,343 | 48,003 | 3.1378% | 12.1645% | 0.992602 | 1.83e-12 | 4.22e-8 |
| fine_1mm | 16,767 | 81,764 | 2.2179% | 10.1221% | 0.994880 | 4.59e-12 | 2.46e-8 |

Last-two displacement/work change เท่ากับ `0.00949702932475448`; stress-error
absolute change เท่ากับ `0.0204245660076813` ทุก gate ผ่าน

## การตรวจสอบ

คำสั่งคืน exit `0` ตาม fail-fast order:

```powershell
py -3.14 -m unittest tests.test_beam_bending_acceptance tests.test_structural_acceptance -v
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work035.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work034.ps1
py -3.14 -m unittest discover -s tests -q
py -3.14 -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Output สำคัญ:

```text
focused: Ran 12 tests ... OK
Work 035: status=passed, 3 meshes, fine=16767 nodes/81764 C3D4
Work 034 regression: status=passed, 3 meshes
full: Ran 280 tests in 36.865s ... OK
compileall: no output
git diff --check: no errors
git diff --cached --check: no errors
```

Staged scope มีเฉพาะ 13 ไฟล์ที่ระบุของ Work 035 และจะรายงาน commit hash ใน
final handoff

## Falsification review และข้อจำกัด

Supporting evidence รวม load/moment closure, analytical global response,
signed stress-field agreement, mesh convergence, fresh artifact และ retained
failed attempt ส่วน simple regular beam/end region ที่ exclude ยังเป็น strong
alternative explanation จึงไม่ใช่ arbitrary-geometry validation

ยังไม่มี independent solver/physical beam data และไม่ได้ parse internal strain
energy อย่างอิสระ Yield, plasticity, torsion, buckling, fracture, fatigue,
joint, connection removal และ `DNF` coupling ยังขาด Work item ถัดไปคือ
solid-shaft torsion specimen ที่มี gate แยก
