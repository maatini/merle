"""
Beispiel: UiPath-Hybrid Bot (Python + Orchestrator Queue).

Zeigt wie man Queue-Items aus UiPath verarbeitet und Ergebnisse zurückschreibt.
"""

import asyncio

from loguru import logger

from merle_core import BaseTask
from merle_core.observability import configure_observability


class ProcessUiPathQueueTask(BaseTask):
    async def execute(self) -> dict:
        self.logger.info("Hole Queue Items aus UiPath Orchestrator...")

        # Hier würde der echte UiPath Queue Client stehen
        # (siehe merle_core.uipath in Zukunft)

        processed = 5

        self.logger.info("{} Queue Items erfolgreich verarbeitet", processed)
        return {"status": "success", "processed_items": processed}


async def main():
    configure_observability(service_name="uipath-hybrid-example")

    task = ProcessUiPathQueueTask(settings=type("Settings", (), {"bot_name": "uipath_demo"})())
    result = await task.run()

    logger.info("Hybrid-Bot Ergebnis: {}", result)


if __name__ == "__main__":
    asyncio.run(main())
