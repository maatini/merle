"""
Vorkonfigurierte Logging-Setup-Funktion.

Kann von Bots importiert werden, die kein eigenes Logging-Setup benötigen.
"""

import sys

from loguru import logger


def setup_logging(level: str = "INFO", json_format: bool = False) -> None:
    """Standard-Logging-Konfiguration."""
    logger.remove()
    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    if json_format:
        logger.add(
            "logs/bot_{time:YYYY-MM-DD}.json",
            level=level,
            format="{time} {level} {message} {extra}",
            serialize=True,
            rotation="10 MB",
            retention="30 days",
        )
