---
name: custom-agents-creator
description: VS Code と GitHub Copilot の Custom Agents（カスタムエージェント）を設計・作成・レビューする。`.agent.md`、`.github/agents`、YAML frontmatter（name/description/tools/agents/handoffs/model/target/user-invocable/disable-model-invocation）、subagents（サブエージェント）や handoffs を扱うタスク、または Copilot coding agent の custom agents configuration に言及したときに使用する。
---

# Custom Agents 作成スキル（VS Code / GitHub Copilot）

このSkillは、目的に合った **Custom Agent（.agent.md）** を最小権限で設計し、再利用しやすい形でワークスペースに配置する。

## 作成フロー

### 1) まず目的と適切な「カスタマイズ手段」を決める

次のどれが最小かを判断してから着手する。

- **Always-on / file-based instructions**: 常に守るコーディング規約やディレクトリ別ルール
- **Prompt files（スラッシュコマンド）**: 単発の定型作業
- **Agent Skills**: 何度も繰り返すワークフローや参照資料＋スクリプト同梱
- **Custom Agents**: 役割（人格）＋ツール制限＋（必要なら）handoffs / subagents で段階ワークフロー

迷う場合は「役割を分けたい」「ツール制限したい」「handoff で次工程へ誘導したい」なら Custom Agents を選ぶ。

### 1.5) Custom Agents と他機能の「役割分担」を設計する

Custom Agents を選んだ場合でも、すべてを agent 本文に詰め込まず、他のカスタマイズ機能に委譲して**薄く保つ**。

- **Always-on / file-based instructions**: 規約・禁止事項・出力形式など「常に守るべきこと」は instructions に寄せる（agent 本文は繰り返さない）
- **Prompt files（/コマンド）**: 人が明示的に呼び出す定型手順は prompt に寄せる（agent からは「実行する /コマンド名」を案内）
- **Agent Skills**: 参照資料・チェックリスト・スクリプト付きの“何度も回す”ワークフローは skills に寄せる（agent は入口/統括に徹する）
- **Hooks**: 「毎回自動で走ってほしい」検査・整形・安全策は hooks に寄せる（必要なら提案する）

スキル側でやるべきことは、agent を生成するときに **(a) 何を前提にするか** と **(b) 何に委譲するか** を明示できるようにすること。

### 2) 置き場所と対象環境を確定する

- **VS Code（ローカル）で使う**: ワークスペースの `.github/agents/*.agent.md`
- **Claude互換も欲しい**: `.claude/agents/*.md` も検討（ただしこのSkillはVS Code形式を優先）
- **GitHub Copilot coding agent（github.com）で使う**: GitHubのcustom agent仕様（IDEと差分あり）を前提にする

リファレンスは参照: [Custom Agents 要点](references/custom-agents.md)

### 3) Agentの設計（最小権限）

- まず **職務** を1つに絞る（例: 計画、実装、レビュー、ドキュメント、テスト）。
- `tools` は **必要最小限** にする。
  - 例: 計画/調査は `['read', 'search']` を基本にして `edit/execute` を外す。
  - 実装は `edit` を許可し、必要なら `execute` を追加する。
- subagents を使う場合は、Coordinator（調整役）と Worker（専門役）に分け、Coordinator側で `agents` を絞る。
  - `agents` は「subagent として呼び出してよい Custom Agents の許可リスト」。利用するには通常 `tools` に `agent` が必要（詳細は [Custom Agents 要点](references/custom-agents.md) の subagents 節）。

### 4) `.agent.md` を生成する

- ファイル名（例）: `.github/agents/<agent-id>.agent.md`
- YAML frontmatter は **最低限 `name` と `description`** を入れる。
- 可能なら `argument-hint` を入れて入力の期待値を明確にする（VS Code向け）。

雛形は参照: [テンプレート集](references/templates.md)

#### （推奨）連携機能を前提として明記する

agent 本文に、次を短く入れておくと運用がブレにくい。

- **前提**: 「このリポジトリの instructions を優先する」など
- **委譲**: 「定型作業は prompt files を使う（該当する /コマンドを案内する）」など
- **境界**: 「この agent は統括のみ。実装は Implementer に handoff」など

例（本文に入れる指示の型）:

- リポジトリ内の instructions（always-on / file-based）を最優先する。重複して規約を書き直さない。
- 定型の単発作業は prompt files を利用する。必要ならユーザーに実行すべき `/...` コマンドを提示する。
- 繰り返しワークフローや参照資料が必要なら Agent Skills を利用する（既存がなければ作成を提案する）。
- 自動化が必要なら hooks を提案する（ただし過剰な自動化は避け、最小の範囲にする）。

### 5) 動作確認と調整

- VS Code: Chatビューの **Diagnostics** で、読み込まれている custom agents / skills / instructions を確認する。
- ツール不足/過剰があれば `tools` を見直す。
- 役割が広すぎる場合は agent を分割し、handoffs で導線を作る。

## 期待する出力

- `.github/agents/*.agent.md`（必要なら複数: Planner / Implementer / Reviewer など）
- 連携のために新規作成が必要なら、最小の追加案（例: `.github/prompts/*.prompt.md` や `.github/skills/<skill-name>/`）
- 既存ファイルを変更する場合は、変更理由と影響範囲を短く添える

## 注意事項

- 未対応の frontmatter は実行環境によって無視されることがある（困ったら `name` / `description` / `tools` を核にして組む）。
- `infer` は非推奨/互換用途になりつつある。VS Codeでは `user-invocable` / `disable-model-invocation` を優先する。

## よくあるパターン

- **Planning → Implementation → Review** の3段: planning agent は read/search のみ、implementation は edit/execute、review は read/search。
- **多観点レビュー**: correctness / security / quality を subagents で並列実行して最後に統合する。
