import os

class CommonConsts:
    ROOT_FOLDER = os.path.abspath(os.path.join(os.path.abspath(__file__), 2 * "../"))
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    CRAWLING_DAY_FORMAT = "%Y-%m-%d"
    
    BASE_URL = "https://batdongsan.com.vn"
    REAL_ESTATE_TYPES = [
        "nha-dat-ban",
        "nha-dat-cho-thue",
    ]
    DATA_PATH = os.path.join(ROOT_FOLDER, "data")