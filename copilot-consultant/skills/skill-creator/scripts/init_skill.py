#!/usr/bin/env python3
"""Skill Initializer - Creates a new Agent Skill directory skeleton.

This script is intentionally dependency-free (stdlib only) to keep it portable.
It generates a minimal, spec-friendly SKILL.md plus optional resource folders.

Usage:
  python scripts/init_skill.py <skill-name> --path <output-directory>

Examples:
  python scripts/init_skill.py webapp-testing --path .github/skills
  python scripts/init_skill.py data-analysis --path .github/skills
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_skill_name(name: str) -> None:
    if not (1 <= len(name) <= 64):
        raise ValueError("name must be 1-64 characters")
    if not _NAME_RE.match(name):
        raise ValueError("name must be lowercase alphanumerics with single hyphens (kebab-case)")
    if name.startswith("-") or name.endswith("-"):
        raise ValueError("name must not start or end with '-' ")
    if "--" in name:
        raise ValueError("name must not contain consecutive hyphens ('--')")


def title_case_skill_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def render_skill_md(skill_name: str) -> str:
    skill_title = title_case_skill_name(skill_name)
    return (
        "---\n"
        f"name: {skill_name}\n"
        "description: [TODO: このSkillが何をするか／いつ使うか（トリガー状況・キーワード・拡張子・タスク例）を1行で具体的に記述する]\n"
        "---\n\n"
        f"# {skill_title}\n\n"
        "## 概要\n"
        "[TODO: このSkillが提供する能力を1〜2文で書く]\n\n"
        "## 進め方（推奨）\n"
        "1. 具体的な利用例（ユーザーが言いそうな依頼）を3つ書く\n"
        "2. その例を繰り返し実行するために必要な手順・判断・出力を箇条書きにする\n"
        "3. 決定性が必要なら scripts/ にスクリプトを追加する\n"
        "4. 詳細仕様や大量の例は references/ に分割する\n\n"
        "## 手順\n"
        "[TODO: ステップバイステップの手順を命令形で書く]\n\n"
        "## 例\n"
        "- 例1: [入力] → [期待出力]\n"
        "- 例2: [入力] → [期待出力]\n\n"
        "## リソース\n"
        "- 参照: references/\n"
        "- スクリプト: scripts/\n"
        "- アセット: assets/\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a new Agent Skill directory")
    parser.add_argument("skill_name", help="Skill name (kebab-case, must match directory name)")
    parser.add_argument("--path", required=True, help="Output directory (skill folder will be created inside)")
    parser.add_argument(
        "--with-resources",
        action="store_true",
        help="Create scripts/, references/, and assets/ directories",
    )
    args = parser.parse_args()

    skill_name = args.skill_name.strip()
    validate_skill_name(skill_name)

    output_root = Path(args.path).expanduser().resolve()
    if not output_root.exists():
        raise SystemExit(f"output directory does not exist: {output_root}")
    if not output_root.is_dir():
        raise SystemExit(f"output path is not a directory: {output_root}")

    skill_dir = output_root / skill_name
    if skill_dir.exists():
        raise SystemExit(f"skill directory already exists: {skill_dir}")

    skill_dir.mkdir(parents=True, exist_ok=False)

    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(render_skill_md(skill_name), encoding="utf-8")

    if args.with_resources:
        (skill_dir / "scripts").mkdir(exist_ok=True)
        (skill_dir / "references").mkdir(exist_ok=True)
        (skill_dir / "assets").mkdir(exist_ok=True)

    print(f"✅ Created skill: {skill_dir}")
    print("Next steps:")
    print("1) Edit SKILL.md (especially description)")
    print("2) Add resources (scripts/references/assets) only if needed")
    print("3) Run scripts/validate_skill.py to sanity-check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
