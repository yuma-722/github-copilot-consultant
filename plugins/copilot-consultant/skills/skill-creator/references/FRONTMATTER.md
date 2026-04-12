# フロントマター リファレンス

SKILL.md のYAMLフロントマターで使用可能なフィールド一覧。

## 必須フィールド

### `name`

Skillの一意識別子。

| 制約 | 内容 |
|------|------|
| 文字数 | 1〜64文字 |
| 使用可能文字 | 小文字英数字（a-z, 0-9）とハイフン（`-`） |
| 禁止 | 先頭・末尾のハイフン、連続ハイフン（`--`） |
| 一致要件 | 親ディレクトリ名と一致させる |

命名の推奨パターン:

- 動名詞形（推奨）: `processing-pdfs`、`analyzing-data`、`testing-code`
- 名詞句: `pdf-processing`、`data-analysis`
- アクション指向: `process-pdfs`、`analyze-data`

避けるべき名前:

- 曖昧: `helper`、`utils`、`tools`
- 汎用的すぎる: `documents`、`data`、`files`

```yaml
# 有効な例
name: pdf-processing
name: data-analysis
name: code-review

# 無効な例
name: PDF-Processing    # 大文字不可
name: -pdf              # 先頭ハイフン不可
name: pdf--processing   # 連続ハイフン不可
```

### `description`

Skillの説明。エージェントがSkillを選択する際の判断基準となる最重要フィールド。

| 制約 | 内容 |
|------|------|
| 文字数 | 1〜1024文字 |
| 必須内容 | 何をするか＋いつ使うか |
| 視点 | 三人称で記述する |

記述のポイント:

1. **何をするか** を具体的に書く（機能の列挙）
2. **いつ使うか** を明記する（トリガーとなるキーワードや状況）
3. 関連するキーワードを含める
4. 三人称で書く（「Processes ...」「Use when ...」）

注意: VS Code（GitHub Copilot）の読み込みでは、`description` に改行を含む書き方（`description: >-` などのブロックスカラー）がエラーになることがある。**`description: ...` の1行で記述する**。

```yaml
# 良い例
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDFs or when the user mentions PDFs, forms, or document extraction.

description: Analyzes Excel spreadsheets, creates pivot tables, and generates charts. Use when analyzing spreadsheets, tabular data, or .xlsx files.

description: Generates descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.

# 悪い例
description: Helps with documents
description: Processes data
description: Does stuff with files
```

## 任意フィールド

### `license`

Skillに適用するライセンス。

```yaml
license: Apache-2.0
license: Proprietary. LICENSE.txt has complete terms
```

### `compatibility`

環境要件がある場合に記述する。ほとんどのSkillでは不要。

```yaml
compatibility: Requires git, docker, jq, and access to the internet
```

### `metadata`

追加のキー・バリューマッピング。

```yaml
metadata:
  author: example-org
  version: "1.0"
```

### `allowed-tools`

事前承認されたツールのスペース区切りリスト（実験的機能）。

```yaml
allowed-tools: Bash(git:*) Bash(jq:*) Read
```

## VS Code 追加フィールド

VS Code（GitHub Copilot）では以下の追加フィールドが使用可能:

注意: これらはAgent Skillsのオープン標準（agentskills.io仕様）には含まれないため、標準準拠の検証ツール（例: skills-ref）ではエラーになる可能性がある。**ポータビリティを最優先**する場合は、標準フィールド（`name`/`description`/`license`/`compatibility`/`metadata`/`allowed-tools`）のみを使い、VS Code固有の挙動はクライアント側設定で補う。

### `argument-hint`

スラッシュコマンドとして呼び出された際にチャット入力欄に表示されるヒントテキスト。

```yaml
argument-hint: "[test file] [options]"
```

### `user-invocable`

`/` メニューにスラッシュコマンドとして表示するかを制御する。デフォルト: `true`。

```yaml
user-invocable: false  # メニューに表示しない（モデル自動呼び出しのみ）
```

### `disable-model-invocation`

モデルがこのSkillを自動的に読み込めるかを制御する。デフォルト: `false`。

```yaml
disable-model-invocation: true  # スラッシュコマンドでのみ呼び出し可能
```

### VS Code でのアクセス制御の組み合わせ

| `user-invocable` | `disable-model-invocation` | `/` メニュー | 自動呼び出し | 用途 |
|:-:|:-:|:-:|:-:|------|
| (省略) | (省略) | ○ | ○ | 汎用Skill |
| `false` | (省略) | × | ○ | バックグラウンド知識Skill |
| (省略) | `true` | ○ | × | オンデマンド専用Skill |
| `false` | `true` | × | × | 無効化されたSkill |

## 完全なフロントマター例

```yaml
---
name: pdf-processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDFs or when the user mentions PDFs, forms, or document extraction.
license: Apache-2.0
compatibility: Requires Python 3.10+ with pdfplumber
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(python:*) Read
---
```
