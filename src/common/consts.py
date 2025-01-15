import os

class CommonConsts:
    ROOT_FOLDER = os.path.abspath(os.path.join(os.path.abspath(__file__), 2 * "../"))
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    CRAWLING_DAY_FORMAT = "%Y-%m-%d"
    
    BASE_URL = "https://batdongsan.com.vn"
    REAL_ESTATE_TYPES = {
        "nha-dat-ban": [
            "Chung cư mini, căn hộ dịch vụ",
            "Nhà riêng",
            "Nhà biệt thự, liền kề",
            "Nhà mặt phố",
            "Shophouse, nhà phố thương mại",
            "Đất nền dự án",
            "Bán đất",
            "Condotel",
            "Kho, nhà xưởng",
            "Bất động sản khác"
        ],
        "nha-dat-cho-thue": [
            "Chung cư mini, căn hộ dịch vụ",
            "Nhà riêng",
            "Nhà biệt thự, liền kề",
            "Nhà mặt phố",
            "Nhà trọ, phòng trọ",
            "Shophouse, nhà phố thương mại",
            "Văn phòng",
            "Cửa hàng, ki ốt",
            "Kho, nhà xưởng, đất",
            "Bất động sản khác"
        ]
    }
    DATA_PATH = os.path.join(ROOT_FOLDER, "data")