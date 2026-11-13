import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "init_project.py"
INSTALLER = Path(__file__).resolve().parents[1] / "scripts" / "install_skill.py"


class InitProjectTests(unittest.TestCase):
    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True)

    def test_creates_docs_in_existing_empty_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "game"
            root.mkdir()
            result = self.run_script("--project-dir", str(root), "--name", "Sample Game")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "studio" / "PROJECT.md").is_file())
            self.assertTrue((root / "studio" / "TASKS.md").is_file())

    def test_refuses_existing_studio_without_modifying_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "game"
            (root / "studio").mkdir(parents=True)
            existing = root / "studio" / "PROJECT.md"
            existing.write_text("keep this", encoding="utf-8")
            result = self.run_script("--project-dir", str(root), "--name", "Sample Game")
            self.assertEqual(result.returncode, 3)
            self.assertEqual(existing.read_text(encoding="utf-8"), "keep this")

    def test_refuses_nonexistent_project_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "missing"
            result = self.run_script("--project-dir", str(root), "--name", "Sample Game")
            self.assertEqual(result.returncode, 2)
            self.assertFalse(root.exists())

    def test_installs_codex_skill_to_native_project_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "game"
            root.mkdir()
            result = subprocess.run(
                [sys.executable, str(INSTALLER), "--target", "codex", "--project-dir", str(root)],
                text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / ".agents/skills/game-studio-ai/SKILL.md").is_file())

    def test_installs_opencode_skill_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "game"
            root.mkdir()
            command = [sys.executable, str(INSTALLER), "--target", "opencode", "--project-dir", str(root)]
            result = subprocess.run(command, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            skill_file = root / ".opencode/skills/game-studio-ai/SKILL.md"
            self.assertTrue(skill_file.is_file())
            before = skill_file.read_text(encoding="utf-8")
            second = subprocess.run(command, text=True, capture_output=True)
            self.assertEqual(second.returncode, 4)
            self.assertEqual(skill_file.read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main()
