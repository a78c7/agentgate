# Quickstart

This guide gets you from clone to first AgentGate report in a few minutes.

## 1. Clone

```bash
git clone https://github.com/a78c7/agentgate.git
cd agentgate
```

## 2. Run A Passing Diff

```bash
python3 agentgate.py check --diff examples/safe-diff.patch --config agentgate.config.example.json
```

Expected:

- Result: `PASS`
- Exit code: `0`

## 3. Run A Blocked Diff

```bash
python3 agentgate.py check --diff examples/unsafe-secret-diff.patch --config agentgate.config.example.json
```

Expected:

- Result: `BLOCKED`
- Exit code: `2`

This example uses placeholder strings only. It demonstrates how AgentGate blocks `.env` and secret-like added lines.

## 4. Run A Warning Diff

```bash
python3 agentgate.py check --diff examples/package-no-lock-diff.patch --config agentgate.config.example.json
```

Expected:

- Result: `WARNING`
- Exit code: `1`

The example changes `package.json` without a lockfile.

## 5. Generate Markdown And JSON Reports

Markdown:

```bash
python3 agentgate.py check --diff examples/safe-diff.patch --config agentgate.config.example.json --output examples/sample-report.md
```

JSON:

```bash
python3 agentgate.py check --diff examples/unsafe-secret-diff.patch --config agentgate.config.example.json --format json
```

## 6. Check Your Own Repository

AgentGate checks staged changes first. If nothing is staged, it checks unstaged changes.

```bash
python3 agentgate.py check --repo . --config agentgate.config.example.json
```

## 7. Add The GitHub Action

Create a workflow that builds a PR diff and runs AgentGate:

```yaml
name: AgentGate

on:
  pull_request:

jobs:
  agentgate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0

      - name: Build PR diff
        run: git diff origin/${{ github.base_ref }}...HEAD > pr.diff

      - name: Run AgentGate
        uses: a78c7/agentgate@v0.1.0
        with:
          diff-path: pr.diff
          config-path: agentgate.config.example.json
```

## 8. Run Tests

```bash
python3 -m unittest discover -s tests
```

## Safety Reminder

AgentGate does not read cookies, keychains, password managers, token values, or private credentials. It does not upload code, call external APIs, create PRs, comment on PRs, or handle payment/KYC/payout flows.
