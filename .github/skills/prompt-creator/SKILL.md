---
name: prompt-creator
description: VS Code の prompt files（slash commands / スラッシュコマンド）を設計・作成・レビューする。.prompt.md、.github/prompts、prompt file、slash command、/コマンドに言及したとき、または定型タスクを「/で呼び出せる形」にしたいときに使用する。
---

# Prompt Files（Slash Commands）作成スキル（VS Code / GitHub Copilot）

このSkillは、VS Code の **prompt files**（`.prompt.md`）を、再利用可能なスラッシュコマンドとして設計し、ワークスペースへ追加する。

## まず決める（最小）

- **目的**: 1回の実行で完結する、繰り返しタスクにする（例: 雛形生成、レビュー、要約、チェックリスト適用）
- **入力**: チャット入力の追加文 / `${selection}` / `${file}` / `${input:...}` のどれを使うか
- **出力**: 期待する形式（箇条書き、差分、ファイル作成、コマンド列など）を明記する

**使い分け（重要）**
- prompt files: **単発で繰り返す作業**を `/` で呼び出す
- custom agents: **継続的な人格/役割**や、複数ツールを使った長いワークフロー向け

## 作成フロー

### 1) 置き場所を選ぶ

ワークスペース内の標準配置は次の通り:

- `.github/prompts/`（ワークスペース限定）

補足: 個人用に複数ワークスペースで再利用する場合は、VS Code のユーザーデータ配下に保存できる。追加の配置場所は `chat.promptFilesLocations` 設定で増やせる。モノレポで親リポジトリ側の prompt files も拾いたい場合は `chat.useCustomizationsInParentRepositories` を確認する。

### 2) ファイル名（= 既定の / コマンド名）を決める

- 迷ったら `kebab-case` を使う（例: `review-pr.prompt.md`）
- YAML の `name` を省略すると **ファイル名が / 名**として使われる

### 3) YAML frontmatter を書く（必要最小限）

最低限は `description` だけでもよい。

- `name`: `/` メニューで使う表示名。省略時はファイル名
- `description`: 何をする prompt か
- `argument-hint`: 入力欄に表示するヒント（例: `topic=... output=...`）
- `agent`: 実行するエージェント（`ask` / `agent` / `plan` / custom agent 名。未指定なら現在のエージェント）
- `tools`: 使えるツールのリスト（指定すると tool 制約がかかる）
- `model`: 使用モデル（未指定なら model picker の選択）

`tools` だけ指定して `agent` を省略した場合、既定の agent は `agent` になる。

ツールの優先順位（競合時）:
1. prompt file の `tools`
2. prompt file が参照する custom agent の `tools`
3. 現在選択中エージェントの既定ツール

### 4) 本文（プロンプト）を書く

- **指示は短く**、出力形式と手順を優先する
- 既存の規約は `.github/copilot-instructions.md` や `.instructions.md` に寄せ、prompt file では **そのタスク固有**に集中する
- 他ファイルを参照したい場合は、prompt file から **相対パス**の Markdown リンクで参照する

### 5) ツールと変数を活用する

- 変数: `${selection}` / `${fileBasename}` / `${workspaceFolder}` / `${input:name}` など
- ツール参照: `#tool:<tool-name>`（本文中で明示したい場合）
- 追加入力を集めたい場合は `vscode/askQuestions` ツールや `${input:name:placeholder}` を使う

### 6) テストとデバッグ

- prompt file をエディタで開き、右上の実行（再生）でテストする
- Chat で `/` を入力して候補に出るか確認する
- `/prompts` や Chat Customizations editor（Preview）から一覧・新規作成・編集を確認する
- `/create-prompt` を使うと初期ドラフトを生成できる
- 期待通りに適用されない場合は Chat の Diagnostics（Configure Chat → Diagnostics）で読み込み状況とエラーを見る

## 期待する出力

- `.github/prompts/<name>.prompt.md` の新規作成、または既存 prompt file の改善
- 変更時は「何をどう変えたか（入力/出力/ツール/安全性）」を短く添える

## テンプレとチェックリスト

- すぐ使える雛形: [references/TEMPLATES.md](references/TEMPLATES.md)

## 参照

- https://code.visualstudio.com/docs/copilot/customization/overview
- https://code.visualstudio.com/docs/copilot/customization/prompt-files
