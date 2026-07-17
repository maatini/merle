# Datenflüsse

## 1. Bot-Generierung (`merle new-bot`)

```mermaid
sequenceDiagram
    actor Dev as RPA-Entwickler
    participant CLI as Merle CLI
    participant Copier as Copier Engine
    participant Template as templates/bot/
    participant Hook as post_gen_project.py
    participant FS as Dateisystem

    Dev->>CLI: merle new-bot invoice_processor --playwright --pandas
    CLI->>CLI: Validiere Argumente (name, browser_engine)
    CLI->>Copier: run_copy(template_path, target_dir, data=answers, unsafe=True)
    Copier->>Template: Lese copier.yml (Fragen-Schema)
    Copier->>Template: Rendere .jinja → .py/.toml/.dockerfile
    Copier->>FS: Schreibe generierte Dateien nach python_bots/invoice_processor/
    Copier->>Hook: Führe post_gen_project.py aus
    Hook->>FS: uv sync --group dev
    Hook->>FS: ruff format . && ruff check --fix .
    Hook-->>Copier: ✅ Fertig
    Copier-->>CLI: ✅ Erfolg
    CLI-->>Dev: ✅ Bot erstellt! Nächste Schritte: cd python_bots/invoice_processor/
```

**Kritische Annahmen:** `unsafe=True` ist nötig, damit der Post-Generation-Hook läuft. Ohne diesen Flag wird `uv sync` nicht ausgeführt und der Bot ist nicht direkt lauffähig.

## 2. Bot-Ausführung (@tag:basebot Lifecycle)

```mermaid
sequenceDiagram
    participant Main as main.py
    participant Bot as BaseBot
    participant Task as BaseTask
    participant Ext as Externe Systeme

    Main->>Main: configure_observability()
    Main->>Main: setup_logging()
    Main->>Bot: bot = InvoiceBot(settings)
    Main->>Bot: result = await bot.run()

    activate Bot
    Bot->>Bot: start_time = now()
    Bot->>Bot: self.logger.info("Bot starting")
    Bot->>Task: result = await self.execute()

    activate Task
    Task->>Task: self.logger.info("Task starting")
    Task->>Ext: HTTP/Playwright/DB-Aufruf (mit @with_retry)
    Ext-->>Task: Antwort
    Task->>Task: self._on_success(result)
    Task-->>Bot: {"status": "ok", "data": ...}
    deactivate Task

    Bot->>Bot: self.duration = now() - start_time
    Bot->>Bot: self._on_success(result)
    Bot->>Bot: OTEL-Metriken aufzeichnen
    Bot-->>Main: {"status": "ok", "result": ..., "duration": 1.23}
    deactivate Bot

    Main->>Bot: health = bot.health_check()
    Bot-->>Main: {"status": "healthy", "uptime": ...}
```

**Invarianten:**

- `execute()` wird **nie direkt** aufgerufen — immer `run()`, das Timing + Logging + Hooks wrappt
- `_on_success` / `_on_failure` sind Hook-Methoden. Default-Implementierung logged nur.
- OTEL-Metriken werden nur aufgezeichnet, wenn `configure_observability()` vorher aufgerufen wurde

## 3. NATS Task-Kommunikation (@tag:nats, Phase 4 PoC)

```mermaid
sequenceDiagram
    participant Producer as WebScraper Bot
    participant NATS as NATS Server
    participant Consumer as DataProcessor Bot

    Producer->>Producer: Erstelle TaskSpec(task_id, payload)
    Producer->>NATS: nats_client.publish_task("tasks.web_scrape", task_spec)

    NATS->>Consumer: Subscribe "tasks.web_scrape"
    Consumer->>Consumer: task_spec = TaskSpec.from_dict(msg.data)
    Consumer->>Consumer: result = await process(task_spec.payload)
    Consumer->>Consumer: task_result = TaskResult.success(task_spec.task_id, result)
    Consumer->>NATS: nats_client.publish(msg.reply, task_result)

    NATS->>Producer: Reply mit TaskResult
    Producer->>Producer: Verarbeite Ergebnis
```

**Aktueller Status:** PoC in `examples/nats-task-communication/`. Produktive JetStream-Nutzung (persistente Queues, Dead Letter Queue) in Phase 4 geplant (ADR-0006).

## 4. Secrets-Resolution (@tag:secrets)

```mermaid
sequenceDiagram
    participant Bot as Bot/BotSettings
    participant Settings as AzureKeyVaultSettings
    participant KV as Azure Key Vault
    participant Env as .env-Datei

    Bot->>Settings: settings = BotSettings()
    Settings->>Env: Lade .env (pydantic-settings)

    alt Wert in .env gefunden
        Env-->>Settings: BOT_API_KEY=xyz
    else Wert fehlt
        Settings->>KV: get_secret("api-key")
        KV-->>Settings: "xyz"
    end

    Settings-->>Bot: settings.api_key = "xyz"
```

**Fallback-Kette:** `.env` → Azure Key Vault → Fehler (kein Default-Fallback auf Hardcode).
