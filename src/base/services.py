import json
import os
import pandas as pd
from typing import Dict, Any, List
from abc import ABC, abstractmethod

from src.base.repositories import BaseRepo
from src.common.consts import CommonConsts
from src.utils.logger import LOGGER

class BaseService(ABC):
    repo: BaseRepo

    @classmethod
    @abstractmethod
    def crawl(cls) -> None:
        pass

    @classmethod
    @abstractmethod
    def extract(cls) -> pd.DataFrame:
        pass

    @classmethod
    @abstractmethod
    def transform(cls, raw_data: pd.DataFrame) -> pd.DataFrame:
        pass

    @classmethod
    @abstractmethod
    def analyze_visualize(cls, tf_data: pd.DataFrame) -> None:
        pass

    @classmethod
    @abstractmethod
    def run_pipeline(cls) -> None:
        pass

    @classmethod
    def load_process(cls) -> Dict[str, Any]:
        try:
            os.makedirs(CommonConsts.TEMP_PATH, exist_ok=True)
            with open(f'{CommonConsts.TEMP_PATH}/process_tracking.json', 'r') as f:
                process = json.load(f)
            LOGGER.info(f"Loaded process tracking: {process}")
            return process
        except FileNotFoundError:
            return {"sell": {}, "rent": {}}

    @classmethod
    def save_process(cls, process: Dict[str, Any]) -> None:
        with open(f'{CommonConsts.TEMP_PATH}/process_tracking.json', 'w') as f:
            json.dump(process, f)


    '''
    Example of :
    {
        "sell": { # status
            "362": 15, # re_type_id: page
            "363": 25,
            },
        "rent": {
            "362": 15,
            "625": 25,
        }
    }
    '''
    