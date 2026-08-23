# Work Plan 005: CAD and MCP Environment Bootstrap

Date: 2026-08-23
Status: Completed

## Objective

Audit the downloaded/installed CAD applications, establish a safe local MCP
environment for Formula Ultimate's first 3D research work, and preserve
reproducible evidence of what is actually connected and tested.

## Scope

- Locate and record installed/downloaded Autodesk Fusion, FreeCAD, CadQuery, and
  Blender versions and executable/runtime paths.
- Distinguish vendor-provided MCP servers from community/project MCP servers.
- Enable and verify the official Autodesk Fusion MCP when the installed Fusion
  version provides it.
- Install CadQuery and its reviewed project-contrib MCP in an isolated,
  project-specific environment with a pinned source revision when practical.
- Verify FreeCAD command-line/Python automation before selecting or installing a
  community MCP bridge.
- Verify the installed Blender version and determine whether the official
  Blender Lab MCP requirements are met; connect only through a reviewed path.
- Record MCP endpoints/configuration without exposing credentials or unrelated
  user data.
- Run non-destructive smoke tests with disposable geometry/artifacts.

## Non-Goals

- Uploading Formula Ultimate designs to cloud services.
- Purchasing or changing CAD subscriptions.
- Installing an unreviewed community MCP server from a moving branch.
- Granting arbitrary filesystem/network access to generated CAD code.
- Designing or optimizing the first research component.
- Calling a successful connection proof of engineering validation.

## Planned Deliverables

- `docs/3d/CAD_MCP_ENVIRONMENT.md`
- `docs/3d/CAD_MCP_ENVIRONMENT.th.md`
- Project-local ignored environments/configuration where needed.
- Separate English and Thai Work 005 result records with exact commands,
  versions, endpoints, tool inventories, test outputs, and limitations.

## Work Sequence

1. Read repository instructions and the applicable Windows/Codex setup skills.
2. Inventory executable paths, installed versions, downloaded installers, and
   current MCP configuration using read-only checks.
3. Review exact MCP package provenance and pin revisions before installation.
4. Bootstrap the CadQuery MCP environment and run import/server/tool smoke tests.
5. Verify FreeCAD headless automation with a disposable solid and neutral export.
6. Enable and probe the official Fusion MCP against a disposable/empty document.
7. Verify Blender version and official MCP compatibility; perform only a
   disposable connection test if installation is straightforward and reviewed.
8. Document confirmed, partial, blocked, and unverified components separately.
9. Run repository tests, compilation, bilingual coverage, and staged-diff gates.
10. Commit and push only repository-owned documentation/configuration/scripts;
    never commit installed environments, user credentials, or CAD caches.

## Validation Plan

- Record exact application and server versions.
- Verify executable discovery from fresh commands.
- For each connected MCP, capture initialization and discovered tool evidence.
- For each CAD smoke test, use a temporary directory and verify artifact type,
  dimensions/properties, and cleanup/recoverability.
- Confirm no credentials, tokens, or machine-specific secret configuration enter
  Git.
- Run the full repository test suite and GitHub Actions.

## Success Criteria

- At least CadQuery MCP is installed in an isolated environment and responds to
  a protocol/tool smoke test.
- FreeCAD headless automation is either proven with a disposable artifact or
  documented with an exact blocker.
- Fusion official MCP status is confirmed from the installed application, not
  assumed from web documentation.
- Blender official MCP compatibility is confirmed from the installed version.
- Environment documentation clearly states what is connected versus merely
  downloaded or installed.
- No sensitive or machine-global configuration is committed.

## Failure Criteria

- A community server is installed without a pinned/reviewed source identity.
- Generated code receives unrestricted access to unrelated files or secrets.
- A GUI screenshot or installed application is reported as an MCP connection.
- Test artifacts modify an existing user CAD project.
- A tool is described as validated without a reproducible command/tool result.

## Risks and Controls

- Installer ambiguity: resolve exact filenames, signatures/publisher, and target
  paths before execution.
- MCP code execution: use isolated environments, bounded temporary workspaces,
  least privilege, and reviewed tool surfaces.
- GUI state: use disposable documents and avoid saving over existing work.
- Version drift: record versions and pin community revisions.
- External accounts: do not upload, share, publish, or change billing/licensing.
- Partial automation: document user-only GUI steps rather than bypassing security
  or silently weakening the test.
