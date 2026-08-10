#!/usr/bin/env python3
"""Shared helpers for the Architecture Buddy research evidence scripts."""

from __future__ import annotations

import csv
import hashlib
import html
import ipaddress
import json
import re
import socket
from datetime import datetime, timezone
from email.message import Message
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse


SOURCE_FIELDS = (
    "source_id",
    "url",
    "title",
    "source_type",
    "status",
    "fetched_at",
    "content_type",
    "raw_file",
    "clean_file",
    "metadata_file",
    "sha256",
    "error",
)
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_plan(workspace: Path) -> dict:
    path = workspace / "research-plan.json"
    with path.open(encoding="utf-8") as handle:
        plan = json.load(handle)
    if not isinstance(plan, dict):
        raise ValueError("research-plan.json 必须是 JSON 对象")
    return plan


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_sources(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise ValueError(f"找不到来源清单 {path}")
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None or not set(("source_id", "url", "title", "source_type")).issubset(reader.fieldnames):
            raise ValueError("sources.tsv 必须包含 source_id、url、title、source_type 列")
        rows: list[dict[str, str]] = []
        seen: set[str] = set()
        for line_number, row in enumerate(reader, start=2):
            if not any((value or "").strip() for value in row.values()):
                continue
            source_id = (row.get("source_id") or "").strip()
            if not source_id:
                raise ValueError(f"sources.tsv 第 {line_number} 行缺少 source_id")
            if not SAFE_ID.fullmatch(source_id):
                raise ValueError(f"来源 ID 不安全：{source_id!r}（只允许字母、数字、点、下划线和短横线）")
            if source_id in seen:
                raise ValueError(f"sources.tsv 存在重复 source_id：{source_id}")
            seen.add(source_id)
            url = (row.get("url") or "").strip()
            if not url:
                raise ValueError(f"sources.tsv 第 {line_number} 行缺少 url")
            rows.append({field: (row.get(field) or "").strip() for field in SOURCE_FIELDS})
        return rows


def write_sources(path: Path, rows: Iterable[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SOURCE_FIELDS, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in SOURCE_FIELDS} for row in rows)


def expected_artifacts(workspace: Path, source_id: str) -> dict[str, Path]:
    """Return fixed artifact locations; never trust paths supplied in a TSV row."""
    return {
        "raw": workspace / "raw" / f"{source_id}.raw",
        "clean": workspace / "clean" / f"{source_id}.txt",
        "metadata": workspace / "metadata" / f"{source_id}.json",
    }


class TextExtractor(HTMLParser):
    """Extract readable HTML text while ignoring executable/presentation blocks."""

    ignored = {"script", "style", "noscript", "template"}
    block = {"article", "aside", "br", "div", "footer", "h1", "h2", "h3", "h4", "header", "li", "main", "p", "pre", "section", "tr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.ignored:
            self.depth += 1
        elif not self.depth and tag in self.block:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.ignored and self.depth:
            self.depth -= 1
        elif not self.depth and tag in self.block:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.depth:
            self.parts.append(data)


def normalize_text(text: str) -> str:
    text = html.unescape(text).replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    result: list[str] = []
    for line in lines:
        if line:
            if result and result[-1] == line:
                continue
            result.append(line)
        elif result and result[-1] != "":
            result.append("")
    while result and result[-1] == "":
        result.pop()
    return "\n".join(result) + ("\n" if result else "")


def clean_html(data: bytes, charset: str) -> str:
    parser = TextExtractor()
    parser.feed(data.decode(charset, errors="replace"))
    parser.close()
    return normalize_text("".join(parser.parts))


def clean_subtitles(data: bytes, charset: str) -> str:
    text = data.decode(charset, errors="replace").replace("\ufeff", "")
    kept: list[str] = []
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        stripped = line.strip()
        if not stripped or stripped.upper() == "WEBVTT" or stripped.upper() == "NOTE" or stripped.upper().startswith("NOTE "):
            continue
        if re.fullmatch(r"\d+", stripped) or "-->" in stripped:
            continue
        stripped = re.sub(r"<[^>]+>", "", stripped)
        if stripped:
            kept.append(stripped)
    return normalize_text("\n".join(kept))


def parse_charset(content_type: str) -> str:
    message = Message()
    message["content-type"] = content_type
    return message.get_param("charset") or "utf-8"


def content_kind(url: str, content_type: str) -> str:
    lower_type = content_type.lower()
    lower_url = url.lower().split("?", 1)[0]
    if "html" in lower_type or lower_url.endswith((".html", ".htm")):
        return "html"
    if "vtt" in lower_type or lower_url.endswith(".vtt"):
        return "vtt"
    if "srt" in lower_type or "subrip" in lower_type or lower_url.endswith(".srt"):
        return "srt"
    if "json" in lower_type or lower_url.endswith(".json"):
        return "json"
    if any(token in lower_type for token in ("text/", "markdown", "xml")) or lower_url.endswith((".txt", ".md", ".markdown", ".xml")):
        return "text"
    return "binary"


def clean_content(data: bytes, url: str, content_type: str) -> tuple[str, str]:
    kind = content_kind(url, content_type)
    charset = parse_charset(content_type)
    if kind == "html":
        return kind, clean_html(data, charset)
    if kind in {"vtt", "srt"}:
        return kind, clean_subtitles(data, charset)
    if kind == "json":
        decoded = data.decode(charset, errors="replace")
        try:
            return kind, json.dumps(json.loads(decoded), ensure_ascii=False, indent=2) + "\n"
        except json.JSONDecodeError:
            return kind, normalize_text(decoded)
    if kind == "text":
        return kind, normalize_text(data.decode(charset, errors="replace"))
    return kind, ""


def validate_url(url: str, allow_private: bool = False) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("只允许带主机名的 http:// 或 https:// URL")
    if parsed.username or parsed.password:
        raise ValueError("URL 不允许携带用户名或密码")
    if allow_private:
        return
    try:
        addresses = {info[4][0] for info in socket.getaddrinfo(parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80), type=socket.SOCK_STREAM)}
    except socket.gaierror as exc:
        raise ValueError(f"无法解析主机名：{parsed.hostname}") from exc
    for address in addresses:
        ip = ipaddress.ip_address(address.split("%", 1)[0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_unspecified or ip.is_multicast or ip.is_reserved:
            raise ValueError(f"默认阻止访问本地或保留地址：{address}；如确需测试请显式使用 --allow-private-hosts")


def atomic_write(path: Path, data: bytes | str, encoding: str | None = None) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    if isinstance(data, bytes):
        temporary.write_bytes(data)
    else:
        temporary.write_text(data, encoding=encoding or "utf-8")
    temporary.replace(path)
