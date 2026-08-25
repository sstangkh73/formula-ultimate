# Independent Energy-Conservation Audit

Status: Implemented for Work 013

Thai companion: `ENERGY_CONSERVATION_AUDIT.th.md`

## Boundary and convention

The auditor checks declared interval energy over a compiled Work 012 graph. All
energy uses joules. Input, output, transfer, and declared loss are nonnegative;
stored-energy change is signed (positive stored, negative released).

```text
component residual = E_in - E_out - E_loss - delta_E_stored
tolerance = absolute_j + relative * max(abs(all declared/observed terms))
```

It separately checks component input/output against sums of connection
transfers. Exact component and connection evidence coverage is required.
Residuals are reported and never corrected.

## Status rules

`valid` requires every balance and interface residual within tolerance, correct
connection endpoints, unique evidence, and no missing/extra evidence. Otherwise
status is `invalid` with ordered violations. Default tolerances are `1e-9 J`
absolute and `1e-12` relative.

The reference `100 J` chain releases `100 J` from storage, loses `10 J` in the
motor, and stores `90 J` in the road sink, closing at `0 J`. Increasing motor
output to `95 J` while retaining `10 J` loss yields `-5 J`; declaring `20 J`
loss while output remains `90 J` yields `-10 J`. Both are invalid.

```powershell
python scripts/validate_energy_audit.py
python -m unittest tests.test_energy_audit -v
```

## Limitations

This algebraic audit does not prove source equations, power integration,
efficiency maps, or physical truth. It audits supplied evidence only. Thermal
state, uncertainty, regenerative timing, and race integration remain later
work. A valid audit is necessary evidence, not physical validation.
