# Work 160 Result: v2 mechanism layer framework and structural deck

Thai companion: `2026-10-12_160_v2-mechanism-backbone-result.th.md`

Status: Completed

## Files changed

- `src/formula_ultimate/hierarchy/mechanisms.py` (new): `measure_cluster`,
  mechanism prism grammar `func-leaf-mechanism-v2` (`prism_program`,
  `validate_mechanism_program`, `prism_vertices`), `plan_backbone`,
  `plan_mechanisms`, `mechanism_problems`, `roll_up_manifest_nodes`,
  `merge_mechanism_layer`, `mechanism_config_record`.
- `scripts/hierarchy/functional_realization.py`: validates mechanism programs
  with `validate_mechanism_program`, others as before.
- `scripts/hierarchy/generate_functional_vehicle.py`: realizes the cluster,
  re-reads its meshes, measures the box, plans/realizes/merges the layer,
  integrates inertia over cluster plus mechanism meshes, hashes the mechanism
  config.
- `src/formula_ultimate/hierarchy/functional.py`: `config_sha256_v2(...,
  mechanisms=None)`.
- `tests/test_hierarchy_mechanisms.py` (new, 10 tests incl. one CAD test).

## Decisions

- Mechanism leaves go into root-level assemblies `m<k>-<capability>` and meet
  the v1 cluster only through the deck (`bonded` seat interface with the
  cluster's lowest leaf, which has a vertex on the deck top at `Z0`).
- Deck: chamfered octagon, thickness 0.04-0.06 m, margin 0.08-0.2 m, chamfer
  0.01-0.03 m, +x bay 0.8-1.2 m, x lip 0.14 m on both ends (reserved for the
  ground-contact lines and axle seats). All seed-drawn.
- v2 interface kinds are appended at manifest level; assembly masses and
  centres are recomputed with the `part_tree.roll_up` arithmetic (tested
  equal).
- Evidence emitted so far: `load_structure: {members: [m0-load_structure.deck]}`.

## Validation

| Command | Exit | Output |
|---|---|---|
| `python -m unittest tests.test_hierarchy_mechanisms -v` | 0 | `Ran 10 tests`, `OK` |
| `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_functional_vehicle.py --seed 11 --out artifacts/work160/seed11` | 0 | 249 leaves, 248 interfaces, 25 s |
| `python scripts/hierarchy/evaluate_level0.py --manifest artifacts/work160/seed11/manifest.json --out artifacts/work160/l0.json` | 0 | `finished`, 9682.3 s, mass 1766.2 kg |
| `python -m unittest test_functional_composition` (in `auto-loop/acceptance`) | 1 | 28 tests, only B1-B9 fail (key set) |
| `pwsh -NoProfile -File auto-loop/verify.ps1` | 3 | Gate 1 PASS; Gate 2 `Ran 1140 tests`, `OK (skipped=11)`; Gate 3 `Ran 41`, `FAILED (failures=9)`: B1-B9 only |

## Limitations

- The deck is heavy: seed 11 root mass rose from 528 kg to 1766 kg (the deck
  is about 1240 kg with the synthetic catalogue density). Level-0 still
  finishes. Lightening holes or a thinner deck are possible follow-ups.
- The deck is not shown to carry load; the seat is a representation contact.
- B1-B9 still fail because the evidence key set is incomplete.

## Follow-up

Ground contacts and braking on the deck lip lines (wheels with polygonal
bores on fixed axles seated on the deck side faces, rotor discs co-rotating
with the wheels, stators on the axle tops), then steering, transmission,
converter, vessel, controller and heat modules in the bay.
