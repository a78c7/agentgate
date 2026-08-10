# Using AgentGate inside an agent harness

AgentGate is a deterministic safety and verification stage for a coding-agent workflow. It checks a unified diff or local repository diff after an agent finishes editing and before a human decides whether the work should proceed.

It is a harness component, not a complete agent harness: AgentGate does not plan tasks, call a model, execute agent tools, create pull requests, or approve changes.

## 1. Pre-PR verification

```text
agent completes task
-> harness exports or retains the diff
-> AgentGate checks the diff
-> exit 0
-> harness may continue to PR creation
```

Example command:

```bash
python3 agentgate.py check \
  --diff agent-change.patch \
  --config agentgate.config.example.json \
  --format json
```

## 2. Human-in-the-loop gate

Use the exit code and structured report to stop automatic continuation:

```python
# Conceptual harness pseudocode, not an AgentGate Python API.
agent_result = run_coding_agent(task)
gate = run_process([
    "python3", "agentgate.py", "check",
    "--diff", agent_result.diff_path,
    "--config", "agentgate.config.example.json",
    "--format", "json",
])

if gate.exit_code != 0:
    require_human_review(gate.stdout)
else:
    continue_to_pull_request()
```

Exit `0` means pass, `1` means warnings, and `2` means blocked or command error. A harness can accept warnings, require a human decision, or use `--fail-on-warning` to treat them as blocking.

## 3. CI verification

After a PR is opened, the bundled composite GitHub Action can apply AgentGate to the PR diff. This creates a second verification point under repository-owned CI policy:

```text
pull request opened
-> workflow builds PR diff
-> AgentGate GitHub Action
-> report + exit code
-> human review and merge decision
```

See [GitHub Action usage](github-action-usage.md) for a working workflow.

## Inputs and outputs

AgentGate accepts either:

- `--diff PATH` for a unified diff file; or
- `--repo PATH` for staged changes, falling back to unstaged changes.

Optional inputs include a JSON policy file and PR body Markdown. Output is Markdown by default or JSON with `--format json`.

The JSON document contains:

- `result`
- `exit_code`
- `summary`
- `blocking_findings`
- `warnings`
- `passed_checks`

These fields let a harness display evidence, route a blocked change to a human, or record the verification result without parsing prose.

## Vendor-neutral placement

AgentGate can be placed in workflows that use Codex, Claude Code, Cursor, OpenHands, or another coding agent that produces a local diff. These are workflow placements, not official product integrations.

The boundary remains the same: AgentGate checks configured, diff-visible risk. It does not prove correctness, execute tests, or replace human review.

