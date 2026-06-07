# AI Agent Workflow

Use AgentGate after an AI coding agent has generated changes and before the work becomes a pull request.

```text
AI agent changes
-> git diff
-> AgentGate check
-> human review
-> tests
-> pull request
```

## Recommended Local Flow

1. Ask Codex, Claude Code, Cursor, or another AI agent to make a small change.
2. Review the diff locally.
3. Run AgentGate:

```bash
python3 agentgate.py check --repo . --config agentgate.config.example.json
```

4. Fix blocking findings.
5. Add PR body sections and test evidence.
6. Run tests.
7. Open a PR only after human review.

## Keep Human Control

AgentGate does not replace human review. It is a gate for obvious safety and process risks.

## Suggested Agent Instruction

Give your coding agent a clear boundary before it edits files:

```text
Do not touch secrets, tokens, auth, payment, KYC, wallet, migration, or GitHub Actions workflow files.
Keep the change small.
Include Summary, Changes, Tests, and Risk sections in the PR body.
Run AgentGate before proposing a PR.
```

See `examples/sample-agent-prompt.md`.
