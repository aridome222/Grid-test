# from selenium import webdriver
# import logging

# logging.basicConfig(level=logging.DEBUG)

# def build_safari_driver():
#     driver = webdriver.Safari()
#     return driver

# def main():
#     try:
#         web_driver = build_safari_driver()
#         web_driver.get("https://www.google.com/")
#         print("Page title is: ", web_driver.title)
#     except Exception as e:
#         print("An error occurred:", e)
#     finally:
#         if 'web_driver' in locals():
#             web_driver.quit()

# if __name__ == "__main__":
#     main()
from selenium import webdriver
import logging

logging.basicConfig(level=logging.DEBUG)

def build_safari_driver():
    driver = webdriver.Safari('/System/Cryptexes/App/usr/bin/safaridriver')
    return driver

def main():
    try:
        web_driver = build_safari_driver()
        web_driver.get("https://www.google.com/")
        print("Page title is: ", web_driver.title)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        if 'web_driver' in locals():
            web_driver.quit()

if __name__ == "__main__":
    main()
