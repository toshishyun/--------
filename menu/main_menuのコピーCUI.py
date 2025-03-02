import sys
import os

# プロジェクトルートの絶対パスを取得（このファイルは project_root/menu にあるため）
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

def display_main_menu():
    print("\n===== メインメニュー =====")
    print("1. MUSESに遷移")
    print("0. システム終了")
    choice = input("番号を選択してください: ").strip()
    return choice

def display_muses_menu():
    print("\n===== MUSES サブメニュー (ダミー) =====")
    print("1. MUSES情報を表示")
    print("2. MUSES操作をシミュレーション")
    print("0. メインメニューに戻る")
    choice = input("番号を選択してください: ").strip()
    return choice

def main_menu_controller():
    # 共通認証モジュールでサインイン（WebDriver取得）
    driver = sign_in()
    if driver is None:
        print("サインインに失敗しました。システムを終了します。")
        return

    while True:
        choice = display_main_menu()
        if choice == "1":
            # MUSESへの遷移処理
            driver = navigate_to_muses(driver)
            # MUSESに遷移後のダミーサブメニュー
            while True:
                muses_choice = display_muses_menu()
                if muses_choice == "1":
                    print("MUSES情報: （ここにMUSESの情報を表示します）")
                elif muses_choice == "2":
                    print("MUSES操作シミュレーション: （ここに操作のシミュレーションを行います）")
                elif muses_choice == "0":
                    print("メインメニューに戻ります。")
                    break
                else:
                    print("無効な選択です。")
        elif choice == "0":
            print("システムを終了します。")
            break
        else:
            print("無効な選択です。")

    driver.quit()

if __name__ == "__main__":
    main_menu_controller()