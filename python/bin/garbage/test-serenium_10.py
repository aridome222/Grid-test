from selenium import webdriver
from concurrent import futures
import time

def test(i):
    screen_shot_file_path = f'/home/pybatch/python/inout/screen_shot{i}.png'

    with webdriver.Remote(
        command_executor=f'http://selenium-hub:4444/wd/hub',
        options=webdriver.ChromeOptions(),
    ) as driver:
        driver.get('https://www.yahoo.co.jp/')
        print(i, driver.current_url)

        start_time = time.time()  # テストの開始時間を記録

        # スクリーンショットを取って保存
        driver.save_screenshot(screen_shot_file_path)

        end_time = time.time()  # テストの終了時間を記録
        elapsed_time = end_time - start_time  # テストの実行時間を計算
        print(f"Test {i} elapsed time: {elapsed_time} seconds")

    return elapsed_time  # テストの実行時間を返す

future_list = []

with futures.ThreadPoolExecutor(max_workers=3) as executor:
    for i in range(10):
        future = executor.submit(test, i)
        future_list.append(future)

    _ = futures.as_completed(fs=future_list)

# トータルの実行時間を計算
total_time = sum([future.result() for future in future_list])
print(f"Total elapsed time: {total_time} seconds")
