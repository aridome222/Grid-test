# 幅を固定せずに自作ページ＆研究室ページ、どちらもフルページ取れたやつ
# ただし、自作ページの変更前ページで既に画面要素のはみ出し発生
# また、研究室ページは、余分に縦に長く撮影していて、白い部分が発生
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os
import time

screen_shot_file_path = './python/inout/screen_shot_SAFARI_1.png'
html_file_path = f'./python/inout/page_source_SAFARI_1.html'

URL="https://earth.cs.miyazaki-u.ac.jp/"
# URL="http://localhost:5000/before"
# URL="http://localhost:5000/after"

try:
    #Safariドライバ起動
    SafariDriver = webdriver.Safari()
    SafariDriver.maximize_window()
    # 最大化されたウィンドウのサイズを取得
    # window_size = SafariDriver.get_window_size()

    # # 最大化されたウィンドウの高さを取得
    # height = window_size['height']
    # width = window_size['width']

    

    # height = SafariDriver.execute_script("return document.body.scrollHeight")
    # height = SafariDriver.execute_script("return document.documentElement.scrollHeight")
    # height = SafariDriver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);")
    # height = 2114
    device_pixel_ratio = SafariDriver.execute_script("return window.devicePixelRatio;")

    # from selenium.webdriver.common.by import By
    # from selenium.webdriver.support.ui import WebDriverWait
    # from selenium.webdriver.support import expected_conditions as EC

    # # ページの読み込み完了を待つ
    # WebDriverWait(SafariDriver, 10).until(
    #     EC.presence_of_element_located((By.TAG_NAME, "body"))
    # )

    # height = SafariDriver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # ページの読み込み完了を待つ (例えば、"body"タグが表示されるまで)
    WebDriverWait(SafariDriver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    height = SafariDriver.execute_script("return document.body.scrollHeight")


    # 幅を指定
    # width = 800
    width = SafariDriver.execute_script("return document.body.scrollWidth")

    print(height*device_pixel_ratio)
    print(width/device_pixel_ratio)


    # 高さは最大化した状態のものを使ってウィンドウサイズを変更
    SafariDriver.set_window_size(width/device_pixel_ratio, height*device_pixel_ratio)

    # アクセスするURL
    SafariDriver.get(URL)

    time.sleep(1)  # 長い処理

    # height = SafariDriver.execute_script("return document.body.scrollHeight")
    height = SafariDriver.execute_script("return document.documentElement.scrollHeight")


    # 幅を指定
    # width = 800
    width = SafariDriver.execute_script("return document.body.scrollWidth")
    # width = SafariDriver.execute_script("return document.documentElement.scrollWidth")

    print(height)
    print(width)

    # 高さは最大化した状態のものを使ってウィンドウサイズを変更
    SafariDriver.set_window_size(width, height)

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
