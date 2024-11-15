# Pythonの軽量なベースイメージを指定
FROM python:3.12

# コンテナ内に作業ディレクトリを作成
WORKDIR /app

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ホストのrequirementsファイルとアプリケーションコードをコンテナにコピー
# COPY requirements_container.txt /app/  # もしかして不要？
COPY app.py /app/
COPY .env /app/
COPY .data /app/.data

# Pythonの依存関係をインストール
# RUN pip install --no-cache-dir -r requirements_container.txt　# もしかして不要？
RUN pip install --no-cache-dir uvicorn[standard]
RUN pip install --no-cache-dir openssa
RUN pip install --no-cache-dir fastapi

# ポートを指定（FastAPIのデフォルトポート）
EXPOSE 8000

# アプリケーションを起動
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
