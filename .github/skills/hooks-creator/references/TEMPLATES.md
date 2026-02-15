# Hooks テンプレートと実装例

## 基本テンプレート: フック設定ファイル

`.github/hooks/` に配置する JSON ファイルの基本構造:

```json
{
  "hooks": {
    "PreToolUse": [],
    "PostToolUse": [],
    "SessionStart": [],
    "Stop": [],
    "UserPromptSubmit": [],
    "PreCompact": [],
    "SubagentStart": [],
    "SubagentStop": []
  }
}
```

必要なイベントだけ記述すればよい。空配列のイベントは省略可能。

## パターン1: 危険コマンドのブロック（PreToolUse）

ターミナルで `rm -rf` や `DROP TABLE` などの破壊的コマンドを防ぐ:

### フック設定

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "node .github/hooks/scripts/block-dangerous.js",
        "timeout": 10
      }
    ]
  }
}
```

### スクリプト例（Node.js）

```javascript
#!/usr/bin/env node
const input = [];
process.stdin.on("data", (chunk) => input.push(chunk));
process.stdin.on("end", () => {
  const data = JSON.parse(Buffer.concat(input).toString());

  if (data.tool_name !== "run_in_terminal") {
    process.stdout.write(JSON.stringify({ continue: true }));
    process.exit(0);
  }

  const command = data.tool_input?.command || "";
  const blocked = [/rm\s+-rf\s+\//, /DROP\s+TABLE/i, /mkfs\./, /:\(\)\{/];

  for (const pattern of blocked) {
    if (pattern.test(command)) {
      process.stdout.write(
        JSON.stringify({
          hookSpecificOutput: {
            hookEventName: "PreToolUse",
            permissionDecision: "deny",
            permissionDecisionReason: `ブロック: ${pattern} にマッチするコマンド`,
          },
        })
      );
      process.exit(0);
    }
  }

  process.stdout.write(JSON.stringify({ continue: true }));
  process.exit(0);
});
```

## パターン2: 自動フォーマット（PostToolUse）

ファイル編集後に Prettier を自動実行する:

### フック設定

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "command",
        "command": "npx prettier --write \"$TOOL_INPUT_FILE_PATH\"",
        "timeout": 15
      }
    ]
  }
}
```

## パターン3: ツール使用ログ（PostToolUse）

すべてのツール呼び出しを監査ログに記録する:

### フック設定

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "command",
        "command": "node .github/hooks/scripts/audit-log.js",
        "timeout": 10
      }
    ]
  }
}
```

### スクリプト例（Node.js）

```javascript
#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

const input = [];
process.stdin.on("data", (chunk) => input.push(chunk));
process.stdin.on("end", () => {
  const data = JSON.parse(Buffer.concat(input).toString());
  const logEntry = {
    timestamp: data.timestamp,
    sessionId: data.sessionId,
    tool: data.tool_name,
    input: data.tool_input,
  };
  const logPath = path.join(data.cwd, ".github/hooks/audit.log");
  fs.appendFileSync(logPath, JSON.stringify(logEntry) + "\n");
  process.stdout.write(JSON.stringify({ continue: true }));
  process.exit(0);
});
```

## パターン4: プロジェクトコンテキスト注入（SessionStart）

セッション開始時にプロジェクト情報を自動注入する:

### フック設定

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "node .github/hooks/scripts/inject-context.js",
        "timeout": 10
      }
    ]
  }
}
```

### スクリプト例（Node.js）

```javascript
#!/usr/bin/env node
const { execSync } = require("child_process");

const branch = execSync("git branch --show-current", {
  encoding: "utf-8",
}).trim();

const nodeVersion = execSync("node --version", { encoding: "utf-8" }).trim();

process.stdout.write(
  JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext: `Branch: ${branch} | Node: ${nodeVersion}`,
    },
  })
);
process.exit(0);
```

## パターン5: 特定ツールの承認要求（PreToolUse）

機密性の高い操作に対してユーザー確認を求める:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "node .github/hooks/scripts/require-approval.js",
        "timeout": 10
      }
    ]
  }
}
```

```javascript
#!/usr/bin/env node
const input = [];
process.stdin.on("data", (chunk) => input.push(chunk));
process.stdin.on("end", () => {
  const data = JSON.parse(Buffer.concat(input).toString());

  const sensitiveTools = ["run_in_terminal", "mcp_github_push_files"];

  if (sensitiveTools.includes(data.tool_name)) {
    process.stdout.write(
      JSON.stringify({
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "ask",
          permissionDecisionReason: `${data.tool_name} は確認が必要です`,
        },
      })
    );
  } else {
    process.stdout.write(JSON.stringify({ continue: true }));
  }
  process.exit(0);
});
```

## パターン6: OS別コマンド

クロスプラットフォームで異なるコマンドを実行する:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "command",
        "command": "./scripts/format.sh",
        "windows": "powershell -File scripts\\format.ps1",
        "linux": "./scripts/format-linux.sh",
        "osx": "./scripts/format-mac.sh"
      }
    ]
  }
}
```

## パターン7: Stop フックでテスト強制

エージェント終了前にテストを必ず実行させる:

```json
{
  "hooks": {
    "Stop": [
      {
        "type": "command",
        "command": "node .github/hooks/scripts/ensure-tests.js",
        "timeout": 10
      }
    ]
  }
}
```

```javascript
#!/usr/bin/env node
const input = [];
process.stdin.on("data", (chunk) => input.push(chunk));
process.stdin.on("end", () => {
  const data = JSON.parse(Buffer.concat(input).toString());

  // 無限ループ防止: 前回のstopフックで既に継続中なら何もしない
  if (data.stop_hook_active) {
    process.stdout.write(JSON.stringify({ continue: true }));
    process.exit(0);
  }

  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "Stop",
        decision: "block",
        reason: "テストスイートを実行してから終了してください",
      },
    })
  );
  process.exit(0);
});
```

## チェックリスト

フックを追加する際の確認事項:

- [ ] `type` が `"command"` になっている
- [ ] ファイル拡張子が `.json` である
- [ ] スクリプトに実行権限がある（Unix系の場合）
- [ ] stdin の JSON を正しくパースしている
- [ ] stdout に有効な JSON を出力している
- [ ] 適切な終了コードを返している（0: 成功、2: ブロッキングエラー）
- [ ] タイムアウトが適切に設定されている
- [ ] シークレットがハードコードされていない
- [ ] stdin 入力をバリデーションしている
- [ ] `stop_hook_active` を確認して無限ループを防止している（Stop/SubagentStop の場合）
