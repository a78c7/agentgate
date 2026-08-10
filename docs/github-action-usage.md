# GitHub Action Usage

AgentGate is a composite action. It does not use Docker, third-party dependencies, secrets, or external APIs.

## Basic Pull Request Workflow

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

## JSON Report

```yaml
      - name: Run AgentGate
        uses: a78c7/agentgate@v0.1.0
        with:
          diff-path: pr.diff
          format: json
          output-path: agentgate-report.json
```

## Fail On Warning

```yaml
      - name: Run AgentGate
        uses: a78c7/agentgate@v0.1.0
        with:
          diff-path: pr.diff
          fail-on-warning: "true"
```

## Upload A Markdown Report

```yaml
      - name: Run AgentGate
        uses: a78c7/agentgate@v0.1.0
        with:
          diff-path: pr.diff
          output-path: agentgate-report.md

      - name: Upload AgentGate report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: agentgate-report
          path: agentgate-report.md
```

## With PR Body Text

If your workflow writes a PR body file, pass it to AgentGate:

```yaml
      - name: Run AgentGate
        uses: a78c7/agentgate@v0.1.0
        with:
          diff-path: pr.diff
          pr-body-path: pr-body.md
          config-path: agentgate.config.example.json
```

## Notes

- Keep `fetch-depth: 0` so the base branch diff can be built.
- Store generated reports as artifacts if you want reviewers to inspect them.
- Keep AgentGate config in the repository so projects can tune warnings and blocking behavior explicitly.
