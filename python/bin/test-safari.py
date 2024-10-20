# Safariで画像取得するためのプログラム
# 今の所、動的に幅と高さを取得している
# 高さはすべてのエレメントを含む高さ
# 幅はbody内の要素を含む幅
import sys
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
from Screenshot import Screenshot

def run_test(screen_shot_file_path, html_file_path, URL):
    if URL.startswith("http://host.docker.internal"):
        url = URL.replace("http://host.docker.internal", "http://localhost")
    else:
        url = URL

    try:
        #Safariドライバ起動
        SafariDriver = webdriver.Safari()
        SafariDriver.maximize_window()

        print("うまくいったね！！！たぶん！")

        # アクセスするURL
        SafariDriver.get(url)

        time.sleep(1)  # 長い処理

        # device_pixel_ratio = SafariDriver.execute_script("return window.devicePixelRatio;")

        # 高さを指定
        # height = SafariDriver.execute_script("return document.body.scrollHeight")
        height = SafariDriver.execute_script("return document.documentElement.scrollHeight")

        # 幅を指定
        width = SafariDriver.execute_script("return document.body.scrollWidth")
        # width = SafariDriver.execute_script("return document.documentElement.scrollWidth")

        # height = 2500
        # width = 800
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
        print("ドライバーがエラーの原因かー")
        print(f"Error occurred: {e}")
        

if __name__ == "__main__":
    # コマンドライン引数からパスとURLを取得
    screen_shot_file_path = sys.argv[1]
    html_file_path = sys.argv[2]
    URL = sys.argv[3]

    run_test(screen_shot_file_path, html_file_path, URL)
