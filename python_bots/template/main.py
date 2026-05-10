"""
RPA Bot Template — Einstiegspunkt.

Dieses Template dient als Ausgangspunkt für jeden neuen Python-Bot.
Es implementiert die verbindlichen Standards:
- loguru für strukturiertes Logging
- tenacity für Retry-Mechanismen
- pydantic-settings für Konfiguration
- Async-first Architektur
"""

import asyncio
import sys
from loguru import logger
from config import BotSettings
from tasks.example_task import ExampleTask


def setup_logging(settings: BotSettings) -> None:
    """Konfiguriere loguru mit den Settings."""
    logger.remove()  # Default-Handler entfernen
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    if settings.log_json:
        logger.add(
            "logs/bot_{time:YYYY-MM-DD}.json",
            level=settings.log_level,
            format="{time} {level} {message} {extra}",
            serialize=True,
            rotation="10 MB",
            retention="30 days",
        )


async def main() -> None:
    """Haupt-Workflow des Bots."""
    settings = BotSettings()  # type: ignore[call-arg]
    setup_logging(settings)

    logger.info("Bot {} wird gestartet", settings.bot_name)
    logger.info("Umgebung: {}", settings.environment)

    try:
        # --- Bot-Logik hier ---
        task = ExampleTask(settings)
        result = await task.run()
        logger.info("Task abgeschlossen: {}", result)

    except Exception as e:
        logger.exception("Kritischer Fehler im Bot: {}", e)
        raise


if __name__ == "__main__":
    asyncio.run(main())
