# AgentCore Local

Amazon Bedrock AgentCore Runtime をローカル環境で再現したプロジェクトです。Ollama、Strands Agents SDK、FastAPI、そして **CopilotKit (AG-UI)** を組み合わせて、完全にローカルで動作するAIエージェントシステムを構築しています。

## 目次

- [プロジェクト概要](#プロジェクト概要)
- [AG-UI対応について](#ag-ui対応について)
- [システム構成](#システム構成)
- [技術スタック](#技術スタック)
- [前提条件](#前提条件)
- [セットアップ](#セットアップ)
- [使用方法](#使用方法)
- [API リファレンス](#api-リファレンス)
- [設定とカスタマイズ](#設定とカスタマイズ)
- [トラブルシューティング](#トラブルシューティング)
- [開発者向け情報](#開発者向け情報)
- [レガシー版について](#レガシー版について)
- [今後の拡張案](#今後の拡張案)
- [参考リンク](#参考リンク)

## プロジェクト概要

このプロジェクトは、以下の特徴を持つローカルAIエージェントシステムです：

- **完全ローカル実行**: インターネット接続不要で、すべての処理がローカル環境で完結
- **AG-UI プロトコル対応**: 標準化されたAgent UI Protocolによる柔軟なUI連携
- **モダンなUI**: Next.js + TypeScript + CopilotKitによるリッチなユーザー体験
- **プライバシー重視**: データは外部に送信されず、すべてローカルに保存
- **拡張可能**: ツール（関数）を追加することで、エージェントの機能を簡単に拡張可能
- **RESTful API**: FastAPIベースのAPIにより、他のアプリケーションとの連携が容易

### ユースケース

- プライバシーが重要な社内チャットボット
- ローカル環境でのAIエージェント開発・検証
- オフライン環境でのAI活用
- Amazon Bedrock AgentCoreのローカル開発環境

## AG-UI対応について

このバージョンでは、**AG-UI (Agent UI Protocol)** に対応した **CopilotKit** を使用しています。

### AG-UIとは？

AG-UIは、エージェントとリッチなUIをつなぐためのオープンプロトコルです。AWS Strandsが公式にサポートしており、以下のような特徴があります：

- **標準化されたプロトコル**: 複数のフレームワークで共通のインターフェース
- **リアルタイムストリーミング**: エージェントの応答をリアルタイムで表示（将来対応予定）
- **ツールベースのGenerative UI**: ツールの実行結果を視覚的に表示（将来対応予定）
- **状態共有**: エージェントとUIの間で状態を同期

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

### コンポーネント説明

#### UI (Next.js + CopilotKit)
- **役割**: ユーザーインターフェースの提供
- **技術**: Next.js 16 + TypeScript + CopilotKit
- **ポート**: 3000
- **機能**:
  - AG-UI プロトコル対応チャットUI
  - サイドバー形式のチャットインターフェース
  - リアルタイムレスポンス表示
  - ツール実行の可視化

#### Agent (Strands Agents SDK + FastAPI)
- **役割**: AIエージェントの実行とAG-UI API提供
- **技術**: Python 3.12 + FastAPI + Strands Agents SDK + ag_ui_strands
- **ポート**: 8000
- **機能**:
  - LLMとの対話処理
  - ツール（関数）の実行
  - AG-UI プロトコルのイベントストリーミング
  - RESTful API の提供

#### Ollama
- **役割**: ローカルLLMサーバー
- **技術**: Ollama + qwen3:8b モデル
- **ポート**: 11434
- **機能**:
  - 大規模言語モデル（LLM）の推論実行
  - GPU アクセラレーション対応
  - 複数モデルの切り替え対応

#### SQLite
- **役割**: データ永続化
- **保存データ**:
  - 会話（Conversation）情報
  - メッセージ（Message）履歴
- **保存場所**: `./data/conversations.db`

## 技術スタック

| コンポーネント | 技術 | バージョン |
|---|---|---|
| Agent Runtime | Python | 3.12 |
| パッケージ管理 | uv | latest |
| Agent Framework | Strands Agents SDK | latest |
| Web Framework | FastAPI | latest |
| LLM Server | Ollama | latest |
| LLM Model | qwen3 | 8b |
| **Frontend** | **Next.js + TypeScript** | **16.x** |
| **UI Framework** | **CopilotKit (AG-UI)** | **1.50.0** |
| **AG-UI Integration** | **ag_ui_strands** | **0.1.0** |
| Database | SQLite | 3 |
| Container | Docker Compose | latest |

## 前提条件

### 必須

- **Docker Desktop** (version 20.10 以上)
- **Docker Compose** (version 2.0 以上)
- **ディスク空き容量**: 最低 10GB（モデルサイズ約5GB + コンテナイメージ）

### オプション（GPU 使用時）

- **NVIDIA GPU** (CUDA対応)
- **nvidia-container-toolkit**
- **WSL2 環境**（Windowsの場合）

### GPU を使用しない場合

GPU がない環境でも動作しますが、推論速度が遅くなります。`docker-compose.yml` から GPU 設定を削除してください。

```yaml
# 以下の部分を削除またはコメントアウト
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

## セットアップ

### 1. プロジェクトの取得

```bash
cd agentcore-local
```

### 2. ディレクトリ構成の確認

```
agentcore-local/
├── docker-compose.yml    # Docker Compose 設定
├── agent/                # Agent コンテナ
│   ├── Dockerfile
│   ├── main_agui.py     # AG-UI対応 FastAPI アプリケーション
│   └── pyproject.toml   # Python 依存関係
├── ui/                   # UI コンテナ
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
├── data/                 # データ永続化（自動作成）
│   └── conversations.db  # SQLite データベース
└── legacy/               # レガシー版（Streamlit等）
    ├── frontend-streamlit/
    ├── frontend-old/
    └── agent-main-old.py
```

### 3. コンテナの起動

```bash
docker compose up -d
```

起動には数分かかる場合があります。以下のコマンドでログを確認できます：

```bash
docker compose logs -f
```

### 4. モデルのダウンロード（初回のみ）

```bash
docker compose exec ollama ollama pull qwen3:8b
```

**注意事項**:
- モデルサイズは約 5GB です
- ダウンロード時間はネットワーク速度に依存します（目安: 10-30分）
- ダウンロード状況は進捗バーで表示されます

### 5. 起動確認

すべてのサービスが正常に起動しているか確認：

```bash
docker compose ps
```

正常な場合、すべてのサービスが `Up` 状態になります。

### 6. ヘルスチェック

各サービスが正常に動作しているか確認：

```bash
# Ollama の確認
curl http://localhost:11434/

# Agent API の確認（AG-UI）
curl http://localhost:8000/ping

# UI の確認（ブラウザで開く）
# http://localhost:3000
```

## 使用方法

### Web UI からの利用

1. ブラウザで http://localhost:3000 を開く
2. 右側にチャットパネルが表示される
3. メッセージを入力して送信
4. エージェントからの応答が表示される

### CopilotKit の機能

- **チャットUI**: サイドバー形式の洗練されたチャットインターフェース
- **会話履歴**: スレッドごとに会話を管理
- **ツール実行**: エージェントがツールを使用して正確な情報を提供
- **ストリーミング**: リアルタイムでレスポンスを表示（将来対応予定）

### 使用例

#### 例1: 現在時刻の取得

```
ユーザー: 今何時ですか？
```

エージェントは `current_time` ツールを自動的に使用して、正確な現在時刻を返します。

```
エージェント: 現在の時刻は 2024年1月15日 14時30分45秒 です。
```

#### 例2: 通常の会話

```
ユーザー: こんにちは！
エージェント: こんにちは！何かお手伝いできることはありますか？

ユーザー: Pythonについて教えて
エージェント: Pythonは、読みやすく書きやすいプログラミング言語です...
```

## API リファレンス

### AG-UI Protocol エンドポイント

| エンドポイント | メソッド | 説明 |
|---|---|---|
| `/ping` | GET | AG-UI ヘルスチェック |
| `/invocations` | POST | AG-UI エージェント実行 |

#### GET /ping

AG-UI プロトコルのヘルスチェック。

**レスポンス例**:
```json
{
  "status": "ok",
  "model": "qwen3:8b"
}
```

#### POST /invocations

AG-UI プロトコルに準拠したエージェント実行エンドポイント。

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

**レスポンス**: Server-Sent Events (SSE) 形式でイベントストリームを返します。

### レガシーエンドポイント（後方互換性）

| エンドポイント | メソッド | 説明 |
|---|---|---|
| `/health` | GET | ヘルスチェック |

#### GET /health

レガシーAPI用のヘルスチェック。

**レスポンス例**:
```json
{
  "status": "healthy",
  "model": "qwen3:8b"
}
```

### API ドキュメント

FastAPI が提供する自動生成ドキュメントも利用できます：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 設定とカスタマイズ

### 環境変数

#### Agent コンテナ

`docker-compose.yml` で設定されている環境変数：

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

### モデルの変更

#### 利用可能なモデル

Ollama で利用可能な主なモデル：

| モデル名 | サイズ | 特徴 |
|---|---|---|
| qwen3:8b | 5GB | バランス型（デフォルト） |
| qwen3:14b | 9GB | 高性能 |
| llama3:8b | 4.7GB | Meta製、汎用性が高い |
| gemma:7b | 5GB | Google製、高速 |

#### 変更手順

1. `docker-compose.yml` の環境変数を編集：

```yaml
services:
  agent:
    environment:
      - OLLAMA_MODEL=qwen3:14b  # モデル名を変更
```

2. 新しいモデルをダウンロード：

```bash
docker compose exec ollama ollama pull qwen3:14b
```

3. Agent コンテナを再起動：

```bash
docker compose restart agent
```

### システムプロンプトのカスタマイズ

[agent/main_agui.py](agent/main_agui.py) の `system_prompt` を編集することで、エージェントの振る舞いをカスタマイズできます。

```python
system_prompt = """あなたは親切で知識豊富なAIアシスタントです。
ユーザーの質問に日本語で丁寧に答えてください。
現在の日時を聞かれた場合は、current_timeツールを使用して正確な時刻を取得してください。
回答は簡潔かつ分かりやすくしてください。"""
```

変更後はコンテナの再ビルドが必要です：

```bash
docker compose up -d --build agent
```

### ツール（関数）の追加

新しいツールを追加することで、エージェントの機能を拡張できます。

例: 計算機能の追加

```python
# agent/main_agui.py

def calculator(expression: str) -> str:
    """数式を評価して結果を返す"""
    try:
        result = eval(expression)  # 本番環境では安全な評価方法を使用
        return f"計算結果: {result}"
    except Exception as e:
        return f"計算エラー: {str(e)}"

# Agent初期化時に追加
strands_agent = Agent(
    model=ollama_model,
    tools=[current_time, calculator],  # ツールを追加
    system_prompt=system_prompt,
)
```

## トラブルシューティング

### UI が起動しない

**症状**: ブラウザで http://localhost:3000 にアクセスできない

**確認手順**:

```bash
# UIコンテナのログを確認
docker compose logs ui -f

# UIコンテナの状態を確認
docker compose ps ui
```

**よくある原因**:
- Node.jsのビルドエラー → ログでエラーメッセージを確認
- Agent APIへの接続失敗 → Agent が起動しているか確認
- ポート3000が使用中 → `docker compose down` で停止してから再起動

### Agent に接続できない

**症状**: UI に「接続エラー」が表示される

**確認手順**:

```bash
# Agent のヘルスチェック
curl http://localhost:8000/ping

# Agent のログを確認
docker compose logs agent -f
```

### Ollama に接続できない

**症状**: Agent が「Ollama に接続できません」というエラーを返す

**確認手順**:

1. Ollama コンテナが起動しているか確認：
```bash
docker compose ps ollama
```

2. Ollama のログを確認：
```bash
docker compose logs ollama
```

3. Ollama のヘルスチェック：
```bash
curl http://localhost:11434/
```

期待される応答: `Ollama is running`

4. モデルがダウンロードされているか確認：
```bash
docker compose exec ollama ollama list
```

**解決方法**:

- モデルが表示されない場合はダウンロード：
```bash
docker compose exec ollama ollama pull qwen3:8b
```

- コンテナを再起動：
```bash
docker compose restart ollama agent
```

### GPU が認識されない

**症状**: GPU を使用したいが CPU で動作している

**確認手順**:

1. NVIDIA ドライバが正しくインストールされているか確認：
```bash
nvidia-smi
```

2. nvidia-container-toolkit がインストールされているか確認：
```bash
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

**解決方法**:

- nvidia-container-toolkit をインストール（Ubuntu/WSL2）：
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

- Docker Desktop の設定で GPU サポートを有効化

### レスポンスが遅い

**症状**: チャットの応答に時間がかかる

**原因と対策**:

1. **GPU を使用していない**: GPU を有効化することで大幅に高速化
2. **モデルサイズが大きい**: より小さなモデルに変更（例: qwen3:8b → gemma:7b）
3. **システムリソース不足**: メモリやCPUの使用状況を確認

```bash
# システムリソースの確認
docker stats
```

## 開発者向け情報

### ローカル開発環境のセットアップ

Docker を使用せずにローカルで開発する場合：

#### UI の開発

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

#### Agent の開発

```bash
cd agent

# uv のインストール（未インストールの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係のインストール
uv sync

# 開発サーバーの起動（AG-UI版）
uv run uvicorn main_agui:app --reload --host 0.0.0.0 --port 8000
```

### コードの編集とホットリロード

開発時は、ローカルのコードをコンテナにマウントすることでホットリロードが可能です。

`docker-compose.yml` に以下を追加：

```yaml
services:
  agent:
    volumes:
      - ./data:/app/data
      - ./agent:/app  # 追加: コードをマウント
    environment:
      - RELOAD=true   # 追加: ホットリロード有効化
```

### ログの確認方法

```bash
# すべてのコンテナのログ
docker compose logs -f

# 特定のコンテナのログ
docker compose logs -f agent
docker compose logs -f ollama
docker compose logs -f ui

# 最新100行のログ
docker compose logs --tail=100 agent
```

### パフォーマンスモニタリング

```bash
# コンテナのリソース使用状況をリアルタイム表示
docker stats

# Ollama のメトリクス（実験的機能）
curl http://localhost:11434/api/metrics
```

## レガシー版について

従来の Streamlit ベースのフロントエンドは `legacy/` ディレクトリに移動されています：

- `legacy/frontend-streamlit/` - Streamlit版フロントエンド
- `legacy/frontend-old/` - 旧フロントエンド
- `legacy/agent-main-old.py` - AG-UI非対応のバックエンド

これらは参考用に保存されていますが、新しいプロジェクトでは AG-UI 版の使用を推奨します。

## 今後の拡張案

### AG-UI機能の拡張

- [ ] **ツールベースのGenerative UI**: ツールの実行結果を視覚的に表示
- [ ] **ストリーミングレスポンス**: リアルタイムで応答を表示
- [ ] **Human-in-the-Loop**: ツール実行前のユーザー承認
- [ ] **Frontend Actions**: UI側からエージェントにアクションを送信
- [ ] **共有状態**: エージェントとUIの状態を同期

### その他の機能

- [ ] **複数ツールの追加**:
  - Web 検索ツール
  - 計算機ツール
  - ファイル読み込みツール
- [ ] **ファイルアップロード対応**: PDFやテキストファイルの内容を解析
- [ ] **RAG (Retrieval-Augmented Generation)**: ベクトルDBを使った情報検索
- [ ] **マルチエージェント構成**: 複数の専門エージェントの協調動作
- [ ] **音声入出力対応**: 音声認識・音声合成の統合
- [ ] **OpenTelemetry によるトレーシング**: パフォーマンス分析とデバッグ
- [ ] **認証・認可機能**: マルチユーザー対応
- [ ] **Kubernetes デプロイ対応**: 本番環境での運用

## 参考リンク

- [Strands Agents SDK](https://strandsagents.com/)
- [AG-UI Protocol](https://docs.ag-ui.com/)
- [CopilotKit](https://copilotkit.ai/)
- [CopilotKit + AWS Strands](https://www.copilotkit.ai/blog/aws-strands-agents-now-compatible-with-ag-ui)
- [AG-UI Integration Guide](https://strandsagents.com/latest/documentation/docs/community/integrations/ag-ui/)
- [Ollama](https://ollama.ai/)
- [FastAPI](https://fastapi.tiangolo.com/)
