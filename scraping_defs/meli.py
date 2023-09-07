from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

from app_types import SiteScrapingDefinition
from utils import findWithoutError, findMultipleWithoutError

def get_search_element_callback(driver: WebDriver):
    return findWithoutError(driver, By.NAME, 'as_word')

def scraping_execution(driver: WebDriver, query: str):
    product_list = findMultipleWithoutError(driver, By.TAG_NAME, 'ol')
    if product_list is None or len(product_list) != 2:
        return
    
    # Taking the list of products from the second element.
    # The first ol tag references the side bar of the page.
    product_list_element = product_list[1]
    row_elements = findMultipleWithoutError(product_list_element, By.TAG_NAME, 'li')
    
    for row in row_elements:
        link_element = findMultipleWithoutError(row, By.TAG_NAME, 'a')
        title_element = findWithoutError(row, By.TAG_NAME, 'h2')
        prices_element = findMultipleWithoutError(row, By.CLASS_NAME, 'andes-money-amount__fraction')
        rating_element = findWithoutError(row, By.CLASS_NAME, 'ui-search-reviews__rating-number')

        if title_element is None or prices_element is None or len(prices_element) == 0:
            continue

        title = title_element.get_attribute('innerHTML') or ''

        if query.lower() not in title.lower():
            continue

        previous_price = None
        if len(prices_element) == 2:
            # When there are 2 elements, then the first one is the price, while the second
            # represents a text with the available fee/quota, so there is no previous price.
            # The previous price applies only when there is an offer for the product.
            # TODO: Create an util function for the products to sanitize the prices in a more fancy way.
            # (would need to check the currency as well to sanitize it correctly)
            current_price = int(prices_element[0].get_attribute('innerHTML').replace('$', '').replace('.', ''))
        
        else:
            # The other case is when there are 3 elements. These are: previous price, current price and available fee/quota.
            previous_price = prices_element[0].get_attribute('innerHTML').replace('$', '').replace('.', '')
            current_price = prices_element[0].get_attribute('innerHTML').replace('$', '').replace('.', '')

        rating = None
        if rating_element is not None:
            rating = rating_element.get_attribute('innerHTML')

        link = None
        if len(link_element) != 0:
            link = link_element[0].get_attribute('href')

        print(title, previous_price, current_price, rating, link)

    pagination_link_elements = findMultipleWithoutError(driver, By.CSS_SELECTOR, '.andes-pagination__link.shops__pagination-link.ui-search-link')
    if pagination_link_elements is None or len(pagination_link_elements) == 0:
        return
    
    # Taking the last element, since for cases when the page is in the middle, there will be both, back and next links.
    target_link_element = pagination_link_elements[-1]

    if target_link_element.get_attribute('title').lower() == 'siguiente':
        # There is at least one more page to check.
        return target_link_element.get_attribute('href')


site_scraping_definition: SiteScrapingDefinition = {
    'site_name': 'Mercado Libre',
    'entrypoint': {
        'url': 'https://www.mercadolibre.cl/',
        'get_search_element': get_search_element_callback,
    },
    'scraping_execution_callback': scraping_execution,
} 