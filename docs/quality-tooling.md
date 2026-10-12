# CIと評価ハーネスの採用方針

確認日: 2026-10-13。このリポジトリは日本語のスキル文書が主な成果物で、Pythonの検証コードを含む。必須とおすすめを実装対象とし、その他は導入条件を残す。

## 必須

| ツール | 用途・採用理由 | 実装・実行方法 |
| --- | --- | --- |
| [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) | Markdownの見出し・リスト・コードブロックなどの構造を統一する | `npm run lint:markdown`。日本語の長い行と表の列幅は強制しない |
| [actionlint](https://github.com/rhysd/actionlint) | Workflowのキー、式、依存ジョブなどを静的検証する | Lintジョブで実行。バージョンを固定する |
| [Agent Skills仕様](https://agentskills.io/specification)に基づくPython検証 | メタデータ、参照欠落、パッケージ外への依存を検出する | `scripts/validate_skills.py`と`unittest`。既存コードを再利用する |
| [skills CLI](https://github.com/vercel-labs/skills) | 実際の配布経路で、CodexとClaude Codeへ全ファイルが届くことを確認する | 変更中のチェックアウトを一時ディレクトリへ導入し、内容を比較する |
| Gatekeeper / GitHub ruleset | CIが失敗・スキップされたPRのマージを防ぐ | 4ジョブがすべて成功したときだけ成功。mainの必須チェックにする |

## おすすめとして採用

| ツール | 用途・採用理由 | 実装・実行方法 |
| --- | --- | --- |
| [textlint](https://github.com/textlint/textlint)＋[ja-technical-writing](https://github.com/textlint-ja/textlint-rule-preset-ja-technical-writing) | 日本語の長すぎる文、助詞の重複、曖昧な表現などを検出する | `npm run lint:text`。ルールの例外は用途を説明して設定する |
| [textlint-rule-prh](https://github.com/textlint-rule/textlint-rule-prh) | 製品名・技術用語の表記揺れを抑える | `prh.yml`でGitHub、Playwrightなどの表記を管理する |
| [Ruff](https://docs.astral.sh/ruff/) | 検証コードの未使用変数、import、書式の問題を検出する | `ruff check`と`ruff format --check` |
| [Gitleaks](https://github.com/gitleaks/gitleaks) | サンプルや作業履歴に混入した秘密情報を検出する | Secret scanジョブでGit履歴を検査。ログはredactする |
| [Dependabot](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference) | lint・ハーネス・Actionsの更新を継続する | npm、pip、GitHub Actionsを週次確認。自動マージは設定しない |
| [promptfoo](https://www.promptfoo.dev/docs/configuration/parameters/) | スキルあり・なしの計画結果を、同じシナリオと判定条件で比較する | 7ケース、JSON判定、失敗例のテスト、fixtureによるハーネス検証、明示したモデルでの手動評価 |

通常のPRでは外部のモデルを呼び出さない。promptfooのfixtureはハーネスの配線確認であり、スキルの行動品質を証明しない。実モデル評価は別途モデルと認証を指定して実行する。

## その他・今回は採用しないもの

| ツール | 用途 | 今回見送る理由・導入条件 |
| --- | --- | --- |
| [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) | Agent Skillsの参照バリデーター | 公式READMEがデモ用途と明記している。唯一の本番ゲートにはせず、仕様調査の参考とする |
| [lychee](https://github.com/lycheeverse/lychee) | 外部URLのリンク切れ検査 | 外部サイトの制限や一時障害でPRを止めやすい。外部リンクが増えたら週次・手動実行として導入する |
| [typos](https://github.com/crate-ci/typos) | 英単語や識別子の誤字検出 | 現状は日本語が中心で、製品名はprhで扱う。英語文書が増えたら導入する |
| [zizmor](https://github.com/zizmorcore/zizmor) | GitHub Actionsのセキュリティ静的解析 | 現状はread-onlyのPR検証で、権限とAction SHAを固定する。公開・クラウド認証などのWorkflowを追加するときに再評価する |
| [yamllint](https://github.com/adrienverge/yamllint) | 汎用YAMLの書式検査 | Workflowはactionlint、スキル表示設定はPythonで検証する。対象YAMLの種類が増えたら追加する |
| [Prettier](https://prettier.io/docs/) | 文書・設定・コードの自動整形 | Markdownはmarkdownlint、PythonはRuffを採用する。JavaScriptが増えたら対象を限定して追加する |
| [CodeQL](https://codeql.github.com/docs/) | コードのセキュリティ解析 | 文書中心で実行コードは小さい。外部入力を処理するアプリやサービスを追加するときに再評価する |
| Codex／Claude Codeによる実ツールE2E | 実委任、編集、ブラウザ操作の確認 | CLI認証、隔離環境、実行コストが必要。今回の計画評価とは別に、小さなテスト用リポジトリを使う段階で導入する |

## Gatekeeperの扱い

`Lint`、`Skill validation`、`Secret scan`、`Evaluation harness smoke`の結果を集約する。成功以外の状態、欠けたジョブ、想定外のジョブは拒否する。Workflow全体にpathフィルターを付けず、文書だけのPRでもゲートを実行する。

mainにはGitHub Actionsを送信元とする`Gatekeeper`を必須登録する。PR経由、最新mainへの追従、強制push禁止、削除禁止、バイパスなしを維持する。CIの合格は人間の承認を代替しない。承認レビュー数は別の設定であり、このCI追加では変更しない。

依存はlockfileまたはバージョンで固定し、ActionsはSHAで固定する。Goツールの固定バージョンはWorkflowに記載するため、更新時はリリース内容を確認して手動で変更する。
