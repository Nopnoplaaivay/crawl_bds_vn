from typing import Dict, Union

class RealEstate:
    table_name = "real_estate"

    def __init__(self, id, status, type, name, location, price, area, desc, url):
        self.id = id
        self.status = status
        self.type = type
        self.name = name
        self.location = location
        self.price = price
        self.area = area
        self.desc = desc
        self.url = url

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {
            "id": self.id,
            "status": self.status,
            "type": self.type,
            "name": self.name,
            "location": self.location,
            "price": self.price,
            "area": self.area,
            "desc": self.desc,
            "url": self.url
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Union[str, int]]) -> "RealEstate":
        return RealEstate(
            id=data["id"],
            status=data["status"],
            type=data["type"],
            name=data["name"],
            location=data["location"],
            price=data["price"],
            area=data["area"],
            desc=data["desc"],
            url=data["url"]
        )