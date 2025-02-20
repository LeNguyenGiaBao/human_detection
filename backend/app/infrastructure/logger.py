import logging
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("backend_logger")
logger.setLevel(logging.DEBUG)

log_file = f"logs/backend_{datetime.now().strftime('%Y-%m-%d')}.log"
file_handler = logging.FileHandler(log_file)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
