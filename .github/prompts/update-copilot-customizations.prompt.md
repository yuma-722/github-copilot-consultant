---
description: GitHub Copilot（VS Code）のカスタマイズ資産（instructions / prompts / agents / skills / hooks）を公式ドキュメントの最新情報に合わせて点検・最小差分で更新する
argument-hint: 対象（例: skills/custom-agents-creator のみ or .github 全体）/完了条件（例: outdated な説明の修正のみ）/制約（例: 新規ファイル追加なし）
tools: [vscode, execute, read, agent, edit, search, web, todo]
---

# 目的

このリポジトリの Copilot カスタマイズ資産（`.github/` 配下）を、**公式ドキュメントの最新情報**に基づいて棚卸しし、古くなった説明・フィールド名・推奨事項を **最小差分** で更新する。

対象:

- `.github/copilot-instructions.md`
- `.github/instructions/*.instructions.md`
- `.github/prompts/*.prompt.md`
- `.github/agents/*.agent.md`
- `.github/skills/*/SKILL.md`（必要なら `references/` まで）
- `.github/hooks/*.json`

# 参照（必ず fetch で確認）

VS Code（Copilot customization）:

- https://code.visualstudio.com/docs/copilot/customization/overview
- https://code.visualstudio.com/docs/copilot/customization/custom-instructions
- https://code.visualstudio.com/docs/copilot/customization/prompt-files
- https://code.visualstudio.com/docs/copilot/customization/custom-agents
- https://code.visualstudio.com/docs/copilot/customization/agent-skills
- https://code.visualstudio.com/docs/copilot/customization/hooks

VS Code（agents / subagents）:

- https://code.visualstudio.com/docs/copilot/agents/subagents

必要に応じて（仕様/互換性の把握）:

- https://agentskills.io/specification

# 制約

- 変更は「最新化」目的に限定し、UX/機能の追加はしない（ドキュメント・テンプレ・説明の更新が主）。
- 既存の方針（`.github/copilot-instructions.md`）と矛盾させない。
- このリポジトリは日本語運用のため、**生成・更新する文書は日本語**にする。
- 迷う場合は保守的に（VS Code が未対応でも壊れないように、核となる `name/description/tools` で成立する構成を優先）。

# 手順

## 1) 現状把握（読む）

- `.github/` 配下の対象ファイルを読み、カスタマイズ資産の一覧を作る（ファイルパス単位）。
- 各ファイルについて「何を保証/説明しているか」を 1〜2 行で要約する。

## 2) 公式ドキュメント確認（fetch）

- 上記 URL を `fetch` で読み、次を抽出する:
  - フィールド名（frontmatter）の正式名称と意味
  - deprecated / renamed / experimental の注意点
  - 既定値（例: `agents: '*'` のような既定挙動）
  - 記載されているベストプラクティス（最小権限、Diagnostics など）

## 3) 差分の棚卸し（ギャップ分析）

各ファイルを「現状」と「最新ドキュメント」で比較して、ギャップを分類する:

- **誤り**: 説明が事実と違う、古いフィールド名のまま、誤解を招く
- **不足**: 重要な注意点が欠けている（例: `agents` と subagents の関係、`infer` の扱い）
- **過剰**: 仕様にない独自ルールが膨らんでいる、重複が多い

## 4) 更新方針（最小差分）

- まずは references や本文の説明を更新し、構造変更は必要な場合だけに限定する。
- テンプレ追加が必要でも、既存ファイルを増やしすぎない。

## 5) 更新を適用（edit）

- 変更対象ファイルを明示してから編集する。
- 1ファイルにつき、変更理由を 1 行で残せる程度の差分にする（大改造しない）。

## 6) 仕上げ

- 「何を更新したか」を箇条書きでまとめる。
- VS Code Chat の Diagnostics で読み込み確認する手順を短く案内する。

# チェックリスト（Done）

- 公式ドキュメントの記述に反する説明が残っていない
- `deprecated` / `experimental` の注意点が必要箇所にだけ入っている
- 変更が過剰になっていない（必要最小限の更新）
- 日本語で一貫している
