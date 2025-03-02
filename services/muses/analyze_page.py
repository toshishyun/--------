import time
import os
from bs4 import BeautifulSoup

def analyze_page(driver, output_filename=None):
    """
    現在のページのHTMLを取得して解析し、出力ファイルに保存する関数。

    Parameters:
      driver: Selenium WebDriver オブジェクト（既に目的のページが表示されていることが前提）
      output_filename: 出力ファイル名（指定がなければ "page_structure_<timestamp>.html" として保存）

    Returns:
      BeautifulSoup オブジェクト（解析済みHTML）
    """
    # 動的に要素が生成されるのを待つ（必要に応じて調整）
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    if output_filename is None:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_filename = f"page_structure_{timestamp}.html"
    
    # 出力ファイルは、現在の作業ディレクトリに保存
    output_path = os.path.join(os.getcwd(), output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(soup.prettify())
    print(f"ページ構造を {output_path} に保存しました。")
    return soup

if __name__ == "__main__":
    # テスト用コード：単体で実行する場合は、指定したURLのページを解析
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get("http://www.example.com")  # ここはテスト用URLです
    analyze_page(driver)
    driver.quit()