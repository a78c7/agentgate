# AgentGate Adoption Guide

AgentGate is for developers and teams that use AI coding agents and want a lightweight safety gate before pull requests.

## Who Should Use It

- Solo developers using Codex, Claude Code, Cursor, or similar tools.
- Teams that want a pre-PR check for risky paths, secret-like text, workflow edits, oversized diffs, and missing test evidence.
- Maintainers who want agent-generated changes to include clear review context.
- Repositories where security-sensitive paths should not be changed casually.

## Who Should Not Treat It As Enough

- Teams that need full SAST, dependency scanning, or compliance tooling.
- Projects that expect automated merge approval.
- Repositories where human review is optional.

AgentGate is a guardrail. It does not prove that a change is correct or secure.

## Local CLI Flow

Ask your agent to make a small change, then inspect the diff and run:

```bash
python3 agentgate.py check --repo . --config agentgate.config.example.json
```

For a specific patch:

```bash
python3 agentgate.py check --diff path/to/change.patch --config agentgate.config.example.json
```

Run tests after fixing any blocking findings:

```bash
python3 -m unittest discover -s tests
```

## Codex Workflow

1. Ask Codex to make a scoped change.
2. Review the diff locally.
3. Run AgentGate before staging or opening a PR.
4. Run the project tests.
5. Create a draft PR for human review.

See [examples/codex-workflow.md](examples/codex-workflow.md).

## Claude Code Workflow

1. Ask Claude Code to keep the change small and avoid sensitive paths.
2. Review generated changes.
3. Run AgentGate on the repository diff.
4. Fix blocking findings.
5. Open a draft PR only after tests and human review.

See [examples/claude-code-workflow.md](examples/claude-code-workflow.md).

## Cursor Workflow

1. Use Cursor for a focused code edit.
2. Inspect the changed files and generated diff.
3. Run AgentGate from the terminal.
4. Run tests and include evidence in the PR body.
5. Keep a human reviewer in the loop.

See [examples/cursor-workflow.md](examples/cursor-workflow.md).

## GitHub Action Flow

Add AgentGate as a pull request workflow after checkout:

```yaml
- name: Build PR diff
  run: git diff origin/${{ github.base_ref }}...HEAD > pr.diff

- name: Run AgentGate
  uses: a78c7/agentgate@v0.1.0
  with:
    diff-path: pr.diff
    config-path: agentgate.config.example.json
```

See [docs/github-action-usage.md](docs/github-action-usage.md).

## Team Rollout

Start with visibility before strict blocking:

1. Run AgentGate locally on a few agent-generated changes.
2. Add the GitHub Action with default settings.
3. Review warnings and false positives.
4. Add repository-specific forbidden paths.
5. Block forbidden paths, workflow changes, and missing test evidence.
6. Consider `fail-on-warning` only after the team agrees on the signal quality.

## Handling False Positives

When AgentGate reports a false positive:

- Confirm that the diff is safe through human review.
- Add a narrow config exception only for the relevant path or keyword.
- Keep the default safety rules intact for the rest of the repo.
- Document the reason in the PR body.

Avoid broad overrides unless the repo has a clear replacement control.

## Safety Boundary

AgentGate does not read cookies, keychain data, password managers, token values, credentials, or private secrets. It does not upload code, call external telemetry, create PRs, comment on PRs, or handle payment, KYC, payout, withdrawal, tax, wallet, or banking flows.
