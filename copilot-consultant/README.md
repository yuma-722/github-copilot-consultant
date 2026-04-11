# Copilot Consultant Plugin

GitHub Copilot のカスタマイズ設定（instructions / prompts / agents / skills / hooks）を効率的に作成・管理するための Agent Plugin です。

> ⚠️ Agent Plugins は Preview 機能です。`chat.plugins.enabled` 設定を有効にする必要があります。

## インストール

### マーケットプレイスから（推奨）

VS Code の `settings.json` に以下を追加してください：

```jsonc
"chat.plugins.marketplaces": ["yuma-722/github-copilot-consultant"]
```

追加後、Extensions ビューで `@agentPlugins` を検索すると `copilot-consultant` が表示されます。`Install` をクリックしてインストールしてください。

### ソースから直接インストール

1. コマンドパレット（`Ctrl+Shift+P`）を開く
2. `Chat: Install Plugin From Source` を実行
3. `https://github.com/yuma-722/github-copilot-consultant` を入力

### ローカルインストール

リポジトリをクローンし、`settings.json` に追加：

```jsonc
"chat.pluginLocations": {
  "/path/to/github-copilot-consultant/copilot-consultant": true
}
```

## 含まれるカスタマイズ

### Agents

| エージェント名 | 説明 |
|----------------|------|
| **Copilot Consultant** | カスタマイズ相談窓口（Coordinator）。目的に応じた最適なカスタマイズ手段を提案し、Worker に作業を委譲する |
| **Copilot Custom Worker** | カスタマイズ成果物の作成担当（Worker）。instructions / prompts / agents / skills / hooks のドラフト作成・更新を行う |

### Skills

| スキル名 | 説明 |
|----------|------|
| **custom-instructions-creator** | カスタム指示ファイルの設計・作成・レビュー |
| **custom-agents-creator** | Custom Agents の設計・作成・レビュー |
| **prompt-creator** | Prompt Files（スラッシュコマンド）の設計・作成・レビュー |
| **hooks-creator** | Agent Hooks の設計・作成・レビュー |
| **plugin-creator** | 既存の Copilot カスタマイズを Agent Plugin としてパッケージングし、マーケットプレイス配布向けに整備する |
| **skill-creator** | Agent Skills の設計・作成・レビュー |

### Commands（スラッシュコマンド）

| コマンド | 説明 |
|----------|------|
| `/copilot-consultant:update-copilot-customizations` | カスタマイズ資産を公式ドキュメントの最新情報に合わせて点検・更新する |
| `/copilot-consultant:update-skill-creator` | skill-creator Skill を最新仕様・ベストプラクティスに沿って改善する |

### MCP Servers

| サーバー名 | 説明 |
|-----------|------|
| **awesome-copilot** | Copilot カスタマイズの参考例を検索・参照するための MCP サーバー |
| **microsoftdocs/mcp** | Microsoft Learn の公式ドキュメントを検索・取得するための MCP サーバー |

## 使い方

1. Plugin をインストール後、Copilot Chat を開く
2. `@copilot-consultant` で Coordinator エージェントに話しかける
3. やりたいことを自然言語で依頼する

### 依頼例

- 「このリポジトリの開発規約に沿うように、Copilot をいい感じにカスタマイズする案を出して」
- 「デプロイ自動化で使うカスタムエージェントを作って」
- 「テスト実行用のスキルを作成して」
- 「既存のカスタマイズが古いので、最新仕様に合わせて更新して」

## 前提条件

- VS Code（Insiders 推奨）
- GitHub Copilot（Chat 有効）
- `chat.plugins.enabled`: `true`
- Docker（awesome-copilot MCP サーバー用）

## ライセンス

MIT
