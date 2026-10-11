# Claude + Codex Auto Loop

Thai companion: `README.th.md`

An unattended loop. Claude works one numbered work item per iteration, hands
well-bounded coding tasks to Codex, and keeps going until `verify.ps1` passes
on a clean, committed tree. Adapted to this repository by Work 148.

```
run-loop.ps1 ──► claude -p (reads PROMPT.md) at the repository root
     ▲               ├─ plan / debug / review / commit  ← Claude
     │               └─ bash auto-loop/tools/codex.sh   ← Codex (no staging, no commits)
     │
     ├─ guards: protected files unchanged, same branch, no rewritten history, main untouched
     └─ verify.ps1 ── Gate 1 material boundary
                      Gate 2 whole repository suite
                      Gate 3 acceptance (the goal)  ── pass + clean tree → stop
```

## Files

| File | Purpose | Edited by |
|---|---|---|
| `GOAL.md` | goal and acceptance contract | human |
| `acceptance/` | the goal as executable tests | human |
| `verify.ps1` | judge: exit 0 = done | human |
| `PROMPT.md` | instructions given to Claude every iteration | human |
| `run-loop.ps1`, `tools/codex.sh` | runner and Codex bridge | human |
| `progress.md` | memory between iterations (committed) | agent |
| `.loop/` | per-iteration logs, Codex logs, last verify output, history | runner (gitignored) |

All human-edited files are protected. The runner hashes them, together with
every test that is tracked in git, and stops if any of them changes.

## How it differs from the original template

- Runs from the repository root and never runs `git init`.
- Refuses to run on `main`. It creates or switches to `loop/hierarchical-composition`
  (`-Branch` to change), and stops if `main` moves.
- Never stages or commits by itself. Each iteration follows `AGENTS.md`:
  bilingual plan/result records, explicit `git add <files>`, and a commit only
  after Gates 1 and 2 pass.
- Blanket staging, amend, reset, rebase, branch switching, push and web tools
  are denied to the headless agent.
- The agent can write `auto-loop/BLOCKED` to stop the loop and ask a human.

## Install (once)

```
npm install -g @anthropic-ai/claude-code @openai/codex
claude        # sign in, then /exit
codex login
```

The pinned CadQuery runtime must exist at `.tools/cadquery-mcp/`
(see `scripts/bootstrap_cadquery_mcp.ps1`).

## Run

```
pwsh -File auto-loop/run-loop.ps1 -PreflightOnly          # checks only, no agent, no branch switch
pwsh -File auto-loop/run-loop.ps1 -MaxIterations 20 -MaxHours 8
```

- **Stop:** create `auto-loop/STOP`, or press Ctrl+C.
- **Watch:** `auto-loop/progress.md`, `git log --oneline`, `auto-loop/.loop/iter-*.log`,
  `auto-loop/.loop/history.txt`.
- **Review:** every iteration is a normal commit on the loop branch. Review it
  before merging anything into `main`.
- **Roll back:** the loop branch is disposable. Delete it or reset it, and
  `main` stays untouched.

## Cost and safety

- Every iteration spends both Claude and OpenAI budget. Bound it with
  `-MaxIterations`, `-MaxHours` and `-MaxTurnsPerIteration`.
- Gate 2 runs the full repository suite, which takes about 6 minutes, and
  Gate 3 runs the generator four times. Each verify can take a while.
- Codex runs with `--sandbox workspace-write` at the repository root.
- Passing Gate 3 is a geometry and assembly representation result, not
  physical validation (see `GOAL.md`).
