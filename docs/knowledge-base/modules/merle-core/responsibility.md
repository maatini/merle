# merle-core — Verantwortlichkeiten

Jedes Submodul von `merle-core` besitzt eine klar definierte Verantwortung. Diese Seite dokumentiert **was jedes Modul besitzt, welche Invarianten gelten und was die Entry Points sind**.

---

## 1. @tag:basebot — `base_bot.py`

**Import:** `from merle_core import BaseBot`

| Aspekt           | Details                                                                                                                                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owns**         | Grobgranularen Bot-Lifecycle: `run()` → `execute()` → Hooks → Health-Check                                                                                                                                |
| **Invarianten**  | `execute()` wird **nie** direkt aufgerufen — immer `run()`. `run()` misst Dauer, loggt Start/Ende, ruft `_on_success`/`_on_failure` auf. `health_check()` gibt immer `{"status": "healthy", ...}` zurück. |
| **Entry Points** | `BaseBot.__init__(settings, name)` → `await bot.run()` → `bot.health_check()`                                                                                                                             |
| **OTEL**         | Zeichnet `bot_executions_total`, `bot_duration_seconds`, `bot_success_total`, `bot_failure_total` auf — aber nur wenn @tag:observability aktiviert ist.                                                   |

**Pattern:** Jeder generierte Bot erbt von `BaseBot` und implementiert `execute()`:

```python
class MyBot(BaseBot):
    def __init__(self, settings):
        super().__init__(settings, name="my_bot")

    async def execute(self) -> dict:
        task = MyTask(self.settings)
        return await task.run()

    def _on_success(self, result):
        self.logger.info("✅ Fertig!")

    def _on_failure(self, exception):
        self.logger.error(f"❌ Fehler: {exception}")
```

---

## 2. @tag:basetask — `base_task.py`

**Import:** `from merle_core import BaseTask`

| Aspekt           | Details                                                                                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owns**         | Feingranularen Task-Lifecycle — identisch zu `BaseBot` aber für einzelne Arbeitseinheiten                                                                 |
| **Invarianten**  | Gleiches Pattern: `run()` wrappt `execute()`. `status` wechselt `"pending"` → `"running"` → `"success"`/`"failed"`. `duration` wird in Sekunden gemessen. |
| **Entry Points** | `BaseTask.__init__(settings, name)` → `await task.run()` → `task.health_check()`                                                                          |
| **OTEL**         | Analog zu BaseBot: `task_executions_total`, `task_duration_seconds`, etc.                                                                                 |

**Pattern:** Tasks werden in `execute()` implementiert, nicht in `run()`:

```python
class FetchDataTask(BaseTask):
    def __init__(self, settings):
        super().__init__(settings, name="FetchData")

    @with_retry(policy=default_http_retry)
    async def execute(self) -> dict:
        # Geschäftslogik hier
        return {"data": [...]}
```

---

## 3. @tag:task-spec — `task.py`

**Import:** `from merle_core import TaskSpec, TaskResult, TaskStatus, TaskError`

| Aspekt             | Details                                                                                                                                                                                                   |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owns**           | Serialisierbare Datenmodelle für Task-Kommunikation (NATS, Queues)                                                                                                                                        |
| **Invarianten**    | `TaskSpec` ist das "Was soll getan werden". `TaskResult` ist das "Was kam raus". `TaskStatus` ist ein Enum (`PENDING`, `RUNNING`, `SUCCESS`, `FAILED`, `RETRY`). `TaskError` kapselt Fehlerinformationen. |
| **Entry Points**   | `TaskSpec(task_id, type, payload, priority)` → `TaskResult.success(task_id, data)` / `TaskResult.failure(task_id, error)`                                                                                 |
| **Serialisierung** | `to_dict()` / `from_dict()` — für NATS Message Payloads                                                                                                                                                   |

---

## 4. Exception-Hierarchie — `exceptions.py`

**Import:** `from merle_core import MerleError, RetryExhaustedError, ...`

| Aspekt           | Details                                                                                            |
| ---------------- | -------------------------------------------------------------------------------------------------- |
| **Owns**         | 1 Basis-Exception + 14 spezialisierte Exceptions                                                   |
| **Invarianten**  | Alle erben von `MerleError`. Jede Exception hat einen `code` (str) und optionale `details` (dict). |
| **Entry Points** | `raise RetryExhaustedError(...)`, `raise PlaywrightError(...)`, etc.                               |

**Hierarchie:**

```
MerleError (Basis)
├── RetryExhaustedError
├── CircuitBreakerOpenError
├── PlaywrightError
│   ├── BrowserLaunchError
│   ├── ElementNotFoundError
│   └── ScreenshotFailedError
├── DataProcessingError
│   ├── ExcelError
│   └── PdfError
├── UiPathError
│   └── QueueItemError
├── SecretsError
│   └── SecretNotFoundError
└── BusinessRuleViolation
```

---

## 5. @tag:retry — `retry.py`

**Import:** `from merle_core import with_retry, default_http_retry, browser_retry, ...`

| Aspekt           | Details                                                                                                                          |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Owns**         | Retry-Policies + Decorator-Factory für @tag:retry                                                                                |
| **Invarianten**  | Alle Policies werfen `RetryExhaustedError` wenn alle Versuche fehlschlagen. `with_retry` ist ein Decorator für async-Funktionen. |
| **Entry Points** | `@with_retry(policy=default_http_retry)`, `await retry_with_policy(policy, coro_fn, *args)`                                      |

**Vordefinierte Policies:**

| Policy                      | Versuche | Wartezeit              | Jitter | Für                         |
| --------------------------- | -------- | ---------------------- | ------ | --------------------------- |
| `default_http_retry`        | 3        | exp. Backoff (1s→4s)   | ja     | HTTP-APIs                   |
| `browser_retry`             | 3        | exp. Backoff (2s→8s)   | ja     | Playwright-Aktionen         |
| `sensitive_operation_retry` | 5        | exp. Backoff (2s→16s)  | ja     | Kritische Ops (Payment, DB) |
| `aggressive_retry`          | 5        | exp. Backoff (0.5s→4s) | ja     | Schnelle Recovery           |

---

## 6. HTTP-Client — `http_client.py`

**Import:** `from merle_core import RpaHttpClient`

| Aspekt           | Details                                                                                 |
| ---------------- | --------------------------------------------------------------------------------------- |
| **Owns**         | Async HTTP-Client mit Bearer-Auth, Retry und RPA-User-Agent                             |
| **Invarianten**  | Immer mit `async with` nutzen. Retry ist eingebaut (nicht via `@with_retry`).           |
| **Entry Points** | `async with RpaHttpClient(base_url, bearer_token) as client:` → `await client.get(...)` |

---

## 7. @tag:loguru — `logging_config.py`

**Import:** `from merle_core import setup_logging`

| Aspekt           | Details                                                                  |
| ---------------- | ------------------------------------------------------------------------ |
| **Owns**         | Standardisierte loguru-Konfiguration                                     |
| **Invarianten**  | Ausgabe auf stderr (farbig) + optional JSON-Datei mit Rotation/Retention |
| **Entry Points** | `setup_logging(level="INFO", json_log_file=None)`                        |

---

## 8. @tag:observability — `observability/`

**Import:** `from merle_core import configure_observability, get_tracer, get_meter`

| Aspekt           | Details                                                                                                                                                             |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owns**         | OpenTelemetry-Integration: Tracing (OTLP/gRPC), Metrics (PeriodicExportingMetricReader), loguru-Kontext-Injection                                                   |
| **Invarianten**  | `configure_observability()` ist **idempotent** und **niemals fatal** — selbst bei Fehlkonfiguration crasht der Bot nicht. Traces und Metrics sind immer nur opt-in. |
| **Entry Points** | `configure_observability(service_name="my-bot", otlp_endpoint="localhost:4317")`, `get_tracer()`, `get_meter()`                                                     |
| **Dateien**      | `tracing.py` (TracerProvider + OTLP Exporter), `metrics.py` (MeterProvider + Counter/Histogram), `logging.py` (loguru → OTEL context injection)                     |

---

## 9. @tag:playwright — `playwright/`

**Import:** `from merle_core import launch_robust_browser, RobustBrowser, robust_goto, safe_click, safe_fill`

| Aspekt                  | Details                                                                                                                                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owns**                | Browser-Automatisierung mit **zwei Engines**: Chromium (via Playwright) und @tag:lightpanda (via CDP)                                                                                                   |
| **Invarianten**         | Immer via `async with launch_robust_browser(engine=...) as browser:` nutzen. `RobustBrowser.__aexit__` macht automatisch Screenshot + HTML-Dump bei Fehlern. Stealth-Script wird automatisch injiziert. |
| **Entry Points**        | `launch_robust_browser(engine="chromium", headless=True, screenshot_on_failure=True)`, `robust_goto(page, url)`, `safe_click(page, selector)`, `safe_fill(page, selector, text)`                        |
| **Dateien**             | `browser.py` (Browser-Launch + RobustBrowser Context Manager), `utils.py` (Page-Interaktionen)                                                                                                          |
| **Engine-Unterschiede** | Chromium: voller Funktionsumfang (Screenshots, PDFs). Lightpanda: kein Screenshot/PDF, dafür 10-16× weniger RAM.                                                                                        |

---

## 10. @tag:secrets — `secrets/`

**Import:** `from merle_core import SecretProvider, AzureKeyVaultProvider, AzureKeyVaultSettings`

| Aspekt             | Details                                                                                                                                                                                                                                       |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owns**           | Secret-Provider-Abstraktion + Azure Key Vault Integration + @tag:pydantic-settings Integration                                                                                                                                                |
| **Invarianten**    | `SecretProvider` ist ein ABC mit `get_secret()` und `get_secret_or_default()`. `AzureKeyVaultProvider` lazy-initialisiert den Client. `AzureKeyVaultSettings` ist eine `BaseSettings`-Unterklasse, die fehlende Werte aus Key Vault nachlädt. |
| **Entry Points**   | `provider = AzureKeyVaultProvider(vault_url=...)`, `secret = await provider.get_secret("api-key")`, `class MySettings(AzureKeyVaultSettings)`                                                                                                 |
| **Fallback-Kette** | `.env` → Azure Key Vault → Fehler (nie Hardcode)                                                                                                                                                                                              |
| **Dateien**        | `base.py` (ABC), `azure.py` (Key Vault Impl), `pydantic.py` (Settings-Integration)                                                                                                                                                            |

---

## 11. @tag:nats — `nats/`

**Import:** `from merle_core import NatsClient, NatsMessage, PullConsumer, TaskSpec, TaskResult`

| Aspekt           | Details                                                                                                                                                    |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owns**         | NATS-Client mit Pub/Sub, Request/Reply, JetStream Pull Consumer. Direkt integriert mit @tag:task-spec.                                                     |
| **Invarianten**  | Immer via `async with NatsClient(...) as client:` nutzen. Auto-Reconnect. `publish_task()` / `request_task()` wrappen `TaskSpec` → NATS Message.           |
| **Entry Points** | `nats_client.publish_task(subject, task_spec)`, `result = await nats_client.request_task(subject, task_spec)`, `async for msg in consume_tasks(consumer):` |
| **Status**       | @tag:nats ist PoC (Phase 4). Produktive JetStream-Nutzung geplant.                                                                                         |

---

## 12. Data — `data/`

**Import:** `from merle_core import ExcelReader, ExcelWriter, PdfExtractor, EmailClient`

| Aspekt           | Details                                                                                                                                                    |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owns**         | Excel-I/O (pandas + openpyxl), PDF-Extraktion (pdfplumber), E-Mail (stdlib: IMAP + SMTP)                                                                   |
| **Invarianten**  | Alle Data-Klassen nutzen dynamische Imports. Ohne `pandas` schlägt `ExcelReader` erst bei **Aufruf** fehl, nicht beim Import.                              |
| **Entry Points** | `df = ExcelReader("file.xlsx").read_sheet("Sheet1")`, `text = PdfExtractor.extract_text("file.pdf")`, `EmailClient.download_attachments(imap_server, ...)` |

---

## 13. @tag:uipath-hybrid — `uipath/`

**Import:** `from merle_core import UiPathOrchestratorClient, UiPathQueueHelper`

| Aspekt           | Details                                                                                                                                                                                                            |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Owns**         | UiPath Orchestrator REST-Client (OAuth2 + OData) + Queue-Helper                                                                                                                                                    |
| **Invarianten**  | `authenticate()` muss vor anderen Calls aufgerufen werden. `UiPathQueueHelper` wrappt `UiPathOrchestratorClient`.                                                                                                  |
| **Entry Points** | `client = UiPathOrchestratorClient(base_url, tenant, client_id, client_secret)`, `await client.authenticate()`, `await client.start_job(release_key)`, `await queue.add_queue_item("QueueName", {"key": "value"})` |

---

## Invarianten-Übersicht (Gesamtsystem)

| Invariante                                                 | Scope                       |
| ---------------------------------------------------------- | --------------------------- |
| `execute()` wird nie direkt aufgerufen — immer `run()`     | @tag:basebot, @tag:basetask |
| Alle externen Aufrufe haben Retry — sonst @tag:retry fehlt | @tag:retry                  |
| `configure_observability()` ist idempotent + niemals fatal | @tag:observability          |
| `launch_robust_browser()` immer via `async with`           | @tag:playwright             |
| Secrets: `.env` → Key Vault → Fehler (nie Hardcode)        | @tag:secrets                |
| @tag:optional-imports: Fehlende Extras sind nie fatal      | Gesamtes Paket              |
| Alle Exceptions erben von `MerleError`                     | `exceptions.py`             |
