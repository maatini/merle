# Projektstruktur und Konventionen

## Repository-Struktur

```
.
├── AGENTS.md                          # Persistenter Kontext für AI-Agenten
├── README.md                          # Projekt-Dokumentation
├── docs/                              # Strategie, Governance, Leitfäden
│   ├── concepts/                      # Kernkonzepte (neu strukturierte Dokumentation)
│   │   ├── strategie.md
│   │   ├── entscheidungsmatrix.md
│   │   ├── governance.md
│   │   ├── projektstruktur.md
│   │   └── entwicklungsleitfaden.md
│   ├── decisions/                     # Architecture Decision Records (ADR)
│   ├── merle-core/                    # Dokumentation zum Core-Framework
│   └── development/                   # Contributing & Setup Guides
│       └── .gitkeep
├── python_bots/                       # Python-Bot-Projekte (via merle new-bot)
├── templates/
│   └── bot/                           # ✨ Offizielles Copier-Template (Single Source of Truth)
│       ├── copier.yml
│       └── {{ bot_name }}/...         # Jinja2-Templates + Hooks
│   │       └── test_main.py
│   └── shared/                        # Gemeinsame Utilities
│       ├── __init__.py
│       ├── base_bot.py                # Basisklasse für Bots
│       ├── logging_config.py          # Logging-Konfiguration
│       └── http_client.py             # Vorkonfigurierter HTTP-Client
├── integration_examples/              # Python ↔ UiPath Integrationsmuster
│   ├── orchestrator_api/              # UiPath Orchestrator REST API
│   │   └── example.py
│   ├── python_scope/                  # Python Scope Activity
│   │   └── README.md
│   └── file_based_integration/        # Dateibasierte Integration
│       └── example.py
├── uipath_templates/                  # UiPath-Templates (nur Ausnahmefälle)
│   └── README.md
└── agent/                             # Agent-Konfiguration
    └── CLAUDE.md                      # Zentrale Regeldatei für AI-Agenten
```

## Python-Bot-Struktur (Template-basiert)

Jeder Bot im `python_bots/`-Verzeichnis folgt dieser Struktur:

```
python_bots/<bot_name>/
├── main.py                  # Einstiegspunkt
├── config.py                # Konfiguration (pydantic-settings)
├── models.py                # Datenmodelle (optional)
├── tasks/                   # Geschäftslogik-Module
│   ├── __init__.py
│   └── example_task.py
├── requirements.txt         # Abhängigkeiten
├── Dockerfile               # Container-Definition
├── docker-compose.yml       # Lokale Entwicklungsumgebung (optional)
├── README.md                # Bot-Dokumentation
└── tests/                   # Tests
    ├── __init__.py
    ├── conftest.py           # Fixtures und Mocks
    └── test_main.py
```

## Namenskonventionen

### Python

- **Dateien**: snake_case (`invoice_processor.py`)
- **Klassen**: PascalCase (`InvoiceProcessor`)
- **Funktionen**: snake_case (`process_invoice()`)
- **Konstanten**: UPPER_SNAKE_CASE (`MAX_RETRIES`)
- **Private**: Prefix `_` (`_internal_method()`)

### Verzeichnisse für Bots

- **Bot-Name**: snake_case, beschreibend (`invoice_approval`, `hr_onboarding`)
- **Pattern**: `<domain>_<action>` oder `<domain>_<process>`

## Abhängigkeitsmanagement

### Python

- `requirements.txt` für direkte Abhängigkeiten mit Version-Pinning
- Optional: `pyproject.toml` für moderne Projekte
- Kein pipenv/poetry ohne Absprache (Vereinfachung)

### Version-Pinning-Strategie

```
# requirements.txt
rpaframework>=28.0,<29.0
playwright>=1.40,<2.0
pandas>=2.0,<3.0
pydantic-settings>=2.0,<3.0
loguru>=0.7,<1.0
tenacity>=8.0,<9.0
httpx>=0.25,<1.0
```

## Git-Workflow

### Branch-Strategie

- `main` — Produktionsreife Bots
- `develop` — Integration
- `feature/<bot-name>` — Neue Bots
- `fix/<issue>` — Bugfixes

### Commit-Konventionen

```
feat(bot-name): Kurze Beschreibung
fix(bot-name): Kurze Beschreibung
docs: Dokumentationsänderung
refactor(bot-name): Refactoring-Beschreibung
test(bot-name): Test-Ergänzung
```

## Konfigurationsmanagement

### 12-Factor-App-Prinzipien

1. Konfiguration über Umgebungsvariablen
2. `.env.example` im Repository (ohne Secrets)
3. `.env` in `.gitignore`
4. Keine Konfiguration im Code

### Beispiel `.env.example`

```bash
# Bot: invoice_processor
LOG_LEVEL=INFO
TARGET_URL=https://example.com
MAX_RETRIES=3
TIMEOUT_SECONDS=30
ORCHESTRATOR_API_URL=https://orchestrator.example.com
# ORCHESTRATOR_API_KEY=<secret>
```

## Testing-Konventionen

### Test-Typen

- `tests/unit/` — Isolierte Unit-Tests
- `tests/integration/` — Tests mit externen Abhängigkeiten (gemockt)
- `tests/e2e/` — End-to-End-Tests (mit Playwright)

### Test-Naming

- `test_<was_getestet_wird>.py`
- Test-Funktionen: `test_<funktion>_<szenario>_<erwartung>()`

## Docker-Konventionen

### Dockerfile (Template)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## Revision

| Version | Datum      | Änderung         | Autor                      |
| ------- | ---------- | ---------------- | -------------------------- |
| 1.0     | 2026-05-10 | Initiale Version | Merle RPA-Hybrid-Architekt |
