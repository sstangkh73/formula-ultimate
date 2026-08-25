# Work 007 Result: Main Research Direction in README

Status: Completed

Thai companion: `2026-08-25_007_main-research-direction-result.th.md`

## Outcome

The English and Thai README files now present the user-confirmed Formula
Ultimate direction as the repository's main entry-point framing:

- autonomous agents may eventually design the complete 3D race vehicle, from
  whole-car architecture to previously unseen internal component geometry;
- conventional vehicle layout, dimensions, powertrain, wheel arrangement, body
  form, and known part shapes are not prescribed merely because historical
  racing practice uses them;
- physics, a versioned Formula One-derived race/energy contract, finite
  resources, safety, and evidence remain hard declared boundaries;
- all primary propulsion energy is onboard before the race and no primary
  energy is replenished during the race;
- fair cross-architecture experiments require a technology-neutral equivalent
  energy profile rather than silently privileging the current FIA ICE/ERS
  architecture;
- complete 3D geometry is a causal physics input from which independent
  evaluators derive physical evidence;
- the objective is minimum total race time among candidates that finish and
  pass the required fidelity gates;
- novelty and discovery claims require fair baselines, falsification, replay
  evidence, and survival at higher fidelity.

The README continues to state that Phase 1 is deliberately narrow and that the
existing Level 0 and Work 006 component loop do not physically validate a race
vehicle.

## Files Changed

- `README.md`
  - added the long-term mission and primary research question;
  - defined the total-race-time objective and hard constraints;
  - documented the Formula One-derived race and energy contract with official
    2026 FIA sources;
  - defined technology-neutral energy equivalence for open powertrain research;
  - defined the open 3D design domain, independent evidence loop, discovery
    standard, current implementation status, and claim boundary;
  - added `docs/3d/` to the repository map.
- `README.th.md`
  - mirrors the English structure, identifiers, equation, rule references,
    dates, links, claims, and limitations in Thai;
  - continues to identify `README.md` as its English source.
- matching Work 007 plan and result records in English and Thai.
- `C:\Users\sstan\.codex\memories\extensions\ad_hoc\notes\2026-08-25T23-00-50-formula-ultimate-main-direction.md`
  - records the same user-confirmed direction for future sessions without
    directly editing the managed memory registry.

No simulator, CAD, physics, optimization, or experiment configuration was
changed. Existing uncommitted Work 006 changes were preserved and not folded
into Work 007.

## Decisions

1. **Define openness as architectural freedom inside explicit constraints.**
   The README does not say “no constraints”; it says no prescribed conventional
   architecture beyond declared physics, race, energy, resource, safety, and
   evidence constraints.
2. **Inherit the F1 race-energy principle, not every current power-unit shape.**
   The README cites FIA 2026 Sporting Regulation B5.1.4 and Technical Regulation
   C6.4.4 for the no-fuel-addition race boundary. Each experiment must pin a
   regulatory profile.
3. **Require energy-equivalent comparisons.** Alternative stores and carriers
   receive the same declared initial primary-energy opportunity unless energy
   budget is the predeclared independent variable. Recovery is admitted only
   through traceable conserved physical flows.
4. **Make 3D geometry causal.** Geometry drives mass, volume, centre of mass,
   inertia, packaging, collision, structural, thermal, flow, electromagnetic,
   and aerodynamic evidence. A render or generator claim is insufficient.
5. **Use total race time after feasibility gates.** Peak speed, incomplete
   attempts, and numerical exploits cannot win the objective.
6. **Separate generated, simulation-valid, promoted, physically validated, and
   discovered.** A novel fastener is allowed, but its novelty is not a research
   discovery until it passes fair comparison and stronger evidence.
7. **Keep current capability honest.** The ultimate direction is now prominent,
   while Phase 1 and the current Level-0/Work-006 limits remain explicit.

## Official Rule Evidence

- [2026 FIA Formula One Sporting Regulations, Section B, Issue
  08](https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_b_sporting_-_iss_08_-_2026-08-05_7.pdf),
  published 5 August 2026: B5.1.4 prohibits adding or removing fuel from the
  reconnaissance-lap boundary through the end-of-session signal.
- [2026 FIA Formula One Technical Regulations, Section C, Issue
  20](https://www.fia.com/system/files/documents/fia_2026_f1_regulations_-_section_c_technical_-_iss_20_-_2026-08-05.pdf),
  published 5 August 2026: C6.4.4 prohibits adding or removing fuel during a
  Race.

These sources are versioned rather than treated as timeless. Formula Ultimate
must explicitly update or retain its pinned profile when FIA rules change.

## Validation

Commands:

```powershell
py -3.14 -m unittest discover -s tests -v
py -3.14 -m compileall -q src scripts tests
git diff --check
rg -n "Primary Research Question|คำถามวิจัยหลัก|B5\.1\.4|C6\.4\.4|external primary-energy|3D|Level 0|Level-0|physical validation|technology-discovery" README.md README.th.md
```

Exit status: `0` for all validation commands.

Relevant output:

```text
Ran 32 tests in 0.670s
OK
```

`compileall` and `git diff --check` reported no errors. Git emitted only Windows
line-ending warnings for modified files. The focused README search found the
research question, equivalent energy constraints, FIA articles, 3D evidence
requirements, discovery standard, and Level-0 non-claim in both languages.

Artifact hashes after validation:

| Artifact | SHA-256 |
|---|---|
| `README.md` | `80D9D0977704179F1945C5D19F7CA443D46B0FFA90614F2EF11CB11CF91055B1` |
| `README.th.md` | `443B01CEBB6B585A1A038901A9340210532B9852F81785739AAD108CE46B3D7E` |
| ad-hoc memory note | `A874933F95701D062E35FAD920244C5B0E4DB342895055A86F42F6103C81C9BD` |

## Limitations

- README is a direction and research contract, not an implementation claim.
- A numerical technology-neutral race-energy budget has not yet been defined;
  it requires a separate experiment/configuration work item.
- The current research charter and design-language boundary still describe the
  narrower staged plan. They are not contradictory, but a later consistency
  work item should propagate the new top-level framing without disguising
  Phase-1 controls.
- No current FIA architecture-specific power, state-of-charge, or per-lap
  recovery limit was adopted automatically.
- No physical, empirical, FEA, CFD, manufacturability, or safety validation was
  added.

## Follow-up Work

1. Define and justify a versioned `FORMULA_ULTIMATE_EQUIVALENT_2026` energy
   profile in SI units, including initial primary-energy accounting, permitted
   recovery, prohibited external inflows, uncertainty, and cross-carrier
   equivalence.
2. Propagate this main framing into the research charter and design-language
   boundary as a separate bilingual consistency work item.
3. Specify the complete-vehicle 3D representation and closure rule so every
   mass, volume, interface, and energy path is physically accounted.
4. Preserve the current Phase-1 fixed-topology baselines and equal-budget
   comparison discipline while expanding later fidelities.
