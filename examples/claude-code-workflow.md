# Claude Code Workflow Example

Use this flow when Claude Code generates a change and you want a pre-PR safety check.

## Flow

1. Ask Claude Code for a focused edit.
2. Inspect the generated diff.
3. Run AgentGate locally.
4. Fix any blocking findings.
5. Run the project test suite.
6. Open a draft PR for human review.

## Example Commands

```bash
git diff > claude-code-change.patch
python3 agentgate.py check --diff claude-code-change.patch --config agentgate.config.example.json
python3 -m unittest discover -s tests
```

For repository mode:

```bash
python3 agentgate.py check --repo . --config agentgate.config.example.json
```

## Suggested Claude Code Instruction

```text
Keep the change small and explain the risk.
Avoid secrets, tokens, auth, payment, KYC, wallet, migrations, and GitHub Actions workflow files.
Include Summary, Changes, Tests, and Risk sections in any PR draft.
Run AgentGate before suggesting that the change is ready.
```

## Boundary

AgentGate does not replace human review. It does not read secrets, cookies, keychain data, password managers, token values, or private credentials. It does not upload code or create PRs.
