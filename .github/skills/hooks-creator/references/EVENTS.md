# イベント別 入出力リファレンス

各ライフサイクルイベントの入出力仕様をまとめる。

## 共通入力フィールド

すべてのフックが stdin で受け取る JSON の共通フィールド:

| フィールド | 型 | 説明 |
|-----------|------|------|
| `timestamp` | string | ISO 8601 タイムスタンプ |
| `cwd` | string | ワークスペースパス |
| `sessionId` | string | セッション識別子 |
| `hookEventName` | string | イベント名 |
| `transcript_path` | string | トランスクリプトファイルパス |

## 共通出力フィールド

すべてのフックが stdout で返せる共通フィールド:

| フィールド | 型 | 説明 |
|-----------|------|------|
| `continue` | boolean | `false` で処理を停止（デフォルト: `true`） |
| `stopReason` | string | 停止理由（モデルに表示） |
| `systemMessage` | string | ユーザーに表示するメッセージ |

## SessionStart

### 入力

共通フィールド + :

| フィールド | 型 | 説明 |
|-----------|------|------|
| `source` | string | セッション開始方法。現在は常に `"new"` |

### 出力

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Project: my-app v2.1.0 | Branch: main"
  }
}
```

| フィールド | 型 | 説明 |
|-----------|------|------|
| `additionalContext` | string | 会話に追加するコンテキスト |

## UserPromptSubmit

### 入力

共通フィールド + `prompt`（ユーザーが送信したテキスト）。

### 出力

共通出力フォーマットのみ（`continue`, `stopReason`, `systemMessage`）。

## PreToolUse

### 入力

共通フィールド + :

| フィールド | 型 | 説明 |
|-----------|------|------|
| `tool_name` | string | ツール名（例: `"editFiles"`, `"run_in_terminal"`） |
| `tool_input` | object | ツールへの入力パラメータ |
| `tool_use_id` | string | ツール使用の一意ID |

### 出力

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "理由",
    "updatedInput": {},
    "additionalContext": "追加コンテキスト"
  }
}
```

| フィールド | 型 | 説明 |
|-----------|------|------|
| `permissionDecision` | `"allow"` / `"deny"` / `"ask"` | ツール実行の制御 |
| `permissionDecisionReason` | string | 決定理由（ユーザーに表示） |
| `updatedInput` | object | 変更後のツール入力（任意） |
| `additionalContext` | string | モデルへの追加コンテキスト |

**優先順位**: 複数フックが同一ツール呼び出しに対して実行された場合、最も制限的な決定が採用される: `deny` > `ask` > `allow`

## PostToolUse

### 入力

共通フィールド + :

| フィールド | 型 | 説明 |
|-----------|------|------|
| `tool_name` | string | ツール名 |
| `tool_input` | object | ツールへの入力パラメータ |
| `tool_use_id` | string | ツール使用の一意ID |
| `tool_response` | string | ツールの実行結果 |

### 出力

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "ファイルにlintエラーがあります"
  }
}
```

| フィールド | 型 | 説明 |
|-----------|------|------|
| `decision` | `"block"` | 以降の処理をブロック（任意） |
| `reason` | string | ブロック理由（モデルに表示） |
| `additionalContext` | string | 会話に追加するコンテキスト |

## PreCompact

### 入力

共通フィールド + :

| フィールド | 型 | 説明 |
|-----------|------|------|
| `trigger` | string | 圧縮のトリガー。会話が長すぎる場合は `"auto"` |

### 出力

共通出力フォーマットのみ。

## SubagentStart

### 入力

共通フィールド + :

| フィールド | 型 | 説明 |
|-----------|------|------|
| `agent_id` | string | サブエージェントの一意ID |
| `agent_type` | string | エージェント名（例: `"Plan"`、カスタムエージェント名） |

### 出力

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "このサブエージェントはコーディングガイドラインに従うこと"
  }
}
```

| フィールド | 型 | 説明 |
|-----------|------|------|
| `additionalContext` | string | サブエージェントの会話に追加するコンテキスト |

## SubagentStop

### 入力

共通フィールド + :

| フィールド | 型 | 説明 |
|-----------|------|------|
| `agent_id` | string | サブエージェントの一意ID |
| `agent_type` | string | エージェント名 |
| `stop_hook_active` | boolean | 前回のstopフックの結果として継続中の場合 `true` |

### 出力

```json
{
  "decision": "block",
  "reason": "結果を検証してから完了すること"
}
```

| フィールド | 型 | 説明 |
|-----------|------|------|
| `decision` | `"block"` | サブエージェントの停止を阻止 |
| `reason` | string | `"block"` 時必須。継続すべき理由 |

## Stop

### 入力

共通フィールド + :

| フィールド | 型 | 説明 |
|-----------|------|------|
| `stop_hook_active` | boolean | 前回のstopフックの結果として継続中の場合 `true`。無限ループ防止に使用する |

### 出力

```json
{
  "hookSpecificOutput": {
    "hookEventName": "Stop",
    "decision": "block",
    "reason": "テストスイートを実行してから終了すること"
  }
}
```

| フィールド | 型 | 説明 |
|-----------|------|------|
| `decision` | `"block"` | エージェントの停止を阻止 |
| `reason` | string | `"block"` 時必須。エージェントに継続すべき理由を伝える |
