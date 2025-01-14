import datetime
import pytz


class TimeUtils:
    @classmethod
    def get_current_vn_time(cls):
        utcnow = datetime.datetime.utcnow()
        return pytz.timezone('Asia/Ho_Chi_Minh').utcoffset(utcnow) + utcnow
