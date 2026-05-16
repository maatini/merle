"""
merle_core.nats

Leichte, RPA-freundliche Abstraktion über NATS.

Ziel von Phase 4 (A1):
- Einfache Publish/Subscribe
- Request/Reply Pattern (sehr nützlich für Tasks)
- Gute Integration mit bestehendem Retry-System
- Vorbereitung für spätere JetStream-Nutzung

Verwendung:
    from merle_core.nats import NatsClient

    async with NatsClient("nats://localhost:4222") as client:
        await client.publish("tasks.web", {"url": "..."})
        result = await client.request("tasks.process", payload, timeout=30)
"""

from .client import NatsClient, NatsMessage, PullConsumer

__all__ = ["NatsClient", "NatsMessage", "PullConsumer"]

# Re-export für bequeme Nutzung
from ..task import TaskSpec, TaskResult