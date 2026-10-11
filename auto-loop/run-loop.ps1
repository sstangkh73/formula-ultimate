<#
  Claude + Codex autonomous loop for Formula Ultimate (Work 148).

  Usage (from anywhere):
    pwsh -File auto-loop/run-loop.ps1 [-MaxIterations 20] [-MaxHours 8] [-MaxTurnsPerIteration 120]
                                      [-Branch loop/hierarchical-composition] [-PreflightOnly]
  Stop:  create auto-loop/STOP (checked before each iteration) or press Ctrl+C.

  The loop, not Claude, decides when the goal is met: verify.ps1 must exit 0 on a
  clean, committed tree. Repository rules (AGENTS.md) still apply in every iteration:
  one numbered work item, bilingual plan/result, explicit staging, commit only after
  validation passes. The loop never stages, commits, pushes, or runs git init itself.
#>
param(
    [int]$MaxIterations = 20,
    [double]$MaxHours = 8,
    [int]$MaxTurnsPerIteration = 120,
    [string]$Branch = 'loop/hierarchical-composition',
    [switch]$PreflightOnly
)

$ErrorActionPreference = 'Stop'
$LoopDir = $PSScriptRoot
$Root = Split-Path $LoopDir -Parent
Set-Location $Root

function Invoke-Git { $out = & git @args 2>&1; if ($LASTEXITCODE -ne 0) { throw "git $args failed: $out" }; $out }

# ---- preflight -------------------------------------------------------------
$top = (Invoke-Git rev-parse --show-toplevel | Out-String).Trim()
if ((Resolve-Path $top).Path -ne (Resolve-Path $Root).Path) { throw "auto-loop must sit at the repository root ($top)" }
if ($Branch -notmatch '^loop/[A-Za-z0-9._/-]+$') { throw "Branch must be named loop/<name>" }

$needed = @('git', 'python')
if (-not $PreflightOnly) { $needed += @('claude', 'codex') }
foreach ($cmd in $needed) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) { throw "command '$cmd' not found - see auto-loop/README.md" }
}
$CadPython = Join-Path $Root '.tools/cadquery-mcp/Scripts/python.exe'
if (-not (Test-Path $CadPython)) { throw "pinned CadQuery runtime missing: $CadPython (scripts/bootstrap_cadquery_mcp.ps1)" }

$dirty = Invoke-Git status --porcelain
if ($dirty) { throw "working tree is not clean - commit or stash first:`n$($dirty -join "`n")" }

$current = (Invoke-Git rev-parse --abbrev-ref HEAD | Out-String).Trim()
$MainSha = (Invoke-Git rev-parse main | Out-String).Trim()
if ($current -ne $Branch) {
    if ($current -notin @('main', 'master')) { throw "on branch '$current'; switch to '$Branch' or main first" }
    if ($PreflightOnly) {
        Write-Host "preflight: would switch from $current to $Branch"
    } else {
        & git show-ref --verify --quiet "refs/heads/$Branch"
        if ($LASTEXITCODE -eq 0) { Invoke-Git switch $Branch | Out-Null } else { Invoke-Git switch -c $Branch | Out-Null }
    }
}

# Files the agent must never change. Any tracked test that exists now is protected;
# new test files may be added.
$Protected = @(
    'auto-loop/GOAL.md', 'auto-loop/GOAL.th.md', 'auto-loop/PROMPT.md', 'auto-loop/PROMPT.th.md',
    'auto-loop/README.md', 'auto-loop/README.th.md', 'auto-loop/verify.ps1', 'auto-loop/run-loop.ps1',
    'auto-loop/tools/codex.sh', 'auto-loop/.gitignore', 'AGENTS.md', 'AGENTS.th.md'
) + @(Invoke-Git ls-files auto-loop/acceptance tests .github)
$Hashes = @{}
foreach ($f in $Protected) {
    if (-not (Test-Path $f)) { throw "protected file missing at start: $f" }
    $Hashes[$f] = (Get-FileHash $f).Hash
}
Write-Host "preflight: $($Protected.Count) protected files hashed; main at $MainSha"

# Allowed tools for the headless agent. Anything else is refused automatically.
$AllowedTools = @(
    'Read', 'Edit', 'Write', 'Glob', 'Grep',
    'Bash(bash auto-loop/tools/codex.sh:*)',
    'Bash(git status:*)', 'Bash(git diff:*)', 'Bash(git log:*)', 'Bash(git show:*)',
    'Bash(git add:*)', 'Bash(git commit:*)', 'Bash(git rev-parse:*)', 'Bash(git ls-files:*)',
    'Bash(python:*)', 'Bash(.tools/cadquery-mcp/Scripts/python.exe:*)',
    'Bash(pwsh -NoProfile -File auto-loop/verify.ps1)',
    'Bash(ls:*)', 'Bash(mkdir:*)', 'Bash(wc:*)', 'Bash(date:*)'
)
$DisallowedTools = @(
    'Bash(git add -A:*)', 'Bash(git add .:*)', 'Bash(git add --all:*)', 'Bash(git add -u:*)',
    'Bash(git commit -a:*)', 'Bash(git commit --amend:*)', 'Bash(git push:*)', 'Bash(git reset:*)',
    'Bash(git checkout:*)', 'Bash(git switch:*)', 'Bash(git rebase:*)', 'Bash(git stash:*)',
    'Bash(git clean:*)', 'Bash(git init:*)', 'WebFetch', 'WebSearch'
)

$env:BASH_DEFAULT_TIMEOUT_MS = '1800000'
$env:BASH_MAX_TIMEOUT_MS = '1800000'

$State = Join-Path $LoopDir '.loop'
New-Item -ItemType Directory -Force $State | Out-Null

function Invoke-Verify {
    $out = & pwsh -NoProfile -File (Join-Path $LoopDir 'verify.ps1') 2>&1 | Out-String
    $code = $LASTEXITCODE
    "exit=$code  ($(Get-Date -Format s))`n$out" | Set-Content (Join-Path $State 'last-verify.txt') -Encoding utf8
    return $code
}

function Assert-Guards([string]$StartHead) {
    foreach ($f in $Protected) {
        if (-not (Test-Path $f) -or (Get-FileHash $f).Hash -ne $Hashes[$f]) {
            throw "protected file changed: $f - loop stopped (inspect with git diff / git log)"
        }
    }
    $touched = @(Invoke-Git diff --name-only $StartHead HEAD) | Where-Object { $_ -in $Protected }
    if ($touched) { throw "a commit touched protected files: $($touched -join ', ') - loop stopped" }
    $now = (Invoke-Git rev-parse --abbrev-ref HEAD | Out-String).Trim()
    if ($now -ne $Branch) { throw "branch changed to '$now' - loop stopped" }
    & git merge-base --is-ancestor $StartHead HEAD
    if ($LASTEXITCODE -ne 0) { throw "history was rewritten (start head is no longer an ancestor) - loop stopped" }
    if ((Invoke-Git rev-parse main | Out-String).Trim() -ne $MainSha) { throw "main moved - loop stopped" }
}

if ($PreflightOnly) {
    $code = Invoke-Verify
    Write-Host "preflight complete; verify exit=$code (see auto-loop/.loop/last-verify.txt). No agent was started."
    exit 0
}

$StartHead = (Invoke-Git rev-parse HEAD | Out-String).Trim()
if ((Invoke-Verify) -eq 0) { Write-Host 'verify already passes - nothing to do'; exit 0 }

$deadline = (Get-Date).AddHours($MaxHours)
$history = Join-Path $State 'history.txt'
for ($i = 1; $i -le $MaxIterations; $i++) {
    if (Test-Path (Join-Path $LoopDir 'STOP')) { Write-Host 'STOP file found - stopping'; exit 2 }
    if ((Get-Date) -gt $deadline) { Write-Host 'time budget reached - stopping'; exit 2 }

    Write-Host "`n=== iteration $i / $MaxIterations   $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" -ForegroundColor Cyan
    $before = (Invoke-Git rev-parse HEAD | Out-String).Trim()
    $log = Join-Path $State ('iter-{0:D3}.log' -f $i)
    $prompt = (Get-Content (Join-Path $LoopDir 'PROMPT.md') -Raw) +
        "`n`n---`nLoop context: iteration $i of $MaxIterations, branch $Branch, HEAD $before."
    $prompt | claude -p --permission-mode acceptEdits --max-turns $MaxTurnsPerIteration `
        --allowedTools @AllowedTools --disallowedTools @DisallowedTools 2>&1 | Tee-Object -FilePath $log

    Assert-Guards $StartHead
    $after = (Invoke-Git rev-parse HEAD | Out-String).Trim()
    $dirty = Invoke-Git status --porcelain
    $code = Invoke-Verify
    $line = "iter=$i head=$after commits=$((Invoke-Git rev-list --count "$before..$after" | Out-String).Trim()) dirty=$([bool]$dirty) verify=$code  $(Get-Date -Format s)"
    Add-Content $history $line
    Write-Host $line

    if (Test-Path (Join-Path $LoopDir 'BLOCKED')) {
        Write-Host 'agent wrote auto-loop/BLOCKED - a human decision is needed:' -ForegroundColor Yellow
        Get-Content (Join-Path $LoopDir 'BLOCKED')
        exit 4
    }
    if ($code -eq 0 -and -not $dirty) { Write-Host "goal met - verify passed on a clean tree in iteration $i" -ForegroundColor Green; exit 0 }
    if ($code -eq 0) { Write-Host 'verify passed but the tree has uncommitted changes - next iteration must record and commit them' -ForegroundColor Yellow }
}

Write-Host 'iteration budget reached and the goal is not met - see auto-loop/progress.md and auto-loop/.loop/' -ForegroundColor Yellow
exit 1
