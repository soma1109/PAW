import sys
import os
import subprocess
import traceback

import glob
import numpy as np
import os
import pandas as pd
import re

# ユーザーからの入力を受け取る
pattern = input("ソート対象のファイル名パターンを入力してください（例: 20240000_ガス_*_fitting）"
                "\n[「*」以前の部分]+[spreadsheet]が出力がファイル名となります"
                "\nソート対象とする数値およびそれ以降を*とすることで正しくソートが可能です")

# アスタリスク部分にマッチする正規表現パターンを作成
regex_pattern = pattern.replace('*', r'(\d+)')

# アスタリスクの前の部分を取得
prefix = pattern.split('*')[0]

current_directory = os.path.dirname(os.path.abspath(__file__))
measurement_files = glob.glob(os.path.join(current_directory, "*.csv"))

# --- ここから差し替え ---

# 数値を含むファイル名でソートするための関数
def extract_number(file_name):
    match = re.search(regex_pattern, file_name)
    return int(match.group(1)) if match else float('inf')

print("\n" + "="*50)
print("【ファイル名の並び替えを実行中...】")
print(f"適応するパターン: {regex_pattern}")
print("="*50)

# ① まず先に「数値に基づいて並び替え（ソート）」を完了させる
measurement_files = sorted(measurement_files, key=lambda f: extract_number(os.path.basename(f)))

# ② 並び替えが【完了したリスト】を画面に表示する
for file in measurement_files:
    b_name = os.path.basename(file)
    num = extract_number(b_name)
    
    if num == float('inf'):
        print(f"❌ マッチ失敗 -> [最後尾へ] : {b_name} (パターンに一致する数値が見つかりません)")
    else:
        print(f"⭕ 並び替え済 -> [判定数値: {num:3d}] : {b_name}")

print("="*50)
print("【並び替え完了】上記の正しい数値順（小さい順）でこれからの解析処理を行います。")
print("="*50 + "\n")

# --- ここまで差し替え ---


ppm_list = []
stdv_list = []

for file in measurement_files:
    df = pd.read_csv(file, on_bad_lines='skip', encoding='shift_jis')

    # ファイル名を取り出す
    file_name = os.path.basename(file)

    ppm = df.iloc[0:5, 1].tolist()
    stdv = df.iloc[0:4, 2].tolist()

    # ファイル名をデータの先頭に追加
    ppm = [file_name] + ppm
    stdv = [file_name] + stdv

    ppm_list.append(ppm)
    stdv_list.append(stdv)

# リストをDataFrameに変換
transposed_ppm = pd.DataFrame(ppm_list)
transposed_stdv = pd.DataFrame(stdv_list)

# ppmとstdvを縦方向に結合する
stdv_row = ['STDV'] + [''] * (transposed_stdv.shape[1] - 1)
transposed_stdv_with_stdvs = pd.DataFrame([stdv_row], columns=transposed_stdv.columns)
combined_data = pd.concat([transposed_ppm, transposed_stdv_with_stdvs, transposed_stdv], axis=0)

# 先頭行に[Result]と[ ,H2O2 ,NO2- ,NO3- ,O2 ,Error Range]を追加
num_columns = combined_data.shape[1]
header = pd.DataFrame([
    ['Result'] + [''] * (num_columns - 1),
    ['', 'H2O2', 'NO2-', 'NO3-', 'O2', 'Error Range']
], columns=[i for i in range(num_columns)])
combined_data_with_header = pd.concat([header, combined_data], ignore_index=True)

# 列名を空に設定してから保存
combined_data_with_header.columns = [''] * num_columns

# 出力ファイル名を生成
output_file_name = f"{prefix}spreadsheet.xlsx"
combined_data_with_header.to_excel(output_file_name, index=False, header=False)

print(f"出力ファイル名: {output_file_name}")
