import json
import os
from typing import Dict, Any

from src.base.repositories import BaseRepo
from src.common.consts import CommonConsts
from src.utils.logger import LOGGER

class BaseService:
    repo: BaseRepo
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
    
    @classmethod
    def save_process(cls, process: Dict[str, Any]) -> None:
        with open(f'{CommonConsts.TEMP_PATH}/process_tracking.json', 'w') as f:
            json.dump(process, f)