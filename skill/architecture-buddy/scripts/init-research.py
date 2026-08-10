#!/usr/bin/env python3
"""Create a user-authorized web research workspace."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from research_common import SOURCE_FIELDS, write_json, write_sources, utc_now


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="初始化联网调查工作区；联网授权必须显式提供。")
    parser.add_argument("--output", required=True, help="调查工作区目录")
    parser.add_argument("--problem-class", required=True, help="已经与用户确认的问题类")
    parser.add_argument("--decision-question", required=True, help="单一、可调查的架构决策问题")
    parser.add_argument("--source", action="append", default=[], metavar="ID=URL", help="预置来源，可重复；标题和类型之后可在 sources.tsv 补充")
    parser.add_argument("--authorize-online-research", action="store_true", help="确认用户已经授权本次联网调查")
    parser.add_argument("--force", action="store_true", help="显式允许覆盖同名工作区文件")
    return parser


def parse_source(value: str) -> dict[str, str]:
    if "=" not in value:
        raise ValueError(f"来源必须采用 ID=URL 格式：{value}")
    source_id, url = value.split("=", 1)
    return {field: "" for field in SOURCE_FIELDS} | {"source_id": source_id.strip(), "url": url.strip(), "source_type": "web"}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output = Path(args.output).expanduser()
    plan_path = output / "research-plan.json"
    sources_path = output / "sources.tsv"
    if (plan_path.exists() or sources_path.exists()) and not args.force:
        print(f"初始化失败：{output} 已有研究工作区；如需覆盖请显式传入 --force", file=sys.stderr)
        return 2
    try:
        sources = [parse_source(value) for value in args.source]
        plan = {
            "schema_version": 1,
            "problem_class": args.problem_class.strip(),
            "decision_question": args.decision_question.strip(),
            "online_research_authorized": bool(args.authorize_online_research),
            "authorization_recorded_at": utc_now() if args.authorize_online_research else "",
            "research_status": "planned",
            "created_at": utc_now(),
            "evidence_file": "evidence.md",
        }
        output.mkdir(parents=True, exist_ok=True)
        (output / "raw").mkdir(exist_ok=True)
        (output / "clean").mkdir(exist_ok=True)
        (output / "metadata").mkdir(exist_ok=True)
        write_json(plan_path, plan)
        write_sources(sources_path, sources)
        (output / "evidence.md").write_text("", encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"初始化失败：{exc}", file=sys.stderr)
        return 2
    print(f"已初始化联网调查工作区：{output}")
    print(f"- 在线调查授权：{'是' if plan['online_research_authorized'] else '否'}")
    print(f"- 来源数量：{len(sources)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
