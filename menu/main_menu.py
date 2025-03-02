import sys
import os
import tkinter as tk
from tkinter import messagebox
import time

# プロジェクトルートの絶対パスを取得し、sys.path に追加（このファイルは project_root/menu に配置）
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from common.auth.signin_module import sign_in
# services/muses/muses_controller.py から MUSES への遷移関連の関数をインポート
from services.muses.muses_controller import navigate_to_muses, navigate_to_student_info
# services/muses/automation/role_experience.py から、役職経験一覧出力処理をインポート
from services.muses.automation.role_experience import run_role_experience_analysis

def main_menu_controller():
    # まず共通認証でサインインして WebDriver を取得
    driver = sign_in()
    if driver is None:
        messagebox.showerror("エラー", "サインインに失敗しました。システムを終了します。")
        sys.exit(1)
    
    # メインウィンドウを作成
    root = tk.Tk()
    root.title("各種処理自動化")
    root.geometry("400x400")
    
    # 画面全体のFrameを作成し、上部にタイトルラベルを配置
    container = tk.Frame(root)
    container.pack(fill="both", expand=True)
    
    title_label = tk.Label(container, text="各種処理自動化", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)
    
    # --- MUSES セクション ---
    muses_header = tk.Label(container, text="MUSES", font=("Arial", 14, "underline"))
    muses_header.pack(pady=5)
    
    # 「学生情報」ボタン（単体で学生情報ページへ遷移）
    def on_student_info():
        try:
            navigate_to_muses(driver)
            navigate_to_student_info(driver)
        except Exception as e:
            messagebox.showerror("エラー", f"学生情報ページへの遷移中にエラーが発生しました:\n{e}")
    
    tk.Button(container, text="学生情報", width=20, command=on_student_info).pack(pady=5)
    
    # 「役職経験一覧」ボタン（学生情報画面に遷移した上で、役職経験一覧表を出力）
    def on_role_experience():
        try:
            navigate_to_muses(driver)
            navigate_to_student_info(driver)
            run_role_experience_analysis(driver)
        except Exception as e:
            messagebox.showerror("エラー", f"役職経験一覧表の出力中にエラーが発生しました:\n{e}")
    
    tk.Button(container, text="役職経験一覧", width=20, command=on_role_experience).pack(pady=5)
    
    # --- ダミー1 セクション ---
    dummy1_header = tk.Label(container, text="ダミー1", font=("Arial", 14, "underline"))
    dummy1_header.pack(pady=5)
    
    tk.Button(container, text="ダミー1の処理", width=20,
              command=lambda: messagebox.showinfo("ダミー1", "ダミー1の処理を実行します。")
             ).pack(pady=5)
    
    # --- ダミー2 セクション ---
    dummy2_header = tk.Label(container, text="ダミー2", font=("Arial", 14, "underline"))
    dummy2_header.pack(pady=5)
    
    tk.Button(container, text="ダミー2の処理", width=20,
              command=lambda: messagebox.showinfo("ダミー2", "ダミー2の処理を実行します。")
             ).pack(pady=5)
    
    # システム終了ボタン
    def on_exit():
        try:
            driver.quit()
        except Exception:
            pass
        root.destroy()
    
    tk.Button(container, text="システム終了", width=20, command=on_exit).pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main_menu_controller()