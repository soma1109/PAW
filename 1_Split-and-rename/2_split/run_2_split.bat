@echo off
echo 2_split の解析を実行中...
docker compose run --rm -w /app/1_Split-and-rename/2_split paw-analyzer python combined_division.py
pause