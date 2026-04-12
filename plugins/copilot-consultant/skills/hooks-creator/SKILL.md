---
name: hooks-creator
description: VS Code の Agent hooks（ライフサイクルフック）を設計・作成・レビューする。.github/hooks/*.json、hook、PreToolUse、PostToolUse、SessionStart、Stop、UserPromptSubmit、PreCompact、SubagentStart、SubagentStop、ライフサイクル自動化、セキュリティポリシー、コード品質自動化に言及したときに使用する。
---

# Agent Hooks 作成スキル（VS Code / GitHub Copilot）

このSkillは、VS Code の **Agent hooks** を設計し、ワークスペースへ追加する。Hooksはエージェントセッションのライフサイクルポイントでシェルコマンドを確定的に実行し、セキュリティ強制・コード品質自動化・監査ログなどを実現する。

## まず決める

- **目的**: 何を自動化するか（セキュリティ制御、フォーマット、ログ、コンテキスト注入、承認制御）
- **イベント**: どのライフサイクルポイントで発火するか
- **スクリプト**: 実行するコマンドまたはスクリプト

## ライフサイクルイベント一覧

| イベント | タイミング | 主な用途 |
|---------|-----------|---------|
| `SessionStart` | 新しいセッション開始時 | リソース初期化、プロジェクトコンテキスト注入 |
| `UserPromptSubmit` | ユーザーがプロンプト送信時 | リクエスト監査、システムコンテキスト注入 |
| `PreToolUse` | ツール実行前 | 危険操作のブロック、承認制御、入力変更 |
| `PostToolUse` | ツール実行後 | フォーマッタ実行、結果ログ、追加アクション |
| `PreCompact` | コンテキスト圧縮前 | 重要コンテキストの退避 |
| `SubagentStart` | サブエージェント生成時 | サブエージェントの追跡・初期化 |
| `SubagentStop` | サブエージェント完了時 | 結果集約、クリーンアップ |
| `Stop` | セッション終了時 | レポート生成、リソース後処理 |

## 作成フロー

### 1) 配置場所を決める

| スコープ | パス |
|---------|------|
| ワークスペース（チーム共有） | `.github/hooks/*.json` |
| ワークスペース（ローカル） | `.claude/settings.local.json` |
| ワークスペース（共有） | `.claude/settings.json` |
| ユーザー全体 | `~/.claude/settings.json` |

ワークスペースhooksがユーザーhooksより優先される。通常は `.github/hooks/` にJSON ファイルを作成する。

### 2) フック設定ファイルを書く

JSON 形式で `hooks` オブジェクトを記述する:

```json
{
  "hooks": {
    "<イベント名>": [
      {
        "type": "command",
        "command": "./scripts/my-hook.sh",
        "timeout": 15
      }
    ]
  }
}
```

### 3) コマンドプロパティを設定する

| プロパティ | 型 | 説明 |
|-----------|------|------|
| `type` | string | 必須。`"command"` 固定 |
| `command` | string | 実行コマンド（クロスプラットフォームデフォルト） |
| `windows` | string | Windows 固有コマンド |
| `linux` | string | Linux 固有コマンド |
| `osx` | string | macOS 固有コマンド |
| `cwd` | string | 作業ディレクトリ（リポジトリルートからの相対パス） |
| `env` | object | 追加の環境変数 |
| `timeout` | number | タイムアウト秒数（デフォルト: 30） |

OS固有コマンドが定義されていない場合、`command` にフォールバックする。

### 4) フックスクリプトを作成する

フックは **stdin で JSON を受け取り、stdout で JSON を返す**。

共通入力フィールド:

```json
{
  "timestamp": "2026-02-09T10:30:00.000Z",
  "cwd": "/path/to/workspace",
  "sessionId": "session-identifier",
  "hookEventName": "PreToolUse",
  "transcript_path": "/path/to/transcript.json"
}
```

共通出力フィールド:

```json
{
  "continue": true,
  "stopReason": "理由（モデルに表示）",
  "systemMessage": "ユーザーに表示するメッセージ"
}
```

終了コード:

| コード | 意味 |
|-------|------|
| `0` | 成功: stdout を JSON としてパース |
| `2` | ブロッキングエラー: 処理を停止しエラーをモデルに表示 |
| その他 | 非ブロッキング警告: 警告を表示し処理を続行 |

### 5) テストとデバッグ

- `/hooks` コマンドで対話的にフック設定を管理できる
- 出力パネルで **GitHub Copilot Chat Hooks** チャンネルを確認する
- Chat ビューを右クリック → **Diagnostics** でフックの読み込み状態を確認する
- スクリプトに実行権限があるか確認する（`chmod +x`）

## イベント別の入出力詳細

詳細な入出力仕様は [references/EVENTS.md](references/EVENTS.md) を参照。

## よくあるパターン

テンプレートと実装例は [references/TEMPLATES.md](references/TEMPLATES.md) を参照。

## セキュリティ上の注意

- フックはVS Codeと同じ権限でシェルコマンドを実行する
- 共有リポジトリのフックスクリプトは使用前に必ずレビューする
- スクリプト内にシークレットをハードコードしない（環境変数やセキュアストレージを使う）
- stdin からの入力を必ずバリデーション・サニタイズする（インジェクション防止）
- `chat.tools.edits.autoApprove` 設定でフックスクリプトの自動編集を禁止することを推奨する

## 期待する出力

- `.github/hooks/<name>.json` の新規作成、または既存フック設定の改善
- 必要に応じてフックスクリプト（`.github/hooks/scripts/` 等）を作成する
- 変更時は「何をどう変えたか（イベント/コマンド/セキュリティ影響）」を短く添える

## 参照

- https://code.visualstudio.com/docs/copilot/customization/hooks
- https://code.visualstudio.com/docs/copilot/customization/overview
