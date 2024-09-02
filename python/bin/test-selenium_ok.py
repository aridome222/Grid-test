from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent import futures
import time
from selenium.common.exceptions import WebDriverException
import os
from enum import Enum

# ブラウザを列挙体で定義
class Browser(Enum):
    CHROME = 'chrome'
    FIREFOX = 'firefox'
    EDGE = 'edge'
    SAFARI = 'safari'

# テストで使用するブラウザのリストを一箇所にまとめて定義
BROWSERS_TO_TEST = [Browser.CHROME, Browser.FIREFOX, Browser.EDGE]

# BROWSERS_TO_TESTの長さに基づいてBROWSER_NUMBERを設定
BROWSER_NUMBER = len(BROWSERS_TO_TEST)
SESSION_NUMBER = 2
TOTAL_SESSION_NUMBER = BROWSER_NUMBER * SESSION_NUMBER

def test(browser, session_number):
    screen_shot_file_path = f'/home/pybatch/python/inout/screen_shot_{browser.name}_{session_number}.png'
    img_directory = os.path.dirname(screen_shot_file_path)
    # 指定したディレクトリが存在しない場合は作成する
    if not os.path.exists(img_directory):
        os.makedirs(img_directory)

    if browser == Browser.CHROME:
        options = webdriver.ChromeOptions()
        # options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')  # ヘッドレスモードで実行
    elif browser == Browser.FIREFOX:
        options = webdriver.FirefoxOptions()
        # options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')  # ヘッドレスモードで実行
    elif browser == Browser.EDGE:
        options = webdriver.EdgeOptions()
        # options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')  # ヘッドレスモードで実行
    elif browser == Browser.SAFARI:
        SafariDriver = webdriver.Safari()
    else:
        raise ValueError("Invalid browser specified")
    
    # Safariの場合は上記で既にdriverが作成されているので、以下の行は不要
    if browser != Browser.SAFARI:
        driver = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            options=options
        )
        
    if browser == Browser.SAFARI:
        try:
            print(f"{browser.name} session {session_number}")
            SafariDriver.maximize_window()
            start_time = time.time()  # テストの開始時間を記録
            SafariDriver.get('https://www.yahoo.co.jp/')
            time.sleep(0.5)
            SafariDriver.save_screenshot(screen_shot_file_path)
            end_time = time.time()  # テストの終了時間を記録
            elapsed_time = end_time - start_time  # テストの実行時間を計算
            print(f"{browser.name} session {session_number} Test elapsed time: {elapsed_time} seconds")
            SafariDriver.quit()
        except WebDriverException as e:
            print(f"Error with {browser.name} session {session_number}: {e}")
            elapsed_time = None
    else:
        try:
            driver.get('https://www.yahoo.co.jp/')
            print(f"{browser.name} session {session_number}", driver.current_url)

            start_time = time.time()  # テストの開始時間を記録

            driver.save_screenshot(screen_shot_file_path)

            end_time = time.time()  # テストの終了時間を記録
            elapsed_time = end_time - start_time  # テストの実行時間を計算
            print(f"{browser.name} session {session_number} Test elapsed time: {elapsed_time} seconds")

            driver.quit()

        except WebDriverException as e:
            print(f"Error with {browser.name} session {session_number}: {e}")
            elapsed_time = None

    return elapsed_time  # テストの実行時間を返す

""" main処理 """
print("----main.py is running.----")
all_start_time = time.time()

future_list = []

# 各WebDriverでTOTAL_SESSION_NUMBERの数だけセッションを並列で実行
with futures.ThreadPoolExecutor(max_workers=TOTAL_SESSION_NUMBER) as executor:
    for browser in BROWSERS_TO_TEST:  # ブラウザリストを参照
        sessions = list(range(1, SESSION_NUMBER + 1))
        for session_number in sessions:
            future = executor.submit(test, browser, session_number)
            future_list.append(future)

_ = futures.wait(fs=future_list)  # 全てのテストが完了するのを待機

for future in future_list:
    elapsed_time = future.result()
    print(f"Test elapsed time: {elapsed_time} seconds")

total_time = sum([result for future in future_list if (result := future.result()) is not None])
print(f"Total elapsed time: {total_time} seconds")

""" END """

all_end_time = time.time()
execution_time = all_end_time - all_start_time
print("プログラム処理時間：", execution_time, "秒")
