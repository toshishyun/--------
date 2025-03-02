import csv
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def into_iframe(driver, iframe_xpath='//*[@id="main-frame-if"]'):
    """
    指定されたiframeに切り替えます。
    """
    iframe = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, iframe_xpath))
    )
    driver.switch_to.frame(iframe)

def out_of_iframe(driver):
    """
    iframeから元のコンテンツに戻します。
    """
    driver.switch_to.default_content()

def get_element(driver, xpath_description, wait_seconds=30, retries=15, msg=""):
    """
    指定したXPathの要素を、指定回数リトライして取得します。
    失敗した場合はエラーメッセージを出力し、最終的に None を返します。
    """
    element = None
    for _ in range(retries):
        try:
            element = WebDriverWait(driver, wait_seconds).until(
                EC.visibility_of_element_located((By.XPATH, xpath_description))
            )
        except TimeoutException:
            print("EXCEPTION:", msg)
            time.sleep(1)
        else:
            break
    if element is None:
        print("DEBUG: ERROR get_element:", msg)
    return element

def extract_role_experience(driver):
    """
    学生情報一覧表から各学生の役職経験情報を抽出します。
    前提:
      - 学生情報一覧表はiframe内に表示されている
      - 表の1行目がヘッダー、2行目以降が各学生のデータ行とする
      - 例として、1列目が学生番号、2列目が氏名、3～5列目に役職経験情報があると仮定する
    Returns:
      2次元リスト（1行目はヘッダー、その後に各学生のデータ）
    """
    data = []
    header = ["学生番号", "氏名", "役職経験1", "役職経験2", "役職経験3"]
    data.append(header)
    
    # 学生情報一覧表の行を取得（ヘッダー行を除く）
    rows_xpath = '/html/body/table[6]/tbody/tr[position()>1]'
    rows = driver.find_elements(By.XPATH, rows_xpath)
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) < 5:
            continue
        student_number = cells[0].text.strip()
        student_name = cells[1].text.strip()
        role1 = cells[2].text.strip()
        role2 = cells[3].text.strip()
        role3 = cells[4].text.strip()
        data.append([student_number, student_name, role1, role2, role3])
    return data

def output_role_experience_csv(data, filename="role_experience.csv"):
    """
    抽出した役職経験情報を CSV ファイルに出力します。
    出力先はプロジェクトルートの output フォルダーとし、存在しない場合は作成します。
    """
    output_folder = os.path.join(os.getcwd(), "output")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, filename)
    with open(output_path, mode="w", newline="", encoding="cp932") as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)
    print(f"役職経験情報を {output_path} に出力しました。")

def run_role_experience_analysis(driver):
    """
    役職経験の一覧表を抽出し、CSVに出力する一連の処理を実行します。
    学生情報一覧表が表示されている状態（iframe内）を前提としています。
    """
    try:
        # iframeに切り替え、学生情報一覧表の解析を開始
        into_iframe(driver)
        data = extract_role_experience(driver)
        out_of_iframe(driver)
        output_role_experience_csv(data)
    except Exception as e:
        print("役職経験分析処理中にエラーが発生しました:", e)
        raise e

if __name__ == "__main__":
    # テスト用コード：実際の環境ではMUSESの学生情報ページに遷移後に run_role_experience_analysis(driver) を呼び出すこと
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get("http://www.example.com")  # テスト用URL。実際はMUSESの学生情報ページに置き換える
    time.sleep(5)
    run_role_experience_analysis(driver)
    driver.quit()