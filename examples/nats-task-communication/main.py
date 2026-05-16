"""
Beispiel: Einfache NATS-basierte Task-Kommunikation (Phase 4 - A1)

Szenario:
- Ein "WebScraper" Task sammelt Daten und veröffentlicht sie via NATS.
- Ein "DataProcessor" Task abonniert die Daten und verarbeitet sie.

Dies zeigt das grundlegende Fire-and-Forget + Request/Reply Pattern.
"""

import asyncio
import uuid

from loguru import logger

from merle_core import TaskResult, TaskSpec
from merle_core.nats import NatsClient


async def run_web_scraper(client: NatsClient):
    """Simuliert einen Web-Scraper, der Ergebnisse per NATS veröffentlicht."""
    task_spec = TaskSpec(
        task_id=str(uuid.uuid4()),
        task_type="web_scrape",
        payload={"url": "https://example.com", "selectors": [".title", ".price"]},
        metadata={"source": "web-scraper-bot"},
    )

    logger.info("WebScraper: Sende Task {}", task_spec.task_id)
    await client.publish("tasks.web_scrape", task_spec.to_dict())


async def run_data_processor(client: NatsClient):
    """Verarbeitet eingehende Web-Daten via NATS."""

    async def handle_message(msg):
        spec = TaskSpec.from_dict(msg.data)
        logger.info("DataProcessor: Verarbeite Task {} vom Typ {}", spec.task_id, spec.task_type)

        # Simuliere Verarbeitung
        await asyncio.sleep(0.5)

        result = TaskResult.success(
            task_id=spec.task_id, result={"processed": True, "records": 12}, processor="data-processor-bot"
        )

        logger.info("DataProcessor: Task {} fertig", spec.task_id)
        if msg.reply:
            await client.reply(msg.reply, result.to_dict())

    await client.subscribe("tasks.web_scrape", handle_message)
    logger.info("DataProcessor läuft und wartet auf Tasks...")


async def main():
    # In der Realität würde hier eine echte NATS-Instanz laufen
    # Für das Beispiel nutzen wir localhost (muss gestartet sein)
    nats_url = "nats://localhost:4222"

    try:
        async with NatsClient(nats_url, name="phase4-demo") as client:
            # Starte beide Rollen parallel (in der Praxis wären das separate Prozesse)
            await asyncio.gather(
                run_web_scraper(client),
                run_data_processor(client),
            )
    except Exception as e:
        logger.error("NATS Demo fehlgeschlagen (läuft NATS auf localhost:4222?): {}", e)


if __name__ == "__main__":
    asyncio.run(main())
