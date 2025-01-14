import os

from src.entities import RealEstate
from src.base.repositories import BaseRepo
from src.common.consts import CommonConsts

class RealEstateRepo(BaseRepo[RealEstate]):
    entity = RealEstate
    db_path = CommonConsts.DATA_PATH + '/real_estate.db'

    @classmethod
    def initialize_db(cls):
        os.makedirs(CommonConsts.DATA_PATH, exist_ok=True)
        """Create the real estate table if it doesn't exist"""
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {cls.entity.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status TEXT NOT NULL,
                    type TEXT NOT NULL,
                    name TEXT NOT NULL,
                    location TEXT NOT NULL,
                    price REAL NOT NULL,
                    area REAL NOT NULL,
                    description TEXT,
                    link TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()