from typing import Union, List

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

def findWithoutError(source: Union[WebDriver, WebElement], by: str, value: str) -> Union[WebElement , None]:
    try:
        return source.find_element(by, value)
    except NoSuchElementException:
        return None
    
def findMultipleWithoutError(source: Union[WebDriver, WebElement], by: str, value: str) -> Union[List[WebElement] , None]:
    try:
        return source.find_elements(by, value)
    except NoSuchElementException:
        return None