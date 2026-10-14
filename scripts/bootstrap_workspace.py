#!/usr/bin/env python3
"""Init laowang-mianshi-zhu workspace."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

import yaml

DIRS = ["sessions", "drills", "audit"]


def default_root(season: str) -> Path:
    return Path(__file__).resolve().parent.parent / "workspace" / season


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--season", default="2027-fall")
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args()

    root = (args.root or default_root(args.season)).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    for d in DIRS:
        (root / d).mkdir(exist_ok=True)

    deck = root / "mianshi-deck.md"
    if not deck.exists():
        tpl = Path(__file__).parent.parent / "assets" / "mianshi-deck-template.md"
        deck.write_text(tpl.read_text(encoding="utf-8"), encoding="utf-8")

    index = root / "deck-index.yaml"
    if not index.exists():
        data = {"season": args.season, "created_at": str(date.today()), "entries": []}
        index.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")

    print(f"OK: {root}")
    print(f"  deck: {deck}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
