# AgentGate Launch Notes

AgentGate is an open-source CLI and GitHub Action for checking AI-agent generated code changes before they become pull requests.

It is built for developers using Codex, Claude Code, Cursor, and similar coding agents.

## Why This Matters

AI-generated code can move quickly, but a fast diff can still:

- Touch secret or credential paths.
- Add token-like or payment-related text.
- Change GitHub Actions workflows.
- Modify dependencies without lockfiles.
- Skip test evidence.
- Produce a PR body with no review context.

AgentGate adds a small safety gate before the PR reaches reviewers.

## What To Say Publicly

AgentGate is a guardrail, not a guarantee. It does not prove that code is secure, correct, or ready to merge. It helps catch configured risk before human review.

## Good Launch Channels

- X for a short launch post and technical thread.
- LinkedIn for developer and engineering-lead context.
- Reddit communities such as r/opensource, r/webdev, and r/SideProject when the post is transparent and non-promotional.
- Hacker News Show HN if the repo and examples are clear.
- GitHub topics for discovery.

## X Short Post

I released AgentGate, an open-source CLI + GitHub Action for checking AI-agent generated code before it becomes a PR.

It blocks risky paths, secret-like text, workflow edits, oversized diffs, and missing test evidence.

Repo: https://github.com/a78c7/agentgate

## X Technical Post

AgentGate is a Python standard-library CLI and composite GitHub Action for teams using Codex, Claude Code, Cursor, or other AI coding agents.

It checks unified diffs for forbidden paths, secret/auth/payment keywords, workflow edits, dependency changes without lockfiles, missing PR body sections, and missing test evidence.

No external APIs. No third-party packages. No secret reading.

https://github.com/a78c7/agentgate

## LinkedIn Draft

I released AgentGate, an open-source safety gate for AI-agent generated code changes.

The idea is simple: before a Codex, Claude Code, Cursor, or other agent-generated change becomes a pull request, run a small local check against the diff.

AgentGate can block high-risk paths, secret-like keywords, workflow modifications, oversized diffs, and PR bodies that lack test evidence. It is not a replacement for human review, but it helps keep obvious risk out of the review queue.

Repo: https://github.com/a78c7/agentgate

## Reddit Draft

I built AgentGate, a small open-source CLI + GitHub Action for checking AI-agent generated diffs before they become pull requests.

It is meant for people using Codex, Claude Code, Cursor, or similar coding agents. It checks for risky paths, secret-like keywords, GitHub workflow edits, oversized diffs, dependency changes without lockfiles, and missing PR/test evidence.

It does not read secrets, cookies, keychain data, or password managers. It does not upload code or create PRs/comments automatically. It is a guardrail before human review, not a guarantee that a change is safe.

Repo: https://github.com/a78c7/agentgate

## Hacker News Draft

Show HN: AgentGate - safety-first checks for AI-generated code diffs

AgentGate is a small Python CLI and GitHub Action for checking AI-agent generated code changes before they become pull requests. It focuses on diff-based guardrails: forbidden paths, secret-like keywords, workflow changes, dependency lockfile warnings, diff size, PR body sections, and test evidence.

It uses the Python standard library, calls no external APIs, and does not read secrets.

https://github.com/a78c7/agentgate

## Safety Wording

Use cautious wording:

- "helps catch configured risk"
- "pre-PR guardrail"
- "does not replace human review"
- "does not read secrets"

Avoid overclaims:

- "makes AI code safe"
- "guarantees secure PRs"
- "prevents all leaks"
- "fully automates review"
