#!/usr/bin/env python3
"""Validate research workspace completeness and provenance."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from research_common import SAFE_ID, expected_artifacts, load_plan, read_sources, sha256_bytes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="检查联网调查工作区的来源、材料和 provenance。")
    parser.add_argument("--workspace", required=True, help="联网调查工作区目录")
    return parser


def validate(workspace: Path) -> list[str]:
    errors: list[str] = []
    try:
        plan = load_plan(workspace)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"无法读取 research-plan.json：{exc}"]
    for field in ("problem_class", "decision_question"):
        if not str(plan.get(field, "")).strip():
            errors.append(f"研究计划缺少 {field}")
    if not plan.get("online_research_authorized"):
        errors.append("研究计划没有记录用户联网调查授权")
    try:
        rows = read_sources(workspace / "sources.tsv")
    except (OSError, ValueError) as exc:
        return errors + [str(exc)]
    if not rows:
        errors.append("sources.tsv 没有来源")
    success_count = 0
    for row in rows:
        source_id = row["source_id"]
        if not SAFE_ID.fullmatch(source_id):
            errors.append(f"来源 {source_id!r} 的 ID 不安全")
        artifacts = expected_artifacts(workspace, source_id)
        expected_paths = {
            "raw_file": f"raw/{source_id}.raw",
            "clean_file": f"clean/{source_id}.txt",
            "metadata_file": f"metadata/{source_id}.json",
        }
        for field, expected in expected_paths.items():
            if row.get(field) and row[field] != expected:
                errors.append(f"来源 {source_id} 的 {field} 路径不符合工作区契约")
        metadata_path = artifacts["metadata"]
        if not metadata_path.is_file():
            errors.append(f"来源 {source_id} 缺少 metadata provenance 文件")
            continue
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"来源 {source_id} 的 metadata 无法读取：{exc}")
            continue
        if metadata.get("source_id") != source_id or metadata.get("url") != row["url"]:
            errors.append(f"来源 {source_id} 的 metadata 与 sources.tsv provenance 不一致")
        status = row.get("status") or "pending"
        if status == "fetched":
            success_count += 1
            clean_path = artifacts["clean"]
            raw_path = artifacts["raw"]
            for path, label in ((clean_path, "clean"), (raw_path, "raw")):
                if not path.is_file():
                    errors.append(f"来源 {source_id} 缺少 {label} 文件")
            if raw_path.is_file() and metadata.get("raw_sha256") != sha256_bytes(raw_path.read_bytes()):
                errors.append(f"来源 {source_id} 的 raw hash 不匹配")
            if clean_path.is_file() and metadata.get("clean_sha256") != sha256_bytes(clean_path.read_bytes()):
                errors.append(f"来源 {source_id} 的 clean hash 不匹配")
            if metadata.get("status") != "fetched" or not metadata.get("fetched_at") or not metadata.get("final_url"):
                errors.append(f"来源 {source_id} 的成功 metadata 缺少状态、时间或最终 URL")
        elif status == "failed":
            if not metadata.get("error"):
                errors.append(f"失败来源 {source_id} 缺少错误信息")
        else:
            errors.append(f"来源 {source_id} 尚未完成抓取（status={status}）")
    if success_count == 0:
        errors.append("没有成功来源，不能形成证据包")
    evidence = workspace / "evidence.md"
    if not evidence.is_file() or not evidence.read_text(encoding="utf-8").strip():
        errors.append("缺少非空 evidence.md")
    elif "来源 URL" not in evidence.read_text(encoding="utf-8") or "原始内容 SHA-256" not in evidence.read_text(encoding="utf-8"):
        errors.append("evidence.md 缺少来源 URL 或原始内容 hash provenance")
    return errors


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    workspace = Path(args.workspace).expanduser()
    errors = validate(workspace)
    if errors:
        print("证据包校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1
    print("证据包校验通过：来源、清洗材料、metadata、hash 和 evidence.md 均可追溯。")
    print("说明：通过不代表来源正确，也不代表架构结论已被证明。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
