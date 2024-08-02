from selenium import webdriver
import time
#Safariドライバ起動
SafariDriver = webdriver.Safari()
SafariDriver.maximize_window()
time.sleep(1)
#susakiworks表示
SafariDriver.get('https://www.susakiworks.com')
time.sleep(3)
# スクリーンショットを撮る
SafariDriver.save_screenshot('susakiworks_screenshot.png')
#ブラウザClose
SafariDriver.quit()