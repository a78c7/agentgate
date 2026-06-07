# Security Policy

AgentGate checks AI-generated diffs before they become pull requests.

## Safety Model

AgentGate does not:

- Read cookies.
- Read keychain data.
- Read password managers.
- Read private credentials.
- Read environment variable tokens.
- Upload code.
- Call external APIs.
- Handle KYC, payment, payout, withdrawal, wallet, tax, or banking flows.
- Automatically comment on PRs.
- Automatically create PRs.
- Enable GitHub Sponsors.

## Reporting Vulnerabilities

Report vulnerabilities through GitHub issues or GitHub security advisories if available.

Include:

- Description.
- Steps to reproduce.
- Expected behavior.
- Actual behavior.
- Whether the issue affects safety boundaries.

Do not include exploit payloads, credential theft instructions, payment abuse flows, KYC bypass instructions, or real secrets.
