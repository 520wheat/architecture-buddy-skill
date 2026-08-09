#!/usr/bin/env python3
"""检查正式架构设计的结构证据，不判断架构方案优劣。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


CORE_SECTIONS = {
    "目标、背景与核心约束": ("目标", "背景", "约束"),
    "实现原则": ("实现原则", "架构原则", "设计原则"),
    "逻辑架构视图": ("逻辑架构", "架构视图", "模块架构", "组件架构"),
    "技术选型与部署方案": ("技术选型", "部署方案", "部署架构", "物理部署"),
    "数据架构与治理": ("数据架构", "数据管理", "数据治理"),
    "非功能设计": ("非功能", "横切关注点", "质量属性"),
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="检查正式架构设计的结构证据。")
    parser.add_argument("file", help="待检查的 Markdown 文件")
    return parser


def has_any(content: str, alternatives: tuple[str, ...]) -> bool:
    return any(item in content for item in alternatives)


def has_heading(headings: list[str], alternatives: tuple[str, ...]) -> bool:
    return any(has_any(heading, alternatives) for heading in headings)


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

    for section, alternatives in CORE_SECTIONS.items():
        if not has_heading(headings, alternatives):
            errors.append(f"缺少核心板块：{section}（标题需包含 { ' / '.join(alternatives) } 之一）")

    if not has_any(content, ("取舍", "关键决策", "决策理由", "选择理由")):
        errors.append("缺少架构决策或取舍：需要说明选择了什么")
    if not has_any(content, ("理由", "依据", "因为", "由于")):
        errors.append("缺少决策理由：需要说明为什么这样选择")
    if not has_any(content, ("验收", "验收条件", "成功标准", "可观察")):
        errors.append("缺少可验证的验收条件")

    if not has_any(content, ("模块", "组件", "服务")):
        errors.append("逻辑架构缺少模块/组件/服务职责证据")
    if not has_any(content, ("协作", "调用", "通信", "接口", "契约", "数据流")):
        errors.append("逻辑架构缺少协作或契约证据")
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
        print("说明：此脚本只判断核心结构证据，不判断架构方案是否正确或优秀。")
        return 1

    print("结构校验通过：已发现六个核心板块及基本决策、协作和验收证据。")
    print("说明：通过不等于架构方案正确或优秀；失败深度、领域不变量、反例和演进按适用性人工审阅。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
