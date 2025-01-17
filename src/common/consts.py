import os

class CommonConsts:
    ROOT_FOLDER = os.path.abspath(os.path.join(os.path.abspath(__file__), 2 * "../"))
    DATA_PATH = os.path.join(ROOT_FOLDER, "data")
    TEMP_PATH = os.path.join(ROOT_FOLDER, "tmp")
    
    
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    CRAWLING_DAY_FORMAT = "%Y-%m-%d"
    
    
    BASE_URL = "https://batdongsan.com.vn"
    REAL_ESTATE_STATUS = [
        "nha-dat-ban",
        "nha-dat-cho-thue"
    ]
    UNIT_MULTIPLIERS = {
        "tỷ": 1e9,
        "triệu": 1e6,
        "nghìn": 1e3,
        "tỷ/tháng": 1e9,
        "triệu/tháng": 1e6,
        "nghìn/tháng": 1e3,
        "triệu/m²": 1e6,
        "nghìn/m²": 1e3
    }