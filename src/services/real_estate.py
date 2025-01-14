from typing import Dict, Union

import numpy
import pandas as pd

from src.common.consts import CommonConsts
from src.entities.real_estate import RealEstate
from src.repositories import RealEstateRepo


class RealEstateService:
    repo = RealEstateRepo

    @classmethod
    def crawl_real_estate(cls):
        cls.repo.initialize_db()
        link_all = [
            f"{CommonConsts.BASE_URL}/{elem}" for elem in CommonConsts.REAL_ESTATE_TYPES
        ]
        print(link_all)
