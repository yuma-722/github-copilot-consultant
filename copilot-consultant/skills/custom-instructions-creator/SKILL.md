---
name: custom-instructions-creator
description: カスタム指示ファイル(custom instructions)を設計・作成・レビューする。対象は .github/copilot-instructions.md（always-on）、.instructions.md（ファイルベース）、AGENTS.md、CLAUDE.md。YAML frontmatter（name/description/applyTo）やglobパターン設計も扱う。カスタム指示、コーディング規約、プロジェクト標準、instructions.md、copilot-instructions、applyTo、ファイルベース指示、always-on指示に言及したときに使用する。
---

# Custom Instructions 作成スキル（VS Code / GitHub Copilot）

このSkillは、プロジェクトや個人に合った **カスタム指示ファイル** を設計し、ワークスペースに配置する。

## 指示ファイルの種類と選び方

まず目的に応じて適切なファイル種別を選ぶ:

| 目的 | ファイル | 適用範囲 |
|------|---------|---------|
| プロジェクト全体のコーディング規約 | `.github/copilot-instructions.md` | 全リクエストに自動適用 |
| 言語・フレームワーク固有のルール | `.instructions.md` | `applyTo` パターンに一致するファイル作業時 |
| 複数AIエージェント共通の規約 | `AGENTS.md` | 全リクエストに自動適用 |
| Claude互換ツールとの共有 | `CLAUDE.md` | 全リクエストに自動適用 |
| 組織横断の標準 | GitHub Organization指示 | 組織内全リポジトリ |

**判断フロー:**

1. **全体に常時適用したい** → `copilot-instructions.md` または `AGENTS.md`
2. **ファイル種別ごとにルールを分けたい** → `.instructions.md` + `applyTo`
3. **Claude Codeなど他ツールとも共有したい** → `AGENTS.md` または `CLAUDE.md`
4. **組織全体で共有したい** → GitHub Organization指示

## 作成フロー

### 1) 目的と対象を明確化する

以下を整理する:

- **何を統一したいか**: コーディングスタイル、命名規約、技術スタック、アーキテクチャ方針、セキュリティ要件、ドキュメント基準
- **適用範囲**: プロジェクト全体か、特定のファイル種別・ディレクトリか
- **既存のルール**: リンター・フォーマッターが既に強制しているルールは書かない（非自明なルールに集中する）

### 2) ファイルを配置する

#### copilot-instructions.md（always-on）

```
.github/copilot-instructions.md
```

プロジェクト全体に適用される。1ファイルのみ。

#### .instructions.md（ファイルベース）

```
.github/instructions/<name>.instructions.md
```

YAML frontmatter で適用条件を制御する:

```yaml
---
name: 'Python Standards'
description: 'Python ファイルのコーディング規約'
applyTo: '**/*.py'
---
```

| フィールド | 必須 | 説明 |
|-----------|------|------|
| `name` | いいえ | UI表示名。省略時はファイル名 |
| `description` | いいえ | ホバー時の説明。タスクとのセマンティックマッチングにも使われる |
| `applyTo` | いいえ | グロブパターン。省略時は自動適用されない（手動添付は可能） |

#### AGENTS.md

```
AGENTS.md                    # ワークスペースルート（always-on）
src/frontend/AGENTS.md       # サブフォルダ（experimental）
```

サブフォルダ版は `chat.useNestedAgentsMdFiles` 設定で有効化する。

#### CLAUDE.md

```
CLAUDE.md                    # ワークスペースルート
.claude/CLAUDE.md            # .claude フォルダ
~/.claude/CLAUDE.md          # ユーザーホーム（全プロジェクト共通）
CLAUDE.local.md              # ローカル専用（VCS対象外）
```

### 3) 指示を記述する

**核心原則: 短く、具体的に、理由付きで**

- 各指示は単純な1文にする。複数の情報は箇条書きで分ける
- ルールの背景（なぜそうするか）を含める → AIがエッジケースで適切に判断できる
- 具体的なコード例で「推奨パターン」と「避けるべきパターン」を示す
- リンター・フォーマッターが既に強制するルールは省く

**良い例:**

```markdown
# コーディング規約

- `moment.js` ではなく `date-fns` を使用する（moment.js は非推奨でバンドルサイズが大きい）
- エラーハンドリングでは Result 型を使用する（例外スローは避ける）
- コンポーネントはクラスではなく関数コンポーネントで実装する

## 命名規約
- React コンポーネント: PascalCase（例: `UserProfile`）
- ユーティリティ関数: camelCase（例: `formatDate`）
- 定数: UPPER_SNAKE_CASE（例: `MAX_RETRY_COUNT`）
```

**悪い例:**

```markdown
# ルール
コードをきれいに書いてください。
変数名は分かりやすくしてください。
```

### 4) applyTo パターンの設計（.instructions.md 用）

よく使うグロブパターン:

| パターン | 対象 |
|---------|------|
| `**/*.py` | 全 Python ファイル |
| `**/*.{ts,tsx}` | 全 TypeScript / TSX ファイル |
| `**/*.test.*` | 全テストファイル |
| `src/frontend/**` | フロントエンドディレクトリ配下 |
| `**` | 全ファイル（description による条件付き適用時に使う） |

`applyTo` を省略すると自動適用されない。description のセマンティックマッチングか手動添付のみで使われる。

### 5) 複数ファイルの構成例

モノレポや大規模プロジェクトでの推奨構成:

```
.github/
├── copilot-instructions.md              # 全体共通（言語問わず）
└── instructions/
    ├── python-standards.instructions.md  # applyTo: '**/*.py'
    ├── typescript-react.instructions.md  # applyTo: 'src/frontend/**/*.{ts,tsx}'
    ├── api-conventions.instructions.md   # applyTo: 'src/api/**'
    ├── testing.instructions.md           # applyTo: '**/*.test.*'
    └── docs-writing.instructions.md      # applyTo: 'docs/**/*.md'
```

**注意:** 複数ファイルが同時に適用される場合、VS Code はすべてをチャットコンテキストに結合する（順序保証なし）。矛盾するルールを書かないように注意する。

### 6) 指示の優先順位

競合時の優先順位（高い順）:

1. 個人指示（ユーザーレベル）
2. リポジトリ指示（`copilot-instructions.md` / `AGENTS.md`）
3. 組織指示

### 7) 確認とデバッグ

- Chat ビューで **Configure Chat（歯車）> Chat Instructions** を開き、指示ファイルの一覧を確認する
- `/instructions` をチャット入力欄に入力して **Configure Instructions and Rules** メニューを開く
- **Diagnostics** ビュー（Chat ビュー右クリック > Diagnostics）で読み込み済みファイルとエラーを確認する
- チャット応答の **References** セクションで、どの指示ファイルが使われたか確認する

## 期待する出力

- `.github/copilot-instructions.md` および/または `.github/instructions/*.instructions.md`
- 必要に応じて `AGENTS.md` / `CLAUDE.md`
- 既存ファイルを変更する場合は、変更理由と影響範囲を短く添える

## 注意事項

- カスタム指示はインライン補完（エディタ入力中のサジェスト）には適用されない
- `.instructions.md` の `applyTo` がないファイルは自動適用されない
- 関連する設定: `chat.includeApplyingInstructions`（パターンベース）、`chat.includeReferencedInstructions`（Markdownリンク参照）、`chat.useAgentsMdFile`（AGENTS.md）
- prompt files や custom agents から指示ファイルを Markdown リンクで参照できる（指示の再利用に活用する）

## よくあるパターン

### プロジェクト初期設定

チャットで `/init` を実行すると、ワークスペースを解析して `copilot-instructions.md` を自動生成できる。生成後に内容を精査・調整する。

### フロントエンド / バックエンド分離

```
.github/instructions/
├── frontend.instructions.md   # applyTo: 'src/frontend/**'
└── backend.instructions.md    # applyTo: 'src/backend/**'
```

### テスト専用ルール

```yaml
---
name: 'Testing Guidelines'
description: 'テストファイルの記述ルール'
applyTo: '**/*.{test,spec}.{ts,tsx,js,jsx}'
---
# テストルール
- AAA パターン（Arrange-Act-Assert）で構成する
- テスト名は「何をテストし、何を期待するか」を日本語で記述する
- モックは最小限にし、可能なら実際の依存を使う
```

## 参照

- [VS Code カスタム指示ドキュメント](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [VS Code カスタマイズ概要](https://code.visualstudio.com/docs/copilot/customization/overview)
