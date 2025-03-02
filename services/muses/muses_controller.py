import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def navigate_to_muses(driver):
    """
    MUSESへの初回遷移処理：
      - 「muses_btn」ボタンをクリックして MUSES のトップ画面へ移行する。
      - 新しいウィンドウが開いたら、そのウィンドウに切り替えた後、安定動作のために短時間待機する。
    """
    try:
        muse_btn = driver.find_element(By.ID, "muses_btn")
        driver.execute_script("arguments[0].click();", muse_btn)
        wait = WebDriverWait(driver, 15)
        wait.until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)  # ページ安定のための待機（必要に応じて調整）
        print("MUSES のトップ画面に遷移しました。")
    except Exception as e:
        print("MUSESへの遷移中にエラーが発生しました:", e)
        raise e
    return driver

def navigate_to_student_info(driver):
    """
    学生情報ページへの遷移処理：
      1. MUSESトップ画面で、学生情報タブ（XPath: '//*[@id="tab-gk"]'）をクリックする。
      2. 続いて、サブメニューの「登録・参照（担任・研究指導用）」リンク（XPath: '//*[@id="tabmenu-ul"]/li[2]/span'）を
         クリックする。クリック可能になるまで待機し、スクロールで可視化してからクリックする。
      3. iframe（XPath: '//*[@id="main-frame-if"]'）に切り替え、学生情報一覧表（XPath: '/html/body/table[6]'）が表示されるのを待機する。
      4. 遷移完了後、必要に応じてデフォルトコンテンツに戻す。
    """
    try:
        # 学生情報タブをクリック
        student_tab = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="tab-gk"]'))
        )
        driver.execute_script("arguments[0].click();", student_tab)
        time.sleep(1)
        
        # サブメニューのリンクがクリック可能になるまで待機
        submenu = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="tabmenu-ul"]/li[2]/span'))
        )
        # スクロールして要素を可視化してからクリック
        driver.execute_script("arguments[0].scrollIntoView(true);", submenu)
        driver.execute_script("arguments[0].click();", submenu)
        print("学生情報リンクをクリックしました。")
        
        # iframeに切り替え、学生情報一覧表が表示されるのを待機
        iframe = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="main-frame-if"]'))
        )
        driver.switch_to.frame(iframe)
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/table[6]'))
        )
        print("学生情報ページへ遷移しました。")
        
        # 必要であれば、元のコンテンツに戻す
        driver.switch_to.default_content()
    except Exception as e:
        print("学生情報ページへの遷移中にエラーが発生しました:", e)
        raise e
    return driver

def return_to_muses_main(driver):
    """
    MUSESのトップ画面に戻る処理：
      - WebDriverをリフレッシュすることで、MUSESの初期状態に戻す。
    """
    try:
        driver.refresh()
        time.sleep(3)
        print("MUSESのトップ画面に戻りました。")
    except Exception as e:
        print("MUSESのトップ画面に戻る処理中にエラーが発生しました:", e)
        raise e
    return driver

if __name__ == "__main__":
    # テスト用コード：単体実行時の動作確認
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get("http://www.example.com")  # テスト用URL（実際のMUSES URLに置き換えてください）
    # 適宜、各関数を呼び出して動作確認してください
    driver.quit()