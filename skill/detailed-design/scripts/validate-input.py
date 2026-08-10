#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from validator_helpers import (
    extract_field,
    markdown_files_referenced,
    non_empty,
    parse_tables,
    read_text,
    section_body,
)


REQUIRED_HANOFF_PHRASES = [
    "architecture file",
    "ADR paths",
    "pre-development",
    "design-ready",
    "scope",
    "confirmed boundaries",
    "quality targets",
    "pending facts",
    "non-goals",
]

PENDING_HEADERS = [
    "事实",
    "单阶段默认值",
    "默认原因",
    "验证条件",
    "回退路径",
    "重新打开条件",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="校验详细设计输入契约。")
    parser.add_argument("architecture", help="架构 Markdown 文件")
    parser.add_argument(
        "--adr",
        action="append",
        dest="adrs",
        default=[],
        metavar="PATH",
        help="ADR 文件路径，可重复出现。",
    )
    return parser


def resolve_path(path: str, base_dir: Path) -> Path:
    candidate = Path(path).expanduser()
    if candidate.is_absolute():
        return candidate
    if (base_dir / candidate).exists():
        return (base_dir / candidate).resolve()
    return candidate.resolve()


def error(message: str) -> str:
    return f"输入校验失败：{message}"


def validate_pending_tables(content: str) -> list[str]:
    errors: list[str] = []
    for table in parse_tables(content):
        if not all(any(required in cell for cell in table.header) for required in PENDING_HEADERS):
            continue
        indices = {header: next(i for i, cell in enumerate(table.header) if header in cell) for header in PENDING_HEADERS}
        for row in table.rows:
            if len(row) < len(table.header):
                row = row + [""] * (len(table.header) - len(row))
            for header in PENDING_HEADERS:
                value = row[indices[header]].strip() if indices[header] < len(row) else ""
                if not value:
                    errors.append(f"待确认事实缺少{header}")
        return errors
    return errors


def validate_handoff_content(content: str) -> list[str]:
    errors: list[str] = []
    for phrase in REQUIRED_HANOFF_PHRASES:
        if phrase not in content:
            errors.append(f"架构交接缺少字段：{phrase}")
    return errors


def validate_architecture(path: Path, adrs: list[Path]) -> list[str]:
    errors: list[str] = []
    if not path.exists() or not path.is_file():
        return [f"架构文件不存在或不可读：{path}"]

    try:
        content = read_text(path)
    except OSError as exc:
        return [f"架构文件无法读取：{path}（{exc}）"]

    scene = extract_field(content, ["场景", "scene"])
    if scene != "pre-development":
        errors.append(f"场景必须是 pre-development，当前为：{scene or '缺失'}")

    state = extract_field(content, ["状态", "state"])
    if state == "complete":
        errors.append("状态不能是 complete，请使用 draft、blocked 或 design-ready")
    elif state != "design-ready":
        errors.append(f"状态必须是 design-ready，当前为：{state or '缺失'}")

    boundary = extract_field(content, ["架构边界", "confirmed boundaries", "confirmed boundary", "边界"])
    if not non_empty(boundary):
        errors.append("缺少架构边界证据")

    pending_errors = validate_pending_tables(content)
    errors.extend(pending_errors)

    referenced_md = markdown_files_referenced(content, path.parent)
    handoff_candidates = [path] + [ref for ref in referenced_md if ref.name == "architecture-handoff.md"]
    seen: set[Path] = set()
    for handoff_path in handoff_candidates:
        if handoff_path in seen:
            continue
        seen.add(handoff_path)
        if not handoff_path.exists() or not handoff_path.is_file():
            continue
        try:
            handoff_content = read_text(handoff_path)
        except OSError as exc:
            errors.append(f"架构交接文件无法读取：{handoff_path}（{exc}）")
            continue
        if "Architecture Handoff Contract" in handoff_content or "Required fields" in handoff_content:
            errors.extend(validate_handoff_content(handoff_content))

    for adr in adrs:
        if not adr.exists() or not adr.is_file():
            errors.append(f"ADR 不可读取：{adr}")
            continue
        try:
            read_text(adr)
        except OSError as exc:
            errors.append(f"ADR 不可读取：{adr}（{exc}）")

    if not adrs:
        errors.append("缺少 --adr 参数，至少需要一个 ADR 文件")

    return errors


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv or sys.argv[1:])
    architecture_path = Path(args.architecture).expanduser()
    base_dir = architecture_path.parent if architecture_path.parent != Path("") else Path.cwd()
    adr_paths = [resolve_path(value, base_dir) for value in args.adrs]

    errors = validate_architecture(architecture_path, adr_paths)
    if errors:
        for message in errors:
            print(error(message), file=sys.stderr)
        return 1

    print("输入校验通过：架构输入、ADR 和待确认事实结构有效，可进入详细设计。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
