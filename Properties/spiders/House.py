import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse
import time

class HouseSpider(scrapy.Spider):
    name = "House"
    allowed_domains = ["bayut.com"]
    start_urls = ['https://www.bayut.com/property-market-analysis/sale/?time_since_creation=6m']
    page_count = 1
    max_pages = 3400

    def __init__(self, *args, **kwargs):
        super(HouseSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)

    def parse(self, response):
        self.logger.info(f"Parsing page {self.page_count}")

        self.driver.get(response.url)
        time.sleep(5)  # Wait for JavaScript to load the content

        rows = self.driver.find_elements(By.CSS_SELECTOR, 'tr[aria-label="Listing"]')
        if rows:
            self.logger.info(f"Found {len(rows)} rows on page {self.page_count}")
        else:
            self.logger.warning("No rows found")

        for row in rows:
            date = row.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text
            location = row.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text
            price = row.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text
            beds = row.find_element(By.CSS_SELECTOR, 'td:nth-child(5)').text
            area_size = row.find_element(By.CSS_SELECTOR, 'td:nth-child(6)').text

            yield {
                'date': date,
                'location': location,
                'price': price,
                'beds': beds,
                'area_size': area_size,
            }

        if self.page_count < self.max_pages:
            try:
                next_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[title="Next"]')))
                next_button.click()
                self.page_count += 1
                time.sleep(5)  # Wait for the next page to load
                # Create a new HtmlResponse object to parse the new page
                new_response = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
                yield from self.parse(new_response)
            except Exception as e:
                self.logger.error(f"Error finding next page: {e}")
        else:
            self.logger.info("Reached max page limit")

    def closed(self, reason):
        self.driver.quit()




