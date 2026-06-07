# Cursor Workflow Example

Use this flow when Cursor assists with code edits and you want a guardrail before review.

## Flow

1. Use Cursor for a targeted edit.
2. Review the changed files.
3. Run AgentGate from the terminal.
4. Run tests.
5. Create a draft PR.
6. Ask a human reviewer to make the merge decision.

## Example Commands

```bash
git diff > cursor-change.patch
python3 agentgate.py check --diff cursor-change.patch --config agentgate.config.example.json
python3 -m unittest discover -s tests
```

If you prefer repo mode:

```bash
python3 agentgate.py check --repo . --config agentgate.config.example.json
```

## Suggested Cursor Prompt

```text
Make a focused change only.
Do not touch secrets, tokens, auth, payment, KYC, wallet, migrations, or GitHub Actions workflow files.
After the edit, summarize changed files and tests.
Use AgentGate before opening a pull request.
```

## Boundary

AgentGate does not replace human review. It does not read secrets, cookies, keychain data, password managers, token values, or private credentials. It does not upload code or create PRs.
