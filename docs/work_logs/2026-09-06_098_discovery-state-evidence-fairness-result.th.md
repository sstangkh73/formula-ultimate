# ผล Work 098: Contract สถานะ หลักฐาน และความเป็นธรรมของการค้นหา

ต้นฉบับภาษาอังกฤษ: `2026-09-06_098_discovery-state-evidence-fairness-result.md`

วันที่: 2026-09-06 (Asia/Bangkok)

Status: Completed

## ผลลัพธ์และไฟล์ที่เปลี่ยน

Implement software contract ของ Work 098 แบบจำกัดตาม whole-vehicle discovery protocol ลงวันที่ Revision เริ่มต้น: `7afb91e` ไม่เปลี่ยน legacy implementation, governing protocol หรือ backup

- Modules ใหม่: `src/formula_ultimate/experiments/discovery_registration.py`, `discovery_evidence.py`, `discovery_ledger.py`, `discovery_audit.py`
- Fixture registration: `config/experiments/discovery_contract_fixture_v1.json`
- Executable fixture: `scripts/experiments/run_discovery_contract.py`
- Adversarial acceptance tests: `tests/test_discovery_contract.py`
- เอกสาร interface/limitations: `docs/contracts/DISCOVERY_STATE_EVIDENCE_FAIRNESS_V1.md` และ `.th.md`
- ผลนี้ แผนที่ตรงกัน และคู่ภาษาไทยทั้งสอง ขอบเขต commit ที่ตั้งใจ: ไฟล์ใหม่ 13 ไฟล์
- Ignored artifacts ที่เก็บไว้: `artifacts/work098/pilot_01/`, `run_a/`, `run_b/`, `full_suite.txt`, `full_suite.exit.txt`

## ข้อตัดสินใจและพฤติกรรมที่สาธิต

- Outcome dimensions แยกกัน Geometry/boundary identities แรก seal ได้ครั้งเดียว การเปลี่ยนภายหลังต้องเป็น descendants หรือ registered evaluation scopes แยก
- การข้ามขีดจำกัดกายภาพเป็น measured failure ปกติ ส่วน divergence, timeout, unsupported domains, physics ที่ยังไม่เรียก และ corrupt provenance แยกกัน
- Exploratory integration ให้สิทธิ์ลอง coupled evaluation พร้อมระบุสิ่งที่ขาด Promotion ต้องมี registered evidence/use และ fixture decisions เข้า scientific counts ไม่ได้
- Single-writer serial events reserve ก่อน invocation และ settle ครั้งเดียว ทุก treatments/seeds ได้ pool opportunities ที่เหมือนกันและแยกกัน Retries ตาม unresolved attempt ล่าสุด ส่วน caches คง context/result เดิมและคิด full registered debit
- Overshoot มองเห็นได้และหยุด campaign การ recovery งานที่เริ่มแล้วเก็บ actual cost ว่าไม่ทราบ ไม่แต่ง measurement และ current scientific counts ถูกบล็อกจนบัญชี admissible V1 ไม่ reconcile ยอด recovery ที่ไม่ทราบให้กลับเข้า scientific run ภายหลัง
- Score-independent stratified audit selection เก็บ inclusion probabilities Error rates ใช้ reference-class denominators แยก strata ส่วน unknown labels ยังคง unknown และไม่อ้าง pooled/population confidence
- Replay ตรวจทั้ง event hashes และ semantic rules ส่วน trusted head checkpoints ตรวจ complete-row rollback Numerical comparison ตรึง tolerances แยกและรายงาน timing ที่เปลี่ยนได้
- ตัวเลข fixture registration ใช้ทดสอบ schema ไม่ใช่ physical thresholds หรือ scientific experiment ที่คำนวณ power แล้ว Actual external evaluator provenance ยังเป็นหน้าที่ trusted producer

## หลักฐาน replay และ identity

- Final registration SHA-256: `c9f2e8c9b3aae3d7db0c394f716dce7d42212fc8effa1ae61a23bac49e14185e`
- Final ledger head SHA-256 ทั้งสอง runs: `8960544be31fd765f8d0f0bcf00124ebe4b1f62a22baeb2cc62e90864403a64e`
- Final reduced-state SHA-256 ทั้งสอง runs: `9e2857a9220e02ff3ced65b63ba139f5bb27688212fe4b9bf965a82daa9f7eaf`
- Final report SHA-256 ทั้งสอง runs: `b9cf48c3264dc01c7c6d2a34b8b203a73b23e079e18c53601ace43b417281795`
- Final mixed fixture: 7 candidates, 25 attempts, 88 ledger events, exact decision replay, ledgers ตรงทุก byte และ scientific survivors 0
- Lost-output case ที่ฉีดจงใจรายงาน `accounting_complete: false` และ `unknown_actual_cost` Stratum หนึ่งมี synthetic false negative อีก stratum มี reference evidence ที่ไม่ทราบและสถานะ `not_estimable` ทั้งหมดเป็น contract checks ไม่ใช่ค่าประเมิน search performance
- Run `pilot_01` ก่อนหน้าผ่านก่อนปรับ fidelity-rank และ reporting ขั้นสุดท้าย Hashes เก่านั้นเป็น developmental evidence เท่านั้น ไม่ใช่ final replay reference

## คำสั่ง validation จริงและผลที่สังเกต

Environment: Windows / PowerShell, Python 3.14.3 คำสั่งเป็น gates แยกกัน เว้นแต่ block ระบุการรักษา Python exit status ชัดเจน

```powershell
python -m unittest tests.test_discovery_contract -v
# initial implementation: exit 0; 56 tests passed

python -m unittest tests.test_discovery_contract -q
# final acceptance additions: exit 0; 62 tests passed

python -m unittest tests.test_constructive_validity tests.test_generalized_geometry_benchmarks tests.test_campaign_runner tests.test_repository_contract -q
# exit 0; 42 tests passed

python -m compileall -q src scripts tests
# exit 0

python scripts/experiments/run_discovery_contract.py --output-dir artifacts/work098/pilot_01
# exit 0; developmental fixture, exact decision replay

python scripts/experiments/run_discovery_contract.py --output-dir artifacts/work098/run_a
# exit 0; 7 candidates, 25 attempts, 0 scientific survivors

python scripts/experiments/run_discovery_contract.py --output-dir artifacts/work098/run_b --replay-reference artifacts/work098/run_a/result.json
# exit 0; complete report equality and exact decision replay

git diff --check
# exit 0 before staging
```

การเรียก `python -m unittest discover -s tests -q` ครั้งแรกคืน process ที่ยังทำงาน หลังกลับมาทำงานต่อ process handle ใช้ไม่ได้และไม่พบ test process ที่ตรงกัน จึงไม่ทราบ exit status และไม่นับว่าผ่าน รัน full suite ใหม่โดยเก็บ output ถาวรและรักษา exit code ชัดเจน:

```powershell
python -m unittest discover -s tests -q *> artifacts/work098/full_suite.txt
$fullSuiteExitCode = $LASTEXITCODE
Set-Content -LiteralPath artifacts/work098/full_suite.exit.txt -Value $fullSuiteExitCode
exit $fullSuiteExitCode
```

ยืนยัน full-suite rerun: exit 0; `Ran 759 tests in 321.874s`; `OK (skipped=7)` โดย durable exit file มีค่า `0` ไม่มี test ที่ล้มเหลวถูกซ่อนด้วยคำสั่งถัดไป Suite รายงาน 7 skips โดย quiet output ไม่ได้แสดงเหตุผลรายตัว

ตรวจเอกสาร: exit 0; คู่สองภาษา 3 คู่ มี technical tokens, fenced content และ numbered sections ตรงกัน และ local links ใช้ได้ 4 ลิงก์ Explicit staged scope มีเฉพาะไฟล์ใหม่ที่ตั้งใจ 13 ไฟล์ ส่วน `git diff --cached --check` ผ่านด้วย exit 0 ไม่มี output Git แจ้ง LF/CRLF advisories เกี่ยวกับการแปลงเมื่อ checkout ภายหลัง ไม่ใช่ validation failures

คำสั่งตรวจเพิ่มเติมที่รันจริง:

````powershell
@'
from pathlib import Path
import re
pairs = [Path('docs/contracts/DISCOVERY_STATE_EVIDENCE_FAIRNESS_V1.md'), Path('docs/work_logs/2026-09-06_098_discovery-state-evidence-fairness-plan.md'), Path('docs/work_logs/2026-09-06_098_discovery-state-evidence-fairness-result.md')]
links=0
for en in pairs:
    th=en.with_name(en.stem+'.th.md')
    a,b=en.read_text(encoding='utf-8'),th.read_text(encoding='utf-8')
    assert '`'+en.name+'`' in b
    assert '\ufffd' not in a+b
    assert re.findall(r'^## (\d+)\.',a,re.M)==re.findall(r'^## (\d+)\.',b,re.M)
    assert re.findall(r'```[^\n]*\n(.*?)```',a,re.S)==re.findall(r'```[^\n]*\n(.*?)```',b,re.S)
    tokens=lambda s:{t for t in re.findall(r'(?<!`)`([^`\n]+)`(?!`)',s) if not t.endswith('.md')}
    assert tokens(a)==tokens(b),(en,tokens(a)^tokens(b))
    for path,text in ((en,a),(th,b)):
        for target in re.findall(r'\]\(([^)]+)\)',text):
            assert (path.parent / target.split('#')[0]).is_file(),target
            links+=1
print('PASS: 3 bilingual pairs; matching technical tokens/fences/numbered sections;',links,'valid local links')
'@ | python -
````

```powershell
python -m unittest tests.test_repository_contract -q
# final documentation status check: exit 0; 6 tests passed

git diff --cached --name-only

git diff --cached --check
```


## การหักล้าง confidence และข้อจำกัด

Supporting evidence: adversarial tests พยายามปลอม status, identity, producer, units, numerical admission, cache result, retry ancestry, registration และ ledger history การ execute fixture สองรอบแยกกันให้ decision evidence ตรงกัน Legacy regressions ยังผ่าน

Contradicting/missing evidence: ไม่มี CAD หรือ field solver จริงรัน Geometry/response ของ fixture เป็น synthetic ส่วน lost-output control จงใจไม่ให้ scientific accounting ครบ Hashes authenticate validation source ภายนอกที่แต่งขึ้นไม่ได้ และ exact-context admission ไม่ยืนยัน numerical applicability นอก context นั้น

Alternative explanation ของ fixture ที่ผ่าน: synthetic cases ที่ส่งมาตรงกับ software contract แบบจำกัด ไม่ได้ยืนยัน discovery capability, real solver correctness, real compute fairness หรือ statistical superiority Confidence จำกัดอยู่ที่พฤติกรรมซอฟต์แวร์ที่ทดสอบ ไม่ใช่ physical feasibility หรือรถทั้งคัน

ไม่มี external watchdog, distributed executor, general stochastic-repeat protocol, shared cross-candidate cache, population-inference engine หรือ QD implementation ส่วน unknown-cost recovery ยังเป็น diagnostic เท่านั้น Event producer ที่ไม่เชื่อถืออาจละงานหรือแต่ง measurements ได้ Campaign จริงต้องมี instrumentation และ evaluator provenance ที่ตรวจยืนยันอย่างอิสระ

## งานต่อและขอบเขต commit

Work 099 ควร implement executable morphology/architecture/interface mutations และ bounded archives โดยใช้ contract นี้ Work 100 ต้องมี actual validated local/coupled evidence และ preregistered contrasts ส่วน Work 101 ต้องสาธิต vehicle integration และ promotion ที่เข้มกว่า ไม่ได้ทำ admitted experiment หรือ push

Plan scope deviations: none เก็บการสังเกต full-suite ที่ขาดช่วงไว้ข้างต้น และใช้ verified rerun แทนก่อน commit จะรายงาน final commit hash ใน handoff แทนการฝังลง commit ของตัวเอง
