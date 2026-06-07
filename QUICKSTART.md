# Quickstart

## Run The CLI

```bash
python3 agentgate.py check --diff examples/safe-diff.patch --config agentgate.config.example.json
```

Expected result: `PASS`, exit code `0`.

## Try A Blocked Diff

```bash
python3 agentgate.py check --diff examples/unsafe-secret-diff.patch --config agentgate.config.example.json
```

Expected result: `BLOCKED`, exit code `2`.

## Try A Warning

```bash
python3 agentgate.py check --diff examples/package-no-lock-diff.patch --config agentgate.config.example.json
```

Expected result: `WARNING`, exit code `1`.

## Generate Markdown Report

```bash
python3 agentgate.py check --diff examples/safe-diff.patch --config agentgate.config.example.json --output examples/sample-report.md
```

## Generate JSON Report

```bash
python3 agentgate.py check --diff examples/unsafe-secret-diff.patch --config agentgate.config.example.json --format json
```

## Check A Repository

AgentGate first checks staged changes. If there are no staged changes, it checks unstaged changes.

```bash
python3 agentgate.py check --repo . --config agentgate.config.example.json
```

## GitHub Action

Use `action.yml` as a composite action. See `docs/github-action-usage.md`.
