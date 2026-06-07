# Social Announcement Copy

## Short

I released AgentGate, a safety-first CLI + GitHub Action for checking AI-generated code changes before they become pull requests.

It blocks risky paths, secret-like keywords, workflow changes, oversized diffs, and missing PR evidence.

Open source: https://github.com/a78c7/agentgate

## Technical

AgentGate is a Python standard-library CLI and composite GitHub Action for teams using Codex, Claude Code, Cursor, or other AI coding agents.

It checks unified diffs for:

- forbidden paths like `.env`, `auth/`, `payment/`, `.github/workflows/`
- secret/auth/payment/security keywords
- large diffs
- missing PR body sections
- missing test evidence
- dependency changes without lockfiles

It calls no external APIs, reads no secrets, and uses no third-party dependencies.

Repo: https://github.com/a78c7/agentgate

## Safety-Focused

AI-generated code should not jump straight into a PR.

AgentGate adds a local pre-PR gate:

```text
AI-generated diff -> AgentGate -> human review -> tests -> PR
```

It does not read cookies, tokens, keychain data, or password managers. It does not auto-comment, auto-create PRs, call paid services, or handle payment/KYC/payout workflows.

Repo: https://github.com/a78c7/agentgate
