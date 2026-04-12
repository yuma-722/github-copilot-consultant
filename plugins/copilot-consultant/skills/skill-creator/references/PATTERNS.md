# よくあるパターンと具体例

Skill本文で使える代表的なパターンを示す。

## テンプレートパターン

出力フォーマットをテンプレートで指定する。厳密さはタスクに応じて調整する。

### 厳密なテンプレート（APIレスポンスやデータ形式向け）

```markdown
## レポート構成

必ずこのテンプレート構造を使用する:

\```markdown
# [分析タイトル]

## エグゼクティブサマリー
[主要な発見の概要（1段落）]

## 主要な発見
- 発見1: 裏付けデータ付き
- 発見2: 裏付けデータ付き

## 推奨事項
1. 具体的なアクション
2. 具体的なアクション
\```
```

### 柔軟なテンプレート（コンテキストに応じた調整が有用な場合）

```markdown
## レポート構成

以下はデフォルトのフォーマットだが、分析内容に応じて判断すること:

\```markdown
# [分析タイトル]

## エグゼクティブサマリー
[概要]

## 主要な発見
[発見に応じてセクションを調整する]

## 推奨事項
[具体的なコンテキストに合わせる]
\```
```

## 入出力例パターン

出力品質が例に依存する場合、入出力ペアを提供する:

```markdown
## コミットメッセージのフォーマット

以下の例に従ってコミットメッセージを生成する:

**例1:**
入力: ユーザー認証にJWTトークンを追加
出力:
\```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
\```

**例2:**
入力: レポートで日付が正しく表示されないバグを修正
出力:
\```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
\```
```

## 条件分岐ワークフローパターン

判断ポイントを明示して、エージェントを適切な手順に誘導する:

```markdown
## ドキュメント変更ワークフロー

1. 変更の種類を判断する:

   **新規作成？** → 下記「作成ワークフロー」に従う
   **既存の編集？** → 下記「編集ワークフロー」に従う

2. 作成ワークフロー:
   - docx-js ライブラリを使用する
   - ゼロからドキュメントを構築する
   - .docx 形式でエクスポートする

3. 編集ワークフロー:
   - 既存ドキュメントをアンパックする
   - XMLを直接変更する
   - 変更ごとにバリデーションする
   - 完了後にリパックする
```

## ワークフロー＋チェックリストパターン

複雑なタスクではチェックリストを提供し、進行状況を追跡する:

```markdown
## PDF フォーム入力ワークフロー

このチェックリストをコピーして進行状況を管理する:

\```
進行状況:
- [ ] Step 1: フォーム解析（analyze_form.py を実行）
- [ ] Step 2: フィールドマッピング作成（fields.json を編集）
- [ ] Step 3: マッピング検証（validate_fields.py を実行）
- [ ] Step 4: フォーム入力（fill_form.py を実行）
- [ ] Step 5: 出力検証（verify_output.py を実行）
\```

**Step 1: フォーム解析**

実行: `python scripts/analyze_form.py input.pdf`

フォームフィールドとその位置を抽出し、`fields.json` に保存する。

**Step 2: フィールドマッピング作成**

`fields.json` を編集して各フィールドに値を追加する。

**Step 3: マッピング検証**

実行: `python scripts/validate_fields.py fields.json`

検証エラーがあれば、続行前に修正する。

**Step 4: フォーム入力**

実行: `python scripts/fill_form.py input.pdf fields.json output.pdf`

**Step 5: 出力検証**

実行: `python scripts/verify_output.py output.pdf`

検証が失敗した場合、Step 2に戻る。
```

## フィードバックループパターン

バリデーターを実行 → エラー修正 → 再実行のループで品質を向上させる:

```markdown
## ドキュメント編集プロセス

1. `word/document.xml` を編集する
2. **即座にバリデーション**: `python ooxml/scripts/validate.py unpacked_dir/`
3. バリデーション失敗時:
   - エラーメッセージを確認する
   - XMLの問題を修正する
   - 再度バリデーションを実行する
4. **バリデーション通過後のみ続行する**
5. リビルド: `python ooxml/scripts/pack.py unpacked_dir/ output.docx`
6. 出力ドキュメントをテストする
```

## ユーティリティスクリプトパターン

エージェントにコードを生成させるより、事前作成スクリプトを提供する方が信頼性が高い:

```markdown
## ユーティリティスクリプト

**analyze_form.py**: PDFからフォームフィールドを抽出する

\```bash
python scripts/analyze_form.py input.pdf > fields.json
\```

出力形式:
\```json
{
  "field_name": {"type": "text", "x": 100, "y": 200},
  "signature": {"type": "sig", "x": 150, "y": 500}
}
\```

**validate_boxes.py**: バウンディングボックスの重複をチェックする

\```bash
python scripts/validate_boxes.py fields.json
# 出力: "OK" またはコンフリクト一覧
\```
```

スクリプトの利点:

- 生成コードより信頼性が高い
- トークンを節約できる（コンテキストにコードを含める必要がない）
- 使用間で一貫性を保てる

SKILL.md 内ではスクリプトを **実行** するのか **参照として読む** のかを明確にする:

- 実行（一般的）: 「`analyze_form.py` を実行してフィールドを抽出する」
- 参照: 「抽出アルゴリズムは `analyze_form.py` を参照」

## アンチパターン（避けるべきこと）

### Windowsスタイルのパスを使わない

```
# 良い例
scripts/helper.py
reference/guide.md

# 悪い例
scripts\helper.py
reference\guide.md
```

### 選択肢を増やしすぎない

```markdown
# 悪い例（混乱を招く）
pypdf、pdfplumber、PyMuPDF、pdf2image のいずれかを使用できます...

# 良い例（デフォルトを提供し、逃げ道を用意）
テキスト抽出には pdfplumber を使用する:
\```python
import pdfplumber
\```

OCRが必要なスキャンPDFには、代わりに pdf2image + pytesseract を使用する。
```

### 時間依存の情報を含めない

```markdown
# 悪い例
2025年8月より前なら旧APIを使用する。

# 良い例
## 現在のメソッド
v2 APIエンドポイントを使用する: `api.example.com/v2/messages`

## 旧パターン
<details>
<summary>レガシー v1 API（2025-08 非推奨）</summary>
v1 APIは `api.example.com/v1/messages` を使用していた。
</details>
```

### ツールがインストール済みだと仮定しない

```markdown
# 悪い例
pdf ライブラリを使ってファイルを処理する。

# 良い例
必要なパッケージをインストールする: `pip install pypdf`

\```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
\```
```

### マジックナンバーを使わない

```python
# 良い例（自己文書化）
# HTTPリクエストは通常30秒以内に完了する
REQUEST_TIMEOUT = 30

# 3回のリトライで信頼性と速度のバランスをとる
MAX_RETRIES = 3

# 悪い例
TIMEOUT = 47  # なぜ47？
RETRIES = 5   # なぜ5？
```

### MCP ツールは完全修飾名を使う

```markdown
# 良い例
BigQuery:bigquery_schema ツールを使用してテーブルスキーマを取得する。
GitHub:create_issue ツールを使用してIssueを作成する。

# 悪い例（ツールが見つからないエラーが発生する可能性）
bigquery_schema ツールを使用する。
```
