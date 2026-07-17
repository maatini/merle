# @Tag Registry

Jeder Tag markiert ein wiederkehrendes Konzept, das modulübergreifend auftaucht. Agenten können diese Tags scannen, um schnell Muster zu erkennen.

| Tag                      | Bedeutung                                                                                                                                             |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `@tag:python-first`      | Python ist der Default für alle Automatisierungen. UiPath nur bei nachgewiesenem Vorteil (ADR-0001).                                                  |
| `@tag:copier-template`   | Jeder neue Bot entsteht ausschließlich via Copier-Template `templates/bot/`. Kein manuelles Scaffolding (ADR-0004).                                   |
| `@tag:basebot`           | `BaseBot` aus `merle_core` ist die Standard-Basisklasse für grobgranulare Bot-Orchestrierung. Bietet `run()`-Lifecycle, Hooks, Health-Check.          |
| `@tag:basetask`          | `BaseTask` aus `merle_core` ist die Standard-Basisklasse für feingranulare Arbeitseinheiten. Gleicher Lifecycle wie BaseBot, aber für einzelne Tasks. |
| `@tag:governance`        | Die 11 Governance-Regeln aus `docs/concepts/governance.md` sind für jeden Bot verbindlich.                                                            |
| `@tag:devbox`            | Devbox + direnv ist die **verbindliche** Entwicklungsumgebung. Alle Tools (Python, uv, Copier) werden über Devbox bereitgestellt.                     |
| `@tag:monorepo`          | Merle ist ein uv-Workspace-Monorepo. Pakete werden relativ via `[tool.uv.sources]` aufgelöst.                                                         |
| `@tag:optional-imports`  | Viele merle-core-Module haben optionale Extras. Fehlende Imports werden via `try/except ImportError` abgefangen — das Paket funktioniert auch ohne.   |
| `@tag:retry`             | Alle externen Aufrufe (HTTP, Browser, DB) müssen mit `@with_retry` oder `tenacity`-Policy geschützt werden (Governance-Regel 5).                      |
| `@tag:observability`     | OpenTelemetry-basiertes Tracing + Metrics + loguru-Kontext-Injection. Opt-in via `configure_observability()`.                                         |
| `@tag:nats`              | NATS + JetStream ist die geplante Kommunikations- und Orchestrierungsschicht (Phase 4, ADR-0006). Derzeit PoC-Status.                                 |
| `@tag:lightpanda`        | Lightpanda ist eine optionale, CDP-kompatible Zig-Browser-Engine. 10-16× weniger RAM als Chromium, aber kein Screenshot/PDF-Support (ADR-0007).       |
| `@tag:playwright`        | Playwright ist die primäre Browser-Automatisierungs-Engine. Wird via `rpaframework` oder direkt genutzt.                                              |
| `@tag:pydantic-settings` | Alle Konfiguration erfolgt via `pydantic-settings.BaseSettings` mit `.env`-Datei. Keine hartcodierten Werte (Governance-Regel 3).                     |
| `@tag:loguru`            | `loguru` ist das verbindliche Logging-Framework. `setup_logging()` aus `merle_core` konfiguriert stderr + optionale JSON-Datei.                       |
| `@tag:secrets`           | Secrets werden via `SecretProvider`-Abstraktion geladen. Primär: Azure Key Vault. Fallback: `.env`.                                                   |
| `@tag:uipath-hybrid`     | Python↔UiPath-Integration erfolgt lose gekoppelt (NATS, Orchestrator-API, Dateien). Kein synchrones Ping-Pong (ADR-0003).                            |
| `@tag:docker`            | Jeder Bot muss in einem Linux-Container lauffähig sein. Das Template generiert ein Multi-Stage-Dockerfile (Governance-Regel 7).                       |
| `@tag:ruff`              | Ruff ist der einzige Linter + Formatter. Ersetzt flake8, isort, pyupgrade, black.                                                                     |
| `@tag:task-spec`         | `TaskSpec` / `TaskResult` sind die serialisierbaren Datenmodelle für Task-Kommunikation (NATS, Queues).                                               |

## Verwendung

- In responsibility.md: "Dieses Modul ist verantwortlich für @tag:basebot — den zentralen Bot-Lifecycle."
- In gotchas.md: "Beachte @tag:optional-imports — fehlende Extras werden nicht als Fehler geworfen."
- Agenten-Kontext: "Ändere ich @tag:basebot? Dann muss ich auch @tag:copier-template prüfen."
