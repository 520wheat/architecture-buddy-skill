#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path


OVERVIEW_FILENAME = "detailed-design-overview.md"
FEEDBACK_FILENAME = "architecture-feedback.md"
MODULES_DIRNAME = "modules"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize a detailed-design workspace from bundled templates."
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output directory for the generated overview, modules/, and feedback files.",
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Design name written into the generated overview template.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite generated files when the target workspace already exists.",
    )
    return parser.parse_args(argv)


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_template(name: str) -> str:
    return (skill_root() / "templates" / name).read_text(encoding="utf-8")


def render_overview(template: str, design_name: str) -> str:
    return template.replace("- 项目：", f"- 项目：{design_name}", 1)


def target_paths(output_dir: Path) -> list[Path]:
    return [
        output_dir / OVERVIEW_FILENAME,
        output_dir / MODULES_DIRNAME,
        output_dir / FEEDBACK_FILENAME,
    ]


def existing_targets(output_dir: Path) -> list[Path]:
    return [path for path in target_paths(output_dir) if path.exists()]


def validate_target_types(output_dir: Path) -> None:
    overview_path = output_dir / OVERVIEW_FILENAME
    feedback_path = output_dir / FEEDBACK_FILENAME
    modules_path = output_dir / MODULES_DIRNAME

    invalid_file_targets = [
        path for path in (overview_path, feedback_path) if path.exists() and path.is_dir()
    ]
    if invalid_file_targets:
        joined = ", ".join(str(path) for path in invalid_file_targets)
        raise ValueError(f"refusing to overwrite directory targets: {joined}")

    if modules_path.exists() and not modules_path.is_dir():
        raise ValueError(f"refusing to treat non-directory path as modules target: {modules_path}")


def initialize_workspace(output_dir: Path, design_name: str, force: bool) -> None:
    existing = existing_targets(output_dir)
    if existing and not force:
        joined = ", ".join(str(path) for path in existing)
        raise FileExistsError(
            f"target files already exist; rerun with --force to overwrite: {joined}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    validate_target_types(output_dir)

    overview_path = output_dir / OVERVIEW_FILENAME
    feedback_path = output_dir / FEEDBACK_FILENAME
    modules_path = output_dir / MODULES_DIRNAME

    overview_path.write_text(
        render_overview(load_template("detailed-design-overview.md"), design_name),
        encoding="utf-8",
    )
    feedback_path.write_text(
        load_template("architecture-feedback.md"),
        encoding="utf-8",
    )
    modules_path.mkdir(parents=True, exist_ok=True)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    output_dir = Path(args.output).expanduser()

    try:
        initialize_workspace(output_dir, args.name, args.force)
    except (FileExistsError, ValueError, OSError) as err:
        print(f"初始化失败：{err}", file=sys.stderr)
        return 1

    print(f"Initialized detailed-design workspace at {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
