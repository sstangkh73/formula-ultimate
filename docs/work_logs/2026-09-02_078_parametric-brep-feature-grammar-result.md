# Work 078 Result: Parametric B-rep Feature Grammar V1

Status: Completed

Thai companion: `2026-09-02_078_parametric-brep-feature-grammar-result.th.md`

## Outcome and files changed

Implemented the fail-closed `parametric_brep_feature_grammar_v1` declaration and CadQuery 2.8.0 executor. The admitted corpus causally executes all 15 required operator identities across a shaft, bracket, hollow housing, ribbed plate, and hub-like rotating part. Every final artifact is exactly one valid positive-volume B-rep solid and exports to a canonical STEP artifact.

Changed files are the Work 078 plan/result pairs; `docs/contracts/PARAMETRIC_BREP_FEATURE_GRAMMAR_V1.md` and Thai companion; `config/cad/brep_feature_grammar_v1.json`; `src/formula_ultimate/components/brep_grammar.py`; component exports; `scripts/cad/generate_brep_feature_corpus.py`; and `tests/test_brep_grammar.py`.

## Decisions and experiment evidence

- Exact schemas and ancestry are validated before loading a candidate into the kernel. Dimensions are finite bounded SI values, converted once from metres to the CadQuery millimetre convention.
- Profiles, extrude/revolve, cuts/bores, shoulder/rib/shell, patterns, edge treatment, and three booleans are distinct executed operators rather than decorative labels.
- Every non-profile feature must be valid, non-empty, finite, and positive-volume. One-solid `Compound` wrappers are representation-preservingly unwrapped; multiple solids are never auto-fused or repaired. The final state must be exactly one solid.
- STEP canonicalization changes only the volatile `FILE_NAME` timestamp. Two output roots produced identical manifest identity and identical STEP bytes per candidate.
- Empty boolean subtraction and a disconnected multi-solid final pattern failed observably.

The admitted manifest SHA-256 is `fff5c0c74513fae1a2bc7cd55020affbbaf67bdd6e9c0908f5aa2ea4131b2448`.

| Candidate | Volume (`m3`) | STEP SHA-256 |
|---|---:|---|
| `shaft_001` | `7.936733407181722e-05` | `34e81618e3cd6fefa278bf6cdfd564db06407d118651efa16c16202971f485c1` |
| `bracket_001` | `8.144352220392309e-05` | `b06e3141f7a1fcad8017537d3680a787164d3190d4503417d3f6c1c98ed1ba89` |
| `hollow_housing_001` | `0.00013046885705011982` | `ef92f5215e5614ebe00f6e2c4e6850cd252f69fc437a81231d0911b21cbd7862` |
| `ribbed_plate_001` | `9.916492873496904e-05` | `af73c6492c9c56fed73e21542c3caba2611f3cc4bc592df129a1683c6a467a10` |
| `hub_like_001` | `0.00014511182449342868` | `8b3ff21861037dea2104d287286cee98f69da59cb4c0eae1d4744c8cedce00f0` |

## Exact validation record

```text
python -m unittest tests.test_brep_grammar.BrepGrammarParserTests -q
Exit: 0
Ran 6 tests in 0.004s — OK

.tools\cadquery-mcp\Scripts\python.exe kernel unittest invocation
Exit: 0
Ran 3 tests in 2.863s — OK

.tools\cadquery-mcp\Scripts\python.exe scripts\cad\generate_brep_feature_corpus.py --config config\cad\brep_feature_grammar_v1.json --output-root artifacts\work078\run_a\step --manifest artifacts\work078\run_a\manifest.json
Exit: 0; status=passed; candidate_count=5

same command with run_b output root and manifest
Exit: 0; status=passed; all five STEP hashes and manifest SHA-256 identical

python -m unittest tests.test_brep_grammar tests.test_repository_contract -v
Exit: 0
Ran 15 tests in 0.713s — OK (skipped=3 kernel tests in non-CadQuery Python)

python -m compileall -q src scripts\cad\generate_brep_feature_corpus.py tests\test_brep_grammar.py
Exit: 0

python -m unittest discover -s tests -q
Exit: 0
Ran 496 tests in 300.327s — OK (skipped=3)
```

The three skipped tests are not missing evidence: they were separately executed and passed inside the pinned CadQuery environment as recorded above.

## Falsification, contradicting evidence, and confidence

An initial pre-admission hollow-housing fixture placed the stepped bore in the already-empty centre after shelling. The kernel correctly returned an empty cut result and the corpus test rejected it. The fixture was changed before admitted replay to place a smaller stepped bore in actual wall material. This contradicts any assumption that a syntactically legal feature sequence necessarily performs causal material removal.

The shell operator also exposed an OCCT representation in which one valid solid was wrapped in a `Compound`. The implementation unwraps only the exact one-solid case; it does not fuse, heal, or alter geometry. A deliberately disconnected two-solid pattern remains rejected as a final part.

Alternative explanations for byte stability include the shared CadQuery/OCCT exporter and pinned environment. Missing evidence includes independent FreeCAD inspection, semantic-interface recovery after STEP, cross-tool B-rep comparison, arbitrary parameter-space robustness, material/process constraints, and structural/physical correlation. Confidence is high for the exact tested corpus/toolchain and low outside the declared grammar domain.

## Limitations and follow-up

V1 lacks freeform loft/sweep, arbitrary transforms and edge queries, threads/gears, sheet-metal/composite process history, and persistent semantic faces. Work 079 must add evidence-bearing material and manufacturing constraints. Work 081 must independently inspect STEP geometry; stable STEP hashes do not establish stable face numbers or physical validation.
