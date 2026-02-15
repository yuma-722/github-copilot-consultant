# Custom Agents 要点（VS Code / GitHub Copilot 共通の考え方）

このドキュメントは、Custom Agent（`.agent.md`）を作るときの要点を、環境差分に深入りせず「困らない範囲」でまとめる。

## 置き場所（VS Code）

- ワークスペース共有: `.github/agents/*.agent.md`
- ユーザープロファイル: プロファイル配下（複数ワークスペースで再利用）
- 追加ロケーション: `chat.agentFilesLocations` で検索場所を増やせる

## `.agent.md` の基本

- Markdownファイル + YAML frontmatter + 本文（指示）
- frontmatter は主に以下を使う（未対応のものは無視されても致命傷にならない設計にする）

### よく使う frontmatter

- `name`: 表示名（省略時はファイル名）
- `description`: 目的/役割
- `argument-hint`: 入力のヒント（VS Code向け）
- `tools`: 利用可能ツールの絞り込み（存在しないツール名は無視される）
- `agents`: subagentとして使ってよいエージェントの許可リスト（`*` / `[]` / 名前配列）
- `model`: 使うモデル（環境により未サポートのことがある）
- `user-invocable`: UIのエージェント一覧に出すか（既定 `true`）
- `disable-model-invocation`: 他エージェントから subagent として呼ばれるのを禁止（既定 `false`）
- `handoffs`: 次のエージェントへ移るボタン（段階ワークフロー）

## subagents（サブエージェント）と `agents` の意味

### subagent とは

subagent は「メインの会話（メインエージェント）が、小タスクを **別コンテキスト** で実行させる委譲先」のこと。

- 既定では、subagent は“現在のメインエージェント”と同じモデル/ツールで実行される
- **Custom Agent を subagent として実行** すると、その Custom Agent 側の `tools`/`model`/本文指示が適用される（この機能はドキュメント上 Experimental 扱いの記載がある）

### `agents`（frontmatter）の役割

`agents` は「この Custom Agent が subagent として **呼び出してよい Custom Agents の許可リスト**」を指定する。

- `agents: '*'` : すべて許可（既定の挙動）
- `agents: []` : subagent の使用を禁止
- `agents: ['Planner', 'Reviewer']` : 指定した名前だけ許可

注意:

- `agents` を指定して subagent を使うなら、`tools` に `agent` を含める（例: `tools: ['agent', 'read', 'search']`）
- 明示的に `agents` に列挙した場合、`disable-model-invocation: true` を上書きして呼べてしまう（= 許可リストが優先される）
- `agents` に書く名前は Custom Agent の `name`（またはファイル名由来の表示名）でマッチするため、リネーム時はリストも更新する

最小例:

```yaml
---
name: Feature Builder
tools: ['agent', 'read', 'search', 'edit']
agents: ['Planner', 'Implementer', 'Reviewer']
---
```

## ベストプラクティス

- 最小権限: `tools` を目的に合わせて削る
- 役割を小さく: 1つのエージェントに詰め込みすぎない
- Handoffsで段階化: 計画→実装→レビューのように合意点を作る
- 読み込まれているか確認: VS Codeの Chat Diagnostics で検証する

## 互換メモ（短縮版）

- 実行環境によって、`model` / `argument-hint` / `handoffs` 等が無視される場合がある。
- そのため、まずは `name` / `description` / `tools` と本文指示で成立するエージェントを作り、必要に応じて追加項目を使う。
