import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ==============================
# LOG DIRECTORY
# ==============================
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s | %(message)s"
)

# =====================================================
# AUTH LOGGER  (logs/auth.log)
# =====================================================
auth_log_file = LOG_DIR / "auth.log"

logger = logging.getLogger("auth_logger")
logger.setLevel(logging.INFO)

auth_file_handler = RotatingFileHandler(
    auth_log_file,
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)

auth_file_handler.setFormatter(formatter)
logger.addHandler(auth_file_handler)


# =====================================================
# BOOK LOGGER  (logs/book.log)
# =====================================================
book_log_file = LOG_DIR / "book.log"

book_logger = logging.getLogger("book_logger")
book_logger.setLevel(logging.INFO)

book_file_handler = RotatingFileHandler(
    book_log_file,
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)

book_file_handler.setFormatter(formatter)
book_logger.addHandler(book_file_handler)
