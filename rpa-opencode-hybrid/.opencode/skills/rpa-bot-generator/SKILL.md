# RPA Bot Generator

## Purpose
Generiert einen neuen Python-Bot **strikt nach dem Template** und allen Qualitätsregeln
des RPA Hybrid Development Kit.

## When to Use
- Wenn die Technologieentscheidung auf **Python** gefallen ist
- Nach der Prozessanalyse (via `rpa-process-analyzer`)
- Immer wenn ein neuer Bot erstellt werden soll

## Process

### 1. Voraussetzungen prüfen
- Technologieentscheidung ist dokumentiert?
- Bot-Name folgt der Konvention (`<domain>_<action>`)?
- Zielverzeichnis `python_bots/<bot_name>/` existiert noch nicht?

### 2. Template klonen
```bash
cp -r python_bots/template/ python_bots/<bot_name>/
```

### 3. Anpassungen vornehmen (in dieser Reihenfolge)

#### 3.1 config.py anpassen
- `bot_name`: Auf tatsächlichen Bot-Namen setzen
- Projektspezifische Settings-Felder hinzufügen (target_url, api_key, etc.)
- UiPath-Orchestrator-Felder nur wenn nötig
- `env_prefix` beibehalten (immer `BOT_`)

```python
class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BOT_", ...)

    bot_name: str = "invoice_processor"
    # Projektspezifische Felder:
    sap_fiori_url: str = ""
    output_dir: str = "/app/output"
```

#### 3.2 requirements.txt anpassen
- Nur tatsächlich benötigte Pakete
- Version-Pinning beibehalten (`>=X,<Y`)

#### 3.3 tasks/ erstellen
- `example_task.py` umbenennen/löschen
- Neue Task-Module pro Prozessschritt:
  - Eine Klasse pro Task
  - `async def run(self) -> dict` als Entry Point
  - Konfiguration via Constructor Injection
  - loguru-Logging mit `logger.bind(task="TaskName")`
  - tenacity-Retry für externe Aufrufe

```python
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

class InvoiceFetchTask:
    def __init__(self, settings):
        self.settings = settings
        self.logger = logger.bind(task="InvoiceFetch")

    async def run(self) -> dict:
        self.logger.info("Starte Rechnungsabruf")
        data = await self._fetch_from_sap()
        return {"count": len(data), "invoices": data}

    @retry(stop=stop_after_attempt(3),
           wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _fetch_from_sap(self) -> list[dict]:
        ...
```

#### 3.4 models.py erstellen (wenn nötig)
- Pydantic-Modelle für Input/Output-Daten

```python
from pydantic import BaseModel

class Invoice(BaseModel):
    id: str
    amount: float
    vendor: str
    status: str = "pending"
```

#### 3.5 main.py anpassen
- Tasks importieren und orchestrieren
- Workflow-Logik: Welche Tasks in welcher Reihenfolge?
- Fehlerbehandlung auf Top-Level
- Logging-Setup beibehalten

```python
async def main():
    settings = BotSettings()
    setup_logging(settings)
    logger.info("Bot {} startet", settings.bot_name)

    try:
        fetch_task = InvoiceFetchTask(settings)
        invoices = await fetch_task.run()

        process_task = InvoiceProcessTask(settings)
        result = await process_task.run(invoices["invoices"])

        logger.info("Bot erfolgreich: {} Rechnungen verarbeitet", result["processed"])
    except Exception:
        logger.exception("Kritischer Fehler")
        raise
```

#### 3.6 Tests schreiben
- `conftest.py`: Settings-Fixture anpassen
- `test_main.py`: Tests für die neuen Tasks
- Mock externe Abhängigkeiten (HTTP, DB)
- Business-Logik ohne Mocks testen

#### 3.7 .env.example aktualisieren
- Alle neuen Konfigurationsvariablen dokumentieren
- Beispielwerte (keine echten Secrets)

#### 3.8 Dockerfile prüfen
- Zusätzliche System-Abhängigkeiten?
- Playwright-Browser nötig?
- User-Kontext korrekt (nicht root)?

#### 3.9 README.md schreiben
```markdown
# <Bot-Name>

## Zweck
[Was macht der Bot? Welches Problem löst er?]

## Prozess
1. [Schritt 1]
2. [Schritt 2]
3. [Schritt 3]

## Konfiguration
| Variable | Beschreibung | Default |
|----------|-------------|---------|
| ... | ... | ... |

## Entwicklung
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Docker
```bash
docker build -t <bot-name> .
docker run --env-file .env <bot-name>
```

## Betrieb
- **Frequenz**: [Stündlich/Täglich/Wöchentlich]
- **Erwartete Laufzeit**: [X Minuten]
- **Fehlerbehandlung**: 3 Retries, dann Alert
```

### 4. Qualitäts-Checkliste (vor Abschluss)
- [ ] Template-Struktur vollständig (main.py, config.py, tasks/, tests/, Dockerfile, README.md)
- [ ] config.py mit pydantic-settings und env_prefix `BOT_`
- [ ] loguru-Logging in allen Modulen
- [ ] tenacity-Retry für externe Aufrufe
- [ ] Unit-Tests für Business-Logik
- [ ] Keine hartcodierten Werte
- [ ] Keine Windows-only-Abhängigkeiten
- [ ] Dockerfile baubar (Docker-spezifische Pfade)
- [ ] .env.example vollständig
- [ ] README.md mit Zweck, Konfiguration, Betrieb

## Hard Constraints
- NIE ein Template-Feld löschen, nur anpassen
- NIE Config-Werte hartcodieren
- NIE print() statt loguru verwenden
- NIE try/except ohne Logging
- IMMER async/await verwenden
- IMMER Type-Hints

## References
- `python_bots/template/` — Das Basis-Template
- `docs/05_Entwicklungsleitfaden.md` — Vollständiger Entwicklungsleitfaden
- `docs/04_Projektstruktur.md` — Konventionen
- `docs/03_Governance.md` — Governance-Regeln
