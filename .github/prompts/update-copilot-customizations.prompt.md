---
description: 'GitHub Copilot（VS Code）のカスタマイズ資産（instructions / prompts / agents / skills / hooks）を公式ドキュメントの最新情報に合わせて点検・最小差分で更新する'
argument-hint: '対象（例: skills/custom-agents-creator のみ or .github 全体）/完了条件（例: outdated な説明の修正のみ）/制約（例: 新規ファイル追加なし）'
tools: [vscode, execute, read, agent, edit, search, web, browser, azure-mcp/search, ms-vscode.vscode-websearchforcopilot/websearch, todo]
---

# 目的

このリポジトリの Copilot カスタマイズ資産（`.github/` 配下）を、**公式ドキュメントの最新情報**に基づいて棚卸しし、古くなった説明・フィールド名・推奨事項を **最小差分** で更新する。

**更新戦略**: Skills（知識ベース）を先に最新化し、更新済み Skills の知識を使って各カスタマイズファイルを更新する。

# 対象

## Skills（Phase 1 で先に最新化）

- `.github/skills/custom-agents-creator/`（SKILL.md + references/）
- `.github/skills/custom-instructions-creator/`（SKILL.md）
- `.github/skills/hooks-creator/`（SKILL.md + references/）
- `.github/skills/prompt-creator/`（SKILL.md + references/）
- `.github/skills/skill-creator/`（SKILL.md + references/）

## カスタマイズファイル（Phase 2 で Skills を使って更新）

- `.github/copilot-instructions.md`
- `.github/instructions/*.instructions.md`
- `.github/prompts/*.prompt.md`
- `.github/agents/*.agent.md`
- `.github/hooks/*.json`
- `.github/skills/*/SKILL.md`（必要なら `references/` まで）

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

## Phase 1: Skills の最新化（知識ベースの更新）

Skills が各カスタマイズ機能の「正」の知識源となるため、先に最新化する。

### 1-1) 公式ドキュメント確認（fetch）

上記 URL を fetch で読み、Skill ごとに以下を抽出する:

- フィールド名（frontmatter）の正式名称と意味
- deprecated / renamed / experimental の注意点
- 既定値（例: `agents: '*'` のような既定挙動）
- ベストプラクティス（最小権限、Diagnostics など）

### 1-2) Skill ごとのギャップ分析

各 Skill の SKILL.md と references/ を公式ドキュメントと比較し、ギャップを分類する。

| Skill | 対応する公式ドキュメント |
|---|---|
| custom-agents-creator | custom-agents, subagents |
| custom-instructions-creator | custom-instructions, overview |
| hooks-creator | hooks |
| prompt-creator | prompt-files |
| skill-creator | agent-skills, agentskills.io/specification |

ギャップの分類:

- **誤り**: 事実と異なる説明、古いフィールド名
- **不足**: 重要な仕様・注意点の欠落
- **過剰**: 仕様にない独自ルール、重複

### 1-3) Skills の更新（edit）

- SKILL.md の説明・手順・参照情報を最新化する。
- references/ 内のリファレンスファイルを更新する（テンプレート、フィールド定義、イベント一覧など）。
- 変更は最小差分に留める（構造変更は必要な場合のみ）。

## Phase 2: カスタマイズ資産の更新（Copilot Custom Worker で並列実行）

Phase 1 で最新化した Skills の知識を基準に、既存のカスタマイズファイルを点検・更新する。
更新作業はサブエージェント **Copilot Custom Worker** にカスタマイズ種別ごとに並列で委任する。

### 2-1) 現状把握（読む）

- `.github/` 配下のカスタマイズファイルを読み、資産一覧を作る（ファイルパス単位）。
- 各ファイルについて「何を保証/説明しているか」を 1〜2 行で要約する。

### 2-2) ギャップ分析（Skills の知識 vs 現状）

各カスタマイズファイルを、対応する Skill の最新知識と比較して、ギャップを分類する:

- **誤り**: Skill の最新情報と矛盾する記述
- **不足**: Skill に記載があるが反映されていない重要事項
- **過剰**: 不要な記述や重複

### 2-3) Copilot Custom Worker に並列で更新を委任

ギャップ分析の結果を基に、カスタマイズ種別ごとに **Copilot Custom Worker** を並列で呼び出す。

各サブエージェントへの依頼に含める情報:

- **合意状況**: 合意済み（本プロンプトで事前合意）
- **変更内容**: 2-2 のギャップ分析結果（誤り・不足・過剰の一覧）
- **対象ファイル**: 変更が必要なファイルパス一覧
- **参照 Skill**: 対応する更新済み Skill（最新知識の基準）
- **制約**: 最小差分、日本語、大改造しない

並列呼び出しの分割単位（独立性がある単位で分割）:

| サブエージェント呼び出し | 対象ファイル | 参照 Skill |
|---|---|---|
| #1 instructions | `copilot-instructions.md`, `instructions/*.instructions.md` | custom-instructions-creator |
| #2 prompts | `prompts/*.prompt.md` | prompt-creator |
| #3 agents | `agents/*.agent.md` | custom-agents-creator |
| #4 hooks | `hooks/*.json` | hooks-creator |
| #5 skills | `skills/*/SKILL.md`（必要なら `references/`） | skill-creator |

> **注意**: 変更が不要な種別はスキップする（ギャップがない場合は呼び出さない）。

## 仕上げ

- Phase 1・Phase 2 それぞれで「何を更新したか」を箇条書きでまとめる。
- VS Code Chat の Diagnostics で読み込み確認する手順を短く案内する。

# チェックリスト（Done）

- Skills の SKILL.md と references/ が公式ドキュメントの最新情報を反映している
- カスタマイズファイルが更新済み Skills の知識と矛盾していない
- `deprecated` / `experimental` の注意点が必要箇所にだけ入っている
- 変更が過剰になっていない（必要最小限の更新）
- 日本語で一貫している
