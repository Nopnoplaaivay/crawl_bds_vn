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
from selenium.webdriver.common.action_chains import ActionChains
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
        options.add_argument("--log-level=3")  
        options.add_argument("--disable-logging")  
        options.add_argument("--silent") 
        # options.add_argument("headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("window-size=1920x1080")
        options.add_argument("disable-gpu")
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(options=options, service=service)
        driver.set_page_load_timeout(30)
        link_all = [
            f"{CommonConsts.BASE_URL}/{elem}" for elem in CommonConsts.REAL_ESTATE_STATUS
        ]
        for i in np.arange(0, len(link_all), 1):
            driver.get(link_all[i])
            real_estate_status = CommonConsts.REAL_ESTATE_STATUS[i]
            if real_estate_status == "nha-dat-ban":
                LOGGER.info("===== Crawling NHÀ ĐẤT BÁN =====")
                re_status = "sell"
            else:
                LOGGER.info("===== Crawling NHÀ ĐẤT CHO THUÊ =====")
                re_status = "rent"
            time.sleep(2)
            
            ''' 
            GET REAL ESTATE TYPES 
            '''
            filter_properties = cls.get_filter_properties(driver)
            get_elems_actions = ActionChains(driver)
            re_type_texts = set()
            re_type_ids = set()
            for li in filter_properties["re_elems"][1:]:
                get_elems_actions.move_to_element(li).perform()
                try:
                    ul = li.find_element(By.CSS_SELECTOR, "ul")
                    li_elems = ul.find_elements(By.CSS_SELECTOR, "li")
                    for li_elem in li_elems:
                            re_type_texts.add(li_elem.text)
                            re_type_ids.add(li_elem.get_attribute("value"))
                except NoSuchElementException:
                        re_type_texts.add(li.text)
                        re_type_ids.add(li.get_attribute("value"))
            re_type_ids = list(re_type_ids)
            # Escape filter box
            filter_properties["re_filter_button"].click()


            '''
            CHECKING REAL ESTATE TYPES & ITERATE THROUGH EACH TYPE TO CRAWL
            '''
            check_elems_actions = ActionChains(driver) 
            for id in re_type_ids:
                # Get new filter properties
                new_filter_properties = cls.get_filter_properties(driver)

                check_elems_actions.move_to_element(new_filter_properties["re_all_types_elem"]).perform()
                new_filter_properties["re_all_types_elem"].click()
                time.sleep(1)
                new_filter_properties["re_all_types_elem"].click()
                check_box = new_filter_properties["re_filter_box"].find_element(By.CSS_SELECTOR, f"[value='{id}']")
                check_elems_actions.move_to_element(check_box).perform()
                check_box.click()

                re_type = check_box.text
                LOGGER.info(f"Crawling {re_type}...")
                new_filter_properties["re_apply_button"].click()
                time.sleep(3)

                '''
                START CRAWLING
                '''
                total_page_elem = driver.find_elements(By.CSS_SELECTOR, ".re__pagination-number")
                total_page = int(total_page_elem[-1].text.replace('.', '')) if len(total_page_elem) > 0 else 1
                LOGGER.info(f"{total_page}")
                # for page in np.arange(1, total_page + 1, 1):
                for page in np.arange(1, 3, 1):
                    # Click page button
                    if total_page > 1:
                        try:
                            page_button_str = f".re__pagination-number[pid='{page}']"
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, page_button_str))
                            )
                            driver.find_element(By.CSS_SELECTOR, page_button_str).click()
                        except (
                            NoSuchElementException, 
                            ElementClickInterceptedException, 
                            StaleElementReferenceException
                        ):
                            LOGGER.error(f"Page {page} of {re_type} not found")
                            continue

                    # Get list of real estate
                    real_estates_diamond = driver.find_elements(By.CSS_SELECTOR, ".js__card.js__card-full-web.pr-container.re__card-full.re__vip-diamond")
                    real_estates_gold = driver.find_elements(By.CSS_SELECTOR, ".js__card.js__card-full-web.re__boosting-cta-section-version-b.pr-container.re__card-full.re__vip-gold")
                    real_estates_silver = driver.find_elements(By.CSS_SELECTOR, ".js__card.js__card-full-web.re__boosting-cta-section-version-b.pr-container.re__card-full.re__vip-silver")
                    real_estates_normal = driver.find_elements(By.CSS_SELECTOR, ".js__card.js__card-full-web.re__boosting-cta-section-version-b.pr-container.re__card-full.re__vip-normal")
                    # real_estates_normal = driver.find_elements(By.CSS_SELECTOR, "js__card.js__card-full-web.card-custom-listing-desktoppr-container.re__card-full.re__card-full-ads.re__card-full-no-label")

                    real_estates = real_estates_diamond + real_estates_gold + real_estates_silver + real_estates_normal
                    LOGGER.info(len(real_estates))


                    # for re in real_estates:
                    #     try:
                    #         title = re.find_element(By.CSS_SELECTOR, ".pr-title.js__card-title").text
                    #         location = re.find_element(By.CSS_SELECTOR, ".re__card-location").find_elements(By.CSS_SELECTOR, "span")[-1].text
                    #         price = re.find_element(By.CSS_SELECTOR, ".re__card-config-price.js__card-config-item").text
                    #         area = re.find_element(By.CSS_SELECTOR, ".re__card-config-area.js__card-config-item").text
                    #         desc = re.find_element(By.CSS_SELECTOR, ".re__card-description.js__card-description").text
                    #         url = re.find_element(By.CSS_SELECTOR, ".js__product-link-for-product-id").get_attribute("href")
                            
                    #         real_estate = RealEstate(
                    #             status=real_estate_status,
                    #             type=re_type,
                    #             title=title,
                    #             location=location,
                    #             price=price,
                    #             area=area,
                    #             desc=desc,
                    #             url=url
                    #         )
                    #         cls.repo.insert(real_estate)
                    #     except Exception as e:
                    #         LOGGER.error(f"Error crawling {re_type}: {e}")


                '''
                Navigate back to the status page: "nha-dat-ban" / "nha-dat-cho-thue"
                '''
                driver.get(link_all[i])



            # total_page_str = driver.find_elements(By.CSS_SELECTOR, ".re__pagination-number")[-1].text
            # total_page = int(total_page_str.replace('.', ''))
            # LOGGER.info(f"Total page of {real_estate_type}: {total_page}")

            # for page in np.arange(1, total_page + 1, 1):
            #     # Click page button
            #     try:
            #         page_button_str = f".re__pagination-number[pid='{page}']"
            #         WebDriverWait(driver, 10).until(
            #             EC.presence_of_element_located((By.CSS_SELECTOR, page_button_str))
            #         )
            #         driver.find_element(By.CSS_SELECTOR, page_button_str).click()
            #     except (
            #         ElementClickInterceptedException, 
            #         NoSuchElementException, 
            #         StaleElementReferenceException
            #     ):
            #         LOGGER.error(f"Page {page} of {real_estate_type} not found")
            #         continue

            #     # Get list of real estate
            #     real_estates = driver.find_elements(By.CSS_SELECTOR, ".js__card.js__card-full-web.pr-container.re__card-full.re__vip-diamond")
            #     print(len(real_estates))
            #     for re in real_estates:
            #         # try:
            #             title = re.find_element(By.CSS_SELECTOR, ".pr-title.js__card-title").text
            #             location = re.find_element(By.CSS_SELECTOR, ".re__card-location").find_elements(By.CSS_SELECTOR, "span")[-1].text
            #             price = re.find_element(By.CSS_SELECTOR, ".re__card-config-price.js__card-config-item").text
            #             area = re.find_element(By.CSS_SELECTOR, ".re__card-config-area.js__card-config-item").text
            #             desc = re.find_element(By.CSS_SELECTOR, ".re__card-description.js__card-description").text
            #             url = re.find_element(By.CSS_SELECTOR, ".js__product-link-for-product-id").get_attribute("href")
                        
            #             real_estate = RealEstate(
            #                 id=None,
            #                 status=real_estate_type,
            #                 type="not_crawl",
            #                 title=title,
            #                 location=location,
            #                 price=price,
            #                 area=area,
            #                 desc=desc,
            #                 url=url
            #             )
            #             cls.repo.insert(real_estate)
            #         # except Exception as e:
            #         #     LOGGER.error(f"Error: {e}")
        LOGGER.info("===== DONE =====")

    @staticmethod
    def get_filter_properties(driver):
        re_filter_button = driver.find_element(By.CSS_SELECTOR, "div[data-default-value='Loại nhà đất']")
        re_filter_button.click()
        re_filter_box = driver.find_element(By.CSS_SELECTOR, ".re__listing-search-select-dropdown.re__multiple.js__listing-search-select-select-dropdown.re__show-fade-in")
        re_elems = re_filter_box.find_elements(By.CSS_SELECTOR, "li")
        re_apply_button = re_filter_box.find_element(By.CSS_SELECTOR, ".re__btn.re__btn-pr-solid--sm.js__listing-search-select-apply-button")
        re_all_types_elem = re_elems[0]

        return {
            "re_filter_button": re_filter_button,
            "re_filter_box": re_filter_box,
            "re_elems": re_elems,
            "re_apply_button": re_apply_button,
            "re_all_types_elem": re_all_types_elem
        }