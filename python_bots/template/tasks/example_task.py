"""
Beispiel-Task — zeigt die Struktur für Geschäftslogik-Module.

Jede Task ist eine eigenständige Klasse mit:
- Konfiguration via Constructor Injection
- Async run()-Methode als Entry Point
- Strukturiertem Logging
- Retry-Mechanismen für externe Aufrufe
"""

from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
import httpx


class ExampleTask:
    """Beispiel-Task, die eine externe API aufruft."""

    def __init__(self, settings):
        self.settings = settings
        self.logger = logger.bind(task="ExampleTask")

    async def run(self) -> dict:
        """Hauptmethode der Task."""
        self.logger.info("Starte ExampleTask")

        # Schritt 1: Daten abrufen
        data = await self._fetch_data()

        # Schritt 2: Daten verarbeiten
        processed = self._process(data)

        self.logger.info("ExampleTask abgeschlossen, {} Einträge verarbeitet", len(processed))
        return {"status": "ok", "items_processed": len(processed)}

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    async def _fetch_data(self) -> list[dict]:
        """Daten von externer API abrufen — mit Retry."""
        self.logger.debug("Rufe API auf: {}", self.settings.target_url)

        async with httpx.AsyncClient(timeout=self.settings.request_timeout) as client:
            response = await client.get(
                self.settings.target_url,
                headers={"Authorization": f"Bearer {self.settings.api_key}"},
            )
            response.raise_for_status()
            return response.json()

    def _process(self, data: list[dict]) -> list[dict]:
        """Daten verarbeiten (Business-Logik)."""
        # Beispiel: Filtere aktive Einträge
        return [item for item in data if item.get("active", False)]
