# NATS Task Communication — Merle Gold Example

Shows decoupled task communication over NATS using Merle's `TaskSpec` /
`TaskResult` model and `NatsClient`.

## What This Example Shows

| Pattern                   | Implementation                            | Why It Matters                 |
| ------------------------- | ----------------------------------------- | ------------------------------ |
| **TaskSpec / TaskResult** | `build_scrape_spec`, `handle_scrape_spec` | JSON-safe NATS payloads        |
| **Publish / Subscribe**   | `NatsClient.publish` + `subscribe`        | Fire-and-forget task routing   |
| **Pure processor logic**  | `tasks/processor.py`                      | Unit-testable without a broker |
| **Configuration**         | `NatsExampleSettings`                     | Env-driven NATS URL / subject  |

## Architecture

```
WebScraper (producer)  --publish TaskSpec-->  NATS subject
DataProcessor (consumer) <--subscribe---------  NATS subject
                         --reply TaskResult-->  (optional inbox)
```

## Unit Tests (no NATS server)

```bash
cd examples/nats-task-communication
uv sync --group dev
uv run pytest tests/ -q
```

These cover TaskSpec/TaskResult roundtrips and a mocked `NatsClient`.

## Live Demo (needs NATS)

```bash
# Terminal 1 — start NATS
docker run --rm -p 4222:4222 nats:latest

# Terminal 2 — run example
cd examples/nats-task-communication
uv sync
export NATS_URL=nats://localhost:4222
uv run python main.py
```

Without a reachable server, `main.py` exits with a clear error message.

## Key Files

- `main.py` — Live producer + consumer over NATS
- `config.py` — `NatsExampleSettings`
- `tasks/scraper.py` — TaskSpec builder
- `tasks/processor.py` — Pure TaskSpec → TaskResult
- `tests/` — Mocked unit tests (CI-safe)

## Next Steps (later phases)

- JetStream durable consumers
- Request/Reply for synchronous tasks
- Orchestrator routing + KV state
