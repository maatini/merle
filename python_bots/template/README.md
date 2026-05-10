# Bot-Template

## Zweck
Dieses Template ist die **verbindliche Basis** für jeden neuen Python-Bot im hybriden RPA-Development-Kit.

## Enthaltene Standards
- ✅ **loguru** für strukturiertes Logging (mit JSON-Support für Produktion)
- ✅ **tenacity** für Retry-Mechanismen mit exponentiellem Backoff
- ✅ **pydantic-settings** für typsichere Konfiguration aus Umgebungsvariablen
- ✅ **httpx** als async HTTP-Client
- ✅ **pytest** für Testing
- ✅ **Docker** für Container-Deployment
- ✅ **Prefect-kompatibel** für Orchestrierung

## Verwendung

### Neuen Bot erstellen
```bash
cp -r python_bots/template/ python_bots/mein_bot/
cd python_bots/mein_bot/
```

### Konfiguration anpassen
1. `config.py` um projektspezifische Felder erweitern
2. `.env`-Datei mit Werten füllen (niemals committen!)

### Entwicklung
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Tests
```bash
pytest tests/ -v
```

### Docker
```bash
docker build -t bot-template .
docker run --env-file .env bot-template
```

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
