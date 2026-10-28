@echo off
echo 2_Convert-to-absorbance の解析を実行中...
docker compose run --rm -w /app/2_Convert-to-absorbance paw-analyzer python abs.py
pause