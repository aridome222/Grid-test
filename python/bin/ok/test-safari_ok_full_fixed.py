# 幅800固定で、自作ページをフルページで取れたやつ、ただし、既に変更前ページで不具合発生
# 一応、研究室ページもフルで取れたが、余分に縦に長く撮りすぎて白い部分ができてしまっている
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
    # 最大化されたウィンドウのサイズを取得
    window_size = SafariDriver.get_window_size()

    # 最大化されたウィンドウの高さを取得
    height = window_size['height']

    height = SafariDriver.execute_script("return document.body.scrollHeight")

    # 幅を指定
    width = 800
    # width = SafariDriver.execute_script("return document.body.scrollWidth")


    # 高さは最大化した状態のものを使ってウィンドウサイズを変更
    SafariDriver.set_window_size(width, height*2)

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
