from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import re
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class Scraper:

    def scrape(self, keyword):
        """
        Input : Keyword: Scraper will scrape keyword's Wikipedia page 
        Enter to close the browser.
        Returns a string of the extracted info.
        """

        string = ''

        # Initialize Chrome options
        options = Options()
        options.add_argument("--headless")  # Run headless mode if you don't need a UI
        options.add_argument("--no-sandbox")  # Avoid sandbox issues
        options.add_argument("--disable-dev-shm-usage")  # Solve potential file descriptor issues

        service = Service(ChromeDriverManager().install())

        # Initialize the WebDriver with the proper options and service
        driver = webdriver.Chrome(service=service, options=options)


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

