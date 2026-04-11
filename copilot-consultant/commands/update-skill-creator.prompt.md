---
description: skill-creator（Agent Skills作成支援Skill）を日本語で改善・更新する
---

# 目的

このリポジトリの `.github/skills/skill-creator/` を、Agent Skills のオープン標準仕様とベストプラクティスに沿って日本語で更新し、必要なら補助ファイルやスクリプトも追加して、再利用しやすい「Skill作成支援Skill」にする。

# 参照（必ず読む/比較する）

- Anthropic: Skill authoring best practices
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- VS Code: Agent Skills
  - https://code.visualstudio.com/docs/copilot/customization/agent-skills
- Agent Skills（agentskills.io）
  - https://agentskills.io/home
  - https://agentskills.io/specification
- 比較対象（Anthropicの skill-creator）
  - https://github.com/anthropics/skills/tree/main/skills/skill-creator

# 前提

- 変更対象は `.github/skills/skill-creator/` 以下。
- `SKILL.md` はフロントマター + 本文（Markdown）。
- プログレッシブ・ディスクロージャーを尊重し、`SKILL.md` 本文は簡潔に（500行以下目安）。
- 不要な補助ドキュメント（README、CHANGELOG等）を増やさない。Skillが仕事をするために必要なものだけを同梱する。

# 実施方針（このチャットで合意した方向性）

## 1) 発火（Skill選択）を最重要視する

- **`description` が発火の主導権を握る**。ここに「何をするか」と「いつ使うか（トリガー）」を集約する。
- 本文の「When to use」節は発火には効かない（本文は有効化後にロードされる）ので、発火に必要な情報は `description` に書く。

## 2) 簡潔さ優先（説明より手順と例）

- モデルは賢い前提で、既知の一般論を繰り返さない。
- 冗長な説明より、短い手順と具体例を優先する。
- 同じ情報を `SKILL.md` と参照ファイルに二重に置かない（重複禁止）。

## 3) 自由度の設計

- タスクの壊れやすさに応じて、高/中/低自由度（テキスト/疑似コード/厳密コマンド）を選ぶ。

## 4) 具体例→再利用資産の発想

- Skillを作る前に「ユーザーが言いそうな依頼」を具体例として集める。
- その具体例を何度も実行するために必要な再利用資産（scripts/references/assets）を洗い出して同梱する。

## 5) VS Code固有拡張の扱い

- VS Code は `argument-hint` / `user-invocable` / `disable-model-invocation` などを使える。
- ただし **agentskills.io の標準バリデータでは弾かれる可能性**があるため、ポータビリティ重視なら標準フィールド中心にする。

# 作業手順

1. 現状の `.github/skills/skill-creator/SKILL.md` を読み、内容が薄い場合は日本語で拡充する。
2. agentskills.io の仕様に沿って、フロントマターの `name` / `description` を点検する（`name` はディレクトリ名と一致、kebab-case）。
3. `SKILL.md` 本文を以下の要素で構成する:
   - Skillの目的（1〜2文）
   - 5ステップ程度の作成ワークフロー（チェックリスト形式）
   - 「具体例から要件を固める」ガイダンス
   - 「descriptionにトリガー集約」注意点
   - プログレッシブ・ディスクロージャーの設計指針（参照は1階層まで）
   - 参照ファイルへのリンク
4. 参照ファイルを `references/` に作る（必要に応じて増やすが増やしすぎない）:
   - `references/FRONTMATTER.md`: フロントマターのリファレンス（標準＋VS Code拡張の注意点）
   - `references/PATTERNS.md`: テンプレート、入出力例、条件分岐ワークフロー等
   - `references/CHECKLIST.md`: 品質チェック項目（不要ファイルを増やさない、参照1階層、用語統一など）
5. （任意だが推奨）再現性向上のためにスクリプトを追加する:
   - `scripts/init_skill.py`: Skill雛形生成（stdlibのみ、依存なし）
   - `scripts/validate_skill.py`: `SKILL.md` の簡易検証（name/description/ディレクトリ一致など）
6. `scripts/validate_skill.py .github/skills/skill-creator` を実行して `✅ OK` を確認する。

# 受け入れ条件（Doneの定義）

- `.github/skills/skill-creator/SKILL.md` が日本語で、作成ワークフローとベストプラクティスを簡潔に説明している。
- `description` が具体的で「何をするか＋いつ使うか（トリガー）」を含む。
- 参照ファイルは `SKILL.md` から直接リンクされ、参照の深いネストがない。
- 余計なドキュメントを増やしていない（Skill実行に不要なREADME等を作らない）。
- （追加した場合）スクリプトが動作し、最低限の検証が通る。

# 追加メモ（任意）

- アンチパターン節は、書く場合は **参照ファイル側** に置き、量を絞る（最重要点のみ）ことでトークン消費を抑える。
