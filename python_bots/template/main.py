"""
RPA Bot Template — Einstiegspunkt.

Dieses Template ist die **verbindliche Basis** für jeden neuen Python-Bot im Merle-Framework.

Standards (Phase 0+):
- merle-core für wiederverwendbare Basisklassen, HTTP-Client und Logging
- pydantic-settings für typsichere Konfiguration
- loguru + tenacity + httpx (via merle-core)
- Async-first + strukturierte Fehlerbehandlung

Verwendung von BaseBot (empfohlen in realen Bots):
    from merle_core import BaseBot
    class MeinBot(BaseBot):
        async def execute(self) -> dict:
            ...
"""

import asyncio

from loguru import logger

from config import BotSettings
from merle_core import setup_logging
from tasks.example_task import ExampleTask


async def main() -> None:
    """Haupt-Workflow des Bots."""
    settings = BotSettings()  # type: ignore[call-arg]

    # Logging jetzt zentral aus merle-core (konsistent über alle Bots)
    setup_logging(level=settings.log_level, json_format=settings.log_json)

    logger.info("Bot {} wird gestartet", settings.bot_name)
    logger.info("Umgebung: {}", settings.environment)

    try:
        # --- Bot-Logik hier ---
        # In produktiven Bots: von BaseBot erben und .run() nutzen
        task = ExampleTask(settings)
        result = await task.run()
        logger.info("Task abgeschlossen: {}", result)

    except Exception as e:
        logger.exception("Kritischer Fehler im Bot: {}", e)
        raise


if __name__ == "__main__":
    asyncio.run(main())
