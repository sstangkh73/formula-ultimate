# ผล Work 099: การค้นหา Morphology, Architecture และ Archive ที่ Execute ได้

ต้นฉบับภาษาอังกฤษ: `2026-09-06_099_executable-morphology-architecture-archive-result.md`

วันที่: 2026-09-06 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และไฟล์ที่เปลี่ยน

Implement deliverable executable-morphology Work 099 แบบจำกัด หลังตรวจ Work 098 commit `ec0004b` ที่เสร็จแล้ว Numerical swept-solid genes สามารถ execute ใน CadQuery, architecture operators split/merge parts และ rewire typed interfaces, measured geometry/terminal ancestry เข้า Work 098 ledger และ bounded multi-disposition archive replay แบบ deterministic ไม่มีไฟล์ Work 098 ที่เสร็จแล้วหรือ historical roadmap ถูกแก้

ขอบเขต commit ที่ตั้งใจคือ 11 ไฟล์:

- `src/formula_ultimate/search/executable_morphology.py`
- `src/formula_ultimate/search/morphology_archive.py`
- `config/experiments/executable_morphology_qd_v1.json`
- `scripts/experiments/run_executable_morphology_qd.py`
- `tests/test_executable_morphology_qd.py`
- `docs/contracts/EXECUTABLE_MORPHOLOGY_ARCHIVE_V1.md` และ `.th.md`
- ผลนี้ แผนที่ตรงกัน และ companion files ของทั้งสองภาษา

Generated evidence เก็บใต้ ignored `artifacts/work099/` รวม final `run_a`, `run_b`, `full_suite.txt`, `full_suite.exit.txt` และ developmental pilots ที่เก็บไว้

## ข้อตัดสินใจและพฤติกรรมที่ implement

- เพิ่ม genotype `executable_swept_network_v1` แบบ strict พร้อม node/radius fields หน่วย SI metre ที่ finite, material regions ที่เชื่อมต่อ, typed interfaces, terminal ancestry และ optional controller genes ขอบเขตชัดและ fail closed
- เพิ่ม deterministic operators `perturb_node`, `grow_branch`, `split_part`, `rewire_interface`, `merge_parts`, `mutate_radius_field` และ `mutate_controller` Child ทุกตัวเก็บ parameters และ parent/child identities ตรงจริง แยกการประกาศ geometry/architecture change
- `split_part` ย้าย terminal หรือ existing interface endpoint ไม่ได้ ส่วน `merge_parts` รวม consumed interface nodes และเขียน dependent terminals/interfaces ใหม่โดยคง lineage
- CadQuery execute spheres และ swept cylinders จาก numerical genes, validate connected region แต่ละส่วน, export canonicalized STEP และวัด volume, area, bounds, centre, จำนวน solid/face/edge, measurements ต่อ region และ terminal positions
- Geometry operator ที่ลงทะเบียนทุกตัวต้องเปลี่ยนทั้ง STEP digest และ measured field อย่างน้อยหนึ่งค่า Identifier/controller-only changes ผ่าน gate นี้ไม่ได้
- Work 098 candidate, reservation, start และ settlement events คิดต้นทุนทุก proposal/attempt Geometry/boundary identities seal แยก ตัวอย่าง zero-length เป็น `representation_invalid` ส่วน ambiguous-terminal fixture ที่ CAD valid หนึ่งตัวเป็น `boundary_unresolved`
- Archive ใช้ part count, interface cycle rank, branch-node count และ terminal-domain count แต่ละ niche จำกัด morphology-fixture `feasible`, `failed` และ `unresolved` แยก Novelty ลบ failure หรือขยาย claim scope ไม่ได้
- CPU/wall timings ที่เปลี่ยนได้ยังอยู่ใน ledger/report ส่วน deterministic archive ordering ใช้ registered opportunity counters เพื่อไม่ให้ runtime noise เปลี่ยน cross-run decisions

## หลักฐาน CAD execution และ replay

Final runs ทั้งสองสร้าง:

- candidate records 18 ตัวจาก seeds `7` และ `19`;
- geometry-change proofs ชัด 10 รายการ;
- bounded functional signatures ต่างกัน 6 แบบ;
- archive niches 3 ช่องซึ่งเก็บ software-fixture records 5 feasible, 1 failed และ 1 unresolved;
- append-only ledger rows 120 แถวต่อ run;
- scientific survivors เป็นศูนย์และ `physical_validation: false`

Deterministic evidence SHA-256 ร่วมคือ `727b75d305bb6e0ae7111d553c73ee9fc8f4cae059e7d5a8602abbfcd2d4515d` ส่วน final archive SHA-256 คือ `5c9d0ec677f936dbb64be16da749e85512c61bf21c8cf3f6aefdafce17024091` Cross-run execution comparison เป็น `identity_exact: true` โดย maximum absolute/relative geometry-measurement differences ที่สังเกตเป็น `0.0` ทั้งคู่ Timing รายงานแยกและไม่ถือเป็น identity

แต่ละ ledger เปิดซ้ำตรง trusted head เพราะ actual CPU/wall observations ต่างกัน ledger head/state hashes ระหว่าง independent executions จึงต่างกันอย่างถูกต้อง Exact decision replay ใช้กับการเปิด immutable event stream แต่ละชุด ส่วน cross-run execution replay ใช้ registered geometry/measurement tolerances

ตัวอย่าง decomposition evidence:

- seed `7` split: STEP `0cbc1f5b7b48338acfb91b9eaf4bdd82895401f1c2c69ae257dcb4dbaa6dfd1b`, 3 solids, 29 faces, 61 edges;
- seed `7` merge: STEP `1979f64530fde895138bbc503371d9b4fd0561ba5a782ac9b86c5f7cfce4b6e1`, 2 solids, 28 faces, 63 edges;
- seed `19` split: STEP `782371b0298f58560a7408c3578a3f4e8b25e1742bf61d7dae27dc4864f6ce7c`, 3 solids, 28 faces, 60 edges;
- seed `19` merge: STEP `a4c3f091bba36c69cd33dc2d171296f1c021cbef72f2c93d35236a2fbd878030`, 2 solids, 27 faces, 63 edges

ทั้งหมดเป็น CAD morphology/decomposition observations ไม่ใช่ structural/functional physics evidence

## คำสั่ง validation จริงและผลที่สังเกต

Pure contract suite:

```powershell
python -m unittest tests.test_executable_morphology_qd -v
# initial: exit 0; 10 passed, 1 CadQuery test skipped

python -m unittest tests.test_executable_morphology_qd -q
# after seed-19 split regression: exit 0; Ran 12 tests; OK (skipped=1)
```

การเรียก CadQuery suite ครั้งแรก exit `1` ก่อนโหลด tests เพราะ isolated environment ไม่มี repository `src` ใน `sys.path`: `ModuleNotFoundError: No module named 'formula_ultimate'` จึงรันซ้ำด้วย `PYTHONPATH` ชัด โดยไม่เปลี่ยน installed packages:

```powershell
$env:PYTHONPATH = (Join-Path $PWD 'src')
& '.tools/cadquery-mcp/Scripts/python.exe' -m unittest tests.test_executable_morphology_qd -v
# final current-code run: exit 0; Ran 12 tests in 3.140s; OK
```

คำสั่ง final real-CAD fixtures:

```powershell
$env:PYTHONPATH = (Join-Path $PWD 'src')
& '.tools/cadquery-mcp/Scripts/python.exe' scripts/experiments/run_executable_morphology_qd.py --output-dir artifacts/work099/run_a
# exit 0; 18 candidates; 6 signatures; exact decision replay

& '.tools/cadquery-mcp/Scripts/python.exe' scripts/experiments/run_executable_morphology_qd.py --output-dir artifacts/work099/run_b --replay-reference artifacts/work099/run_a/result.json
# exit 0; deterministic SHA-256 เดียวกัน; identity exact; measurement differences 0.0
```

Targeted regression และ compile gates:

```powershell
python -m unittest tests.test_discovery_contract tests.test_topology_genome tests.test_topology_mutation tests.test_freeform_solid_grammar tests.test_repository_contract -q
# exit 0; Ran 91 tests in 18.437s; OK (skipped=2)

python -m compileall -q src scripts tests
# exit 0
```

Full suite เก็บ exit status ของตัวเอง:

```powershell
python -m unittest discover -s tests -q *> artifacts/work099/full_suite.txt
$work099FullSuiteExit = $LASTEXITCODE
Set-Content -LiteralPath artifacts/work099/full_suite.exit.txt -Value $work099FullSuiteExit
exit $work099FullSuiteExit
# exit 0; Ran 771 tests in 301.188s; OK (skipped=8)
```

Skipped tests ขึ้นกับ environment รวม real-CAD Work 099 test ภายใต้ repository Python โดย test เดียวกันนั้นผ่านใต้ pinned CadQuery environment ข้างต้น

## Defects ที่พบและหลักฐานที่เก็บ

Full runner pilot แรกหยุดใน seed `19` ด้วย `interface node is missing` Selector ของ `split_part` อนุญาตให้ existing interface leaf ถูกย้ายไป region ใหม่ ทำให้ interface เดิม stale ตอนนี้ selector กันทั้ง external-terminal และ interface endpoints พร้อม direct regression ครบทุก registered seed Failed pilot อยู่ที่ `artifacts/work099/pilot_failed_interface_endpoint/`

Cross-run pilot ถัดมาหยุดด้วย `replay archive differs` เพราะใช้ actual wall time เป็น unresolved/archive cost tie-break ทำให้ runtime noise เปลี่ยน archive identity ตอนนี้ archive cost ใช้ deterministic attempt/geometry/CAD opportunity counters ขณะที่ actual CPU/wall time ยังคิดและรายงานแยก หลักฐานก่อนแก้อยู่ใต้ `pilot_pre_deterministic_cost/` และ `pilot_failed_archive_replay/`

ไม่มี failed run ถูก relabel เป็นผ่านและไม่มีหลักฐานถูกลบเพื่อทำให้ replay สำเร็จ

## การหักล้าง confidence และข้อจำกัด

Supporting evidence มี adversarial tests สำหรับ non-finite, short-edge, stale-interface, missing-ancestry, claim-scope, overwrite และ archive-cap; สอง seeds; actual CAD execution; exact trusted-head reopening; และ repeated execution อิสระที่ให้ geometry evidence ตรงกัน

Contradicting/missing evidence สำคัญมากสำหรับ claims เหนือ Work 099: ไม่มี stress, thermal, flow, contact, motion หรือ energy field solve; ไม่มี process evaluator; ไม่มี vehicle task; ไม่มี race baseline; และไม่มี statistical archive-retention comparison Archive `feasible` หมายถึง executable morphology-fixture success เท่านั้น Functional signature เป็น bounded color refinement และอาจชนกันสำหรับกราฟ non-isomorphic บางแบบ

Alternative explanation ของผลสำเร็จคือ swept-solid representation และ mutations ที่เลือกเหมาะกับ CadQuery fixture นี้ ไม่ได้ยืนยันว่า arbitrary geometry execute ได้, archive ทำให้ search ดีขึ้น หรือ candidate ใดมี useful physical behavior Confidence สูงสำหรับ software/CAD invariants ที่ทดสอบและจำกัดอยู่แค่นั้น

Work 100 ต้องเพิ่ม independently validated geometry-derived local/coupled evidence และ preregistered contrasts ส่วน Work 101 ยังรับผิดชอบ complete-vehicle integration และ stronger promotion ไม่มี admitted experiment, physical/discovery claim, external publication, push หรือ history rewrite

Final documentation QA ผ่าน: คู่สองภาษา 3 คู่คง English-source names, numbered sections, executable commands, technical claim-boundary tokens และ valid local links `python -m unittest tests.test_repository_contract -q` ผ่าน 6 tests ใน `0.640s` และ `git diff --check` exit `0` โดยไม่มี output Explicit staging แสดงเฉพาะ 11 ไฟล์ที่ตั้งใจ ส่วน `git diff --cached --check` exit `0` โดยไม่มี output ข้อความ LF/CRLF ของ Git อธิบายการแปลงเมื่อ checkout ภายหลัง ไม่ใช่ validation failure รายงาน verified commit hash ใน handoff เพราะ commit ไม่สามารถบรรจุ hash ของตัวเองได้
