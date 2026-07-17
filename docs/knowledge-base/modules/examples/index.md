# Examples & Integration Patterns

Referenz-Implementierungen und Integrationsmuster für Merle-Bots.

## Beispiel-Bots (`examples/`)

| Beispiel                    | Zweck                                                       | merle-core-Features                                                                |
| --------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **invoice-processing**      | 🥇 **Gold Standard.** Vollständige Pipeline: IMAP→PDF→Excel | BaseBot, BaseTask, @with_retry, OTEL, self-healing, simulate-mode, ExcelWriter     |
| **web-automation**          | Playwright-Browser-Steuerung mit Stealth-Mode               | launch_robust_browser, RobustBrowser, BaseTask, @with_retry, Screenshot-on-Failure |
| **excel-processing**        | Strukturierte Excel-Datenverarbeitung                       | BaseTask, pandas, openpyxl                                                         |
| **uipath-hybrid**           | Python + UiPath Orchestrator Queue (Platzhalter)            | BaseTask (geplant: merle_core.uipath)                                              |
| **nats-task-communication** | @tag:nats Task-Kommunikation zwischen Bots (PoC)            | NatsClient, TaskSpec, TaskResult, Pub/Sub                                          |

## Integration Patterns (`integration_examples/`)

| Pattern                    | Zweck                                    | Technologie                       |
| -------------------------- | ---------------------------------------- | --------------------------------- |
| **orchestrator_api**       | Python ruft UiPath Orchestrator REST API | httpx + OAuth2 Client Credentials |
| **file_based_integration** | Datenaustausch via JSON/CSV-Dateien      | Datei-System, JSON, CSV           |
| **python_scope**           | UiPath Workflow ruft Python auf          | UiPath Python Scope Activity      |

## Links

- **[`responsibility.md`](./responsibility.md)** — Was jedes Beispiel demonstriert, welche Patterns es zeigt
- **[`gotchas.md`](./gotchas.md)** — Simulierte Daten, NATS-Docker-Requirement, Platzhalter-Code
