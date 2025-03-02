import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def navigate_to_muses(driver):
    """
    MUSESへの遷移処理：
      - ID "muses_btn" のボタンをクリックし、MUSESトップ画面に遷移する。
      - 新しいウィンドウが開くのを待機し、ウィンドウを切り替える。
      - 安定動作のため、切り替え後に数秒待機する。
    """
    try:
        muse_btn = driver.find_element(By.ID, "muses_btn")
        driver.execute_script("arguments[0].click();", muse_btn)
        
        # 新しいウィンドウが開くのを待機
        wait = WebDriverWait(driver, 15)
        wait.until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(5)
        print("MUSES 起動完了")
    except Exception as e:
        print("MUSESへの遷移中にエラーが発生しました:", e)
        raise e
    return driver

def navigate_to_student_info(driver):
    """
    学生情報（仮）ページへの遷移処理：
      - まず、MUSESのトップ画面に遷移している前提で、学生情報ページへ URL で遷移する。
      ※実際のURLや待機条件は運用に合わせて調整してください。
    """
    student_info_url = "http://www.mukogawa-u.ac.jp/studentinfo"  # 仮のURLです
    try:
        driver.get(student_info_url)
        wait = WebDriverWait(driver, 10)
        # ページタイトルに「学生情報」が含まれることを確認（例）
        wait.until(lambda d: "学生情報" in d.title)
        print("学生情報ページへ遷移しました。")
    except Exception as e:
        print("学生情報ページへの遷移中にエラーが発生しました:", e)
        raise e
    return driver