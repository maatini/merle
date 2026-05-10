"""
Gemeinsame Basisklasse für alle RPA-Bots.

Bietet:
- Einheitliches Logging-Setup
- Konfigurations-Loading
- Health-Check-Methode
- Standard-Fehlerbehandlung
"""

from pathlib import Path
from loguru import logger
from abc import ABC, abstractmethod


class BaseBot(ABC):
    """Abstrakte Basisklasse für RPA-Bots."""

    def __init__(self, settings):
        self.settings = settings
        self.logger = logger.bind(bot=settings.bot_name)

    @abstractmethod
    async def execute(self) -> dict:
        """Hauptlogik des Bots — muss von Subklassen implementiert werden."""
        ...

    async def run(self) -> dict:
        """Standard-Run-Methode mit Pre/Post-Processing."""
        self.logger.info("Bot {} startet (env={})", self.settings.bot_name, self.settings.environment)
        try:
            result = await self.execute()
            self.logger.info("Bot erfolgreich beendet: {}", result)
            return result
        except Exception:
            self.logger.exception("Bot mit Fehler beendet")
            raise

    def health_check(self) -> dict:
        """Health-Check für Monitoring."""
        return {
            "status": "healthy",
            "bot": self.settings.bot_name,
            "environment": self.settings.environment,
        }
