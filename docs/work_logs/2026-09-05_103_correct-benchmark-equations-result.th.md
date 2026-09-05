# ผล Work 103: แก้สมการและหลักฐานสมดุลของ benchmark

ต้นฉบับภาษาอังกฤษ: `2026-09-05_103_correct-benchmark-equations-result.md`

Status: Completed

## ผลและไฟล์

แก้ `src/formula_ultimate/structural/generalized_geometry_benchmarks.py`, เพิ่ม version ผลใน `scripts/structural/run_generalized_geometry_benchmarks.py`, เพิ่ม tests ใน `tests/test_generalized_geometry_benchmarks.py` และปรับ `docs/contracts/GENERALIZED_GEOMETRY_BENCHMARKS_V1.md` กับ `.th.md` พร้อมแผน/ผล Work 103 สองภาษารวม 4 ไฟล์ commit ครอบคลุมเฉพาะ 9 ไฟล์นี้

เก็บผลใหม่ใน `artifacts/work103/run_a/result.json` และ `artifacts/work103/run_b/result.json` ซึ่งไม่อยู่ใน Git ไม่แก้ outputs Work 097 เดิม และไม่เปลี่ยน config/load/threshold/source identities

## สมการและการตัดสินใจด้านหลักฐาน

- หา K จาก geometry/material/discrete compliance ก่อนประเมิน response แล้วตรวจ q = K*u^p แทนการหา K ย้อนจาก q/u
- สำหรับ Hertz แบบ quasistatic อินทิเกรต F = K*delta^(3/2) ได้ U = (2/5)*K*delta^(5/2) ไม่ใช่ (1/2)*F*delta ใช้ E* = E/[2(1-nu^2)] และ effective-radius proxy เดียวกันใน indentation กับ contact pressure
- คง contact radius บวกที่ป้อน แม้ thickness ใหญ่กว่า ใช้ thickness เฉพาะเมื่อไม่มี radius และปฏิเสธ radius ผิดโดเมน
- งานความดัน-การกระจัดมีหน่วย J/m^2 ส่วนแรง-การกระจัดมีหน่วย J
- แทน field force/moment/energy residual ที่สร้างให้หักล้างกันเองด้วย null และ `full_balance_validated=false` residual ของสมการ/พลังงานสเกลาร์ที่ตั้งชื่อชัดเป็นการตรวจความสอดคล้อง ไม่ใช่ field balance อิสระ
- กำหนด convergence จาก scalar residual จริง บันทึก Newton history และ effort ที่ใช้ หากงบหมดต้องเป็น invalid โดยไม่มี fallback
- คำนวณ scalar evidence/reference error ใหม่ใน adjudication ตรวจลำดับเพิ่มสองเท่า และปฏิเสธ field zeros แบบเก่า/ปลอม หรือ scope ที่หาย
- ระบุ `evaluator_version=generalized_geometry_equations_v2` โดย input schema ยังเป็น V1 ห้ามถือว่าผลเก่าและใหม่ replay เป็นผลเดียวกัน

ตรวจความสัมพันธ์ Hertz normal contact กับ [CompuTiX theory](https://computix.gitlabpages.inria.fr/computix/db/d6e/group__Hertz.html) และหาตัวคูณพลังงานด้วยการอินทิเกรตกฎแรงโดยตรง ยังสมมติวัสดุยืดหยุ่นเท่ากัน effective-radius proxy และการเพิ่มโหลด quasistatic ตามที่เปิดเผย

## การทดสอบและผลที่วัด

คำสั่งตรงที่รันจาก `C:\Formula Ultimate` ตรวจ exit status แยกแต่ละคำสั่ง:

```powershell
python -m unittest tests.test_generalized_geometry_benchmarks -v
python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work103/run_a/result.json
python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work103/run_b/result.json --replay-reference artifacts/work103/run_a/result.json
python -m unittest discover -s tests -q
python -m unittest tests.test_repository_contract -q
git diff --check
git diff --cached --check
```

- Focused tests: exit 0, 17 tests ใน 0.319 s, OK (เพิ่ม 8 test methods) เพิ่ม assertion nonzero-Poisson/equal-effective-modulus ระหว่าง full suite ทำงาน และตรวจครอบคลุมด้วย focused run สุดท้ายนี้ ไม่เปลี่ยน production code ระหว่าง full run
- Full suite: exit 0, `Ran 697 tests in 427.395s`, `OK (skipped=7)`.
- Repository contracts และ whitespace checks: ยืนยันผ่านรอบสุดท้ายก่อน commit
- Runner และ exact replay: exit 0 ผ่าน 7 cases ด้วย configuration เดิม Result SHA-256: `1b38f6468cd94f8c604120aa8af8f8c7a5c14842420c894926a22bc45bed466d`
- Contact case ที่เก็บไว้: pressure เปลี่ยนจาก 211763869.07630363 Pa เป็น 144061379.89067543 Pa; yield-screen ratio จาก 0.8792554763052145 เป็น 0.6084455195627017 โดยไม่ปรับ load/threshold
- Hertz indentation = 1.6584132504364747e-06 m; stored energy = 1.6584132504364745e-05 J; Newton 5 iterations ประวัติ relative residual: [0.6464466094067258, 0.16862910096068973, 0.004122917441717817, 2.8227306565042907e-06, 1.3281464816827792e-12, 0.0]
- scalar equilibrium residual สูงสุดทุกระดับ = 1.4551915228366853e-16 ยังไม่ได้คำนวณ field balance ค่าสเกลาร์เล็กนี้จึงไม่ใช่การอ้าง physical validation

หลักฐาน regression อิสระรวมสปริงเชิงเส้น 400 N/m การอินทิเกรตเชิงตัวเลขและ dU/ddelta = F กรณี Hertz ที่ทราบค่า load 1 N / indentation 1e-4 m / energy 4e-5 J / peak pressure 4774.64829275686 Pa การสเกล load/modulus ค่า E* เท่ากันจาก E/nu ต่างกัน หน่วยความดัน การรบกวน response งบ Newton หมดจริง และโดเมนผิด

## การพิจารณาหลักฐานและข้อจำกัด

ตัวแปรต้นคือ implementation ที่แก้ ระดับ iteration/refinement และการรบกวนใน tests ตัวควบคุมคือ config/material/witness/load/threshold identities เดิม ตัวชี้วัดคือ displacement, energy, contact pressure, residuals, convergence, failure screens และ exact replay เกณฑ์สำเร็จผ่าน: ตรวจสมการที่ทราบค่า ปฏิเสธคำตอบที่รบกวน ผ่าน 7 กรณีแบบจำกัดและ replay หลักฐานสนับสนุนคือการตรวจค่า/อินทิกรัล/scaling อิสระ ส่วนหลักฐานโต้แย้งการยืนยันที่กว้างกว่านี้คือยังไม่มี field reactions อิสระ คำอธิบายทางเลือกของ residual เล็กคือเพียงแก้ constitutive law ลดรูปได้ตรง ซึ่งระบุไว้ชัด ไม่ตีความเป็นความแม่นโลกจริง

มั่นใจสูงต่อความสัมพันธ์ Hertz สเกลาร์ที่แก้และพฤติกรรม regression แต่ยังไม่มี physical validation ของวัสดุ synthetic, radius proxy, frictional contact, geometry STEP ทั่วไป หรือรถทั้งคัน failure screens อื่นยังเป็น proxies แบบจำกัด งานต่อคือต้องมี mesh/field reactions อิสระและตรวจขอบเขตใช้ได้ของแต่ละโมเดล

การ apply patch ครั้งหนึ่งไม่ตรง context จึงไม่เปลี่ยนไฟล์ และแก้โดยอ่าน source ตรงก่อน apply ใหม่ การค้นแรกมี wildcard/directory ที่ไม่มี 2 แห่ง จึงใช้ path ตรงที่ถูกต้องภายหลัง ทั้งหมดเป็นปัญหาแก้ไฟล์/ค้นไฟล์ ไม่ใช่ validation gate ล้มเหลว ชุด tests เดิม 9 tests ผ่านก่อนเพิ่ม regression ใหม่ 8 methods

หลัง gates สุดท้ายผ่าน ให้ stage เฉพาะ 9 ไฟล์ที่ประกาศ ตรวจ scope แล้ว commit และตรวจ commit ใหม่กับสถานะสะอาด รายงาน short hash ใน final handoff ไม่ push หรือแก้ประวัติเดิม
