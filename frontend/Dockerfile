FROM python:3.12-slim

WORKDIR /app

# 依存関係をコピー&インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションをコピー
COPY app.py .

# ポートを公開
EXPOSE 3000

# Streamlitを起動
CMD ["streamlit", "run", "app.py", "--server.port=3000", "--server.address=0.0.0.0", "--server.headless=true"]
