from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from concurrent import futures
import time
import os
from enum import Enum

from cmd_runner import CommandRunner

# ブラウザを列挙体で定義
class Browser(Enum):
    CHROME = 'chrome'
    FIREFOX = 'firefox'
    EDGE = 'edge'
    SAFARI = 'safari'

# テストで使用するブラウザのリストを一箇所にまとめて定義
BROWSERS_TO_TEST = [Browser.CHROME, Browser.FIREFOX, Browser.EDGE, Browser.SAFARI]

# BROWSERS_TO_TESTの長さに基づいてBROWSER_NUMBERを設定
BROWSER_NUMBER = len(BROWSERS_TO_TEST)
SESSION_NUMBER = 1
TOTAL_SESSION_NUMBER = BROWSER_NUMBER * SESSION_NUMBER

URL = 'https://earth.cs.miyazaki-u.ac.jp/'

def test(browser, session_number):
    # SafariDriverかそれ以外かを判定
    if browser == Browser.SAFARI:
        # スクリーンショットの保存先を定義
        screen_shot_file_path = f'./python/inout/screen_shot_{browser.name}_{session_number}.png'
        # HTMLコードの保存先を定義
        html_file_path = f'./python/inout/page_source_{browser.name}_{session_number}.html'

        # スクリーンショット画像とHTMLコードの取得
        print(f"{browser.name} session {session_number}", URL)
        start_time = time.time()  # テストの開始時間を記録

        runner = CommandRunner("http://host.docker.internal:5001/run-command")
        output = runner.run_command("python3 ./python/bin/test-safari.py")

        """ TODO: エラーの場合の処理 """
        # if output == "error":
        #     print(f"Error with {browser.name} session {session_number}: {output}")
        #     elapsed_time = None
        
        """ 今はハードコーディングだけど、今後スクショに関する情報をローカルサーバ上に送信できるようにする """
        # # ウィンドウのサイズ設定
        # SafariDriver.maximize_window()
        # # アクセスするURL
        # SafariDriver.get('https://earth.cs.miyazaki-u.ac.jp/')
        # # スクリーンショットを保存
        # SafariDriver.save_screenshot(screen_shot_file_path)  
        # # HTMLコードを保存
        # with open(html_file_path, 'w', encoding='utf-8') as f:
        #     f.write(SafariDriver.page_source)

        """ 今は同期処理。今後、非同期処理にしたい。 """
        # time.sleep(1)  # 長い処理

        end_time = time.time()  # テストの終了時間を記録
        elapsed_time = end_time - start_time  # テストの実行時間を計算
        print(f"{browser.name} session {session_number} Test elapsed time: {elapsed_time} seconds")
    else:
        # スクリーンショットの保存先を定義
        screen_shot_file_path = f'/home/pybatch/python/inout/screen_shot_{browser.name}_{session_number}.png'
        # HTMLコードの保存先を定義
        html_file_path = f'/home/pybatch/python/inout/page_source_{browser.name}_{session_number}.html'
        
        # スクリーンショット画像とHTMLコードを保存するディレクトリのパス
        img_directory = os.path.dirname(screen_shot_file_path)
        # 指定したディレクトリが存在しない場合は作成する
        if not os.path.exists(img_directory):
            os.makedirs(img_directory)

        # RemoteWebDriverの設定
        if browser == Browser.CHROME:
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')  # ヘッドレスモードで実行
        elif browser == Browser.FIREFOX:
            options = webdriver.FirefoxOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')  # ヘッドレスモードで実行
        elif browser == Browser.EDGE:
            options = webdriver.EdgeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')  # ヘッドレスモードで実行
        else:
            raise ValueError("Invalid browser specified")
        
        driver = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            options=options
        )

        # スクリーンショット画像とHTMLコードの取得
        try:
            driver.get(URL)
            print(f"{browser.name} session {session_number}", driver.current_url)

            start_time = time.time()  # テストの開始時間を記録

            # スクリーンショットを保存
            driver.save_screenshot(screen_shot_file_path)
            
            # HTMLコードを保存
            with open(html_file_path, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)

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
