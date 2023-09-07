import time
from typing import List, TypedDict

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from app_types import SiteScrapingDefinition
from scraping_defs import scraping_definitions

class ProductsScraperConfig(TypedDict):
    scraping_defs: List[SiteScrapingDefinition]

class ProductsScraper:
    def __init__(self, config: ProductsScraperConfig):
        self.config = config
        # TODO: Allow to select a specific driver and its configuration.
        self.driver = webdriver.Chrome()

    def execute_search(self, query: str):
        print(f'Executing search for query: "{query}".')

        for scraping_def in self.config['scraping_defs']:
            print(f'Executing scraping for site: "{scraping_def["site_name"]}".')

            self.driver.get(scraping_def['entrypoint']['url'])

            search_element = scraping_def['entrypoint']['get_search_element'](self.driver)
            if search_element is None:
                print(f'Could not resolve a search element for site {scraping_def["site_name"]}.')
                continue
            
            search_element.clear()
            search_element.send_keys(query)
            search_element.send_keys(Keys.RETURN)

            next_url = scraping_def['scraping_execution_callback'](self.driver, query)

            while next_url is not None:
                print(f'Got a new URL after scraping process for site: "{scraping_def["site_name"]}".')

                time.sleep(0.5)
                
                self.driver.get(next_url)
                
                next_url = scraping_def['scraping_execution_callback'](self.driver, query)

            if next_url is not None:
                print(f'Got a new URL after scraping process for site: "{scraping_def["site_name"]}".')

            time.sleep(0.5)

        self.driver.close()


if __name__ == '__main__':
    scraper = ProductsScraper({ 'scraping_defs': scraping_definitions })
    scraper.execute_search('MSI Geforce RTX')