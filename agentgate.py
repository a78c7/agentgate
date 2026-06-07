#!/usr/bin/env python3
"""AgentGate CLI.

Safety-first checks for AI-generated diffs before they become pull requests.
The CLI uses Python standard library only, calls no external APIs, and does
not read secrets, cookies, keychain data, password managers, or tokens.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Optional


VERSION = "0.1.0"

DEFAULT_FORBIDDEN_PATHS = [
    ".env",
    ".env.*",
    ".npmrc",
    ".pypirc",
    "secrets/",
    "secret/",
    "credentials/",
    "credential/",
    "auth/",
    "oauth/",
    "payment/",
    "billing/",
    "wallet/",
    "crypto/",
    "kyc/",
    "migrations/",
    ".github/workflows/",
]

DEFAULT_FORBIDDEN_KEYWORDS = [
    "password",
    "token",
    "secret",
    "credential",
    "api_key",
    "private_key",
    "oauth",
    "auth",
    "payment",
    "billing",
    "stripe",
    "wallet",
    "crypto",
    "kyc",
    "destructive migration",
    "production database",
    "exploit",
    "rce",
    "xss",
    "csrf",
    "ssrf",
]

DEFAULT_CONFIG = {
    "max_changed_files": 12,
    "max_added_lines": 800,
    "max_deleted_lines": 400,
    "block_on_forbidden_path": True,
    "block_on_forbidden_keyword": True,
    "block_on_workflow_change": True,
    "require_tests_section": True,
    "require_pr_body_sections": True,
    "require_ai_disclosure": False,
    "warn_on_dependency_without_lockfile": True,
    "allowed_docs_only_extensions": [".md", ".mdx", ".rst", ".txt"],
    "forbidden_paths": [],
    "forbidden_keywords": [],
    "override_default_forbidden_paths": False,
    "override_default_forbidden_keywords": False,
    "fail_on_warning": False,
}

LOCKFILE_RELATIONS = {
    "package.json": ["package-lock.json", "pnpm-lock.yaml", "yarn.lock"],
    "Cargo.toml": ["Cargo.lock"],
    "go.mod": ["go.sum"],
}


@dataclass
class Finding:
    rule: str
    message: str
    evidence: str = ""


@dataclass
class DiffStats:
    changed_files: list[str]
    added_lines: int
    deleted_lines: int


@dataclass
class Report:
    result: str
    exit_code: int
    summary: dict
    blocking_findings: list[dict]
    warnings: list[dict]
    passed_checks: list[str]
    suggested_fixes: list[str]


def deep_merge_config(config_path: Optional[str]) -> dict:
    config = dict(DEFAULT_CONFIG)
    if config_path:
        user_config = json.loads(Path(config_path).read_text(encoding="utf-8"))
        config.update(user_config)
    if config.get("override_default_forbidden_paths"):
        config["_effective_forbidden_paths"] = list(config.get("forbidden_paths") or [])
    else:
        config["_effective_forbidden_paths"] = DEFAULT_FORBIDDEN_PATHS + list(config.get("forbidden_paths") or [])
    if config.get("override_default_forbidden_keywords"):
        config["_effective_forbidden_keywords"] = list(config.get("forbidden_keywords") or [])
    else:
        config["_effective_forbidden_keywords"] = DEFAULT_FORBIDDEN_KEYWORDS + list(config.get("forbidden_keywords") or [])
    return config


def normalize_path(path: str) -> str:
    path = path.strip()
    if path.startswith("a/") or path.startswith("b/"):
        path = path[2:]
    return path.strip("/")


def parse_diff(diff_text: str) -> tuple[DiffStats, dict[str, list[str]]]:
    changed_files: list[str] = []
    added_by_file: dict[str, list[str]] = {}
    current_file: Optional[str] = None
    added_lines = 0
    deleted_lines = 0

    def mark_file(path: str) -> None:
        nonlocal current_file
        if path == "/dev/null":
            return
        normalized = normalize_path(path)
        if not normalized:
            return
        current_file = normalized
        if normalized not in changed_files:
            changed_files.append(normalized)
        added_by_file.setdefault(normalized, [])

    for line in diff_text.splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            if len(parts) >= 4:
                mark_file(parts[3])
            continue
        if line.startswith("+++ "):
            mark_file(line[4:].strip())
            continue
        if line.startswith("--- "):
            continue
        if line.startswith("+") and not line.startswith("+++"):
            added_lines += 1
            if current_file:
                added_by_file.setdefault(current_file, []).append(line[1:])
        elif line.startswith("-") and not line.startswith("---"):
            deleted_lines += 1

    return DiffStats(changed_files, added_lines, deleted_lines), added_by_file


def path_matches_pattern(path: str, pattern: str) -> bool:
    path_l = normalize_path(path).lower()
    pattern_l = pattern.strip().lower().strip("/")
    if not pattern_l:
        return False
    if "*" in pattern_l and fnmatch.fnmatch(path_l, pattern_l):
        return True
    if path_l == pattern_l:
        return True
    if path_l.startswith(pattern_l + "/"):
        return True
    return f"/{pattern_l}/" in f"/{path_l}/"


def contains_keyword(text: str, keyword: str) -> bool:
    return keyword.lower() in text.lower()


def check_forbidden_paths(stats: DiffStats, config: dict) -> tuple[list[Finding], list[str]]:
    findings = []
    for path in stats.changed_files:
        for pattern in config["_effective_forbidden_paths"]:
            if path_matches_pattern(path, pattern):
                findings.append(Finding("forbidden_path", f"Changed file matches forbidden path pattern `{pattern}`.", path))
                break
    passed = [] if findings else ["Forbidden path check passed"]
    return findings, passed


def check_workflow_changes(stats: DiffStats, config: dict) -> tuple[list[Finding], list[str]]:
    findings = []
    for path in stats.changed_files:
        if path_matches_pattern(path, ".github/workflows/"):
            findings.append(Finding("workflow_modification", "GitHub Actions workflow modification detected.", path))
    passed = [] if findings else ["Workflow modification check passed"]
    return findings, passed


def check_forbidden_keywords(added_by_file: dict[str, list[str]], config: dict) -> tuple[list[Finding], list[str]]:
    findings = []
    for path, lines in added_by_file.items():
        for index, line in enumerate(lines, start=1):
            for keyword in config["_effective_forbidden_keywords"]:
                if contains_keyword(line, keyword):
                    findings.append(
                        Finding(
                            "forbidden_keyword",
                            f"Added line contains forbidden keyword `{keyword}`.",
                            f"{path}: added line {index}",
                        )
                    )
                    break
    passed = [] if findings else ["Forbidden keyword check passed"]
    return findings, passed


def check_diff_size(stats: DiffStats, config: dict) -> tuple[list[Finding], list[str]]:
    findings = []
    if len(stats.changed_files) > int(config["max_changed_files"]):
        findings.append(Finding("diff_size", "Changed file count exceeds configured limit.", str(len(stats.changed_files))))
    if stats.added_lines > int(config["max_added_lines"]):
        findings.append(Finding("diff_size", "Added line count exceeds configured limit.", str(stats.added_lines)))
    if stats.deleted_lines > int(config["max_deleted_lines"]):
        findings.append(Finding("diff_size", "Deleted line count exceeds configured limit.", str(stats.deleted_lines)))
    passed = [] if findings else ["Diff size check passed"]
    return findings, passed


def basename_set(paths: Iterable[str]) -> set[str]:
    return {Path(path).name for path in paths}


def check_dependency_lockfiles(stats: DiffStats, config: dict) -> tuple[list[Finding], list[str]]:
    if not config.get("warn_on_dependency_without_lockfile", True):
        return [], ["Dependency lockfile check skipped by config"]
    warnings = []
    names = basename_set(stats.changed_files)
    for dependency_file, lockfiles in LOCKFILE_RELATIONS.items():
        if dependency_file in names and not any(lockfile in names for lockfile in lockfiles):
            warnings.append(
                Finding(
                    "dependency_without_lockfile",
                    f"`{dependency_file}` changed without corresponding lockfile update.",
                    ", ".join(lockfiles),
                )
            )
    for dependency_file in ("pyproject.toml", "requirements.txt"):
        if dependency_file in names:
            warnings.append(
                Finding(
                    "python_dependency_review",
                    f"`{dependency_file}` changed. Review dependency impact and lock strategy manually.",
                    dependency_file,
                )
            )
    passed = [] if warnings else ["Dependency lockfile check passed"]
    return warnings, passed


def read_pr_body(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    return Path(path).read_text(encoding="utf-8")


def check_pr_body(pr_body: Optional[str], config: dict) -> tuple[list[Finding], list[Finding], list[str]]:
    blocking = []
    warnings = []
    passed = []
    if pr_body is None:
        passed.append("PR body checks skipped because --pr-body was not provided")
        return blocking, warnings, passed

    body_l = pr_body.lower()
    missing_sections = [section for section in ("summary", "changes", "tests", "risk") if section not in body_l]
    if missing_sections and config.get("require_pr_body_sections", True):
        blocking.append(Finding("pr_body_sections", "PR body is missing required sections.", ", ".join(missing_sections)))
    elif missing_sections:
        warnings.append(Finding("pr_body_sections", "PR body is missing recommended sections.", ", ".join(missing_sections)))
    else:
        passed.append("PR body required section check passed")

    test_terms = ("tests", "test command", "result")
    outcome_terms = ("passed", "failed")
    has_test_evidence = all(term in body_l for term in test_terms) and any(term in body_l for term in outcome_terms)
    if not has_test_evidence and config.get("require_tests_section", True):
        blocking.append(Finding("test_evidence", "PR body lacks explicit test command, result, and pass/fail evidence."))
    elif not has_test_evidence:
        warnings.append(Finding("test_evidence", "PR body lacks explicit test evidence."))
    else:
        passed.append("Test evidence check passed")

    ai_terms = ("ai-assisted", "codex", "claude", "generated with ai")
    has_ai_disclosure = any(term in body_l for term in ai_terms)
    if not has_ai_disclosure and config.get("require_ai_disclosure"):
        blocking.append(Finding("ai_disclosure", "PR body lacks required AI assistance disclosure."))
    elif not has_ai_disclosure:
        warnings.append(Finding("ai_disclosure", "PR body does not disclose AI assistance."))
    else:
        passed.append("AI disclosure check passed")

    return blocking, warnings, passed


def get_repo_diff(repo_path: str) -> str:
    repo = Path(repo_path)
    if not repo.exists():
        raise FileNotFoundError(f"Repository path does not exist: {repo_path}")
    cached = subprocess.run(["git", "-C", str(repo), "diff", "--cached"], capture_output=True, text=True, check=False)
    if cached.returncode != 0:
        raise RuntimeError(cached.stderr.strip() or "git diff --cached failed")
    if cached.stdout.strip():
        return cached.stdout
    unstaged = subprocess.run(["git", "-C", str(repo), "diff"], capture_output=True, text=True, check=False)
    if unstaged.returncode != 0:
        raise RuntimeError(unstaged.stderr.strip() or "git diff failed")
    return unstaged.stdout


def load_diff(args: argparse.Namespace) -> str:
    if args.diff:
        return Path(args.diff).read_text(encoding="utf-8")
    if args.repo:
        return get_repo_diff(args.repo)
    raise ValueError("Provide --diff or --repo.")


def make_report(diff_text: str, config: dict, pr_body: Optional[str]) -> Report:
    stats, added_by_file = parse_diff(diff_text)
    blocking_findings: list[Finding] = []
    warnings: list[Finding] = []
    passed_checks: list[str] = []

    size_blocking, size_passed = check_diff_size(stats, config)
    blocking_findings.extend(size_blocking)
    passed_checks.extend(size_passed)

    path_findings, path_passed = check_forbidden_paths(stats, config)
    if config.get("block_on_forbidden_path", True):
        blocking_findings.extend(path_findings)
    else:
        warnings.extend(path_findings)
    passed_checks.extend(path_passed)

    workflow_findings, workflow_passed = check_workflow_changes(stats, config)
    if config.get("block_on_workflow_change", True):
        blocking_findings.extend(workflow_findings)
    else:
        warnings.extend(workflow_findings)
    passed_checks.extend(workflow_passed)

    keyword_findings, keyword_passed = check_forbidden_keywords(added_by_file, config)
    if config.get("block_on_forbidden_keyword", True):
        blocking_findings.extend(keyword_findings)
    else:
        warnings.extend(keyword_findings)
    passed_checks.extend(keyword_passed)

    dependency_warnings, dependency_passed = check_dependency_lockfiles(stats, config)
    warnings.extend(dependency_warnings)
    passed_checks.extend(dependency_passed)

    pr_blocking, pr_warnings, pr_passed = check_pr_body(pr_body, config)
    blocking_findings.extend(pr_blocking)
    warnings.extend(pr_warnings)
    passed_checks.extend(pr_passed)

    if warnings and config.get("fail_on_warning", False):
        blocking_findings.extend(warnings)
        warnings = []

    if blocking_findings:
        result = "blocked"
        exit_code = 2
    elif warnings:
        result = "warning"
        exit_code = 1
    else:
        result = "pass"
        exit_code = 0

    summary = {
        "changed_files": len(stats.changed_files),
        "changed_file_paths": stats.changed_files,
        "added_lines": stats.added_lines,
        "deleted_lines": stats.deleted_lines,
        "checks_run": len(passed_checks) + len(blocking_findings) + len(warnings),
    }
    suggested_fixes = suggest_fixes(blocking_findings, warnings)
    return Report(
        result=result,
        exit_code=exit_code,
        summary=summary,
        blocking_findings=[asdict(item) for item in blocking_findings],
        warnings=[asdict(item) for item in warnings],
        passed_checks=passed_checks,
        suggested_fixes=suggested_fixes,
    )


def suggest_fixes(blocking: list[Finding], warnings: list[Finding]) -> list[str]:
    suggestions = []
    rules = {item.rule for item in blocking + warnings}
    if "forbidden_path" in rules:
        suggestions.append("Move sensitive or high-risk changes out of this PR, or request explicit human review.")
    if "forbidden_keyword" in rules:
        suggestions.append("Remove secrets, credentials, auth/payment/security terms, or explain why the change is safe.")
    if "workflow_modification" in rules:
        suggestions.append("Avoid changing GitHub Actions workflows in AI-generated PRs unless explicitly approved.")
    if "diff_size" in rules:
        suggestions.append("Split the change into smaller, reviewable PRs.")
    if "test_evidence" in rules:
        suggestions.append("Add test commands and pass/fail results to the PR body.")
    if "pr_body_sections" in rules:
        suggestions.append("Add Summary, Changes, Tests, and Risk sections to the PR body.")
    if "dependency_without_lockfile" in rules or "python_dependency_review" in rules:
        suggestions.append("Update lockfiles where applicable and document dependency risk.")
    if "ai_disclosure" in rules:
        suggestions.append("Disclose AI assistance when required by project policy.")
    return suggestions or ["No fixes needed."]


def markdown_report(report: Report) -> str:
    result_label = report.result.upper()

    def findings(items: list[dict]) -> str:
        if not items:
            return "- none"
        lines = []
        for item in items:
            evidence = f" Evidence: `{item['evidence']}`." if item.get("evidence") else ""
            lines.append(f"- `{item['rule']}`: {item['message']}{evidence}")
        return "\n".join(lines)

    return "\n".join(
        [
            "# AgentGate Report",
            "",
            "## Result",
            "",
            f"- {result_label}",
            f"- Exit code: {report.exit_code}",
            "",
            "## Summary",
            "",
            f"- changed files: {report.summary['changed_files']}",
            f"- added lines: {report.summary['added_lines']}",
            f"- deleted lines: {report.summary['deleted_lines']}",
            f"- checks run: {report.summary['checks_run']}",
            "",
            "## Blocking Findings",
            "",
            findings(report.blocking_findings),
            "",
            "## Warnings",
            "",
            findings(report.warnings),
            "",
            "## Passed Checks",
            "",
            "\n".join(f"- {item}" for item in report.passed_checks) if report.passed_checks else "- none",
            "",
            "## Suggested Fixes",
            "",
            "\n".join(f"- {item}" for item in report.suggested_fixes),
            "",
        ]
    )


def json_report(report: Report) -> str:
    payload = {
        "result": report.result,
        "exit_code": report.exit_code,
        "summary": report.summary,
        "blocking_findings": report.blocking_findings,
        "warnings": report.warnings,
        "passed_checks": report.passed_checks,
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def run_check(args: argparse.Namespace) -> int:
    config = deep_merge_config(args.config)
    if args.fail_on_warning:
        config["fail_on_warning"] = True
    diff_text = load_diff(args)
    pr_body = read_pr_body(args.pr_body)
    report = make_report(diff_text, config, pr_body)
    output = json_report(report) if args.format == "json" else markdown_report(report)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)
    return report.exit_code


def run_init_config(args: argparse.Namespace) -> int:
    output = json.dumps(DEFAULT_CONFIG, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AgentGate safety checks for AI-generated code changes.")
    parser.add_argument("--version", action="version", version=f"AgentGate {VERSION}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="Check a diff file or repository diff.")
    source = check.add_mutually_exclusive_group(required=True)
    source.add_argument("--diff", help="Unified diff file to check.")
    source.add_argument("--repo", help="Repository path. Uses git diff --cached, then git diff.")
    check.add_argument("--config", help="JSON config path.")
    check.add_argument("--pr-body", help="PR body Markdown file to validate.")
    check.add_argument("--format", choices=["markdown", "json"], default="markdown")
    check.add_argument("--output", help="Write report to path.")
    check.add_argument("--fail-on-warning", action="store_true", help="Treat warnings as blocked.")
    check.set_defaults(func=run_check)

    init_config = subparsers.add_parser("init-config", help="Print or write default configuration.")
    init_config.add_argument("--output", help="Write config to path instead of stdout.")
    init_config.set_defaults(func=run_init_config)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"agentgate: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
