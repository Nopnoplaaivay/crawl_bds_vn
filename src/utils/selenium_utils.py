from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random

class SeleUtils:
    @staticmethod
    def find_elem_by_css(driver_element, css: str) :
        try:
            return driver_element.find_element(By.CSS_SELECTOR, css)
        except NoSuchElementException:
            return None
    @staticmethod
    def find_elems_by_css(driver_element, css: str):
        try:
            return driver_element.find_elements(By.CSS_SELECTOR, css)
        except NoSuchElementException:
            return None
                
    @staticmethod
    def find_wait_elem_by_css(driver_element, css: str, retries: int = 3, wait_time: int = 20):
        for attempt in range(retries):
            try:
                return WebDriverWait(driver_element, wait_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css))
                )
            except (TimeoutException, NoSuchElementException):
                if attempt < retries - 1:
                    time.sleep(random.randint(3, 5))
                else:
                    return None

    @staticmethod
    def find_wait_elems_by_css(driver_element, css: str, retries: int = 3, wait_time: int = 20):
        for attempt in range(retries):
            try:
                return WebDriverWait(driver_element, wait_time).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, css))
                )
            except (TimeoutException, NoSuchElementException):
                if attempt < retries - 1:
                    time.sleep(random.randint(3, 5))
                else:
                    return None