# Bot Template — Copier Code-Generator

**Pfad:** `templates/bot/` | **Engine:** Copier + Jinja2 | **Invocation:** `merle new-bot <name>` oder `copier copy templates/bot/ python_bots/<name>`

Das Bot-Template ist die **alleinige Quelle der Wahrheit** für die Struktur jedes neuen Python-Bots (@tag:copier-template). Es definiert via **14 Jinja2-Dateien** und **1 Copier-Konfiguration**, wie ein generierter Bot aussieht.

## Dateiübersicht

| Datei                         | Typ    | Zweck                                                       |
| ----------------------------- | ------ | ----------------------------------------------------------- |
| `copier.yml`                  | Config | Fragenschema: 10 User-Inputs → Template-Variablen           |
| `README.md`                   | Meta   | Dokumentiert das Template selbst (wird nicht generiert)     |
| `pyproject.toml.jinja`        | Jinja2 | Bot-Manifest mit Feature-Flag-gesteuerten merle-core-Extras |
| `main.py.jinja`               | Jinja2 | Bot-Entry-Point: BaseBot-Subklasse oder einfaches Script    |
| `config.py.jinja`             | Jinja2 | pydantic-settings Config (@tag:pydantic-settings)           |
| `tasks/example_task.py.jinja` | Jinja2 | BaseTask-Beispiel mit @tag:retry                            |
| `Dockerfile.jinja`            | Jinja2 | Multi-Stage-Dockerfile (Monorepo + Standalone)              |
| `.dockerignore.jinja`         | Jinja2 | Dynamisches .dockerignore (monorepo-aware)                  |
| `.dockerignore`               | Static | Fallback für Standalone-Modus                               |
| `README.md.jinja`             | Jinja2 | Bot-README mit Feature-Flag-Badges                          |
| `.env.example`                | Static | Environment-Template für @tag:pydantic-settings             |
| `hooks/post_gen_project.py`   | Hook   | Auto-exec nach Generierung: `uv sync` + `ruff format`       |
| `tasks/__init__.py`           | Static | Package-Init (nur Docstring)                                |
| `tests/__init__.py`           | Static | Package-Init                                                |
| `tests/conftest.py.jinja`     | Jinja2 | Pytest-Fixture für BotSettings                              |
| `tests/test_main.py.jinja`    | Jinja2 | Grundlegende Config-Tests                                   |
| `tests/test_tasks.py.jinja`   | Jinja2 | Async-Test für ExampleTask                                  |

## Feature-Flags

| Flag (copier.yml)             | CLI-Flag                 | Effekt                                                     |
| ----------------------------- | ------------------------ | ---------------------------------------------------------- |
| `include_playwright`          | `--playwright`           | Playwright-Abhängigkeit + Browser-Konfiguration            |
| `browser_engine`              | `--browser-engine`       | `chromium` oder `lightpanda` (nur wenn include_playwright) |
| `include_pandas`              | `--pandas`               | pandas + openpyxl                                          |
| `include_pdf`                 | `--pdf`                  | pdfplumber                                                 |
| `include_uipath_orchestrator` | `--uipath`               | UiPath Orchestrator Client                                 |
| `use_base_bot_class`          | `--basebot/--no-basebot` | BaseBot-Subklasse vs. einfaches Script                     |
| `location`                    | `--location`             | `python_bots` (Monorepo) vs. `standalone`                  |

## Links

- **[`responsibility.md`](./responsibility.md)** — Jedes Template-File: was es generiert, wovon es abhängt
- **[`dependencies.md`](./dependencies.md)** — Feature-Flag → merle-core-Extra Mapping, Monorepo vs. Standalone
- **[`interfaces.md`](./interfaces.md)** — copier.yml Fragenschema, Template-Variablen
- **[`gotchas.md`](./gotchas.md)** — .jinja vs. static Konflikte, Docker COPY-Pfade, uv sources
