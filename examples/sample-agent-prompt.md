# Sample AI Agent Prompt

Use this prompt before asking a coding agent to work in a repository that uses AgentGate.

```text
Make the smallest reasonable change for the requested issue.

Before suggesting a PR:
- Keep the diff focused.
- Do not modify .env files, credentials, auth, payment, wallet, crypto, KYC, migrations, or GitHub Actions workflows.
- Do not add secrets, tokens, passwords, private keys, or credential-like values.
- Include a PR body with Summary, Changes, Tests, and Risk sections.
- Include the test command and pass/fail result.
- Disclose AI assistance if project policy requires it.

After the change, run:

python3 agentgate.py check --repo . --config agentgate.config.example.json
```
