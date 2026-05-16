# Entwicklungsumgebung einrichten

## Voraussetzungen

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (empfohlen)
- Git

## Einrichtung

```bash
# Repository klonen
git clone https://github.com/maatini/merle.git
cd merle

# Merle CLI installieren (für Bot-Generierung)
uv pip install -e tools/merle

# Abhängigkeiten für shared/merle-core
cd python_bots/shared
uv sync --group dev
```

## Wichtige Befehle

```bash
# Neuen Bot erzeugen
merle new-bot mein_bot --playwright --pandas

# Tests ausführen
uv run pytest

# Docs lokal bauen
uv run --with mkdocs-material mkdocs serve
```

## OpenCode (empfohlen)

Einfach `opencode` im Merle-Root starten — der **RPA-Hybrid-Architekt** ist automatisch aktiv.

---

**Nächster Schritt**: Lies den [Schnellstart](../getting-started/quickstart.md).