import sys
import os
import tkinter as tk
from tkinter import messagebox

# プロジェクトルートの絶対パスを取得し、sys.path に追加
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 共通認証モジュールからサインイン処理を呼び出す
from common.auth.signin_module import sign_in
# サービス毎の遷移処理（現時点ではMUSESのみ）
from services.muses.muses_navigate import navigate_to_muses

def main_menu_controller():
    # まずサインインしてWebDriverを取得
    driver = sign_in()
    if driver is None:
        messagebox.showerror("エラー", "サインインに失敗しました。システムを終了します。")
        sys.exit(1)
    
    root = tk.Tk()
    root.title("メインメニュー")
    root.geometry("300x200")
    
    # メインウィンドウ内で各画面用のフレームを作成
    main_frame = tk.Frame(root)
    muses_frame = tk.Frame(root)
    
    # どのフレームも同じ位置に配置（これにより、tkraise() で表示を切り替えられる）
    for frame in (main_frame, muses_frame):
        frame.grid(row=0, column=0, sticky="nsew")
    
    # main_frame：メインメニュー
    tk.Label(main_frame, text="サービスを選択してください", font=("Arial", 12)).pack(pady=10)
    
    def on_muses():
        try:
            # MUSES への遷移処理（同じWebDriver内で遷移処理を実行）
            navigate_to_muses(driver)
        except Exception as e:
            messagebox.showerror("エラー", f"MUSESへの遷移中にエラーが発生しました:\n{e}")
        # メインウィンドウ内の表示をMUSESメニューに切り替え
        muses_frame.tkraise()
    
    tk.Button(main_frame, text="MUSESに遷移", width=20, command=on_muses).pack(pady=5)
    
    def on_exit():
        try:
            driver.quit()
        except Exception:
            pass
        root.destroy()
    
    tk.Button(main_frame, text="システム終了", width=20, command=on_exit).pack(pady=5)
    
    # muses_frame：MUSESサブメニュー（ダミー）
    tk.Label(muses_frame, text="MUSES サブメニュー (ダミー)", font=("Arial", 12)).pack(pady=10)
    tk.Button(muses_frame, text="MUSES情報を表示",
              command=lambda: messagebox.showinfo("MUSES情報", "ここにMUSESの情報を表示します。")
             ).pack(pady=5)
    tk.Button(muses_frame, text="MUSES操作をシミュレーション",
              command=lambda: messagebox.showinfo("MUSES操作", "ここにMUSESの操作シミュレーションを行います。")
             ).pack(pady=5)
    tk.Button(muses_frame, text="メインメニューに戻る", command=lambda: main_frame.tkraise()
             ).pack(pady=10)
    
    # 初期表示は main_frame
    main_frame.tkraise()
    root.mainloop()

if __name__ == "__main__":
    main_menu_controller()