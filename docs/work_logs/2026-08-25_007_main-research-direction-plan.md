# Work 007 Plan: Main Research Direction in README

Status: Completed

Thai companion: `2026-08-25_007_main-research-direction-plan.th.md`

## Objective

Make the agreed Formula Ultimate direction prominent in the English and Thai
README files and preserve it as cross-session project guidance: autonomous
agents may design the complete vehicle and its 3D components without a
prescribed conventional architecture, while every candidate remains subject to
physics, a versioned Formula One-derived race/energy contract, independent
geometry-derived evidence, and multi-fidelity validation.

## Scope

- Rewrite the README introduction around the main research mission rather than
  the current narrow implementation phase.
- State the primary research question in falsifiable language.
- Define the distinction between removed legacy architecture restrictions and
  retained explicit constraints.
- Record the race-energy rule: primary propulsion energy is carried before the
  race and is not replenished during the race; internal recovery must remain
  traceable through energy conservation.
- Explain that a technology-neutral energy-equivalent profile is required when
  comparing architectures outside the current FIA ICE/ERS layout.
- Make complete 3D design a causal simulation input: geometry must determine
  packaging, mass, centre of mass, inertia, and later structural, thermal, and
  aerodynamic evidence.
- Preserve the current narrow Phase-1 implementation and its claim limits.
- Update English and Thai README files together with equivalent identifiers,
  equations, units, statuses, sources, and limitations.
- Add a small ad-hoc memory update note because the user explicitly requested
  that this direction remain the main guidance for future work.

## Planned Files

- `README.md`
- `README.th.md`
- matching Work 007 plan/result records in English and Thai
- one new note under
  `C:\Users\sstan\.codex\memories\extensions\ad_hoc\notes\`

## Validation

```powershell
py -3.14 -m unittest discover -s tests -v
py -3.14 -m compileall -q src scripts tests
git diff --check
```

The final review will also verify that:

- each README links to its language companion;
- the Thai README identifies `README.md` as its English source;
- the README does not imply that Level 0 or Work 006 physically validates a
  vehicle;
- FIA claims link to the current official 2026 regulations consulted for this
  work;
- open-ended invention and hard physics/energy/3D evidence constraints are
  both stated without contradiction.

## Success Criteria

- A new reader can identify the ultimate mission, objective function, retained
  constraints, 3D evidence requirement, discovery standard, current phase, and
  non-claims directly from the README.
- The no-race-refuelling rule is accurately attributed and versioned.
- Alternative energy carriers are not granted an undeclared energy advantage.
- Generated geometry cannot self-report mass or performance; independent
  evaluation remains explicit.
- English and Thai documentation are structurally equivalent and all repository
  tests pass.
- The memory update note captures the same direction without modifying the
  managed memory registry directly.

## Risks

- Copying all architecture-specific FIA power-unit limits would undermine the
  intended open design search; the README must separate the inherited race
  protocol from technology-neutral equivalence rules.
- Saying “no constraints” would invite infinite-energy, magic-material, or
  solver-exploit solutions; the README must use “no prescribed conventional
  architecture beyond declared constraints.”
- A broad long-term mission could be confused with current implementation
  capability; current status and fidelity limits must remain prominent.
- FIA regulations evolve, so the exact 2026 issue and links must be recorded
  rather than described as timeless rules.

## Explicit Non-Goals

- No simulator, CAD, physics, optimization, or configuration changes.
- No claim that an agent has already discovered a new vehicle technology.
- No claim that Work 006 provides FEA, CFD, manufacturability, safety, or full
  vehicle validation.
- No adoption of every current FIA geometry, power-unit architecture, or
  component restriction.
- No rewriting of the research charter or design-language boundary in this work
  item; those may receive a separate consistency work item if requested.
