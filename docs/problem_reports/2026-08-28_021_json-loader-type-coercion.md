# Work 021 Problem Report: JSON Loader Type Coercion

Status: Resolved

Thai companion: `2026-08-28_021_json-loader-type-coercion.th.md`

## Problem

Code review after the first passing Work 021 focused suite found that the JSON
architecture loader called `str(...)` on `schema_version`, `architecture_id`,
module identity/stage/version, and every signal. A malformed declaration such
as `"architecture_id": 123` could therefore become the valid-looking string
`"123"` instead of failing closed.

## Impact

The committed reference JSON uses correct string types, so its fingerprint and
stage evidence were not affected. However, accepting a wrong JSON type would
weaken the central configuration contract and could make producer/consumer
identity differ from the author's actual declaration.

## Fix

Add strict JSON string and string-array readers. Root and module string fields
must now already be JSON strings; list items must already be strings. No type is
coerced. Add a regression fixture with numeric `architecture_id` and require a
`CouplingContractError`.

## Verification

The corrected loader and its regression case passed all Work 021 and repository
gates on 2026-08-28:

```powershell
python -m unittest tests.test_coupling_contracts -v
# Ran 12 tests ... OK (exit 0)

python -m unittest discover -s tests -v
# Ran 166 tests ... OK (exit 0)

python scripts/validate_coupling_contracts.py
# invalid JSON types rejected; exit 0

python -m compileall -q src scripts tests
# exit 0
```

The loader now preserves declaration intent by rejecting the wrong JSON type;
it does not silently repair or reinterpret it.
