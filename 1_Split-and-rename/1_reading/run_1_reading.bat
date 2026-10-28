@echo off
echo 1_reading の解析を実行中...
docker compose run --rm -w /app/1_Split-and-rename/1_reading paw-analyzer python reading.py
pause