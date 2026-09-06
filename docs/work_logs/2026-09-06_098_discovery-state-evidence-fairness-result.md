# Work 098 Result: Discovery State, Evidence and Fairness Contract

Thai companion: `2026-09-06_098_discovery-state-evidence-fairness-result.th.md`

Date: 2026-09-06 (Asia/Bangkok)

Status: Completed

## Outcome and files changed

Implemented the bounded Work 098 software contract against the dated whole-vehicle discovery protocol. Starting revision: `7afb91e`. No legacy implementation, governing protocol or backup was changed.

- New modules: `src/formula_ultimate/experiments/discovery_registration.py`, `discovery_evidence.py`, `discovery_ledger.py`, `discovery_audit.py`.
- Fixture registration: `config/experiments/discovery_contract_fixture_v1.json`.
- Executable fixture: `scripts/experiments/run_discovery_contract.py`.
- Adversarial acceptance tests: `tests/test_discovery_contract.py`.
- Interface/limitations documentation: `docs/contracts/DISCOVERY_STATE_EVIDENCE_FAIRNESS_V1.md` and `.th.md`.
- This result, matching plan, and both Thai companions. Intended commit scope: 13 new files.
- Ignored retained artifacts: `artifacts/work098/pilot_01/`, `run_a/`, `run_b/`, `full_suite.txt`, `full_suite.exit.txt`.

## Decisions and demonstrated behavior

- Outcome dimensions are independent; first geometry/boundary identities can be sealed once. Subsequent changes require descendants or separate registered evaluation scopes.
- Physical limit exceedance returns a normal measured failure. Divergence, timeout, unsupported domains, never-invoked physics and corrupt provenance remain distinct.
- Exploratory integration is a permission to attempt a coupled evaluation with explicit omissions. Promotion requires registered evidence and use; fixture decisions cannot become scientific counts.
- Single-writer serial events reserve before invocation and settle once. All treatments/seeds receive identical separate pool opportunities. Retries follow the latest unresolved attempt; caches preserve exact context/result and incur the full registered debit.
- Overshoot remains observable and stops the campaign. Started-work recovery retains an unknown actual cost rather than fabricating a measurement; current scientific counts are blocked until accounting is admissible. V1 does not reconcile unknown recovered spending into a later scientific run.
- Score-independent stratified audit selection records inclusion probabilities. Error rates use reference-class denominators within strata; unknown labels remain unknown and there is no pooled or population-confidence claim.
- Replay checks both event hashes and semantic rules. Trusted head checkpoints detect complete-row rollback. Numerical comparison separately pins tolerances and reports variable timing.
- Fixture registration numbers exercise the schema, not physical thresholds or a powered scientific experiment. Actual external evaluator provenance remains a trusted producer obligation.

## Replay and identity evidence

- Final registration SHA-256: `c9f2e8c9b3aae3d7db0c394f716dce7d42212fc8effa1ae61a23bac49e14185e`.
- Final ledger head SHA-256, both runs: `8960544be31fd765f8d0f0bcf00124ebe4b1f62a22baeb2cc62e90864403a64e`.
- Final reduced-state SHA-256, both runs: `9e2857a9220e02ff3ced65b63ba139f5bb27688212fe4b9bf965a82daa9f7eaf`.
- Final report SHA-256, both runs: `b9cf48c3264dc01c7c6d2a34b8b203a73b23e079e18c53601ace43b417281795`.
- Final mixed fixture: 7 candidates, 25 attempts, 88 ledger events, exact decision replay, byte-identical ledgers, 0 scientific survivors.
- The injected lost-output case intentionally reports `accounting_complete: false` and `unknown_actual_cost`. One stratum has a synthetic false negative; another has unknown reference evidence and status `not_estimable`. These are contract checks, not search-performance estimates.
- The earlier `pilot_01` run passed before the final fidelity-rank and reporting refinements. Its older hashes are developmental evidence only, not the final replay reference.

## Exact validation commands and observed results

Environment: Windows / PowerShell, Python 3.14.3. Commands are separate gates unless the block explicitly preserves the Python exit status.

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

The first `python -m unittest discover -s tests -q` launch returned an ongoing process. After task continuation its process handle was unavailable and no matching test process remained; its exit status is unknown and is not counted as a pass. The full suite was restarted with durable output and explicit exit-code preservation:

```powershell
python -m unittest discover -s tests -q *> artifacts/work098/full_suite.txt
$fullSuiteExitCode = $LASTEXITCODE
Set-Content -LiteralPath artifacts/work098/full_suite.exit.txt -Value $fullSuiteExitCode
exit $fullSuiteExitCode
```

Verified full-suite rerun: exit 0; `Ran 759 tests in 321.874s`; `OK (skipped=7)`. The durable exit file contains `0`. No failing test was hidden by a later command. The 7 skips are reported by the suite; the quiet output does not list their individual reasons.

Documentation verification: exit 0; 3 bilingual pairs with matching technical tokens, fenced content and numbered sections; 4 valid local links. Explicit staged scope contains only the 13 intended new files. `git diff --cached --check` passed with exit 0 and no output. Git's LF/CRLF advisories concern later checkout conversion, not validation failures.

Exact additional verification commands:

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


## Falsification, confidence and limitations

Supporting evidence: adversarial tests attempt to forge status, identity, producer, units, numerical admission, cache result, retry ancestry, registration and ledger history. Two independent fixture executions produce identical decision evidence. Legacy regressions remain passing.

Contradicting/missing evidence: no actual CAD or field solver executes; fixture geometry and response data are synthetic. The lost-output control deliberately prevents complete scientific accounting. Hashes cannot authenticate an invented external validation source. Exact-context admission does not establish numerical applicability outside that context.

Alternative explanation for fixture success: the supplied synthetic cases satisfy a bounded software contract; that does not establish discovery capability, real solver correctness, real compute fairness or statistical superiority. Confidence is limited to the exercised software behavior, not physical feasibility or a complete vehicle.

No external watchdog, distributed executor, general stochastic-repeat protocol, shared cross-candidate cache, population-inference engine or QD implementation is included. Unknown-cost recovery remains diagnostic. An untrusted event producer could omit work or fabricate measurements; real campaigns require independently verified instrumentation and evaluator provenance.

## Follow-up and commit boundary

Work 099 should implement executable morphology/architecture/interface mutations and bounded archives using this contract. Work 100 must provide actual validated local/coupled evidence and preregistered contrasts; Work 101 must demonstrate vehicle integration and stronger promotion. No admitted experiment or push was performed.

Plan scope deviations: none. The interrupted full-suite observation is retained above and replaced by a verified rerun before commitment. The final commit hash will be reported in the handoff rather than embedded into its own commit.
