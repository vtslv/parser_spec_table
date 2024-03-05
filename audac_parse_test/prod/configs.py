import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# from constants import BASE_DIR
BASE_DIR = Path(__file__).parent

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'


def configure_logging():
    """Конфигурация логирования."""
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'parser.log'
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5, encoding='utf-8',
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        encoding='utf-8',
        handlers=(rotating_handler, logging.StreamHandler())
    )
