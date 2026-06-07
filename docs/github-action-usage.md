# GitHub Action Usage

AgentGate is a composite action.

```yaml
name: AgentGate

on:
  pull_request:

jobs:
  agentgate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Build PR diff
        run: git diff origin/${{ github.base_ref }}...HEAD > pr.diff

      - name: Run AgentGate
        uses: yourname/agentgate@v0.1.0
        with:
          diff-path: pr.diff
          config-path: agentgate.config.example.json
```

## JSON Report

```yaml
      - name: Run AgentGate
        uses: yourname/agentgate@v0.1.0
        with:
          diff-path: pr.diff
          format: json
          output-path: agentgate-report.json
```

## Fail On Warning

```yaml
      - name: Run AgentGate
        uses: yourname/agentgate@v0.1.0
        with:
          diff-path: pr.diff
          fail-on-warning: "true"
```

The action does not use Docker, third-party dependencies, secrets, or external APIs.
