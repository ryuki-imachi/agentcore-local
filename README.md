# AgentCore Local

Amazon Bedrock AgentCore Runtime をローカル環境で再現したプロジェクトです。Ollama、Strands Agents SDK、FastAPI、Streamlit を組み合わせて、完全にローカルで動作するAIエージェントシステムを構築しています。

## 目次

- [プロジェクト概要](#プロジェクト概要)
- [システム構成](#システム構成)
- [技術スタック](#技術スタック)
- [前提条件](#前提条件)
- [セットアップ](#セットアップ)
- [使用方法](#使用方法)
- [API リファレンス](#api-リファレンス)
- [設定とカスタマイズ](#設定とカスタマイズ)
- [トラブルシューティング](#トラブルシューティング)
- [開発者向け情報](#開発者向け情報)
- [今後の拡張案](#今後の拡張案)
- [ライセンス](#ライセンス)

## プロジェクト概要

このプロジェクトは、以下の特徴を持つローカルAIエージェントシステムです：

- **完全ローカル実行**: インターネット接続不要で、すべての処理がローカル環境で完結
- **プライバシー重視**: データは外部に送信されず、すべてローカルに保存
- **拡張可能**: ツール（関数）を追加することで、エージェントの機能を簡単に拡張可能
- **会話履歴の永続化**: SQLiteを使用して会話履歴を保存し、過去の対話を参照可能
- **RESTful API**: FastAPIベースのAPIにより、他のアプリケーションとの連携が容易

### ユースケース

- プライバシーが重要な社内チャットボット
- ローカル環境でのAIエージェント開発・検証
- オフライン環境でのAI活用
- Amazon Bedrock AgentCoreのローカル開発環境

## システム構成

```
┌─────────────────────────────────────────────────────────────────┐
│  Docker Compose (WSL2)                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Frontend     │  │ Agent        │  │ Ollama       │          │
│  │ Streamlit    │──│ Strands SDK  │──│ qwen3:8b     │          │
│  │ Port:3000    │  │ FastAPI      │  │ Port:11434   │          │
│  └──────────────┘  │ Port:8000    │  └──────────────┘          │
│                    └──────┬───────┘                            │
│                           │                                    │
│                    ┌──────▼───────┐                            │
│                    │ SQLite       │                            │
│                    │ (会話履歴)    │                            │
│                    └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

### コンポーネント説明

#### Frontend (Streamlit)
- **役割**: ユーザーインターフェースの提供
- **技術**: Python + Streamlit
- **ポート**: 3000
- **機能**:
  - チャット形式のUI
  - メッセージ送信・受信
  - 会話履歴の表示

#### Agent (Strands Agents SDK + FastAPI)
- **役割**: AIエージェントの実行とAPI提供
- **技術**: Python 3.12 + FastAPI + Strands Agents SDK
- **ポート**: 8000
- **機能**:
  - LLMとの対話処理
  - ツール（関数）の実行
  - 会話履歴の管理（SQLite）
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
| Frontend | Streamlit | latest |
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
│   ├── main.py          # FastAPI アプリケーション
│   └── pyproject.toml   # Python 依存関係
├── frontend/             # Frontend コンテナ
│   ├── Dockerfile
│   ├── app.py           # Streamlit アプリケーション
│   └── pyproject.toml
└── data/                 # データ永続化（自動作成）
    └── conversations.db  # SQLite データベース
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

# Agent API の確認
curl http://localhost:8000/health

# Frontend の確認（ブラウザで開く）
# http://localhost:3000
```

## 使用方法

### Web UI からの利用

1. ブラウザで http://localhost:3000 を開く
2. 画面下部のテキストボックスにメッセージを入力
3. 「送信」ボタンをクリック、または Enter キーを押す
4. エージェントからの応答が表示される

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

#### 例3: コンテキストを持った会話

エージェントは会話履歴を保持しているため、前の発言を踏まえた応答が可能です。

```
ユーザー: 東京の天気について教えて
エージェント: 申し訳ございません。現在、天気情報を取得するツールは...

ユーザー: では、時刻を教えて
エージェント: 現在の時刻は...
```

### API からの利用

#### cURL を使用した例

```bash
# チャットメッセージの送信
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "こんにちは！今何時ですか？"
  }'

# 会話一覧の取得
curl http://localhost:8000/conversations

# 特定の会話の取得
curl http://localhost:8000/conversations/{conversation_id}
```

#### Python を使用した例

```python
import requests

# チャット送信
response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "こんにちは！"}
)
result = response.json()
print(f"Response: {result['response']}")
print(f"Conversation ID: {result['conversation_id']}")

# 会話履歴の取得
conversations = requests.get(
    "http://localhost:8000/conversations"
).json()
for conv in conversations:
    print(f"{conv['title']} - {conv['updated_at']}")
```

## API リファレンス

### エンドポイント一覧

| エンドポイント | メソッド | 説明 |
|---|---|---|
| `/health` | GET | ヘルスチェック |
| `/chat` | POST | チャットメッセージの送信 |
| `/conversations` | GET | 会話一覧の取得 |
| `/conversations/{id}` | GET | 特定の会話の詳細取得 |
| `/conversations/{id}` | DELETE | 会話の削除 |

### 詳細仕様

#### GET /health

サービスの稼働状況を確認します。

**レスポンス例**:
```json
{
  "status": "healthy",
  "model": "qwen3:8b"
}
```

#### POST /chat

チャットメッセージを送信し、エージェントからの応答を取得します。

**リクエストボディ**:
```json
{
  "message": "こんにちは！",
  "conversation_id": "20240115143045123456"  // オプション
}
```

**レスポンス例**:
```json
{
  "response": "こんにちは！何かお手伝いできることはありますか？",
  "conversation_id": "20240115143045123456",
  "timestamp": "2024-01-15T14:30:45.123456"
}
```

**パラメータ**:
- `message` (必須): ユーザーのメッセージ
- `conversation_id` (オプション): 既存の会話IDを指定すると、その会話の続きとして処理されます。未指定の場合は新しい会話が作成されます。

#### GET /conversations

すべての会話の一覧を取得します（更新日時の降順）。

**レスポンス例**:
```json
[
  {
    "id": "20240115143045123456",
    "title": "こんにちは！",
    "created_at": "2024-01-15T14:30:45.123456",
    "updated_at": "2024-01-15T14:35:12.654321"
  }
]
```

#### GET /conversations/{id}

特定の会話の詳細情報とメッセージ履歴を取得します。

**レスポンス例**:
```json
{
  "id": "20240115143045123456",
  "title": "こんにちは！",
  "messages": [
    {
      "role": "user",
      "content": "こんにちは！"
    },
    {
      "role": "assistant",
      "content": "こんにちは！何かお手伝いできることはありますか？"
    }
  ],
  "created_at": "2024-01-15T14:30:45.123456",
  "updated_at": "2024-01-15T14:35:12.654321"
}
```

#### DELETE /conversations/{id}

特定の会話を削除します。

**レスポンス例**:
```json
{
  "status": "deleted"
}
```

### API ドキュメント

FastAPI が提供する自動生成ドキュメントも利用できます：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 設定とカスタマイズ

### 環境変数

Agent コンテナで使用される環境変数は `docker-compose.yml` で設定されています。

| 変数名 | デフォルト値 | 説明 |
|---|---|---|
| `OLLAMA_HOST` | `http://ollama:11434` | Ollama サーバーの接続先URL |
| `OLLAMA_MODEL` | `qwen3:8b` | 使用する LLM モデル |

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

`agent/main.py` の `system_prompt` を編集することで、エージェントの振る舞いをカスタマイズできます。

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
# agent/main.py

def calculator(expression: str) -> str:
    """数式を評価して結果を返す"""
    try:
        result = eval(expression)  # 本番環境では安全な評価方法を使用
        return f"計算結果: {result}"
    except Exception as e:
        return f"計算エラー: {str(e)}"

# Agent初期化時に追加
agent = Agent(
    model=ollama_model,
    tools=[current_time, calculator],  # ツールを追加
    system_prompt=system_prompt,
)
```

## トラブルシューティング

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

### Agent がエラーを返す

**症状**: チャットで500エラーが返される

**確認手順**:

1. Agent のログを確認：
```bash
docker compose logs agent -f
```

2. Agent のヘルスチェック：
```bash
curl http://localhost:8000/health
```

**よくある原因**:

- Ollama への接続失敗 → 上記「Ollama に接続できない」を参照
- モデルの読み込み失敗 → ログでエラーメッセージを確認
- メモリ不足 → システムリソースを確認

**解決方法**:

```bash
# コンテナの再起動
docker compose restart agent

# ログの詳細確認
docker compose logs agent --tail=100
```

### 会話履歴が表示されない

**症状**: Frontend で過去の会話が表示されない

**確認手順**:

1. データベースファイルが存在するか確認：
```bash
ls -lh ./data/conversations.db
```

2. データベースの内容を確認：
```bash
docker compose exec agent sqlite3 /app/data/conversations.db "SELECT * FROM conversations;"
```

**解決方法**:

- データベースファイルが破損している場合は削除して再作成：
```bash
docker compose down
rm -rf ./data/conversations.db
docker compose up -d
```

### ポートが既に使用されている

**症状**: `docker compose up` 時に「port is already allocated」エラー

**確認手順**:

```bash
# 使用中のポートを確認
sudo lsof -i :3000
sudo lsof -i :8000
sudo lsof -i :11434
```

**解決方法**:

- 他のプロセスを停止する、または
- `docker-compose.yml` でポート番号を変更：

```yaml
services:
  frontend:
    ports:
      - "3001:3000"  # ホスト側のポートを変更
```

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

#### Agent の開発

```bash
cd agent

# uv のインストール（未インストールの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係のインストール
uv sync

# 開発サーバーの起動
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend の開発

```bash
cd frontend

# 依存関係のインストール
uv sync

# 開発サーバーの起動
uv run streamlit run app.py --server.port 3000
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

### データベーススキーマ

#### conversations テーブル

| カラム名 | 型 | 説明 |
|---|---|---|
| id | TEXT | 会話ID（主キー） |
| title | TEXT | 会話のタイトル |
| created_at | TEXT | 作成日時（ISO 8601形式） |
| updated_at | TEXT | 更新日時（ISO 8601形式） |

#### messages テーブル

| カラム名 | 型 | 説明 |
|---|---|---|
| id | INTEGER | メッセージID（主キー、自動採番） |
| conversation_id | TEXT | 会話ID（外部キー） |
| role | TEXT | ロール（"user" または "assistant"） |
| content | TEXT | メッセージ内容 |
| timestamp | TEXT | タイムスタンプ（ISO 8601形式） |

### ログの確認方法

```bash
# すべてのコンテナのログ
docker compose logs -f

# 特定のコンテナのログ
docker compose logs -f agent
docker compose logs -f ollama
docker compose logs -f frontend

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

## 今後の拡張案

以下の機能追加を検討しています：

### 短期的な拡張

- [ ] **ストリーミングレスポンス**: リアルタイムで応答を表示
- [ ] **複数ツールの追加**:
  - Web 検索ツール
  - 計算機ツール
  - ファイル読み込みツール
- [ ] **ファイルアップロード対応**: PDFやテキストファイルの内容を解析
- [ ] **会話のエクスポート**: JSON/Markdown 形式でエクスポート

### 中長期的な拡張

- [ ] **マルチエージェント構成**: 複数の専門エージェントの協調動作
- [ ] **RAG (Retrieval-Augmented Generation)**: ベクトルDBを使った情報検索
- [ ] **音声入出力対応**: 音声認識・音声合成の統合
- [ ] **OpenTelemetry によるトレーシング**: パフォーマンス分析とデバッグ
- [ ] **認証・認可機能**: マルチユーザー対応
- [ ] **Kubernetes デプロイ対応**: 本番環境での運用
