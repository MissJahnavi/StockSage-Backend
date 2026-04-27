import sys
from loguru import logger


def setup_logging():
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")
    logger.add("logs/app.log", rotation="10 MB", retention="7 days", level="DEBUG")
