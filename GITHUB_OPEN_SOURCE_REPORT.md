# GitHub Open Source Report

## Timestamp

2026-06-07 16:29:15 CST

## Repository

```text
https://github.com/a78c7/agentgate
```

- Repository: `a78c7/agentgate`
- Visibility: public
- Default branch: `main`

## Release

```text
https://github.com/a78c7/agentgate/releases/tag/v0.1.0
```

- Tag: `v0.1.0`
- Title: `AgentGate v0.1.0`
- Draft: no
- Prerelease: no

## Commit

```text
dd9ccb80015161253cc20d5e003062f6ce31e4e2
```

## Release Asset

```text
agentgate-0.1.0.zip
```

Download URL:

```text
https://github.com/a78c7/agentgate/releases/download/v0.1.0/agentgate-0.1.0.zip
```

Asset metadata:

- Content type: `application/zip`
- Size: `26548`
- SHA-256 digest: `1b59a659b08937a5f8ab66a784baaab87c529d13793a6b333485ef94591b5492`
- State: `uploaded`

## Tests

Status: pass

```text
Ran 9 tests
OK
```

## CLI Verification

Verified:

- Safe diff passes with exit code `0`.
- Unsafe secret diff blocks with exit code `2`.
- Unsafe auth diff blocks with exit code `2`.
- Dependency change without lockfile warns with exit code `1`.
- Repo mode passes on a clean checkout.
- `init-config` outputs valid JSON.

## Package

Status: pass

```text
dist/agentgate-0.1.0.zip
```

The ZIP was uploaded as a GitHub Release asset and was not committed to git.

## Security Scan

Safety scan result:

```text
./examples/unsafe-secret-diff.patch
```

This is a non-sensitive placeholder example required by the project. It contains `replace-me` values only and no real secrets, tokens, cookies, credentials, keychain data, or state files.

ZIP sensitive path scan: pass.

## Boundaries Confirmed

- No `codex-bounty-hunter` modifications.
- No `bountylens` modifications.
- No KYC/payment/withdrawal handling.
- No GitHub Sponsors setup.
- No paid services.
- No cookie/keychain/password manager reads.
- No secrets or tokens written to project files.

## Next Steps

Manual follow-up:

1. Open the repo page and confirm README rendering.
2. Download the release ZIP and confirm it opens.
3. Check the Actions tab after GitHub runs the first workflow.
4. Optionally add a social preview image.
5. Optionally enable Discussions.
6. Do not enable GitHub Sponsors unless the user later handles all payout/KYC/tax requirements manually.
