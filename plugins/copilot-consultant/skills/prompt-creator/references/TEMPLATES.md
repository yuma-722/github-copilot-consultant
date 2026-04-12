# Prompt file テンプレ集（.prompt.md）

このファイルは `.github/prompts/*.prompt.md` の雛形を置く。

## 最小テンプレ（説明だけ）

```md
---
description: ここに prompt の目的を書く（例: PR をレビューする）
---

# 目的

- ここに期待する成果を書く

# 手順

1. 入力（チャットの追加文/選択範囲/ファイル）を確認する
2. 期待する出力形式で回答する
```

## 引数入力を使うテンプレ（${input:...}）

```md
---
description: 指定された条件で要約する
argument-hint: topic=... format=... (例: topic=設計 format=箇条書き)
---

次の条件で要約する:
- topic: ${input:topic}
- format: ${input:format}

対象:
${selection}

出力は ${input:format} に従う。
```

## ツールを絞るテンプレ（tools）

```md
---
description: 変更差分をチェックして要点をまとめる
agent: agent
tools:
  - read_file
  - grep_search
  - get_changed_files
argument-hint: scope=staged|unstaged
---

次を実施する:
1. ${input:scope} の変更ファイルを列挙する
2. 変更の意図を推測せず、観測できる事実として要約する
3. リスク（破壊的変更/互換性/セキュリティ）を短く列挙する
```

## 参照リンクを使うテンプレ（規約の重複を避ける）

```md
---
description: ドキュメントを規約に沿って更新する
---

必ずこのプロジェクトの指示に従う:
- [.github/copilot-instructions.md](../copilot-instructions.md)

対象ファイル:
- ${file}

実施:
- 既存の文章のトーンを崩さずに、必要最小限の追記/修正を行う
- 変更点を最後に箇条書きでまとめる
```

## 作成チェックリスト

- `/` で呼び出す **単発タスク** になっている（大きすぎない）
- 入力（追加文/selection/input variables）が明確
- 出力形式が明確（見出し/箇条書き/JSON など）
- 既存の規約はリンク参照し、prompt file に重複記載しない
- `tools` を指定する場合、足りないツールで詰まらない（必要最小限 + 実行可能）
- エディタ実行（再生）で試して、必要なら `argument-hint` を改善する
