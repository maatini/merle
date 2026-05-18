# merle-core v0.2

**Core utilities, resilience patterns and observability for Merle RPA bots.**

`merle-core` ist das zentrale wiederverwendbare Framework für alle Python-First RPA-Bots im Merle-Ökosystem.

## Komponenten (v0.2)

### Kern

- **BaseBot** + **BaseTask** — Abstrakte Basisklassen mit Lifecycle, Timing, Metriken und Self-Healing-Hooks (`_on_success`, `_on_failure`)
- **RpaHttpClient** — Resilienter async HTTP-Client
- **retry** — Starke zentrale Policies + `@with_retry(policy=...)` Dekorator
- **exceptions** — Professionelle, unterscheidbare Exception-Hierarchie

### Observability (Extra: `observability`)

- `configure_observability(service_name=...)` — Einmal-Setup
- Automatisches Tracing in `BaseBot` / `BaseTask` (zukünftig)
- Loguru-Sink mit automatischer `trace_id` / `span_id` Anreicherung
- Standard-Metriken (`bot_executions_total`, `task_duration_seconds`, `errors_total` etc.)

### Weitere Module

- `playwright` (Extra `playwright`) – `launch_robust_browser()` mit Stealth, Auto-Screenshot, Proxy + **zwei Engines**:
  - `chromium` (Default)
  - `lightpanda` (Zig-basiert via CDP – 10–16× weniger RAM)
- `secrets` (Extra `azure`) – `AzureKeyVaultProvider` + `AzureKeyVaultSettings` für pydantic-settings
- `uipath` – Orchestrator Queue & Job Helpers
- `data` – Excel, PDF, E-Mail Utilities

## Installation

```bash
# Minimal
uv add merle-core

# Mit Playwright (Chromium)
uv add "merle-core[playwright,observability]"

# Mit Lightpanda (Zig-basiert, ressourcenschonend – empfohlen für hochvolumige Bots)
uv add "merle-core[lightpanda,observability]"
```

## Philosophie

- Leichter Core, optionale Extras
- Jeder Bot **muss** merle-core verwenden (Governance-Regel 10)
- Kein Bot implementiert selbst Retry, Logging oder Browser-Handling
- Automatische Observability (Metrics + Traces) ohne zusätzlichen Code

## Installation (uv workspace)

From the repository root:

```bash
uv sync --group dev
```

Then in any bot:

```python
from merle_core import BaseBot, RpaHttpClient, setup_logging
```

## Development

```bash
cd python_bots/shared
uv run ruff check .
uv run mypy src/merle_core
```

## Versioning

Follows semantic versioning. This package is published internally and consumed by individual RPA bots via uv workspace or as a versioned dependency.
