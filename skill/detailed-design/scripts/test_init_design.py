import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().with_name("init-design.py")


class InitDesignCLITest(unittest.TestCase):
    def run_init_design(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_initializes_design_workspace_for_unicode_and_space_safe_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "设计 空间"

            result = self.run_init_design(
                "--output",
                str(output_dir),
                "--name",
                "SRE Buddy 设计",
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue((output_dir / "detailed-design-overview.md").is_file())
            self.assertTrue((output_dir / "architecture-feedback.md").is_file())
            self.assertTrue((output_dir / "modules").is_dir())
            self.assertIn("- 项目：SRE Buddy 设计", (output_dir / "detailed-design-overview.md").read_text())

    def test_refuses_to_overwrite_existing_workspace_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "design"

            first_result = self.run_init_design(
                "--output",
                str(output_dir),
                "--name",
                "SRE Buddy",
            )
            self.assertEqual(first_result.returncode, 0, msg=first_result.stderr)

            overview_path = output_dir / "detailed-design-overview.md"
            original_content = overview_path.read_text()
            overview_path.write_text("sentinel\n")

            second_result = self.run_init_design(
                "--output",
                str(output_dir),
                "--name",
                "SRE Buddy",
            )

            self.assertNotEqual(second_result.returncode, 0)
            self.assertIn("already exist", second_result.stderr.lower())
            self.assertEqual(overview_path.read_text(), "sentinel\n")
            self.assertNotEqual(overview_path.read_text(), original_content)


if __name__ == "__main__":
    unittest.main()
