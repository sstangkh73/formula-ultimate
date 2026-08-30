# Fatigue Damage and Life Acceptance

Thai companion: `FATIGUE_DAMAGE_ACCEPTANCE.th.md`

## Outcome and claim boundary

Work 044 passed deterministic rainflow counting, Goodman mean-stress correction, synthetic Basquin S-N life, append-only Miner damage, first-crossing localization, uncertainty emission, replay, and unsupported-domain rejection.

This validates arithmetic and event contracts only. It is not sourced material life, crack-growth validation, multiaxial/non-proportional fatigue, strain-life/plastic hysteresis, environment/process evidence, or a real component service-life claim.

## Model

The synthetic record declares `Sa_ref=200 MPa`, `N_ref=1000`, Basquin exponent `m=5`, corrected-stress domain `80..300 MPa`, ultimate stress `500 MPa`, Goodman correction, and life-scatter factor `2`:

```text
Sa_corrected = Sa / (1 - Sm/Su)
N = N_ref (Sa_corrected/Sa_ref)^(-m)
D = sum(n_i/N_i)
failure crossing: first D >= 1
```

NASA references describe rainflow as reducing reversal histories to cycle range/mean events, Palmgren-Miner damage as a sum of life fractions, and modified Goodman correction for combined alternating/mean stress. The Work 044 curve values remain synthetic and prohibited from design fitness.

## Results

- Constant fully reversed `Sa=200 MPa`: rainflow counted exactly `1200` cycles, cumulative `D=1.2`, and localized the first failure at cycle `1000`. Damage was not clipped to `1`.
- High→low blocks: `300` cycles at `Sa=240 MPa`, then `1000` at `160 MPa`; final `D=1.074176`, first crossing at cycle `1073.632813`.
- Low→high blocks: the same bins in reverse order; final `D=1.074176`, first crossing at cycle `1270.190329`.
- Positive mean case `50..250 MPa`: `Sa=100 MPa`, `Sm=150 MPa`, Goodman-corrected `Sa=142.857143 MPa`, predicted life `5378.24` cycles, and `100` cycles give `D=0.01859344`.
- Six negative controls rejected overload, below-domain stress, mean stress at ultimate, missing curve, missing provenance, and non-finite history.

The equal final Miner sums under block permutation are a model property, not proof that real materials lack sequence effects. The differing event-cycle chronology remains observable.

## Falsification review

Supporting evidence includes exact constant cycle count/damage, an unclipped first crossing, deterministic identical replay, chronological block events, Goodman correction, uncertainty intervals on every ledger entry, and exact domain rejection. No admitted result contradicts the preferred arithmetic hypothesis.

The central alternative explanation and limitation is Miner linear accumulation: it omits load interaction, overload retardation, residual stress evolution, and crack growth. Missing evidence includes sourced S-N scatter, surface/notch/process/temperature/environment records, multiaxial and strain-life validation, physical spectrum tests, and fracture-mechanics growth. Confidence is high for deterministic accounting only.

## Reproduction

```powershell
.\scripts\run_work044.ps1
py -3.14 -m unittest tests.test_fatigue_damage -v
```

Machine-readable evidence is written to ignored `artifacts/work044/experiment_summary.json`.
