# NATS Client (Phase-4 Foundation)

`merle_core.nats` ist die **leichte Client-Abstraktion** für Publish/Subscribe, Request/Reply und JetStream-Pull-Consumer. Es ist **kein** vollständiger Orchestrator und **kein** produktiver Scheduler.

Roadmap und Architektur: [docs/ROADMAP.md](../ROADMAP.md), [ADR-0006](../decisions/0006-nats-orchestration-foundation.md).  
Gotchas: [KB merle-core](../knowledge-base/modules/merle-core/gotchas.md) (`@tag:nats`).

## Extra installieren

```bash
uv add "merle-core[nats]"
# zieht: nats-py
```

Ohne Extra: `ImportError` mit Hinweis auf `merle-core[nats]` beim Connect.

## Scope (was es ist / was es nicht ist)

| Ist                                                   | Ist nicht                                     |
| ----------------------------------------------------- | --------------------------------------------- |
| `NatsClient` mit connect, publish, subscribe, request | Zentraler Orchestrator / Worker-Runtime       |
| JetStream-Hilfen (`PullConsumer`, TaskSpec-Streaming) | Resource-aware Scheduling, Prioritäten-Engine |
| Foundation für Phase-4-Orchestrierung                 | Ersatz für Bot-lokale `BaseTask`-Ausführung   |

Produktive Bots **müssen** heute nicht von NATS abhängen. Referenz: `examples/nats-task-communication/`.

## Minimalbeispiel

```python
from merle_core.nats import NatsClient


async def demo() -> None:
    async with NatsClient("nats://localhost:4222") as client:
        await client.publish("tasks.web", {"url": "https://example.com"})
        result = await client.request("tasks.process", {"id": 1}, timeout=30)
```

Lokaler Broker (Entwicklung):

```bash
docker run --rm -p 4222:4222 nats:latest
```

## Task-Modell

`TaskSpec` / `TaskResult` (aus `merle_core.task`) sind für künftige NATS-Verteilung ausgelegt und werden vom NATS-Modul re-exportiert. Die eigentliche Orchestrierung (Routing, Retries über Workers, Dead-Letter) bleibt Roadmap.

## Verwandte Docs

- [merle-core Index](index.md)
- [ROADMAP — Orchestration Foundation](../ROADMAP.md)
- [ADR-0006 NATS Orchestration Foundation](../decisions/0006-nats-orchestration-foundation.md)
