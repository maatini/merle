#!/usr/bin/env python3
"""
Merle NATS Task Communication — Gold Reference Example

Demonstrates:
- TaskSpec / TaskResult serialisation for NATS transport
- Publish + subscribe via merle_core.nats.NatsClient
- Separation of producer (scraper) and consumer (processor)

**Live NATS required for main.py.** Unit tests mock the client (no server).
"""

from __future__ import annotations

import asyncio

from loguru import logger

from config import settings
from merle_core import TaskSpec
from merle_core.nats import NatsClient, NatsMessage
from tasks import build_scrape_spec, handle_scrape_spec


async def run_web_scraper(client: NatsClient, subject: str) -> TaskSpec:
    """Publish a scrape TaskSpec onto NATS."""
    task_spec = build_scrape_spec("https://example.com")
    logger.info("WebScraper: publishing task {}", task_spec.task_id)
    await client.publish(subject, task_spec.to_dict())
    return task_spec


async def run_data_processor(client: NatsClient, subject: str) -> None:
    """Subscribe and process incoming scrape tasks."""

    async def handle_message(msg: NatsMessage) -> None:
        spec = TaskSpec.from_dict(msg.data)
        logger.info(
            "DataProcessor: handling task {} type={}",
            spec.task_id,
            spec.task_type,
        )
        result = handle_scrape_spec(spec)
        logger.info("DataProcessor: done task {}", spec.task_id)
        if msg.reply:
            await client.reply(msg.reply, result.to_dict())

    await client.subscribe(subject, handle_message)
    logger.info("DataProcessor subscribed to {}", subject)


async def main() -> None:
    nats_url = settings.nats_url
    subject = settings.subject

    logger.info(
        "NATS demo starting (url={}, subject={}). Live server required.",
        nats_url,
        subject,
    )

    try:
        async with NatsClient(nats_url, name=settings.nats_name) as client:
            # Subscribe first so we do not miss the publish
            await run_data_processor(client, subject)
            await asyncio.sleep(0.2)
            await run_web_scraper(client, subject)
            # Allow handler to run
            await asyncio.sleep(1.0)
            logger.success("NATS demo finished (check logs above)")
    except Exception as e:
        logger.error(
            "NATS demo failed — is NATS running at {}? Start with: docker run -p 4222:4222 nats:latest  | error={}",
            nats_url,
            e,
        )
        raise SystemExit(1) from e


if __name__ == "__main__":
    asyncio.run(main())
