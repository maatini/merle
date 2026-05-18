# Entwicklungsleitfaden für Bot-Entwicklung

## Ziel

Dieser Leitfaden beschreibt den vollständigen Prozess zur Entwicklung eines neuen Python-Bots im Merle-Framework — von der ersten Idee bis zum produktiven Einsatz in Azure AKS.

## Merle Bot Lifecycle – Der gesamte Weg auf einen Blick

![Merle Bot Lifecycle – von der Idee bis zum produktiven Bot](assets/images/onboarding/merle-bot-lifecycle.jpg)

---

## Phase 1: Anforderungsanalyse und Technologieentscheidung

### Schritt 1: Prozess verstehen

1. Prozessbeschreibung vom Fachbereich einholen
2. Input-/Output-Daten identifizieren
3. Systeme und Schnittstellen auflisten
4. Häufigkeit und Volumen bestimmen
5. Fehlertoleranz und SLAs klären

### Schritt 2: Technologieentscheidung treffen

1. Entscheidungsmatrix (`entscheidungsmatrix.md`) anwenden
2. Bei Python-Domäne: Direkt zu Phase 2
3. Bei unklarem Fall: Scoring-Modell anwenden
4. Bei UiPath-Erwägung: Prototyp bauen und vergleichen
5. Entscheidung dokumentieren (ADR in `docs/decisions/`)

---

## Phase 2: Bot-Gerüst aufsetzen

### Schritt 1: Bot mit Copier erzeugen (empfohlen)

```bash
# Mit der Merle CLI (beste DX)
merle new-bot <bot_name> --playwright --pandas

# Lightpanda (Zig-basiert, extrem ressourcenschonend)
merle new-bot high_volume_scraper --playwright --lightpanda
# oder: --browser-engine lightpanda

# Oder direkt mit Copier
copier copy templates/bot python_bots/<bot_name>
cd python_bots/<bot_name>
uv sync --group dev
```

> **Hinweis**: Das alte `cp -r python_bots/template/` wurde mit PR 1 (2026-05) entfernt. Neue Bots immer via `merle new-bot` / Copier.

> **Browser-Engine (seit 2026-05)**: Bei `--playwright` kannst du mit `--browser-engine lightpanda` die Zig-basierte Lightpanda-Engine wählen (10–16× weniger RAM, 5–11× schneller). Default bleibt `chromium` für maximale Kompatibilität + Screenshot/PDF-Fähigkeit. Siehe ADR-0007.

### Schritt 2: Konfiguration anpassen

1. `config.py`: Settings-Klasse mit projektspezifischen Feldern
2. `.env.example`: Alle Konfigurationsvariablen dokumentieren
3. `.env`: Lokale Entwicklungskonfiguration (in .gitignore)

### Schritt 3: Abhängigkeiten definieren

1. `pyproject.toml`: Nur benötigte Pakete (via `uv add`)
2. Version-Pinning nach Konvention (siehe `projektstruktur.md`)

---

## Phase 3: Implementierung

### Reihenfolge

1. **Datenmodelle** (`models.py`) — Pydantic-Modelle für Input/Output
2. **Konfiguration** (`config.py`) — Vollständige Settings
3. **Geschäftslogik** (`tasks/`) — In fokussierte Module aufteilen
4. **Orchestrierung** (`main.py`) — Workflow, Error-Handling, Logging

### Coding-Standards

#### Logging (loguru)

```python
from loguru import logger

logger.info("Starte Rechnungsverarbeitung für {}", invoice_id)
logger.error("Fehler bei API-Aufruf: {}", error)
```

#### Retry (tenacity)

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def call_external_api(url: str) -> dict:
    ...
```

#### Konfiguration (pydantic-settings)

```python
from pydantic_settings import BaseSettings

class BotSettings(BaseSettings):
    target_url: str
    api_key: str
    max_retries: int = 3

    model_config = SettingsConfigDict(env_prefix="BOT_")
```

#### HTTP-Client (httpx, async-first)

```python
import httpx

async with httpx.AsyncClient(timeout=30.0) as client:
    response = await client.get(url, headers={"Authorization": f"Bearer {token}"})
    response.raise_for_status()
    return response.json()
```

---

## Phase 4: Testing

### Unit-Tests

```python
# tests/test_main.py
import pytest
from main import process_data

def test_process_data_valid_input():
    result = process_data({"id": 1, "value": "test"})
    assert result["status"] == "processed"

def test_process_data_missing_field():
    with pytest.raises(ValueError):
        process_data({"id": 1})  # Fehlendes 'value'-Feld
```

### Integration-Tests mit Mocks

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_api_integration():
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value.json = AsyncMock(return_value={"status": "ok"})
        result = await fetch_data("https://api.example.com")
        assert result["status"] == "ok"
```

### Playwright E2E-Tests

```python
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_login_flow():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com/login")
        # ... Test-Logik
```

---

## Phase 5: Docker und CI/CD

### Docker-Build lokal testen

```bash
docker build -t bot-name .
docker run --env-file .env bot-name
```

### CI/CD-Pipeline (GitHub Actions Beispiel)

```yaml
name: Bot CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
  docker:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t bot-name .
      - run: docker run --rm bot-name python -c "print('Smoke test OK')"
```

---

## Phase 6: Dokumentation und Übergabe

### README.md Template

````markdown
# <Bot-Name>

## Zweck

Kurze Beschreibung, was der Bot macht.

## Konfiguration

| Variable         | Beschreibung | Default |
| ---------------- | ------------ | ------- |
| `BOT_TARGET_URL` | Ziel-URL     | —       |
| `BOT_API_KEY`    | API-Key      | —       |
| `LOG_LEVEL`      | Log-Level    | `INFO`  |

## Entwicklung

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
````

## Docker

```bash
docker build -t bot-name .
docker run --env-file .env bot-name
```

## Betrieb

- **Frequenz**: Stündlich
- **Erwartete Laufzeit**: < 5 Minuten
- **Fehlerbehandlung**: 3 Retries, dann Alert

```

---

## Checkliste für Bot-Fertigstellung

- [ ] Technologieentscheidung dokumentiert
- [ ] Template-Struktur vorhanden
- [ ] Konfiguration über pydantic-settings
- [ ] loguru-Logging konfiguriert
- [ ] tenacity-Retries für externe Aufrufe
- [ ] Unit-Tests für Business-Logik
- [ ] Integration-Tests für kritische Pfade
- [ ] Dockerfile baubar
- [ ] README.md vollständig
- [ ] .env.example mit allen Variablen
- [ ] Code-Review durchgeführt
- [ ] CI/CD-Pipeline eingerichtet
- [ ] Keine hartcodierten Werte
- [ ] Keine Windows-only-Abhängigkeiten

---

## Revision

| Version | Datum | Änderung | Autor |
|---------|-------|----------|-------|
| 1.0 | 2026-05-10 | Initiale Version | Merle RPA-Hybrid-Architekt |
```
