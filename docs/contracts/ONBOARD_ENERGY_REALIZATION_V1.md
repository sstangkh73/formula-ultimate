# Onboard Energy Realization V1

Thai companion: `ONBOARD_ENERGY_REALIZATION_V1.th.md`

Status: Implemented by Work 120 as bounded Level-0 reference evidence.

## Boundary, geometry and state

This contract pins Work 115 thermal, Work 116 material-scope and Work 119 realized-actuation identities. One disclosed synthetic stored-electric/DC route includes active storage, enclosure shell, insulation, connectors, four mounts and converter. Active mass and energy derive from volume, density and specific energy; enclosure and connector masses derive from geometry; all other counted hardware masses are explicit. External replenishment is prohibited and initial stored state and modeled losses are inside the energy boundary.

The reference has nominal active energy `28.8 MJ`, usable fraction `0.8`, initial fraction `0.8`, maximum output `15000 W`, efficiency `0.95`, nominal voltage `400 V`, connector resistance `0.02 ohm`, and applicability `280-330 K`. Delivered output plus conversion/conductor loss must equal stored-energy decrease within `1e-8 J`. Loss energy raises one registered lumped thermal capacity; operation stops at the temperature bound.

## Controls and limitations

Empty storage, excessive demand, disconnected converter, thermal limit, omitted containment, hidden replenishment and inconsistent energy boundary are mandatory controls. Missing containment or hidden external energy fails closed; rate and temperature limits remain observable states rather than silent corrections.

Unsupported chemistry hazards, alternative field storage/conversion, aging and fault propagation remain unresolved extension domains. Work 116 material eligibility remains blocked. This contract is not permission to build or energize hardware and does not establish chemistry safety, validated capacity/rate/life, technology superiority/neutrality or physical validation.
