# Work 107 Result: Detailed Work-Package Plans

Thai companion: `2026-09-07_107_detailed-work-package-plans-result.th.md`

Started: 2026-09-07. Continued/result date: 2026-09-09 (Asia/Bangkok).

Status: Completed

## Outcome and exact scope

Expanded Work 106 into [26 separate detailed work plans](../plans/detailed_part_to_vehicle_v1/README.md), each with a Thai companion. Actual Work 107 is this documentation work, so the original proposed packages 107–132 are explicitly mapped to proposed implementation Works 108–133. Historical roadmap and work logs were not rewritten.

Changes are exactly 58 Markdown files: 52 individual plan files, two index files and four Work 107 plan/result files. No runtime source, tests, configurations, dependencies, generated experiment outputs or physical hardware changed. Printed module paths and CLI commands are proposed implementation seams, not existing runnable capabilities.

## Content and decisions

Each package contains nine numbered sections: outcome/inputs; proposed files; four ordered implementation steps; IV/DV/controls; targeted tests/falsification; numerical registration/acceptance; artifacts/handoff; risks/non-goals; and proposed validation/replay commands.

The index provides mandatory execution and evidence rules, prerequisites, numerical fields that must be filled before admitted execution, and old-to-new numbering. Capability dependencies permit early B-rep meshing, interface development and local co-design without claiming missing branches complete. Larger solver or physical-test programs must split into bounded execution works when necessary.

Preserved principles: shape and topology freedom, geometry-causal fields, detailed internal hardware, no free ideal resources, real material ownership, same-topology useful effects, early exploratory integration, scoped reduced models, complete costs, fair controls and explicit unresolved evidence. Physical Works 131–133 require separate authorization and qualified review; proposed runners analyze recorded data offline only.

## Validation commands

Repository contract gate:

```powershell
python -m unittest tests.test_repository_contract -v
```

Read-only plan integrity gate:

```powershell
$workPlanCheck = @'
import re
from pathlib import Path
root = Path.cwd()
directory = root / 'docs/plans/detailed_part_to_vehicle_v1'
english = sorted(p for p in directory.glob('work*.md') if not p.name.endswith('.th.md'))
assert len(english) == 26
ids = [int(re.match(r'work(\d+)-', p.name).group(1)) for p in english]
assert ids == list(range(108, 134)), ids
graph = {}
for p in english:
    pair = [p, p.with_name(p.stem + '.th.md')]
    texts = [q.read_text(encoding='utf-8') for q in pair]
    number = int(re.match(r'work(\d+)-', p.name).group(1))
    assert f'Original Work 106 package: {number - 1}' in texts[0]
    assert f'`{p.name}`' in texts[1]
    for text in texts:
        assert 'Status: Planned' in text
        assert re.findall(r'^## (\d+)\.', text, re.M) == list(map(str, range(1, 10)))
        assert len(re.findall(r'^\d+\. ', text, re.M)) == 4
        for label in ('IV:', 'DV:', 'Controls:'):
            assert label in text
    literals = [set(re.findall(r'(?<!`)`([^`\n]+)`(?!`)', t)) - {q.name for q in pair} for t in texts]
    assert literals[0] == literals[1], (p.name, literals[0] ^ literals[1])
    commands = [re.findall(r'```powershell\n(.*?)```', t, re.S) for t in texts]
    assert commands[0] == commands[1] and len(commands[0]) == 1, p.name
    dep_line = re.search(r'^Dependencies: (.*)$', texts[0], re.M).group(1)
    graph[number] = [int(v) for v in re.findall(r'Work (\d+)', dep_line)]
    th_dep_line = re.search(r'^พึ่งพา: (.*)$', texts[1], re.M).group(1)
    assert graph[number] == [int(v) for v in re.findall(r'Work (\d+)', th_dep_line)]
    assert all(d in ids and d != number for d in graph[number])
visited, active = set(), set()
def visit(node):
    assert node not in active, f'dependency cycle: {node}'
    if node in visited:
        return
    active.add(node)
    for dep in graph[node]:
        visit(dep)
    active.remove(node)
    visited.add(node)
for node in ids:
    visit(node)
for index in (directory / 'README.md', directory / 'README.th.md'):
    rows = re.findall(r'^\| (\d+) \| (\d+) \|', index.read_text(encoding='utf-8'), re.M)
    assert rows == [(str(n), str(n-1)) for n in ids]
for p in directory.glob('*.md'):
    text = p.read_text(encoding='utf-8')
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
        if not target.startswith('https://'):
            assert (p.parent / target.split('#')[0]).resolve().is_file(), (p.name, target)
print('PASS: 26 paired plans; 9 sections and 4 steps each; matching literals/CLI/dependencies; valid numbering, DAG and local links')
'@
python -c $workPlanCheck
```

Validation result: both commands exited `0`. Repository output: `Ran 6 tests`; `OK`. Integrity output: `PASS: 26 paired plans; 9 sections and 4 steps each; matching literals/CLI/dependencies; valid numbering, DAG and local links`. Both were repeated after formatting correction. The full physics suite was not rerun because this work changes documentation only.

The initial `git diff --cached --check` exited `1`, reporting `new blank line at EOF` in 56 generated documents. Commit was stopped. Removed only trailing empty lines using patches, restaged the same explicit files and reran the gate: exit `0`, no output. Git's LF-to-CRLF working-copy warnings did not change the intended content or relax the whitespace gate.

## Manual review and limitations

Reviewed each package against the source roadmap, functional dependencies, entry conditions and falsification intent. No per-package scientific success is asserted. The planning checks cannot validate the future CAD, meshing, contact, material, energy, flow or vehicle implementations.

Tolerance values, sample sizes, compute allocations, backend choices and physical safe operating bounds require disclosed pilots, eligible data and frozen execution registrations. No universal shape coverage, finish date, performance win, manufacturing readiness or physical validation is promised.

## Commit and follow-up

Staged all 58 explicit work-item paths and compared `git diff --cached --name-only` against the expected list: exact match, no unrelated files. `git diff --check` and the corrected `git diff --cached --check` exited `0`; `git diff --cached --shortstat` confirmed 58 added Markdown files. The status-only final edits are restaged and validation repeated immediately before commit.

Commit command: `git commit -m "docs: expand detailed part-to-vehicle work plans"`. Verify with `git log -1 --oneline`, `git show --shortstat --oneline HEAD` and `git status --short`; report the verified hash in the final handoff after success. Do not push or rewrite history.

Next implementation: proposed Work 108 spatial material/void ownership and actual CAD mass-property evidence. Every future execution requires its own dated bilingual plan/result, physical-law tests where applicable and validated commit.
