from selenium import webdriver
from selenium.webdriver.safari.options import Options
import time

def main():
    print("スタート")
    hub_host = "172.19.0.3"  # ここに確認したIPアドレスを設定
    hub_port = "4444"
    command_executor_url = f'http://{hub_host}:{hub_port}/wd/hub'
    print(f"コマンドエグゼキュータURL: {command_executor_url}")

    safari_options = Options()
    
    print("Safari options 取得")
    driver = None
    try:
        driver = webdriver.Remote(
            command_executor=command_executor_url,
            options=safari_options
        )
        
        # テストコード
        print("URLアクセス")
        driver.get("https://www.example.com")
        print(driver.title)
    except Exception as e:
        print(f"WebDriverの初期化エラー: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
