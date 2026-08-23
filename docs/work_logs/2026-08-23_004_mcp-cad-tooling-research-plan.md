# Work Plan 004: MCP-Compatible Engineering CAD Research

Date: 2026-08-23
Status: Completed

## Objective

Research software capable of detailed mechanical-part design that can be
controlled through the Model Context Protocol (MCP), then recommend a practical
toolchain for Formula Ultimate's future agent-designed 3D component pipeline.

## Scope

- Evaluate engineering CAD, programmatic CAD, mesh/generative modeling, and
  adjacent validation tools only when they materially support the pipeline.
- Distinguish native/official MCP support from community MCP servers and custom
  MCP feasibility.
- Verify current capabilities from official product documentation and primary
  MCP project repositories.
- Compare parametric solids/B-rep, constraints, assemblies, STEP/STL export,
  scripting/API access, headless use, Windows support, licensing, determinism,
  MCP maturity, and engineering suitability.
- Recommend a near-term stack for Formula Ultimate rather than selecting a tool
  solely because an MCP demo exists.

## Non-Goals

- Installing or connecting any CAD/MCP software in this work item.
- Purchasing licenses or changing external accounts.
- Treating mesh generation alone as validated mechanical engineering.
- Claiming an unofficial MCP server is supported by the CAD vendor.
- Designing the first Formula Ultimate component.

## Planned Deliverables

- `docs/research/MCP_CAD_TOOLING_REPORT.md`
- `docs/research/MCP_CAD_TOOLING_REPORT.th.md`
- Separate English and Thai Work 004 result records with source and validation
  evidence.

## Evaluation Criteria

1. Mechanical design depth and geometric representation.
2. Parametric constraints, assemblies, materials, and manufacturability path.
3. Automation/API quality and deterministic artifact generation.
4. Export formats and interoperability with CFD/FEA/property extraction.
5. MCP provenance, feature coverage, maintenance, and security boundary.
6. Headless/batch operation, reproducibility, and compute scaling.
7. Cost, license restrictions, operating-system fit, and vendor lock-in.
8. Suitability for agent exploration versus authoritative validation.

## Research Method

1. Search official CAD documentation for current geometry and automation
   capabilities.
2. Search primary MCP repositories and vendor materials for actual integrations.
3. Inspect install/architecture/tool surfaces for the strongest candidates.
4. Classify MCP support as official, vendor-adjacent, community, custom-only, or
   unverified.
5. Compare candidates against Formula Ultimate's 1D-to-3D trusted-evaluator
   architecture.
6. Produce a tiered recommendation, implementation path, risks, and a small
   proof-of-concept plan.

## Validation Plan

- Cite every time-sensitive MCP/support claim near the statement it supports.
- Prefer official documentation for CAD capabilities and primary repositories
  for community MCP implementations.
- Record research date and clearly mark inference versus confirmed facts.
- Verify URLs open and directly support the associated claim.
- Run repository Markdown companion, Python, compilation, and staged-diff tests.

## Success Criteria

- The report identifies at least three credible tool paths and their tradeoffs.
- Official and unofficial MCP support are never conflated.
- The recommendation covers detailed solid design, exploratory geometry, neutral
  interchange, and independent validation.
- The report produces an actionable Formula Ultimate proof-of-concept sequence.
- English and Thai reports preserve equivalent technical findings and citations.

## Risks and Controls

- Fast-moving MCP ecosystem: include access date, provenance, and maintenance
  caveats.
- Demo bias: prioritize geometry kernels, APIs, export, and validation over
  screenshots or popularity.
- Repository supply-chain risk: recommend pinned revisions, local sandboxing,
  least privilege, and source review for community MCP servers.
- Vendor lock-in: prioritize neutral artifacts such as STEP, B-rep, STL/3MF,
  solver inputs, and content-addressed metadata.
