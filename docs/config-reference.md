# Config Reference

Default config lives in:

```text
agentgate.config.example.json
```

## Limits

- `max_changed_files`: maximum changed file count.
- `max_added_lines`: maximum added lines.
- `max_deleted_lines`: maximum deleted lines.

## Blocking Flags

- `block_on_forbidden_path`
- `block_on_forbidden_keyword`
- `block_on_workflow_change`

## PR Body Flags

- `require_tests_section`
- `require_pr_body_sections`
- `require_ai_disclosure`

`require_ai_disclosure` defaults to `false`; missing disclosure is a warning by default.

## Dependency Rules

- `warn_on_dependency_without_lockfile`

Package manager lockfile checks:

- `package.json` -> `package-lock.json`, `pnpm-lock.yaml`, or `yarn.lock`
- `Cargo.toml` -> `Cargo.lock`
- `go.mod` -> `go.sum`
- `pyproject.toml` and `requirements.txt` -> warning only

## Custom Forbidden Rules

Custom rules append to defaults:

- `forbidden_paths`
- `forbidden_keywords`

To replace defaults:

- `override_default_forbidden_paths: true`
- `override_default_forbidden_keywords: true`

Use overrides carefully. Defaults are intentionally conservative.
