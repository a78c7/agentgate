#!/usr/bin/env bash
set -euo pipefail

VERSION="0.1.0"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ZIP_PATH="$ROOT_DIR/dist/agentgate-$VERSION.zip"

cd "$ROOT_DIR"
mkdir -p dist
rm -f "$ZIP_PATH"

required_files=(
  "README.md"
  "QUICKSTART.md"
  "CHANGELOG.md"
  "LICENSE"
  "PRODUCT_REPORT.md"
  "OPEN_SOURCE_READY_REPORT.md"
  "POST_RELEASE_POLISH_REPORT.md"
  "SECURITY.md"
  "CONTRIBUTING.md"
  "CODE_OF_CONDUCT.md"
  "action.yml"
  "assets/agentgate-flow.svg"
  "assets/cli-demo.svg"
  "agentgate.py"
  "agentgate.config.example.json"
  "pyproject.toml"
  "package-release.sh"
  ".gitignore"
  ".github/workflows/test.yml"
  ".github/ISSUE_TEMPLATE/bug_report.md"
  ".github/ISSUE_TEMPLATE/feature_request.md"
  ".github/ISSUE_TEMPLATE/safety_rule.md"
  ".github/PULL_REQUEST_TEMPLATE.md"
  "docs/safety-model.md"
  "docs/config-reference.md"
  "docs/github-action-usage.md"
  "docs/ai-agent-workflow.md"
  "docs/examples.md"
  "docs/demo-assets.md"
  "docs/repo-topics.md"
  "docs/social-announcement.md"
  "examples/safe-diff.patch"
  "examples/unsafe-auth-diff.patch"
  "examples/unsafe-secret-diff.patch"
  "examples/missing-tests-diff.patch"
  "examples/package-no-lock-diff.patch"
  "examples/sample-pr-body.md"
  "examples/sample-report.md"
  "examples/sample-agentgate.config.json"
  "examples/sample-github-action.yml"
  "examples/sample-agent-prompt.md"
  "tests/test_agentgate.py"
)

for file in "${required_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "Missing required file: $file" >&2
    exit 1
  fi
done

python3 -m unittest discover -s tests

zip -r "$ZIP_PATH" \
  README.md \
  QUICKSTART.md \
  CHANGELOG.md \
  LICENSE \
  PRODUCT_REPORT.md \
  OPEN_SOURCE_READY_REPORT.md \
  POST_RELEASE_POLISH_REPORT.md \
  SECURITY.md \
  CONTRIBUTING.md \
  CODE_OF_CONDUCT.md \
  action.yml \
  assets \
  agentgate.py \
  agentgate.config.example.json \
  pyproject.toml \
  package-release.sh \
  .gitignore \
  .github \
  docs \
  examples \
  tests \
  -x "*/.git/*" \
  -x "*/node_modules/*" \
  -x "*secrets*" \
  -x "*cookies*" \
  -x "*keychain*" \
  -x "*tokens*" \
  -x "*state.json" \
  -x "*codex-bounty-hunter*" \
  -x "*.DS_Store" \
  -x "dist/unpacked/*"

if unzip -l "$ZIP_PATH" | grep -Eiq '(^|/)(\.git|node_modules)(/|$)|secrets|cookies|keychain|tokens|state\.json|codex-bounty-hunter|\.env'; then
  echo "Sensitive or excluded path found in zip listing." >&2
  exit 1
fi

echo "Created $ZIP_PATH"
