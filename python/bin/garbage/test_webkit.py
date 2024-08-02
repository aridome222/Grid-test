from selenium.webdriver.common.by import By
from selenium import webdriver
import unittest

class WebKitFeatureStatusTest(unittest.TestCase):

    def setUp(self):
        # SafariDriverを初期化
        self.driver = webdriver.Safari()

    def tearDown(self):
        # SafariDriverを終了
        self.driver.quit()

    def test_feature_status_page_search(self):
        self.driver.get("https://webkit.org/status/")

        # "CSS"を検索ボックスに入力
        search_box = self.driver.find_element_by_id("search")
        search_box.send_keys("CSS")
        value = search_box.get_attribute("value")
        self.assertTrue(len(value) > 0)
        search_box.submit()

        # 検索結果の数をカウント
        feature_count = self.shown_feature_count()
        self.assertTrue(len(feature_count) > 0)

    def test_feature_status_page_filters(self):
        self.driver.get("https://webkit.org/status/")

        filters = self.driver.find_elements(By.CSS_SELECTOR, "ul#status-filters li input[type=checkbox]")
        self.assertTrue(len(filters) == 7)  # "is"ではなく"=="を使用

        # すべてのフィルターがオフになっていることを確認
        for checked_filter in filter(lambda f: f.is_selected(), filters):
            checked_filter.click()

        # 各フィルターが選択されたときのアイテム数をカウント
        unfiltered_count = self.shown_feature_count()
        running_count = 0
        for filt in filters:
            filt.click()
            self.assertTrue(filt.is_selected())
            running_count += self.shown_feature_count()
            filt.click()

        self.assertTrue(running_count == unfiltered_count)  # "is"ではなく"=="を使用

    def shown_feature_count(self):
        return len(self.driver.execute_script("return document.querySelectorAll('li.feature:not(.is-hidden)')"))

if __name__ == '__main__':
    unittest.main()
