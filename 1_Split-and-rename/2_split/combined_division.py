import sys
import os
import subprocess
import traceback

import pandas as pd

def process_excel_files():
    original_excel_files = [f for f in os.listdir() if f.endswith('.xlsx') and not f.startswith('~$')]
    generated_files = []

    for excel_file in original_excel_files:
        print(f"処理中の元Excel: {excel_file}")
        df = pd.read_excel(excel_file)
        first_column = df.iloc[:, 0]
        
        for col_index in range(1, df.shape[1]):
            col_name = str(df.columns[col_index]).strip()
            
            # 【安全対策】ファイル名に使えない文字が含まれていたら置換する
            for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
                col_name = col_name.replace(char, '_')
                
            file_name = f"{col_name}.xlsx"
            
            paired_df = pd.DataFrame({
                str(df.columns[0]): first_column,
                col_name: df.iloc[:, col_index]
            })
            
            paired_df.to_excel(file_name, index=False)
            print(f"  -> 生成: {file_name}")
            generated_files.append(file_name)

    return original_excel_files, generated_files

def excel_to_txt(excel_files):
    for excel_file in excel_files:
        df = pd.read_excel(excel_file)
        txt_file_name = f"{os.path.splitext(excel_file)[0]}.txt"
        
        with open(txt_file_name, 'w', encoding='utf-8') as f:
            f.write(f"{df.columns[0]}\t{df.columns[1]}\n")
            for _, row in df.iterrows():
                f.write(f"{row.iloc[0]}\t{row.iloc[1]}\n")
        
        print(f"  -> Text変換: {txt_file_name}")

def delete_generated_files(generated_files, original_files):
    current_excel_files = [f for f in os.listdir() if f.endswith('.xlsx')]
    for file in current_excel_files:
        if file not in original_files and file in generated_files:
            os.remove(file)
            print(f"削除: {file}")

def main():
    print("--- 処理開始 ---")
    original_files, generated_files = process_excel_files()
    
    print("--- テキスト変換開始 ---")
    excel_to_txt(generated_files)
    
    print("--- 一時ファイル削除開始 ---")
    delete_generated_files(generated_files, original_files)
    print("--- すべて完了 ---")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("\n" + "!"*60)
        print(" 【エラーが発生して処理が中断されました】")
        print("!"*60)
        traceback.print_exc()
        print("!"*60)
    finally:
        input("\n終了するには Enter キーを押してください...")