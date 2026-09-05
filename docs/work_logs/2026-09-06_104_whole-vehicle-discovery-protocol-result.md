# Work 104 Result: Whole-Vehicle and Technology Discovery Protocol

Thai companion: `2026-09-06_104_whole-vehicle-discovery-protocol-result.th.md`

Date: 2026-09-06 (Asia/Bangkok)

Status: Completed

## Outcome and changed files

- Added `docs/contracts/WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.md` and its Thai companion: the new dated normative protocol, with implementation explicitly pending.
- Added dated supersession notices to `docs/reports/GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1.md` and its Thai companion. The historical bodies are preserved byte-for-byte.
- Added exact pre-change copies of both roadmap files under `docs/reports/backups/2026-09-06_104/`.
- Added this result, the Work 104 plan, and their Thai companions. Total intended commit scope: 10 Markdown files.

## Decisions

- Internal component boundaries, multifunctional regions, architecture and controllers may co-evolve while the registered external task remains fixed.
- Exploratory integration may start with declared incomplete local evidence; complete-vehicle claims still require all applicable promotion evidence and complete accounted three-dimensional design.
- Evidence states are orthogonal and scoped by domain/fidelity/process/use. Untested, unsupported, numerical failure, physical failure and corrupted provenance remain distinct.
- Post-result learning creates a new descendant or evaluation identity without rewriting the parent, prior criteria or cost.
- Registration defines explicit budget, replay, audit, statistical and holdout rules. Numerical study thresholds must be supplied before admitted observations; none are fabricated for unimplemented domains.
- Novel geometry, mechanism, vehicle utility and external novelty require different evidence. Graph non-isomorphism is not mandatory for every discovery.
- Works 098–101 receive revised deliverables; Work 104 does not implement or complete them.

## Backup evidence

Source revision: `9889daf`.

- English SHA-256: `686b81df2f98b566775010aabcf225ae32a8552f9ec1818d43b1457070dbc449`.
- Thai SHA-256: `f86ee5472f5afe02f18ac14685dcf755de7a56bd82c5ade960cc2b51d71338c3`.

Both backups were copied and hash-checked before changing either original, then verified against Git source bytes and staged backup blobs.

## Validation

Environment: Windows / PowerShell; Python 3.14.3. Gates ran separately; no commit proceeded after a failed gate.

- Backup/content/link verification: exit 0; 2 exact backups, 2 exact historical bodies, 15 matched numbered sections, identical fenced content and technical token sets, 14 valid local links. Manual bilingual review checked equivalent scope, claim limits and implementation boundaries.
- Staged backup verification: exit 0; both staged Git blobs equal their original blobs at `9889daf`.
- Repository contract tests: exit 0; 6 tests passed. Physics suites were not rerun because no implementation changed.
- `git diff --check`: exit 0.
- Staged scope inspection: exit 0; exactly the 10 intended Markdown files.
- First `git diff --cached --check`: exit 1, reporting 6 trailing-whitespace lines from Markdown hard breaks in the new protocol metadata. Replaced them with blank-separated paragraphs in both languages; rerun exit 0 with no output. The failed check stopped the commit path until repaired.
- Git emitted LF/CRLF checkout advisories; backup working bytes and staged blobs were verified independently. No backup normalization was used as a substitute for byte equality.

Exact validation commands (each gate checked independently):

````powershell
@'
from pathlib import Path
import hashlib, re, subprocess
root = Path.cwd()
name = 'WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06'
protocols = [root / 'docs/contracts' / (name + ext) for ext in ('.md', '.th.md')]
texts = [p.read_text(encoding='utf-8') for p in protocols]
for text in texts:
    assert '2026-09-06' in text and 'FU-WHOLE-VEHICLE-DISCOVERY-V1-2026-09-06' in text
    assert 'Status: Normative design protocol; implementation pending' in text
    assert re.findall(r'^## (\d+)\.', text, re.M) == [str(i) for i in range(1, 16)]
    assert '\ufffd' not in text
assert re.findall(r'```[^\n]*\n(.*?)```', texts[0], re.S) == re.findall(r'```[^\n]*\n(.*?)```', texts[1], re.S)
tokens = [set(t for t in re.findall(r'(?<!`)`([^`\n]+)`(?!`)', text) if not t.endswith('.md')) for text in texts]
assert tokens[0] == tokens[1], tokens[0] ^ tokens[1]
link_sources = list(zip(protocols, texts))
for suffix in ('.md', '.th.md'):
    filename = 'GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1' + suffix
    original = subprocess.check_output(['git', 'show', '9889daf:docs/reports/' + filename])
    backup = root / 'docs/reports/backups/2026-09-06_104' / filename
    current = root / 'docs/reports' / filename
    assert backup.read_bytes() == original, filename
    value = current.read_bytes()
    assert value.endswith(original), filename
    notice = value[:-len(original)].decode('utf-8')
    assert notice.startswith('> ') and '2026-09-06' in notice
    digest = hashlib.sha256(original).hexdigest()
    assert all(digest in text for text in texts)
    link_sources.append((current, notice))
    print(filename, digest, 'backup and historical body exact')
links = 0
for path, text in link_sources:
    for target in re.findall(r'\]\(([^)]+)\)', text):
        assert (path.parent / target.split('#')[0]).is_file(), (path, target)
        links += 1
print('PASS: 2 exact backups; 2 exact historical bodies; 15 matched sections; identical fenced content and technical token sets;', links, 'valid local links')
'@ | python -
````

```powershell
@'
import subprocess
for suffix in ('.md','.th.md'):
    name = 'GENERATION_FIRST_PHYSICS_EVALUATION_ROADMAP_V1' + suffix
    original = subprocess.check_output(['git','show','9889daf:docs/reports/' + name])
    backup = subprocess.check_output(['git','show',':docs/reports/backups/2026-09-06_104/' + name])
    assert backup == original, name
print('Both staged backup blobs exactly match original Git blobs.')
'@ | python -
```

```powershell
python -m unittest tests.test_repository_contract -q

git diff --check

git diff --cached --name-only

git diff --cached --check
```


## Limitations and follow-up

Documentation only; no CAD, physics solver, search, admitted experiment, actual survivor, vehicle superiority or technology discovery was produced. Preserved backup links retain their original `docs/reports/` context. No historical result was rewritten, no code was changed, and no push was requested.

Next: implement Work 098 against this contract, including the required acceptance cases and concrete registration/budget schemas. Later implementation requires separate plans, validations and commits. The final commit hash will be reported in the handoff; it cannot be embedded in its own commit.

Plan deviations: none.
