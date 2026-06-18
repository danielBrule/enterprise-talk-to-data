import logging
import os
import sys

DEFAULT_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DEFAULT_LOG_DATETIME_FORMAT = "%Y%m%d-%H%M%S"

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

formatter = logging.Formatter(fmt=DEFAULT_LOG_FORMAT, datefmt=DEFAULT_LOG_DATETIME_FORMAT)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger("newspaper_talk_to_data")
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)
logger.propagate = False
