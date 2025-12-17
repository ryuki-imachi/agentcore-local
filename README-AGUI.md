# AgentCore Local - AG-UI Edition

Amazon Bedrock AgentCore Runtime をローカル環境で再現したプロジェクトです。Ollama、Strands Agents SDK、FastAPI、そして**CopilotKit (AG-UI)**を組み合わせて、完全にローカルで動作するAIエージェントシステムを構築しています。

## 🆕 AG-UI対応について

このバージョンでは、従来のStreamlitフロントエンドに代わって、**AG-UI (Agent UI Protocol)** に対応した **CopilotKit** を使用しています。

### AG-UIとは？

AG-UIは、エージェントとリッチなUIをつなぐためのオープンプロトコルです。AWS Strandsが公式にサポートしており、以下のような特徴があります：

- **リアルタイムストリーミング**: エージェントの応答をリアルタイムで表示
- **ツールベースのGenerative UI**: ツールの実行結果を視覚的に表示
- **状態共有**: エージェントとUIの間で状態を同期
- **標準化されたプロトコル**: 複数のフレームワークで共通のインターフェース

## システム構成

```
┌─────────────────────────────────────────────────────────────────┐
│  Docker Compose (WSL2)                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ UI           │  │ Agent        │  │ Ollama       │          │
│  │ Next.js      │──│ Strands SDK  │──│ qwen3:8b     │          │
│  │ CopilotKit   │  │ FastAPI      │  │ Port:11434   │          │
│  │ Port:3000    │  │ AG-UI API    │  └──────────────┘          │
│  └──────────────┘  │ Port:8000    │                            │
│                    └──────┬───────┘                            │
│                           │                                    │
│                    ┌──────▼───────┐                            │
│                    │ SQLite       │                            │
│                    │ (会話履歴)    │                            │
│                    └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

## 技術スタック

| コンポーネント | 技術 | バージョン |
|---|---|---|
| Agent Runtime | Python | 3.12 |
| パッケージ管理 | uv | latest |
| Agent Framework | Strands Agents SDK | latest |
| Web Framework | FastAPI | latest |
| LLM Server | Ollama | latest |
| LLM Model | qwen3 | 8b |
| **Frontend** | **Next.js + TypeScript** | **15.x** |
| **UI Framework** | **CopilotKit (AG-UI)** | **latest** |
| Database | SQLite | 3 |
| Container | Docker Compose | latest |

## セットアップ

### 1. プロジェクトの確認

```bash
cd agentcore-local
```

### 2. ディレクトリ構成

```
agentcore-local/
├── docker-compose.yml    # Docker Compose 設定
├── agent/                # Agent コンテナ
│   ├── Dockerfile
│   ├── main_agui.py     # AG-UI対応 FastAPI アプリケーション
│   ├── main.py          # レガシーAPI (後方互換性)
│   └── pyproject.toml   # Python 依存関係
├── ui/                   # UI コンテナ (NEW!)
│   ├── Dockerfile
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   └── src/
│       └── app/
│           ├── layout.tsx
│           ├── page.tsx
│           └── api/copilotkit/
│               └── route.ts  # CopilotKit APIルート
├── frontend/             # レガシー Streamlit (無効化)
└── data/                 # データ永続化
    └── conversations.db  # SQLite データベース
```

### 3. コンテナの起動

```bash
docker compose up -d
```

起動には数分かかる場合があります。

### 4. モデルのダウンロード（初回のみ）

```bash
docker compose exec ollama ollama pull qwen3:8b
```

### 5. 起動確認

```bash
# すべてのサービスが起動しているか確認
docker compose ps

# Ollama の確認
curl http://localhost:11434/

# Agent API の確認（AG-UI Ping）
curl http://localhost:8000/ping

# UI にアクセス
# http://localhost:3000
```

## 使用方法

### Web UI からの利用

1. ブラウザで http://localhost:3000 を開く
2. 右側にチャットパネルが表示される
3. メッセージを入力して送信
4. エージェントからの応答が表示される

### CopilotKit の機能

- **チャットUI**: サイドバー形式のチャットインターフェース
- **ストリーミング**: リアルタイムでレスポンスを表示（将来対応予定）
- **会話履歴**: スレッドごとに会話を管理
- **ツール実行**: エージェントがツールを使用して正確な情報を提供

## API リファレンス

### AG-UI Protocol エンドポイント

| エンドポイント | メソッド | 説明 |
|---|---|---|
| `/ping` | GET | AG-UI ヘルスチェック |
| `/invocations` | POST | AG-UI エージェント実行 |

### レガシーエンドポイント（後方互換性）

| エンドポイント | メソッド | 説明 |
|---|---|---|
| `/health` | GET | ヘルスチェック |
| `/chat` | POST | チャットメッセージの送信 |
| `/conversations` | GET | 会話一覧の取得 |

### AG-UI Invocations API

**リクエスト例**:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "今何時ですか？"
    }
  ],
  "threadId": "20240115143045123456"
}
```

**レスポンス例**:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "今何時ですか？"
    },
    {
      "role": "assistant",
      "content": "現在の時刻は2024年1月15日 14時30分45秒です。"
    }
  ],
  "threadId": "20240115143045123456"
}
```

## 設定とカスタマイズ

### 環境変数

#### Agent コンテナ

| 変数名 | デフォルト値 | 説明 |
|---|---|---|
| `OLLAMA_HOST` | `http://ollama:11434` | Ollama サーバーの接続先URL |
| `OLLAMA_MODEL` | `qwen3:8b` | 使用する LLM モデル |
| `AGENT_PORT` | `8000` | エージェントAPIのポート |
| `AGENT_MODULE` | `main_agui` | 使用するPythonモジュール |

#### UI コンテナ

| 変数名 | デフォルト値 | 説明 |
|---|---|---|
| `AGENT_URL` | `http://agent:8000/invocations` | Agent API の接続先URL |

### レガシー Streamlit UI の使用

従来のStreamlitフロントエンドを使用したい場合は、`docker-compose.yml` の該当セクションのコメントを外してください：

```yaml
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: agentcore-frontend
    ports:
      - "3001:3000"  # ポート3001で起動
    depends_on:
      - agent
    restart: unless-stopped
```

その後、コンテナを再起動：

```bash
docker compose up -d
```

Streamlit UI は http://localhost:3001 でアクセスできます。

## トラブルシューティング

### UI が起動しない

**確認手順**:

```bash
# UIコンテナのログを確認
docker compose logs ui -f
```

**よくある原因**:
- Node.jsのビルドエラー → ログでエラーメッセージを確認
- Agent APIへの接続失敗 → Agent が起動しているか確認

### Agent に接続できない

**確認手順**:

```bash
# Agent のヘルスチェック
curl http://localhost:8000/ping

# Agent のログを確認
docker compose logs agent -f
```

## 開発者向け情報

### ローカル開発（UI）

```bash
cd ui

# 依存関係のインストール
npm install

# 環境変数を設定
export AGENT_URL=http://localhost:8000/invocations

# 開発サーバーの起動
npm run dev
```

開発サーバーは http://localhost:3000 で起動します。

### ローカル開発（Agent）

```bash
cd agent

# uv のインストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係のインストール
uv sync

# 開発サーバーの起動（AG-UI版）
uv run uvicorn main_agui:app --reload --host 0.0.0.0 --port 8000
```

## 今後の拡張案

### AG-UI機能の拡張

- [ ] **ツールベースのGenerative UI**: ツールの実行結果を視覚的に表示
- [ ] **ストリーミングレスポンス**: リアルタイムで応答を表示
- [ ] **Human-in-the-Loop**: ツール実行前のユーザー承認
- [ ] **Frontend Actions**: UI側からエージェントにアクションを送信
- [ ] **共有状態**: エージェントとUIの状態を同期

### その他の機能

- [ ] **複数ツールの追加**: Web検索、計算機など
- [ ] **RAG対応**: ベクトルDBを使った情報検索
- [ ] **マルチエージェント**: 複数の専門エージェントの協調

## 参考リンク

- [Strands Agents SDK](https://github.com/strands-agents)
- [AG-UI Documentation](https://docs.ag-ui.com/)
- [CopilotKit](https://copilotkit.ai/)
- [CopilotKit + AWS Strands](https://www.copilotkit.ai/blog/aws-strands-agents-now-compatible-with-ag-ui)
- [AG-UI Integration Guide](https://strandsagents.com/latest/documentation/docs/community/integrations/ag-ui/)
