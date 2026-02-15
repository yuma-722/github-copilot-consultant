#!/usr/bin/env python3
"""Quick Skill Validator - Sanity-checks a skill folder.

This is a lightweight validator intended for fast feedback.
It intentionally supports only a conservative subset of YAML frontmatter:
- `name: ...`
- `description: ...` (single-line scalar; VS Code 互換のため改行やブロックスカラーは不可)

For full spec validation, use an Agent Skills spec validator (e.g. skills-ref)
when available.

Usage:
  python scripts/validate_skill.py <path/to/skill-folder>

Example:
  python scripts/validate_skill.py .github/skills/my-skill
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_skill_name(name: str) -> str | None:
    name = name.strip()
    if not name:
        return "name is empty"
    if len(name) > 64:
        return "name must be <= 64 characters"
    if name.startswith("-") or name.endswith("-"):
        return "name must not start or end with '-'"
    if "--" in name:
        return "name must not contain consecutive hyphens ('--')"
    if not _NAME_RE.match(name):
        return "name must be lowercase alphanumerics with single hyphens (kebab-case)"
    return None


def extract_frontmatter(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    return text[4:end]


def parse_frontmatter(frontmatter: str) -> dict[str, str]:
    """Parse a minimal YAML frontmatter subset."""
    result: dict[str, str] = {}
    lines = frontmatter.splitlines()

    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue

        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            i += 1
            continue

        key = m.group(1)
        value = m.group(2)

        # block scalar
        if value in (">-", "|", ">", "|-"):
            block_lines: list[str] = []
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if re.match(r"^[A-Za-z0-9_-]+:\s*", nxt):
                    break
                # YAML indentation for block content is typically 2 spaces
                block_lines.append(nxt[2:] if nxt.startswith("  ") else nxt)
                i += 1
            result[key] = "\n".join(block_lines).strip("\n")
            continue

        result[key] = value.strip().strip('"').strip("'")
        i += 1

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Quick validate an Agent Skill folder")
    parser.add_argument("skill_path", help="Path to skill folder containing SKILL.md")
    args = parser.parse_args()

    skill_dir = Path(args.skill_path).expanduser().resolve()
    if not skill_dir.exists() or not skill_dir.is_dir():
        print(f"❌ Not a directory: {skill_dir}")
        return 1

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print("❌ SKILL.md not found")
        return 1

    content = skill_md.read_text(encoding="utf-8")
    frontmatter_text = extract_frontmatter(content)
    if frontmatter_text is None:
        print("❌ YAML frontmatter not found or malformed (must start with '---' and contain closing '---')")
        return 1

    # VS Code 互換: description のブロックスカラー（>-, | 等）はエラーになることがあるため禁止する
    if re.search(r"(?m)^description:\s*(>[>-]?|\|[+-]?)\s*$", frontmatter_text):
        print("❌ description must be a single-line scalar for VS Code (do not use block scalars like 'description: >-' or 'description: |')")
        return 1

    fm = parse_frontmatter(frontmatter_text)

    name = fm.get("name", "")
    desc = fm.get("description", "")

    if not name:
        print("❌ Missing required frontmatter: name")
        return 1
    if not desc:
        print("❌ Missing required frontmatter: description")
        return 1

    err = validate_skill_name(name)
    if err:
        print(f"❌ Invalid name: {err} (name={name!r})")
        return 1

    # Parent directory must match name
    if skill_dir.name != name:
        print(f"❌ Directory name must match frontmatter name: dir={skill_dir.name!r} name={name!r}")
        return 1

    if len(desc) > 1024:
        print("❌ description must be <= 1024 characters")
        return 1

    if "\n" in desc or "\r" in desc:
        print("❌ description must be single-line (no newlines) for VS Code")
        return 1

    print("✅ OK")
    print(f"- name: {name}")
    print(f"- description length: {len(desc)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
