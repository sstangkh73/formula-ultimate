# Work 021 Plan: Coupling Contract and Architecture Compiler

Status: Completed

Thai companion: `2026-08-28_021_coupling-contract-architecture-plan.th.md`

## Objective

Create the first executable central contract for the coupled-vehicle program:
a versioned experiment manifest, topology-neutral shared vehicle state,
deterministic physics-stage architecture compiler, residual ledger, and event
arbitration. Also create the ordered Work 021–030 integration queue. This work
defines and validates the coupling boundary; it does not yet execute the
independent Work 011–019 physics solvers as one vehicle.

## Scope

- List Work 021–030 in a bilingual sequential implementation queue with one
  completion gate per item.
- Define a canonical causal stage order from environment inputs through aero,
  load balance, contacts, motion, energy, health, and race progress.
- Define module declarations with version, consumed signals, and produced
  signals; compile arbitrary input ordering into deterministic execution order.
- Reject missing producers, duplicate outputs, same/later-stage dependencies,
  duplicate identities, missing required stages, and malformed JSON.
- Define an immutable experiment manifest that pins candidate/design language,
  geometry hashes, catalogs, circuit/regulatory/energy/solver profiles,
  architecture fingerprint, source commit, seed, timestep, and evaluation
  budget; derive a deterministic SHA-256 identity.
- Define a topology-neutral shared vehicle state with arbitrary contact and
  component-health collections and strict SI/numerical contracts.
- Define residual entries/ledger without silent correction and deterministic
  event arbitration with declared tie priority/tolerance.
- Add a versioned reference architecture configuration mapping the existing
  Level-0 capability boundaries into the future coupling order.
- Add tests, validator, bilingual model/result documentation, separate bilingual
  problem reports for any issue encountered, and one verified commit.

## Planned files

- `docs/integration/COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.md` and `.th.md`
- `docs/simulation/COUPLING_CONTRACT_AND_ARCHITECTURE.md` and `.th.md`
- `config/simulation/coupled_level0_architecture_v1.json`
- `src/formula_ultimate/simulation/coupling.py`
- `src/formula_ultimate/simulation/__init__.py`
- `tests/test_coupling_contracts.py`
- `scripts/validate_coupling_contracts.py`
- this bilingual plan/result pair
- separate bilingual problem reports for encountered issues

## Work 021 boundary

The compiler reasons about explicit signal provenance and stage ordering. It
does not call physics modules or claim their units/interfaces are already
adapted. The reference architecture is a coupling specification, not an
integrated simulation result.

The shared state supports any non-empty, uniquely identified set of contact
states and any uniquely identified component-health set. It does not prescribe
four wheels, paired axles, a conventional body, or a powertrain type.

## Experiment definition

- Preferred hypothesis: a central typed contract can make missing, duplicate,
  or causally reversed physics dependencies fail before a race, while identical
  declarations compile and fingerprint identically regardless of input order.
- Independent variables: module declarations/order, signal dependencies,
  manifest identities/hashes/profiles/seed/budget/timestep, shared state,
  residual values/tolerances, and event candidate times.
- Dependent variables: compiled module order/fingerprint, manifest fingerprint,
  contract acceptance/rejection, residual status/failed IDs, and event decision.
- Controls: canonical eight-stage order, strict earlier-stage dependency, SI
  state fields, SHA-256 canonical serialization, fixed event priority, and no
  physics solver execution or stochastic draw.
- Metrics: replay equality, permutation invariance, reference architecture
  stage coverage, invalid dependency coverage, state validation, residual
  visibility, event-time/priority correctness, repository gates, and commit.
- Success: the reference architecture loads and compiles deterministically;
  all planned invalid cases fail; arbitrary three-contact state is accepted;
  over-tolerance residual is observable; event ties are deterministic; all
  repository gates pass.
- Failure criteria: hidden producer, duplicate signal, causal reversal,
  architecture/manifest nondeterminism, invalid state accepted, residual
  correction, ambiguous event winner, bilingual mismatch, or failed commit.
- Falsification: permute modules, remove a producer/stage, duplicate output,
  consume from the same/later stage, corrupt a hash, duplicate a contact, force
  a residual failure, and create an exact event tie.

## Risks

- A central schema can become a conventional-car prescription if it encodes
  fixed wheel count, axle layout, or powertrain components.
- Signal names alone do not prove unit or semantic compatibility; later adapter
  work must define executable typed payloads.
- A deterministic architecture graph can still couple physically incorrect
  equations; Work 022–030 must test transactions, conservation, integration,
  numerical refinement, and higher-fidelity promotion.

## Explicit non-goals

- No coupled physics step, complete vehicle, whole-race integrated result,
  autonomous search, optimizer, CAD generation, CFD, FEA, calibration, README
  rewrite, remote push, or physical-validation claim.
- No claim that the reference architecture already makes Work 011–019 exchange
  real state or energy.

## Validation

```powershell
python -m unittest tests.test_coupling_contracts -v
python -m unittest discover -s tests -v
python scripts/validate_coupling_contracts.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Every gate runs fail-fast. Completion requires synchronized bilingual queue,
model, and result documents; any necessary problem reports; explicit staging;
a successful commit; and post-commit hash/clean-state evidence.
