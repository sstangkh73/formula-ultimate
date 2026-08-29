# Work 032 Plan: Design Search Agent v0 Research Report

Status: Completed

Thai companion: `2026-08-29_032_design-search-agent-v0-report-plan.th.md`

## Objective

Produce an implementation-ready research plan for Formula Ultimate's first
Design Search Agent, grounded in the completed Research Experiment Protocol and
the current `3D -> STEP -> FreeCAD -> Level 0` evidence boundary.

## Scope

- Define the agent's role, authority boundary, inputs, outputs, state, and
  interaction with deterministic evaluators.
- Select a first functional component experiment with declared interfaces,
  loads, keep-out region, material assumptions, and failure criteria.
- Specify candidate representation, generation operators, rejection behavior,
  baselines, matched compute budget, seeds, metrics, and falsification tests.
- Define an ordered implementation and promotion roadmap from parameter search
  through independent structural evidence without claiming complete-vehicle
  discovery.
- Identify safety, research-integrity, simulator-exploitation, and evidence
  risks with explicit controls.
- Maintain separate English and Thai report versions.

## Planned Files

- `docs/reports/DESIGN_SEARCH_AGENT_V0_PLAN.md`
- `docs/reports/DESIGN_SEARCH_AGENT_V0_PLAN.th.md`
- matching Work 032 plan/result records in English and Thai

No simulator, CAD grammar, optimizer, candidate artifact, or external service
will be implemented or run in this documentation-only work item.

## Report Questions

1. Which agent performs design search, and which systems remain non-agentic
   evaluators?
2. What is the smallest scientifically meaningful first design task?
3. Which variables may the agent change, and which controls are immutable?
4. How are candidate validity, performance, and failure measured?
5. What baseline and compute-budget rules make comparison fair?
6. Which evidence gates are required before promotion beyond Level 0?
7. What implementation sequence can be tested and falsified incrementally?

## Validation

Planned commands:

```powershell
py -3.14 -m unittest tests.test_repository_contract -v
py -3.14 -m unittest discover -s tests -q
git diff --check
git diff --cached --check
```

The result record will capture exact exit codes and concise output.

## Success Criteria

- The report distinguishes Codex orchestration, the future Design Search Agent,
  and deterministic CAD/physics evaluators.
- The first experiment has explicit independent/dependent variables, controls,
  metrics, success criteria, and failure criteria.
- Fixed/random/search treatments receive matched declared budgets and seeds.
- The plan attempts to falsify the preferred hypothesis and records alternative
  explanations and missing evidence.
- The roadmap remains inside current implementation evidence and does not call
  Level 0 physical validation.
- Bilingual, repository, whitespace, and staged-scope checks pass and the work
  is committed.

## Risks

- A broad “design a race car” goal would exceed current geometry and physics
  contracts.
- A component grammar can accidentally encode the preferred solution and make
  search appear more intelligent than it is.
- Mass-only Level 0 fitness would reward structurally impossible material
  removal.
- Unequal optimization effort could make a searched treatment appear superior
  to an under-tuned baseline.
- A report may be mistaken for implemented capability; status and non-goals
  must remain explicit.

## Explicit Non-Goals

- No Design Search Agent implementation or autonomous run.
- No complete-vehicle generation, free-topology claim, FEA/CFD result, physical
  validation, safety claim, manufacturing claim, or discovery claim.
- No conventional vehicle-layout prescription based only on historical racing
  practice.
- No push, publication, external upload, or history rewrite.
