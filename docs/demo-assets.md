# Demo Assets

AgentGate includes local SVG assets that can be used in README previews, launch posts, or demos.

## Workflow Diagram

```text
assets/agentgate-flow.svg
```

Shows the intended flow:

```text
AI agent -> AgentGate -> human review -> tests -> PR
```

## CLI Demo

```text
assets/cli-demo.svg
```

Shows a blocked `unsafe-secret-diff.patch` report.

## Suggested Demo Script

1. Show an AI-generated diff.
2. Run:

```bash
python3 agentgate.py check --diff examples/unsafe-secret-diff.patch --config agentgate.config.example.json
```

3. Point out the blocked `.env` path and placeholder secret-like keywords.
4. Run:

```bash
python3 agentgate.py check --diff examples/safe-diff.patch --config agentgate.config.example.json
```

5. Explain that AgentGate is a pre-PR gate, not a replacement for human review.
