from selenium import webdriver
import unittest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=webdriver.SafariOptions()
        )

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.submit()
        self.assertIn("No results found.", driver.page_source)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
