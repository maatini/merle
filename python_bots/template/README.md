# Bot-Template (Phase 0+)

Dieses Template ist die **verbindliche Basis** für jeden neuen Python-Bot im Merle-Framework.

## Neue Architektur (ab Phase 0)

- **`merle-core`** (Workspace-Package) liefert:
  - `BaseBot` – abstrakte Basisklasse mit standardisiertem Lifecycle
  - `RpaHttpClient` – mit tenacity-Retry & Auth
  - `setup_logging()` – einheitliches loguru-Setup
- Vollständiges **uv**-Management (pyproject.toml + uv.lock)
- Docker-Image mit uv (reproduzierbar, schnell, non-root)

## Verwendung

### 1. Neuen Bot erstellen
```bash
cp -r python_bots/template/ python_bots/mein_invoice_bot/
cd python_bots/mein_invoice_bot/
```

### 2. uv Sync (einmalig)
```bash
uv sync --group dev
```

uv zieht automatisch `merle-core` aus dem Parent-Workspace.

### 3. Konfiguration
```bash
cp .env.example .env
# .env anpassen (niemals committen!)
```

### 4. Bot starten
```bash
uv run python main.py
# oder einfach: uv run main.py
```

### Linting, Format, Type-Check, Test
```bash
uv run ruff check --fix .
uv run ruff format .
uv run mypy .
uv run pytest -v
```

### Docker (empfohlen)
```bash
docker build -t mein-bot .
docker run --env-file .env mein-bot
```

> **Hinweis**: Das neue Dockerfile nutzt uv intern und ist deutlich schneller beim Rebuild als das alte pip-basierte.

## Enthaltene Standards (2026)

- merle-core (BaseBot, RpaHttpClient, einheitliches Logging)
- pydantic-settings (12-Factor Config)
- loguru + tenacity + httpx
- ruff + mypy (strict) + pytest
- uv + Docker (Linux-Container-first)
- .env.example + klare Governance

## Nächste Schritte beim Bot-Bau

1. `config.py` um domänenspezifische Felder erweitern
2. Eigene Tasks unter `tasks/` anlegen (am besten mit `RpaHttpClient` aus merle-core)
3. Optional: eigene Klasse von `BaseBot` ableiten und `execute()` implementieren
4. Tests schreiben
5. ADR bei architekturrelevanten Entscheidungen in `docs/decisions/` anlegen

## Konfiguration

| Variable | Beschreibung | Default |
|----------|-------------|---------|
| `BOT_BOT_NAME` | Name des Bots | `template_bot` |
| `BOT_ENVIRONMENT` | Umgebung | `development` |
| `BOT_LOG_LEVEL` | Log-Level | `INFO` |
| `BOT_LOG_JSON` | JSON-Format-Logging | `false` |
| `BOT_MAX_RETRIES` | Maximale Retries | `3` |
| `BOT_REQUEST_TIMEOUT` | HTTP-Timeout (Sekunden) | `30.0` |
| `BOT_TARGET_URL` | Ziel-URL | `https://example.com/api` |
| `BOT_API_KEY` | API-Key | — |

## Governance
Dieses Template implementiert die Regeln aus:
- `docs/03_Governance.md`
- `docs/05_Entwicklungsleitfaden.md`
