from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os
import time

screen_shot_file_path = './python/inout/screen_shot_SAFARI_1.png'
html_file_path = f'./python/inout/page_source_SAFARI_1.html'

# URL="https://earth.cs.miyazaki-u.ac.jp/"
URL="http://localhost:5000/before"

try:
    #Safariドライバ起動
    SafariDriver = webdriver.Safari()
    SafariDriver.maximize_window()

    # アクセスするURL
    SafariDriver.get(URL)

    time.sleep(1)  # 長い処理

    # スクリーンaショットを撮る
    SafariDriver.save_screenshot(screen_shot_file_path)

    # HTMLコードを保存
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(SafariDriver.page_source)

    #ブラウザClose
    SafariDriver.quit()
except WebDriverException as e:
    pass
