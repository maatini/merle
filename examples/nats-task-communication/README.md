# NATS Task Communication Example (Phase 4 - A1)

Dieses Beispiel zeigt die grundlegende, entkoppelte Kommunikation zwischen Tasks über NATS.

## Was wird demonstriert?

- Verwendung von `TaskSpec` und `TaskResult`
- Publish/Subscribe Pattern via `merle_core.nats`
- Trennung von Producer (WebScraper) und Consumer (DataProcessor)

## Voraussetzung

Du brauchst eine laufende NATS-Instanz:

```bash
docker run -p 4222:4222 nats:latest
```

## Starten

```bash
cd examples/nats-task-communication
uv sync
uv run python main.py
```

## Nächste Schritte (spätere Phasen)

- JetStream für persistente Tasks
- Request/Reply für synchrone Task-Ausführung
- Echter Orchestrator, der Tasks routed
- Task State Management über NATS KV

Dieses Beispiel ist bewusst einfach gehalten, um das Grundprinzip zu vermitteln.
