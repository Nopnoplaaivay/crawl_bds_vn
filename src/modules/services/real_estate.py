import time
import random
import json
from typing import Dict, Union
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException
)
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


from src.common.consts import CommonConsts
from src.modules.entities.real_estate import RealEstate
from src.modules.repositories import RealEstateRepo
from src.base.services import BaseService
from src.utils.logger import LOGGER
from src.utils.selenium_utils import SeleUtils


class RealEstateService(BaseService):
    repo = RealEstateRepo

    @classmethod
    def crawl(cls) -> None:
        '''
        SETUP CHROME DRIVER
        '''
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--log-level=3")  
        options.add_argument("--disable-logging")  
        options.add_argument("--silent") 
        # options.add_argument("headless")
        options.add_argument("window-size=1920x1080")
        options.add_argument("disable-gpu")
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(options=options, service=service)
        driver.set_page_load_timeout(60)

        '''
        INITIALIZE DATABASE
        '''
        cls.repo.initialize_db()

        '''
        PROCESS TRACKING
        '''
        process = cls.load_process()

        '''
        ITERATE THROUGH REAL ESTATE STATUS: "nha-dat-ban" / "nha-dat-cho-thue"
        '''
        link_all = [f"{CommonConsts.BASE_URL}/{elem}" for elem in CommonConsts.REAL_ESTATE_STATUS]
        for link_idx in range(len(link_all)):
            driver.get(link_all[link_idx])
            real_estate_status = CommonConsts.REAL_ESTATE_STATUS[link_idx]
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
            re_type_mapping = {}
            for li in filter_properties["re_elems"][1:]:
                get_elems_actions.move_to_element(li).perform()
                try:
                    ul = li.find_element(By.CSS_SELECTOR, "ul")
                    li_elems = ul.find_elements(By.CSS_SELECTOR, "li")
                    for li_elem in li_elems:
                        re_text = li_elem.text
                        re_type_id = li_elem.get_attribute("value")

                        re_type_texts.add(re_text)
                        re_type_ids.add(re_type_id)
                        re_type_mapping[f"{re_type_id}"] = re_text

                        if f"{re_type_id}" not in process[re_status]:
                            process[re_status][f"{re_type_id}"] = 1

                except NoSuchElementException:
                        re_text = li.text
                        re_type_id = li.get_attribute("value")

                        re_type_texts.add(re_text)
                        re_type_ids.add(re_type_id)
                        re_type_mapping[f"{re_type_id}"] = re_text

                        if f"{re_type_id}" not in process[re_status]:
                            process[re_status][f"{re_type_id}"] = 1
            re_type_ids = list(re_type_ids)

            # Escape filter box
            filter_properties["re_filter_button"].click()


            '''
            CHECKING REAL ESTATE TYPES & ITERATE THROUGH EACH TYPE TO CRAWL
            '''
            check_elems_actions = ActionChains(driver) 
            for re_type_id in re_type_ids:
                # Get new filter properties
                new_filter_properties = cls.get_filter_properties(driver)

                # Select real estate type
                check_elems_actions.move_to_element(new_filter_properties["re_all_types_elem"]).perform()
                new_filter_properties["re_all_types_elem"].click()
                time.sleep(1)
                new_filter_properties["re_all_types_elem"].click()
                check_box = new_filter_properties["re_filter_box"].find_element(By.CSS_SELECTOR, f"[value='{re_type_id}']")
                check_elems_actions.move_to_element(check_box).perform()
                check_box.click()

                # re_type = check_box.text
                re_type = re_type_mapping[f"{re_type_id}"]
                LOGGER.info(f"Crawling {re_type}...")
                new_filter_properties["re_apply_button"].click()
                time.sleep(3)

                '''
                START CRAWLING
                '''
                total_page_elem = driver.find_elements(By.CSS_SELECTOR, ".re__pagination-number")
                total_page = int(total_page_elem[-1].text.replace('.', '')) if len(total_page_elem) > 0 else 1
                current_url = driver.current_url
                LOGGER.info(f"Total pages: {total_page}")


                for page in range(process[re_status][f"{re_type_id}"], total_page + 1):
                    # Navigate to page
                    time.sleep(random.randint(3, 5))
                    if total_page > 1:
                        try:
                            driver.get(f"{current_url}/p{page}")
                            LOGGER.info(f"Crawling page {page} of {re_type}...")
                            time.sleep(random.randint(3, 5))
                        except TimeoutException:
                            LOGGER.error(f"Page {page} of {re_type} not found")
                            continue


                    try:
                        re_divs = driver.find_elements(By.CSS_SELECTOR, ".re__srp-list .js__card.js__card-full-web")
                        for idx, re in enumerate(re_divs):
                            parent = re.find_element(By.XPATH, "..")
                            if "re__srp-list" in parent.get_attribute("class"): # Exclude ads
                                # Get raw data
                                re_title = SeleUtils.find_elem_by_css(re, ".re__card-info") 
                                re_location = SeleUtils.find_elem_by_css(re, ".re__card-location")
                                re_price = SeleUtils.find_elem_by_css(re, ".re__card-config-price.js__card-config-item")
                                re_area = SeleUtils.find_elem_by_css(re, ".re__card-config-area.js__card-config-item")
                                re_desc = SeleUtils.find_elem_by_css(re, ".re__card-description.js__card-description")
                                re_url = SeleUtils.find_elem_by_css(re, ".js__product-link-for-product-id")

                                # Transform data
                                data = {
                                    "status": real_estate_status,
                                    "type": re_type,
                                    "title": re_title.get_attribute("title") if re_title else None,
                                    "location": re_location.text.strip().replace("·", "").strip() if re_location else None,
                                    "price": re_price.text.strip() if re_price else None,
                                    "area": re_area.text.strip() if re_area else None,
                                    "desc": re_desc.text.strip() if re_desc else None,
                                    "url": re_url.get_attribute("href") if re_url else None
                                }
                                LOGGER.info(f"{idx + 1}: {data['url']}")
                                
                                # Insert data
                                real_estate = RealEstate(
                                    status=data["status"],
                                    type=data["type"],
                                    title=data["title"],
                                    location=data["location"],
                                    price=data["price"],
                                    area=data["area"],
                                    desc=data["desc"],
                                    url=data["url"]
                                )
                                cls.repo.insert(real_estate)

                        # Update process
                        process[re_status][f"{re_type_id}"] = page + 1
                        cls.save_process(process)

                    except TimeoutException:
                        LOGGER.error(f"TimeoutException at page {page} of {re_type}")
                        process[re_status][f"{re_type_id}"] = page  
                        continue

                '''
                Navigate to the next status page:
                '''
                driver.get(link_all[link_idx])
        
        driver.quit()
        LOGGER.info("===== DONE =====")

    @staticmethod
    def get_filter_properties(driver) -> Dict[str, Union[WebElement, list]]:
        re_filter_button = SeleUtils.find_wait_elem_by_css(driver, "div[data-default-value='Loại nhà đất']")
        re_filter_button.click()
        re_filter_box = SeleUtils.find_elem_by_css(driver, ".re__listing-search-select-dropdown.re__multiple.js__listing-search-select-select-dropdown.re__show-fade-in")
        re_elems = SeleUtils.find_elems_by_css(re_filter_box, "li")
        re_apply_button = SeleUtils.find_elem_by_css(re_filter_box, ".re__btn.re__btn-pr-solid--sm.js__listing-search-select-apply-button")
        re_all_types_elem = re_elems[0] if len(re_elems) > 0 else None

        return {
            "re_filter_button": re_filter_button,
            "re_filter_box": re_filter_box,
            "re_elems": re_elems,
            "re_apply_button": re_apply_button,
            "re_all_types_elem": re_all_types_elem
        }


# List of real estate levels for future use
# real_estates_diamond = driver.find_elements(By.CSS_SELECTOR, ".js__card.js__card-full-web.pr-container.re__card-full.re__vip-diamond")
# real_estates_gold = driver.find_elements(By.CSS_SELECTOR, ".js__card.js__card-full-web.re__boosting-cta-section-version-b.pr-container.re__card-full.re__vip-gold")
# real_estates_silver = driver.find_elements(By.CSS_SELECTOR, ".js__card.js__card-full-web.re__boosting-cta-section-version-b.pr-container.re__card-full.re__vip-silver")
# real_estates_normal = driver.find_elements(By.CSS_SELECTOR, ".js__card.js__card-full-web.re__boosting-cta-section-version-b.pr-container.re__card-full.re__vip-normal")
# real_estates_no_label = driver.find_elements(By.CSS_SELECTOR, "js__card.js__card-full-web.card-custom-listing-desktoppr-container.re__card-full.re__card-full-ads.re__card-full-no-label")
# real_estates = real_estates_diamond + real_estates_gold + real_estates_silver + real_estates_normal