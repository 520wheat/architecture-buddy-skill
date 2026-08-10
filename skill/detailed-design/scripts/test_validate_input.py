import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().with_name("validate-input.py")


def write_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def minimal_architecture(
    *,
    state: str = "design-ready",
    scene: str = "pre-development",
    boundary: str = "边界：清晰",
    confirmed_boundaries: str = "明确输入输出边界",
    adr_ref: str = "ADR-1.md",
    pending_fact_block: str = (
        "| PF-1 | 待确认输入 | 临时默认 | 原因 | 验证条件 | 回退路径 | 重新打开条件 |"
    ),
) -> str:
    return f"""# 架构输入

- 场景：{scene}
- 状态：{state}
- 架构边界：{boundary}
- ADR：{adr_ref}
- scope：服务初始化
- confirmed boundaries：{confirmed_boundaries}
- quality targets：可校验、可回退
- non-goals：不做代码生成

## 待确认事实

| 编号 | 事实 | 单阶段默认值 | 默认原因 | 验证条件 | 回退路径 | 重新打开条件 |
| --- | --- | --- | --- | --- | --- | --- |
{pending_fact_block}
"""


def minimal_handoff(*, missing: str = "") -> str:
    fields = [
        "- architecture file",
        "- ADR paths",
        "- `pre-development`",
        "- `design-ready`",
        "- scope",
        "- confirmed boundaries",
        "- quality targets",
        "- pending facts",
        "- non-goals",
    ]
    if missing:
        fields = [field for field in fields if missing not in field]
    return (
        "# Architecture Handoff Contract\n\n"
        "## Required fields\n\n"
        + "\n".join(fields)
        + "\n"
        "\n## Pending facts\n\n"
        "| 事实 | 单阶段默认值 | 默认原因 | 验证条件 | 回退路径 | 重新打开条件 |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| 待确认输入 | 临时默认 | 原因 | 验证条件 | 回退路径 | 重新打开条件 |\n"
    )


class ValidateInputCLITest(unittest.TestCase):
    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_help_exists(self) -> None:
        result = self.run_validator("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage:", result.stdout.lower())

    def test_accepts_valid_design_ready_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            arch = root / "architecture.md"
            adr = root / "ADR-1.md"
            write_file(adr, "# ADR\n")
            write_file(arch, minimal_architecture())

            result = self.run_validator(str(arch), "--adr", str(adr))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("输入校验通过", result.stdout)

    def test_rejects_draft_scene(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            arch = root / "architecture.md"
            adr = root / "ADR-1.md"
            write_file(adr, "# ADR\n")
            write_file(arch, minimal_architecture(scene="reference"))

            result = self.run_validator(str(arch), "--adr", str(adr))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("输入校验失败：", result.stderr)
            self.assertIn("pre-development", result.stderr)

    def test_rejects_blocked_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            arch = root / "architecture.md"
            adr = root / "ADR-1.md"
            write_file(adr, "# ADR\n")
            write_file(arch, minimal_architecture(state="blocked"))

            result = self.run_validator(str(arch), "--adr", str(adr))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("design-ready", result.stderr)

    def test_rejects_missing_boundary_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            arch = root / "architecture.md"
            adr = root / "ADR-1.md"
            write_file(adr, "# ADR\n")
            write_file(arch, minimal_architecture(boundary="", confirmed_boundaries=""))

            result = self.run_validator(str(arch), "--adr", str(adr))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("架构边界", result.stderr)

    def test_rejects_missing_adr(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            arch = root / "architecture.md"
            write_file(arch, minimal_architecture())

            result = self.run_validator(str(arch))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--adr", result.stderr)

    def test_rejects_unreadable_adr(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            arch = root / "architecture.md"
            adr = root / "missing.md"
            write_file(arch, minimal_architecture())

            result = self.run_validator(str(arch), "--adr", str(adr))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ADR", result.stderr)

    def test_rejects_missing_handoff_field_when_handoff_present(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            arch = root / "architecture.md"
            adr = root / "ADR-1.md"
            handoff = root / "architecture-handoff.md"
            write_file(adr, "# ADR\n")
            write_file(handoff, minimal_handoff(missing="quality targets"))
            write_file(
                arch,
                minimal_architecture() + f"\n## Handoff\n\n{handoff.name}\n",
            )

            result = self.run_validator(str(arch), "--adr", str(adr))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("quality targets", result.stderr)

    def test_rejects_missing_pending_fact_default_reason_validation_roll_back_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            arch = root / "architecture.md"
            adr = root / "ADR-1.md"
            write_file(adr, "# ADR\n")
            write_file(
                arch,
                minimal_architecture(
                    pending_fact_block=(
                        "| PF-1 | 待确认输入 |  |  | 验证条件 | 回退路径 | 重新打开条件 |"
                    )
                ),
            )

            result = self.run_validator(str(arch), "--adr", str(adr))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("默认值", result.stderr)


if __name__ == "__main__":
    unittest.main()
