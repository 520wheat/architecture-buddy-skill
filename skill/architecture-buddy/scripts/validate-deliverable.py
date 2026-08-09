#!/usr/bin/env python3
"""检查正式架构设计的结构证据，不判断架构方案优劣。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_GROUPS = {
    "设计标题": (("架构设计",),),
    "问题类与目标": (("问题类",), ("目标",)),
    "边界与上下文": (("边界",),),
    "主路径": (("主路径",),),
    "组件与契约": (("组件", "模块"), ("契约", "接口")),
    "基本事实或领域不变量": (("基本事实", "不变量"),),
    "失败证据": (("用户可见状态",), ("触发条件",), ("观察结果",), ("恢复动作",), ("残余风险",)),
    "演进": (("演进",),),
    "机制与策略": (("机制",), ("策略",)),
    "取舍与理由": (("取舍", "决定"), ("理由", "依据")),
    "验收": (("验收",),),
    "组合边界": (("N+1",), ("反例",)),
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="检查正式架构设计的结构证据。")
    parser.add_argument("file", help="待检查的 Markdown 文件")
    return parser


def has_any(content: str, alternatives: tuple[str, ...]) -> bool:
    return any(item in content for item in alternatives)


def validate(content: str) -> list[str]:
    errors: list[str] = []
    headings = [line.lstrip("#").strip() for line in content.splitlines() if line.startswith("#")]
    has_formal_heading = any("架构设计" in heading and "记录" not in heading for heading in headings)
    is_process_record = (
        any(heading.startswith(("会议记录", "决策过程记录")) for heading in headings)
        or "产物角色：**决策过程记录**" in content
    )
    if is_process_record and not has_formal_heading:
        errors.append("文件看起来是会议记录，缺少正式架构设计正文")

    for group, requirements in REQUIRED_GROUPS.items():
        for alternatives in requirements:
            if not has_any(content, alternatives):
                errors.append(f"缺少结构证据：{group}（需要 { ' / '.join(alternatives) }）")

    if content.count("用户可见状态") < 1 or content.count("残余风险") < 1:
        errors.append("失败证据必须包含结构化失败表，而不是只写重试或降级")
    return errors


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    path = Path(args.file).expanduser()
    if not path.is_file():
        print(f"校验失败：找不到文件 {path}", file=sys.stderr)
        return 2
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"校验失败：无法读取文件：{exc}", file=sys.stderr)
        return 2

    errors = validate(content)
    if errors:
        print("结构校验失败：")
        for error in errors:
            print(f"- {error}")
        print("说明：此脚本只判断结构证据，不判断架构设计是否优秀。")
        return 1

    print("结构校验通过：已发现正式架构设计所需的主要结构证据。")
    print("说明：通过不等于架构方案正确或优秀，仍需人工审阅和领域验证。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
