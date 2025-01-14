import sqlite3
from typing import List, Dict, Any, TypeVar, Generic
from contextlib import contextmanager
from abc import ABC, abstractmethod

from src.common.consts import CommonConsts

T = TypeVar('T')

class BaseRepo(Generic[T], ABC):
    entity: T
    db_path: str

    @classmethod
    @contextmanager
    def get_connection(cls):
        conn = sqlite3.connect(cls.db_path)
        conn.row_factory = sqlite3.Row  
        try:
            yield conn
        finally:
            conn.close()

    @classmethod
    @abstractmethod
    def initialize_db(cls):
        pass

    @classmethod
    def insert(cls, entity: T) -> int:
        data = entity.to_dict()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())
        
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            query = f'INSERT INTO {cls.entity.table_name} ({columns}) VALUES ({placeholders})'
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid
        
    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {cls.entity.table_name}')
            return [dict(row) for row in cursor.fetchall()]