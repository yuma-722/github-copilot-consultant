# Plugin 構成例

## 例1: シンプルな Skills-only Plugin

Skills のみを含む最小構成。デフォルトパス規約（`skills/`）に従うため、plugin.json で `skills` を明示的に指定しなくても自動検出される。

```
my-testing-plugin/
├── plugin.json
├── skills/
│   └── test-runner/
│       ├── SKILL.md
│       └── scripts/
│           └── run-tests.sh
└── README.md
```

plugin.json:

```json
{
  "name": "my-testing-plugin",
  "description": "テスト実行と結果分析を支援するPlugin",
  "version": "1.0.0",
  "keywords": ["testing", "automation"],
  "author": { "name": "Team" },
  "license": "MIT"
}
```

> `skills` フィールド省略時はデフォルトで `skills/` ディレクトリが検索される。

## 例2: Agent + Skills + Commands の複合Plugin

`agents` と `skills` には文字列と配列のどちらも使える。

```
copilot-customization-toolkit/
├── plugin.json
├── skills/
│   ├── custom-instructions-creator/
│   │   └── SKILL.md
│   └── custom-agents-creator/
│       └── SKILL.md
├── extra-skills/
│   └── hooks-creator/
│       └── SKILL.md
├── agents/
│   └── copilot-consultant.agent.md
├── commands/
│   └── update-customizations.md
└── README.md
```

plugin.json:

```json
{
  "name": "copilot-customization-toolkit",
  "description": "GitHub Copilot のカスタマイズ設定を効率的に作成・管理するツール群",
  "version": "1.0.0",
  "keywords": ["copilot", "customization", "instructions", "agents"],
  "category": "developer-tools",
  "author": { "name": "Team" },
  "license": "MIT",
  "agents": "agents/",
  "commands": ["./commands/update-customizations.md"],
  "skills": ["./skills", "./extra-skills/hooks-creator"]
}
```

> `agents` は文字列でディレクトリを指定、`skills` は配列で複数ディレクトリを指定する例。

## 例3: Hooks + MCP Server 付きPlugin（インライン定義）

hooks と mcpServers を plugin.json にインラインで定義する例。外部ファイルを用意する必要がなく、シンプルな構成になる。

```
code-quality-plugin/
├── plugin.json
├── scripts/
│   ├── lint-check.sh
│   └── format-on-save.sh
└── README.md
```

plugin.json:

```json
{
  "name": "code-quality-plugin",
  "description": "コード品質チェックを自動化し、品質ダッシュボードと連携するPlugin",
  "version": "1.0.0",
  "keywords": ["quality", "linting", "formatting"],
  "author": { "name": "Team" },
  "license": "MIT",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/lint-check.sh"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "quality-dashboard": {
      "command": "npx",
      "args": ["@company/quality-mcp-server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

> hooks と mcpServers のインライン定義により、別途 `hooks.json` や `.mcp.json` を用意する必要がない。

## 例3b: Hooks + MCP Server 付きPlugin（外部ファイル配置）

hooks と MCP servers を外部ファイルとして配置する例。plugin.json からパスを指定するか、自動検出に任せる。

```
code-quality-plugin/
├── plugin.json
├── hooks.json
├── scripts/
│   ├── lint-check.sh
│   └── format-on-save.sh
├── .mcp.json
└── README.md
```

hooks/hooks.json:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/lint-check.sh"
          }
        ]
      }
    ]
  }
}
```

.mcp.json:

```json
{
  "mcpServers": {
    "quality-dashboard": {
      "command": "npx",
      "args": ["@company/quality-mcp-server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

plugin.json（外部ファイル参照版）:

```json
{
  "name": "code-quality-plugin",
  "description": "コード品質チェックを自動化し、品質ダッシュボードと連携するPlugin",
  "version": "1.0.0",
  "keywords": ["quality", "linting", "formatting"],
  "author": { "name": "Team" },
  "license": "MIT",
  "hooks": "hooks.json",
  "mcpServers": ".mcp.json"
}
```

## 例4: 両フォーマット対応 Plugin

Copilot と Claude の両方のマーケットプレイスで配布する場合:

```
my-plugin/
├── plugin.json                  # ルートのマニフェスト（両方で検出可能）
├── .github/
│   └── plugin/
│       └── plugin.json          # Copilot format 用（ルートと同内容）
├── .claude-plugin/
│   └── plugin.json              # Claude format 用（ルートと同内容）
├── hooks.json                   # Copilot 用（ルート配置）
├── hooks/
│   └── hooks.json               # Claude 用
├── skills/
│   └── my-skill/
│       └── SKILL.md
└── README.md
```

> ルートの `plugin.json` は最優先で検索されるため、Copilot 専用の `.github/plugin/` 配置は省略してもよい。

## 例5: 公式リファレンス形式の plugin.json

GitHub 公式ドキュメント掲載の参考例:

```json
{
  "name": "my-dev-tools",
  "description": "React development utilities",
  "version": "1.2.0",
  "author": {
    "name": "Jane Doe",
    "email": "jane@example.com"
  },
  "license": "MIT",
  "keywords": ["react", "frontend"],
  "agents": "agents/",
  "skills": ["skills/", "extra-skills/"],
  "hooks": "hooks.json",
  "mcpServers": ".mcp.json"
}
```

> 出典: [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson)

## カスタマイズ種別の変換ルール

ワークスペースのカスタマイズを Plugin に変換する際の対応表:

| ワークスペース | Plugin 内 | 備考 |
|---------------|----------|------|
| `.github/skills/<name>/` | `skills/<name>/` | そのままコピー |
| `.github/agents/<name>.agent.md` | `agents/<name>.agent.md` | `tools` の調整が必要な場合あり |
| `.github/prompts/<name>.prompt.md` | `commands/<name>.md` | Plugin では commands として扱う |
| `.github/hooks/*.json` | `hooks/hooks.json` | 統合し、パスを `${CLAUDE_PLUGIN_ROOT}` に書き換え |
| `.mcp.json` | `.mcp.json` | トップレベルキーを `mcpServers` に統一 |
| `.github/instructions/*.instructions.md` | ❌ 直接バンドル不可 | skills や agents の本文に組み込む |

### Agent の tools 調整

ワークスペースで使える tools キーワードの一部は Plugin コンテキストで利用できない場合がある。Plugin にバンドルする際は、agent の `tools` 宣言を確認し、Plugin が提供する MCP servers や汎用ツールに限定する。
