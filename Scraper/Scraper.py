from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time

class Scraper:

    def scrape(self, keyword):
        """
        Input : Keyword: Scraper will scrape keyword's Wikipedia page 
        Enter to close the browser.
        Returns a string of the extracted info.
        """
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('window-size=1200x7000')
        options.add_argument('--headless')

        string = ''

        driver = webdriver.Chrome(options=options)

        try:
            url = 'https://en.wikipedia.org/wiki/' + keyword
            driver.get(url)

            # Allow time for page to load completely
            time.sleep(2)

            # Refetch elements in each iteration to avoid stale references
            texts = driver.find_elements(By.TAG_NAME, 'p')
            for i in range(len(texts)):
                try:
                    # Refetch the element before accessing it
                    para = driver.find_elements(By.TAG_NAME, 'p')[i].text
                    para = re.sub(r"[\(\[].*?[\)\]]", "", para)
                    string += para
                except Exception as e:
                    print(f"Skipping paragraph {i} due to an error: {e}")
                    continue

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Ensure the browser is closed in case of errors
            driver.quit()

        return string

