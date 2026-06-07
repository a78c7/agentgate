# AgentGate Product Report

## Overview

AgentGate is a safety-first CLI and GitHub Action that checks AI-generated code changes before they become pull requests.

It is built for developers using Codex, Claude Code, Cursor, and other AI coding agents.

## Implemented

- Python CLI using standard library only.
- Composite GitHub Action.
- Unified diff parser.
- Repository mode using `git diff --cached` or `git diff`.
- Markdown and JSON reports.
- Forbidden path checks.
- Forbidden keyword checks.
- Diff size checks.
- PR body section and test evidence checks.
- Optional AI disclosure check.
- Dependency lockfile warnings.
- Workflow modification blocking.
- Example diffs and report.
- Unit tests.
- Release packaging script.

## Safety Boundaries

AgentGate does not read cookies, keychain data, password managers, environment token values, credentials, or secrets. It does not call external APIs, upload code, handle KYC/payment/withdrawal/tax, enable Sponsors, auto-comment, or auto-create PRs.

## Release Artifact

```text
dist/agentgate-0.1.0.zip
```

## Verification

Run:

```bash
python3 -m unittest discover -s tests
python3 agentgate.py check --diff examples/safe-diff.patch --config agentgate.config.example.json --output examples/sample-report.md
bash package-release.sh
```
