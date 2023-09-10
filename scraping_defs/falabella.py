from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

from app_types import SiteScrapingDefinition
from utils import findWithoutError, findMultipleWithoutError

def get_search_element_callback(driver: WebDriver):
    return findWithoutError(driver, By.ID, 'testId-SearchBar-Input')

def scraping_execution(driver: WebDriver, query: str):
    results = []
    # TODO: This site does not have a direct link to the next page that could be copied.
    # Instead, allow this return to either specify a url (str) or a button to click (web element).
    # next_page_button = findWithoutError(driver, By.ID, 'testId-pagination-bottom-arrow-right')
    products_divs = findMultipleWithoutError(findWithoutError(driver, By.ID, 'testId-searchResults-products'), By.XPATH, './div/div')

    for product_div in products_divs:
        internal_divs = findMultipleWithoutError(product_div, By.XPATH, './div')
        price_section = findWithoutError(product_div, By.XPATH, './a')

        if len(internal_divs) < 2:
            continue

        brand_element = findWithoutError(internal_divs[1], By.XPATH, './a/div/b')
        product_element = findWithoutError(internal_divs[1], By.XPATH, './a/span/b')
        price_elements = findMultipleWithoutError(price_section, By.XPATH, './div/ol/li/div/span')

        prices = []
        brand = brand_element.get_property('innerHTML')
        detail_link = price_section.get_attribute('href')
        title = product_element.get_property('innerHTML')

        if query.lower() not in title.lower():
            continue

        for price_element in price_elements:
            prices.append(price_element.get_property('innerHTML').split('-')[0].strip())
        
        results.append({
            'title': title,
            'brand': brand,
            'prices': prices,
            'detail_link': detail_link,
        })

    return (None, results)

def resolve_results_filename(query: str) -> str:
    return f'falabella_product_{query.lower().strip().replace(" ", "_")}'

site_scraping_definition: SiteScrapingDefinition = {
    'site_name': 'Falabella',
    'entrypoint': {
        'url': 'https://www.falabella.com/falabella-cl',
        'get_search_element': get_search_element_callback,
    },
    'scraping_execution_callback': scraping_execution,
    'get_storage_filename': resolve_results_filename
}