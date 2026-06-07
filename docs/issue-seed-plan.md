# Issue Seed Plan

These issues are intended to make the roadmap visible and give contributors concrete entry points.

Do not create duplicates. If an issue already exists, link to it instead of opening another one.

## Suggested Issues

### 1. Add SARIF output support

Add an optional `--format sarif` output so AgentGate results can be consumed by GitHub code scanning and other security dashboards.

Scope:

- Keep Markdown and JSON behavior unchanged.
- Map blocking findings and warnings to SARIF results.
- Add tests for at least one blocked diff and one warning diff.

### 2. Add GitHub Step Summary output

Add a workflow-friendly output mode that writes a readable summary to `$GITHUB_STEP_SUMMARY`.

Scope:

- Keep the composite action safety boundary unchanged.
- Make the summary readable in GitHub Actions.
- Avoid auto-commenting on PRs.

### 3. Add config preset: docs-only

Add a preset for documentation-only changes where Markdown and docs paths can be reviewed with lower noise while sensitive paths still block.

Scope:

- Keep forbidden path and forbidden keyword checks active.
- Do not weaken workflow modification blocking.
- Document when the preset is appropriate.

### 4. Add config preset: strict enterprise mode

Add a stricter preset for teams that want warnings treated as blocking and tighter diff size limits.

Scope:

- Include a sample config file.
- Document rollout guidance.
- Add tests for strict behavior.

### 5. Add examples for Codex / Claude Code / Cursor workflows

Expand workflow documentation for common AI coding tools.

Scope:

- Show where AgentGate runs in each workflow.
- Include test and human review steps.
- Repeat that AgentGate does not read secrets or upload code.

## Labels

Suggested labels:

- `enhancement`
- `good first issue`
- `documentation`
- `question`

If labels are not available, issues can still be created without labels.
