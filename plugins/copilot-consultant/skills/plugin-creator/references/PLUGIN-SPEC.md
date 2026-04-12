# plugin.json スキーマリファレンス

## マニフェスト検索順

Plugin ディレクトリ内で以下の順にマニフェストファイルを検索し、最初に見つかったものが使用される:

1. `.plugin/plugin.json`
2. `plugin.json`（ルート）
3. `.github/plugin/plugin.json`
4. `.claude-plugin/plugin.json`

## 必須フィールド

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `name` | string | Plugin の一意識別子。kebab-case、小文字英数字とハイフンのみ。最大64文字 |

## 任意メタデータフィールド

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `description` | string | Plugin の説明。何をするか、どんなワークフローをサポートするか。最大1024文字 |
| `version` | string | セマンティックバージョニング（例: `1.0.0`） |
| `author` | object | `{ "name": "Author Name", "email": "optional", "url": "optional" }` |
| `homepage` | string | Plugin のホームページ URL |
| `repository` | string | リポジトリURL |
| `license` | string | ライセンス識別子（例: `MIT`） |
| `keywords` | string[] | 検索・分類用のキーワード |
| `category` | string | Plugin のカテゴリ |
| `tags` | string[] | 追加タグ（`keywords` とは別） |

## コンポーネントパスフィールド

Plugin の構成要素を指定する。すべて任意。省略時は CLI がデフォルト規約に従い自動検出する。

| フィールド | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| `agents` | string \| string[] | `agents/` | Agent ディレクトリ（`.agent.md` ファイル）へのパス |
| `skills` | string \| string[] | `skills/` | Skill ディレクトリ（`SKILL.md` ファイル）へのパス |
| `commands` | string \| string[] | — | Command ディレクトリへのパス |
| `hooks` | string \| object | — | Hooks 設定ファイルへのパス、またはインラインの hooks オブジェクト |
| `mcpServers` | string \| object | — | MCP 設定ファイルへのパス（例: `.mcp.json`）、またはインラインの server 定義 |
| `lspServers` | string \| object | — | LSP 設定ファイルへのパス、またはインラインの server 定義 (**Copilot CLI のみ**) |

> **注意**: `agents` と `skills` にはデフォルトパスがあるため、標準的なディレクトリ名を使う場合は明示的に指定しなくてもよい。

### agents

`.agent.md` ファイルまたはそれを含むディレクトリを指定する。文字列または配列のどちらでも可。

```json
"agents": "agents/"
```

```json
"agents": ["./agents", "./extra-agents"]
```

### commands

Plugin 内の slash commands。ワークスペースの prompt files に相当する。
Plugin インストール後は `/<plugin-name>:<command-name>` で呼び出せる。

```json
"commands": ["./commands/my-command.md"]
```

### skills

Skill ディレクトリ（`SKILL.md` を含むフォルダ）を指定する。文字列または配列のどちらでも可。

```json
"skills": "skills/"
```

```json
"skills": ["./skills/my-skill", "./extra-skills"]
```

### hooks（plugin.json 内でのインライン定義）

hooks 設定ファイルへのパスを文字列で指定するか、オブジェクトとしてインライン定義できる。

```json
"hooks": "hooks.json"
```

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

### mcpServers（plugin.json 内でのインライン定義）

MCP 設定ファイルへのパスを文字列で指定するか、オブジェクトとしてインライン定義できる。

```json
"mcpServers": ".mcp.json"
```

```json
"mcpServers": {
  "my-server": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/my-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
  }
}
```

## Hooks（外部ファイル配置）

hooks を plugin.json に含めず別ファイルとして配置することもできる。自動検出される。

| Hooks ファイルパス | 備考 |
|------------------|------|
| `hooks.json`（Plugin ルート） | |
| `hooks/hooks.json` | |

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

`${CLAUDE_PLUGIN_ROOT}` を使用してPlugin内のファイルを参照する。ランタイムに絶対パスへ展開される。環境変数 `CLAUDE_PLUGIN_ROOT` もプロセスに注入される。

### `${CLAUDE_PLUGIN_ROOT}` が展開されるフィールド

`command` / `args` / `cwd` / `env` / `envFile` / `url` / `headers`

## MCP Servers（外部ファイル配置）

`.mcp.json` を Plugin ルートに配置する。以下のパスが自動検出される:

- `.mcp.json`
- `.vscode/mcp.json`
- `.devcontainer/devcontainer.json`
- `.github/mcp.json`

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

## LSP Servers（Copilot CLI のみ）

> **注意**: LSP Servers は Copilot CLI でのみサポートされる。VS Code には独自の LSP 基盤があるため使用しない。

`lsp.json` または `.github/lsp.json` を Plugin ルートに配置するか、`plugin.json` でインライン定義する。

## Plugin フォーマットの比較

| 項目 | Copilot format | Claude format |
|------|---------------|---------------|
| メタデータ | `.github/plugin/plugin.json` | `.claude-plugin/plugin.json`（またはルートの `plugin.json`） |
| Hooks | `hooks.json`（ルート） | `hooks/hooks.json` |
| 自動検出 | 両フォーマットを自動検出 | 両フォーマットを自動検出 |

両対応する場合は、それぞれのパスに配置する（内容は同一でよい）。

## ロード順と優先度

複数のPlugin や プロジェクト設定にて同名のコンポーネントが存在する場合、以下の優先度ルールが適用される:

### Agents / Skills: first-found-wins（先に見つかったもの優先）

プロジェクトレベルの agent / skill と同名のものが Plugin にあった場合、Plugin 側は無視される。Plugin がプロジェクトの設定を上書きすることはない。

- Agents は **ファイル名から導出される ID**（例: `reviewer.agent.md` → ID: `reviewer`）で重複判定
- Skills は **`SKILL.md` 内の `name` フィールド**で重複判定

### MCP Servers: last-wins（後から読み込まれたもの優先）

同名の MCP server を定義する Plugin をインストールすると、Plugin の定義が優先される。

> **Copilot CLI のみ**: `--additional-mcp-config` フラグを使うと、Plugin よりもさらに高い優先度で MCP server を上書きできる。

### ビルトイン

ビルトインのツールとエージェントは常に存在し、ユーザー定義のコンポーネントで上書きできない。

## マーケットプレイス配布

### marketplace.json

Plugin マーケットプレイスは `marketplace.json` で定義する。配置場所の検索順:

1. `marketplace.json`（ルート）
2. `.plugin/marketplace.json`
3. `.github/plugin/marketplace.json`
4. `.claude-plugin/marketplace.json`

#### トップレベルフィールド

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `name` | string | Yes | kebab-case のマーケットプレイス名。最大64文字 |
| `owner` | object | Yes | `{ "name": "Org Name", "email": "optional" }` |
| `plugins` | array | Yes | Plugin エントリの配列（下記参照） |
| `metadata` | object | No | `{ "description": "説明", "version": "1.0.0", "pluginRoot": "path" }` |

#### Plugin エントリフィールド（plugins 配列内のオブジェクト）

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `name` | string | Yes | kebab-case の Plugin 名。最大64文字 |
| `source` | string \| object | Yes | 取得元（相対パス、GitHub、URL） |
| `description` | string | No | 説明。最大1024文字 |
| `version` | string | No | バージョン |
| `author` | object | No | `{ "name", "email?", "url?" }` |
| `homepage` | string | No | ホームページ URL |
| `repository` | string | No | リポジトリ URL |
| `license` | string | No | ライセンス識別子 |
| `keywords` | string[] | No | 検索キーワード |
| `category` | string | No | カテゴリ |
| `tags` | string[] | No | 追加タグ |
| `strict` | boolean | No | `true`（デフォルト）で厳密なスキーマ検証。`false` で緩い検証（直接インストールやレガシーPlugin 向け） |

コンポーネント指定フィールド（`agents`, `skills`, `commands`, `hooks`, `mcpServers`, `lspServers`）も Plugin エントリに含めることができる。

#### marketplace.json の例

```json
{
  "name": "my-marketplace",
  "owner": {
    "name": "Your Organization",
    "email": "plugins@example.com"
  },
  "metadata": {
    "description": "Curated plugins for our team",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "frontend-design",
      "description": "Create a professional-looking GUI ...",
      "version": "2.1.0",
      "source": "./plugins/frontend-design"
    },
    {
      "name": "security-checks",
      "description": "Check for potential security vulnerabilities ...",
      "version": "1.3.0",
      "source": "./plugins/security-checks"
    }
  ]
}
```

> `source` の相対パスはリポジトリルートからの相対。`./` は省略可能。

### VS Code でのインストール

#### ローカルインストール

```json
// settings.json
"chat.pluginLocations": {
  "/path/to/my-plugin": true
}
```

#### ソースからインストール

コマンドパレット: `Chat: Install Plugin From Source` → Git リポジトリ URL を入力

#### ワークスペース推奨

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

### Copilot CLI でのインストール（Copilot CLI のみ）

#### インストール指定形式

| 形式 | 指定方法 | 例 |
|------|---------|-----|
| マーケットプレイス | `plugin@marketplace` | `my-plugin@my-marketplace` |
| GitHub リポジトリ | `OWNER/REPO` | `octo-org/my-plugin` |
| GitHub サブディレクトリ | `OWNER/REPO:PATH/TO/PLUGIN` | `octo-org/mono:plugins/my-plugin` |
| Git URL | `https://github.com/o/r.git` | `https://github.com/octo-org/my-plugin.git` |
| ローカルパス | `./my-plugin` or `/abs/path` | `./plugins/my-plugin` |

#### CLI コマンド一覧

| コマンド | 説明 |
|---------|------|
| `copilot plugin install SPECIFICATION` | Plugin をインストール |
| `copilot plugin uninstall NAME` | Plugin を削除 |
| `copilot plugin list` | インストール済み Plugin を一覧表示 |
| `copilot plugin update NAME` | Plugin を更新 |
| `copilot plugin marketplace add SPECIFICATION` | マーケットプレイスを登録 |
| `copilot plugin marketplace list` | 登録済みマーケットプレイスを一覧表示 |
| `copilot plugin marketplace browse NAME` | マーケットプレイスの Plugin を閲覧 |
| `copilot plugin marketplace remove NAME` | マーケットプレイスの登録を解除 |

#### CLI でのファイル配置（Copilot CLI のみ）

| 項目 | パス |
|------|------|
| インストール済み Plugin（marketplace 経由） | `~/.copilot/installed-plugins/MARKETPLACE/PLUGIN-NAME` |
| インストール済み Plugin（直接） | `~/.copilot/installed-plugins/_direct/SOURCE-ID/` |
| マーケットプレイスキャッシュ（Linux） | `~/.cache/copilot/marketplaces/` |
| マーケットプレイスキャッシュ（macOS） | `~/Library/Caches/copilot/marketplaces/` |

> キャッシュディレクトリは環境変数 `COPILOT_CACHE_HOME` で上書き可能。
