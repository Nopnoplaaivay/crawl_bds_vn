from typing import Dict, Union

class RealEstate:
    table_name = "real_estate"

    def __init__(self, status, type, title, location, price, area, desc, url):
        self.status = status
        self.type = type
        self.title = title
        self.location = location
        self.price = price
        self.area = area
        self.desc = desc
        self.url = url

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {
            "status": self.status,
            "type": self.type,
            "title": self.title,
            "location": self.location,
            "price": self.price,
            "area": self.area,
            "desc": self.desc,
            "url": self.url
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Union[str, int]]) -> "RealEstate":
        return RealEstate(
            status=data["status"],
            type=data["type"],
            title=data["title"],
            location=data["location"],
            price=data["price"],
            area=data["area"],
            desc=data["desc"],
            url=data["url"]
        )