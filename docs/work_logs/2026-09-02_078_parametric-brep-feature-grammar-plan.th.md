# แผน Work 078: Parametric B-rep Feature Grammar V1

สถานะ: Completed

ต้นฉบับภาษาอังกฤษ: `2026-09-02_078_parametric-brep-feature-grammar-plan.md`

## วัตถุประสงค์และขอบเขต

Implement parametric B-rep feature grammar แบบ bounded หน่วย SI ที่ agent ใช้สร้างและ replay solid ของ single part จริงได้ V1 ครอบคลุม sketch profile, extrude, revolve, pocket/cut, through hole, stepped bore, shaft shoulder, rib/web, shell/wall thickness, linear/circular pattern, bounded fillet/chamfer และ boolean union/subtract/intersect

Corpus ที่รับได้ประกอบด้วย shaft, bracket, hollow housing, ribbed plate และ hub-like rotating part งานนี้ validate เฉพาะ grammar ที่ระบุ, route CadQuery/OCCT, valid-solid final state และ deterministic STEP identity ไม่ยืนยัน material adequacy, manufacturability, structural capacity, assembly behavior หรือ physical validation

## แบบการทดลอง

- ตัวแปรอิสระ: feature operator/order, มิติ SI แบบ bounded, parent-feature reference, profile type, pattern count/spacing/angle, wall/fillet/chamfer size และ boolean operation
- ตัวแปรตาม: parse admission/rejection, feature execution status, final solid count/validity/volume/bounds, STEP SHA-256 และ replay identity
- ตัวแปรควบคุม: canonical part family 5 แบบ; config/order replay; control สำหรับ zero thickness, parameter เกิน bound, unknown operator/field/unit, forward/unknown parent, subtract ที่ลบตัวเองหมด, empty intersection, shell failure และ final multi-solid
- สมมติฐานที่ต้องการ: part family ทั้ง 5 execute เป็น solid เดียว valid มี volume เป็นบวก และ replay เป็น canonical STEP hash ที่เหมือนกันทุก byte ภายใต้ toolchain CadQuery ที่ pin; declaration หรือ kernel result ที่ผิดต้อง fail closed
- การหักล้าง: operator ถูกข้าม, แปลงหน่วยโดยปริยาย, ยอมรับ invalid/intermediate kernel state, รับ final ที่ empty/multi-solid, hidden geometry repair, hash drift จากเวลา/path หรือ replay mismatch

## ไฟล์ที่วางแผน

- `config/cad/brep_feature_grammar_v1.json`
- `src/formula_ultimate/components/brep_grammar.py` และ component exports
- `scripts/cad/generate_brep_feature_corpus.py`
- `tests/test_brep_grammar.py`
- `docs/contracts/PARAMETRIC_BREP_FEATURE_GRAMMAR_V1.md` และคู่ภาษาไทย
- plan นี้และ result record คู่สองภาษา
- หลักฐานที่ ignore ใต้ `artifacts/work078/`

## การตรวจและเกณฑ์สำเร็จ

Operator ที่ระบุทุกตัวต้องถูก execute โดย feature อย่างน้อยหนึ่งรายการใน corpus ที่ผ่าน Part family ที่บังคับทั้ง 5 ต้องให้ solid เดียว valid มี finite positive volume และ canonical STEP artifact Output root อิสระสองตำแหน่งต้องให้ STEP SHA-256 ต่อ candidate และ canonical manifest identity เดียวกันภายใต้ toolchain ที่ pin Negative control ต้องปฏิเสธ zero thickness, unknown field/unit/operator, ancestry/bounds ผิด, empty boolean result และ invalid final solid state Focused parser/kernel tests, full regression, compilation, bilingual contract, scoped staging, `git diff --cached --check`, commit เดียว และ post-commit replay ต้องผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำโดยชัดแจ้ง

OCCT boolean, shell และ edge treatment อาจล้มเหลวกับ parameter ที่ดูถูกต้องและ failure นั้นต้อง observable แทนการซ่อม Stable STEP bytes ขึ้นกับ toolchain และไม่แปลว่า face numbering คงที่ Corpus bounded 5 family ไม่ใช่ arbitrary topology, manufacturing process model, FEA evidence หรือหลักฐานความสามารถออกแบบ part ได้ครบทุกแบบ
