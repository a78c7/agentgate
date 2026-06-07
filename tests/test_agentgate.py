import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "agentgate.py"
CONFIG = ROOT / "agentgate.config.example.json"

spec = importlib.util.spec_from_file_location("agentgate", CLI)
agentgate = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = agentgate
spec.loader.exec_module(agentgate)


class AgentGateTest(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_safe_diff_passes(self):
        result = self.run_cli("check", "--diff", "examples/safe-diff.patch", "--config", str(CONFIG), "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["result"], "pass")

    def test_unsafe_secret_blocks(self):
        result = self.run_cli("check", "--diff", "examples/unsafe-secret-diff.patch", "--config", str(CONFIG), "--format", "json")
        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["result"], "blocked")
        self.assertTrue(any(item["rule"] == "forbidden_path" for item in payload["blocking_findings"]))
        self.assertTrue(any(item["rule"] == "forbidden_keyword" for item in payload["blocking_findings"]))

    def test_unsafe_auth_blocks(self):
        result = self.run_cli("check", "--diff", "examples/unsafe-auth-diff.patch", "--config", str(CONFIG), "--format", "json")
        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertTrue(any(item["rule"] == "forbidden_path" for item in payload["blocking_findings"]))

    def test_dependency_without_lockfile_warns(self):
        result = self.run_cli("check", "--diff", "examples/package-no-lock-diff.patch", "--config", str(CONFIG), "--format", "json")
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["result"], "warning")
        self.assertTrue(any(item["rule"] == "dependency_without_lockfile" for item in payload["warnings"]))

    def test_pr_body_missing_sections_blocks(self):
        temp_body = ROOT / "examples" / "tmp-pr-body-missing-tests.md"
        temp_body.write_text("# Summary\n\nSmall change.\n", encoding="utf-8")
        try:
            result = self.run_cli(
                "check",
                "--diff",
                "examples/missing-tests-diff.patch",
                "--config",
                str(CONFIG),
                "--pr-body",
                str(temp_body),
                "--format",
                "json",
            )
        finally:
            temp_body.unlink(missing_ok=True)
        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertTrue(any(item["rule"] == "test_evidence" for item in payload["blocking_findings"]))

    def test_pr_body_sample_passes_with_safe_diff(self):
        result = self.run_cli(
            "check",
            "--diff",
            "examples/safe-diff.patch",
            "--config",
            str(CONFIG),
            "--pr-body",
            "examples/sample-pr-body.md",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_markdown_output_file(self):
        output = ROOT / "examples" / "sample-report.md"
        result = self.run_cli("check", "--diff", "examples/safe-diff.patch", "--config", str(CONFIG), "--output", str(output))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# AgentGate Report", output.read_text(encoding="utf-8"))

    def test_init_config_outputs_json(self):
        result = self.run_cli("init-config")
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["max_changed_files"], 12)

    def test_fail_on_warning_blocks(self):
        result = self.run_cli(
            "check",
            "--diff",
            "examples/package-no-lock-diff.patch",
            "--config",
            str(CONFIG),
            "--format",
            "json",
            "--fail-on-warning",
        )
        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["result"], "blocked")


if __name__ == "__main__":
    unittest.main()
