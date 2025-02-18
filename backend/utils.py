from datetime import datetime, timedelta


def gen_filename():
    now = datetime.now()
    filename = now.strftime("%Y%m%d_%H%M%S") + ".jpg"
    return filename


def utc_to_utc_plus_7(utc_time: datetime) -> datetime:
    return utc_time + timedelta(hours=7)
