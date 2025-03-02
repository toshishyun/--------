import sys
import os
import tkinter as tk
from tkinter import messagebox
import time

# プロジェクトルートの絶対パスを取得し、sys.path に追加（このファイルは project_root/menu に配置）
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# 共通認証モジュールからサインイン処理を呼び出す
from common.auth.signin_module import sign_in
# services/muses 内の MUSES 操作モジュールから各関数をインポート
from services.muses.muses_controller import navigate_to_muses, navigate_to_student_info

def main_menu_controller():
    # まずサインインして WebDriver を取得
    driver = sign_in()
    if driver is None:
        messagebox.showerror("エラー", "サインインに失敗しました。システムを終了します。")
        sys.exit(1)
    
    # 1つのウィンドウ内で画面切替（SPA風）を行うため、Frame を用いる
    root = tk.Tk()
    root.title("メインメニュー")
    root.geometry("300x250")
    
    # メインメニュー画面と各サービス画面用の Frame を作成
    main_frame = tk.Frame(root)
    muses_frame = tk.Frame(root)
    student_frame = tk.Frame(root)
    
    for frame in (main_frame, muses_frame, student_frame):
        frame.grid(row=0, column=0, sticky="nsew")
    
    # --- main_frame: メインメニュー ---
    tk.Label(main_frame, text="サービスを選択してください", font=("Arial", 12)).pack(pady=10)
    
    def on_muses():
        try:
            # MUSES への遷移処理は services/muses/muses_controller.py の関数で実行
            navigate_to_muses(driver)
        except Exception as e:
            messagebox.showerror("エラー", f"MUSES への遷移中にエラーが発生しました:\n{e}")
        muses_frame.tkraise()
    
    def on_student():
        try:
            # 学生情報（仮）の遷移処理
            navigate_to_student_info(driver)
        except Exception as e:
            messagebox.showerror("エラー", f"学生情報ページへの遷移中にエラーが発生しました:\n{e}")
        student_frame.tkraise()
    
    tk.Button(main_frame, text="MUSESに遷移", width=20, command=on_muses).pack(pady=5)
    tk.Button(main_frame, text="学生情報（仮）", width=20, command=on_student).pack(pady=5)
    
    def on_exit():
        try:
            driver.quit()
        except Exception:
            pass
        root.destroy()
    
    tk.Button(main_frame, text="システム終了", width=20, command=on_exit).pack(pady=5)
    
    # --- muses_frame: MUSES サブメニュー（ダミー） ---
    tk.Label(muses_frame, text="MUSES サブメニュー (ダミー)", font=("Arial", 12)).pack(pady=10)
    tk.Button(muses_frame, text="MUSES情報を表示",
              command=lambda: messagebox.showinfo("MUSES情報", "ここに MUSES の情報を表示します。")
             ).pack(pady=5)
    tk.Button(muses_frame, text="MUSES操作をシミュレーション",
              command=lambda: messagebox.showinfo("MUSES操作", "ここに MUSES の操作シミュレーションを行います。")
             ).pack(pady=5)
    tk.Button(muses_frame, text="メインメニューに戻る", command=lambda: main_frame.tkraise()
             ).pack(pady=10)
    
    # --- student_frame: 学生情報（仮）サブメニュー（ダミー） ---
    tk.Label(student_frame, text="学生情報（仮） サブメニュー (ダミー)", font=("Arial", 12)).pack(pady=10)
    tk.Button(student_frame, text="学生情報を表示",
              command=lambda: messagebox.showinfo("学生情報", "ここに学生情報を表示します。")
             ).pack(pady=5)
    tk.Button(student_frame, text="学生情報操作をシミュレーション",
              command=lambda: messagebox.showinfo("学生情報操作", "ここに学生情報の操作シミュレーションを行います。")
             ).pack(pady=5)
    tk.Button(student_frame, text="メインメニューに戻る", command=lambda: main_frame.tkraise()
             ).pack(pady=10)
    
    # 初期表示は main_frame
    main_frame.tkraise()
    root.mainloop()

if __name__ == "__main__":
    main_menu_controller()