#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from validator_helpers import (
    extract_field,
    find_rows,
    line_has_substance,
    parse_tables,
    read_text,
    section_body,
    substantive_value,
)


OVERVIEW_SECTIONS = [
    "元数据与架构输入",
    "设计范围与非目标",
    "设计单元索引",
    "架构反馈索引",
    "单元关系",
    "跨模块契约",
    "端到端流程",
    "统一规则",
    "测试策略",
    "实现顺序",
    "待确认事实",
    "回退项",
    "完成状态",
]

MODULE_SECTIONS = [
    "职责与边界",
    "依赖与禁止边",
    "外部接口与内部接口",
    "请求 / 响应与字段约束",
    "错误语义",
    "状态机与不变量",
    "行为与时序",
    "超时 / 重试 / 幂等 / 并发",
    "权限 / 审计 / 日志 / 指标 / 追踪 / 配置",
    "测试",
    "验收条件",
    "待确认事实",
    "回退项",
]

PENDING_HEADERS = [
    "编号",
    "事实",
    "单阶段默认值",
    "默认原因",
    "验证条件",
    "回退路径",
    "重新打开条件",
]

ROLLBACK_HEADERS = [
    "编号",
    "回退触发事实",
    "回退目标",
    "回退动作",
    "恢复条件",
    "关联待确认事实",
]

OVERVIEW_TABLE_HEADERS = {
    "设计单元索引": ["顺序", "单元", "责任", "产物"],
    "架构反馈索引": ["编号", "标题", "影响模块", "当前状态", "反馈文档引用"],
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="校验详细设计交付物目录。")
    parser.add_argument("output_dir", help="详细设计输出目录")
    return parser


def error(message: str) -> str:
    return f"详细设计校验失败：{message}"


def complete_row(headers: list[str], row: list[str]) -> bool:
    if len(row) < len(headers):
        row = row + [""] * (len(headers) - len(row))
    return all(substantive_value(row[idx]) for idx in range(len(headers)))


def validate_table_section(content: str, section: str, headers: list[str]) -> list[str]:
    errors: list[str] = []
    rows = find_rows(section_body(content, section) or "", headers)
    if not rows:
        errors.append(f"{section}缺少结构化表格或条目")
        return errors
    table = None
    for candidate in parse_tables(section_body(content, section) or ""):
        if all(any(required in cell for cell in candidate.header) for required in headers):
            table = candidate
            break
    if table is None:
        errors.append(f"{section}缺少所需表头：{' / '.join(headers)}")
        return errors
    for row in table.rows:
        if not complete_row(table.header, row):
            errors.append(f"{section}存在未完成条目：{' / '.join(headers)}")
            break
    return errors


def validate_pending_section(content: str, section: str) -> list[str]:
    return validate_table_section(content, section, PENDING_HEADERS)


def validate_rollback_section(content: str, section: str) -> list[str]:
    return validate_table_section(content, section, ROLLBACK_HEADERS)


def validate_nonempty_section(content: str, section: str) -> list[str]:
    body = section_body(content, section)
    if body is None:
        return [f"缺少模板证据：{section}"]
    if not line_has_substance(body):
        return [f"{section}缺少可验证内容"]
    return []


def validate_overview(content: str) -> list[str]:
    errors: list[str] = []
    state_value = extract_field(content, ["状态"])
    if state_value == "blocked":
        errors.append("输出状态不能是 blocked")
    if state_value == "complete":
        errors.append("输出状态不能是 complete，请使用 draft、blocked 或 design-ready")

    for section in OVERVIEW_SECTIONS:
        errors.extend(validate_nonempty_section(content, section))

    for section, headers in OVERVIEW_TABLE_HEADERS.items():
        errors.extend(validate_table_section(content, section, headers))

    errors.extend(validate_pending_section(content, "待确认事实"))
    errors.extend(validate_rollback_section(content, "回退项"))

    contract_body = section_body(content, "跨模块契约")
    if contract_body is None or not line_has_substance(contract_body):
        errors.append("缺少跨模块契约证据")

    return errors


def validate_module(content: str, module_path: Path) -> list[str]:
    errors: list[str] = []
    for section in MODULE_SECTIONS:
        if section in {"待确认事实", "回退项"}:
            continue
        errors.extend(validate_nonempty_section(content, section))

    errors.extend(validate_pending_section(content, "待确认事实"))
    errors.extend(validate_rollback_section(content, "回退项"))

    return errors


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv or sys.argv[1:])
    root = Path(args.output_dir).expanduser()

    if not root.exists() or not root.is_dir():
        print(error(f"输出目录不存在或不是目录：{root}"), file=sys.stderr)
        return 1

    overview_path = root / "detailed-design-overview.md"
    modules_dir = root / "modules"

    if not overview_path.is_file():
        print(error(f"缺少 overview 文件：{overview_path}"), file=sys.stderr)
        return 1
    if not modules_dir.is_dir():
        print(error(f"缺少 modules 目录：{modules_dir}"), file=sys.stderr)
        return 1

    module_files = sorted(path for path in modules_dir.glob("*.md") if path.is_file())
    if not module_files:
        print(error("至少需要一个 module 文档"), file=sys.stderr)
        return 1

    errors: list[str] = []
    try:
        overview_content = read_text(overview_path)
    except OSError as exc:
        print(error(f"无法读取 overview：{exc}"), file=sys.stderr)
        return 1

    errors.extend(validate_overview(overview_content))

    for module_path in module_files:
        try:
            module_content = read_text(module_path)
        except OSError as exc:
            errors.append(f"无法读取模块文档 {module_path.name}：{exc}")
            continue
        errors.extend(validate_module(module_content, module_path))

    if errors:
        for message in errors:
            print(error(message), file=sys.stderr)
        return 1

    print("详细设计校验通过：目录结构、模板证据、跨模块契约和回退项已就绪。")
    print("说明：本脚本只检查结构证据，不判断架构质量。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
