from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent import futures
import time
from selenium.common.exceptions import WebDriverException


BROWSER_NUMBER = 4
SESSION_NUMBER = 1
TOTAL_SESSION_NUMBER = BROWSER_NUMBER * SESSION_NUMBER


def test(browser, session_number):
    screen_shot_file_path = f'/home/pybatch/python/inout/screen_shot_{browser}_{session_number}.png'

    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')  # ヘッドレスモードで実行
        # options.add_argument('--disable-gpu')  # GPU を無効にする
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')  # ヘッドレスモードで実行
        # options.add_argument('--disable-gpu')  # GPU を無効にする
    elif browser == 'edge':
        options = webdriver.EdgeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')  # ヘッドレスモードで実行
        # options.add_argument('--disable-gpu')  # GPU を無効にする
    elif browser == 'safari':
        #Safariドライバ起動
        SafariDriver = webdriver.Safari()
        # options = Options()
        # driver = webdriver.Remote(command_executor='http://host.docker.internal:4446/wd/hub', options=options)
    else:
        raise ValueError("Invalid browser specified")
    
    # Safariの場合は上記で既にdriverが作成されているので、以下の行は不要
    if browser != 'safari':
        driver = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            options=options
        )
    if browser == 'safari':
        print(f"{browser} session {session_number}", )
        SafariDriver.maximize_window()
        time.sleep(1)
        #susakiworks表示
        SafariDriver.get('https://www.yahoo.co.jp/')
        time.sleep(3)
        # スクリーンショットを撮る
        SafariDriver.save_screenshot('susakiworks_screenshot.png')
        #ブラウザClose
        SafariDriver.quit()
    else:
        try:
            driver.get('https://www.yahoo.co.jp/')
            print(f"{browser} session {session_number}", driver.current_url)

            start_time = time.time()  # テストの開始時間を記録

            # スクリーンショットを取って保存
            driver.save_screenshot(screen_shot_file_path)

            end_time = time.time()  # テストの終了時間を記録
            elapsed_time = end_time - start_time  # テストの実行時間を計算
            print(f"{browser} session {session_number} Test elapsed time: {elapsed_time} seconds")

            driver.quit()

        except WebDriverException as e:
            print(f"Error with {browser} session {session_number}: {e}")
            elapsed_time = None

    return elapsed_time  # テストの実行時間を返す


""" main処理 """
print("----main.py is running.----")
# 処理開始時間を記録
start_time = time.time()



""" Selenium Gridの処理 """

future_list = []

# 各WebDriverでTOTAL_SESSION_NUMBERの数だけセッションを並列で実行
with futures.ThreadPoolExecutor(max_workers=TOTAL_SESSION_NUMBER) as executor:
    for browser in ['chrome', 'firefox', 'edge']:
        # SESSION_NUMBERに応じたセッション番号のリストを生成
        sessions = list(range(1, SESSION_NUMBER + 1))
        for session_number in sessions:
            future = executor.submit(test, browser, session_number)
            future_list.append(future)
            time.sleep(0.5)
_ = futures.wait(fs=future_list)  # 全てのテストが完了するのを待機

# 各テストの実行時間を取得
for future in future_list:
    elapsed_time = future.result()
    print(f"Test elapsed time: {elapsed_time} seconds")

# トータルの実行時間を計算
total_time = sum([result for future in future_list if (result := future.result()) is not None])
print(f"Total elapsed time: {total_time} seconds")

""" END """



# 処理終了時間を記録
end_time = time.time()
# 処理時間を計算して表示
execution_time = end_time - start_time
print("プログラム処理時間：", execution_time, "秒")