#!/usr/bin/env python3
"""Merge a session markdown into mianshi-deck.md (incremental)."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

import yaml

CHAPTER_RE = re.compile(r"^## 岗：.+$", re.M)
ENTRY_ID_RE = re.compile(r"^deck_entry_id:\s*(\S+)\s*$", re.M)


def read_entry_id(session_path: Path) -> str:
    text = session_path.read_text(encoding="utf-8")
    m = ENTRY_ID_RE.search(text)
    if not m:
        raise ValueError(f"session missing deck_entry_id: {session_path}")
    return m.group(1)


def extract_title(session_text: str) -> str:
    for line in session_text.splitlines():
        if line.startswith("# 岗："):
            return line.replace("# 岗：", "## 岗：", 1)
    raise ValueError("session missing '# 岗：' title")


def archive_chapter(deck_text: str, entry_id: str, audit_dir: Path) -> str | None:
    pattern = re.compile(
        rf"(## 岗：[^\n]+\n<!-- entry_id: {re.escape(entry_id)} -->.*?)(?=\n## 岗：|\Z)",
        re.S,
    )
    m = pattern.search(deck_text)
    if not m:
        return None
    old = m.group(1)
    audit_dir.mkdir(parents=True, exist_ok=True)
    out = audit_dir / f"archived-{entry_id}-{date.today().isoformat()}.md"
    out.write_text(old, encoding="utf-8")
    return old


def wrap_session(session_text: str, entry_id: str) -> str:
    title = extract_title(session_text)
    body = session_text
    if body.startswith("---"):
        end = body.find("---", 3)
        if end != -1:
            body = body[end + 3 :].lstrip()
    if body.startswith("# 岗："):
        body = body.split("\n", 1)[1].lstrip()
    return f"{title}\n<!-- entry_id: {entry_id} -->\n\n{body}\n"


def merge_deck(deck_path: Path, session_path: Path, index_path: Path) -> None:
    entry_id = read_entry_id(session_path)
    session_text = session_path.read_text(encoding="utf-8")
    chapter = wrap_session(session_text, entry_id)
    deck_text = deck_path.read_text(encoding="utf-8")
    audit_dir = deck_path.parent / "audit"

    pattern = re.compile(
        rf"## 岗：[^\n]+\n<!-- entry_id: {re.escape(entry_id)} -->.*?(?=\n## 岗：|\Z)",
        re.S,
    )
    if pattern.search(deck_text):
        archive_chapter(deck_text, entry_id, audit_dir)
        deck_text = pattern.sub(chapter.rstrip() + "\n", deck_text)
        action = "replaced"
    else:
        deck_text = deck_text.rstrip() + "\n\n---\n\n" + chapter
        action = "appended"

    deck_path.write_text(deck_text, encoding="utf-8")

    index_data = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
    entries = index_data.get("entries", [])
    entries = [e for e in entries if e.get("id") != entry_id]
    company, role = "", ""
    m_co = re.search(r"^company:\s*(.+)$", session_text, re.M)
    m_ro = re.search(r"^role:\s*(.+)$", session_text, re.M)
    if m_co:
        company = m_co.group(1).strip()
    if m_ro:
        role = m_ro.group(1).strip()
    entries.append(
        {
            "id": entry_id,
            "company": company,
            "role": role,
            "session_file": str(session_path.relative_to(deck_path.parent)),
            "updated_at": str(date.today()),
            "status": "active",
        }
    )
    index_data["entries"] = entries
    index_path.write_text(yaml.dump(index_data, allow_unicode=True, sort_keys=False), encoding="utf-8")

    log = audit_dir / f"deck-merge-{date.today().isoformat()}.md"
    line = f"- {action} `{entry_id}` from `{session_path.name}`\n"
    if log.is_file():
        log.write_text(log.read_text(encoding="utf-8") + line, encoding="utf-8")
    else:
        log.write_text(f"# deck-merge log\n\n{line}", encoding="utf-8")

    print(f"OK: {action} {entry_id}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deck", type=Path, required=True)
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--index", type=Path, required=True)
    args = parser.parse_args()
    merge_deck(args.deck, args.session, args.index)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
