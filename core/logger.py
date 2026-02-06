import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "auth.log"

logger = logging.getLogger("auth_logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s | %(message)s"
)

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=5,
    encoding="utf-8",
)

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
