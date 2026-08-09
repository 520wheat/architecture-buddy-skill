#!/usr/bin/env python3
"""初始化 Architecture Buddy 的三类设计产物。"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TEMPLATE_FILES = {
    "architecture": ("architecture-deliverable.md", "{name}-architecture-design.md"),
    "adr": ("adr-template.md", "{name}-adr.md"),
    "record": ("decision-record.md", "{name}-decision-record.md"),
}


def safe_name(value: str) -> str:
    """将用户名称变成不会穿越目录的可读文件名前缀。"""
    normalized = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", value.strip(), flags=re.UNICODE)
    normalized = normalized.strip(".-")
    return normalized or "architecture-design"


def replace_title(content: str, kind: str, name: str) -> str:
    if kind == "architecture":
        return content.replace("# 架构设计：<问题类一句话>", f"# 架构设计：{name}", 1)
    if kind == "adr":
        return content.replace("# ADR：<具体决策名称>", f"# ADR：{name}", 1)
    return content.replace("# 决策过程记录：<问题或决策点>", f"# 决策过程记录：{name}", 1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="在指定目录初始化正式架构设计、架构 ADR 和决策过程记录。"
    )
    parser.add_argument("--output", required=True, help="产物输出目录")
    parser.add_argument("--name", required=True, help="设计名称，用于标题和文件名前缀")
    parser.add_argument("--force", action="store_true", help="允许覆盖同名产物")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_dir = Path(args.output).expanduser()
    name = safe_name(args.name)
    template_dir = Path(__file__).resolve().parent.parent / "templates"
    targets = {
        kind: output_dir / filename.format(name=name)
        for kind, (_, filename) in TEMPLATE_FILES.items()
    }

    existing = [path for path in targets.values() if path.exists()]
    if existing and not args.force:
        print("初始化失败：以下产物已存在；如需覆盖请显式传入 --force：", file=sys.stderr)
        for path in existing:
            print(f"- {path}", file=sys.stderr)
        return 2

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        for kind, (template_name, _) in TEMPLATE_FILES.items():
            template = template_dir / template_name
            if not template.is_file():
                print(f"初始化失败：找不到运行时模板 {template}", file=sys.stderr)
                return 2
            content = replace_title(template.read_text(encoding="utf-8"), kind, name)
            targets[kind].write_text(content.rstrip() + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"初始化失败：{exc}", file=sys.stderr)
        return 2

    print(f"已初始化设计工作区：{output_dir}")
    for kind in TEMPLATE_FILES:
        print(f"- {kind}: {targets[kind]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
