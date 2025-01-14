import time
import numpy as np
import pandas as pd
from typing import Dict, Union
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException
)
from webdriver_manager.chrome import ChromeDriverManager

from src.common.consts import CommonConsts
from src.modules.entities.real_estate import RealEstate
from src.modules.repositories import RealEstateRepo
from src.utils.logger import LOGGER


class RealEstateService:
    repo = RealEstateRepo

    @classmethod
    def crawl(cls):
        cls.repo.initialize_db()

        # Set up Chrome driver
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--log-level=3")  # Suppress logs
        options.add_argument("--disable-logging")  # Disable logging
        options.add_argument("--silent")  # Silent mode
        # options.add_argument("headless")
        options.add_argument("window-size=1920x1080")
        options.add_argument("disable-gpu")
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(options=options, service=service)
        driver.set_page_load_timeout(30)
        link_all = [
            f"{CommonConsts.BASE_URL}/{elem}" for elem in CommonConsts.REAL_ESTATE_TYPES
        ]
        for i in np.arange(0, len(link_all), 1):
            real_estate_type = CommonConsts.REAL_ESTATE_TYPES[i]
            driver.get(link_all[i])
            time.sleep(2)
            total_page_str = driver.find_elements(By.CSS_SELECTOR, ".re__pagination-number")[-1].text
            total_page = int(total_page_str.split(" ")[-1])
            LOGGER.info(f"Total page of {real_estate_type}: {total_page}")


