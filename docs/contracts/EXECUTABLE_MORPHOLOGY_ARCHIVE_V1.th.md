# Contract Morphology, Architecture และ Archive ที่ Execute ได้ V1

ต้นฉบับภาษาอังกฤษ: `EXECUTABLE_MORPHOLOGY_ARCHIVE_V1.md`

Status: Implemented by Work 099

## 1. ขอบเขตและ claim boundary

Contract นี้ implement morphology loop ที่ execute ได้แบบจำกัดบน Work 098 discovery ledger โดยยืนยันว่า numerical genes สามารถสร้าง CadQuery solids จริง เปลี่ยน measured geometry เปลี่ยน part/interface decomposition เก็บ typed terminal ancestry และเติม deterministic bounded archives ได้ Evidence scope คือ `software_fixture_with_executed_cad` / `morphology_software_fixture_only`

ผลลัพธ์ไม่ใช่ physical feasibility, manufacturing feasibility, race performance, technology novelty หรือ physical validation ไม่มี field solver ทำงาน ชื่อ archive `feasible`, `failed` และ `unresolved` อธิบายเฉพาะ morphology software fixture ที่ลงทะเบียนนี้ ห้าม relabel เป็น Work 100 physics states หรือ scientific survivors Registration ของ Work 098 ที่นำมาใช้มี evidence class `software_fixture` และ runner บังคับให้จำนวน scientific survivor คงเป็นศูนย์

## 2. Representation ที่ execute ได้

`src/formula_ultimate/search/executable_morphology.py` กำหนด `executable_swept_network_v1` Genotype ประกอบด้วย:

- material regions/parts แบบ variable-length;
- node positions หน่วย SI metre ที่ finite และ radius fields ที่มีขอบเขต;
- swept-solid edges ที่เชื่อมต่อกันภายในแต่ละ part;
- typed part interfaces พร้อม endpoint-node และ ancestry records;
- external terminals พร้อม role, domains และ ancestry;
- optional registered controller gene

Implementation รองรับสูงสุด 8 parts, 24 nodes ต่อ part, 32 edges ต่อ part, 16 interfaces และ 12 terminals ภายใต้ fixture ที่ commit Radius อยู่ใน `[0.002, 0.04] m`, coordinates อยู่ใน `±0.5 m` และ edge length ต้องไม่น้อยกว่า `0.002 m` ทุก part และ part-interface architecture ต้องเชื่อมต่อกัน ต้องมี source/sink terminals ค่า non-finite, stale node references, ancestry ที่หาย และกราฟไม่เชื่อมต่อจะ fail ก่อน CAD

V1 นี้เป็น swept sphere/cylinder solid-network representation ไม่ใช่ arbitrary CAD รองรับหลาย physical regions โดยไม่บังคับ universal single solid หรือ conventional vehicle layout

## 3. Registered operators และ lineage

Operator schedule ที่แน่นอนคือ:

1. `perturb_node`
2. `grow_branch`
3. `split_part`
4. `rewire_interface`
5. `merge_parts`
6. `mutate_radius_field`
7. `mutate_controller`

ทุก call ตรึง parent/child genotype digests, parent/child functional signatures, seed, step, numerical parameters และการประกาศว่า geometry/architecture เปลี่ยนหรือไม่ `split_part` ย้ายได้เฉพาะ leaf ที่ไม่ใช่ terminal/interface ไป material region ใหม่และเพิ่ม typed interface พร้อม split ancestry ส่วน `merge_parts` ใช้ interface รวม endpoint nodes และเขียน terminals/interfaces ที่ได้รับผลใหม่โดยไม่ลบ ancestry การเปลี่ยน controller อย่างเดียวไม่ถูกเรียกว่า geometry change

Functional signature ไม่ขึ้นกับ ID และ refine part labels จาก internal node degree, terminal role/domain/ancestry และ typed neighboring interfaces เป็น deterministic diversity signature สำหรับ representation แบบจำกัดนี้ ไม่ใช่ proof ทั่วไปของ graph isomorphism หรือ functional novelty

## 4. CAD execution และ measurement

`scripts/experiments/run_executable_morphology_qd.py` สร้าง sphere หนึ่งลูกที่แต่ละ node และ cylinder หนึ่งแท่งต่อ edge, fuse แต่ละ connected part และ export parts เป็น STEP compound Canonicalize export timestamps ก่อน hash ไม่อนุญาต automatic geometry healing

สำหรับ genotype ที่สำเร็จทุกตัว runner บันทึก:

- STEP SHA-256 และ measurement SHA-256;
- volume หน่วย `m^3`, surface area หน่วย `m^2`, bounds และ centre หน่วย `m`;
- จำนวน solid, face และ edge;
- volume/area ต่อ part;
- terminal positions, roles, domains และ ancestry;
- boundary identity ที่ derive จาก measured terminals และ declared interfaces

Geometry operator ทุกตัวที่ประกาศต้องเปลี่ยน STEP digest และ measured field อย่างน้อยหนึ่งค่าเทียบ parent `split_part`/`merge_parts` แสดง decomposition change ด้วย solid/topology counts ได้แม้ occupied material รวมใกล้เดิม Transform-only หรือ identifier-only changes ไม่ได้ลงทะเบียนเป็น geometry operators

## 5. การเชื่อมกับ Work 098 ledger

Genotype แต่ละตัว append เป็น Work 098 candidate พร้อม immutable parent links และ mutation trace การตรวจ geometry/CAD execution และ terminal binding ถูก reserve, start และ settle แยกกัน Execution ที่สำเร็จ seal `geometry_sha256`; terminal binding ที่สำเร็จ seal `boundary_sha256` ตัวอย่าง zero-length ที่ฉีดไว้เป็น `representation_invalid` ส่วน valid CAD specimen หนึ่งตัวได้รับ diagnostic ambiguous-terminal ที่ระบุชัดว่า synthetic และเป็น `boundary_unresolved` ทั้งสองไม่ถูกยุบเป็น physical failure

CPU/wall time และ CAD/attempt counters ที่สังเกตจริงถูกคิดใน Work 098 ledger ส่วน archive ใช้ deterministic opportunity cost (`attempts + geometry_executions + cad_calls`) สำหรับการเรียง โดยเก็บ CPU/wall timing ที่เปลี่ยนได้เป็นหลักฐานแยก วิธีนี้ป้องกัน runtime noise เปลี่ยน cross-run archive identity โดยไม่ซ่อน timing ที่วัดจริง

Ledger เปิดใหม่ด้วย trusted head Exact decision replay หมายถึง stored events เดิมสร้าง state/accounting เดิมได้ตรงกัน Cross-run execution replay เทียบ genotype, functional, STEP และ measurement identities, numerical fields ภายใต้ registered tolerances และ archives ส่วน timing ถูกรายงานแต่ไม่ใช้เทียบ identity

## 6. Bounded quality-diversity archive

Niches ใช้ causal/topological descriptors แทน visual curvature:

- จำนวน part;
- part-interface cycle rank;
- internal branch-node count;
- terminal-domain count

แต่ละ niche มี slots แยกและจำกัดเป็น `feasible: 2`, `failed: 1`, `unresolved: 1` Feasible records เรียงด้วย fixture quality แล้ว novelty/cost; failed records เรียงด้วย measured margin แล้ว novelty/cost; unresolved records ให้ deterministic opportunity cost ต่ำก่อน Stable candidate-ID tie-breaking ทำให้ decision replay ได้ Novelty เปลี่ยน disposition, ลบ failure หรือขยาย evidence scope ไม่ได้

Reproduction caps ต่อ niche คือหนึ่ง record จากแต่ละ disposition นี่สาธิต bounded stepping-stone permissions ไม่ใช่ empirical claim ว่าการให้ failed/unresolved reproduce ทำให้ discovery ดีขึ้น Archive entries ที่ถูก evict ยังคง immutable อยู่ใน Work 098 ledger แม้ active archive มีขอบเขต

## 7. คำสั่งและหลักฐาน

รัน pure contract tests ด้วย repository Python:

```powershell
python -m unittest tests.test_executable_morphology_qd -v
```

รัน tests ทั้งหมดรวม actual CadQuery execution และ fixtures อิสระสองรอบ:

```powershell
$env:PYTHONPATH = (Join-Path $PWD 'src')
& '.tools/cadquery-mcp/Scripts/python.exe' -m unittest tests.test_executable_morphology_qd -v
& '.tools/cadquery-mcp/Scripts/python.exe' scripts/experiments/run_executable_morphology_qd.py --output-dir artifacts/work099/run_a
& '.tools/cadquery-mcp/Scripts/python.exe' scripts/experiments/run_executable_morphology_qd.py --output-dir artifacts/work099/run_b --replay-reference artifacts/work099/run_a/result.json
```

Final verified runs มี 18 candidates, geometry-change proofs 10 รายการ, functional signatures 6 แบบ และ archive niches 3 ช่อง Ledger แต่ละชุดมี append-only rows 120 แถวและเปิดซ้ำที่ trusted head ได้ตรงกัน Cross-run deterministic evidence SHA-256 คือ `727b75d305bb6e0ae7111d553c73ee9fc8f4cae059e7d5a8602abbfcd2d4515d`; geometry measurements ที่เทียบทั้งหมดต่างกัน `0.0` ใน rerun ที่สังเกต Active bounded archive เก็บ fixture records 5 feasible, 1 failed และ 1 unresolved ตัวเลขเหล่านี้อธิบาย software fixture ไม่ใช่ search performance

## 8. ข้อจำกัดและงานต่อ

Implementation นี้ไม่มี geometry-derived stress, thermal, flow, contact, motion หรือ energy field solver; ไม่มี manufacturing process evaluator; ไม่มี vehicle task; ไม่มี optimization baseline; และไม่มี statistical archive-retention experiment CAD validity/reproducibility ไม่ยืนยัน usefulness Functional signature อาจชนกันสำหรับกราฟ non-isomorphic บางแบบ เพราะเป็น bounded refinement signature ไม่ใช่ exhaustive isomorphism solver

Work 100 ต้องเพิ่ม independently validated, geometry-derived local/coupled evaluators และ preregistered contrasts ก่อนตีความใดเป็น `physically_feasible` หรือ `candidate_survivor` ส่วน Work 101 ยังรับผิดชอบ complete-vehicle integration, holdout/independent promotion และ fair optimized baseline evidence
