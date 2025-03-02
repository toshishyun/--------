import os
import json
import re
import time
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# プロジェクトルートを取得（このファイルは project_root/common/auth に配置）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 設定ファイルは project_root/config に配置
CONFIG_FILE = os.path.join(BASE_DIR, "config", "credentials.enc")
KEY_FILE = os.path.join(BASE_DIR, "config", "secret.key")

# 定数設定
LOGIN_URL = "http://www.mukogawa-u.ac.jp/cgi-bin/jump.cgi?http://www.mukogawa-u.ac.jp/~jouhou-c/onlineservices.html"

# ----- 暗号化／復号処理 -----
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print("新しい暗号化キーを生成しました。")
    return key

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            key = f.read()
        print("暗号化キーをファイルから読み込みました。")
        return key
    else:
        print("暗号化キーが見つかりません。新規生成します。")
        return generate_key()

def encrypt_and_save(data, key):
    fernet = Fernet(key)
    enc_data = fernet.encrypt(json.dumps(data).encode())
    with open(CONFIG_FILE, "wb") as f:
        f.write(enc_data)
    print("認証情報を暗号化して保存しました。")

def load_and_decrypt(key):
    if not os.path.exists(CONFIG_FILE):
        print("認証情報ファイルが見つかりません。")
        return None
    with open(CONFIG_FILE, "rb") as f:
        enc_data = f.read()
    fernet = Fernet(key)
    dec_data = fernet.decrypt(enc_data)
    print("認証情報を復号しました。")
    return json.loads(dec_data.decode())

# ----- GUIによる初回設定：入力フォーム（再入力可能な仕様） -----
def setup_credentials_gui():
    def on_submit():
        uname = entry_username.get().strip()
        pwd = entry_password.get().strip()
        pc1 = entry_pc1.get().strip()
        pc2 = entry_pc2.get().strip()
        pc3 = entry_pc3.get().strip()
        if not uname or not pwd or not pc1 or not pc2 or not pc3:
            messagebox.showerror("エラー", "すべての項目は必須です。")
            return
        confirm_text = f"ユーザー名: {uname}\n認証用パスコード画像: {pc1}, {pc2}, {pc3}\n\nこの内容で保存しますか？"
        if messagebox.askyesno("入力内容確認", confirm_text):
            data = {"username": uname, "password": pwd, "passcode": [pc1, pc2, pc3]}
            encrypt_and_save(data, load_key())
            # 設定保存完了のメッセージウィンドウを表示（2秒後に自動閉鎖）
            info_win = tk.Toplevel(root)
            info_win.title("完了")
            tk.Label(info_win, text="設定を保存しました。", padx=20, pady=20).pack()
            root.after(2000, lambda: (info_win.destroy(), root.destroy()))
    
    root = tk.Tk()
    root.title("初回設定: サインイン情報の入力")
    
    tk.Label(root, text="ユーザー名:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_username = tk.Entry(root, width=30)
    entry_username.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(root, text="パスワード:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_password = tk.Entry(root, width=30, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(root, text="1枚目の画像ファイル名:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_pc1 = tk.Entry(root, width=30)
    entry_pc1.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Label(root, text="2枚目の画像ファイル名:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_pc2 = tk.Entry(root, width=30)
    entry_pc2.grid(row=3, column=1, padx=10, pady=5)
    
    tk.Label(root, text="3枚目の画像ファイル名:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entry_pc3 = tk.Entry(root, width=30)
    entry_pc3.grid(row=4, column=1, padx=10, pady=5)
    
    submit_btn = tk.Button(root, text="保存", command=on_submit, width=15)
    submit_btn.grid(row=5, column=0, columnspan=2, pady=10)
    
    # eawasepics.png を表示（このファイルはこのコードファイルと同じディレクトリにある）
    try:
        # ファイルパスは __file__ を基準にする
        img_path = os.path.join(os.path.dirname(__file__), "eawasepics.png")
        img = tk.PhotoImage(file=img_path)
        img_label = tk.Label(root, image=img)
        img_label.image = img  # 参照保持
        img_label.grid(row=6, column=0, columnspan=2, pady=10)
    except Exception as e:
        print("画像の読み込みに失敗しました:", e)
    
    root.mainloop()

# ----- サインイン処理（自動ログイン＋二段階認証） -----
def sign_in():
    key = load_key()
    credentials = load_and_decrypt(key)
    if not credentials or not credentials.get("username") or not credentials.get("password"):
        setup_credentials_gui()
        credentials = load_and_decrypt(key)
    
    driver = webdriver.Chrome()
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, 10)
    
    try:
        user_input = wait.until(EC.visibility_of_element_located((By.NAME, "twuser")))
        user_input.clear()
        user_input.send_keys(credentials["username"])
        
        pass_input = driver.find_element(By.NAME, "twpassword")
        pass_input.clear()
        pass_input.send_keys(credentials["password"])
        
        login_btn = driver.find_element(By.NAME, "login")
        driver.execute_script("arguments[0].click();", login_btn)
        print("ユーザー認証情報を送信しました。")
    except Exception as e:
        print("ログインフォーム操作中のエラー:", e)
        driver.quit()
        return None
    
    try:
        wait.until(EC.visibility_of_element_located((By.ID, "btnLogin")))
        print("二段階認証画面を検出しました。")
    except Exception as e:
        print("二段階認証画面が表示されませんでした:", e)
        driver.quit()
        return None
    
    idNames = ["button" + str(i) for i in range(25)]
    
    def click_icon(target_icon):
        target_filename = target_icon + ".gif"
        for idname in idNames:
            try:
                currentIcon = driver.find_element(By.ID, idname)
                currentStyle = currentIcon.get_attribute("style")
                m = re.search(r'(e\d{1,2}\.gif)', currentStyle)
                if m and m.group(1) == target_filename:
                    driver.execute_script("arguments[0].click();", currentIcon)
                    print(f"{target_filename} を選択しました。")
                    return True
            except Exception:
                continue
        return False

    for icon in credentials["passcode"]:
        if not click_icon(icon):
            print(f"{icon}.gif が見つかりません")
    
    try:
        btn = driver.find_element(By.ID, "btnLogin")
        driver.execute_script("arguments[0].click();", btn)
        print("btnLogin をクリックしました。")
    except Exception as e:
        print("btnLoginクリック時のエラー:", e)
        driver.quit()
        return None
    
    try:
        wait.until(EC.visibility_of_element_located((By.NAME, "SUBMIT")))
        print("最終認証完了要素 (SUBMIT) を検出しました。")
    except Exception as e:
        print("最終認証完了要素が見つかりませんでした:", e)
        driver.quit()
        return None
    
    print("サインイン処理完了")
    return driver

if __name__ == "__main__":
    sign_in()