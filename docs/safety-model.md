# Safety Model

AgentGate is designed for local pre-PR review of AI-generated code changes.

## What It Checks

- Forbidden paths.
- Forbidden keywords in added diff lines.
- GitHub Actions workflow modifications.
- Diff size.
- PR body sections.
- Test evidence.
- Optional AI disclosure.
- Dependency changes without lockfile updates.

## What It Does Not Do

AgentGate does not:

- Read cookies.
- Read keychain data.
- Read password managers.
- Read environment variable tokens.
- Read private credentials.
- Upload code.
- Call external APIs.
- Handle KYC, payment, payout, withdrawal, wallet, tax, or banking flows.
- Automatically comment on PRs.
- Automatically create PRs.
- Enable GitHub Sponsors.

## Conservative Defaults

Sensitive paths and terms block by default. Dependency lockfile risk warns by default. Missing PR body test evidence blocks only when `--pr-body` is provided and required by config.
