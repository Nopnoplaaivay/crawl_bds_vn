from typing import Dict, Union

class RealEstate:
    def __init__(self, id, status, name, location, price, area, desc, link):
        self.id = id
        self.status = status
        self.name = name
        self.location = location
        self.price = price
        self.area = area
        self.desc = desc
        self.link = link

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {
            "id": self.id,
            "status": self.status,
            "name": self.name,
            "location": self.location,
            "price": self.price,
            "area": self.area,
            "desc": self.desc,
            "link": self.link
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Union[str, int]]) -> "RealEstate":
        return RealEstate(
            id=data["id"],
            status=data["status"],
            name=data["name"],
            location=data["location"],
            price=data["price"],
            area=data["area"],
            desc=data["desc"],
            link=data["link"]
        )