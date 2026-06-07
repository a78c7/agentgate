# AgentGate

A safety-first CLI and GitHub Action that checks AI-generated code changes before they become a pull request.

AgentGate 是一个安全优先的 CLI + GitHub Action，用来在 Codex / Claude Code / Cursor / 其他 AI agent 生成改动之后，检查这些改动是否安全、是否可测试、是否不该进入 PR。

AgentGate is open source and local-first.

It does not:

- Read cookies, keychain data, password managers, private credentials, or tokens.
- Read environment variables for tokens.
- Upload code.
- Call external APIs.
- Use paid services.
- Handle KYC, payment, payout, withdrawal, wallet, or tax flows.
- Enable GitHub Sponsors.
- Automatically comment on pull requests.
- Automatically create pull requests.

## Features

- Python standard-library CLI.
- Composite GitHub Action.
- Unified diff scanning.
- Repository mode using `git diff --cached` or `git diff`.
- Markdown and JSON reports.
- Blocking checks for forbidden paths, forbidden keywords, workflow changes, and large diffs.
- PR body checks for Summary, Changes, Tests, Risk, test evidence, and optional AI disclosure.
- Dependency lockfile warnings.
- Conservative default configuration.

## Quickstart

Run a safe example:

```bash
python3 agentgate.py check --diff examples/safe-diff.patch --config agentgate.config.example.json
```

Run JSON output:

```bash
python3 agentgate.py check --diff examples/unsafe-secret-diff.patch --config agentgate.config.example.json --format json
```

Check a repository:

```bash
python3 agentgate.py check --repo . --config agentgate.config.example.json
```

Generate a report:

```bash
python3 agentgate.py check --diff examples/safe-diff.patch --config agentgate.config.example.json --output examples/sample-report.md
```

Print default config:

```bash
python3 agentgate.py init-config
```

## Exit Codes

- `0` = pass
- `1` = warnings only
- `2` = blocked

## GitHub Action Usage

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

To fail on warnings:

```yaml
      - name: Run AgentGate
        uses: yourname/agentgate@v0.1.0
        with:
          diff-path: pr.diff
          fail-on-warning: "true"
```

## Checks

AgentGate checks:

- Forbidden paths such as `.env`, `secrets/`, `auth/`, `payment/`, `kyc/`, `migrations/`, and `.github/workflows/`.
- Forbidden keywords such as `password`, `token`, `secret`, `credential`, `oauth`, `payment`, `stripe`, `wallet`, `crypto`, `kyc`, `exploit`, `rce`, `xss`, `csrf`, and `ssrf`.
- Diff size limits.
- Missing PR body sections.
- Missing test command/result evidence.
- Missing optional AI disclosure.
- Dependency changes without lockfile updates.

## Configuration

Start from:

```text
agentgate.config.example.json
```

Custom `forbidden_paths` and `forbidden_keywords` append to defaults unless:

- `override_default_forbidden_paths` is `true`
- `override_default_forbidden_keywords` is `true`

Safety defaults are intentionally conservative.

## Development

Run tests:

```bash
python3 -m unittest discover -s tests
```

Generate sample report:

```bash
python3 agentgate.py check --diff examples/safe-diff.patch --config agentgate.config.example.json --output examples/sample-report.md
```

Build release ZIP:

```bash
bash package-release.sh
```

## Docs

- [Safety model](docs/safety-model.md)
- [Config reference](docs/config-reference.md)
- [GitHub Action usage](docs/github-action-usage.md)
- [AI agent workflow](docs/ai-agent-workflow.md)
- [Examples](docs/examples.md)

## License

MIT License. See [LICENSE](LICENSE).
