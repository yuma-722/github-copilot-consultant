# plugin.json スキーマリファレンス

## 必須フィールド

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `name` | string | Plugin の一意識別子。kebab-case、小文字英数字とハイフンのみ |
| `description` | string | Plugin の説明。何をするか、どんなワークフローをサポートするか |
| `version` | string | セマンティックバージョニング（例: `1.0.0`） |

## 任意フィールド

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `keywords` | string[] | 検索・分類用のキーワード |
| `author` | object | `{ "name": "Author Name" }` |
| `repository` | string | リポジトリURL |
| `license` | string | ライセンス識別子（例: `MIT`） |
| `agents` | string[] | Agent ファイル/ディレクトリへの相対パス |
| `commands` | string[] | Slash Command（prompt files）への相対パス |
| `skills` | string[] | Skill ディレクトリへの相対パス |

## Content フィールド詳細

### agents

`.agent.md` ファイルまたはそれを含むディレクトリを指定する。

```json
"agents": ["./agents"]
```

または個別指定:

```json
"agents": ["./agents/my-agent.agent.md"]
```

### commands

Plugin 内の slash commands。ワークスペースの prompt files に相当する。
Plugin インストール後は `/<plugin-name>:<command-name>` で呼び出せる。

```json
"commands": ["./commands/my-command.md"]
```

### skills

Skill ディレクトリ（`SKILL.md` を含むフォルダ）を指定する。

```json
"skills": ["./skills/my-skill"]
```

## Hooks（plugin.json 外）

Hooks は `plugin.json` 内で定義せず、別ファイルとして配置する。VS Code が自動検出する。

| Plugin フォーマット | Hooks ファイルパス |
|-------------------|------------------|
| Copilot | `hooks.json`（Plugin ルート） |
| Claude | `hooks/hooks.json` |

### Hooks 設定フォーマット

**フラット形式:**

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

**Matcher 形式（Claude 互換）:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
          }
        ]
      }
    ]
  }
}
```

**注意**: VS Code は `matcher` フィールドをパースするが、現在のところ値は無視される。

### サポートされるイベント

`SessionStart` / `UserPromptSubmit` / `PreToolUse` / `PostToolUse` / `PreCompact` / `SubagentStart` / `SubagentStop` / `Stop`

### パス参照トークン

`${CLAUDE_PLUGIN_ROOT}` を使用してPlugin内のファイルを参照する。VS Code がランタイムに絶対パスへ展開する。環境変数 `CLAUDE_PLUGIN_ROOT` もプロセスに注入される。

## MCP Servers（plugin.json 外）

`.mcp.json` を Plugin ルートに配置する。

```json
{
  "mcpServers": {
    "my-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/my-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    }
  }
}
```

**注意**: トップレベルキーは `mcpServers`（ワークスペース版の `servers` とは異なる）。

### `${CLAUDE_PLUGIN_ROOT}` が展開されるフィールド

`command` / `args` / `cwd` / `env` / `envFile` / `url` / `headers`

## Plugin フォーマットの比較

| 項目 | Copilot format | Claude format |
|------|---------------|---------------|
| メタデータ | `.github/plugin/plugin.json` | `.claude-plugin/plugin.json`（またはルートの `plugin.json`） |
| Hooks | `hooks.json`（ルート） | `hooks/hooks.json` |
| 自動検出 | VS Code が両フォーマットを自動検出 | VS Code が両フォーマットを自動検出 |

両対応する場合は、それぞれのパスに配置する（内容は同一でよい）。

## マーケットプレイス配布

### awesome-copilot / copilot-plugins への登録

`marketplace.json` にエントリを追加する:

```json
{
  "name": "my-plugin",
  "source": {
    "source": "github",
    "repo": "owner/repo"
  },
  "description": "Plugin の説明",
  "version": "1.0.0"
}
```

### ローカルインストール

```json
// settings.json
"chat.pluginLocations": {
  "/path/to/my-plugin": true
}
```

### ソースからインストール

コマンドパレット: `Chat: Install Plugin From Source` → Git リポジトリ URL を入力

### ワークスペース推奨

```json
{
  "enabledPlugins": {
    "my-plugin@marketplace-name": true
  },
  "extraKnownMarketplaces": {
    "my-marketplace": {
      "source": {
        "source": "github",
        "repo": "org/marketplace-repo"
      }
    }
  }
}
```
