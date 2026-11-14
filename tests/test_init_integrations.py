import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "init_integrations.py"


class InitIntegrationsTests(unittest.TestCase):
    def run_script(self, project_dir):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--project-dir", str(project_dir)],
            text=True,
            capture_output=True,
        )

    def test_adds_checklist_to_existing_studio_without_touching_other_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "game"
            studio = root / "studio"
            studio.mkdir(parents=True)
            project = studio / "PROJECT.md"
            project.write_text("keep this", encoding="utf-8")
            result = self.run_script(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(project.read_text(encoding="utf-8"), "keep this")
            self.assertTrue((studio / "AI_INTEGRATIONS.md").is_file())
            manifest = json.loads((studio / "integrations.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema_version"], 1)

    def test_preserves_existing_checklist_and_adds_missing_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "game"
            studio = root / "studio"
            studio.mkdir(parents=True)
            checklist = studio / "AI_INTEGRATIONS.md"
            checklist.write_text("keep this", encoding="utf-8")
            result = self.run_script(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(checklist.read_text(encoding="utf-8"), "keep this")
            manifest = json.loads((studio / "integrations.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema_version"], 1)

    def test_leaves_both_existing_integration_files_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "game"
            studio = root / "studio"
            studio.mkdir(parents=True)
            checklist = studio / "AI_INTEGRATIONS.md"
            manifest = studio / "integrations.json"
            checklist.write_text("keep checklist", encoding="utf-8")
            manifest.write_text('{"custom": true}', encoding="utf-8")
            result = self.run_script(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(checklist.read_text(encoding="utf-8"), "keep checklist")
            self.assertEqual(manifest.read_text(encoding="utf-8"), '{"custom": true}')

    def test_refuses_missing_project_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "missing"
            result = self.run_script(root)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(root.exists())


if __name__ == "__main__":
    unittest.main()
