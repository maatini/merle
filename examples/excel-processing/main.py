"""
Beispiel: Excel-Verarbeitung mit merle-core + pandas.

Zeigt saubere Task-Struktur für Datenverarbeitung.
"""

import asyncio

from loguru import logger

from merle_core import BaseTask
from merle_core.observability import configure_observability


class ProcessExcelTask(BaseTask):
    async def execute(self) -> dict:
        # Hier würde man echte Excel-Dateien verarbeiten
        self.logger.info("Verarbeite Excel-Datei...")

        # Platzhalter-Logik
        processed_rows = 1247

        return {"status": "success", "rows_processed": processed_rows, "file": "rechnungen_q2.xlsx"}


async def main():
    configure_observability(service_name="excel-processing-example")

    task = ProcessExcelTask(settings=type("Settings", (), {"bot_name": "excel_demo"})())
    result = await task.run()

    logger.info("Excel-Verarbeitung abgeschlossen: {}", result)


if __name__ == "__main__":
    asyncio.run(main())
