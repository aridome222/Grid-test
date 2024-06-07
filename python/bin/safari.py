from selenium.webdriver import Safari

# Safariオプションを設定
options = Safari.Options()
# Optional: Use Safari Technology Preview
options.set_capability('safari:useTechnologyPreview', True)

# Safariドライバーを初期化
driver = Safari(options=options)

# ウェブページを開く
driver.get("https://www.example.com")

# ウェブページのタイトルを取得して表示
print(driver.title)

# ブラウザを閉じる
driver.quit()
