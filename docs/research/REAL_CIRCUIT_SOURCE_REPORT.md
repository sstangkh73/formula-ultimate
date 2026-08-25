# Real-Circuit Source Report — Catalogue v1

Status: Evidence baseline captured on 2026-08-25

English source for Thai companion: `REAL_CIRCUIT_SOURCE_REPORT.th.md`

## Selection rationale

The set deliberately spans a narrow street circuit, a maximum-speed circuit, a
long elevation-sensitive circuit, a hot and confined night street circuit,
high-speed direction-change circuits, a short high-downforce circuit, a very
high-altitude circuit, a desert braking/traction circuit, and an undulating
counterclockwise circuit. The purpose is not to reproduce the championship; it
is to expose a design agent to conflicting real-world demands before geometry
generation.

## Captured facts

| Profile | Length (m) | Laps | Race (m) | Turns | Published width (m) | Primary design contrast |
|---|---:|---:|---:|---:|---:|---|
| Monaco 2026 | 3,337 | 78 | 260,286 | 19 | min 7 | confinement and agility |
| Monza current | 5,793 | 53 | 306,720 | 11 | 10–12 | top speed and braking |
| Spa 2026 | 7,004 | 44 | 308,052 | 19 | unresolved | long lap, elevation, fast corners |
| Singapore 2025 | 4,940 | 62 | 306,143 | 19 | unresolved | heat, bumps, walls, traction |
| Suzuka 2026 | 5,807 | 53 | 307,471 | 18 | 10–16 | high-speed direction changes |
| Silverstone 2026 | 5,891 | 52 | 306,198 | 18 | unresolved | sustained fast-corner aero load |
| Hungaroring 2026 | 4,381 | 70 | 306,630 | 14 | unresolved | linked corners and high downforce |
| Mexico City current | 4,304 | 71 | 305,354 | 17 | unresolved | `2,285 m` air density and cooling |
| Bahrain current | 5,412 | 57 | 308,238 | 15 | unresolved | braking, traction, temperature |
| Sao Paulo current | 4,309 | 71 | 305,879 | 15 | 12–15 | banking, camber, climb and weather |

## Source hierarchy

Facts were accepted from FIA/Formula 1, the circuit operator, or the event
organizer. Search-result blogs and unsourced circuit databases were not used as
hard-dimensional evidence. A qualitative description can support an ordinal
pressure hypothesis, but phrases such as “narrow” or “tight” were not converted
into metres.

Official Formula 1 circuit/statistic sources:

- [Monaco 2026 circuit guide](https://www.formula1.com/en/latest/article/circuit-guide-everything-you-need-to-know-about-the-circuit-de-monaco.vFsmfGHr6RWyLFtxi58wi)
- [Monza circuit page](https://www.formula1.com/en/information/italy-autodromo-nazionalemonza.FiJN1jnQlRLeHqOxIt13m)
- [Spa 2026 circuit guide](https://www.formula1.com/en/latest/article/circuit-guide-everything-you-need-to-know-about-the-circuit-de-spa-francorchamps.pC5N3J3W9LEj8REFvU6FX)
- [Singapore 2025 preview](https://www.formula1.com/en/latest/article/need-to-know-the-most-important-facts-stats-and-trivia-ahead-of-the-2025-singapore.468A8YSelm8nsKywLuGTf) and [FIA 2025 media kit](https://www.fia.com/sites/default/files/spg2025_0062_f1_mediakit_2025_eng_a4_250623_view.pdf)
- [Suzuka 2026 circuit guide](https://www.formula1.com/en/latest/article/circuit-guide-everything-you-need-to-know-about-the-suzuka-circuit.2BbgsRdkeux78UBGbmYiZV)
- [Silverstone 2026 circuit guide](https://www.formula1.com/en/latest/article/circuit-guide-everything-you-need-to-know-about-silverstone-2026.5Sl0O8g393enBWVIkjRzOr)
- [Hungaroring 2026 circuit guide](https://www.formula1.com/en/latest/article/circuit-guide-everything-you-need-to-know-about-the-hungaroring.4ddtLbzLWLRjli7Y793jqh)
- [Mexico City circuit page](https://www.formula1.com/en/information/mexico-autodromo-hermanos-rodriguez-mexico-city.1K2WPfBcI8kTXjcTHcbsBM) and [Formula 1 altitude evidence](https://ticketing.formula1.com/tickets/en/mexico/general-admission-f1-ciudad-de-mexico-waitlist)
- [Bahrain circuit page](https://www.formula1.com/en/information/bahrain-international-circuit.2CaIdaOTCgQ3Yfnb37NmSS)
- [Sao Paulo circuit page](https://www.formula1.com/en/information/brazil-autodromo-jose-carlos-pace-sao-paulo.5z2RfrmiTTfEP6Wnxv1yIW)

Official width evidence:

- Monaco: the official Mexico GP organizer's engineering article describes
  Monaco's streets as only `7 m` wide and explains how increasing car size
  degrades racing on the circuit: [vehicle-size article](https://www.mexicogp.mx/noticia/asi-afecta-el-tamano-de-los-autos-a-la-formula-1/?IDM=LANG_EN).
- Monza: the circuit operator publishes `min 10 m – max 12 m`:
  [Monza layout](https://www.monzanet.it/en/circuit/).
- Suzuka: the circuit operator publishes `10–16 m`:
  [Suzuka course guide](https://www.suzukacircuit.jp/eng/course_s/).
- Sao Paulo: the municipal circuit operator publishes `12–15 m`:
  [Interlagos circuit page](https://autodromodeinterlagos.prefeitura.sp.gov.br/circuito).

The [Bahrain operator page](https://www.bahraingp.com/corporate-sales/track-hire/)
publishes `14–15 m` under **Inner Track**, not **Grand Prix Track**. It is
explicitly non-applicable to the Formula 1 width gate and Bahrain remains
indeterminate.

## Evidence conflict retained

Singapore's temporary layout has changed. The FIA 2025 media kit identifies a
`4.94 km`, 19-turn, 62-lap layout and `306.143 km` race distance. The organizer
currently advertises a future `4.927 km` figure, while its historical 2008 page
published `10–15 m` width for the old 5.067 km layout. Catalogue v1 therefore
pins Singapore to the 2025 FIA layout and refuses to transfer the historical
width into the current hard gate. This is an intentional `indeterminate`, not a
missing-value default.

## Review discipline

Independent variables are circuit profile and proposed vehicle width.
Dependent variables are the static-width status, ISA density where altitude is
known, race-scale values, and the eight-axis pressure vector. The control is
the same clearance policy and catalogue version for every vehicle candidate.

The preferred hypothesis is that exposing diverse real circuits before design
will prevent one unconstrained large vehicle from dominating. The deliberately
oversized `7.0 m` test falsifies universal eligibility because Monaco rejects it
with a `0.25 m` clearance on each side. Contradicting evidence is that a static
width pass does not prove the vehicle can turn; six profiles also lack current
minimum-width evidence. Alternative explanations for later performance include
the pressure scoring choices, missing surface/weather data, and vehicle control
quality rather than topology itself. Confidence is high in sourced race-scale
facts, medium in the four published width screens, and low-to-medium in the
ordinal pressure hypotheses until sensitivity analysis is run.
