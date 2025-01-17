import os

from src.modules.entities import RealEstate
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
                    title TEXT,
                    location TEXT, 
                    price REAL,
                    area REAL,
                    desc TEXT,
                    url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()