from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os
import time

from Screenshot import Screenshot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

screen_shot_file_path = './python/inout/screen_shot_SAFARI_1.png'
html_file_path = f'./python/inout/page_source_SAFARI_1.html'
URL="http://localhost:5000/before"
# URL="https://earth.cs.miyazaki-u.ac.jp/"

try:
    #Safariドライバ起動
    SafariDriver = webdriver.Safari()
    # SafariDriver.maximize_window()

    # アクセスするURL
    SafariDriver.get(URL)

    time.sleep(1)  # 長い処理

    # スクリーンaショットを撮る

    ob = Screenshot.Screenshot()

    #ウインドウサイズをWebサイトに合わせて変更
    width = SafariDriver.execute_script("return document.body.scrollWidth;")
    height = SafariDriver.execute_script("return document.body.scrollHeight;")
    SafariDriver.set_window_size(width,height)

    # タイムアウト判定を行う
    try:
        # 全てのコンテンツが読み込まれるまで待機
        WebDriverWait(SafariDriver, 15).until(EC.presence_of_all_elements_located)
    except TimeoutException as e:
        # 例外処理
        print(e)

    # 追加: ここでフルページのスクリーンショットを取る  
    # ob.full_screenshot(SafariDriver, save_path="./python/inout/", image_name=f"screen_shot_SAFARI_1.png") 
    ob.full_screenshot(SafariDriver, save_path="./python/inout/", image_name=f"screen_shot_SAFARI_1.png", is_load_at_runtime = True, load_wait_time=10) 
    # ob.full_screenshot(driver, save_path=output_dir, image_name=output_file_name, is_load_at_runtime = True, load_wait_time=10) 

    # HTMLコードを保存
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(SafariDriver.page_source)

    #ブラウザClose
    SafariDriver.quit()
except WebDriverException as e:
    pass
