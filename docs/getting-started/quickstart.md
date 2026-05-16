# Schnellstart

## 1. Voraussetzungen

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (empfohlen) oder pip

## 2. Neuen Bot erstellen

### Variante A – Mit der merle CLI (empfohlen)

```bash
merle new-bot rechnungsverarbeitung --playwright --pandas
cd python_bots/rechnungsverarbeitung
```

### Variante B – Mit Copier

```bash
copier copy templates/bot python_bots/rechnungsverarbeitung
cd python_bots/rechnungsverarbeitung
```

## 3. Abhängigkeiten installieren

```bash
uv sync --group dev
```

## 4. Bot starten

```bash
uv run python main.py
```

## 5. Tests ausführen

```bash
uv run pytest -v
```

## Nächste Schritte

- `config.py` anpassen
- Eigene Tasks unter `tasks/` anlegen (von `BaseTask` erben)
- `configure_observability()` in `main.py` aktivieren
- `.env` mit echten Werten befüllen (niemals committen!)