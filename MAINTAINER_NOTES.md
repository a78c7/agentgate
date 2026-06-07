# Maintainer Notes

These notes define the maintenance posture for AgentGate.

## Safety Boundary

AgentGate is a local-first safety gate. It should inspect diffs, config, and optional PR body text. It should not inspect private machine state.

Do not add behavior that reads:

- Cookies.
- Keychain data.
- Password managers.
- Token values.
- Secret stores.
- Private credentials.
- Environment variable values for secrets.

Do not add behavior that handles:

- Payment.
- KYC.
- Payout.
- Withdrawal.
- Tax.
- Wallets.
- Banking flows.
- GitHub Sponsors setup.

## Automation Boundary

AgentGate should not automatically:

- Create pull requests.
- Submit pull request comments.
- Approve or merge pull requests.
- Claim bounties.
- Upload repository code.
- Call external telemetry or analytics services.

If future integrations need reporting, prefer explicit local output such as Markdown, JSON, SARIF, or GitHub Step Summary content controlled by the workflow author.

## Rule Philosophy

Defaults should remain conservative:

- Blocking rules should protect high-risk paths and high-risk text.
- Warning rules should surface review work without silently passing important risk.
- New rules should be explainable from the diff.
- Config overrides should be narrow and documented.

## Dependencies

The CLI currently uses Python standard library only. Avoid third-party dependencies unless the benefit clearly outweighs the maintenance and supply-chain cost.

## Action Boundary

The composite action should keep a narrow execution path:

- Accept a diff path or run in repo mode.
- Use the checked-out repository and bundled AgentGate files.
- Avoid secrets, external APIs, and paid services.
- Keep user-provided workflow permissions under repository owner control.

## Release Guidance

Docs-only changes usually do not require a patch release. Create a new release only when users need changed behavior, changed packaged files, or a materially improved downloadable artifact.
