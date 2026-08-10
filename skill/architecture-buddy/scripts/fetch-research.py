#!/usr/bin/env python3
"""Fetch explicitly listed research sources and preserve provenance."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

from research_common import (
    atomic_write,
    clean_content,
    expected_artifacts,
    load_plan,
    read_sources,
    sha256_bytes,
    utc_now,
    validate_url,
    write_json,
    write_sources,
)


class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, allow_private: bool) -> None:
        super().__init__()
        self.allow_private = allow_private

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        validate_url(urljoin(req.full_url, newurl), self.allow_private)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="抓取 sources.tsv 中已授权的研究来源并生成 raw/clean/metadata。")
    parser.add_argument("--workspace", required=True, help="联网调查工作区目录")
    parser.add_argument("--timeout", type=float, default=15, help="单个来源超时秒数，默认 15")
    parser.add_argument("--max-bytes", type=int, default=5_000_000, help="单个响应最大字节数，默认 5000000")
    parser.add_argument("--refresh", action="store_true", help="重新抓取已成功来源")
    parser.add_argument("--allow-private-hosts", action="store_true", help="允许本地/私有地址，仅用于明确授权的测试场景")
    return parser


def fetch_one(row: dict[str, str], workspace: Path, args: argparse.Namespace) -> None:
    source_id = row["source_id"]
    now = utc_now()
    artifacts = expected_artifacts(workspace, source_id)
    metadata_path = artifacts["metadata"]
    metadata = {
        "source_id": source_id,
        "url": row["url"],
        "title": row.get("title", ""),
        "source_type": row.get("source_type", "web") or "web",
        "fetched_at": now,
        "status": "failed",
    }
    try:
        validate_url(row["url"], args.allow_private_hosts)
        request = urllib.request.Request(row["url"], headers={"User-Agent": "architecture-buddy-research/1.0"})
        opener = urllib.request.build_opener(SafeRedirectHandler(args.allow_private_hosts))
        with opener.open(request, timeout=args.timeout) as response:
            content_type = response.headers.get("Content-Type", "application/octet-stream")
            data = bytearray()
            while True:
                chunk = response.read(min(64 * 1024, args.max_bytes + 1 - len(data)))
                if not chunk:
                    break
                data.extend(chunk)
                if len(data) > args.max_bytes:
                    raise ValueError(f"响应超过 --max-bytes 限制（{args.max_bytes} 字节）")
            raw = bytes(data)
            final_url = response.geturl()
        raw_name = f"{source_id}.raw"
        atomic_write(artifacts["raw"], raw)
        metadata.update({
            "final_url": final_url,
            "content_type": content_type,
            "raw_file": f"raw/{raw_name}",
            "raw_bytes": len(raw),
            "raw_sha256": sha256_bytes(raw),
        })
        kind, clean = clean_content(raw, final_url, content_type)
        if kind == "binary":
            raise ValueError(f"不支持将该内容类型整理为文本证据：{content_type}")
        clean_name = f"{source_id}.txt"
        atomic_write(artifacts["clean"], clean, "utf-8")
        metadata.update({
            "status": "fetched",
            "final_url": final_url,
            "content_type": content_type,
            "content_kind": kind,
            "raw_file": f"raw/{raw_name}",
            "clean_file": f"clean/{clean_name}",
            "clean_bytes": len(clean.encode("utf-8")),
            "clean_sha256": sha256_bytes(clean.encode("utf-8")),
        })
        row.update({
            "status": "fetched",
            "fetched_at": now,
            "content_type": content_type,
            "raw_file": f"raw/{raw_name}",
            "clean_file": f"clean/{clean_name}",
            "metadata_file": f"metadata/{source_id}.json",
            "sha256": metadata["raw_sha256"],
            "error": "",
        })
    except (LookupError, OSError, ValueError, urllib.error.URLError, urllib.error.HTTPError) as exc:
        metadata["error"] = str(exc)
        row.update({"status": "failed", "fetched_at": now, "metadata_file": f"metadata/{source_id}.json", "error": str(exc)})
    write_json(metadata_path, metadata)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    workspace = Path(args.workspace).expanduser()
    if args.timeout <= 0 or args.max_bytes <= 0:
        print("抓取失败：timeout 和 max-bytes 必须为正数", file=sys.stderr)
        return 2
    try:
        plan = load_plan(workspace)
        if not plan.get("online_research_authorized"):
            print("抓取失败：研究计划没有记录用户的联网调查授权", file=sys.stderr)
            return 2
        rows = read_sources(workspace / "sources.tsv")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"抓取失败：{exc}", file=sys.stderr)
        return 2

    attempted = 0
    fetched = 0
    skipped = 0
    for row in rows:
        if row.get("status") == "fetched" and not args.refresh:
            skipped += 1
            continue
        attempted += 1
        fetch_one(row, workspace, args)
        if row.get("status") == "fetched":
            fetched += 1
    write_sources(workspace / "sources.tsv", rows)
    plan["research_status"] = "fetched" if any(row.get("status") == "fetched" for row in rows) else "failed"
    plan["last_fetched_at"] = utc_now()
    write_json(workspace / "research-plan.json", plan)
    print(f"抓取完成：成功 {fetched}，跳过 {skipped}，尝试 {attempted}")
    if any(row.get("status") == "failed" for row in rows):
        print("提示：失败来源已保留状态和错误；可修正来源后使用 --refresh 重试。")
    return 0 if fetched or skipped else 1


if __name__ == "__main__":
    raise SystemExit(main())
