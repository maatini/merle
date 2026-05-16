# ⚠️ LEGACY – Nicht mehr verwenden (Professional Foundation v0.2+)

**Dieses Verzeichnis (`python_bots/template/`) ist veraltet.**

Die **verbindliche und empfohlene** Methode, neue Merle-Bots zu erstellen, ist seit der Professional Foundation (v0.2):

### Empfohlener Weg (2026+)

```bash
# Mit der offiziellen Merle CLI (beste DX)
merle new-bot mein_bot --playwright --pandas

# Oder direkt mit Copier (die Quelle der Wahrheit)
copier copy templates/bot python_bots/mein_bot
```

Das echte, wartbare Template liegt unter:
- `templates/bot/` (Copier-basiert, mit Feature-Flags, Jinja, Post-Hooks)
- `tools/merle/` (CLI: `merle new-bot`)

---

## Warum dieses alte Template nicht mehr verwendet werden sollte

- Es ist eine statische Kopie und wird nicht mehr gepflegt.
- Es kennt keine Feature-Flags (`--playwright`, `--pandas`, `--pdf`...).
- Es enthält keine modernen Patterns aus `merle-core` (verbessertes `BaseBot`, NATS-Vorbereitung, etc.).
- Docker-Builds und CI sind auf das neue Copier-Template optimiert.

---

## Was tun, wenn du bereits Bots aus diesem Ordner hast?

Kopiere die **Logik** in einen frisch generierten Bot aus `templates/bot/`.

Die alte `cp -r` Methode wird **nicht mehr unterstützt**.

---

**Siehe auch:**
- [Quickstart](../../docs/getting-started/quickstart.md)
- [templates/bot/README.md](../../templates/bot/README.md)
- `merle new-bot --help`

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
