from typing import Callable, List, Union, Tuple, TypedDict
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

class SiteEntryPointDefinition(TypedDict):
    # The URL that will be opened by the driver.
    url: str;
    # The function that will run to resolve the search element for the site.
    get_search_element: Callable[[WebDriver], Union[WebElement, None]]

class SiteScrapingDefinition(TypedDict):
    site_name: str;
    # The definition of the url and search element of the site to execute the query.
    entrypoint: SiteEntryPointDefinition
    # Callback to perform the scraping and that will run after running the query in the website.
    # It returns a tuple containing the next page link (in case there is one) and the list of obtained results.
    scraping_execution_callback: Callable[[WebDriver, str], Tuple[Union[str, None], List[dict]]]
    # Callback to resolve the name of the file where the results will be executed. Takes the initial query as input.
    get_storage_filename: Callable[[str], str]