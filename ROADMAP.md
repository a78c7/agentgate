# AgentGate Roadmap

AgentGate is a small safety gate for AI-agent generated code changes. The roadmap favors conservative checks, clear reports, and workflows that keep humans in control.

No dates are promised. Items can move based on user feedback and maintainer capacity.

## v0.1 Completed

- Python standard-library CLI.
- Composite GitHub Action.
- Unified diff checks.
- Repository mode using staged or unstaged `git diff`.
- Markdown and JSON reports.
- Forbidden path checks.
- Forbidden keyword checks.
- GitHub Actions workflow modification blocking.
- Diff size limits.
- PR body section and test evidence checks.
- Dependency lockfile warnings.
- Example diffs, sample PR body, and sample report.
- Unit tests and release packaging.

## v0.2 Ideas

- SARIF output for GitHub code scanning and security dashboards.
- GitHub Step Summary output for easier workflow reading.
- Better PR body checks for common AI-agent workflows.
- Config presets for common rollout modes.

## v0.3 Ideas

- Language-aware dependency checks for JavaScript, Python, Go, Rust, and mixed repos.
- Monorepo config with path-specific rules.
- Docs-only mode for low-risk documentation PRs.
- More examples for agent-assisted development workflows.

## Principles

- Do not weaken the default safety posture.
- Do not read secrets, cookies, keychain data, password managers, token values, or credentials.
- Do not upload code or call external telemetry.
- Do not create PRs or comments automatically.
- Keep AgentGate useful before human review, not as a replacement for review.
