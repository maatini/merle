# merle-core — Gotchas & Pitfalls

Diese Seite sammelt bekannte Fallstricke, Edge Cases und Dinge, die man "einfach wissen muss", wenn man mit `merle_core` arbeitet.

---

## @tag:optional-imports: Module fehlen still

**Problem:** `from merle_core import launch_robust_browser` schlägt **nicht** fehl, wenn Playwright nicht installiert ist — es ist einfach `None`.

```python
# Das geht immer, auch ohne Playwright:
from merle_core import launch_robust_browser

# Aber das crasht zur Laufzeit:
browser = await launch_robust_browser()  # NameError, wenn Optional-Extra fehlt!
```

**Lösung:** Entweder das passende Extra installieren (`uv add "merle-core[playwright]"`) oder vor der Nutzung prüfen:

```python
from merle_core import launch_robust_browser
if launch_robust_browser is None:
    raise RuntimeError("merle-core[playwright] nicht installiert")
```

---

## @tag:basebot: `execute()` vs `run()`

**Falle:** `execute()` direkt aufzurufen umgeht das gesamte Lifecycle-Management.

```python
# ❌ Falsch — keine Zeitmessung, kein Logging, keine Hooks, keine OTEL-Metriken
result = await bot.execute()

# ✅ Richtig
result = await bot.run()
```

Gleiches gilt für `BaseTask`. Der Lifecycle (`run()`) ist der einzige Entry Point für die Ausführung.

---

## @tag:observability: OTEL Collector muss laufen

**Problem:** `configure_observability()` versucht standardmäßig, zu `localhost:4317` (OTLP/gRPC) zu verbinden. Wenn dort kein Collector läuft, **verliert der Bot keine Daten** — aber Traces und Metriken gehen ins Leere.

**Lösung:** Für lokale Entwicklung fällt `init_tracing()` auf `ConsoleSpanExporter` zurück. Für Produktion muss ein OTEL Collector (z.B. via Docker) auf dem konfigurierten Endpoint laufen.

```bash
# Lokaler OTEL Collector für Entwicklung:
docker run -p 4317:4317 otel/opentelemetry-collector
```

---

## @tag:playwright: Engine-Unterschiede Chromium vs Lightpanda

| Feature                 | Chromium | @tag:lightpanda    |
| ----------------------- | -------- | ------------------ |
| Screenshots             | ✅       | ❌                 |
| PDF-Generierung         | ✅       | ❌                 |
| JavaScript              | ✅       | ✅ (eingeschränkt) |
| RAM-Verbrauch           | ~500 MB  | ~30-50 MB          |
| CDP-Protokoll           | ✅       | ✅                 |
| `screenshot_on_failure` | ✅       | ❌ (ignored)       |

**Falle:** `launch_robust_browser(engine="lightpanda", screenshot_on_failure=True)` erzeugt **keine** Screenshots bei Fehlern. Die Option wird still ignoriert.

---

## @tag:playwright: Lightpanda benötigt separaten Prozess

**Problem:** Im Gegensatz zu Chromium (das Playwright automatisch managed) muss Lightpanda **vorher** als separater Prozess gestartet sein:

```bash
# Lightpanda muss auf localhost:9222 laufen, bevor der Bot startet
lightpanda --port 9222
```

Der `launch_robust_browser(engine="lightpanda")` Context Manager verbindet sich via CDP, startet den Prozess aber nicht selbst.

---

## @tag:secrets: AzureKeyVaultSettings erfordert async-Initialisierung

**Problem:** `AzureKeyVaultSettings` kann nicht einfach `Settings()` erstellt werden, wenn Key Vault Secrets involviert sind.

```python
# ❌ Funktioniert nicht für Key Vault Secrets (kein async in __init__):
settings = BotSettings()

# ✅ Richtig:
settings = await BotSettings.from_keyvault(vault_url="https://my-vault.vault.azure.net")
```

Der Grund: `BaseSettings.__init__()` ist synchron, aber `get_secret()` ist async. Die `from_keyvault()`-Factory löst dieses Problem.

---

## @tag:nats: NATS-Server muss laufen

**Problem:** `NatsClient` verbindet sich zu `nats://localhost:4222`. Ohne laufenden NATS-Server crasht der `async with`-Block.

```bash
# Vor der Nutzung:
docker run -d -p 4222:4222 nats:latest
```

**Status:** @tag:nats ist derzeit PoC (Phase 4). Keine produktiven Bots sollten aktuell davon abhängen.

---

## @tag:retry: `with_retry` nur für async-Methoden

**Problem:** `@with_retry` funktioniert nur auf `async def`-Methoden. Für synchrone Funktionen oder manuelle Aufrufe:

```python
# ❌ Falsch:
@with_retry(policy=default_http_retry)
def sync_function(): ...  # Wird nicht funktionieren

# ✅ Richtig:
result = await retry_with_policy(default_http_retry, some_async_func, arg1, arg2)
```

---

## Loguru: `setup_logging()` ist nicht idempotent

**Problem:** Zweimaliges Aufrufen von `setup_logging()` fügt doppelte Handler hinzu, was zu duplizierten Log-Einträgen führt.

```python
# ❌ Falsch:
setup_logging(level="DEBUG")  # Erster Handler
setup_logging(json_log_file="bot.log")  # Zweiter Handler → doppelte Logs!

# ✅ Richtig: Alle Optionen auf einmal setzen
setup_logging(level="DEBUG", json_log_file="bot.log")
```

Im Gegensatz dazu ist `configure_observability()` idempotent.

---

## OTEL-Metriken: `create_bot_metrics()` wird pro Klasse aufgerufen

**Problem:** In `base_bot.py` und `base_task.py` wird `create_bot_metrics()` auf **Modulebene** aufgerufen. Das erzeugt die Counter/Histogram **einmal** beim Import — aber nur wenn `observability` installiert ist.

Wenn `observability` **nach** dem ersten Import installiert wird, fehlen die Metriken. Ein Neustart des Python-Prozesses ist nötig.
