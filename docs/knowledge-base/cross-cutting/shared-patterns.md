# Shared Patterns

Diese Patterns tauchen modulübergreifend auf. Jeder Bot und jedes Template folgt ihnen.

---

## 1. Bot-Lifecycle (@tag:basebot + @tag:basetask)

**Pattern:** Jede Ausführung folgt einem standardisierten Lifecycle: `run()` → `execute()` → Hooks → Health-Check.

```python
# 1. Bot definieren
class MyBot(BaseBot):
    def __init__(self, settings):
        super().__init__(settings, name="my_bot")

    async def execute(self) -> dict:
        # 2. Tasks orchestrieren
        task = MyTask(self.settings)
        return await task.run()

    def _on_success(self, result):
        self.logger.info("✅ Erfolg")

    def _on_failure(self, exception):
        self.logger.error(f"❌ {exception}")

# 3. Starten
async def main():
    configure_observability(service_name="my-bot")
    setup_logging(level="INFO")
    bot = MyBot(settings)
    result = await bot.run()           # run() wrappt execute()
    health = await bot.health_check()  # Post-Mortem

asyncio.run(main())
```

**Invarianten:**

- `execute()` wird **nie direkt** aufgerufen
- `run()` misst Dauer, loggt, feuert Hooks, zeichnet OTEL-Metriken auf
- Jeder Bot endet mit `health_check()`

---

## 2. Config Pattern (@tag:pydantic-settings)

**Pattern:** Alle Konfiguration via `pydantic-settings.BaseSettings` mit `.env`-Fallback, `env_prefix` und strenger Validation.

```python
from pydantic_settings import BaseSettings

class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="BOT_",
        extra="ignore",
    )

    bot_name: str = "my_bot"
    environment: str = "development"
    log_level: str = "INFO"
    max_retries: int = 3
    target_url: str
    api_key: str
```

**Invarianten:**

- Keine hartcodierten Credentials, URLs, Pfade
- `.env`-Datei ist nicht versioniert (`.gitignore`)
- `.env.example` ist versioniert (zeigt Struktur ohne Secrets)

---

## 3. Retry-Pattern (@tag:retry)

**Pattern:** Jeder externe Aufruf (HTTP, Browser, DB) bekommt `@with_retry` mit passender Policy.

```python
from merle_core import with_retry, default_http_retry, sensitive_operation_retry

class FetchDataTask(BaseTask):
    @with_retry(policy=default_http_retry)      # HTTP: 3 Versuche, 1s→4s Backoff
    async def fetch_api(self) -> dict: ...

    @with_retry(policy=sensitive_operation_retry) # Kritisch: 5 Versuche, 2s→16s
    async def process_payment(self) -> dict: ...
```

**Policy-Auswahl:**
| Externes System | Policy |
|----------------|--------|
| HTTP-APIs | `default_http_retry` |
| Browser-Aktionen | `browser_retry` |
| Payment, DB-Writes | `sensitive_operation_retry` |
| Schnelle Recovery (Cache) | `aggressive_retry` |

---

## 4. Observability Pattern (@tag:observability)

**Pattern:** `configure_observability()` einmal am Anfang — dann automatisches Tracing für HTTP, Playwright, und Tasks.

```python
from merle_core import configure_observability

async def main():
    configure_observability(
        service_name="my-bot",
        otlp_endpoint="localhost:4317",   # OTEL Collector
    )
    # Ab hier: alle BaseBot/BaseTask.run()-Aufrufe sind getraced
    # HTTP-Calls via RpaHttpClient sind getraced (wenn OTEL-instrumentiert)
```

**Invarianten:**

- `configure_observability()` ist **idempotent** — mehrfacher Aufruf harmlos
- **Niemals fatal** — Bot crasht nicht, wenn Collector nicht erreichbar
- Immer **vor** `bot.run()` aufrufen

---

## 5. Task-Decomposition Pattern

**Pattern:** Komplexe Bots werden in feingranulare, unabhängige `BaseTask`-Einheiten zerlegt. Der `BaseBot` orchestriert die Pipeline.

```python
class InvoiceBot(BaseBot):
    async def execute(self) -> dict:
        # 1. Download
        downloader = DownloadInvoicesTask(self.settings)
        invoices = await downloader.run()

        # 2. Parse
        parser = ParseInvoicesTask(self.settings)
        parsed = await parser.run(invoices["data"])

        # 3. Report
        reporter = WriteReportTask(self.settings)
        return await reporter.run(parsed["data"])
```

Jeder Task ist eine eigene Klasse mit:

- Eigenem `execute()`
- Eigenen `_on_success` / `_on_failure` Hooks
- Eigenem `@with_retry`
- Eigenem Logging (via `self.logger`)

**Vorteil:** Testbarkeit. Jeder Task kann einzeln mit Mock-Settings getestet werden.
