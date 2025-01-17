"""
Title: Thu thập dữ liệu cơ bản về thị trường bất động sản Việt Nam
Author: Mai Vĩnh Khang
Description: None
Date: 14/01/2025
"""


from src.modules.services import RealEstateService

if __name__ == "__main__":
    # RealEstateService.crawl()
    raw_data = RealEstateService.run_pipeline()