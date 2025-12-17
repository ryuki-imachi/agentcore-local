FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# 依存関係ファイルとmain.pyをコピー
COPY pyproject.toml main.py ./

# プロジェクトをインストール（依存関係も含む）
RUN uv pip install --system --no-cache .

# データディレクトリを作成
RUN mkdir -p /app/data

# ポートを公開
EXPOSE 8000

# アプリケーションを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
