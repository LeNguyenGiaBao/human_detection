from datetime import datetime


def gen_filename():
    now = datetime.now()
    filename = now.strftime("%Y%m%d_%H%M%S") + ".jpg"
    return filename
