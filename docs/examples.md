# Examples

## Pass

```bash
python3 agentgate.py check --diff examples/safe-diff.patch --config agentgate.config.example.json
```

## Blocked Secret Diff

```bash
python3 agentgate.py check --diff examples/unsafe-secret-diff.patch --config agentgate.config.example.json
```

## Blocked Auth Diff

```bash
python3 agentgate.py check --diff examples/unsafe-auth-diff.patch --config agentgate.config.example.json
```

## Warning For Dependency Without Lockfile

```bash
python3 agentgate.py check --diff examples/package-no-lock-diff.patch --config agentgate.config.example.json
```

## PR Body Check

```bash
python3 agentgate.py check --diff examples/safe-diff.patch --config agentgate.config.example.json --pr-body examples/sample-pr-body.md
```

## JSON Output

```bash
python3 agentgate.py check --diff examples/unsafe-secret-diff.patch --config agentgate.config.example.json --format json
```

## Sample GitHub Action

See:

```text
examples/sample-github-action.yml
```

## Sample Agent Prompt

See:

```text
examples/sample-agent-prompt.md
```
