import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_integrations.py"


class CheckIntegrationsTests(unittest.TestCase):
    def make_project(self, root, runtime=None, providers=None, requirements=None):
        studio = root / "studio"
        studio.mkdir()
        data = {
            "schema_version": 1,
            "runtime": runtime or {
                "provider": "claude-code",
                "auth_mode": "subscription-login",
                "status": "verified",
                "secret_env": [],
            },
            "providers": providers or [],
            "task_requirements": requirements or {},
        }
        (studio / "integrations.json").write_text(json.dumps(data), encoding="utf-8")

    def run_check(self, root, task="model-inference", env=None):
        clean_env = os.environ.copy()
        clean_env.pop("CODEX_API_KEY", None)
        clean_env.pop("SCENARIO_API_KEY", None)
        if env:
            clean_env.update(env)
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--project-dir", str(root), "--task", task],
            text=True,
            capture_output=True,
            env=clean_env,
        )

    def test_pending_runtime_blocks_model_inference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_project(root, runtime={"provider": "", "auth_mode": "", "status": "pending", "secret_env": []})
            result = self.run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("PRE-FLIGHT BLOQUEADO", result.stdout)

    def test_verified_oauth_runtime_needs_no_api_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_project(root)
            result = self.run_check(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("runtime central", result.stdout)

    def test_required_api_env_must_exist_without_printing_its_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_project(
                root,
                runtime={"provider": "codex-cli", "auth_mode": "api-key", "status": "verified", "secret_env": ["CODEX_API_KEY"]},
            )
            result = self.run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("CODEX_API_KEY ausente", result.stdout)
            self.assertNotIn("secret-value", result.stdout)

    def test_missing_conditional_provider_does_not_block_unrelated_inference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_project(
                root,
                providers=[{"id": "scenario", "auth_mode": "api-key", "status": "not_configured", "secret_env": ["SCENARIO_API_KEY"]}],
                requirements={"concept_art": ["scenario"]},
            )
            inference = self.run_check(root, "model-inference")
            concept = self.run_check(root, "concept_art")
            self.assertEqual(inference.returncode, 0, inference.stdout + inference.stderr)
            self.assertEqual(concept.returncode, 1)
            self.assertIn("provider scenario", concept.stdout)

    def test_local_docs_can_pass_without_model_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_project(root, runtime={"provider": "", "auth_mode": "", "status": "pending", "secret_env": []})
            result = self.run_check(root, "local-docs")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unknown_task_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_project(root)
            result = self.run_check(root, "not-a-real-task")
            self.assertEqual(result.returncode, 2)
            self.assertIn("capacidade desconhecida", result.stdout)

    def test_invalid_status_content_is_redacted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_project(
                root,
                runtime={"provider": "claude-code", "auth_mode": "login", "status": "secret-value-must-not-leak", "secret_env": []},
            )
            result = self.run_check(root)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("secret-value-must-not-leak", result.stdout)


if __name__ == "__main__":
    unittest.main()
