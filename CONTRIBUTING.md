# Contributing

All changes follow the auditable workflow in `docs/WORK_PROTOCOL.md`.

Minimum requirements for a change:

1. Separate English and Thai plan records created before implementation.
2. A bounded change consistent with the plan.
3. Automated tests proportional to the claim being made.
4. Separate English and Thai result records with equivalent reproducibility
   evidence.
5. No stronger physics or research claim than the completed validation supports.

Every maintained English Markdown file must have a sibling `.th.md` translation.
Both versions are updated together; technical identifiers, equations, paths,
commands, units, values, and limitations must remain equivalent.

Use SI units internally. Include units in public names when ambiguity is
possible, for example `speed_mps`, `torque_nm`, and `temperature_k`.
