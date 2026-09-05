# Work 102 Result: Literature and Simulator Gap Review

Thai companion: `2026-09-05_102_literature-simulator-gap-review-result.th.md`

Status: Completed

## Outcome and changed files

Created eight documents: the four English/Thai Work 102 plan/result records; `docs/reports/LITERATURE_AND_SIMULATOR_GAP_REVIEW_2026-09-05.md` and `.th.md`; `docs/research/RELATED_WORK_CATALOG_2026-09-05.md` and `.th.md`. No code, configuration or existing experiment outputs changed.

Cataloged 62 academic works and 8 industry/tool sources with primary links, E/A/M reading depth and limitations. Publication and preprint-deposit dates are distinguished where needed; versions of the same paper are not double-counted. Neither a systematic review nor full reading of every paper is claimed.

## Decisions and evidence

- Assessed `251ede5` and current source/results through Work 097, rather than treating the early README as the complete implementation.
- Work 088 has `candidate_verdict=not_ready` and 0/11 ready; Work 076 is a 50 m circle, not real-circuit minimum-time optimization.
- Work 097 lines 193–194 of `generalized_geometry_benchmarks.py` construct residual identities and `solver_converged=True`; they are not independent field-equilibrium evidence. Preserved the distinction from genuine CalculiX calls in the older campaign.
- Work 062 has 21/72 = 29.17% promoted-candidate refinement rejection; p = 0.5 and p = 0.0625 do not support superiority at 0.05.
- Did not invent a percentage or years-to-F1 estimate without matched vehicle/track/measurement data and protocol.
- Recommended independent geometry evaluation, a correlated racing baseline, design/controller fairness and rejected-candidate audits before broader QD/free-topology claims. Preserved open-ended architecture and reserved Works 098–101 for the existing roadmap.

## Validation

Commands ran in `C:\Formula Ultimate`, with each gate's exit status checked separately:

```powershell
python -m unittest discover -s tests -q
```

Exit 0: `Ran 689 tests in 285.212s`, `OK (skipped=7)`. Software validation, not physical validation.

```powershell
python -m unittest discover -s tests -p test_repository_contract.py -q
```

Exit 0: `Ran 6 tests in 2.459s`, `OK`. Rechecked after adding results and changing plan status; final passing state verified before commit.

Exact scoped QA command below: exit 0, output `PASS: 62 papers, 8 industry/tool sources; bilingual IDs, primary URLs, key numbers/statuses and local links; retained JSON readable.` This checks URL syntax/parity, not every URL's HTTP availability. Source access was inspected during browsing and limitations are recorded in the catalog.

```powershell
$reviewCheck = @'
from pathlib import Path
import re, json
from urllib.parse import urlparse
root=Path.cwd()
files=[root/'docs/reports/LITERATURE_AND_SIMULATOR_GAP_REVIEW_2026-09-05.md', root/'docs/research/RELATED_WORK_CATALOG_2026-09-05.md']
for en in files:
    th=en.with_name(en.stem+'.th.md')
    a,b=en.read_text(encoding='utf-8'),th.read_text(encoding='utf-8')
    assert '`'+en.name+'`' in b
    for f,t in [(en,a),(th,b)]:
        for target in re.findall(r'\]\(([^)]+)\)',t):
            if target.startswith('https://'):
                assert urlparse(target).netloc and ' ' not in target
            else:
                assert (f.parent/target).resolve().is_file(), (f,target)
    if 'CATALOG' in en.name:
        for t in [a,b]:
            assert re.findall(r'^### (P\d+) ',t,re.M)==[f'P{i:02d}' for i in range(1,63)]
            assert re.findall(r'^### (I\d+) ',t,re.M)==[f'I{i:02d}' for i in range(1,9)]
        assert re.findall(r'\]\((https://[^)]+)\)',a)==re.findall(r'\]\((https://[^)]+)\)',b)
    else:
        nums=['689','285.212','2,880','2,107','773','29.17%','0.1667','0.0625','-2.232959','22.14108931044568','0.0014270788520555852','0.0042775693130952114','0.007','0.000001','44%','8.7%']
        for x in nums: assert x in a and x in b, x
        for ident in re.findall(r'\b[PI]\d{2}\b',a+b):
            assert 1 <= int(ident[1:]) <= (62 if ident[0]=='P' else 8)
        for status in ['not_ready','not_run_pre_admission_blocked','design_use_allowed=false','arbitrary_3d_nonlinear_contact_solved=false']:
            assert status in a and status in b
for work in ['088','097']:
    value=json.loads((root/f'artifacts/work{work}/run_a/result.json').read_text(encoding='utf-8'))
    assert value
assert abs(21/72*100-29.17)<0.005
print('PASS: 62 papers, 8 industry/tool sources; bilingual IDs, primary URLs, key numbers/statuses and local links; retained JSON readable.')
'@
$reviewCheck | python -
```

Git sequence after validation:

```powershell
git diff --check
git add -- docs/reports/LITERATURE_AND_SIMULATOR_GAP_REVIEW_2026-09-05.md docs/reports/LITERATURE_AND_SIMULATOR_GAP_REVIEW_2026-09-05.th.md docs/research/RELATED_WORK_CATALOG_2026-09-05.md docs/research/RELATED_WORK_CATALOG_2026-09-05.th.md docs/work_logs/2026-09-05_102_literature-simulator-gap-review-plan.md docs/work_logs/2026-09-05_102_literature-simulator-gap-review-plan.th.md docs/work_logs/2026-09-05_102_literature-simulator-gap-review-result.md docs/work_logs/2026-09-05_102_literature-simulator-gap-review-result.th.md
git diff --cached --stat
git diff --cached --check
git commit -m "docs: assess simulator gaps and catalog related research"
git log -1 --oneline
git status --short
```

Inspect staged scope for exactly these eight files, stopping immediately if any gate exits nonzero. The verified commit hash is reported in the final handoff to avoid a self-referential hash in the committed file. No push or history rewrite.

## Limitations and follow-up

Historical campaigns and third-party solvers were not rerun. No tyre-data purchase/access was obtained. This documentation work does not repair residuals or mechanics. F1 internals are only partially public; some papers were accessible only through abstracts or metadata. The report specifies independent/dependent variables, controls, metrics, pass/fail criteria, supporting/contradicting evidence, alternatives and confidence for proposed follow-up studies. Each implementation requires its own future work item.
