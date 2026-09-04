# แผน Work 090: Search-Space Bias and Diversity Contract

ไฟล์ต้นฉบับภาษาอังกฤษ: `2026-09-04_090_search-space-bias-diversity-contract-plan.md`

## สถานะ

สถานะ: Completed

## วัตถุประสงค์

Implement งานแรกใน `GEOMETRIC_DESIGN_DIVERSITY_ROADMAP_V1`: contract ความหลากหลายแบบ deterministic ที่ไม่เปลี่ยนตามชื่อ rigid transform และ uniform scale พร้อม census ที่ทำซ้ำได้ของ bounded whole-vehicle proposal space ปัจจุบัน ผลต้องวัด fixed-topology/primitive bias ก่อน Work 091 ขยาย representation

## ขอบเขตและไฟล์ที่วางแผน

- `config/experiments/design_diversity_v1.json`
- `src/formula_ultimate/experiments/design_diversity.py`
- `scripts/experiments/run_design_diversity_baseline.py`
- `tests/test_design_diversity.py`
- `docs/contracts/DESIGN_DIVERSITY_V1.md` และไฟล์ภาษาไทยคู่กัน
- แผน/ผลนี้และไฟล์ภาษาไทยคู่กัน
- หลักฐานที่ ignore ใต้ `artifacts/work090/`

## ตัวแปรต้น/ตามและตัวควบคุม

- Input อิสระ: exact base assembly ปัจจุบัน, exact Work 050 search protocol ปัจจุบัน, treatment/seed/attempt ledger ที่ตรึง และ metamorphic/topology control ที่ฉีดเข้าไป
- Output ตาม: topology signature, normalized geometry signature, primitive fraction, operator/type entropy, curvature-class distribution, graph-path signature, unique-signature ratio, duplicate phenotype rate และสาเหตุ rejection
- Control: translation, rigid axis permutation/sign change, component/interface renaming, uniform scale, branch addition, path reroute, primitive-family change และ interface-topology change

## การตรวจสอบและเกณฑ์สำเร็จ

- Translation, rotation/reflection ที่แทนด้วย signed axis permutation, component/interface renaming และ uniform scale ที่เท่าเทียมต้องคง normalized signature
- การเพิ่ม branch, reroute connectivity, เปลี่ยน primitive family และเปลี่ยน interface topology ต้องเปลี่ยน signature ที่เกี่ยวข้อง
- Census proposal ปัจจุบัน exactly `288` ตัว: สาม treatment, สาม seed และสามสิบสอง attempt ต่อ treatment/seed
- Config เดิมต้องสร้าง result/census ที่เหมือนกันทุก byteใน clean root สองชุด
- Unknown field, identity หาย, geometry non-finite, reference หลุด และ source hash เปลี่ยนต้อง fail closed
- Focused test, repository-contract test, compilation และ full regression ต้องผ่าน

## ความเสี่ยงและสิ่งที่ไม่ทำ

Canonical graph labeling อาจพึ่งชื่อโดยไม่ตั้งใจหรือกำกวมกับ node สมมาตร Geometry normalization อาจลบผลของ absolute scale ที่มีความหมาย ดังนั้น metric topology/shape diversity ต้องแยกจาก physical fitness และบันทึก raw scale แยก งานนี้วัด opportunity set เดิม ไม่ขยาย geometry, ไม่เสนอ topology ใหม่, ไม่พิสูจน์ novelty และไม่อ้าง physical validation
