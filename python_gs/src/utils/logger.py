import logging
import os
from pathlib import Path

_LOG_FILE = Path(__file__).parent.parent.parent / "logs" / "agrosat.log"


def setup_logger(name: str = "agrosat") -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    _LOG_FILE.parent.mkdir(exist_ok=True)

    file_handler = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger() -> logging.Logger:
    return logging.getLogger("agrosat")
