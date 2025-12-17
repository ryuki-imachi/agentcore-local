FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# 依存関係ファイルとソースファイルをコピー
COPY pyproject.toml main.py main_agui.py ./

# プロジェクトをインストール（依存関係も含む）
RUN uv pip install --system --no-cache .

# データディレクトリを作成
RUN mkdir -p /app/data

# ポートを公開
EXPOSE 8000 8080

# 環境変数でポートを設定可能にする（デフォルトは8000、AG-UIでは8080推奨）
ENV AGENT_PORT=8000
ENV AGENT_MODULE=main_agui

# アプリケーションを起動
CMD uvicorn ${AGENT_MODULE}:app --host 0.0.0.0 --port ${AGENT_PORT}
