import sys
import os
import subprocess
import traceback

def switch_to_venv():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_python = os.path.abspath(os.path.join(current_dir, "../.venv/Scripts/python.exe"))
    
    if os.path.normcase(os.path.abspath(sys.executable)) == os.path.normcase(target_python):
        return

    if os.path.exists(target_python):
        print(f"[自動切替] .venv の環境に切り替えます...")
        try:
            result = subprocess.run([target_python] + sys.argv)
            sys.exit(result.returncode)
        except Exception as e:
            print(f"環境の切り替えに失敗しました: {e}")
            sys.exit(1)
    else:
        print(f"【警告】指定された仮想環境が見つかりません: {target_python}")
        print("システム側の Python で続行します...")

switch_to_venv()

import glob
import numpy as np

def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # 1. DIWファイルの検索とチェック
    DIWfile = glob.glob(os.path.join(current_directory, "*DIW*.txt"))
    if not DIWfile:
        print("\n【エラー】名前に 'DIW' が含まれるテキストファイルが見つかりません！")
        print(f"検索場所: {current_directory}")
        return

    print(f"基準となるDIWファイルを発見: {os.path.basename(DIWfile[0])}")
    DIWdata = np.loadtxt(DIWfile[0], skiprows=1)

    # 2. 測定用ファイルの検索
    measurement_files = glob.glob(os.path.join(current_directory, "*.txt"))
    measurement_files = list(set(measurement_files) - set(DIWfile))

    if not measurement_files:
        print("\n【警告】処理対象の測定用テキストファイル(.txt)が見つかりません。")
        return

    print(f"処理対象ファイル数: {len(measurement_files)}件")

    # 3. 計算と保存
    for filename in measurement_files:
        print(f"処理中: {os.path.basename(filename)}")
        data = np.loadtxt(filename, skiprows=1)
        
        # 吸光度（Abs）の計算
        Abs = -np.log10(data[:, 1] / DIWdata[:, 1])
        
        # ファイル名を .csv に変更して保存
        savename = os.path.splitext(filename)[0] + ".csv"
        np.savetxt(savename, np.stack([data[:, 0], Abs], 1), delimiter=",", fmt="%.1f,%.8e")
        print(f"  -> 保存完了: {os.path.basename(savename)}")

    print("\nすべての処理が正常に終了しました！")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("\n" + "!"*60)
        print(" 【予期せぬエラーが発生しました】")
        print("!"*60)
        traceback.print_exc()
        print("!"*60)
    finally:
        input("\n終了するには Enter キーを押してください...")