# Codex Workflow Example

Use this flow when Codex generates a local change and you want to check it before opening a pull request.

## Flow

1. Ask Codex to make a scoped change.
2. Review the changed files and local diff.
3. Run AgentGate.
4. Run project tests.
5. Open a draft PR.
6. Keep human review as the final decision point.

## Example Commands

```bash
git diff > codex-change.patch
python3 agentgate.py check --diff codex-change.patch --config agentgate.config.example.json
python3 -m unittest discover -s tests
```

If the change is staged:

```bash
python3 agentgate.py check --repo . --config agentgate.config.example.json
```

## Suggested Codex Instruction

```text
Make the smallest change needed.
Do not touch secrets, tokens, auth, payment, KYC, wallet, migration, or GitHub Actions workflow files.
After editing, run AgentGate and tests.
Do not open or merge a PR without human review.
```

## Boundary

AgentGate does not replace human review. It does not read secrets, cookies, keychain data, password managers, token values, or private credentials. It does not upload code or create PRs.
