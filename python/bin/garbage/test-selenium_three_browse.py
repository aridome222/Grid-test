from selenium import webdriver
from concurrent import futures
import time
import os

def test(browser):
    screen_shot_file_path = f'/home/pybatch/python/inout/screen_shot_{browser}.png'

    # 指定したディレクトリが存在しない場合は作成する
    if not os.path.exists(screen_shot_file_path):
        os.makedirs(screen_shot_file_path)

    if browser == 'chrome':
        options = webdriver.ChromeOptions()
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
    elif browser == 'edge':
        options = webdriver.EdgeOptions()
    else:
        raise ValueError("Invalid browser specified")

    # `desired_capabilities`は削除し、`options`を直接使用
    driver = webdriver.Remote(
        command_executor='http://selenium-hub:4444/wd/hub',
        options=options
    )

    driver.get('https://www.yahoo.co.jp/')
    print(browser, driver.current_url)

    start_time = time.time()  # テストの開始時間を記録

    # スクリーンショットを取って保存
    driver.save_screenshot(screen_shot_file_path)

    end_time = time.time()  # テストの終了時間を記録
    elapsed_time = end_time - start_time  # テストの実行時間を計算
    print(f"{browser} Test elapsed time: {elapsed_time} seconds")

    driver.quit()

    return elapsed_time  # テストの実行時間を返す

future_list = []

# 各WebDriverでテストを実行
with futures.ThreadPoolExecutor(max_workers=3) as executor:
    for browser in ['chrome', 'firefox', 'edge']:
        future = executor.submit(test, browser)
        future_list.append(future)

_ = futures.wait(fs=future_list)  # 全てのテストが完了するのを待機

# 各テストの実行時間を取得
for future in future_list:
    elapsed_time = future.result()
    print(f"Test elapsed time: {elapsed_time} seconds")

# トータルの実行時間を計算
total_time = sum([future.result() for future in future_list])
print(f"Total elapsed time: {total_time} seconds")
