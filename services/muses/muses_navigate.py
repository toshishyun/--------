import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def navigate_to_muses(driver):
    """
    MUSESへの遷移処理：
      - ID "muses_btn" のボタンをクリック
      - 新しいウィンドウが開くのを待機し、ウィンドウを切り替える
      - 安定動作のために少し待機する
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
    return driver