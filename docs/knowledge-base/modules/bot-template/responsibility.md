# Bot Template — Verantwortlichkeiten

Jedes Template-File hat eine klar definierte Verantwortung im Generierungsprozess.

---

## `copier.yml` — Generierungs-Konfiguration

**Owns:** Das Fragenschema, das bestimmt welche Variablen der Nutzer setzen kann und wie sie in Jinja2 verfügbar sind.

| Variable                      | Typ  | Default         | Steuert                                       |
| ----------------------------- | ---- | --------------- | --------------------------------------------- |
| `bot_name`                    | str  | (erforderlich)  | Dateinamen, Klassennamen, Package-Namen       |
| `bot_description`             | str  | `""`            | README, Docstrings                            |
| `python_version`              | str  | `"3.11"`        | `requires-python` in pyproject.toml           |
| `include_playwright`          | bool | `false`         | Playwright-Extra, Browser-Config, Docker-Deps |
| `browser_engine`              | str  | `"chromium"`    | `chromium` vs. `lightpanda` (conditional)     |
| `include_pandas`              | bool | `false`         | pandas + openpyxl Extra                       |
| `include_pdf`                 | bool | `false`         | pdfplumber Extra                              |
| `include_uipath_orchestrator` | bool | `false`         | UiPath Orchestrator Extra + Config            |
| `use_base_bot_class`          | bool | `true`          | BaseBot-Subklasse vs. einfaches Script        |
| `location`                    | str  | `"python_bots"` | Monorepo-Pfad vs. standalone                  |

---

## `pyproject.toml.jinja` — Abhängigkeits-Manifest

**Owns:** Die korrekte merle-core-Extra-Auswahl basierend auf Feature-Flags.

| Feature-Flag(s)                                         | merle-core-Extra                     |
| ------------------------------------------------------- | ------------------------------------ |
| (immer)                                                 | `observability`                      |
| `include_pandas OR include_pdf`                         | `data`                               |
| `include_playwright AND browser_engine == "chromium"`   | `playwright`                         |
| `include_playwright AND browser_engine == "lightpanda"` | `lightpanda`                         |
| `include_uipath_orchestrator`                           | (uipath ist immer in core enthalten) |

**Monorepo vs. Standalone:**

```toml
# location == "python_bots":
[tool.uv.sources]
merle-core = { path = "../../packages/merle-core" }

# location == "standalone":
[tool.uv.sources]
merle-core = ">=0.1.0"    # Von internem PyPI
```

Zusätzlich konfiguriert es ruff, mypy (strict), pytest mit asyncio_mode="auto".

---

## `main.py.jinja` — Bot Entry Point

**Owns:** Das zentrale `async def main()` Pattern — der einzige Weg, einen Bot zu starten.

**Zwei Modi:**

1. **BaseBot-Subklasse** (`use_base_bot_class = true`): Generiert `InvoiceProcessorBot(BaseBot)` mit `execute()`, `_on_success`, `_on_failure`
2. **Einfaches Script** (`use_base_bot_class = false`): `async def main()` ohne BaseBot, nur `setup_logging()`

**Immer enthalten:**

- `configure_observability()` — @tag:observability (safe, crasht nie)
- `setup_logging()` — @tag:loguru
- `asyncio.run(main())`

---

## `config.py.jinja` — BotSettings

**Owns:** @tag:pydantic-settings Konfiguration mit `env_prefix="BOT_"` und `.env`-Loading.

**Conditional Fields:**

- Playwright: `browser_engine`, `lightpanda_host`, `lightpanda_port`, `lightpanda_log_level`
- UiPath: `orchestrator_url`, `orchestrator_tenant`, `orchestrator_client_id`, `orchestrator_client_secret`

---

## `tasks/example_task.py.jinja` — Task-Muster

**Owns:** Das empfohlene @tag:basetask Pattern mit @tag:retry via `@with_retry`.

```python
class ExampleTask(BaseTask):
    def __init__(self, settings: BotSettings):
        super().__init__(settings, name="ExampleTask")

    @with_retry(policy=default_http_retry)
    async def _do_work(self) -> dict: ...

    async def execute(self) -> dict:
        return await self._do_work()
```

---

## `Dockerfile.jinja` — Docker-Build

**Owns:** Multi-Stage Dockerfile mit zwei Build-Modi (Monorepo vs. Standalone), gesteuert via `BUILD_MODE` ARG.

**Stages:**

1. **Builder**: `uv` (von `ghcr.io/astral-sh/uv:0.11`), installiert Dependencies mit `--no-dev`
2. **Runtime**: Non-root `bot`-User (UID 1000), kopiert `.venv`, HEALTHCHECK

**Browser-Dependencies (conditional):**

- Chromium-Modus: Schwere System-Deps (libnss3, libgbm, etc.)
- Lightpanda-Modus: Nur `ca-certificates curl`

---

## `hooks/post_gen_project.py` — Post-Generation

**Owns:** Automatisches Setup nach der Generierung. Läuft **nur** wenn Copier mit `unsafe=True` aufgerufen wird.

**Ablauf:**

1. `uv sync --group dev` — Installiert alle Dependencies inkl. merle-core
2. `ruff format .` — Formatiert generierten Code
3. `ruff check --fix .` — Lintet + Auto-Fix
4. Print-Success-Banner mit nächsten Schritten

---

## Test-Dateien (`tests/`)

| Datei                 | Zweck                                                               |
| --------------------- | ------------------------------------------------------------------- |
| `conftest.py.jinja`   | `settings` Fixture mit Test-Defaults                                |
| `test_main.py.jinja`  | Validiert BotSettings (name, environment)                           |
| `test_tasks.py.jinja` | Async-Test: `ExampleTask.run()` → assert `result["status"] == "ok"` |

---

## Was das Template **nicht** besitzt

- **Keine** Geschäftslogik — nur generische Struktur
- **Keine** produktiven Secrets oder URLs — nur `.env.example`
- **Keine** eigenen Dependencies außer merle-core — keine direkten `loguru`/`tenacity` Imports (kommen via merle-core)
