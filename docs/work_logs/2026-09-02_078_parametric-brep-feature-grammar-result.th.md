# ผล Work 078: Parametric B-rep Feature Grammar V1

สถานะ: Completed

ต้นฉบับภาษาอังกฤษ: `2026-09-02_078_parametric-brep-feature-grammar-result.md`

## ผลลัพธ์และไฟล์ที่เปลี่ยน

Implement declaration แบบ fail-closed `parametric_brep_feature_grammar_v1` และ executor CadQuery 2.8.0 Corpus ที่รับ execute operator identity ที่บังคับครบ 15 ตัวแบบ causal ผ่าน shaft, bracket, hollow housing, ribbed plate และ hub-like rotating part Final artifact ทุกตัวเป็น B-rep solid เดียว valid มี volume เป็นบวกและ export เป็น canonical STEP artifact

ไฟล์ที่เปลี่ยนคือคู่ plan/result ของ Work 078; `docs/contracts/PARAMETRIC_BREP_FEATURE_GRAMMAR_V1.md` และคู่ภาษาไทย; `config/cad/brep_feature_grammar_v1.json`; `src/formula_ultimate/components/brep_grammar.py`; component exports; `scripts/cad/generate_brep_feature_corpus.py`; และ `tests/test_brep_grammar.py`

## การตัดสินใจและหลักฐานการทดลอง

- ตรวจ exact schema และ ancestry ก่อนโหลด candidate เข้า kernel มิติเป็นค่า SI finite แบบ bounded และแปลงจาก metre ไป convention millimetre ของ CadQuery หนึ่งครั้ง
- Profile, extrude/revolve, cut/bore, shoulder/rib/shell, pattern, edge treatment และ boolean สามชนิดเป็น operator ที่ execute ต่างกันจริง ไม่ใช่ label ประดับ
- Non-profile feature ทุกตัวต้อง valid, non-empty, finite และ positive-volume `Compound` ที่ห่อ solid เดียวถูก unwrap แบบรักษา representation; หลาย solid ไม่ถูก auto-fuse หรือ repair Final state ต้องมี solid เดียว exact
- STEP canonicalization เปลี่ยนเฉพาะ timestamp ที่เปลี่ยนได้ใน `FILE_NAME` Output root สองชุดให้ manifest identity และ STEP bytes ต่อ candidate เหมือนกัน
- Empty boolean subtraction และ disconnected multi-solid final pattern fail แบบ observable

Manifest SHA-256 ที่รับคือ `fff5c0c74513fae1a2bc7cd55020affbbaf67bdd6e9c0908f5aa2ea4131b2448`

| Candidate | Volume (`m3`) | STEP SHA-256 |
|---|---:|---|
| `shaft_001` | `7.936733407181722e-05` | `34e81618e3cd6fefa278bf6cdfd564db06407d118651efa16c16202971f485c1` |
| `bracket_001` | `8.144352220392309e-05` | `b06e3141f7a1fcad8017537d3680a787164d3190d4503417d3f6c1c98ed1ba89` |
| `hollow_housing_001` | `0.00013046885705011982` | `ef92f5215e5614ebe00f6e2c4e6850cd252f69fc437a81231d0911b21cbd7862` |
| `ribbed_plate_001` | `9.916492873496904e-05` | `af73c6492c9c56fed73e21542c3caba2611f3cc4bc592df129a1683c6a467a10` |
| `hub_like_001` | `0.00014511182449342868` | `8b3ff21861037dea2104d287286cee98f69da59cb4c0eae1d4744c8cedce00f0` |

## บันทึก validation แบบ exact

```text
python -m unittest tests.test_brep_grammar.BrepGrammarParserTests -q
Exit: 0
Ran 6 tests in 0.004s — OK

.tools\cadquery-mcp\Scripts\python.exe kernel unittest invocation
Exit: 0
Ran 3 tests in 2.863s — OK

.tools\cadquery-mcp\Scripts\python.exe scripts\cad\generate_brep_feature_corpus.py --config config\cad\brep_feature_grammar_v1.json --output-root artifacts\work078\run_a\step --manifest artifacts\work078\run_a\manifest.json
Exit: 0; status=passed; candidate_count=5

คำสั่งเดียวกันโดยใช้ run_b output root และ manifest
Exit: 0; status=passed; STEP hash ทั้งห้าและ manifest SHA-256 เหมือนกัน

python -m unittest tests.test_brep_grammar tests.test_repository_contract -v
Exit: 0
Ran 15 tests in 0.713s — OK (skipped=3 kernel tests ใน Python ที่ไม่มี CadQuery)

python -m compileall -q src scripts\cad\generate_brep_feature_corpus.py tests\test_brep_grammar.py
Exit: 0

python -m unittest discover -s tests -q
Exit: 0
Ran 496 tests in 300.327s — OK (skipped=3)
```

Test ที่ skip สามตัวไม่ใช่ missing evidence เพราะถูกรันแยกและผ่านใน pinned CadQuery environment ตาม record ด้านบน

## การหักล้าง หลักฐานขัดแย้ง และ confidence

Fixture hollow-housing ก่อน admitted run เริ่มแรกวาง stepped bore ไว้กลางช่องที่ว่างอยู่แล้วหลัง shell Kernel คืนผล cut ว่างและ corpus test ปฏิเสธอย่างถูกต้อง Fixture ถูกเปลี่ยนก่อน admitted replay ให้วาง stepped bore ขนาดเล็กลงในเนื้อผนังจริง สิ่งนี้ขัดแย้งกับสมมติฐานว่า feature sequence ที่ syntax ถูกต้องจะตัด material แบบ causal เสมอ

Shell operator ยังเปิดเผย representation ของ OCCT ที่ห่อ solid เดียวที่ valid ใน `Compound` Implementation unwrap เฉพาะกรณี solid เดียว exact และไม่ fuse, heal หรือเปลี่ยน geometry ส่วน disconnected pattern สอง solid ที่ตั้งใจยังถูกปฏิเสธเป็น final part

Alternative explanation ของ byte stability รวมการใช้ CadQuery/OCCT exporter ร่วมกันและ environment ที่ pin Missing evidence รวม independent FreeCAD inspection, semantic-interface recovery หลัง STEP, cross-tool B-rep comparison, robustness ทั่ว parameter space, material/process constraint และ structural/physical correlation Confidence สูงสำหรับ corpus/toolchain ที่ทดสอบ exact และต่ำเมื่ออยู่นอก domain ของ grammar ที่ประกาศ

## ข้อจำกัดและงานถัดไป

V1 ยังไม่มี freeform loft/sweep, arbitrary transform/edge query, thread/gear, sheet-metal/composite process history และ persistent semantic face Work 079 ต้องเพิ่ม material/manufacturing constraint ที่มีหลักฐาน และ Work 081 ต้องตรวจ STEP geometry อิสระ Stable STEP hash ไม่พิสูจน์ stable face number หรือ physical validation
