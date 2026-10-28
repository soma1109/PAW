@echo off
echo 3_Integration の解析を実行中...
docker compose run --rm -w /app/3_Integration paw-analyzer python sum.py
pause