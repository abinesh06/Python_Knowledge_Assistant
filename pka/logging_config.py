"""
Central logging configuration for the pka package.

Call setup_logging() ONCE, when the app starts (from main.py).
Every other module just does `logger = logging.getLogger(__name__)`
and automatically inherits whatever config was set up here.
"""

import logging
import sys
from pathlib import Path
import json

LOG_DIR = Path("data/logs")
LOG_FILE = LOG_DIR / "pka.log"


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_data)


def setup_logging(level: str = "INFO") -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    console_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_formatter = JSONFormatter()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(file_formatter)

    root_logger = logging.getLogger("pka")
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)