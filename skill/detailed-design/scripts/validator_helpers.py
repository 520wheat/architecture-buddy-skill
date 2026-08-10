from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MarkdownTable:
    header: list[str]
    rows: list[list[str]]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_field(content: str, labels: list[str]) -> str | None:
    for label in labels:
        pattern = re.compile(
            rf"^\s*[-*]?\s*{re.escape(label)}\s*[:：][^\S\r\n]*(?P<value>[^\r\n]*)$",
            re.MULTILINE,
        )
        match = pattern.search(content)
        if match:
            value = match.group("value").strip()
            if value:
                return value
    return None


def section_body(content: str, heading: str) -> str | None:
    lines = content.splitlines()
    start_index = None
    level = 0
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        heading_marks, _, title = stripped.partition(" ")
        if title.strip() == heading:
            start_index = index + 1
            level = len(heading_marks)
            break
    if start_index is None:
        return None
    collected: list[str] = []
    for line in lines[start_index:]:
        stripped = line.strip()
        if stripped.startswith("#"):
            next_marks, _, _ = stripped.partition(" ")
            if len(next_marks) <= level:
                break
        collected.append(line)
    return "\n".join(collected).strip()


def is_separator_row(line: str) -> bool:
    stripped = line.strip()
    if "|" not in stripped:
        return False
    core = stripped.strip("|").replace(" ", "")
    return bool(core) and set(core) <= {"-", ":"}


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_tables(content: str) -> list[MarkdownTable]:
    tables: list[MarkdownTable] = []
    block: list[str] = []
    for line in content.splitlines():
        if "|" in line:
            block.append(line)
            continue
        if block:
            tables.extend(parse_table_block(block))
            block = []
    if block:
        tables.extend(parse_table_block(block))
    return tables


def parse_table_block(block: list[str]) -> list[MarkdownTable]:
    rows = [split_row(line) for line in block if line.strip() and not is_separator_row(line)]
    if len(rows) < 2:
        return []
    return [MarkdownTable(header=rows[0], rows=rows[1:])]


def find_table(content: str, required_headers: list[str]) -> MarkdownTable | None:
    for table in parse_tables(content):
        if all(any(required in cell for cell in table.header) for required in required_headers):
            return table
    return None


def find_rows(content: str, required_headers: list[str]) -> list[list[str]]:
    table = find_table(content, required_headers)
    if table is None:
        return []
    return table.rows


def non_empty(value: str | None) -> bool:
    return bool(value and value.strip())


def substantive_value(value: str | None) -> bool:
    if not value:
        return False
    stripped = value.strip()
    if not stripped:
        return False
    if re.search(r"[:：]\s*\S", stripped):
        return True
    stripped = re.sub(r"^[-*]\s*", "", stripped)
    stripped = re.sub(r"^\d+\.\s*", "", stripped)
    if not stripped:
        return False
    if stripped.endswith((":", "：")):
        return False
    return bool(stripped)


def line_has_substance(block: str) -> bool:
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped in {"|", "||"}:
            continue
        if stripped.startswith("|") and is_separator_row(stripped):
            continue
        if stripped.startswith("|"):
            cells = split_row(stripped)
            if any(substantive_value(cell) for cell in cells):
                return True
        elif substantive_value(stripped):
            return True
    return False


def markdown_files_referenced(content: str, base_dir: Path) -> list[Path]:
    refs: list[Path] = []
    seen: set[Path] = set()
    for raw in re.findall(r"([A-Za-z0-9_./\\-]+\.md)", content):
        path = Path(raw)
        if not path.is_absolute():
            path = (base_dir / path).resolve()
        if path in seen:
            continue
        seen.add(path)
        refs.append(path)
    return refs
