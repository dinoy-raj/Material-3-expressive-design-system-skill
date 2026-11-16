#!/usr/bin/env python3
"""Validate the skill: SKILL.md frontmatter, size, and that every file it or the docs point to exists.

Run from anywhere: python3 scripts/validate_skill.py
Exits 1 and lists the problems if anything is wrong.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Folders packed into the downloadable skill zip (keep in sync with SKILL_FOLDERS in scripts/build_site.py).
SKILL_FOLDERS = {"tokens", "docs", "components", "android", "templates"}
# Markdown files whose references are checked.
CHECKED = ["SKILL.md", "README.md", *sorted(str(p.relative_to(ROOT)) for p in (ROOT / "docs").glob("*.md")),
           *sorted(str(p.relative_to(ROOT)) for p in (ROOT / "templates").glob("*.md"))]

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
CODE_PATH_RE = re.compile(r"`((?:docs|tokens|components|android|templates|scripts|examples|assets)/[^`\s]+)`")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
MAX_DESCRIPTION = 1024
MAX_SKILL_LINES = 500


def frontmatter(text: str) -> tuple[dict[str, str], str] | None:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    meta = {}
    for line in m.group(1).splitlines():
        if line[:1].isspace():  # nested keys (metadata:) are not checked
            continue
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip().strip('"')
    return meta, text[m.end():]


def check_skill(errors: list[str]) -> None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    parsed = frontmatter(text)
    if parsed is None:
        errors.append("SKILL.md: must start with --- frontmatter ---")
        return
    meta, _ = parsed
    name, desc = meta.get("name", ""), meta.get("description", "")
    if not NAME_RE.fullmatch(name):
        errors.append(f"SKILL.md: name '{name}' must be lowercase words joined by single hyphens")
    if not desc:
        errors.append("SKILL.md: description is missing")
    elif len(desc) > MAX_DESCRIPTION:
        errors.append(f"SKILL.md: description is {len(desc)} characters (max {MAX_DESCRIPTION})")
    if "<" in desc or ">" in desc:
        errors.append("SKILL.md: description must not contain angle brackets")
    for key in ("license",):
        if key not in meta:
            errors.append(f"SKILL.md: frontmatter is missing '{key}'")
    lines = text.count("\n") + 1
    if lines > MAX_SKILL_LINES:
        errors.append(f"SKILL.md: {lines} lines (keep it under {MAX_SKILL_LINES}; move detail into docs/)")


def check_references(errors: list[str]) -> None:
    for rel in CHECKED:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        refs = set(CODE_PATH_RE.findall(text))
        for link in LINK_RE.findall(text):
            if re.match(r"[a-z]+:", link) or link.startswith("#"):
                continue
            target = (path.parent / link.split("#")[0]).resolve()
            refs.add(str(target.relative_to(ROOT)) if target.is_relative_to(ROOT) else link)
        for ref in sorted(refs):
            if "<" in ref or "*" in ref:  # placeholders like components/<Name>/README.md
                continue
            if not (ROOT / ref.rstrip("/")).exists():
                errors.append(f"{rel}: points to '{ref}', which does not exist")
            elif rel == "SKILL.md" and ref.split("/")[0] not in SKILL_FOLDERS:
                errors.append(f"SKILL.md: points to '{ref}', which is not packed into the skill zip")


def main() -> int:
    errors: list[str] = []
    check_skill(errors)
    check_references(errors)
    if errors:
        print("Skill validation failed:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"Skill is valid ({len(CHECKED)} Markdown files checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
