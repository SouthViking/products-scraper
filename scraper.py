import os
import json
import time
import argparse
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

            total_results = { 'products': [] }

            self.driver.get(scraping_def['entrypoint']['url'])

            search_element = scraping_def['entrypoint']['get_search_element'](self.driver)
            if search_element is None:
                print(f'Could not resolve a search element for site {scraping_def["site_name"]}.')
                continue
            
            search_element.clear()
            search_element.send_keys(query)
            search_element.send_keys(Keys.RETURN)

            next_url, results = scraping_def['scraping_execution_callback'](self.driver, query)
            total_results['products'].extend(results)

            while next_url is not None:
                print(f'Got a new URL after scraping process for site: "{scraping_def["site_name"]}".')

                time.sleep(0.5)
                
                self.driver.get(next_url)
                
                next_url, results = scraping_def['scraping_execution_callback'](self.driver, query)
                total_results['products'].extend(results)

            storage_filename = scraping_def['get_storage_filename'](query)

            self.store_results(storage_filename, total_results)

            time.sleep(0.5)

        self.driver.close()

    def store_results(self, filename: str, data: dict):
        try:
            if filename is None or len(filename) == 0:
                print('Cannot save results. Filename is not valid.')
                return

            storage_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
            if not os.path.exists(storage_folder_path):
                os.mkdir(storage_folder_path)
            
            target_file_path = os.path.join(storage_folder_path, f'{filename}.json')

            with open(target_file_path, 'w', encoding = 'utf-8') as storage_file:
                json.dump(data, storage_file, indent = 4, ensure_ascii = False)    
        
        except Exception as error:
            print(f'There was a problem after trying to store results. Error: {error}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Web scraping for website products.')
    parser.add_argument('product', metavar ='p', type = str, help = 'The product to search')

    args = parser.parse_args().__dict__

    scraper = ProductsScraper({ 'scraping_defs': scraping_definitions })
    scraper.execute_search(args['product'])