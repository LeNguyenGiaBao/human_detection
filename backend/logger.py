import logging
import os
import sys
from datetime import datetime

from constants import LOG_DIR

os.makedirs(LOG_DIR, exist_ok=True)
logger = logging.getLogger("backend_logger")
logger.setLevel(logging.DEBUG)

log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)

log_file = f"logs/backend_{datetime.now().strftime('%Y-%m-%d')}.log"
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(log_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
