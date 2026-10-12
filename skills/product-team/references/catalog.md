# 職能一覧

全体委任は[マネージャー](roles/manager.md)を起動する。以下の22職能はすべてマネージャー直下で、さらに委任しない。個別指定のときはホストから直接呼べる。担当者を増やすためでなく、必要な成果と独立した検証を得るために選ぶ。

| 呼び名 / ID | 責任・呼ぶ場面 | 定義 |
| --- | --- | --- |
| BizOps / bizops | 部門横断フロー、KPI、引き継ぎ | [BizOps](roles/bizops.md) |
| SalesOps / salesops | IS・FSの営業プロセス、CRM、案件管理の仕組み | [SalesOps](roles/salesops.md) |
| CS Ops / csops | 導入・定着・更新支援の標準化と検知の仕組み | [CS Ops](roles/csops.md) |
| IS / is | 見込み客の理解、接点づくり、商談化 | [インサイドセールス](roles/is.md) |
| FS / fs | 個別商談、提案、懸念への回答、次の行動 | [フィールドセールス](roles/fs.md) |
| プレセールス / presales | 技術適合、デモ、PoC、導入条件 | [プレセールス](roles/presales.md) |
| CS / cs | 顧客ごとの導入・活用・更新の支援 | [カスタマーサクセス](roles/cs.md) |
| マーケ / marketing | 対象市場、価値訴求、獲得施策と検証 | [マーケティング](roles/marketing.md) |
| PdM / pdm | 課題、優先度、範囲、受入条件 | [プロダクトマネージャー](roles/pdm.md) |
| UX / ux-designer | 利用者理解、情報設計、導線、操作フロー | [UXデザイナー](roles/ux-designer.md) |
| UI / ui-designer | 画面、視覚階層、コンポーネントと状態 | [UIデザイナー](roles/ui-designer.md) |
| 設計 / architect | 技術境界、API・データ契約、設計判断 | [設計エンジニア](roles/architect.md) |
| FE / frontend | 画面と操作の実装、APIとの接続 | [フロントエンド](roles/frontend.md) |
| BE / backend | 業務ロジック、API、永続化、権限の実装 | [バックエンド](roles/backend.md) |
| インフラ / infrastructure | 実行基盤、CI/CD、監視、復旧 | [インフラ](roles/infrastructure.md) |
| QA設計 / qa-planner | リスクと受入条件からテストケース設計 | [QA設計](roles/qa-planner.md) |
| QA実行・打鍵 / qa-runner | 実ブラウザ等の操作、手順ごとの検証と証拠 | [QA実行](roles/qa-runner.md) |
| セキュリティ / security | 認証、権限、テナント分離、情報保護の検証 | [セキュリティ](roles/security.md) |
| データ分析 / data-analyst | 指標、計測、効果検証、解釈 | [データ分析](roles/data-analyst.md) |
| ドキュメント担当 / technical-writer | 仕様・操作手順・FAQ・リリースノート | [テクニカルライター](roles/technical-writer.md) |
| 事業責任者 / business-owner | 収益・顧客価値・優先順位のレビュー | [事業責任者](roles/business-owner.md) |
| 経営者 / executive | 戦略、資源配分、事業リスクのレビュー | [経営者](roles/executive.md) |

## 選び方

- 受注後の導入改善: CS・CS Ops・SalesOpsで引き継ぎを調べ、変更が必要ならPdM・UX・実装・QAへつなぐ。
- UI改善: UX・UI・FEで必要な分担を決め、QA設計が操作ケースを作り、QA実行が動作を確認する。
- 技術導入の商談: FS・プレセールス。技術判断が残れば設計担当へ問い合わせる。
- 料金や事業方針: PdM・事業責任者、必要なら経営者・データ分析。実データなしで収益や効果を断定しない。
- ドキュメントのみ: 指定された職能を優先する。担当指定がない文書依頼ならライターを直接呼び、不足する根拠だけ実装担当やQAへ問い合わせる。全体開発を開始しない。

未知の職能をユーザーが指定した場合は目的・成果物・境界を短く定義して起動する。既存名へ無理に読み替えず、起動数・深さ・権限の共通契約を守る。
