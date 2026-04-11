# Plugin 構成例

## 例1: シンプルな Skills-only Plugin

Skills のみを含む最小構成。

```
my-testing-plugin/
├── .github/
│   └── plugin/
│       └── plugin.json
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
  "license": "MIT",
  "skills": ["./skills/test-runner"]
}
```

## 例2: Agent + Skills + Commands の複合Plugin

```
copilot-customization-toolkit/
├── .github/
│   └── plugin/
│       └── plugin.json
├── skills/
│   ├── custom-instructions-creator/
│   │   └── SKILL.md
│   └── custom-agents-creator/
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
  "author": { "name": "Team" },
  "license": "MIT",
  "agents": ["./agents"],
  "commands": ["./commands/update-customizations.md"],
  "skills": [
    "./skills/custom-instructions-creator",
    "./skills/custom-agents-creator"
  ]
}
```

## 例3: Hooks + MCP Server 付きPlugin

```
code-quality-plugin/
├── .github/
│   └── plugin/
│       └── plugin.json
├── hooks/
│   └── hooks.json
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

plugin.json:

```json
{
  "name": "code-quality-plugin",
  "description": "コード品質チェックを自動化し、品質ダッシュボードと連携するPlugin",
  "version": "1.0.0",
  "keywords": ["quality", "linting", "formatting"],
  "author": { "name": "Team" },
  "license": "MIT"
}
```

**注意**: hooks と MCP servers は plugin.json に列挙せず、ファイル配置により自動検出される。

## 例4: 両フォーマット対応 Plugin

Copilot と Claude の両方のマーケットプレイスで配布する場合:

```
my-plugin/
├── .github/
│   └── plugin/
│       └── plugin.json          # Copilot format
├── .claude-plugin/
│   └── marketplace.json         # Claude format（plugin.json へのシンボリックリンクでも可）
├── hooks.json                   # Copilot 用（ルート配置）
├── hooks/
│   └── hooks.json               # Claude 用
├── skills/
│   └── my-skill/
│       └── SKILL.md
└── README.md
```

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
