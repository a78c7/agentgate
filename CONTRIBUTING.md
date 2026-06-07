# Contributing

AgentGate is safety-first. Contributions must preserve the local-only, no-credentials, no-payment model.

## Run Tests

```bash
python3 -m unittest discover -s tests
```

## Test The CLI

```bash
python3 agentgate.py check --diff examples/safe-diff.patch --config agentgate.config.example.json
python3 agentgate.py check --diff examples/unsafe-secret-diff.patch --config agentgate.config.example.json
```

## Package

```bash
bash package-release.sh
```

## Do Not Add

- Telemetry.
- External API calls.
- Cookie access.
- Token reading.
- Keychain access.
- Password manager access.
- Payment, KYC, payout, withdrawal, wallet, tax, or banking flows.
- Automatic GitHub comments.
- Automatic PR creation.
- GitHub Sponsors setup.

## Before Large Changes

Open an issue before large changes, especially if the change affects:

- Rule severity.
- GitHub Action behavior.
- Config semantics.
- Network behavior.
- Security boundaries.
