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
        # Safariドライバを起動
        SafariDriver = webdriver.Safari()
        # SafariDriver.maximize_window()

        # 指定されたURLにアクセス
        SafariDriver.get(url)

        # ページ全体が読み込まれるまで待機 (document.readyState == "complete")
        try:
            WebDriverWait(SafariDriver, 15).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
        except TimeoutException as e:
            print(f"Timeout occurred while waiting for page to load: {e}")

        # ウィンドウサイズをWebページのサイズに合わせる
        # width = SafariDriver.execute_script("return document.body.scrollWidth;")
        # height = SafariDriver.execute_script("return document.body.scrollHeight;")
        # width = SafariDriver.execute_script("return Math.max(document.body.scrollWidth, document.documentElement.scrollWidth);")
        # height = SafariDriver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);")
        # SafariDriver.set_window_size(width, height)
        
        # devicePixelRatioを考慮したウィンドウサイズを計算
        device_pixel_ratio = SafariDriver.execute_script("return window.devicePixelRatio;")
        width = SafariDriver.execute_script("return Math.max(document.body.scrollWidth, document.documentElement.scrollWidth);")
        height = SafariDriver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);")

        # ウィンドウサイズにデバイスピクセル比を掛ける
        SafariDriver.set_window_size(width * device_pixel_ratio, height * device_pixel_ratio)

        # スクリーンショットの取得
        ob = Screenshot.Screenshot()
        ob.full_screenshot(SafariDriver, save_path=os.path.dirname(screen_shot_file_path), 
            image_name=os.path.basename(screen_shot_file_path), is_load_at_runtime=True, load_wait_time=10)

        # HTMLコードを保存
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(SafariDriver.page_source)

        # ブラウザを閉じる
        SafariDriver.quit()

    except WebDriverException as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # コマンドライン引数からパスとURLを取得
    screen_shot_file_path = sys.argv[1]
    html_file_path = sys.argv[2]
    URL = sys.argv[3]

    run_test(screen_shot_file_path, html_file_path, URL)
