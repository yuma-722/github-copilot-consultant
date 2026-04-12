---
name: plugin-creator
description: ワークスペースの既存カスタマイズ（skills / agents / prompts / hooks / MCP servers）をスキャンし、ユーザーが選択したものを Agent Plugin としてパッケージングする。plugin、プラグイン作成、カスタマイズのバンドル、Plugin パッケージ、配布可能なカスタマイズ、agent plugin、copilot plugin に言及したときに使用する
---

# Agent Plugin 作成ガイド

ワークスペースの既存 Copilot カスタマイズを Agent Plugin としてパッケージし、マーケットプレイスやローカルインストールで配布可能にする。

## Plugin とは

Agent Plugin は、skills / agents / slash commands / hooks / MCP servers を1つのバンドルとしてまとめ、インストール可能にしたものである。VS Code（Preview 機能、`chat.plugins.enabled` が必要）および Copilot CLI の両方で利用できる。

## 作成ワークフロー

```
作成チェックリスト:
- [ ] Step 1: ワークスペースのカスタマイズをスキャンする
- [ ] Step 2: Pluginに含めるカスタマイズをヒアリングする
- [ ] Step 3: Pluginメタデータを収集する
- [ ] Step 4: Pluginディレクトリを生成する
- [ ] Step 5: 検証とドキュメント生成
```

### Step 1: ワークスペースのカスタマイズをスキャン

以下のパスを走査し、既存カスタマイズの一覧を作成する:

| 種別 | 検索パス |
|------|----------|
| Skills | `.github/skills/*/SKILL.md` |
| Agents | `.github/agents/*.agent.md` |
| Prompts（Slash Commands） | `.github/prompts/*.prompt.md` |
| Hooks | `.github/hooks/*.json` |
| MCP Servers | `.mcp.json`、`mcp.json` |
| Instructions | `.github/instructions/*.instructions.md` |

**注意**: instructions は Plugin に直接バンドルできない。skills や agents の本文に含めるか、除外する。

### Step 2: ヒアリング（AskQuestions）

スキャン結果をもとに、`#askQuestions` ツールで以下を確認する:

```
質問1: どのカスタマイズをPluginに含めますか？
  → スキャン結果をオプションとして表示（multiSelect: true）

質問2: Plugin のフォーマットはどちらにしますか？
  → Copilot format（plugin.json をルートまたは .github/plugin/ に配置）← 推奨
  → Claude format（.claude-plugin/marketplace対応）
  → 両対応
```

**一度に質問しすぎない。** 最重要の2問から始め、追加は Step 3 で行う。

### Step 3: メタデータ収集（AskQuestions）

`#askQuestions` で Plugin メタデータを取得する:

```
質問: Plugin の基本情報を教えてください
  - Plugin名（kebab-case、最大64文字、例: my-awesome-plugin）
  - 説明文（何をするPluginか、最大1024文字）
  - バージョン（デフォルト: 1.0.0）
  - キーワード（カンマ区切り、任意）
  - カテゴリ（任意）
  - 作者名（メール・URL は任意）
  - ホームページURL（任意）
  - リポジトリURL（任意）
  - ライセンス（デフォルト: MIT）
```

### Step 4: Plugin ディレクトリ生成

選択されたカスタマイズと収集したメタデータをもとに、Plugin ディレクトリを生成する。

#### 出力先

Plugin はワークスペースルートの `plugins/<plugin-name>/` に生成する。

#### ディレクトリ構成

```
plugins/<plugin-name>/
├── plugin.json                  # Plugin マニフェスト（ルート配置推奨）
├── skills/
│   └── <skill-name>/
│       └── SKILL.md             # コピー元から複製
├── agents/
│   └── <agent-name>.agent.md    # コピー元から複製
├── commands/
│   └── <command-name>.md        # prompt files → commands
├── hooks.json                   # hooks設定の統合（該当時のみ）
├── scripts/
│   └── <script-files>           # hooksが参照するスクリプト
├── .mcp.json                    # MCP server定義（該当時のみ）
└── README.md                    # 自動生成ドキュメント
```

> **マニフェスト検索順**: `plugin.json`（ルート）が最も見つかりやすい。他に `.plugin/plugin.json`、`.github/plugin/plugin.json`、`.claude-plugin/plugin.json` も検出される。

#### plugin.json の生成

```json
{
  "name": "<plugin-name>",
  "description": "<description>",
  "version": "<version>",
  "keywords": ["<keyword1>", "<keyword2>"],
  "category": "<category>",
  "author": { "name": "<author>" },
  "homepage": "<homepage-url>",
  "repository": "<repository-url>",
  "license": "<license>",
  "agents": "agents/",
  "commands": ["./commands"],
  "skills": ["./skills/<skill-name>"],
  "hooks": "hooks.json",
  "mcpServers": ".mcp.json"
}
```

**生成ルール:**

- `agents`: `string | string[]` で指定。デフォルト `agents/` なので標準ディレクトリ名なら省略可能
- `skills`: `string | string[]` で指定。デフォルト `skills/` なので標準ディレクトリ名なら省略可能
- `commands`: `string | string[]` で指定。Plugin インストール後は `/<plugin-name>:<command-name>` で呼び出せる
- `hooks`: `string | object` で指定。外部ファイルパス（例: `"hooks.json"`）またはインラインオブジェクト
- `mcpServers`: `string | object` で指定。外部ファイルパス（例: `".mcp.json"`）またはインラインオブジェクト
- `category`, `tags`, `homepage` は任意だが、マーケットプレイスでの発見性向上に有効

#### Prompt → Command の変換

ワークスペースの prompt files（`.prompt.md`）は、Plugin では commands として扱われる。配置先を変更する:

```
元: .github/prompts/my-command.prompt.md
先: plugins/<plugin-name>/commands/my-command.md
```

フロントマターの `description` は維持する。`tools` や `agents` は Plugin コンテキストに合わせて調整する。

#### Hooks のパス解決

Plugin 内の hooks は `${CLAUDE_PLUGIN_ROOT}` トークンを使ってスクリプトを参照する。hooks は外部ファイルとして配置するか、plugin.json にインラインで定義できる:

**外部ファイル（hooks.json）:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
      }
    ]
  }
}
```

**plugin.json にインライン定義する場合:**

```json
"hooks": {
  "PostToolUse": [
    {
      "type": "command",
      "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
    }
  ]
}
```

ワークスペース内の相対パスを `${CLAUDE_PLUGIN_ROOT}` ベースのパスに書き換える。

#### MCP Servers のパス解決

`.mcp.json` 内のパスも `${CLAUDE_PLUGIN_ROOT}` トークンで書き換える。MCP servers も外部ファイルまたは plugin.json インライン定義が可能:

**外部ファイル（.mcp.json）:**

```json
{
  "mcpServers": {
    "my-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/my-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  }
}
```

**plugin.json にインライン定義する場合:**

```json
"mcpServers": {
  "my-server": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/my-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
  }
}
```

### Step 5: 検証とドキュメント

#### 構造検証チェック

- [ ] `plugin.json` に `name`（必須）が存在し、`description`・`version` が適切に設定されている
- [ ] `agents`、`commands`、`skills` のパスが plugin.json の指定（または デフォルト `agents/`、`skills/`）と一致している
- [ ] hooks 内のスクリプト参照が `${CLAUDE_PLUGIN_ROOT}` を使用している（外部ファイル・インライン共通）
- [ ] MCP server のパス参照が `${CLAUDE_PLUGIN_ROOT}` を使用している（外部ファイル・インライン共通）
- [ ] Skills の `SKILL.md` に `name` と `description` が存在する（`name` は重複判定に使われる）

#### README.md の自動生成

以下のテンプレートで README.md を生成する:

```markdown
# <Plugin名>

<description>

## インストール

### VS Code でのローカルインストール
VS Code の `chat.pluginLocations` 設定に追加:
{
  "<plugin-path>": true
}

### Copilot CLI でのインストール（Copilot CLI のみ）
copilot plugin install <plugin-name>@<marketplace>
copilot plugin install OWNER/REPO
copilot plugin install ./local-path

## 含まれるカスタマイズ

### Skills
| スキル名 | 説明 |
|----------|------|
| ... | ... |

### Agents
| エージェント名 | 説明 |
|----------------|------|
| ... | ... |

### Commands
| コマンド | 説明 |
|----------|------|
| ... | ... |

## ライセンス
<license>
```

## 注意事項

- VS Code では Preview 機能。`chat.plugins.enabled` 設定が必要。Copilot CLI でも利用可能
- Plugin 内の hooks と MCP servers はユーザーのマシンでコードを実行する。セキュリティレビューを行うこと
- instructions は Plugin にバンドルできない。スキルやエージェントの本文に組み込む
- `${CLAUDE_PLUGIN_ROOT}` は Copilot / Claude 両方で動作する
- 両フォーマット対応する場合は `.github/plugin/plugin.json` と `.claude-plugin/` の両方に配置する
- **ロード優先度**: Agents と Skills は **first-found-wins**（プロジェクト設定が Plugin より優先）。MCP Servers は **last-wins**（Plugin が既存設定を上書き可能）
- **重複判定**: Agents はファイル名由来の ID、Skills は `SKILL.md` 内の `name` フィールドで判定される
- `plugin.json` の `agents` と `skills` にはデフォルトパス（`agents/`、`skills/`）があるため、標準的なディレクトリ名を使えば明示的に指定不要

## 参照

- [PLUGIN-SPEC.md](references/PLUGIN-SPEC.md): plugin.json スキーマと両フォーマットの詳細
- [EXAMPLES.md](references/EXAMPLES.md): 実際の Plugin 構成例
