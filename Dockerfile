# ベースとなるPythonの環境を指定（軽量版の3.10）
FROM python:3.10-slim

# コンテナ内の作業ディレクトリを設定
WORKDIR /app

# 1. ライブラリの注文書（requirements.txt）をコンテナにコピー
COPY requirements.txt .

# 2. pipを更新して、requirements.txtに書いたライブラリを一括インストール
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 3. 手元のPAWの中身（3つのフォルダなど全ファイル）をコンテナにコピー
COPY . .