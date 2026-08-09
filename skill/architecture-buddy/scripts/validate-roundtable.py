#!/usr/bin/env python3
"""检查圆桌过程证据和正式产物回写，不评价席位观点质量。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


FULL_RECORD_FIELDS = (
    "高影响互斥分叉",
    "提议圆桌",
    "主持人提问",
    "用户同意圆桌",
    "席位选择理由",
    "用户反馈",
    "反馈影响",
    "主持人综合结论",
    "正式架构设计",
    "架构 ADR",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="检查圆桌过程证据和综合回写字段。")
    parser.add_argument("file", help="待检查的决策过程记录 Markdown 文件")
    return parser


def field_value(content: str, label: str) -> str:
    for line in content.splitlines():
        if line.startswith(label + "："):
            return line.split("：", 1)[1].strip()
        if line.startswith(label + ":"):
            return line.split(":", 1)[1].strip()
    return ""


def validate(content: str) -> list[str]:
    errors: list[str] = []
    if "用户选择跳过圆桌" in content:
        required = ("高影响互斥分叉", "提议圆桌", "主持人提问", "用户同意圆桌", "正式架构设计", "架构 ADR")
        for label in required:
            if not field_value(content, label) and label not in content:
                errors.append(f"跳过圆桌记录缺少：{label}")
        return errors

    for label in FULL_RECORD_FIELDS:
        if not field_value(content, label):
            errors.append(f"缺少过程记录字段：{label}")

    feedback = field_value(content, "用户反馈")
    normalized_feedback = feedback.strip().rstrip("。.!！?？")
    if normalized_feedback in {"同意", "用户同意", "是", "ok", "OK", ""}:
        errors.append("用户反馈必须是实质性选择、质疑、修改、补充约束或待验证标记")
    impact = field_value(content, "反馈影响")
    normalized_impact = impact.strip().rstrip("。.!！?？")
    if normalized_impact in {"无", "没有", "不变", "未改变", ""}:
        errors.append("反馈影响必须绑定到具体的选择、边界、代价、验收或演进项")
    if "## Lens:" not in content and "透镜状态：无匹配透镜" not in content:
        errors.append("缺少至少一个透镜输出，或缺少无匹配透镜的诚实降级记录")
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
        print("圆桌过程校验失败：")
        for error in errors:
            print(f"- {error}")
        print("说明：此脚本只判断过程证据，不判断圆桌观点或架构方案是否优秀。")
        return 1

    print("圆桌过程校验通过：已发现提议、反馈、综合和正式产物回写证据。")
    print("说明：通过不等于圆桌结论正确，仍需主持人和用户审阅。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
