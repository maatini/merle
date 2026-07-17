# merle-core — Gemeinsame RPA-Kernbibliothek

**Paket:** `packages/merle-core/` | **Import:** `from merle_core import ...` | **Version:** 0.4.0

`merle-core` ist die zentrale, von **allen Bots importierte** Bibliothek. Sie stellt den @tag:basebot / @tag:basetask Lifecycle, @tag:retry Policies, @tag:observability, @tag:playwright, @tag:secrets, @tag:nats, Datenverarbeitung und @tag:uipath-hybrid Integration bereit.

**Kernprinzip:** @tag:optional-imports — alle Extras sind optional und werden via `try/except ImportError` geladen. Das Paket funktioniert ohne Playwright, OpenTelemetry, NATS etc.

## Dateiübersicht

| Datei               | Zweck                                                | Schlüssel-Exports                                                                  |
| ------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `__init__.py`       | Zentrale Public-API. Re-exportiert **alles**.        | Alles unten Genannte                                                               |
| `base_bot.py`       | @tag:basebot — grobgranularer Bot-Lifecycle          | `BaseBot`                                                                          |
| `base_task.py`      | @tag:basetask — feingranulare Arbeitseinheit         | `BaseTask`                                                                         |
| `task.py`           | Serialisierbare Task-Datenmodelle (@tag:task-spec)   | `TaskSpec`, `TaskResult`, `TaskStatus`, `TaskError`                                |
| `exceptions.py`     | Exception-Hierarchie (1 Base + 14 Spezialisierungen) | `MerleError`, `RetryExhaustedError`, `PlaywrightError`, etc.                       |
| `retry.py`          | @tag:retry Policies + Decorator                      | `with_retry`, `default_http_retry`, `browser_retry`, etc.                          |
| `http_client.py`    | HTTP-Client mit Retry                                | `RpaHttpClient`                                                                    |
| `logging_config.py` | @tag:loguru Setup                                    | `setup_logging`                                                                    |
| `observability/`    | @tag:observability (OTEL Tracing + Metrics)          | `configure_observability`, `get_tracer`, `get_meter`                               |
| `playwright/`       | @tag:playwright (Chromium + @tag:lightpanda)         | `launch_robust_browser`, `RobustBrowser`, `robust_goto`, `safe_click`, `safe_fill` |
| `secrets/`          | @tag:secrets (Azure Key Vault)                       | `SecretProvider`, `AzureKeyVaultProvider`, `AzureKeyVaultSettings`                 |
| `nats/`             | @tag:nats Messaging-Client                           | `NatsClient`, `PullConsumer`, `NatsMessage`                                        |
| `data/`             | Excel/PDF/Email-Verarbeitung                         | `ExcelReader`, `ExcelWriter`, `PdfExtractor`, `EmailClient`                        |
| `uipath/`           | @tag:uipath-hybrid Orchestrator-Client               | `UiPathOrchestratorClient`, `UiPathQueueHelper`                                    |

## Installation

```bash
# Minimal (BaseBot + BaseTask + Retry + Logging):
uv add merle-core

# Mit Browser-Automatisierung:
uv add "merle-core[playwright]"
uv add "merle-core[lightpanda]"

# Mit Observability:
uv add "merle-core[observability]"

# Mit Datenverarbeitung:
uv add "merle-core[data]"

# Mit Secrets:
uv add "merle-core[azure]"

# Mit NATS:
uv add "merle-core[nats]"

# Alles:
uv add "merle-core[playwright,lightpanda,observability,data,azure,nats]"
```

## Schnell-Referenz: Welches File für welches Problem?

- **"Ich will einen neuen Bot schreiben"** → [`responsibility.md`](./responsibility.md) (BaseBot + BaseTask Pattern)
- **"Ich brauche Retry-Logik"** → [`responsibility.md`](./responsibility.md) (Retry-Sektion) + [`interfaces.md`](./interfaces.md)
- **"Ich will Playwright nutzen"** → [`responsibility.md`](./responsibility.md) (Playwright-Sektion)
- **"Ich muss Secrets aus Key Vault laden"** → [`responsibility.md`](./responsibility.md) (Secrets-Sektion)
- **"Ich muss eine Abhängigkeit hinzufügen"** → [`dependencies.md`](./dependencies.md)
- **"Warum funktioniert X nicht ohne Y?"** → [`gotchas.md`](./gotchas.md)
